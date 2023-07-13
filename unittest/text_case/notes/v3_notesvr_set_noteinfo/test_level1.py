import time
import unittest  # 导入数据库
import requests
from common.check_commne import CheckCommon  # 载入一个类
import parameterized  # 参数化使用库
import inspect
from common.ReadYaml import ReadYaml
from business.apicommon import ApiCommon
from common.customsLog import info_log, error_log, warn_log, class_case_log
from business.apicommon import note_info, note_info_delete, note_info_look
from colorama import Fore

readYaml = ReadYaml
env_config = readYaml.common_yaml()
host = env_config['host']  # 属于环境变量，跟随测试环境变更，请求体和路径不随环境改变而改变，所以不属于环境变量
wps_sid = env_config['wps_sid']  # 属于环境变量，跟随测试环境变更
x_user_key = env_config['x_user_key']  # 属于环境变量，跟随测试环境变更
path = '/v3/notesvr/set/noteinfo'
url = host + path
apicommon = ApiCommon()
readYaml = ReadYaml
api_data = readYaml.api_yaml('notes/test_noteinfo')
checkCommon = CheckCommon()  # 以小驼峰将类进行实例化,括号要记得加才是实例化


@class_case_log
class NoteContentLevel1(unittest.TestCase):  # 改成接口名字+重要级别
    host = env_config['host']  # 属于环境变量，跟随测试环境变更，请求体和路径不随环境改变而改变，所以不属于环境变量
    wps_sid = env_config['wps_sid']  # 属于环境变量，跟随测试环境变更
    x_user_key = env_config['x_user_key']  # 属于环境变量，跟随测试环境变更

    def setUp(self):
        print(Fore.LIGHTCYAN_EX + '----------------------------清空首页环境---------------------------')
        note_info_delete()

    def testCase_major(self):  # 会按序号去执行。
        """创建便签信息内容主流程,校验点①协议规范②接口返回③数据查询④默认内容确认"""
        info_log('step1 新建信息主体和内容')
        note_id = str(int((time.time()) * 1000)) + 'note_id'
        body_note_info = {'noteId': note_id}
        body_note_content = {
            'noteId': note_id,
            'title': str(int((time.time()) * 1000)) + 'title',
            'summary': str(int((time.time()) * 1000)) + 'summary',
            'body': str(int((time.time()) * 1000)) + 'body',
            'BodyType': 0,
            'localContentVersion': 1
        }
        Ap = apicommon.post(url=host + path, sid=env_config['wps_sid'], body=body_note_info,
                            user_id=env_config['x_user_key'])
        apicommon.post(url=host + '/v3/notesvr/set/notecontent', sid=env_config['wps_sid'], body=body_note_content,
                       user_id=env_config['x_user_key'])
        self.assertEqual(200, Ap.status_code, msg="状态码校验失败")
        response = Ap.json()
        check_items = {'responseTime': 1, 'infoVersion': 1, 'infoUpdateTime': 1}
        checkCommon.check_response_len_type_key(check_items=check_items, response=response)
        info_log('step2 获取新建便签内容')
        get_path = '/v3/notesvr/get/notebody'  # 查询接口
        get_url = self.host + get_path
        get_body = {'noteIds': [note_id]}  # 注意字典包id，否则传参失败
        get_res = apicommon.post(url=get_url, body=get_body, user_id=self.x_user_key,
                                 sid=self.wps_sid)  # 通过查询接口查询内容
        self.assertEqual(200, get_res.status_code, 'noteIds新建失败')  # 先保证查询能查到，就代表新建成功。
        info_log('step2 获取新建便签信息主体进行比较默认项')
        note_look = note_info_look()
        self.assertTrue(note_look.json()["webNotes"][0]["star"] == 0)
        self.assertTrue(note_look.json()["webNotes"][0]["remindTime"] == 0)
        self.assertTrue(note_look.json()["webNotes"][0]["groupId"] == None)

    def testCase_major2(self):  # 会按序号去执行。
        """创建便签信息更新主流程,校验点①内容确认"""
        info_log('step1 新建信息主体和内容')
        note_id = str(int((time.time()) * 1000)) + 'note_id'
        body_note_info = {'noteId': note_id, 'remindTime': 1115555}
        body_note_content = {
            'noteId': note_id,
            'title': str(int((time.time()) * 1000)) + 'title',
            'summary': str(int((time.time()) * 1000)) + 'summary',
            'body': str(int((time.time()) * 1000)) + 'body',
            'BodyType': 0,
            'localContentVersion': 1
        }
        apicommon.post(url=host + path, sid=env_config['wps_sid'], body=body_note_info,
                       user_id=env_config['x_user_key'])
        apicommon.post(url=host + '/v3/notesvr/set/notecontent', sid=env_config['wps_sid'], body=body_note_content,
                       user_id=env_config['x_user_key'])
        info_log('step2 新建信息主体更改为标星')
        body_update = {'noteId': note_id, 'star': 1}
        apicommon.post(url=host + path, sid=env_config['wps_sid'], body=body_update,
                       user_id=env_config['x_user_key'])
        info_log('step3 获取新建便签信息主体进行比较')
        note_look = note_info_look()
        if note_look.json()["webNotes"][0]['noteId'] == note_id:
            self.assertTrue(note_look.json()["webNotes"][0]["star"] == 1)
        else:
            error_log('更新失败')
            raise ValueError

    def testCase02_handle(self):
        """###检测其他用户的NoteID能否修改必填项校验①规范校验②修改内容校验###"""
        info_log('step1 新建信息主体和内容')
        note_id = str(int((time.time()) * 1000)) + 'note_id'
        body_note_info = {'noteId': note_id}
        body_note_content = {
            'noteId': note_id,
            'title': str(int((time.time()) * 1000)) + 'title',
            'summary': str(int((time.time()) * 1000)) + 'summary',
            'body': str(int((time.time()) * 1000)) + 'body',
            'BodyType': 0,
            'localContentVersion': 1
        }
        apicommon.post(url=url, sid=env_config['wps_sid'], body=body_note_info,
                       user_id=env_config['x_user_key'])
        apicommon.post(url=host + '/v3/notesvr/set/notecontent', sid=env_config['wps_sid'], body=body_note_content,
                       user_id=env_config['x_user_key'])
        info_log('step2 用户B进行更改该便签为标星')
        body_b = {
            'noteId': note_id,
            'star': 1
        }
        apicommon.post(url=url, body=body_b, user_id=env_config['x_user_key_B'], sid=env_config['wps_sid_B'])
        info_log('step3 获取用户A信息查看是否标星')
        note_look = note_info_look()
        if note_look.json()["webNotes"][0]['noteId'] == note_id:
            self.assertFalse(note_look.json()["webNotes"][0]["star"] == 1)

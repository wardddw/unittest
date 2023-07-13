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
path = '/v3/notesvr/set/notecontent'
url = host + path
apicommon = ApiCommon()
readYaml = ReadYaml
api_data = readYaml.api_yaml('notes/test_notebody')
checkCommon = CheckCommon()  # 以小驼峰将类进行实例化,括号要记得加才是实例化


@class_case_log
class NoteContentLevel1(unittest.TestCase):  # 改成接口名字+重要级别
    title_summary_must_key = api_data['title_summary_must_key']  # 参数化的元组列表，请求头必填项校验
    body_BodyType_must_key = api_data['body_BodyType_must_key']
    """如果你有两个值要改变比如({key:'title','res_code':200},{key:'noteId','res_code':500})不能这样表示，会直接报错"""
    """要用yaml文件参数那种才可以([{key:'title','res_code':200}],[{key:'noteId','res_code':500}])在外面套一个框"""
    host = env_config['host']  # 属于环境变量，跟随测试环境变更，请求体和路径不随环境改变而改变，所以不属于环境变量
    wps_sid = env_config['wps_sid']  # 属于环境变量，跟随测试环境变更
    x_user_key = env_config['x_user_key']  # 属于环境变量，跟随测试环境变更

    # def setUpClass(cls) -> None:#类级别的前置步骤，初始化、登录等
    # def tearDown(self) -> None:#后置步骤
    def setUp(self):
        print(Fore.LIGHTCYAN_EX + '----------------------------清空首页环境---------------------------')
        note_info_delete()

    def testCase_major(self):  # 会按序号去执行。
        """创建便签信息内容主流程,校验点①协议规范②接口返回③数据数据存储"""
        note_id = str(int((time.time()) * 1000)) + 'note_id'
        title = '12347'
        summary = '123'
        note_body = '123'
        body = {
            'noteId': note_id,
            'title': title,
            'summary': summary,
            'body': note_body,
            'BodyType': 0,
            'localContentVersion': 1
        }
        info_log('step1 新建用户1便签')
        res = apicommon.post(url=url, body=body, user_id=self.x_user_key, sid=self.wps_sid)
        '''协议规范校验'''
        self.assertEqual(200, res.status_code, msg="状态码校验失败")  # 传两个参数，还会打印出来对比，期望值放前面。
        '''接口返回校验'''
        response = res.json()  # json和text的区别就是一个是字符串一个是字典
        check_items = {'responseTime': 1, 'contentVersion': 1, 'contentUpdateTime': 1}  # 弄成一个字典，可以校验类型，也可以校验是否在
        checkCommon.check_response_len_type_key(check_items=check_items, response=response)
        '''通过查询接口校验返回内容'''
        info_log('step2 获取用户1新建便签信息进行比较')
        get_path = '/v3/notesvr/get/notebody'  # 查询接口
        get_url = self.host + get_path
        get_body = {'noteIds': [note_id]}  # 注意字典包id，否则传参失败
        get_res = apicommon.post(url=get_url, body=get_body, user_id=self.x_user_key,
                                 sid=self.wps_sid)  # 通过查询接口查询内容
        self.assertEqual(200, get_res.status_code, 'noteIds新建失败')  # 先保证查询能查到，就代表新建成功。
        check_body = {
            'noteId': note_id,
            'title': title,
            'summary': summary,
            'body': note_body,
            'bodyType': 0,
            'contentVersion': 1
        }  # 期望检查的内容
        if note_id in get_res.json()['noteBodies'][0]['noteId']:
            checkCommon.check_response_body(check_body, get_res.json(), 'noteBodies')  # 比较返回内容和输出内容是否一致。
        else:
            raise ValueError

    def testCase01_input(self):
        """###noteId必填项校验①规范校验②返回内容###"""
        note_id = str(int((time.time()) * 1000)) + 'note_id'
        title = '12347'
        summary = '123'
        note_body = '123'
        body = {
            'noteId': note_id,
            'title': title,
            'summary': summary,
            'body': note_body,
            'BodyType': 0,
            'localContentVersion': 1
        }
        body.pop('noteId')
        res = apicommon.post(url=url, body=body, user_id=self.x_user_key, sid=self.wps_sid)
        response = res.json()
        self.assertEqual(500, res.status_code)
        self.assertEqual('参数不合法！', response['errorMsg'])
        self.assertEqual(-7, response['errorCode'])

    @parameterized.parameterized.expand(title_summary_must_key)  # 参数化是一个装饰器,对象要么是元组，要么是列表。
    def testCase02_input(self, key):
        """###title、summary必填项校验①规范校验②返回内容###"""
        note_id = str(int((time.time()) * 1000)) + 'note_id'
        title = '12347'
        summary = '123'
        note_body = '123'
        body = {
            'noteId': note_id,
            'title': title,
            'summary': summary,
            'body': note_body,
            'BodyType': 0,
            'localContentVersion': 1
        }
        body.pop(key)
        res = apicommon.post(url=url, body=body, user_id=self.x_user_key, sid=self.wps_sid)
        response = res.json()
        self.assertEqual(500, res.status_code)
        self.assertEqual('参数不合法！', response['errorMsg'])
        self.assertEqual(-7, response['errorCode'])

    @parameterized.parameterized.expand(body_BodyType_must_key)  # 参数化是一个装饰器,对象要么是元组，要么是列表。
    def testCase03_input(self, key):
        """###body、BodyType必填项校验①规范校验②返回内容###"""
        note_id = str(int((time.time()) * 1000)) + 'note_id'
        title = '12347'
        summary = '123'
        note_body = '123'
        body = {
            'noteId': note_id,
            'title': title,
            'summary': summary,
            'body': note_body,
            'BodyType': 0,
            'localContentVersion': 1
        }
        body.pop(key)
        res = apicommon.post(url=url, body=body, user_id=self.x_user_key, sid=self.wps_sid)
        response = res.json()
        self.assertEqual(500, res.status_code)
        self.assertEqual('参数不合法！', response['errorMsg'])
        self.assertEqual(-7, response['errorCode'])

    def testCase04_input(self):
        """###localContentVersion必填项校验①规范校验②返回内容###"""
        note_id = str(int((time.time()) * 1000)) + 'note_id'
        title = '12347'
        summary = '123'
        note_body = '123'
        body = {
            'noteId': note_id,
            'title': title,
            'summary': summary,
            'body': note_body,
            'BodyType': 0,
            'localContentVersion': 1
        }
        body.pop('localContentVersion')
        res = apicommon.post(url=url, body=body, user_id=self.x_user_key, sid=self.wps_sid)
        self.assertEqual(200, res.status_code)

    def testCase05_handle(self):
        """###检测其他用户的NoteID能否修改必填项校验①规范校验②修改内容校验###"""
        info_log('step1 用户A进行新建便签')
        note_id = str(int((time.time()) * 1000)) + 'note_id'
        title = '12347'
        summary = '123'
        note_body = '123'
        body = {
            'noteId': note_id,
            'title': title,
            'summary': summary,
            'body': note_body,
            'BodyType': 0,
            'localContentVersion': 1
        }
        res_a = apicommon.post(url=url, body=body, user_id=self.x_user_key, sid=self.wps_sid)
        self.assertEqual(200, res_a.status_code)
        info_log('step2 用户B进行更改该便签的summary')
        body_b = {
            'noteId': note_id,
            'title': title,
            'summary': 'bbbbbbb',
            'body': note_body,
            'BodyType': 0,
            'localContentVersion': 1
        }
        res_b = apicommon.post(url=url, body=body_b, user_id=env_config['x_user_key_B'], sid=env_config['wps_sid_B'])
        self.assertEqual(200, res_b.status_code)
        self.assertFalse(note_info_look().json()["webNotes"][0]["summary"] == 'bbbbbbb')

    def testCase06_handle(self):
        """###noteId_title唯一性校验①规范校验②修改内容###"""
        info_log('step1 用户A进行新建便签')
        note_id = str(int((time.time()) * 1000)) + 'note_id'
        title = '12347'
        summary = '123'
        note_body = '123'
        body = {
            'noteId': note_id,
            'title': title,
            'summary': summary,
            'body': note_body,
            'BodyType': 0,
            'localContentVersion': 1
        }
        res_a = apicommon.post(url=url, body=body, user_id=self.x_user_key, sid=self.wps_sid)
        self.assertEqual(200, res_a.status_code)
        info_log('step2 修改刚刚的新建便签title，其他不变')
        body_b = {
            'noteId': note_id,
            'title': '111',
            'body': note_body,
            'localContentVersion': 1
        }
        res_b = apicommon.post(url=url, body=body_b, user_id=env_config['x_user_key'], sid=env_config['wps_sid'])
        self.assertEqual(200, res_b.status_code)
        self.assertTrue(note_info_look().json()["webNotes"][0]['title'] == '111')
        self.assertTrue(note_info_look().json()["webNotes"][0]['summary'] == summary)


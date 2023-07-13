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

    def testCase01_input(self):
        """###X-user-key数值类型校验'0'①规范校验②返回内容###"""
        note_id = str(int((time.time()) * 1000)) + 'note_id'
        body = {
            'noteId': note_id,
            'title': str(int((time.time()) * 1000)) + 'title',
            'summary': str(int((time.time()) * 1000)) + 'summary',
            'body': str(int((time.time()) * 1000)) + 'body',
            'BodyType': 0,
            'localContentVersion': 1
        }
        body.pop('noteId')
        res = apicommon.post(url=url, body=body, user_id='0', sid=self.wps_sid)
        response = res.json()
        self.assertEqual(500, res.status_code)
        self.assertEqual('参数不合法！', response['errorMsg'])
        self.assertEqual(-7, response['errorCode'])

    def testCase02_input(self):
        """###X-user-key数值类型校验'-1'①规范校验②返回内容###"""
        note_id = str(int((time.time()) * 1000)) + 'note_id'
        body = {
            'noteId': note_id,
            'title': str(int((time.time()) * 1000)) + 'title',
            'summary': str(int((time.time()) * 1000)) + 'summary',
            'body': str(int((time.time()) * 1000)) + 'body',
            'BodyType': 0,
            'localContentVersion': 1
        }
        body.pop('noteId')
        res = apicommon.post(url=url, body=body, user_id='-1', sid=self.wps_sid)
        response = res.json()
        self.assertEqual(500, res.status_code)
        self.assertEqual('参数不合法！', response['errorMsg'])
        self.assertEqual(-7, response['errorCode'])

    def testCase03_input(self):
        """###X-user-key数值类型校验'2*256'①规范校验②返回内容###"""
        note_id = str(int((time.time()) * 1000)) + 'note_id'
        body = {
            'noteId': note_id,
            'title': str(int((time.time()) * 1000)) + 'title',
            'summary': str(int((time.time()) * 1000)) + 'summary',
            'body': str(int((time.time()) * 1000)) + 'body',
            'BodyType': 0,
            'localContentVersion': 1
        }
        body.pop('noteId')
        res = apicommon.post(url=url, body=body, user_id=('2' * 256), sid=self.wps_sid)
        response = res.json()
        self.assertEqual(500, res.status_code)
        self.assertEqual('参数不合法！', response['errorMsg'])
        self.assertEqual(-7, response['errorCode'])

    def testCase04_input(self):
        """###X-user-key数值类型校验'-2*256'①规范校验②返回内容###"""
        note_id = str(int((time.time()) * 1000)) + 'note_id'
        body = {
            'noteId': note_id,
            'title': str(int((time.time()) * 1000)) + 'title',
            'summary': str(int((time.time()) * 1000)) + 'summary',
            'body': str(int((time.time()) * 1000)) + 'body',
            'BodyType': 0,
            'localContentVersion': 1
        }
        body.pop('noteId')
        res = apicommon.post(url=url, body=body, user_id=('-2' * 256), sid=self.wps_sid)
        response = res.json()
        self.assertEqual(500, res.status_code)
        self.assertEqual('参数不合法！', response['errorMsg'])
        self.assertEqual(-7, response['errorCode'])

    def testCase05_input(self):
        """###X-user-key数值类型校验'1.5'①规范校验②返回内容###"""
        note_id = str(int((time.time()) * 1000)) + 'note_id'
        body = {
            'noteId': note_id,
            'title': str(int((time.time()) * 1000)) + 'title',
            'summary': str(int((time.time()) * 1000)) + 'summary',
            'body': str(int((time.time()) * 1000)) + 'body',
            'BodyType': 0,
            'localContentVersion': 1
        }
        body.pop('noteId')
        res = apicommon.post(url=url, body=body, user_id='1.5', sid=self.wps_sid)
        response = res.json()
        self.assertEqual(500, res.status_code)
        self.assertEqual('参数不合法！', response['errorMsg'])
        self.assertEqual(-7, response['errorCode'])

    def testCase06_input(self):
        """###X-user-key数值类型校验'"1"'①规范校验②返回内容###"""
        note_id = str(int((time.time()) * 1000)) + 'note_id'
        body = {
            'noteId': note_id,
            'title': str(int((time.time()) * 1000)) + 'title',
            'summary': str(int((time.time()) * 1000)) + 'summary',
            'body': str(int((time.time()) * 1000)) + 'body',
            'BodyType': 0,
            'localContentVersion': 1
        }
        body.pop('noteId')
        res = apicommon.post(url=url, body=body, user_id='"1"', sid=self.wps_sid)
        response = res.json()
        self.assertEqual(500, res.status_code)
        self.assertEqual('参数不合法！', response['errorMsg'])
        self.assertEqual(-7, response['errorCode'])

    def testCase07_input(self):
        """###X-user-key数值类型校验None①规范校验②返回内容###"""
        note_id = str(int((time.time()) * 1000)) + 'note_id'
        body = {
            'noteId': note_id,
            'title': str(int((time.time()) * 1000)) + 'title',
            'summary': str(int((time.time()) * 1000)) + 'summary',
            'body': str(int((time.time()) * 1000)) + 'body',
            'BodyType': 0,
            'localContentVersion': 1
        }
        body.pop('noteId')
        res = apicommon.post(url=url, body=body, user_id=None, sid=self.wps_sid)
        response = res.json()
        self.assertEqual(500, res.status_code)
        self.assertEqual('参数不合法！', response['errorMsg'])
        self.assertEqual(-7, response['errorCode'])

    def testCase08_input(self):
        """###noteId数值类型校验1*256①规范校验②返回内容###"""
        body = {
            'noteId': ('1' * 256),
            'title': str(int((time.time()) * 1000)) + 'title',
            'summary': str(int((time.time()) * 1000)) + 'summary',
            'body': str(int((time.time()) * 1000)) + 'body',
            'BodyType': 0,
            'localContentVersion': 1
        }
        res = apicommon.post(url=url, body=body, user_id=self.x_user_key, sid=self.wps_sid)
        response = res.json()
        self.assertEqual(500, res.status_code)
        self.assertEqual('参数不合法！', response['errorMsg'])
        self.assertEqual(-7, response['errorCode'])

    def testCase09_input(self):
        """###noteId数值类型校验空字符串①规范校验②返回内容###"""
        body = {
            'noteId': "",
            'title': str(int((time.time()) * 1000)) + 'title',
            'summary': str(int((time.time()) * 1000)) + 'summary',
            'body': str(int((time.time()) * 1000)) + 'body',
            'BodyType': 0,
            'localContentVersion': 1
        }
        res = apicommon.post(url=url, body=body, user_id=self.x_user_key, sid=self.wps_sid)
        response = res.json()
        self.assertEqual(500, res.status_code)
        self.assertEqual('参数不合法！', response['errorMsg'])
        self.assertEqual(-7, response['errorCode'])

    def testCase10_input(self):
        """###noteId数值类型校验特殊字符①规范校验②返回内容###"""
        body = {
            'noteId': '……%￥……）（#%',
            'title': str(int((time.time()) * 1000)) + 'title',
            'summary': str(int((time.time()) * 1000)) + 'summary',
            'body': str(int((time.time()) * 1000)) + 'body',
            'BodyType': 0,
            'localContentVersion': 1
        }
        res = apicommon.post(url=url, body=body, user_id=self.x_user_key, sid=self.wps_sid)
        response = res.json()
        self.assertEqual(500, res.status_code)
        self.assertEqual('参数不合法！', response['errorMsg'])
        self.assertEqual(-7, response['errorCode'])

    def testCase11_input(self):
        """###noteId数值类型校验中文①规范校验②返回内容###"""
        body = {
            'noteId': '啊松大',
            'title': str(int((time.time()) * 1000)) + 'title',
            'summary': str(int((time.time()) * 1000)) + 'summary',
            'body': str(int((time.time()) * 1000)) + 'body',
            'BodyType': 0,
            'localContentVersion': 1
        }
        res = apicommon.post(url=url, body=body, user_id=self.x_user_key, sid=self.wps_sid)
        response = res.json()
        self.assertEqual(500, res.status_code)
        self.assertEqual('参数不合法！', response['errorMsg'])
        self.assertEqual(-7, response['errorCode'])

    def testCase12_input(self):
        """###noteId数值类型校验int①规范校验②返回内容###"""
        body = {
            'noteId': 123,
            'title': str(int((time.time()) * 1000)) + 'title',
            'summary': str(int((time.time()) * 1000)) + 'summary',
            'body': str(int((time.time()) * 1000)) + 'body',
            'BodyType': 0,
            'localContentVersion': 1
        }
        res = apicommon.post(url=url, body=body, user_id=self.x_user_key, sid=self.wps_sid)
        response = res.json()
        self.assertEqual(500, res.status_code)
        self.assertEqual('参数不合法！', response['errorMsg'])
        self.assertEqual(-7, response['errorCode'])

    def testCase13_input(self):
        """###noteId数值类型校验空①规范校验②返回内容###"""
        body = {
            'noteId': None,
            'title': str(int((time.time()) * 1000)) + 'title',
            'summary': str(int((time.time()) * 1000)) + 'summary',
            'body': str(int((time.time()) * 1000)) + 'body',
            'BodyType': 0,
            'localContentVersion': 1
        }
        res = apicommon.post(url=url, body=body, user_id=self.x_user_key, sid=self.wps_sid)
        response = res.json()
        self.assertEqual(500, res.status_code)
        self.assertEqual('参数不合法！', response['errorMsg'])
        self.assertEqual(-7, response['errorCode'])

    def testCase14_input(self):
        """###title数值类型校验'1*256'①规范校验②返回内容###"""
        note_id = str(int((time.time()) * 1000)) + 'note_id'
        body = {
            'noteId': note_id,
            'title': ('1' * 256),
            'summary': str(int((time.time()) * 1000)) + 'summary',
            'body': str(int((time.time()) * 1000)) + 'body',
            'BodyType': 0,
            'localContentVersion': 1
        }
        res = apicommon.post(url=url, body=body, user_id=self.x_user_key, sid=self.wps_sid)
        response = res.json()
        self.assertEqual(500, res.status_code)
        self.assertEqual('参数不合法！', response['errorMsg'])
        self.assertEqual(-7, response['errorCode'])

    def testCase15_input(self):
        """###title数值类型校验空字符串①规范校验②返回内容###"""
        note_id = str(int((time.time()) * 1000)) + 'note_id'
        body = {
            'noteId': note_id,
            'title': '',
            'summary': str(int((time.time()) * 1000)) + 'summary',
            'body': str(int((time.time()) * 1000)) + 'body',
            'BodyType': 0,
            'localContentVersion': 1
        }
        res = apicommon.post(url=url, body=body, user_id=self.x_user_key, sid=self.wps_sid)
        response = res.json()
        check_item = {"responseTime": 1, "contentVersion": 1, "contentUpdateTime": 1}
        self.assertEqual(200, res.status_code)
        if check_item.keys() == response.keys():
            for key in check_item:
                if key in response:
                    checkCommon.check_response_len_type_key(check_items=check_item, response=response)
        else:
            error_log('key not in check_key')
            self.assertTrue(1 != 1)

    def testCase16_input(self):
        """###title数值类型校验特殊字符①规范校验②返回内容###"""
        note_id = str(int((time.time()) * 1000)) + 'note_id'
        body = {
            'noteId': note_id,
            'title': '……%￥……#',
            'summary': str(int((time.time()) * 1000)) + 'summary',
            'body': str(int((time.time()) * 1000)) + 'body',
            'BodyType': 0,
            'localContentVersion': 1
        }
        res = apicommon.post(url=url, body=body, user_id=self.x_user_key, sid=self.wps_sid)
        response = res.json()
        self.assertEqual(500, res.status_code)
        self.assertEqual('参数不合法！', response['errorMsg'])
        self.assertEqual(-7, response['errorCode'])

    def testCase17_input(self):
        """###title数值类型校验'ABC'①规范校验②返回内容###"""
        note_id = str(int((time.time()) * 1000)) + 'note_id'
        body = {
            'noteId': note_id,
            'title': 'ABC',
            'summary': str(int((time.time()) * 1000)) + 'summary',
            'body': str(int((time.time()) * 1000)) + 'body',
            'BodyType': 0,
            'localContentVersion': 1
        }
        res = apicommon.post(url=url, body=body, user_id=self.x_user_key, sid=self.wps_sid)
        response = res.json()
        check_item = {"responseTime": 1, "contentVersion": 1, "contentUpdateTime": 1}
        self.assertEqual(200, res.status_code)
        if check_item.keys() == response.keys():
            for key in check_item:
                if key in response:
                    checkCommon.check_response_len_type_key(check_items=check_item, response=response)
        else:
            error_log('key not in check_key')
            self.assertTrue(1 != 1)

    def testCase18_input(self):
        """###title数值类型校验中文①规范校验②返回内容###"""
        note_id = str(int((time.time()) * 1000)) + 'note_id'
        body = {
            'noteId': note_id,
            'title': '啊松大',
            'summary': str(int((time.time()) * 1000)) + 'summary',
            'body': str(int((time.time()) * 1000)) + 'body',
            'BodyType': 0,
            'localContentVersion': 1
        }
        res = apicommon.post(url=url, body=body, user_id=self.x_user_key, sid=self.wps_sid)
        response = res.json()
        self.assertEqual(500, res.status_code)
        self.assertEqual('参数不合法！', response['errorMsg'])
        self.assertEqual(-7, response['errorCode'])

    def testCase19_input(self):
        """###title数值类型校验int①规范校验②返回内容###"""
        note_id = str(int((time.time()) * 1000)) + 'note_id'
        body = {
            'noteId': note_id,
            'title': 123,
            'summary': str(int((time.time()) * 1000)) + 'summary',
            'body': str(int((time.time()) * 1000)) + 'body',
            'BodyType': 0,
            'localContentVersion': 1
        }
        res = apicommon.post(url=url, body=body, user_id=self.x_user_key, sid=self.wps_sid)
        response = res.json()
        self.assertEqual(500, res.status_code)
        self.assertEqual('参数不合法！', response['errorMsg'])
        self.assertEqual(-7, response['errorCode'])

    def testCase20_input(self):
        """###title数值类型校验NONE①规范校验②返回内容###"""
        note_id = str(int((time.time()) * 1000)) + 'note_id'
        body = {
            'noteId': note_id,
            'title': None,
            'summary': str(int((time.time()) * 1000)) + 'summary',
            'body': str(int((time.time()) * 1000)) + 'body',
            'BodyType': 0,
            'localContentVersion': 1
        }
        res = apicommon.post(url=url, body=body, user_id=self.x_user_key, sid=self.wps_sid)
        response = res.json()
        self.assertEqual(500, res.status_code)
        self.assertEqual('参数不合法！', response['errorMsg'])
        self.assertEqual(-7, response['errorCode'])

    def testCase21_input(self):
        """###summary数值类型校验长度1=1687541①规范校验②返回内容###"""
        note_id = str(int((time.time()) * 1000)) + 'note_id'
        body = {
            'noteId': note_id,
            'title': str(int((time.time()) * 1000)) + 'title',
            'summary': ('1') * 1687541,
            'body': str(int((time.time()) * 1000)) + 'body',
            'BodyType': 0,
            'localContentVersion': 1
        }
        res = apicommon.post(url=url, body=body, user_id=self.x_user_key, sid=self.wps_sid)
        response = res.json()
        self.assertEqual(500, res.status_code)
        self.assertEqual('参数不合法！', response['errorMsg'])
        self.assertEqual(-7, response['errorCode'])

    def testCase22_input(self):
        """###summary数值类型校验长度1=""①规范校验②返回内容###"""
        note_id = str(int((time.time()) * 1000)) + 'note_id'
        body = {
            'noteId': note_id,
            'title': str(int((time.time()) * 1000)) + 'title',
            'summary': "",
            'body': str(int((time.time()) * 1000)) + 'body',
            'BodyType': 0,
            'localContentVersion': 1
        }
        res = apicommon.post(url=url, body=body, user_id=self.x_user_key, sid=self.wps_sid)
        response = res.json()
        self.assertEqual(500, res.status_code)
        self.assertEqual('参数不合法！', response['errorMsg'])
        self.assertEqual(-7, response['errorCode'])

    def testCase23_input(self):
        """###summary数值类型特殊字符""①规范校验②返回内容###"""
        note_id = str(int((time.time()) * 1000)) + 'note_id'
        body = {
            'noteId': note_id,
            'title': str(int((time.time()) * 1000)) + 'title',
            'summary': "……%￥……#",
            'body': str(int((time.time()) * 1000)) + 'body',
            'BodyType': 0,
            'localContentVersion': 1
        }
        res = apicommon.post(url=url, body=body, user_id=self.x_user_key, sid=self.wps_sid)
        response = res.json()
        self.assertEqual(500, res.status_code)
        self.assertEqual('参数不合法！', response['errorMsg'])
        self.assertEqual(-7, response['errorCode'])

    def testCase24_input(self):
        """###summary数值类型ABC""①规范校验②返回内容###"""
        note_id = str(int((time.time()) * 1000)) + 'note_id'
        body = {
            'noteId': note_id,
            'title': str(int((time.time()) * 1000)) + 'title',
            'summary': "ABC",
            'body': str(int((time.time()) * 1000)) + 'body',
            'BodyType': 0,
            'localContentVersion': 1
        }
        res = apicommon.post(url=url, body=body, user_id=self.x_user_key, sid=self.wps_sid)
        response = res.json()
        check_item = {"responseTime": 1, "contentVersion": 1, "contentUpdateTime": 1}
        self.assertEqual(200, res.status_code)
        if check_item.keys() == response.keys():
            for key in check_item:
                if key in response:
                    checkCommon.check_response_len_type_key(check_items=check_item, response=response)
        else:
            error_log('key not in check_key')
            self.assertTrue(1 != 1)

    def testCase25_input(self):
        """###summary数值类型特殊中文‘啊松大’""①规范校验②返回内容###"""
        note_id = str(int((time.time()) * 1000)) + 'note_id'
        body = {
            'noteId': note_id,
            'title': str(int((time.time()) * 1000)) + 'title',
            'summary': "啊松大",
            'body': str(int((time.time()) * 1000)) + 'body',
            'BodyType': 0,
            'localContentVersion': 1
        }
        res = apicommon.post(url=url, body=body, user_id=self.x_user_key, sid=self.wps_sid)
        response = res.json()
        check_item = {"responseTime": 1, "contentVersion": 1, "contentUpdateTime": 1}
        self.assertEqual(200, res.status_code)
        if check_item.keys() == response.keys():
            for key in check_item:
                if key in response:
                    checkCommon.check_response_len_type_key(check_items=check_item, response=response)
        else:
            error_log('key not in check_key')
            self.assertTrue(1 != 1)

    def testCase26_input(self):
        """###summary数值类型int123""①规范校验②返回内容###"""
        note_id = str(int((time.time()) * 1000)) + 'note_id'
        body = {
            'noteId': note_id,
            'title': str(int((time.time()) * 1000)) + 'title',
            'summary': 123,
            'body': str(int((time.time()) * 1000)) + 'body',
            'BodyType': 0,
            'localContentVersion': 1
        }
        res = apicommon.post(url=url, body=body, user_id=self.x_user_key, sid=self.wps_sid)
        response = res.json()
        self.assertEqual(500, res.status_code)
        self.assertEqual('参数不合法！', response['errorMsg'])
        self.assertEqual(-7, response['errorCode'])

    def testCase27_input(self):
        """###summary数值类型None""①规范校验②返回内容###"""
        note_id = str(int((time.time()) * 1000)) + 'note_id'
        body = {
            'noteId': note_id,
            'title': str(int((time.time()) * 1000)) + 'title',
            'summary': None,
            'body': str(int((time.time()) * 1000)) + 'body',
            'BodyType': 0,
            'localContentVersion': 1
        }
        res = apicommon.post(url=url, body=body, user_id=self.x_user_key, sid=self.wps_sid)
        response = res.json()
        self.assertEqual(500, res.status_code)
        self.assertEqual('参数不合法！', response['errorMsg'])
        self.assertEqual(-7, response['errorCode'])

    def testCase28_input(self):
        """###body数值类型"1"*1687541①规范校验②返回内容###"""
        note_id = str(int((time.time()) * 1000)) + 'note_id'
        body = {
            'noteId': note_id,
            'title': str(int((time.time()) * 1000)) + 'title',
            'summary': str(int((time.time()) * 1000)) + 'summary',
            'body': "1" * 1687541,
            'BodyType': 0,
            'localContentVersion': 1
        }
        res = apicommon.post(url=url, body=body, user_id=self.x_user_key, sid=self.wps_sid)
        response = res.json()
        self.assertEqual(500, res.status_code)
        self.assertEqual('参数不合法！', response['errorMsg'])
        self.assertEqual(-7, response['errorCode'])

    def testCase29_input(self):
        """###body数值类型空字符串""①规范校验②返回内容###"""
        note_id = str(int((time.time()) * 1000)) + 'note_id'
        body = {
            'noteId': note_id,
            'title': str(int((time.time()) * 1000)) + 'title',
            'summary': str(int((time.time()) * 1000)) + 'summary',
            'body': "",
            'BodyType': 0,
            'localContentVersion': 1
        }
        res = apicommon.post(url=url, body=body, user_id=self.x_user_key, sid=self.wps_sid)
        response = res.json()
        self.assertEqual(412, res.status_code)
        self.assertEqual('Note body Requested!', response['errorMsg'])
        self.assertEqual(-1012, response['errorCode'])

    def testCase30_input(self):
        """###body数值类型“啊松大”""①规范校验②返回内容###"""
        note_id = str(int((time.time()) * 1000)) + 'note_id'
        body = {
            'noteId': note_id,
            'title': str(int((time.time()) * 1000)) + 'title',
            'summary': str(int((time.time()) * 1000)) + 'summary',
            'body': "啊松大",
            'BodyType': 0,
            'localContentVersion': 1
        }
        res = apicommon.post(url=url, body=body, user_id=self.x_user_key, sid=self.wps_sid)
        response = res.json()
        self.assertEqual(500, res.status_code)
        self.assertEqual('参数不合法！', response['errorMsg'])
        self.assertEqual(-7, response['errorCode'])

    def testCase31_input(self):
        """###body数值类型特殊字符“……%￥……#”""①规范校验②返回内容###"""
        note_id = str(int((time.time()) * 1000)) + 'note_id'
        body = {
            'noteId': note_id,
            'title': str(int((time.time()) * 1000)) + 'title',
            'summary': str(int((time.time()) * 1000)) + 'summary',
            'body': "……%￥……#",
            'BodyType': 0,
            'localContentVersion': 1
        }
        res = apicommon.post(url=url, body=body, user_id=self.x_user_key, sid=self.wps_sid)
        response = res.json()
        self.assertEqual(500, res.status_code)
        self.assertEqual('参数不合法！', response['errorMsg'])
        self.assertEqual(-7, response['errorCode'])

    def testCase32_input(self):
        """###body数值类型特殊字符“ABC""①规范校验②返回内容###"""
        note_id = str(int((time.time()) * 1000)) + 'note_id'
        body = {
            'noteId': note_id,
            'title': str(int((time.time()) * 1000)) + 'title',
            'summary': str(int((time.time()) * 1000)) + 'summary',
            'body': "ABC",
            'BodyType': 0,
            'localContentVersion': 1
        }
        res = apicommon.post(url=url, body=body, user_id=self.x_user_key, sid=self.wps_sid)
        response = res.json()
        check_item = {"responseTime": 1, "contentVersion": 1, "contentUpdateTime": 1}
        self.assertEqual(200, res.status_code)
        if check_item.keys() == response.keys():
            for key in check_item:
                if key in response:
                    checkCommon.check_response_len_type_key(check_items=check_item, response=response)
        else:
            error_log('key not in check_key')
            self.assertTrue(1 != 1)

    def testCase33_input(self):
        """###body数值类型int123"①规范校验②返回内容###"""
        note_id = str(int((time.time()) * 1000)) + 'note_id'
        body = {
            'noteId': note_id,
            'title': str(int((time.time()) * 1000)) + 'title',
            'summary': str(int((time.time()) * 1000)) + 'summary',
            'body': 123,
            'BodyType': 0,
            'localContentVersion': 1
        }
        res = apicommon.post(url=url, body=body, user_id=self.x_user_key, sid=self.wps_sid)
        response = res.json()
        self.assertEqual(500, res.status_code)
        self.assertEqual('参数不合法！', response['errorMsg'])
        self.assertEqual(-7, response['errorCode'])

    def testCase34_input(self):
        """###body数值类型None"①规范校验②返回内容###"""
        note_id = str(int((time.time()) * 1000)) + 'note_id'
        body = {
            'noteId': note_id,
            'title': str(int((time.time()) * 1000)) + 'title',
            'summary': str(int((time.time()) * 1000)) + 'summary',
            'body': None,
            'BodyType': 0,
            'localContentVersion': 1
        }
        res = apicommon.post(url=url, body=body, user_id=self.x_user_key, sid=self.wps_sid)
        response = res.json()
        self.assertEqual(412, res.status_code)
        self.assertEqual('Note body Requested!', response['errorMsg'])
        self.assertEqual(-1012, response['errorCode'])

    def testCase35_input(self):
        """###localContentVersion数值类型16888888811"①规范校验②返回内容###"""
        note_id = str(int((time.time()) * 1000)) + 'note_id'
        body = {
            'noteId': note_id,
            'title': str(int((time.time()) * 1000)) + 'title',
            'summary': str(int((time.time()) * 1000)) + 'summary',
            'body': str(int((time.time()) * 1000)) + 'body',
            'BodyType': 0,
            'localContentVersion': 16888888811
        }
        res = apicommon.post(url=url, body=body, user_id=self.x_user_key, sid=self.wps_sid)
        response = res.json()
        self.assertEqual(500, res.status_code)
        self.assertEqual('', response['errorMsg'])
        self.assertEqual(-7, response['errorCode'])

    def testCase36_input(self):
        """###localContentVersion数值类型-16888888811"①规范校验②返回内容###"""
        note_id = str(int((time.time()) * 1000)) + 'note_id'
        body = {
            'noteId': note_id,
            'title': str(int((time.time()) * 1000)) + 'title',
            'summary': str(int((time.time()) * 1000)) + 'summary',
            'body': str(int((time.time()) * 1000)) + 'body',
            'BodyType': 0,
            'localContentVersion': 16888888811
        }
        res = apicommon.post(url=url, body=body, user_id=self.x_user_key, sid=self.wps_sid)
        response = res.json()
        self.assertEqual(500, res.status_code)
        self.assertEqual('', response['errorMsg'])
        self.assertEqual(-7, response['errorCode'])

    def testCase37_input(self):
        """###localContentVersion数值类型1.5"①规范校验②返回内容###"""
        note_id = str(int((time.time()) * 1000)) + 'note_id'
        body = {
            'noteId': note_id,
            'title': str(int((time.time()) * 1000)) + 'title',
            'summary': str(int((time.time()) * 1000)) + 'summary',
            'body': str(int((time.time()) * 1000)) + 'body',
            'BodyType': 0,
            'localContentVersion': 1.5
        }
        res = apicommon.post(url=url, body=body, user_id=self.x_user_key, sid=self.wps_sid)
        response = res.json()
        self.assertEqual(500, res.status_code)
        self.assertEqual('', response['errorMsg'])
        self.assertEqual(-7, response['errorCode'])

    def testCase38_input(self):
        """###localContentVersion数值类型1.5"①规范校验②返回内容###"""
        note_id = str(int((time.time()) * 1000)) + 'note_id'
        body = {
            'noteId': note_id,
            'title': str(int((time.time()) * 1000)) + 'title',
            'summary': str(int((time.time()) * 1000)) + 'summary',
            'body': str(int((time.time()) * 1000)) + 'body',
            'BodyType': 0,
            'localContentVersion': '1'
        }
        res = apicommon.post(url=url, body=body, user_id=self.x_user_key, sid=self.wps_sid)
        response = res.json()
        self.assertEqual(500, res.status_code)
        self.assertEqual('', response['errorMsg'])
        self.assertEqual(-7, response['errorCode'])

    def testCase39_input(self):
        """###localContentVersion数值类型None"①规范校验②返回内容###"""
        note_id = str(int((time.time()) * 1000)) + 'note_id'
        body = {
            'noteId': note_id,
            'title': str(int((time.time()) * 1000)) + 'title',
            'summary': str(int((time.time()) * 1000)) + 'summary',
            'body': str(int((time.time()) * 1000)) + 'body',
            'BodyType': 0,
            'localContentVersion': None
        }
        res = apicommon.post(url=url, body=body, user_id=self.x_user_key, sid=self.wps_sid)
        response = res.json()
        self.assertEqual(500, res.status_code)
        self.assertEqual('', response['errorMsg'])
        self.assertEqual(-7, response['errorCode'])

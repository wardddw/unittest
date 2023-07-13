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
    remindTime_remindType = api_data['remindTime_remindType_key']

    def setUp(self):
        print(Fore.LIGHTCYAN_EX + '----------------------------清空首页环境---------------------------')
        note_info_delete()

    def testCase01_input(self):
        """###noteId数值类型校验1*256①规范校验②返回内容###"""
        body = {
            'noteId': ('1' * 256),
        }
        res = apicommon.post(url=url, body=body, user_id=self.x_user_key, sid=self.wps_sid)
        response = res.json()
        self.assertEqual(500, res.status_code)
        self.assertEqual('参数不合法！', response['errorMsg'])
        self.assertEqual(-7, response['errorCode'])

    def testCase02_input(self):
        """###noteId数值类型校验空字符串①规范校验②返回内容###"""
        body = {
            'noteId': "",
        }
        res = apicommon.post(url=url, body=body, user_id=self.x_user_key, sid=self.wps_sid)
        response = res.json()
        self.assertEqual(500, res.status_code)
        self.assertEqual('参数不合法！', response['errorMsg'])
        self.assertEqual(-7, response['errorCode'])

    def testCase03_input(self):
        """###noteId数值类型校验特殊字符①规范校验②返回内容###"""
        body = {
            'noteId': '……%￥……）（#%',
        }
        res = apicommon.post(url=url, body=body, user_id=self.x_user_key, sid=self.wps_sid)
        response = res.json()
        self.assertEqual(500, res.status_code)
        self.assertEqual('参数不合法！', response['errorMsg'])
        self.assertEqual(-7, response['errorCode'])

    def testCase04_input(self):
        """###noteId数值类型校验中文①规范校验②返回内容###"""
        body = {
            'noteId': '啊松大',
        }
        res = apicommon.post(url=url, body=body, user_id=self.x_user_key, sid=self.wps_sid)
        response = res.json()
        self.assertEqual(500, res.status_code)
        self.assertEqual('参数不合法！', response['errorMsg'])
        self.assertEqual(-7, response['errorCode'])

    def testCase05_input(self):
        """###noteId数值类型校验int①规范校验②返回内容###"""
        body = {
            'noteId': 123,
        }
        res = apicommon.post(url=url, body=body, user_id=self.x_user_key, sid=self.wps_sid)
        response = res.json()
        self.assertEqual(500, res.status_code)
        self.assertEqual('参数不合法！', response['errorMsg'])
        self.assertEqual(-7, response['errorCode'])

    def testCase06_input(self):
        """###noteId数值类型校验空①规范校验②返回内容###"""
        body = {
            'noteId': None,
        }
        res = apicommon.post(url=url, body=body, user_id=self.x_user_key, sid=self.wps_sid)
        response = res.json()
        self.assertEqual(500, res.status_code)
        self.assertEqual('参数不合法！', response['errorMsg'])
        self.assertEqual(-7, response['errorCode'])

    @parameterized.parameterized.expand(remindTime_remindType)
    def testCase07_input(self, key):
        """###remindTime、remindType、star数值类型168888888111①规范校验②返回内容###"""
        body = {
            'noteId': str(int((time.time()) * 1000)) + 'note_id',
            key: 16888888811
        }
        res = apicommon.post(url=url, body=body, user_id=self.x_user_key, sid=self.wps_sid)
        response = res.json()
        self.assertEqual(500, res.status_code)
        self.assertEqual('参数不合法！', response['errorMsg'])
        self.assertEqual(-7, response['errorCode'])

    @parameterized.parameterized.expand(remindTime_remindType)
    def testCase08_input(self, key):
        """###remindTime、remindType、star数值类型0①规范校验②返回内容###"""
        body = {
            'noteId': str(int((time.time()) * 1000)) + 'note_id',
            key: 0
        }
        res = apicommon.post(url=url, body=body, user_id=self.x_user_key, sid=self.wps_sid)
        response = res.json()
        self.assertEqual(500, res.status_code)
        self.assertEqual('参数不合法！', response['errorMsg'])
        self.assertEqual(-7, response['errorCode'])

    @parameterized.parameterized.expand(remindTime_remindType)
    def testCase09_input(self, key):
        """###remindTime、remindType、star数值类型-1①规范校验②返回内容###"""
        body = {
            'noteId': str(int((time.time()) * 1000)) + 'note_id',
            key: -1
        }
        res = apicommon.post(url=url, body=body, user_id=self.x_user_key, sid=self.wps_sid)
        response = res.json()
        self.assertEqual(500, res.status_code)
        self.assertEqual('参数不合法！', response['errorMsg'])
        self.assertEqual(-7, response['errorCode'])

    @parameterized.parameterized.expand(remindTime_remindType)
    def testCase10_input(self, key):
        """###remindTime、remindType、star数值类型-2147483649①规范校验②返回内容###"""
        body = {
            'noteId': str(int((time.time()) * 1000)) + 'note_id',
            key: -2147483649
        }
        res = apicommon.post(url=url, body=body, user_id=self.x_user_key, sid=self.wps_sid)
        response = res.json()
        self.assertEqual(500, res.status_code)
        self.assertEqual('参数不合法！', response['errorMsg'])
        self.assertEqual(-7, response['errorCode'])

    @parameterized.parameterized.expand(remindTime_remindType)
    def testCase11_input(self, key):
        """###remindTime、remindType、star数值类型2147483649①规范校验②返回内容###"""
        body = {
            'noteId': str(int((time.time()) * 1000)) + 'note_id',
            key: 2147483649
        }
        res = apicommon.post(url=url, body=body, user_id=self.x_user_key, sid=self.wps_sid)
        response = res.json()
        self.assertEqual(500, res.status_code)
        self.assertEqual('参数不合法！', response['errorMsg'])
        self.assertEqual(-7, response['errorCode'])

    @parameterized.parameterized.expand(remindTime_remindType)
    def testCase12_input(self, key):
        """###remindTime、remindType、star数值类型1.5①规范校验②返回内容###"""
        body = {
            'noteId': str(int((time.time()) * 1000)) + 'note_id',
            key: 1.5
        }
        res = apicommon.post(url=url, body=body, user_id=self.x_user_key, sid=self.wps_sid)
        response = res.json()
        self.assertEqual(500, res.status_code)
        self.assertEqual('参数不合法！', response['errorMsg'])
        self.assertEqual(-7, response['errorCode'])

    @parameterized.parameterized.expand(remindTime_remindType)
    def testCase13_input(self, key):
        """###remindTime、remindType、star数值类型'1'①规范校验②返回内容###"""
        body = {
            'noteId': str(int((time.time()) * 1000)) + 'note_id',
            key: '1'
        }
        res = apicommon.post(url=url, body=body, user_id=self.x_user_key, sid=self.wps_sid)
        response = res.json()
        self.assertEqual(500, res.status_code)
        self.assertEqual('参数不合法！', response['errorMsg'])
        self.assertEqual(-7, response['errorCode'])

    @parameterized.parameterized.expand(remindTime_remindType)
    def testCase14_input(self, key):
        """###remindTime、remindType、star数值类型None①规范校验②返回内容###"""
        body = {
            'noteId': str(int((time.time()) * 1000)) + 'note_id',
            key: None
        }
        res = apicommon.post(url=url, body=body, user_id=self.x_user_key, sid=self.wps_sid)
        response = res.json()
        self.assertEqual(500, res.status_code)
        self.assertEqual('参数不合法！', response['errorMsg'])
        self.assertEqual(-7, response['errorCode'])

    def testCase15_input(self):
        """###groupld数值类型1*256①规范校验②返回内容###"""
        body = {
            'noteId': str(int((time.time()) * 1000)) + 'note_id',
            ' groupld': '1' * 256
        }
        res = apicommon.post(url=url, body=body, user_id=self.x_user_key, sid=self.wps_sid)
        response = res.json()
        self.assertEqual(500, res.status_code)
        self.assertEqual('参数不合法！', response['errorMsg'])
        self.assertEqual(-7, response['errorCode'])

    def testCase16_input(self):
        """###groupld数值类型空字符串①规范校验②返回内容###"""
        body = {
            'noteId': str(int((time.time()) * 1000)) + 'note_id',
            ' groupld': ''
        }
        res = apicommon.post(url=url, body=body, user_id=self.x_user_key, sid=self.wps_sid)
        response = res.json()
        self.assertEqual(500, res.status_code)
        self.assertEqual('参数不合法！', response['errorMsg'])
        self.assertEqual(-7, response['errorCode'])

    def testCase17_input(self):
        """###groupld数值类型特殊字符串①规范校验②返回内容###"""
        body = {
            'noteId': str(int((time.time()) * 1000)) + 'note_id',
            ' groupld': '！@￥@#￥%%……￥**（）/'
        }
        res = apicommon.post(url=url, body=body, user_id=self.x_user_key, sid=self.wps_sid)
        response = res.json()
        self.assertEqual(500, res.status_code)
        self.assertEqual('参数不合法！', response['errorMsg'])
        self.assertEqual(-7, response['errorCode'])

    def testCase18_input(self):
        """###groupld数值类型中文①规范校验②返回内容###"""
        body = {
            'noteId': str(int((time.time()) * 1000)) + 'note_id',
            ' groupld': '中文'
        }
        res = apicommon.post(url=url, body=body, user_id=self.x_user_key, sid=self.wps_sid)
        response = res.json()
        check_item = {"responseTime": 1, "infoVersion": 1, "infoUpdateTime": 1}
        self.assertEqual(200, res.status_code)
        if check_item.keys() == response.keys():
            for key in check_item:
                if key in response:
                    checkCommon.check_response_len_type_key(check_items=check_item, response=response)
        else:
            error_log('key not in check_key')
            self.assertTrue(1 != 1)

    def testCase19_input(self):
        """###groupld数值类型int123①规范校验②返回内容###"""
        body = {
            'noteId': str(int((time.time()) * 1000)) + 'note_id',
            ' groupld': 123
        }
        res = apicommon.post(url=url, body=body, user_id=self.x_user_key, sid=self.wps_sid)
        response = res.json()
        self.assertEqual(500, res.status_code)
        self.assertEqual('参数不合法！', response['errorMsg'])
        self.assertEqual(-7, response['errorCode'])
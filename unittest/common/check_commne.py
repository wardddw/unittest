import unittest


class CheckCommon(unittest.TestCase):
    def check_response_len_type_key(self, check_items, response):
        self.assertEqual(len(check_items), len(response))  # 验证长度
        for key, values in check_items.items():
            self.assertIn(key, response)  # 返回体是否正确（长度卡死，这个也通过了即正确）
            self.assertEqual(type(values), type(response[key]))  # 产看返回体的类型是否相等。

    def check_response_body(self, check_body, get_response,body_key):  # 通过查询接口对比返回体和检查体内容的方法。
        for key, value in check_body.items():
            self.assertEqual(value, get_response[body_key][0][key])




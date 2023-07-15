import unittest  # 导入数据库
from BeautifulReport import BeautifulReport
import os

DIR = os.path.dirname(os.path.abspath(__file__))  # 获取当前目录，os系统命令。跟随当前目录虽在位置，是不会变化的。
# 可以实现环境模块的切换
# Environ_offline = '/env_config/offline'
Environ_online = '/env_config/online'


# os.path.dirname（os.path.dirname(os.path.abspath(__file__))）#套多一层就是回到上一层目录

# suite = unittest.TestSuite()  # 套件实例化
# suite.addTest(NoteContent('test01_major'))
# suite.addTest(NoteContent('test02_input'))
# suite.addTest(NoteContent('test03_input'))  # 如果只用测试套件只能用这种方法去一条一条加
#
# if __name__ == '__main__':
#     runner = unittest.TextTestRunner()  # 实例化 .是正常 f是断言失败 e是错误 @unitter.skip是跳过用例，断言结果会显示s
#     runner.run(suite)
def run(test_suite):
    # 定义输出文件和名字
    filename = "report.html"
    result = BeautifulReport(test_suite)
    result.report(filename=filename, description="测试报告", report_dir=DIR)  # dir是存储目录,


if __name__ == '__main__':
    strategy = "all"
    if strategy == 'smoke':
        pattern = 'test_level1.py'
        suite = unittest.TestLoader().discover("unittest/text_case", pattern)
    else:
        suite = unittest.TestLoader().discover("unittest/text_case",
                                               "test*.py")  # 把目录名写，自动遍历目录下所有，必须是一个包！                                          # runner = unittest.TextTestRunner()使用Beautiful库就不用这个了
    run(suite)

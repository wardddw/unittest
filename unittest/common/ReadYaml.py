import yaml
import os
from main import Environ_online

DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class ReadYaml:
    @staticmethod
    def api_yaml(filename):
        """
        接口数据的读取方式
        :param filename:如何没有嵌套的，直接导入unittest目录下的包名例如api_yaml(notes).
        如果有嵌套的目录结构，例如api_yaml(notes/v3_notesvr_set_notecontent)
        :return:
        """
        with open(DIR + '/data' + '/' + filename + '/api_note.yaml', mode='r', encoding='utf-8') as f:
            return yaml.load(f, Loader=yaml.FullLoader)  # 读取yaml配置

    @staticmethod
    def common_yaml():
        with open(DIR + Environ_online + '/config.yaml', mode='r', encoding='utf-8') as f:
            return yaml.load(f, Loader=yaml.FullLoader)  # 读取yaml配置


# 实例方法：

if __name__ == '__main__':
    Ry = ReadYaml
    api_data = Ry.api_yaml('notes/test_notebody')
    # print(api_data)
    Cy = Ry.common_yaml()
    print(Cy)

from datetime import datetime
import inspect
import os
from colorama import Fore
from main import DIR
import time
import functools

current_time = datetime.now()  # 获取当前时间戳并转换格式
str_time = current_time.strftime("%Y-%m-%d")  # 获取年月日
log_dir = DIR + "/logs/"
log_name = "{}_info.log".format(str_time)  # 获取日志名
formatted_time = current_time.strftime('%H;%M;%S;.%f')[:-3]  # 获取当前时间戳并转换格式


def info_log(text):
    stack = inspect.stack()  # 获取当前执行路径
    code_path = f"{os.path.basename(stack[1].filename)}:{stack[1].lineno}"  # 获取当前执行路径
    text = f"【info】{code_path}-{formatted_time}  >>  {text}"
    print(Fore.GREEN + text)
    with open(log_dir + log_name, mode="a", encoding="utf-8") as f:
        f.write(text + '\n')


def error_log(text):
    stack = inspect.stack()  # 获取当前执行路径
    code_path = f"{os.path.basename(stack[1].filename)}:{stack[1].lineno}"  # 获取当前执行路径
    text = f"【error】{code_path}-{formatted_time}  >>  {text}"
    print(Fore.RED + text)
    with open(log_dir + log_name, mode="a", encoding="utf-8") as f:
        f.write(text + '\n')


def warn_log(text):
    stack = inspect.stack()  # 获取当前执行路径
    code_path = f"{os.path.basename(stack[1].filename)}:{stack[1].lineno}"  # 获取当前执行路径
    text = f"【warn】{code_path}-{formatted_time}  >>  {text}"
    print(Fore.YELLOW + text)
    with open(log_dir + log_name, mode="a", encoding="utf-8") as f:
        f.write(text + '\n')


def case_logs(func):
    "用例日志装饰器,写开头那几条"

    @functools.wraps(func)  # 不影响原有变量装饰器，固定用法
    def wrapper(*args, **kwargs):
        print(
            Fore.LIGHTCYAN_EX + "-------------------------------------------CASE START-------------------------------------------")
        class_name = args[0].__class__.__name__  # 获取装饰对象的类目
        methon_name = func.__name__  # 获取装饰对象的方法名
        docstring = inspect.getdoc(func)  # 获取方法注释
        info_log(f'TestCase:{methon_name} of class {class_name}')
        info_log(f'Describe:{docstring}')
        func(*args, **kwargs)
        return func

    return wrapper


def class_case_log(cls):  # 类级别的装饰器,给类下的每一条用例都套上case_logs，写开头那几条
    for name, method in inspect.getmembers(cls, inspect.isfunction):  # 获取函数名，类名
        if name.startswith('testCase'):  # 如果是testCase开头，就套上。
            setattr(cls, name, case_logs(method))  # 套上
    return cls


if __name__ == '__main__':
    warn_log("asdasd")

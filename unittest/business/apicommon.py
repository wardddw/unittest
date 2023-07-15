import requests
from common.customsLog import info_log
import time
from common.ReadYaml import ReadYaml
import functools

host = 'http://note-api.wps.cn'


class ApiCommon:
    @staticmethod
    def post(url, body, user_id, sid):  # body作为一个形参传入封装方法。
        headers = {
            'Cookie': f'wps_sid={sid}',
            'X-User-Key': str(user_id),
            'Content-Type': 'application/json'
        }
        info_log(f'request url:{url}')
        info_log(f'request heard:{headers}')
        info_log(f'request body:{body}')
        res = requests.post(url=url, headers=headers, json=body)
        info_log(f'response code:{res.status_code}')
        info_log(f'response text:{res.text}')  # 有可能不是Json，所以用text字符串打印就可以了。
        return res

    @staticmethod
    def get(url, user_id, sid):
        headers = {
            'Cookie': f'wps_sid={sid}',
            'X-User-Key': str(user_id),
            'Content-Type': 'application/json'
        }
        info_log(f'request url:{url}')
        info_log(f'request heard:{headers}')
        res = requests.get(url=url, headers=headers)
        info_log(f'response code:{res.status_code}')
        info_log(f'response text:{res.text}')  # 有可能不是Json，所以用text字符串打印就可以了。
        return res


"""批量造数据（信息主体）"""
Ap = ApiCommon()
path_note_info = '/v3/notesvr/set/noteinfo'
path_note_content = '/v3/notesvr/set/notecontent'
readYaml = ReadYaml
env_config = readYaml.common_yaml()


def note_info(count, wps_sid, x_user_key):
    noteId_list = []
    for i in range(1, count):
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
        Ap.post(url=host + path_note_info, sid=wps_sid, body=body_note_info,
                user_id=x_user_key)
        Ap.post(url=host + path_note_content, sid=wps_sid, body=body_note_content,
                user_id=x_user_key)
        i = i + 1
        noteId_list.append(note_id)
    info_log(f'循环创建{count - 1}条便签，便签noteId分别为{noteId_list}')
    return noteId_list


def note_info_look(x_user_key):
    userid = x_user_key
    startindex = '0'
    rows = '999'
    get_note_path = f'/v3/notesvr/user/{userid}/home/startindex/{startindex}/rows/{rows}/notes'
    res_get = Ap.get(url=host + get_note_path, user_id=env_config['x_user_key'], sid=env_config['wps_sid'])
    return res_get


#删除所有首页便签数据


def note_info_delete():
    """查询首页便签"""
    userid = env_config['x_user_key']
    startindex = '0'
    rows = '999'
    get_note_path = f'/v3/notesvr/user/{userid}/home/startindex/{startindex}/rows/{rows}/notes'
    info_log('自动查询首页所有便签')
    res_get = Ap.get(url=host + get_note_path, user_id=env_config['x_user_key'], sid=env_config['wps_sid'])
    info_log('循环删除首页便签')
    delete_info_path = '/v3/notesvr/delete'
    if len(res_get.json()['webNotes']) != 0:
        for key in res_get.json()['webNotes']:
            noteId = key['noteId']
            body = {
                'noteId': noteId}
            Ap.post(url=host + delete_info_path, user_id=env_config['x_user_key'], sid=env_config['wps_sid'], body=body)
    info_log('查询回收站便签便签')
    note_recycle_path = f'/v3/notesvr/user/{userid}/invalid/startindex/{startindex}/rows/{rows}/notes'
    res_recycle = Ap.get(url=host + note_recycle_path, user_id=env_config['x_user_key'], sid=env_config['wps_sid'])
    info_log('循环删除回收站便签')
    dele_recycle_path = '/v3/notesvr/cleanrecyclebin'
    if len(res_recycle.json()['webNotes']) != 0:
        for key in res_recycle.json()['webNotes']:
            noteId = key['noteId']
            body = {
                'noteIds': [noteId]}
            Ap.post(url=host + dele_recycle_path, user_id=env_config['x_user_key'], sid=env_config['wps_sid'],
                    body=body)



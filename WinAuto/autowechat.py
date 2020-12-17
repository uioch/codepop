from psutil import process_iter
from pywinauto import *

def get_pid():
    PID = process_iter()
    name = ''
    pid_num = 0
    for pid_temp in PID:
        pid_dic = pid_temp.as_dict(attrs = ['pid','name'])
        if pid_dic ['name'] == 'WeChat.exe':
            name = pid_dic ['name']
            pid_num = pid_dic ['pid']
            break
    if name =='WeChat.exe':
        return pid_num
    else :
        return False


def get_text(win):
    data = ''
    try:
        data = win.Edit2.get_value()
    except:
        data = '-ERR-'
    return data

def get_users(win):
    user_lis = []
    try:
        conunacation = win.child_window(title = "会话",control_type = "List")
        position = conunacation.rectangle()
        mouse.click(button = 'left',coords = (position.left + 100 ,position.top + 10 ))
        
        users = conunacation.children()
        for user in users:
            user_lis.append(user.window_text())
    except:
        pass
    return user_lis


app = Application(backend = 'uia')

app.connect(process = get_pid())

# 定位到微信窗口
win = app['微信']

print(get_text(win))
print(get_users())
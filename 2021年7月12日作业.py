import paramiko
import time
import sys


def qytang_multicmd(ip, username, password, cmd_list, enable='', wait_time=2, verbose=True):
    ssh = paramiko.SSHClient()  # 创建SSH Client
    ssh.load_system_host_keys()  # 加载系统SSH密钥
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # 添加新的SSH密钥
    ssh.connect(ip, port=22, username=username, password=password, timeout=5, compress=True)  # SSH连接
    chan = ssh.invoke_shell()  # 激活交互式shell
    time.sleep(1)  # 等待网络设备回应
    x = chan.recv(2048).decode()  # 获取路由器返回的信息
    if enable and '>' in x:
        chan.send('enable'.encode())  # 发送命令
        chan.send('\n')  # 回车
        chan.send(enable.encode())
        chan.send('\n')
        time.sleep(wait_time)
    elif not enable and '>' in x:
        print('需要配置enable密码！')
        return
    for cmd in cmd_list:
        chan.send(cmd.encode())
        chan.send('\n')
        time.sleep(wait_time)
        x = chan.recv(40960).decode()
        if verbose:
            print(x)
    chan.close()
    ssh.close()


if __name__ == '__main__':
    qytang_multicmd('1.1.1.200', 'cisco', 'cisco', ['terminal length 0', 'show ver', 'config ter', 'router ospf 1'])

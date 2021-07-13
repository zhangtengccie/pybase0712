import paramiko
import time
import sys


def ssh_multi_cmd(ip, username, password, cmd_list, verbose=True):
    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, port=22, username=username, password=password, timeout=5, compress=True)

    chan = ssh.invoke_shell()
    time.sleep(1)
    x = chan.recv(2048).decode()

    for cmd in cmd_list:
        chan.send(cmd.encode())
        chan.send(b'\n')
        time.sleep(2)
        x = chan.recv(40960).decode()
        if verbose:
            print(x)

    chan.close()
    ssh.close()


if __name__ == '__main__':
    ssh_multi_cmd('1.1.1.200', 'cisco', 'cisco', ['terminal length 0', 'show ver', 'config ter', 'router ospf 1'])

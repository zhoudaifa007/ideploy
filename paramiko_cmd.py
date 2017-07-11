# -*- coding:utf-8 -*-
import paramiko
from deploy_config import ConfigHandler


class SftpCmd(object):
    def __init__(self, host, port, user, password):
        self.host = host
        self.port = port
        self.user = user
        self.password = password

    def connect(self):
        self.ssh_client = paramiko.SSHClient()
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh_client.connect(self.host, self.port, self.user, self.password)
        print("connect sftp success")

    def execCmd(self, cmd):
        self.ssh_client.exec_command(cmd)

    def close(self):
        self.ssh_client.close()

    def test(self):
        cmd1 = "cd /app/zdf"
        self.ssh_client.exec_command(cmd1)
        cmd2 = "cd /app/zdf;ls -l"
        std_in, std_out, std_err = self.ssh_client.exec_command(cmd2)
        for line in std_out:
            print(line.strip("\n"))


if __name__ == '__main__':
    configHandler = ConfigHandler()
    host = configHandler.getProperty('remote', 'ip')
    port = configHandler.getProperty('remote', 'port')
    user = configHandler.getProperty('remote', 'user')
    passWord = configHandler.getProperty('remote', 'passWord')
    sftpCmd = SftpCmd(host, port, user, passWord)
    sftpCmd.connect()

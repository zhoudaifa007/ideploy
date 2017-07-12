# -*- coding:utf-8 -*-
import paramiko
import time
import threading
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
        self.chan = self.ssh_client.invoke_shell()
        print("connect sftp success")

        thread = threading.Thread(target=self.process)
        thread.daemon = True
        thread.start()

    def execCmd(self, cmd):
        self.ssh_client.exec_command(cmd)
        print("excute commond %s success", cmd)

    def invokeShell(self, shell):
        self.chan.send(shell + "\n")
        time.sleep(2)
        print ("invoke shell success" + shell)

    def process(self):
        while True:
            # Print data when available
            if self.chan != None and self.chan.recv_ready():
                alldata = self.chan.recv(1024)
                while self.chan.recv_ready():
                    alldata += self.chan.recv(1024)
                strdata = str(alldata, "utf8")
                strdata.replace('\r', '')
                print(strdata, end="")
                if (strdata.endswith("$ ")):
                    print("\n$ ", end="")

    def close(self):
        self.ssh_client.close()

    def test(self):
        cmd1 = "cd /app/zdf"
        self.ssh_client.exec_command(cmd1)
        cmd2 = "cd /app/zdf;ls -l"
        std_in, std_out, std_err = self.ssh_client.exec_command(cmd2)
        for line in std_out:
            print(line.strip("\n"))
        print("hello")
        std_in, std_out, std_err = self.ssh_client.exec_command("env")
        for line in std_out:
            print(line.strip("\n"))

    def testStop(self):
        stopCmd = "cd /usr/local/jdk/bin;" + configHandler.getProperty('remote', 'filePath') + "stop.sh"
        std_in, std_out, std_err = self.ssh_client.exec_command(stopCmd)
        for line in std_out:
            print(line.strip("\n"))

    def testStart(self):
        startCmd = configHandler.getProperty('remote', 'filePath') + "start.sh"
        self.chan.send(startCmd)
        print(self.chan.recv(2048))


if __name__ == '__main__':
    configHandler = ConfigHandler()
    host = configHandler.getProperty('remote', 'ip')
    port = configHandler.getProperty('remote', 'port')
    user = configHandler.getProperty('remote', 'user')
    passWord = configHandler.getProperty('remote', 'passWord')
    sftpCmd = SftpCmd(host, port, user, passWord)
    sftpCmd.connect()
    # sftpCmd.test()
    sftpCmd.testStart()
    # sftpCmd.testStop()

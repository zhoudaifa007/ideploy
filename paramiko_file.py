# -*- coding:utf-8 -*-
import paramiko
import time
from deploy_config import ConfigHandler


class SftpFile(object):
    def __init__(self, host, port, user, password):
        self.host = host
        self.port = port
        self.user = user
        self.password = password

    def connect(self):
        self.t = paramiko.Transport((self.host, self.port))
        self.t.connect(username=self.user, password=self.password)
        self.sftp = paramiko.SFTPClient.from_transport(self.t)
        print("connect sftp server success")

    def upload(self, src, dst):
        self.sftp.put(src, dst)
        print("send file success")

    def rename(self, src, dst):
        self.sftp.rename(src, dst)
        print("rename file success")

    def remove(self, path):
        self.sftp.remove(path)
        print ("delete file success")

    def close(self):
        self.t.close()
        self.sftp.close()


if __name__ == '__main__':
    configHandler = ConfigHandler()
    host = configHandler.getProperty('remote', 'ip')
    port = configHandler.getProperty('remote', 'port')
    user = configHandler.getProperty('remote', 'user')
    passWord = configHandler.getProperty('remote', 'passWord')
    src = configHandler.getProperty('local', 'filePath') + configHandler.getProperty('local', 'fileName')
    dst = configHandler.getProperty('remote', 'filePath') + configHandler.getProperty('local', 'fileName')
    mySFTP = SftpFile(host, port, user, passWord)
    mySFTP.connect()
    mySFTP.upload(src, dst)
    remoreSoltLink = configHandler.getProperty('remote', 'filePath') + configHandler.getProperty('remote', 'fileName')
    remoreDst = (remoreSoltLink.split('.'))[0] + '.' + time.strftime("%Y%m%d%H%M", time.localtime()) + '.jar'
    print (remoreDst)
    mySFTP.rename(dst, remoreDst)
    mySFTP.remove(remoreSoltLink)
    mySFTP.close()

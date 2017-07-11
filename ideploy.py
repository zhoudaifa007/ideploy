# -*- coding:utf-8 -*-
import time
from paramiko_cmd import SftpCmd
from paramiko_file import SftpFile
from deploy_config import ConfigHandler


class DeployJar(object):
    def __init__(self):
        configHandler = ConfigHandler()
        host = configHandler.getProperty('remote', 'ip')
        port = configHandler.getProperty('remote', 'port')
        user = configHandler.getProperty('remote', 'user')
        passWord = configHandler.getProperty('remote', 'passWord')
        self.sftp_file = SftpFile(host, port, user, passWord)
        self.sftp_cmd = SftpCmd(host, port, user, passWord)

    def sendFile(self):
        # step1:上传文件
        configHandler = ConfigHandler()
        src = configHandler.getProperty('local', 'filePath') + configHandler.getProperty('local', 'fileName')
        dst = configHandler.getProperty('remote', 'filePath') + configHandler.getProperty('local', 'fileName')
        self.sftp_file.connect()
        self.sftp_file.upload(src, dst)
        # step2:重命名文件
        remoreSoltLink = configHandler.getProperty('remote', 'filePath') + configHandler.getProperty('remote', 'fileName')
        self.remoreDst = (remoreSoltLink.split('.'))[0] + '.' + time.strftime("%Y%m%d%H%M", time.localtime()) + '.jar'
        self.sftp_file.rename(dst, self.remoreDst)
        # step3:删除文件
        self.sftp_file.remove(remoreSoltLink)
        self.sftp_file.close()

    def sendCmd(self):
        configHandler = ConfigHandler()
        self.sftp_cmd.connect()
        # step4：建立链接文件
        remoreSoltLink = configHandler.getProperty('remote', 'filePath') + configHandler.getProperty('remote','fileName')
        createLink = "ln -s " + self.remoreDst + " " + remoreSoltLink
        self.sftp_cmd.execCmd(createLink)
        # step5:停止进程
        stopCmd = configHandler.getProperty('remote', 'filePath') + "bin/stop.sh"
        self.sftp_cmd.execCmd(stopCmd)
        startCmd = configHandler.getProperty('remote', 'filePath') + "bin/start.sh"
        self.sftp_cmd.execCmd(startCmd)
        # step6:启动进程
        self.sftp_cmd.close()

if __name__ == '__main__':
    deployJar = DeployJar()
    deployJar.sendFile()
    deployJar.sendCmd()

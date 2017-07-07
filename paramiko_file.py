# -*- coding:utf-8 -*-
import paramiko

host  = '10.10.10.10'
port = 22
user = 'root'
password = '******'
src = "F:/work1/cloud_dts1/cloud-dts-parent/cloud-dts-track/cloud-dts-track-provider/target/cloud-dts-track-provider-0.0.1-SNAPSHOT.jar"
dst = "/app/zdf/cloud-dts-track-provider-0.0.1-SNAPSHOT.jar"

class SFTP:
    def __init__(self,host,port, user, password):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
    def connect(self):
        self.t = paramiko.Transport((self.host, self.port))
        self.t.connect(username=user, password=password)
        self.sftp = paramiko.SFTPClient.from_transport(self.t)
    def upload(self,src, dst):
        self.sftp.put(src, dst)
    def close(self):
        self.t.close()
        self.sftp.close()

if __name__ == '__main__':
    mySFTP = SFTP(host,port,user,password)
    mySFTP.connect()
    mySFTP.upload(src,dst)
    mySFTP.close()

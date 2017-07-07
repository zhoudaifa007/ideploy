# -*- coding:utf-8 -*-
import paramiko

host  = '10.10.10.10'
user = 'root'
password = '******'

def sftp_upload_file(server_path, local_path):
    t = paramiko.Transport((host, 22))
    t.connect(username=user, password=password)
    sftp = paramiko.SFTPClient.from_transport(t)
    sftp.put("F:/work1/cloud_dts1/cloud-dts-parent/cloud-dts-track/cloud-dts-track-provider/target/cloud-dts-track-provider-0.0.1-SNAPSHOT.jar", "/app/zdf/cloud-dts-track-provider-0.0.1-SNAPSHOT.jar")
    t.close()


if __name__ == '__main__':
    sftp_upload_file("/root/bug.txt", "D:/bug.txt")
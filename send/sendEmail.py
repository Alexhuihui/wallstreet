# -*- coding:utf-8 -*-
import smtplib
from email.header import Header
from email.mime.text import MIMEText
import datetime
import time
from databaseconnection import dao

class Sender(object):

    def __init__(self):
        self.mail_host = "smtp.163.com"  # SMTP服务器
        self.mail_user = "17770848782"  # 用户名
        self.mail_pass = "QWErty123"  # 授权密码，非登录密码

        self.sender = "17770848782@163.com"
        self.receivers = ["2930807240@qq.com"]
        self.dao = dao.Dao()

    #从数据库中查询数据并组合成字符串
    def selectdata(self):
	    content = self.dao.select()
	    return content

    #控制函数
    def main(self, m=0, h=21):
        while True:
            now = datetime.datetime.now()
            print(now.hour, now.minute)
            # 每天晚上9点停止程序
            if now.hour >= h:
                break
                # 每隔一个小时发送一次邮件
            content = self.selectdata()
            self.sendemail(content)
            time.sleep(120)

    #发送邮件
    def sendemail(self, content='我用Python'):
        title = '华尔街快讯'
        message = MIMEText(content, 'plain', 'utf-8')  # 内容, 格式, 编码
        message['From'] = "{}".format(self.sender)
        message['To'] = ",".join(self.receivers)
        message['Subject'] = title

        try:
            smtpObj = smtplib.SMTP_SSL(self.mail_host, 465)  # 启用SSL发信, 端口一般是465
            smtpObj.login(self.mail_user, self.mail_pass)  # 登录验证
            smtpObj.sendmail(self.sender, self.receivers, message.as_string())  # 发送
            print("mail has been send successfully.")
        except smtplib.SMTPException as e:
            print(e)

if __name__ == '__main__':
    sender = Sender()
    sender.main()
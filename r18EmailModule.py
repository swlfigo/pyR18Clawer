# -*- coding:utf-8 -*-
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from email.utils import formataddr

sender = '发件人邮箱'
smtpServer = '发件人smtp'
userName = '邮箱用户名'
password = '邮箱PassWord'
smtpPort = 25

class r18EmailModule(object):

    def __init__(self):
        self.emailList = []
        #存放地址的数组
        self.fileContent = []


    def startSendEmail(self):

        #读取邮箱地址
        self.emailPath = os.path.dirname(os.path.abspath("__file__"))
        self.emailPath = os.path.join(self.emailPath , 'emailList.txt')
        # 获取EmailList
        try:
            f = open(self.emailPath, 'r')
            line = f.readlines()
            for emailaddress in line:
                self.emailList.append(emailaddress)
            f.close()
        except:
            print('open email path error')
            pass

        if len(self.emailList) == 0:
            return
        # print(self.emailList)


        # 构造MIMEMultipart对象做为根容器
        msg = MIMEMultipart()
        text_msg = MIMEText("Python学习资料\n", _charset="utf-8")
        msg.attach(text_msg)

        if len(self.fileContent) > 0:
            for fileName in self.fileContent:
                try:
                    part = MIMEBase('application', 'octet-stream')
                    data = open(fileName, 'rb').read()
                    part.set_payload(data)
                    encoders.encode_base64(part)
                    part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(fileName))
                    msg.attach(part)
                except Exception as e:
                    print('打开附件文件失败')
                    print(e)
                    pass

        # 可以打印出和SMTP服务器交互的所有信息
        # set_debuglevel(1)
        # server.set_debuglevel(1)

        # 设置根容器属性
        msg['From'] = sender
        msg['Subject'] = "邮件主题"

        try:
            print('开始发送邮件')
            
            #此处邮件服务商信息更改
            #此例子使用SSL发送，可以更改为 纯smtp 25端口发送
            #详情百度
            smtp = smtplib.SMTP(smtpServer,587)
            smtp.set_debuglevel(1)
            
            # smtp.connect(smtpServer, 587)
            smtp.ehlo()
            smtp.starttls()
            smtp.login(userName, password)
            smtp.sendmail(sender, self.emailList, msg.as_string())
            smtp.close()
        except Exception as e:
            print(e)
            print('发送邮件失败')

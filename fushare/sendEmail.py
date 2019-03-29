# encoding: UTF-8
'''
Created on 2019年01月06日
@author: lowin
@contact: li783170560@126.com

发送邮件
'''

import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart

def sendEmail(msg, fromEmail, password, toEmail, host, port, attachName = False, attachRoot = False, SSL = False):
    """
            发送一封邮件
        Parameters
        ------
            msg: string 邮件的主题
            fromEmail: string 发送邮件的邮箱          
            password: string 发送邮件的密码
            toEmail: string 接收邮件的邮箱
            host：string 邮箱服务器地址（邮箱服务商查询）
            port：string 端口（邮箱服务商查询）
            attachName：string 单个附件名字/ list 多个附件名字列表
            attachRoot： 附件本机目录
            SSL： bool 是否使用ssl加密协议（QQ邮箱需要使用）
        Return
        -------
            None
    """


    message = MIMEMultipart()
    message['From'] = fromEmail
    message['To'] =  toEmail
    message['Subject'] = Header(msg)

    if bool(attachName) and bool(attachRoot):
        if type(attachName) == type(''):
            part = MIMEText(open(attachRoot+attachName, 'rb').read(), 'base64', 'utf-8')
            part.add_header('Content-Disposition', 'attachment', filename=attachName)
            message.attach(part)
        elif type(attachName) == type([]):
            for name in attachName:
                part = MIMEText(open(attachRoot+name, 'rb').read(), 'base64', 'utf-8')
                part.add_header('Content-Disposition', 'attachment', filename=name)
                message.attach(part)
    if SSL:
        smtpObj = smtplib.SMTP_SSL()
    else:
        smtpObj = smtplib.SMTP()
    smtpObj.connect(host,port)
    smtpObj.login(fromEmail,password)
    smtpObj.sendmail(fromEmail, toEmail, message.as_string())
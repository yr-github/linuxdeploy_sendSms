import requests
import json
import sqlpy
import logging
import time
import smtplib
from email.mime.text import MIMEText


Dbpath = "/mnt/data/com.android.providers.telephony/databases/mmssms.db"#数据库地址，记得必须挂载
useWechat = True #@TRUE =使用企业微信信息 @False=使用邮件发送信息

#企业微信配置
AgentId = ""
CropId = ""
Secret = ""
Touser = ""
Touser = " WangWu|ZhaoSi "
#邮箱配置，以163为例
smtpHost = 'smtp.163.com'#邮箱发送配置
neateasyUser = 'xxx@163.com'# 163用户名
neateaseCode = ''# s授权码
sendEmail = 'xxxx@163.com'# 邮件发送方邮箱地址
receiveEmails = ['xxx@qq.com','xxx@gmail.com']#可以写多个接收方 qq邮箱记得添加白名单



log_name = 'runtime.log'
LOGGER = logging.getLogger(__name__)
fh = logging.FileHandler(encoding='utf-8', mode='a', filename=log_name)
logging.basicConfig(handlers=[fh], format='[%(asctime)s %(levelname)s]<%(process)d> %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)

def refreshAccesToken():
    try:
        url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=%s&corpsecret=%s" %(CropId,Secret)
        resp = requests.get(url)
        result = json.loads(resp.content.decode('utf-8'))["access_token"]
        LOGGER.info("重新获取获取accestoken成功")
    except :
        LOGGER.info("获取accestoken失败")
        result = 0
    return result

def sendSmsWecht(content):
    accesstoken ="useless"
    try:
        while True:
            LOGGER.info("开始发送信息")
            LOGGER.info(content[1])
            sns = "FROM:" + content[0] + "\n" +content[1]
            url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=%s" %(accesstoken)
            #url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=%s" % (acc)
            body = {
                'touser':Touser,
                'msgtype': 'text',
                'agentid':AgentId,
                'text':{'content':sns,},
                'safe': 0,
            }
            r = requests.post(url,data=json.dumps(body, ensure_ascii = False).encode('utf-8'))
            result = json.loads(r.content.decode('utf-8'))
            LOGGER.info(result['errcode'])
            if result['errcode'] == 40014 or result['errcode'] == 42001:
                accesstoken = refreshAccesToken()
            if result['errcode'] == 0:
                sqlObj = sqlpy.OperateSQL(Dbpath, LOGGER)
                sqlObj.updateSms()
                del sqlObj
                LOGGER.info("信息发送成功")
                break
    except:
        LOGGER.info("发送信息失败,将循环重发")

def sendSmsEmail(content):
    message = MIMEText(content[1], 'plain', 'utf-8')
    message['Subject'] = "From: " + content[0]
    message['From'] = sendEmail
    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(smtpHost, 25)
        smtpObj.login(neateasyUser, neateaseCode)
        smtpObj.sendmail(sendEmail, receiveEmails, message.as_string())
        smtpObj.quit()
        sqlObj = sqlpy.OperateSQL(Dbpath, LOGGER)
        sqlObj.updateSms()
        del sqlObj
        LOGGER.info("邮件发送成功")
    except smtplib.SMTPException as e:
        LOGGER.info("邮件发送失败")

def sendLoop(path):
    while True:
        sqlObj = sqlpy.OperateSQL(path,LOGGER)
        contents = sqlObj.readSms()
        if contents!=0:
            if useWechat :
                for content in contents:
                    sendSmsWecht(content)
            else:
                for content in contents:
                    sendSmsEmail(content)
        else:
            time.sleep(1)
            LOGGER.info("数据库错误,将循环读取")
        del sqlObj



sendLoop(Dbpath)

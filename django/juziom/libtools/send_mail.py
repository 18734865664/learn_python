#! /bin/env python
# -*- encoding: utf-8 -*-
import smtplib
import sys
import time
from email.header import Header
from email.mime.text import MIMEText

if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')

host = "smtp.exmail.qq.com"  # 设置服务器
user = "update@happyjuzi.com"  # 用户名
password = "Juzi@123"
_mailFrom = "Update"
fromMail = "update@happyjuzi.com"


def Updatesendmail(project_name, username, jobid, mailto, change_content, cc=''):
    messages = str('''项目:%s \n %s:%s\n 任务ID:%s \n 请查看详细结果''' % (project_name, username, change_content, jobid))

    subject = "%s" % project_name + " Code update " + time.strftime('%Y-%m-%d %H:%M:%S')
    me = ("%s<" + fromMail + ">") % (Header(_mailFrom, 'utf-8'),)
    msg = MIMEText(messages, 'plain', 'utf-8')
    # if not isinstance(subject,unicode):
    #    subject = unicode(subject)
    msg['Subject'] = Header(subject, 'utf-8')
    msg['From'] = me
    msg['To'] = mailto
    msg['Cc'] = cc
    msg["Accept-Language"] = "zh-CN"
    msg["Accept-Charset"] = "ISO-8859-1,utf-8"

    # print me,[mailto,cc], msg.as_string()

    if msg['Cc'] is None:
        try:
            s = smtplib.SMTP_SSL()
            s.connect(host, 465)
            s.login(user, password)
            s.sendmail(me, mailto, msg.as_string())
            s.close()
            print u"发送成功"
        except Exception, e:
            print str(e)
            return False
    else:
        try:
            s = smtplib.SMTP_SSL()
            s.connect(host, 465)
            s.login(user, password)
            list_c = cc.split(',')
            list_c.append(mailto)

            s.sendmail(me, list_c, msg.as_string())
            s.close()
            print u"发送成功"
        except Exception, e:
            print str(e)
            return False


if __name__ == '__main__':
    gitsendmails("管理员", "橘子API", 123, "aa@happyjuzi.com", "测试http://192.168.10.111/history/githistory", cc='aa@qq.com')

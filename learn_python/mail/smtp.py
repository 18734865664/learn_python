#! /usr/local/python3/bin/python3
# encoding: utf-8

from email.mime.text  import MIMEText
import smtplib
from email.utils import formataddr


from_addr = "569776435@qq.com"
password = "tdcxngprhpgmbbic"
to_addr = "qiangguo22@creditease.cn"
smtp_server = "smtp.qq.com"

msg = MIMEText("hello, send by gq...", 'plain', 'utf-8')
msg["From"] = formataddr(["guoqiang", from_addr])
msg['To'] = formataddr(["yx", to_addr])
msg["Subject"] = "测试测试"

server = smtplib.SMTP_SSL(smtp_server, 465)

server.set_debuglevel(1)
server.login(from_addr, password)
server.sendmail(from_addr, [to_addr], msg.as_string())
server.quit()

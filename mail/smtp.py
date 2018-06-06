#! /usr/local/python3/bin/python3
# encoding: utf-8
# author: qiangguo
# last_modify: 20180515

'''
    学习使用python smptlib 发送邮件

'''

from email.mime.text  import MIMEText    # 构建文本实例
from email.mime.multipart import MIMEMultipart  # 构建多媒体形式
from email.mime.image import MIMEImage  # 构建图片形式
import smtplib
from email.utils import formataddr


# 定义变量
from_addr = "******@qq.com"
password = "tdcxngprhpgmbbic"     # 在qq邮箱生成的三方客户端使用的密码
to_addr = "qiangguo22@*****"
smtp_server = "smtp.qq.com"



def mail():
    
    # 定义邮件内容相关
    # 实例化多媒体邮件实例
    msg = MIMEMultipart(alternative)    # 传递alternative作为唯一的参数实例化，不传这个参数，有的邮件服务器，attach进去的纯文本、图片回作为消息的附件传输
    
    # 定义文本组件  plain   html
    # msg = MIMEText("hello, send by gq...", 'plain', 'utf-8')  # 邮件正文内容，普通文本
    msg_body = """
    <h1> hello </h1>
    <h2> world </h2>
    <img alt="" src="cid:image1">"""    # 引用图片，需要将该图片作为附件发送，定义“Content-ID” 进行引用
    msg_text = MIMEText(msg_body, 'html', 'utf-8')  # 邮件正文内容，html文件
    
    # 定义图片实例
    fp = open("./p1-1.png", "rb")
    msg_image = MIMEImage(fp.read())
    fp.close()
    msg_image.add_header("Content-ID", "<image1>")     # 定义Content-ID，供文本组件引用

    # 创建附件
    msg_attach = MIMEText(open('./attach.txt', "rb").read(), 'base64', 'utf-8')
    msg_attach["Content-Type"] = "application/octet-stream"
    msg_attach["Content-Disposition"] = "attachment; filename='ceshi.txt'"     # 这里的filename就是邮件中显示的附件名
    
    # 将页面组件嵌入多媒体邮件实例
    msg.attach(msg_text)
    msg.attach(msg_image)
    msg.attach(msg_attach)
    
    # 定义邮件实例属性
    msg["From"] = formataddr(["guoqiang", from_addr])  # 显示的发件人信息
    msg['To'] = formataddr(["yx", to_addr])            # 显示的收件人信息
    msg["Subject"] = "测试测试"                        # 显示的title
    
    try:
        # 实例化smtp
        # server = smtplib.SMTP(smtp_server, 25)      # 非ssl 方式连接
        server = smtplib.SMTP_SSL(smtp_server, 465)   # ssl 连接
        # 开启debug 会显示发送邮件的详细过程
        server.set_debuglevel(1)
        # 登陆
        server.login(from_addr, password)
        # 发送邮件
        # import pdb; pdb.set_trace()
        server.sendmail(from_addr, [from_addr], msg.as_string())
        print("邮件发送成功")
    except Exception:
        print("邮件发送失败")
    finally:
        server.quit()
    
if __name__ == "__main__":
    mail()

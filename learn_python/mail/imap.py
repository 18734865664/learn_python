#! /usr/local/python3/bin/python3
# encoding: utf-8
# author: qiangguo
# last_modify: 20180515

"""
    imaplib 模块定义了三个类：
    IMAP4：连接IMAP4服务器
    IMAP4_SSL：通过SSL加密的套接字，连接IMAP4服务器
    IMAP$_stream：通过一个类似文件的对象接口与IMAP4服务器交互
    
    POP3和IMAP协议的区别:
    虽然这两个协议都是从邮件服务器那里下载邮件到本地的协议，但是不同的是IMAP提供跟邮件服务器的双向通信，也即在客户端所作的更改会反馈给服务器端，跟服务器端形成同步（例如删除邮件，创建文件夹等等的操作）。而POP3是单向通信的，即下载邮件到本地就算了，所作的更改都只是在客户端，不会反映到服务器端。所以使用IMAP协议也会更便捷，体验更好，更可靠。
    官方文档：https://docs.python.org/3.6/library/imaplib.html
"""

from imaplib import IMAP4_SSL
import email

# 定义变量
imap_server = "pop.qq.com" 
user = "******@qq.com"
password = "tdcxngprhpgmbbic" 

def recevie_mail():
   try:
       # 实例化imap服务器
       recevie_server = IMAP4_SSL(imap_server)
       recevie_server.login(user, password)
       # recevie_server.list()    # 查看所有的文件夹(IMAP可以支持创建文件夹)
       # recevie_server.select("Inbox")  # 默认选择文件夹是“INBOX”
       # recevie_server.search(None, "ALL")  # 两个参数，第一个是charset，通常为None(ASCII),第二个参数决定检索的关键字,ALL表示所有邮件，SEEN表示已读邮件，NEW表示未读邮件，参考http://afterlogic.com/mailbee-net/docs/MailBee.ImapMail.Imap.Search_overload_2.html
       # recevie_server.fetch(messages_set, message_parts), 两个参数，第一个是邮件的索引，第二个是决定是抓取message中的哪些部分，参考文档http://james.apache.org/server/rfclist/imap4/rfc2060.txt
       recevie_server.select()
       print("+" * 10 + "获取单份邮件" + "+" * 10)
       import pdb; pdb.set_trace()
       print(recevie_server.fetch(recevie_server.select("Inbox")[1][0].decode(), "(BODY[HEADER])")[1][0][1].decode())
       print("+" * 10 + "获取多份邮件" + "+" * 10)
       for i in recevie_server.fetch("98:100", "(BODY[HEADER])")[1]:
           try:
               print(i[1].decode())
               print( "+" * 30 + "\n")
           except:
               pass

   except Exception as err:
       print(err)
   finally:
       recevie_server.logout()


if __name__ == "__main__":
    recevie_mail()
        


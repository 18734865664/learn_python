#! /usr/local/python3/bin/python3
# encoding: utf-8
# author: qiangguo
# last_modify: 20180515

from poplib import POP3_SSL

# 定义变量
pop_server = "pop.qq.com"
user = "569776435@qq.com"
password = "tdcxngprhpgmbbic"


def recevie_mail():
    try:
        # 实例化pop服务器
        recevie_server = POP3_SSL(pop_server)    # 开启SSL认证的邮箱服务器使用 POP3_SSL, 未开启的使用POP3
        recevie_server.set_debuglevel(1)
        recevie_server.user(user)                # user 向服务器传递用户名，同pass_ 方法一样，通过则会导致状态转变
        recevie_server.pass_(password)           # 通过认证，会返回“+OK ready”, 未通过会引发 poplib.error_proto异常
        # recevie_server.stat()                    # 请求服务器返回关于邮箱的统计资料，二元元祖（邮件总数，总字节数）
        # recevie_server.list()                    # 返回邮件信息，三元元组，（返回状态，消息列表，消息的大小）,消息列表是二元元组组成的列表（邮件索引，邮件字节数）,如果指定参数，会返回指定邮件的信息
        # recevie_server.dele(num)                 # 将指定邮件标记为删除，quit()函数执行时真正删除
        # recevie_server.rset()                    # 重置所有标记为删除的邮件，用于撤销dele命令
        
        
        # 获取最后一封邮件
        # 调用retr函数收取指定的邮件, 返回一个三元元组，(服务器响应，消息的所有行，消息的字节数)，该邮件设置为已读
        rsp, msg, siz = recevie_server.retr(recevie_server.stat()[0])
        sep = msg.index(b'')  # RFC 2822  要求消息头和正文之间需要用空行隔开，所以遇到空行，说明后面的是正文
        print("rsp: ", rsp)     # 服务器返回信息“b'+OK'”
        print("siz: ", siz)     # 消息的字节数
        recevie_body = msg[sep + 1 :]
        print(recevie_body)
    except Exception as err:
        print(err)
    finally:
        recevie_server.quit()                    # 退出
    
    
if __name__ == "__main__":
    recevie_mail()

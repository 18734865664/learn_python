#! /usr/local/python3/bin/python3
# encoding: utf-8

import tornado.iploop
import tornado.web

class MainHandler(tornado,web.RequestHandler):
    def get(self):
        self.write("Hello, world")
    
    application = tornado.web.Application([
    (r'/', MainHandler),
)

if __name__ == "__main__":
    application.listen(8889)
    tornado.iploop.IOLoop.instance().start()

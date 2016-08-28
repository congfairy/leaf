import tornado.ioloop
import tornado.web
import tornado.options
import os
from tornado import gen

GB = 1024 * 1024 * 1024
chunk_size = 1024
class StreamingRequestHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @gen.coroutine
    def get(self):
        total_sent = 0
        file_object = open('./logclient','rb')
        pos = 500
        file_object.seek(pos,0)
        self.set_header('Content-Length', os.path.getsize('./logclient'))
        print("content_length",os.path.getsize('./logclient'))
        while True:
                print("position is",pos)
                chunk = file_object.read(chunk_size)
                pos = pos + chunk_size
                file_object.seek(pos,1)
                if not chunk:
                   break   
                self.write(chunk)
                yield gen.Task(self.flush)
                total_sent += len(chunk)
                print("sent",total_sent)
         
        self.finish()


if __name__ == "__main__":
    tornado.options.parse_command_line()
    application = tornado.web.Application([
        (r"/", StreamingRequestHandler),
    ])
    application.listen(8880)
    tornado.ioloop.IOLoop.instance().start()

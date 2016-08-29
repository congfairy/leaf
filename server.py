import tornado.ioloop
import tornado.web
import tornado.options
from tornado import gen

GB = 1024 * 1024 * 1024
chunk_size = 1024

def read_in_chunks(infile, chunk_size=1024*64):
   chunk = infile.read(chunk_size)
   while chunk:
       yield chunk
       chunk = infile.read(chunk_size)


class StreamingRequestHandler(tornado.web.RequestHandler):
   @tornado.web.asynchronous
   @gen.coroutine
   def get(self):
       # ideally you would send in the get request what file you want to send
       # back as right now this is limited to what is hard coded in
       total_sent = 0

       with open('./logclient', 'rb') as infile:
           for chunk in read_in_chunks(infile):
               self.write(chunk)
               yield gen.Task(self.flush)
               total_sent += len(chunk)
               print("sent",total_sent)

       self.finish()


if __name__ == "__main__":
   tornado.options.parse_command_line()
   application = tornado.web.Application([(r"/", StreamingRequestHandler),])
   application.listen(8880)
   tornado.ioloop.IOLoop.instance().start()


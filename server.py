import tornado.ioloop
import tornado.web
import tornado.options
from tornado import gen
import os,sys
from stat import *

GB = 1024 * 1024 * 1024
chunk_size = 1024

def read_in_chunks(infile, chunk_size=1024*64):
   chunk = infile.read(chunk_size)
   while chunk:
       yield chunk
       chunk = infile.read(chunk_size)

class ListRequestHandler(tornado.web.RequestHandler):
   @tornado.web.asynchronous
   @gen.coroutine
   def get(self):
        uid = self.get_argument('uid')
        gid = self.get_argument('gid')
        base_dir = self.get_argument('path')
        if (base_dir==None or uid==None or gid==None):
            self.write("Invalid argument!You caused a %d error."%status_code)
            exit(1)
        if(os.path.exists(base_dir)):
          statinfo = os.stat(base_dir)
          statdict = {'path':base_dir,'mode':statinfo.st_mode,'ino':statinfo.st_ino,'dev':statinfo.st_dev,'nlink':statinfo.st_nlink,'uid':statinfo.st_uid,'gid':statinfo.st_gid,'size':statinfo.st_size,'atime':statinfo.st_atime,'mtime':statinfo.st_mtime,'ctime':statinfo.st_ctime}
          if(int(uid)==statinfo.st_uid and int(gid)==statinfo.st_gid):
              self.write(statdict)
              mode = statinfo.st_mode
          else:
              self.write("Permission denied.")
              exit(1)
        else:
            self.write("File or directory doesn't exist!You caused a %d error."%status_code)
            exit(1)
        if (S_ISDIR(mode)==None):
                self.write("This is not a directory!You caused a %d error."%status_code)
                exit(1)
        else:
                files = os.listdir(base_dir)
                for f in files:
                    statinfo = os.stat(base_dir + '/' +f)
                    statdict = {'path':(base_dir + '/' +f),'mode':statinfo.st_mode,'ino':statinfo.st_ino,'dev':statinfo.st_dev,'nlink':statinfo.st_nlink,'uid':statinfo.st_uid,'gid':statinfo.st_gid,'size':statinfo.st_size,'atime':statinfo.st_atime,'mtime':statinfo.st_mtime,'ctime':statinfo.st_ctime}
              #      print ("statdict",statdict)
                    self.write(statdict)
                self.write("end")
   def write_error(self,status_code,**kwargs):
                self.write("Gosh darnit,user!You caused a %d error."%status_code)

class StreamingRequestHandler(tornado.web.RequestHandler):
   @tornado.web.asynchronous
   @gen.coroutine
   def get(self):
       # ideally you would send in the get request what file you want to send
       # back as right now this is limited to what is hard coded in
        total_sent = 0
        uid = self.get_argument('uid')
        gid = self.get_argument('gid')
        base_dir = self.get_argument('filepath')
        if (base_dir==None or uid==None or gid==None):
            self.write("Invalid argument!You caused a %d error."%status_code)
            exit(1)
        if(os.path.exists(base_dir)):
          statinfo = os.stat(base_dir)
          if(int(uid)==statinfo.st_uid and int(gid)==statinfo.st_gid):
              mode = statinfo.st_mode
          else:
              self.write("Permission denied.")
              exit(1)
        else:
            self.write("File or directory doesn't exist!You caused a %d error."%status_code)
            exit(1)
        if (S_ISDIR(mode)):
            self.write("This is not a file!You caused a %d error."%status_code)
            exit(1)
        else:
            with open(base_dir, 'rb') as infile:
                for chunk in read_in_chunks(infile):
                    self.write(chunk)
                    yield gen.Task(self.flush)
                    total_sent += len(chunk)
                    print("sent",total_sent)

            self.finish()

if __name__ == "__main__":
   tornado.options.parse_command_line()
   application = tornado.web.Application([(r"/download", StreamingRequestHandler),(r"/list",ListRequestHandler)])
   application.listen(8880)
   tornado.ioloop.IOLoop.instance().start()


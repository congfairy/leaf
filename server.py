import tornado.ioloop
import tornado.web
import tornado.options
from tornado import gen
import os,sys
from stat import *

GB = 1024 * 1024 * 1024

# not really being used any more
# chunk_size = 1024

# Typically current Python style is to use 4 spaces.

# You can use and size space you want but most Pythonista use 4 spaces
# You can also use a Tab but most Pythonista have stopped using them these days
# Never mix Tabs with Spaces in same page of Python code

# White space is how Python defines everything and does not us { } or ; per se

# All thought in some advance Python one-liner code styling it can use the ;
# But for most Python code the ; is not used very often or at all


def read_in_chunks(infile, chunk_size=1024):
   chunk = infile.read(chunk_size)
   while chunk:
       yield chunk
       chunk = infile.read(chunk_size)

def read_in_chunks_pos(infile, pos, chunk_size=1024):
   infile.seek(int(pos))
   chunk = infile.read(chunk_size)
   while chunk:
       yield chunk
       chunk = infile.read(chunk_size)

class ReadRequestHandler(tornado.web.RequestHandler):
   # @tornado.web.asynchronous    # try using without this call if you are using current Tornado version
   @gen.coroutine
   def get(self):
        total_sent = 0
        uid = self.get_argument('uid')
        gid = self.get_argument('gid')
        base_dir = self.get_argument('filepath')


        # with the code I sent you earlier you should not have to messing with
        # defining chunk positioning. Python file reader calls really are doing
        # this for you under the hood. Once you define what size chunk to read
        # Python will send that size and the final chunk could be smaller and
        # Python will adjust for this with how the code was set up.
        pos = self.get_argument('pos',0)



        # Python protocol does not require () on it's if statements like you are
        # use to using them in other languages.
        # () can come in handy to insure logical is looked in section as in * / + - operations
        # but general Python does not require them as you are using them.

        # if (base_dir==None or uid==None or gid==None or pos==None):
        if base_dir==None or uid==None or gid==None or pos==None:
            self.write("Invalid argument!You caused a %d error."%status_code)
            exit(1)

        # if(os.path.exists(base_dir)):
        if os.path.exists(base_dir):



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
                for chunk in read_in_chunks_pos(infile,pos):
                    self.write(chunk)
                    yield gen.Task(self.flush)
                    total_sent += len(chunk)
                    print("sent",total_sent)

            self.finish()
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
   # this is was connected to the pyCurl call and as far as I know now not
   # beng used so try without to insure it's no longer needed
   # tornado.options.parse_command_line()


   # Typically Python code lines are 72 to 120 characters long by style choice only
   # They can be as long as you prefer, but most Pythonista use the 80 Char line length
   # I typically use what works for me from looking at the code logical

   # Often times most Pythonista will break up a line like the application line
   # into several lines line below to make it easier to read and insure that
   # you are not missing anything.

   # Again this is only a Pythonista style thing and Python itself does not care
   # generally how long the line is per se.

   # Most of what Python care most about is white space to define code logic blocks with

   application = tornado.web.Application([
    (r"/download", StreamingRequestHandler),
    (r"/list",ListRequestHandler),
    (r"/read",ReadRequestHandler)
    ])
   application.listen(8880)
   tornado.ioloop.IOLoop.instance().start()


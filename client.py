from tornado.httpclient import HTTPRequest, AsyncHTTPClient
import tornado.ioloop
import tornado.web
import os,sys
from tornado import gen
from functools import partial

total_downloaded = 0
action = sys.argv[1]
filepath = sys.argv[2]
def geturl():
    if(action=="download"):
        uid = sys.argv[3]
        gid = sys.argv[4]
        url = "http://127.0.0.1:8880/download?filepath="+filepath+"&uid="+uid+"&gid="+gid
        return url
    elif(action=="read"):
        uid = sys.argv[3]
        gid = sys.argv[4]
        pos = sys.argv[5] 
        url = "http://127.0.0.1:8880/read?filepath="+filepath+"&uid="+uid+"&gid="+gid+"&pos="+pos
        return url
        
        
def chunky(path, chunk):
   global total_downloaded
   total_downloaded += len(chunk)
   print("chunk size",len(chunk))
   # the OS blocks on file reads + writes -- beware how big the chunks is as it could effect things
   with open(path, 'a+b') as f:
       f.write(chunk)

@gen.coroutine
def writer(file_name):
   f = open(os.path.basename(filepath)+"new",'w')
   f.close()
   request = HTTPRequest(geturl(), streaming_callback=partial(chunky, file_name))
   http_client = AsyncHTTPClient()
   response = yield http_client.fetch(request)
   tornado.ioloop.IOLoop.instance().stop()
   print("total bytes downloaded was", total_downloaded)

if __name__ == "__main__":
   writer(os.path.basename(filepath)+"new")
   tornado.ioloop.IOLoop.instance().start()



from tornado.httpclient import HTTPRequest, AsyncHTTPClient
import tornado.ioloop
import tornado.web
from tornado import gen
from functools import partial
import datetime
import os,sys
total_downloaded = 0
action = sys.argv[1]
filepath = sys.argv[2]
def geturl():
    if action == "download":
        uid = sys.argv[3]
        gid = sys.argv[4]
        url = "http://127.0.0.1:8880/download?filepath="+filepath+"&uid="+uid+"&gid="+gid
        return url
    elif action=="read":
        uid = sys.argv[3]
        gid = sys.argv[4]
        pos = sys.argv[5]
        url = "http://127.0.0.1:8880/read?filepath="+filepath+"&uid="+uid+"&gid="+gid+"&pos="+pos
        return url

def spawn_callback(callback, *args, **kwargs):
   with NullContext():
       add_callback(callback, *args, **kwargs)

def chunky(path, chunk):
   global total_downloaded
   total_downloaded += len(chunk)
   print(len(chunk), total_downloaded)
   with open(path, 'a+b') as f:
       f.write(chunk)

async def writer(file_name):
   print('start:')
   f = open(os.path.basename(filepath)+"_new",'w')
   f.close()
   s = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
   request = HTTPRequest(geturl(), streaming_callback=partial(chunky, file_name))
   http_client = AsyncHTTPClient(max_body_size=1024*1024*550) # 550MB file limit
   response = await http_client.fetch(request)
   tornado.ioloop.IOLoop.instance().stop()
   print("total bytes downloaded was", total_downloaded)
   e = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
   print(s,e)



if __name__ == "__main__":
   io_loop = tornado.ioloop.IOLoop.instance()
   io_loop.spawn_callback(writer, os.path.basename(filepath)+"_new")
   io_loop.instance().start()

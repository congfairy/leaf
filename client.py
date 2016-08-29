from tornado.httpclient import HTTPRequest, AsyncHTTPClient
import tornado.ioloop
import tornado.web
from tornado import gen

from functools import partial

total_downloaded = 0

def chunky(path, chunk):
   global total_downloaded
   total_downloaded += len(chunk)
   print("chunk size",len(chunk))
   # the OS blocks on file reads + writes -- beware how big the chunks is as it could effect things
   with open(path, 'a+b') as f:
       f.write(chunk)

@gen.coroutine
def writer(file_name):
   request = HTTPRequest('http://127.0.0.1:8880/', streaming_callback=partial(chunky, file_name))
   http_client = AsyncHTTPClient()
   response = yield http_client.fetch(request)

   tornado.ioloop.IOLoop.instance().stop()
   print("total bytes downloaded was", total_downloaded)

if __name__ == "__main__":
   writer('test78')
   tornado.ioloop.IOLoop.instance().start()



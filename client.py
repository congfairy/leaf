from tornado.httpclient import HTTPRequest, AsyncHTTPClient
import tornado.ioloop
import tornado.web
from tornado import gen

GB = 1024 * 1024 * 1024
total_downloaded = 0


def streaming_callback(chunk):
    global total_downloaded
    total_downloaded += len(chunk)
    print ("downloaded",len(chunk), "total is now ", total_downloaded)


@gen.coroutine
def fetch():
    request = HTTPRequest(
        'http://localhost:8880', streaming_callback=streaming_callback)

    http_client = AsyncHTTPClient()
    response = yield http_client.fetch(request)
    print (response)
    tornado.ioloop.IOLoop.instance().stop()


if __name__ == "__main__":
    AsyncHTTPClient.configure("tornado.curl_httpclient.CurlAsyncHTTPClient")
    fetch()
    tornado.ioloop.IOLoop.instance().start()

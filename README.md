# leaf_upload
=======
##ls
input this url in your browser：http://192.168.83.218:8880/list?uid=0&gid=0&path=/root/leaf<br>
the result will be below which can be used by some program in the client：<br>
{"dev": 64768, "size": 4096, "nlink": 3, "mode": 16877, "uid": 0, "ino": 1167010, "gid": 0, "atime": 1472453479.7655556, "mtime": 1472453478.6536202, "ctime": 1472453478.6536202, "path": "/root/leaf"}{"dev": 64768, "size": 4096, "nlink": 8, "mode": 16877, "uid": 0, "ino": 67621657, "gid": 0, "atime": 1472091798.8171768, "mtime": 1472441247.0332892, "ctime": 1472441247.0332892, "path": "/root/leaf/.git"}{"dev": 64768, "size": 1956, "nlink": 1, "mode": 33188, "uid": 0, "ino": 1167022, "gid": 0, "atime": 1472369637.7267528, "mtime": 1472091801.801006, "ctime": 1472091801.801006, "path": "/root/leaf/list.php"}{"dev": 64768, "size": 13030046, "nlink": 1, "mode": 33188, "uid": 0, "ino": 1231600, "gid": 0, "atime": 1472369656.72266, "mtime": 1472369559.5022523, "ctime": 1472369559.5022523, "path": "/root/leaf/logclient"}{"dev": 64768, "size": 6799, "nlink": 1, "mode": 33188, "uid": 0, "ino": 1292161, "gid": 0, "atime": 1472369656.8876507, "mtime": 1472369559.5032525, "ctime": 1472369559.5032525, "path": "/root/leaf/logserver"}{"dev": 64768, "size": 14, "nlink": 1, "mode": 33188, "uid": 0, "ino": 1310814, "gid": 0, "atime": 1472369656.7216601, "mtime": 1472369630.184187, "ctime": 1472369630.184187, "path": "/root/leaf/README.md"}{"dev": 64768, "size": 26060092, "nlink": 1, "mode": 33188, "uid": 0, "ino": 1532775, "gid": 0, "atime": 1472435825.156429, "mtime": 1472436237.5957775, "ctime": 1472436237.5957775, "path": "/root/leaf/test78"}{"dev": 64768, "size": 867, "nlink": 1, "mode": 33188, "uid": 0, "ino": 1532783, "gid": 0, "atime": 1472441189.5247421, "mtime": 1472436231.520126, "ctime": 1472441150.077005, "path": "/root/leaf/client.py"}{"dev": 64768, "size": 12288, "nlink": 1, "mode": 33188, "uid": 0, "ino": 1231603, "gid": 0, "atime": 1472441255.5936832, "mtime": 1472437917.2924542, "ctime": 1472437917.2924542, "path": "/root/leaf/.server.py.swp"}{"dev": 64768, "size": 3023, "nlink": 1, "mode": 33188, "uid": 0, "ino": 1310805, "gid": 0, "atime": 1472453479.7645557, "mtime": 1472453478.5686245, "ctime": 1472453478.6536202, "path": "/root/leaf/server.py"}end <br>
check the "end" string to make sure you get the whole information。<br>

##read
Client:python3 client.py read filepath uid gid pos<br>
       for example:python3 client.py read /root/leaf/test78 0 0 138<br>
Server:python3 server.py<br>
Then new file will be stored locally<br>

##download
Client: python3 client.py download /root/leaf/logclient 0 0 (the parameters are:filepath,uid,gid)<br>
        and the file will be downloaded with the filename filepathnew<br>
server:just run :python3 server.py<br>
Then the file will be downloaded



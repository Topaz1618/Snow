#_*_coding:utf-8_*_
# Author:Topaz
import socket
import select
import time
import re
# from django.http import HttpResponse

class Snow(object):
    def __init__(self,routes):
        self.routes = routes
        self.inputs = set()
        self.request = None
        self.async_request_header = {}


    def run(self,host="localhost",port=9999):
        my_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)        #得到文件描述符
        my_socket.bind((host,port))        #我们在哪个端口？
        my_socket.listen(5)     #有人给我打电话吗？
        my_socket.setblocking(0)    #设置为非阻塞socket，循环的 read 或 accept，直到读完所有的数据，抛出 EWOULDBLOCK 异常
        self.inputs.add(my_socket)
        try:
            while True:
                r_list,w_list,e_list = select.select(self.inputs,[],[],0.05)    #多路I/O检测多个socket是否有数据，没有就阻塞，rlist -- wait until ready for reading
                print("喵~")
                time.sleep(2)
                for conn in r_list:
                    if my_socket == conn:
                        client,addr = conn.accept() #"Thank you for calling port 3490."
                        client.setblocking(0)
                        self.inputs.add(client)
                    else:
                        gen = self.process(conn)
                        if isinstance(gen,HttpResponse):
                            conn.sendall(gen.response())
                            self.inputs.remove(conn)
                            conn.close()
                        else:
                            print('wtgen',gen)  #是个生成器
                            yieldld = next(gen)  #拿到class对象，再说一遍yield，返回的生成器调用成员方法时，相应的生成器函数中的代码才会执行
                            print('yield是什么',yieldld)
                            self.async_request_header[conn] = yieldld   #注意哦，key是conn，conn可以发 连接
                self.asynchronous()
        except Exception as e:
            print('抓到一个错误',e)
        finally:
            my_socket.close()

    def asynchronous(self):
        #self.async_request_header{socket对象：}
        for conn in list(self.async_request_header.keys()):
            yieldld = self.async_request_header[conn]
            if not yieldld.ready:
                print("等。。。")
                continue
            else:
                print("超时了",yieldld)
            if yieldld.callback:
                print('看看这儿',yieldld,yieldld.callback)
                ret = yieldld.callback(self.request,yieldld)
            m = HttpResponse("Timeout")
            conn.sendall(m.response())
            self.inputs.remove(conn)
            del self.async_request_header[conn]
            conn.close()

    def process(self,conn):
        print("process")
        func = None
        self.request = HttpResquest(conn)
        for route in self.routes:
            if  re.match(route[0],self.request.url):
                func = route[1]
                break
        if not func:
            return HttpNotFound("404")
        else:
            return func(self.request)

class Future(object):
    def __init__(self,callback):
        self._ready = False
        self.callback = callback
    def set_result(self,value=None):
        self.value = value
        self._ready = True
    @property
    def ready(self):
        return self._ready

class TimeoutFuture(Future):
    def __init__(self,timeout):
        self.timeout = timeout
        super(TimeoutFuture,self).__init__(callback=None)
        self.start_time = time.time()
    @property
    def ready(self):
        current_time = time.time()
        if current_time - self.start_time > self.timeout:
            self._ready = True
        return self._ready

class HttpResquest(object):
    def __init__(self,conn):
        print("HttpResquest")
        self.conn = conn
        self.header = bytes()
        self.body = bytes()
        self.header_dic = {}
        self.method =""
        self.url = ""
        self.protocol = ""
        self.cutting()
        self.save()

    def cutting(self):
        while True:
            try:
                rec = self.conn.recv(8096)
            except Exception as e:
                rec = None
            if not rec:
                break
            cut = rec.split(b'\r\n\r\n')    #分隔符为\r\n\r\n
            if len(cut) == 1:
                self.header += cut
            else:
                h,b = cut
                self.header += h
                self.body += b

    @property
    def header_str(self):
        return str(self.header,encoding="utf-8")

    def save(self):
        headers = self.header_str.split('\r\n')
        first_line = headers[0].split(' ')
        if len(first_line) == 3:
            self.method,self.url,self.protocol = first_line
            for line in headers:
                kv = line.split(':')
                if len(kv) == 2:
                    k,v = kv
                    self.header_dic[k] = v

class HttpResponse(object):
    def __init__(self,message):
        self.message = message
        print('message类型',type(self.message))
    def response(self):
        return bytes(self.message,encoding="utf-8")

class HttpNotFound(HttpResponse):
    def __init__(self,message):
        super(HttpNotFound,self).__init__(message)















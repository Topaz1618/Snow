#_*_coding:utf-8_*_
# Author:Topaz
from snow import Snow
from django.shortcuts import redirect
from snow import HttpResponse
from snow import Future
from snow import TimeoutFuture

request_list = []

def index(request):
    return HttpResponse('ok')


def async(request):
    obj = TimeoutFuture(1)
    yield obj

def req(request):
    obj = Future(callback=callback) # <snow.Future object at 0x000001535D47D278> HttpResponse(future.value)
    request_list.append(obj)
    print('request_list',request_list)
    yield obj   #yield 是一个类似 return 的关键字，只是这个函数返回的是个生成器，返回的生成器调用成员方法时，相应的生成器函数中的代码才会执行

def stop(request):
    obj = request_list[0]   #列表一直增加，这个就取第一个
    del request_list[0] #然后删除掉
    obj.set_result('done')
    return HttpResponse('Stop')

def callback(request,future):
    return HttpResponse(future.value)

routes = [
    # ('/index/',index),
    ('/async/',async),  #超时
    ('/req/',req),      #自己停止
    ('/stop/',stop),
]

app = Snow(routes)
app.run(port=8001)
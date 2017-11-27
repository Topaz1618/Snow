# 异步非阻塞web框架
## 介绍
    超时事件处理
    是web框架也是web server
    通过非阻塞socket和select I/O多路复用实现
    模仿了Tronado
    参考：http://sanyuesha.com/2017/02/08/tornado-async-style/

## 目录结构
    snow.py     # server端，接收请求
    use.py      # 路由系统/views
    test        # test 文件
    client.py   # test 文件
## 执行
    Python python use.py   # 执行use去调用server.py下的Snow开始接收请求
    浏览器访问：http://127.0.0.1:8001/async/  #超时后返回所需页面
    浏览器访问：http://127.0.0.1:8001/req/    #访问http://127.0.0.1:8001/stop/才返回页面
## server 端流程
    1.新的请求连接进来加到列表里，交给select的readfds数组，select检测这个数组
    2.select 是 I/O多路复用机制，如果哪个套接字就绪select函数就返回，就绪条件之一就是接受缓存区大于缓存区最低水位1
    3.这时候可以调用recv函数来取数据，socket使用非阻塞I/O，非阻塞I/O的特点就是有数据就取，没数据就返回错误，如果使用了阻塞I/O，它并不知道要取多少数据会一直等


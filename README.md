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

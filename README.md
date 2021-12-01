# 上海大学校园网络认证脚本

### 依赖

本脚本采用Python3编写，依赖于

````
Requests
IPy
pywifi
````

### 0. ⭐Star⭐

### 1. 修改id

在python文件的main()函数中下，将00000000改成学号，"xxxxxx"改为密码

```
connect_wire(00000000, "xxxxxx")
```

### 2. 设置自启动和定时任务

#### windows

参考链接：https://blog.csdn.net/u012849872/article/details/82719372

#### Linux

##### -设置定时任务

bash里输入 crontab -e

然后编辑界面加上具体的命令语句，每五分钟执行一次

````
*/5 * * * * /usr/bin/python3.6 youpath/auto-shunet.py
````

##### -设置开机启动

在/etc/rc.local中添加指令

````
/usr/bin/python3.6 youpath/auto-shunet.py
````

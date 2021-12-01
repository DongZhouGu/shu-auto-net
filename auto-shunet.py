from psutil import net_if_addrs, net_if_stats
from IPy import IP
import socket
from requests import get, post
import os
import sys
import pywifi
from pywifi import const
import time

class shuConnect:
    def __init__(self, user, passwd):
        self.user = user
        self.passwd = passwd

    def check_connect(self):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)
            sock.connect(("10.10.9.9", 8080))
            pre_status = True
        except socket.error:
            pre_status = False
        finally:
            sock.close()

        if pre_status:
            r = get("http://10.10.9.9:8080")
            if "success.jsp" in r.url:
                return 1
            else:
                return 2
        else:
            return 3

    def catch_data(self):
        r = get("http://123.123.123.123/")
        query_string = r.text
        st = query_string.find("index.jsp?") + 10
        end = query_string.find("'</script>")
        query_string = query_string[st:end]

        data = {"userId": self.user,
                "password": self.passwd,
                "passwordEncrypt": "false",
                "queryString": query_string,
                "service": "shu",
                "operatorPwd": "",
                "operatorUserId": "",
                "validcode": ""}

        return data

    def connect(self):
        r = post("http://10.10.9.9:8080/eportal/InterFace.do?method=login", data=self.catch_data())
        r.encoding = "utf-8"
        resp = r.json()

        if resp["result"] == "success":
            return True, ""
        else:
            return False, resp["message"]

    def start_connect(self):
        status = self.check_connect()
        if status == 1:
            print('=====已认证 & 用户已在线=====\n')
            r = True
        elif status == 2:
            r, msg = self.connect()
            if r:
                print(f'=====认证成功 & 用户{self.user}登陆成功=====\n')
            else:
                print(f'=====认证失败=====\n' + msg)
        else:
            print('=====校园网不可用=====\n')
            r = False
        return r


def connect_wire(id, pwd):
    wire_name = '以太' if 'win' in sys.platform else 'enp'
    for key in net_if_addrs().keys():
        if wire_name in key and net_if_stats()[key].isup:
            break

    all_nets = net_if_addrs()[key]
    for i in range(len(all_nets)):
        try:
            ip = all_nets[i].address
            if IP(ip).version() == 4:
                if (shuConnect(id, pwd).start_connect()):
                    return
        except:
            pass
    print("有线网连接失败，尝试无线网")
    connect_wifi() #预先链接Shu（ForAll）
    if (shuConnect(id, pwd).start_connect()):
        print("无线网认证成功")
    else:
        print("有线无线 网络认证失败")


def connect_wifi():
    wifi = pywifi.PyWiFi() 
    interFace = wifi.interfaces()[0] 
    print(interFace.name()) 
    interFace.disconnect() 
    profile = pywifi.Profile()  
    profile.ssid = "Shu(ForAll)" 
    profile.akm.append(const.AUTH_ALG_OPEN)  
    profile.cipher = const.CIPHER_TYPE_CCMP 

    tmp_profile = interFace.add_network_profile(profile)  

    interFace.connect(tmp_profile)  
    time.sleep(5) 
    isok = True
    if interFace.status() == const.IFACE_CONNECTED:
        print("成功连接")
    else:
        print("失败")
    #ifaces.disconnect()  # 断开连接
    time.sleep(1)
    return isok

if __name__ == '__main__':
    if "win" in sys.platform:
        ret = os.system("ping -n 1 www.baidu.com")
    else:
        ret = os.system("ping -c 1 www.baidu.com")
    if ret == 0:
        print("本机已联网")
    else:
        connect_wire(00000000, "xxxxxxxx")
        


###############################
# 功能:自动更新IPv6地址到noip
# 说明:本脚本仅适用于Windows系统
# 具体API请参考:
# https://www.noip.com/integrate/request
# https://www.noip.com/integrate/response
###############################
import os
import re
import asyncio
import aiohttp
import socket
import time
from datetime import datetime

hostname = "yourhostname.ddns.net"
username = "yourusername"
password = "yourpassword"
useragent = "Xiaomi AX9000/2.23_66039-td84as@mi.com"
scandelay = 120  # 秒
retrydelay = 5  # 秒


def getIPv6Address():
    output = os.popen("ipconfig /all").read()
    result = re.findall(r"(([a-f0-9]{1,4}:){7}[a-f0-9]{1,4})", output, re.I)
    return result[0][0]


async def uploadIPv6Address(ipv6address):
    url = "http://{}:{}@dynupdate.no-ip.com/nic/update".format(username, password)
    # url = "http://www.google.com"
    headers = {
        "User-Agent": useragent
    }
    params = {
        "hostname": domain_name,
        "myipv6": ipv6address,
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, params=params) as response:
                r = await response.text()
                print(r)
                if ("good" in r):
                    return 0
                if ("nochg" in r):
                    return 1
                else:
                    return 2
    except Exception as e:
        print(f"Error retrieving text from {url}: {e}")
        return 3


async def uploadIPv6UntilSuccess(ipv6address):  # 记录值与当前值不同时，才会上传，直到上传成功。
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "正在上传本机IPv6地址")
    while True:
        state = await uploadIPv6Address(ipv6address)
        if (state == 0):
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S")+":上传成功")
            break
        elif (state == 1):
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S")+":上传成功!与已记录的地址相同,没有发生变化")
            break
        elif (state == 2):
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S")+":上传失败,{}秒后重试".format(retrydelay))
        elif (state == 3):
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S")+":网络连接失败,{}秒后重试".format(retrydelay))
        time.sleep(retrydelay)


async def main():
    while True:
        os.system('cls')
        try:
            # 获取域名绑定的IPv6地址
            domainIPv6Address = (socket.getaddrinfo(domain_name, None, socket.AF_INET6))[0][4][0]
            # 获取本机的IPv6地址
            localIPv6Address = getIPv6Address()
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ":域名:" + domain_name)
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ":目标域名IPv6地址:" + domainIPv6Address)
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ":当前本机IPv6地址:" + localIPv6Address)
            if domainIPv6Address != localIPv6Address:
                await uploadIPv6UntilSuccess(localIPv6Address)
            else:
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ":IPv6地址未变化")
        except:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ":网络好像没连上~")
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ":{}秒后进行下一次扫描".format(scandelay))
        time.sleep(scandelay)

if __name__ == "__main__":
    asyncio.run(main())

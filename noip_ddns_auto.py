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
import time
from datetime import datetime

hostname = "yourhostname.ddns.net"
username = "yourusername"
password = "yourpassword"
UPLOAD_AT_STARTUP = False  # 是否在启动时上传当前IPv6地址
useragent = "Xiaomi AX9000/2.23.0.4.388_194-d4aw5e@xiaomi.com"
delay = 120  # 秒
currentIPv6Address = ""


def getIPv6Address():
    output = os.popen("ipconfig /all").read()
    result = re.findall(r"(([a-f0-9]{1,4}:){7}[a-f0-9]{1,4})", output, re.I)
    return result[0][0]


async def uploadIPv6Address(ipv6address):
    url = "http://{}:{}@dynupdate.no-ip.com/nic/update".format(username, password)
    headers = {
        "User-Agent": useragent
    }
    params = {
        "hostname": hostname,
        "myipv6": ipv6address,
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, params=params) as response:
            return await response.text()


def InterpretResponse(response):
    if ("good" in response):
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S")+":上传成功")
        return 0
    if ("nochg" in response):
        print(print(datetime.now().strftime("%Y-%m-%d %H:%M:%S")+":重复上传!IP地址与上次相同"))
        return 1
    else:
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S")+":上传失败")
    return 2


async def checkIPv6Address():
    global currentIPv6Address
    currentIPv6Address = getIPv6Address()
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S")+":当前IPv6:\n" + getIPv6Address())
    if (UPLOAD_AT_STARTUP):
        response = await uploadIPv6Address(currentIPv6Address)
        print(response)
    while True:
        newIPv6Address = getIPv6Address()
        if currentIPv6Address != newIPv6Address:
            response = await uploadIPv6Address(currentIPv6Address)
            print(response)
            if (InterpretResponse(response) != 2):
                currentIPv6Address = newIPv6Address
        else:
            # 清空当前行
            print("\r" + " " * 50 + "\r", end="", flush=True)
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S")+":IPv6地址未变化", end="\r")
        time.sleep(delay)

if __name__ == "__main__":
    asyncio.run(checkIPv6Address())

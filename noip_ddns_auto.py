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
useragent = "ASUS TUF-AX5400/3.0.0.4.388_22525-gd35b8fe@asus.com"
scandelay = 120  # 秒
retrydelay = 5  # 秒
recordedIPv6Address = ""


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
        "hostname": hostname,
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


async def uploadIPv6UntilSuccess():  # 记录值与当前值不同时，才会上传，直到上传成功。
    global recordedIPv6Address
    while True:
        currentIPv6Address = getIPv6Address()
        if (recordedIPv6Address != currentIPv6Address):
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S")+":当前IPv6:" + currentIPv6Address)
            state = await uploadIPv6Address(currentIPv6Address)
            if (state == 0):
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S")+":上传成功")
                recordedIPv6Address = currentIPv6Address
                break
            elif (state == 1):
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S")+":重复上传!IP地址与上次相同")
                recordedIPv6Address = currentIPv6Address
                break
            elif (state == 2):
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S")+":上传失败,{}秒后重试".format(retrydelay))
            elif (state == 3):
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S")+":网络连接失败,{}秒后重试".format(retrydelay))
            time.sleep(retrydelay)
        else:
            break


async def main():
    global recordedIPv6Address
    if (UPLOAD_AT_STARTUP == False):
        recordedIPv6Address = getIPv6Address()  # 开始时记录值与当前值相同，uploadIPv6UntilSuccess()不上传
    while True:
        if recordedIPv6Address != getIPv6Address():
            await uploadIPv6UntilSuccess()
        else:
            print("\r" + " " * 50 + "\r", end="", flush=True)  # 清空当前行
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S")+":IPv6地址未变化:"+recordedIPv6Address, end="\r")
        time.sleep(scandelay)

if __name__ == "__main__":
    asyncio.run(main())

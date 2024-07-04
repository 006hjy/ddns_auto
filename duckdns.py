import datetime
import re
import socket
import time
import requests
import os


def getLocalIPv6Address():
    output = os.popen("ipconfig /all").read()
    result = re.findall(r"(([a-f0-9]{1,4}:){7}[a-f0-9]{1,4})", output, re.I)
    return result[0][0]


def getDomainIPv6Address(domain_name):
    return (socket.getaddrinfo(domain_name, None, socket.AF_INET6))[0][4][0]


def updateDuckDNS(_ipv6):
    url = "https://www.duckdns.org/update"
    params = {
        "domains": "your No.3 domain name",
        "token": "your domain token",
        "ip": "",
        "ipv6": _ipv6
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()  # 如果请求失败，抛出异常
        print("DuckDNS update succeeded.")
        print(response.text)
        if response.text == "OK":
            return True
        else:
            return False
    except requests.exceptions.RequestException as e:
        print("DuckDNS update failed:", e)
        return False
    except:
        print("Unknow ERROR!")
        return False


def main():
    while True:
        try:
            os.system('Ipconfig/flushdns')
            os.system('cls')
            _time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"本次扫描时间:{_time}")
            domain = "hexin.duckdns.org"
            print(f"目标域名:{domain}")
            local_ipv6 = getLocalIPv6Address()
            print(f"本地IPv6地址:{local_ipv6}")
            domain_ipv6 = getDomainIPv6Address(domain)
            print(f"域名IPv6地址:{domain_ipv6}")
            if domain_ipv6 == local_ipv6:
                print("域名已正确绑定，60秒后再次扫描。")
                time.sleep(60)
                ...
            else:
                print("域名地址不匹配，正在尝试绑定...")
                # 调用函数更新DuckDNS
                updateDuckDNS(local_ipv6)
                time.sleep(5)
        except:
            pass

            
if __name__ == '__main__':
    main()

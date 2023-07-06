# -*- coding: utf-8 -*-
###############################
# 功能:自动更新IPv6地址到阿里云DDNS
# 说明:本脚本仅适用于Windows系统
# 具体API请参考:
# https://help.aliyun.com/document_detail/2355673.html
###############################
import os
import sys
import re
import asyncio
import socket
import time
from datetime import datetime
from typing import List
from alibabacloud_alidns20150109.client import Client as Alidns20150109Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_alidns20150109 import models as alidns_20150109_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_console.client import Client as ConsoleClient
from alibabacloud_tea_util.client import Client as UtilClient

ALIBABA_CLOUD_ACCESS_KEY_ID = 'key_id'
ALIBABA_CLOUD_ACCESS_KEY_SECRET = 'key_secret'

scandelay = 120  # 秒
retrydelay = 5  # 秒
domain = "www.baidu.com"


def getLocalIPv6Address():
    output = os.popen("ipconfig /all").read()
    result = re.findall(r"(([a-f0-9]{1,4}:){7}[a-f0-9]{1,4})", output, re.I)
    return result[0][0]


def getDomainIPv6Address(domain_name):
    return (socket.getaddrinfo(domain_name, None, socket.AF_INET6))[0][4][0]


class Alicloud:
    def __init__(self):
        pass

    @staticmethod
    def create_client(
        access_key_id: str,
        access_key_secret: str,
    ) -> Alidns20150109Client:
        """
        使用AK&SK初始化账号Client
        @param access_key_id:
        @param access_key_secret:
        @return: Client
        @throws Exception
        """
        config = open_api_models.Config(
            # 必填，您的 AccessKey ID,
            access_key_id=access_key_id,
            # 必填，您的 AccessKey Secret,
            access_key_secret=access_key_secret
        )
        # 访问的域名
        config.endpoint = f'alidns.cn-hangzhou.aliyuncs.com'
        return Alidns20150109Client(config)

    @staticmethod
    async def main_async(ipv6: str):
        # 请确保代码运行环境设置了环境变量 ALIBABA_CLOUD_ACCESS_KEY_ID 和 ALIBABA_CLOUD_ACCESS_KEY_SECRET。
        # 工程代码泄露可能会导致 AccessKey 泄露，并威胁账号下所有资源的安全性。以下代码示例仅供参考，建议使用更安全的 STS 方式，更多鉴权访问方式请参见：https://help.aliyun.com/document_detail/378659.html
        client = Alicloud.create_client(ALIBABA_CLOUD_ACCESS_KEY_ID, ALIBABA_CLOUD_ACCESS_KEY_SECRET)
        update_domain_record_request = alidns_20150109_models.UpdateDomainRecordRequest(
            lang='',
            user_client_ip='',
            rr='www',
            type='AAAA',
            value=ipv6,
            ttl=600,
            line='',
            record_id='record_id_number'
        )
        runtime = util_models.RuntimeOptions()
        resp = await client.update_domain_record_with_options_async(update_domain_record_request, runtime)
        ConsoleClient.log(UtilClient.to_jsonstring(resp))


async def main():
    await Listen()


async def Listen():
    while True:
        os.system('cls')
        try:
            # 获取域名绑定的IPv6地址
            domainIPv6Address = getDomainIPv6Address(domain)
            # 获取本机的IPv6地址
            localIPv6Address = getLocalIPv6Address()
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ":域名:" + domain)
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ":目标域名IPv6地址:" + domainIPv6Address)
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ":当前本机IPv6地址:" + localIPv6Address)
            if domainIPv6Address != localIPv6Address:
                await Alicloud.main_async(localIPv6Address)
            else:
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ":IPv6地址未变化")
        except Exception as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ":出了一些问题,以下是错误信息:")
            print(e)
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ":{}秒后进行下一次扫描".format(scandelay))
        time.sleep(scandelay)


if __name__ == '__main__':
    asyncio.run(main())

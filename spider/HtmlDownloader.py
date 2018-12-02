# coding:utf-8

import random
import re

import PyV8
from requests import ConnectionError

import config
import json
from db.DataStore import sqlhelper
from getcookie import Getcookie, getHtml
from util.logger import logger_proxy
from selenium import webdriver

__author__ = 'qiye'

import requests
import chardet


# 参数包含两个：
# containVar：查找包含的字符
# stringVar：所要查找的字符串
def containVarInString(containVar, stringVar):
    try:
        if isinstance(stringVar, str):
            if stringVar.find(containVar):
                return True
            else:
                return False
        else:
            return False
    except Exception, e:
        print e


class Html_Downloader(object):
    @staticmethod
    def download(url):
        try:
            cookie = None
            cookie = Getcookie(url)
            r = requests.get(url=url, headers=config.get_header(), timeout=config.TIMEOUT, cookies=cookie)
            r.encoding = chardet.detect(r.content)['encoding']
            print r.content
            if (not r.ok) or len(r.content) < 500:
                raise ConnectionError
            else:
                return r.text



        except Exception:
            count = 0  # 重试次数
            proxylist = sqlhelper.select(10)
            if not proxylist:
                return None

            while count < config.RETRY_TIME:
                try:
                    proxy = random.choice(proxylist)
                    ip = proxy[0]
                    port = proxy[1]
                    proxies = {"http": "http://%s:%s" % (ip, port), "https": "http://%s:%s" % (ip, port)}

                    r = requests.get(url=url, headers=config.get_header(), timeout=config.TIMEOUT, proxies=proxies)
                    r.encoding = chardet.detect(r.content)['encoding']
                    if (not r.ok) or len(r.content) < 500:
                        raise ConnectionError
                    else:
                        return r.text
                except Exception:
                    count += 1

        return None

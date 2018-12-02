# coding=utf-8
import re

import PyV8
import requests

import config


def getHtml(url, cookie=None):
    try:
        html = requests.get(url=url, headers=config.get_header(), timeout=30, cookies=cookie).content
        return html
    except Exception:
        return  None


def executeJS(js_func_string, arg):
    ctxt = PyV8.JSContext()
    ctxt.enter()
    func = ctxt.eval("({js})".format(js=js_func_string))
    return func(arg)


def parseCookie(string):
    string = string.replace("document.cookie='", "")
    clearance = string.split(';')[0]
    return {clearance.split('=')[0]: clearance.split('=')[1]}


def Getcookie(url):
    first_html = getHtml(url)
    js_func = ''.join(re.findall(r'(function .*?)</script>', first_html))
    js_arg = ''.join(re.findall(r'setTimeout\(\"\D+\((\d+)\)\"', first_html))
    js_func = js_func.replace('eval("qo=eval;qo(po);")', 'return po')
    # 执行JS获取Cookie
    cookie_str = executeJS(js_func, js_arg)
    # 将Cookie转换为字典格式
    cookie = parseCookie(cookie_str)
    if cookie:
        return cookie
    else:
        return None

"""
重定向回上一个网页：用户完成登录认证后应该回到上一个访问的页面而不是直接进入主页
核心要点：拿到上一个网页URL，如果没拿到上一个页面的URL，默认回到主页

安全问题：对跳转的url进项检验
1.首先要拿到我们程序内的地址，这样才知道主机内的地址有哪些做个参照
2.把获取的url格式转换为绝对url地址
3.把分析后的目标URL地址和主机地址进行匹配，匹配成功才能跳转
"""

from flask import request,redirect,url_for
from urllib.parse import urlparse, urljoin

def redirect_up(default='index', **kwargs):
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_url_safe(target):
            return redirect(target)

    return redirect(url_for(default, **kwargs))


def is_url_safe(target):
    host_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http','https') and \
        test_url.netloc == host_url.netloc
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import render, HttpResponse, redirect
from rbac import models
import re


def get_power_url(request):
    re_url = []  # 设置存放
    session_user_data = request.session.get('user_data')  # 从当前session中获取用户是否登录或者登录后的信息
    if session_user_data:  # 如果有值 是登录的用户
        # request.session['user_data'] = {"username": username, 'uid': uid}
        username = session_user_data['username']  # 获取当前登录用户名
        # 获取当前用户的所有权限url并去重
        url = models.UserInfo.objects.filter(username=username).values("role__power__url").distinct()
        for power_url in url:  # 把获取到的url存放到 re_url中用于正则校验
            re_url.append(power_url["role__power__url"])
        return re_url  # 返回收集好的re_url返回给调用者
    else:  # 未登录用户返回至登录界面
        return re_url


class Rbac(MiddlewareMixin):  # 创建中间件
    def process_request(self, request):  # 中间件用于验证用户是否有权限登录相应的url
        current_path = request.path_info  # 获取用户访问的路径
        url_white_list = ['/login/', '/enter/', '/admin/', '/home/', '/enterout/']  # 创建用户白名单 不需要权限就可以访问的名单
        for white_url in url_white_list:
            ret = re.match('^%s$' % white_url, current_path)  # 循环用户白名单 如果匹配到白名单url直接返回
            if ret:
                return None
        power_url = get_power_url(request)  # 调用 get_power_url 函数 获取当前用户权限url
        if power_url:  # 如果re_url不为空即为用户登录成功
            Flag = False  # 设置标记位 如果用户在访问权限中可访问当前页面
            for url in power_url:
                ret = re.match('^%s$' % url, current_path)
                if ret:  # 如果用户权限在访问的url中 使flag=true
                    Flag = True
                    break
            if Flag:
                return None
            else:
                return HttpResponse('无权限访问')
        else:
            return redirect('/enter/')

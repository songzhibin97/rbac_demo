from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, HttpResponse, redirect
# 引入rbac model中form组件 定义的登录注册校验方式
from rbac.models import Login, Enter
from rbac import models
from django.contrib.auth import authenticate, login, logout
from rbac.functions.function import set_session
import json
import hashlib


# 处理用户注册的函数
def login(request):
    if request.method == "POST":
        # post请求
        # form组件验证
        login_obj = Login(request.POST)
        if login_obj.is_valid():
            # # 验证通后删除不需要的数据 password2 login_obj中包含提交上来的所有键值对数据
            # del login_obj.cleaned_data["password2"]
            # 将数据打散后 在Userinfo表中创建用户
            username = login_obj.cleaned_data.get("username")
            password_unencrypted = login_obj.cleaned_data.get("password")  # 获取未加密的password
            password = hashlib.md5(b'welcomebinhome.club')  # hashlib加盐
            password.update(bytes(password_unencrypted, encoding='utf-8'))  # 把password进行摘要
            password_new = password.hexdigest()  # 获得加密后的password
            try:
                # 如果注册无异常 使用返回json数据data
                models.UserInfo.objects.create(username=username, password=password_new)
                dat = {'mode': 1, 'data': '注册成功'}
                data = json.dumps(dat)
                return HttpResponse(data)
            except Exception as e:
                # 如注册报错后 捕获错误返回json数据data
                dat = {'mode': 0, 'data': '注册失败'}
                data = json.dumps(dat)
                return HttpResponse(data)
        # 如验证未通过的 返回json数据data
        dat = {'mode': 2, 'errors': login_obj.errors}
        data = json.dumps(dat)
        return HttpResponse(data)
    else:
        # get请求
        # 实例化login对象login_obj返回给页面渲染
        login_obj = Login()
        return render(request, 'rbac_login.html', {'login_obj': login_obj})


# 处理用户登录的函数
def enter(request):
    # 处理enter post请求
    if request.method == 'POST':
        # form组件验证
        enter_obj = Enter(request.POST)
        if enter_obj.is_valid():
            # 校验通过
            username = enter_obj.cleaned_data.get("username")
            password_unencrypted = enter_obj.cleaned_data.get("password")  # 获得用户输入密码
            password = hashlib.md5(b'welcomebinhome.club')  # 加盐
            password.update(bytes(password_unencrypted, encoding='utf-8'))  # 进行数据摘要
            password_new = password.hexdigest()  # 取出结果
            user_obj = models.UserInfo.objects.filter(username=username, password=password_new)
            if user_obj:
                # 如果用户验证通过 绑定信息到session中
                set_session(request, username)
                # 给前端返回data信息判断是否已登录成功
                dat = {'mode': 1, 'data': '登录成功'}
                data = json.dumps(dat)
                return HttpResponse(data)
            else:
                # 登录失败
                dat = {'mode': 0, 'data': '账号或密码错误'}
                data = json.dumps(dat)
                return HttpResponse(data)
        else:
            # 验证失败
            dat = {'mode': 2, 'errors': enter_obj.errors}
            data = json.dumps(dat)
            return HttpResponse(data)
    else:
        # 如果enter为get请求 实例化enter对象为enter_obj 返回给页面渲染
        enter_obj = Enter()
        return render(request, 'rbac_enter.html', {'enter_obj': enter_obj})


# 处理用户注销
def enterout(request):
    request.session.flush()
    return redirect('/enter/')


# 站点首页
def home(request):
    # 判断用户是否登录
    username = request.session.get("user_data")
    if username:
        # 获取user对象传入前端模板渲染
        user_obj = models.UserInfo.objects.filter(username=username["username"])[0]
        # 获取power对象传入
        power_obj = models.Power.objects.filter(role__userinfo__username=username["username"])
    else:
        user_obj = None
        power_obj = None
    return render(request, 'home.html', {"user_obj": user_obj, 'power_obj': power_obj})

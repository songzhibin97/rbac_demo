from django.db import models

# Create your models here.
from django import forms
from django.core.exceptions import ValidationError


# form 组件实现注册功能
class Login(forms.Form):
    # 验证用户名
    username = forms.CharField(
        required=True,
        label="账号:",
        max_length=20,
        min_length=3,
        error_messages={
            "required": "不能为空",
            "max_length": "账号最大不能超过20位",
            "min_length": "账号最小不能少于3位"
        },
        widget=forms.widgets.TextInput(attrs={'class': 'form-control'}, )

    )
    # 验证密码
    password = forms.CharField(
        required=True,
        label="密码:",
        max_length=20,
        min_length=6,
        widget=forms.widgets.PasswordInput(attrs={'class': 'form-control'}, render_value=True),
        error_messages={
            "required": "不能为空",
            "max_length": "账号最大不能超过20位",
            "min_length": "账号最小不能少于6位"
        },

    )
    # 二次校验密码
    password2 = forms.CharField(
        required=True,
        label="确认密码:",
        max_length=20,
        min_length=6,
        widget=forms.widgets.PasswordInput(attrs={'class': 'form-control'}, render_value=True),
        error_messages={
            "required": "不能为空",
            "max_length": "账号最大不能超过20位",
            "min_length": "账号最小不能少于6位"
        }
    )

    # 局部钩子 用于检测username包含敏感词
    def clean_username(self):
        Forbidden = ['金瓶梅', "法轮功"]
        value = self.cleaned_data.get("username")
        for i in Forbidden:
            if i in value:
                raise ValidationError("包含敏感词")
        return value

    # 全局钩子 用于检测两次密码是否一致
    def clean(self):
        value1 = self.cleaned_data.get("password")
        value2 = self.cleaned_data.get("password2")
        if value1 != value2:
            self.add_error("password2", "两次密码不一致")
            raise ValidationError("两次密码不一致")
        else:
            return self.cleaned_data


# form 组件实现注册功能
class Enter(forms.Form):
    # 验证用户名
    username = forms.CharField(
        required=True,
        label="账号:",
        max_length=20,
        min_length=3,
        error_messages={
            "required": "不能为空",
            "max_length": "账号最大不能超过20位",
            "min_length": "账号最小不能少于3位"
        },
        widget=forms.widgets.TextInput(attrs={'class': 'form-control'}, )

    )
    # 验证密码
    password = forms.CharField(
        required=True,
        label="密码:",
        max_length=20,
        min_length=6,
        widget=forms.widgets.PasswordInput(attrs={'class': 'form-control'}, render_value=True),
        error_messages={
            "required": "不能为空",
            "max_length": "账号最大不能超过20位",
            "min_length": "账号最小不能少于6位"
        }, )


# 创建用户表 与角色表设置多对多关系 使用manytomany创建第三张表关系模型
class UserInfo(models.Model):
    uid = models.AutoField(primary_key=True)
    username = models.CharField(max_length=32, unique=True)
    password = models.CharField(max_length=32)
    role = models.ManyToManyField(to='Role')


# 创建角色表 与权限表设置多对多关系 使用manytomany创建第三张表关系模型
class Role(models.Model):
    rid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32)
    power = models.ManyToManyField(to='Power')


# 创建权限表 权限存放正则匹配规则 配对注释
class Power(models.Model):
    pid = models.AutoField(primary_key=True)
    url = models.CharField(max_length=64)
    annotation = models.CharField(max_length=32)

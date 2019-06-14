"""rbac_demo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
# 引入rbac视图函数 别名为rbac_views
from rbac import views as rbac_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/', rbac_views.login),
    url(r'^enter/', rbac_views.enter),
    url(r'^home/', rbac_views.home),
    url(r'^enterout/', rbac_views.enterout),

]

"""djangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import to include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app01.views import base, views, statistics, oldman, volunteers

urlpatterns = [
    # path('admin/', admin.site.urls),
    # www.xxx.com/index/ -> 函数

    # test 测试
    path('display/video/', views.video),
    path('event/list', statistics.eventList.as_view()),

    # BASE 基本
    path('user/login', base.login),
    path('user/register', base.register),
    path('user/modifypwd', base.modify_pwd),

    # OLD MAN 老人
    path('oldman/getall', oldman.get_all_oldman),
    path('oldman/getbyname', oldman.select_oldman_byname),
    path('oldman/delete', oldman.delete_by_id),
    path('oldman/add', oldman.add_oldman),
    path('oldman/modify', oldman.modify_oldman),

    # VOLUNTEERS 义工
    path('volunteers/getall', volunteers.get_all_volunteers),
    path('volunteers/getbyname', volunteers.select_volunteers_byname),
    path('volunteers/delete', volunteers.delete_by_id),
    path('volunteers/add', volunteers.add_volunteers),
    path('volunteers/modify', volunteers.modify_volunteers),


]

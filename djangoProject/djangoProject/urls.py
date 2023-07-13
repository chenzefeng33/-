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
from django.urls import path, re_path

from app01.views import base, employee, oldman, statistics, volunteers, websockets, live, views

urlpatterns = [
    # path('admin/', admin.site.urls),
    # www.xxx.com/index/ -> 函数

    # STATISTICS 静态方法
    path('statistics/upload', statistics.uploadAvatar),
    path('statistics/getimg/<str:type>/<str:id>/', statistics.getImg),

    # BASE 基本
    path('user/login', base.login),
    path('user/register', base.register),
    path('user/modifypwd', base.modify_pwd),

    # OLD MAN 老人
    path('oldman/getall', oldman.get_all_oldman),
    path('oldman/getbyname', oldman.select_oldman_byname),
    path('oldman/getbyidcard', oldman.select_oldman_byidcard),
    path('oldman/delete', oldman.delete_by_id),
    path('oldman/add', oldman.add_oldman),
    path('oldman/modify', oldman.modify_oldman),

    # VOLUNTEERS 义工
    path('volunteers/getall', volunteers.get_all_volunteers),
    path('volunteers/getbyname', volunteers.select_volunteers_byname),
    path('volunteers/getbyidcard', volunteers.select_volunteers_byidcard),
    path('volunteers/delete', volunteers.delete_by_id),
    path('volunteers/add', volunteers.add_volunteers),
    path('volunteers/modify', volunteers.modify_volunteers),

    # EMPLOYEE 工作人员
    path('employee/getall', employee.get_all_employee),
    path('employee/getbyname', employee.select_employee_byname),
    path('employee/delete', employee.delete_by_id),
    path('employee/add', employee.add_employee),
    path('employee/modify', employee.modify_employee),

    # CV 算法
    path('live/video/', live.play_video),

    # TEST 测试
    path('test/index/', views.index),
    path('test/index1/', views.index1),

]

websocket_urlpatterns = [
    # 前端请求websocket连接
    re_path(r'video/(?P<group>\w+)/$', websockets.VideoConsumer.as_asgi()),
    re_path(r'room/(?P<group>\w+)/$', websockets.ChatConsumer.as_asgi()),
]

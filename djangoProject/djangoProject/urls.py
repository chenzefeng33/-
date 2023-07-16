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
from django.urls import path

from app01.views import base, employee, oldman, statistics, volunteers, views, event

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

    # EVENT 事件
    path('event/add', event.add_event),

    # 视频流与事件的处理_测试接口
    path('display/video_test/', views.video_test),
    path('display/emo_frame/', views.emo_frame),

    # cv算法的开启、关闭接口
    path('display/emo_stream/', views.emo_stream),
    path('display/fall_stream/', views.fall_stream),
    path('display/close_emotion_stream/', views.close_emotion_stream),
    path('display/close_fall_stream/', views.close_fall_stream),

    # 录入人脸
    path('display/get_face/', views.getFace),
    # 加载人脸特征
    path('display/load_face/', views.loadFace),

    # 一个事件写入调用的接口-仅用于测试
    path('event/', views.write_to),
]
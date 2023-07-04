from django.shortcuts import render, redirect
from django.http import JsonResponse, StreamingHttpResponse
from django.core import serializers
import cv2

from app01.models import sys_user
from app01.models import event_info

# Create your views here.

def eventinfo_all(request):
    data_list = event_info.objects.all()
    data_list_json = serializers.serialize('json', data_list)
    print(data_list_json)

    return JsonResponse(data_list_json, safe=False)

def gen_display(camera):
    """
    视频流生成器功能。
    """
    while True:
        # 读取图片
        ret, frame = camera.read()
        if ret:
            # 将图片进行解码
            ret, frame = cv2.imencode('.jpeg', frame)
            if ret:
                # 转换为byte类型的，存储在迭代器中
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame.tobytes() + b'\r\n')

def video(request):
    """
    视频流路由。将其放入img标记的src属性中。
    例如：<img src='https://ip:port/uri' >
    """
    # 视频流相机对象
    camera = cv2.VideoCapture(0)
    # 使用流传输传输视频流
    return StreamingHttpResponse(gen_display(camera), content_type='multipart/x-mixed-replace; boundary=frame')

def login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    if username and password:
        try:
            user = sys_user.objects.get(UserName = username)
        except:
            return JsonResponse({'loginstatus':0}, safe=False)
        if user.Password == password:
            return JsonResponse({'loginstatus':1}, safe=False)
        return JsonResponse({'loginstatus':-1}, safe=False)

def register(request):
    try:
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password:
            same_user = sys_user.objects.filter(UserName=username)
            if same_user.exists():
                return JsonResponse({'rigisterstatus': 0}, safe=False)
            else:
                sys_user.objects.create(UserName=username, Password=password)
    except:
        return JsonResponse({'rigisterstatus': -1}, safe=False)
    return JsonResponse({'rigisterstatus': 1}, safe=False)
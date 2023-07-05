from django.shortcuts import render, redirect
from django.http import JsonResponse, StreamingHttpResponse
import cv2
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView

from djangoProject.serializer import EventSerializer
from app01.models import event_info

# Create your views here.

class eventList(APIView):
    def get(self,request):
        serialize = EventSerializer(instance=event_info.objects.all(), many=True)
        return Response(serialize.data)


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
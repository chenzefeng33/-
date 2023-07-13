from django.http import JsonResponse, StreamingHttpResponse
import cv2
from django.shortcuts import render


# Create your views here.

def gen_display(camera):
    """
    视频流生成器功能。
    """
    while True:
        # 读取图片
        ret, frame = camera.read()
        print(frame)
        print(ret)
        if ret:
            frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
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


def index(request):
    return render(request, "index.html")


def index1(request):
    response = render(request, "index1.html")
    response['cache-control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    return response

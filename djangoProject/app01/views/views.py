import csv
from datetime import datetime

import cv2
from django.http import StreamingHttpResponse, JsonResponse
from rest_framework.decorators import api_view

from app01.Face_emotion_detect import Face_emotion_detect
from app01.models import oldperson_info
from app01.views.unjson import UnJson
from cvSource.emotionSource.features_extraction_to_csv import load_face_features_to_csv
from cvSource.emotionSource.get_faces_from_camera import Face_Register
from djangoProject.serializer import EventSerializer
from fallSource import fallDetection
from fallSource.fallDetection import fall_detect_stream

"""
设置相机捕获的视频流的参数
"""


def setCamera(camera):
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)
    camera.set(cv2.CAP_PROP_FPS, 15)


"""
原生人脸视频流传输到前端，对应的是video_test.html
"""


def faceDetect(camera):
    """
    视频流生成器功能。
    """
    while True:
        # 读取图片
        ret, frame = camera.read()

        if ret:
            # 将图片进行解码
            ret, frame = cv2.imencode('.jpeg', frame)
            # 转换为byte类型的，存储在迭代器中
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame.tobytes() + b'\r\n')


def video_test(request):
    # 视频流相机对象
    camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    # 使用流传输传输视频流
    return StreamingHttpResponse(faceDetect(camera), content_type='multipart/x-mixed-replace; boundary=frame')


"""
人脸检测+情感识别的源码
"""

# 加载情感检测器
Face_Recognizer_con = Face_emotion_detect()


def append_data_to_csv_view(file_path, data_list):
    with open(file_path, 'a', newline='') as file:
        writer = csv.writer(file)
        for data in data_list:
            writer.writerow(data)


"""
cv算法接收 视频流 进行处理
"""


def close_emotion_stream(request):
    Face_Recognizer_con.open = 0


def face_emotion_detect_stream():
    Face_Recognizer_con.open = 1
    Face_Recognizer_con.process()


def emo_stream(request):
    # 视频流相机对象
    # 使用流传输传输视频流,但是其实并没有传回到前端
    return StreamingHttpResponse(face_emotion_detect_stream(),
                                 content_type='multipart/x-mixed-replace; boundary=frame')


"""
cv算法接收 帧 进行处理
"""


def face_emotion_detect_frame(camera):
    count = 1
    while True:
        event = []
        ret, frame = camera.read()
        if count:
            count = 1 - count
            frame, event = Face_Recognizer_con.processFrame(frame, event)
            print("此处的event是", event)
            if event[0][0] == -1:
                event = []
        else:
            count = 1 - count
            print("原生推送")
        if event:
            append_data_to_csv_view("app01/elderSmileEvent.csv", event)
            print("=====当前获得到的事件是", event)

        ret, frame = cv2.imencode('.jpeg', frame)
        # 转换为byte类型的，存储在迭代器中
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame.tobytes() + b'\r\n')


def emo_frame(request):
    """
    视频流路由。将其放入img标记的src属性中。
    例如：<img src='https://ip:port/uri' >
    """
    # 视频流相机对象
    camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    # setCamera(camera)
    # 使用流传输传输视频流
    return StreamingHttpResponse(face_emotion_detect_frame(camera),
                                 content_type='multipart/x-mixed-replace; boundary=frame')


# 调用插入数据库方法实例
def write_to(request):
    event = ('elder', 'Tang', 'Happy', 565)
    elderName = event[1]
    elderId = oldperson_info.objects.filter(username=elderName).values('ID')
    print("对应的老人的id是", elderId[0]['ID'])
    eventType = 1
    eventLocation = "教室"
    eventDes = elderName + " in " + eventLocation + " smile"
    eventDate = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    event_send = {
        "event_type": eventType,
        "event_date": eventDate,
        "event_location": eventLocation,
        "event_desc": eventDes,
        "oldperson_id": elderId[0]['ID']
    }

    serializer = EventSerializer(data=event_send)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse({"status": "success", "message": "数据保存成功。"})
    else:
        return JsonResponse({"status": "error", "message": serializer.errors})


"""
人脸录入
"""


@api_view(['POST'])
def getFace(request):
    # 我需要的是录入人脸信息的type和name
    data = UnJson(request.data)
    typeNum = data.type
    name = data.name
    face_register = Face_Register(int(typeNum), name)
    face_register.run()
    return JsonResponse(typeNum, name, status=200)


"""
人脸特征加载
"""


@api_view(['POST'])
def loadFace(request):
    # 我需要的是录入人脸信息的type和name
    load_face_features_to_csv()
    return JsonResponse({"status": "success"}, status=200)

"""
跌倒检测
"""


def close_fall_stream(request):
    fallDetection.fallOpen = 0


def fall_detect_process(camera):
    fallDetection.fallOpen = 1
    fall_detect_stream(camera)


def fall_stream(request):
    # 视频流相机对象
    camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    # setCamera(camera)
    # 使用流传输传输视频流
    return StreamingHttpResponse(fall_detect_process(camera),
                                 content_type='multipart/x-mixed-replace; boundary=frame')

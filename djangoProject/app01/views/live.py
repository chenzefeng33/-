import queue
import subprocess as sp
import threading

import cv2 as cv
from django.http import JsonResponse
from rest_framework.decorators import api_view

from app01.views.cv import faceDetectProcess, fallDetectProcess, emotionDetectProcess
from app01.views.unjson import UnJson


class Live(object):
    def __init__(self, way):
        self.way = way
        self.frame_queue = queue.Queue()
        self.command = ""
        # 自行设置
        self.rtmpUrl = "rtmp://localhost:1935/live/home"
        self.camera_path = 0

    def read_frame(self):
        print("开启推流")
        cap = cv.VideoCapture(0)
        # Get video information
        fps = int(cap.get(cv.CAP_PROP_FPS))
        width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))

        # ffmpeg command
        self.command = ['ffmpeg',
                        '-y',
                        '-f', 'rawvideo',
                        '-vcodec', 'rawvideo',
                        '-pix_fmt', 'bgr24',
                        '-s', "{}x{}".format(width, height),
                        '-r', str(fps),
                        '-i', '-',
                        '-c:v', 'libx264',
                        '-pix_fmt', 'yuv420p',
                        '-preset', 'ultrafast',
                        '-f', 'flv',
                        self.rtmpUrl]

        # read webcamera
        while cap.isOpened():
            ret, frame = cap.read()

            if not ret:
                print("Opening camera is failed")
                # 说实话这里的break应该替换为：
                cap = cv.VideoCapture(self.camera_path)
                # 因为我这俩天遇到的项目里出现断流的毛病
                # 特别是拉取rtmp流的时候！！！！
                # break

            # put frame into queue
            self.frame_queue.put(frame)

        cap.release()

    def push_frame(self):
        # 防止多线程时 command 未被设置
        while True:
            if len(self.command) > 0:
                # 管道配置
                p = sp.Popen(self.command, shell=False, stdin=sp.PIPE)
                break

        while True:
            if not self.frame_queue.empty():
                frame = self.frame_queue.get()
                # process frame
                # 你处理图片的代码
                if self.way == "face":
                    faceDetectProcess(frame)
                elif self.way == "fall":
                    fallDetectProcess(frame)
                elif self.way == "emotion":
                    emotionDetectProcess(frame)
                # write to pipe
                p.stdin.write(frame.tostring())

        p.stdin.close()

        p.wait()

    def run(self):
        threads = [
            threading.Thread(target=Live.read_frame, args=(self,)),
            threading.Thread(target=Live.push_frame, args=(self,))
        ]
        [thread.setDaemon(True) for thread in threads]
        [thread.start() for thread in threads]


@api_view(['POST'])
def play_video(request):
    data = UnJson(request.data)
    # 推流
    live = Live(data.way)
    live.run()
    return JsonResponse({'status': '推流成功', 'code': 200}, safe=False)

# def play_video(request):
#     # 视频读取对象
#     cap = cv.VideoCapture(0, cv.CAP_DSHOW)
#
#     # 推流地址
#     rtsp = "rtmp://localhost:1935/live/home"  # 推流的服务器地址
#     # 设置推流的参数
#     command = ['ffmpeg',
#                '-y',
#                '-f', 'rawvideo',
#                '-vcodec', 'rawvideo',
#                '-pix_fmt', 'bgr24',
#                '-s', '640*480',  # 根据输入视频尺寸填写
#                '-r', '30',
#                '-i', '-',
#                '-c:v', 'libx264',
#                '-pix_fmt', 'yuv420p',
#                '-preset', 'ultrafast',
#                '-f', 'flv',
#                rtsp]
#     # 创建、管理子进程
#     pipe = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE)
#     size = (int(cap.get(cv.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv.CAP_PROP_FRAME_HEIGHT)))
#
#     # 循环读取
#     num = 0
#     while cap.isOpened():
#         num = num + 1
#         # 读取一帧
#         ret, frame = cap.read()
#         faceDetectProcess(frame)
#         if frame is None:
#             print('read frame err!')
#             continue
#
#         # 显示一帧
#         cv.imshow("frame", frame)
#
#         # 按键退出
#         if cv.waitKey(1) & 0xFF == ord('q'):
#             break
#
#         # 读取尺寸、推流
#         img = cv.resize(src=frame, dsize=size)
#
#         pipe.stdin.write(img.tobytes())
#
#     # 关闭输入流
#     pipe.stdin.close()
#
#     # 等待子进程结束
#     pipe.wait()
#
#     # 关闭窗口
#     cv.destroyAllWindows()
#
#     # 停止读取
#     cap.release()

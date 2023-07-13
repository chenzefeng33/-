import pickle
from statistics import mode

import numpy as np
from django.http import StreamingHttpResponse
from keras.models import load_model

from cvSource.emotionDetect.utils.datasets import get_labels
from cvSource.emotionDetect.utils.inference import apply_offsets, draw_bounding_box, draw_texts
from cvSource.emotionDetect.utils.preprocessor import preprocess_input
from cvSource.fallDetect.fallDetection import *


def setCamera(camera):
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)
    camera.set(cv2.CAP_PROP_FPS, 15)


def faceDetect(camera):
    """
    视频流生成器功能。
    """
    while True:
        # 读取图片
        ret, frame = camera.read()
        faceDetectProcess(frame)
        if ret:
            # 将图片进行解码
            ret, frame = cv2.imencode('.jpeg', frame)
            # 转换为byte类型的，存储在迭代器中
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame.tobytes() + b'\r\n')


def emotionDetect(camera):
    """
        视频流生成器功能。
        """
    while True:
        # 读取图片
        ret, frame = camera.read()
        emotionDetectProcess(frame)
        if ret:
            # 将图片进行解码
            ret, frame = cv2.imencode('.jpeg', frame)
            # 转换为byte类型的，存储在迭代器中
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame.tobytes() + b'\r\n')


def fallDetect(camera):
    """
        视频流生成器功能。
        """
    while True:
        # 读取图片
        ret, frame = camera.read()
        fallDetectProcess(frame)
        if ret:
            # 将图片进行解码
            ret, frame = cv2.imencode('.jpeg', frame)
            # 转换为byte类型的，存储在迭代器中
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame.tobytes() + b'\r\n')


def video(request):
    """
    视频流路由。将其放入img标记的src属性中。
    例如：<img src='https://ip:port/uri' >
    """
    # 视频流相机对象
    camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    setCamera(camera)
    # 使用流传输传输视频流
    return StreamingHttpResponse(faceDetect(camera), content_type='multipart/x-mixed-replace; boundary=frame')


def emotion(request):
    """
        视频流路由。将其放入img标记的src属性中。
        例如：<img src='https://ip:port/uri' >
        """
    # 视频流相机对象
    camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    # setCamera(camera)
    # 使用流传输传输视频流
    return StreamingHttpResponse(emotionDetect(camera), content_type='multipart/x-mixed-replace; boundary=frame')


def fall(request):
    """
            视频流路由。将其放入img标记的src属性中。
            例如：<img src='https://ip:port/uri' >
            """
    # 视频流相机对象
    camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    # setCamera(camera)
    # 使用流传输传输视频流
    return StreamingHttpResponse(fallDetect(camera), content_type='multipart/x-mixed-replace; boundary=frame')


def faceDetectProcess(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces_rect = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
    for (x, y, w, h) in faces_rect:
        face = gray[y:y + h, x:x + w]
        face = cv2.resize(face, (128, 128))

        # 进行人脸识别
        label_id, confidence = face_recognizer.predict(face)

        if confidence < 99:
            # 已知人脸
            label = list(label_mapping.keys())[list(label_mapping.values()).index(label_id)]
            cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        else:
            # 陌生人
            cv2.putText(frame, "Unknown", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)


def emotionDetectProcess(frame):
    gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5,
                                          minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)

    for face_coordinates in faces:
        x1, x2, y1, y2 = apply_offsets(face_coordinates, emotion_offsets)
        x, y, w, h = face_coordinates
        gray_face = gray_image[y1:y2, x1:x2]
        try:
            gray_face = cv2.resize(gray_face, emotion_target_size)
        except:
            continue

        gray_face = preprocess_input(gray_face, True)
        gray_face = np.expand_dims(gray_face, 0)
        gray_face = np.expand_dims(gray_face, -1)
        emotion_prediction = emotion_classifier.predict(gray_face)
        emotion_probability = np.max(emotion_prediction)
        emotion_label_arg = np.argmax(emotion_prediction)
        emotion_text = emotion_labels[emotion_label_arg]
        emotion_window.append(emotion_text)

        if len(emotion_window) > frame_window:
            emotion_window.pop(0)
        try:
            emotion_mode = mode(emotion_window)
        except:
            continue

        if emotion_text == 'angry':
            color = emotion_probability * np.asarray((255, 0, 0))
        elif emotion_text == 'sad':
            color = emotion_probability * np.asarray((0, 0, 255))
        elif emotion_text == 'happy':
            color = emotion_probability * np.asarray((255, 255, 0))
        elif emotion_text == 'surprise':
            color = emotion_probability * np.asarray((0, 255, 255))
        else:
            color = emotion_probability * np.asarray((0, 255, 0))

        color = color.astype(int)
        color = color.tolist()

        # draw_text(face_coordinates, frame, label, emotion_mode, color, 0, -45, 1, 1)

        """
        """
        face = gray_image[y:y + h, x:x + w]
        face = cv2.resize(face, (128, 128))
        label_id, confidence = face_recognizer.predict(face)

        if confidence < 99:
            # 已知人脸
            label = list(label_mapping.keys())[list(label_mapping.values()).index(label_id)]
            draw_bounding_box(face_coordinates, frame, color)
            draw_texts(face_coordinates, frame, label, emotion_mode, color, 0, -45, 1, 1)
        else:
            # 陌生人
            draw_bounding_box(face_coordinates, frame, color)
            draw_texts(face_coordinates, frame, "Unknown", emotion_mode, color, 0, -45, 1, 1)
        """
        """


def fallDetectProcess(image):
    # 初始化姿势估计器
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:

        # 将图像转换为 RGB 格式
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # 进行姿势估计
        results = pose.process(image_rgb)

        # 绘制检测到的姿势
        if results.pose_landmarks:
            mp_drawing.draw_landmarks(
                image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            # 检测到的姿势
            pose_landmarks = results.pose_landmarks

            if pose_landmarks:
                # 提取人物的边界框
                image_height, image_width, _ = image.shape
                bounding_box = get_pose_bounding_box(pose_landmarks, image_height, image_width)

                # 在图像上绘制矩形框
                cv2.rectangle(image, bounding_box[0], bounding_box[1], (0, 255, 0), 2)

            # 检测人物动作
            is_standing = is_person_standing(results.pose_landmarks)
            is_sitting = is_person_sitting(results.pose_landmarks)
            is_laying = is_person_laying(results.pose_landmarks)
            is_falling = is_person_falling(results.pose_landmarks)

            # 根据动作显示文本提示
            # 根据动作显示文本提示
            if is_standing:
                draw_text(image, 'Standing', bounding_box)
            elif is_falling:
                draw_text(image, 'Falling', bounding_box)
            elif is_laying:
                draw_text(image, 'Laying', bounding_box)
            elif is_sitting:
                draw_text(image, 'Sitting', bounding_box)



"""
进行模型加载和参数加载,人脸识别
"""
# 加载训练好的模型
face_recognizer = cv2.face.LBPHFaceRecognizer_create()
face_recognizer.read("cvSource/faceDetect/detectPeople/face_recognizer_model.xml")

# 加载 label_mapping 和 face_boxes
with open("cvSource/faceDetect/detectPeople/label_mapping.pkl", "rb") as f:
    label_mapping = pickle.load(f)
with open("cvSource/faceDetect/detectPeople/face_boxes.pkl", "rb") as f:
    face_boxes = pickle.load(f)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
"""
进行模型加载，用于情感分析
"""
# parameters for loading data and images
emotion_model_path = 'cvSource/emotionDetect/models/emotion_model.hdf5'
emotion_labels = get_labels('fer2013')

# hyper-parameters for bounding boxes shape
frame_window = 10
emotion_offsets = (20, 40)

# loading models
# face_cascade = cv2.CascadeClassifier('./models/haarcascade_frontalface_default.xml')
emotion_classifier = load_model(emotion_model_path)

# getting input model shapes for inference
emotion_target_size = emotion_classifier.input_shape[1:3]

# starting lists for calculating modes
emotion_window = []

"""
加载跌倒检测的代码
"""
# 初始化 MediaPipe 的姿势估计模块
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# 定义动作阈值和关键点索引

# 全局变量
prev_pose_landmarks = None
prev_time = None

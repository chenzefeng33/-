import cv2
import os
import numpy as np
import pickle


def train_face_recognizer(data_dir):
    face_boxes = {}
    faces = []
    labels = []
    label_mapping = {}
    current_label = 0

    # 遍历数据集目录
    for root, dirs, files in os.walk(data_dir):
        for file in files:
            if file.endswith(".jpg") or file.endswith(".png"):
                # 获取图像文件路径和标签
                image_path = os.path.join(root, file)
                label = os.path.basename(root)
                if label not in label_mapping:
                    label_mapping[label] = current_label
                    current_label += 1
                label_id = label_mapping[label]

                # 读取图像并进行人脸检测
                image = cv2.imread(image_path)
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
                faces_rect = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

                for (x, y, w, h) in faces_rect:
                    # 提取人脸区域
                    face = gray[y:y + h, x:x + w]
                    face = cv2.resize(face, (128, 128))

                    # 将人脸数据和标签添加到训练集
                    faces.append(face)
                    labels.append(label_id)

                    # 记录每个人脸对应的标注框坐标
                    face_boxes[(label_id, len(faces) - 1)] = (x, y, w, h)

    # 创建并训练人脸识别模型
    face_recognizer = cv2.face.LBPHFaceRecognizer_create()
    face_recognizer.train(faces, np.array(labels))

    # 保存模型、label_mapping 和 face_boxes
    face_recognizer.save("face_recognizer_model.xml")
    with open("label_mapping.pkl", "wb") as f:
        pickle.dump(label_mapping, f)
    with open("face_boxes.pkl", "wb") as f:
        pickle.dump(face_boxes, f)

    print("模型已保存")

    return face_recognizer, label_mapping, face_boxes


# 数据集目录，其中每个子目录名为人物姓名，包含该人物的人脸图像
data_dir = "../faces_dataset"

# 训练人脸识别器
face_recognizer, label_mapping, face_boxes = train_face_recognizer(data_dir)





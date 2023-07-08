import cv2
import os
import time


def main():
    cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

    if not cap.isOpened():
        print("无法打开摄像头。")
        return

    # 加载人脸检测模型
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    output_dir = input("请输入图像输出目录名称：")  # 获取用户输入的目录名称
    output_path = os.path.join("../faces_dataset", output_dir)  # 构建输出目录路径

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    face_count = 0  # 人脸计数器

    while True:
        start_time = time.time()  # 记录开始时间
        while len(os.listdir(output_path)) < 500:  # 持续获取图像200张之后自动关闭
            ret, frame = cap.read()  # cap读取每一帧的图像
            if not ret:
                print("无法读取视频流。")
                break
            # 我们只需要进行检测，因此转为灰度图便于分析
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.3, minNeighbors=5)

            for (x, y, w, h) in faces:
                if w >= 200 and h >= 200:  # 检查人脸图像尺寸是否正确
                    face_roi = frame[y:y + h, x:x + w]
                    face_file_path = os.path.join(output_path, f"{output_dir}_{face_count}.jpg")
                    cv2.imwrite(face_file_path, face_roi)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 2)
                    face_count += 1

            cv2.imshow('Video', frame)
            k = cv2.waitKey(1)
            if k == 27:
                break

        break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

import cv2
import pickle


def recognize_faces(face_recognizer, label_mapping, face_boxes):
    cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

    if not cap.isOpened():
        print("无法打开摄像头。")
        return

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    while True:
        ret, frame = cap.read()

        if not ret:
            print("无法读取视频流。")
            break

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
        cv2.imshow('vedio', frame)

        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


# 加载训练好的模型
face_recognizer = cv2.face.LBPHFaceRecognizer_create()
face_recognizer.read("face_recognizer_model.xml")

# 加载 label_mapping 和 face_boxes
with open("label_mapping.pkl", "rb") as f:
    label_mapping = pickle.load(f)
with open("face_boxes.pkl", "rb") as f:
    face_boxes = pickle.load(f)

# 进行人脸识别
recognize_faces(face_recognizer, label_mapping, face_boxes)


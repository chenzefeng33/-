import sys
import time

import cv2
import numpy as np
import torch
import torchvision.transforms.transforms as transforms

from cvSource.emotionSource.face_alignment.face_alignment import FaceAlignment
from cvSource.emotionSource.face_detector.face_detector import DnnDetector
from cvSource.emotionSource.model.model import Mini_Xception
from cvSource.emotionSource.utils import histogram_equalization, get_label_emotion

sys.path.insert(1, 'face_detector')
device = torch.device("cpu")

# Initialize models and detectors
mini_xception = Mini_Xception().to(device)
mini_xception.eval()

root = 'cvSource/emotionSource/face_detector'
face_detector = DnnDetector(root)
face_alignment = FaceAlignment()

# Load model
checkpoint = torch.load("cvSource/emotionSource/checkpoint/model_weights/weights_epoch_75.pth.tar", map_location=device)
mini_xception.load_state_dict(checkpoint['mini_xception'])


def process_frame(frame, emo_list):
    t2 = time.time()
    process_frame.t1 = t2

    # faces
    faces = face_detector.detect_faces(frame)
    length = len(faces)
    print("长度是：" + str(length) + "\n")
    for face in faces:
        (x, y, w, h) = face

        # preprocessing
        input_face = face_alignment.frontalize_face(face, frame)
        input_face = cv2.resize(input_face, (48, 48))

        input_face = histogram_equalization(input_face)
        cv2.imshow('input face', cv2.resize(input_face, (120, 120)))

        input_face = transforms.ToTensor()(input_face).to(device)
        input_face = torch.unsqueeze(input_face, 0)

        with torch.no_grad():
            input_face = input_face.to(device)
            t = time.time()
            emotion = mini_xception(input_face)
            # print(f'\ntime={(time.time() - t) * 1000} ms')

            torch.set_printoptions(precision=6)
            softmax = torch.nn.Softmax()
            emotions_soft = softmax(emotion.squeeze()).reshape(-1, 1).cpu().detach().numpy()
            emotions_soft = np.round(emotions_soft, 3)
            for i, em in enumerate(emotions_soft):
                em = round(em.item(), 3)
                # print(f'{get_label_emotion(i)} : {em}')

            emotion = torch.argmax(emotion)
            percentage = round(emotions_soft[emotion].item(), 2)
            emotion = emotion.squeeze().cpu().detach().item()
            emotion = get_label_emotion(emotion)

            frame[y - 30:y, x:x + w] = (50, 50, 50)
            cv2.putText(frame, emotion, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 200, 200))
            cv2.putText(frame, str(percentage), (x + w - 40, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (200, 200, 0))
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 3)
            emo_list.append((x, emotion))

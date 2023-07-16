import logging
import os
import time

import cv2
import dlib
import numpy as np
import pandas as pd

from cvSource.emotionSource.emotionGet import process_frame

# Dlib 正向人脸检测器 / Use frontal face detector of Dlib
detector = dlib.get_frontal_face_detector()

# Dlib 人脸 landmark 特征点检测器 / Get face landmarks
predictor = dlib.shape_predictor('cvSource/emotionSource/data/data_dlib/shape_predictor_68_face_landmarks.dat')

# Dlib Resnet 人脸识别模型, 提取 128D 的特征矢量 / Use Dlib resnet50 model to get 128D face descriptor
face_reco_model = dlib.face_recognition_model_v1(
    "cvSource/emotionSource/data/data_dlib/dlib_face_recognition_resnet_model_v1.dat")

name_type_table = dict()
elder_smile_count = dict()

smile_limit = 5


class Face_emotion_detect:
    def __init__(self):
        self.font = cv2.FONT_ITALIC

        # FPS
        self.frame_time = 0
        self.frame_start_time = 0
        self.fps = 0
        self.fps_show = 0
        self.start_time = time.time()

        # cnt for frame
        self.frame_cnt = 0

        # 用来存放所有录入人脸特征的数组 / Save the features of faces in the database
        self.face_features_known_list = []
        # 存出对应人脸的类型
        self.face_name_known_type = []
        # 存储录入人脸名字 / Save the name of faces in the database
        self.face_name_known_list = []

        # 用来存储上一帧和当前帧 ROI 的质心坐标 / List to save centroid positions of ROI in frame N-1 and N
        self.last_frame_face_centroid_list = []
        self.current_frame_face_centroid_list = []

        # 用来存储上一帧和当前帧检测出目标的名字 / List to save names of objects in frame N-1 and N
        self.last_frame_face_n1ame_list = []
        self.current_frame_face_name_list = []

        # 上一帧和当前帧中人脸数的计数器 / cnt for faces in frame N-1 and N
        self.last_frame_face_cnt = 0
        self.current_frame_face_cnt = 0

        # 用来存放进行识别时候对比的欧氏距离 / Save the e-distance for faceX when recognizing
        self.current_frame_face_X_e_distance_list = []

        # 存储当前摄像头中捕获到的所有人脸的坐标名字 / Save the positions and names of current faces captured
        self.current_frame_face_position_list = []
        # 存储当前摄像头中捕获到的人脸特征 / Save the features of people in current frame
        self.current_frame_face_feature_list = []

        # e distance between centroid of ROI in last and current frame
        self.last_current_frame_centroid_e_distance = 0

        # 控制再识别的后续帧数 / Reclassify after 'reclassify_interval' frames
        # 如果识别出 "unknown" 的脸, 将在 reclassify_interval_cnt 计数到 reclassify_interval 后, 对于人脸进行重新识别
        self.reclassify_interval_cnt = 0
        self.reclassify_interval = 10

        self.name_type_list = {"unknown": ""}

    # 从 "features_all.csv" 读取录入人脸特征 / Get known faces from "features_all.csv"
    def get_face_database(self):
        if os.path.exists("cvSource/emotionSource/data/features_all.csv"):
            path_features_known_csv = "cvSource/emotionSource/data/features_all.csv"
            csv_rd = pd.read_csv(path_features_known_csv, header=None)
            for i in range(csv_rd.shape[0]):
                features_someone_arr = []
                self.face_name_known_type.append(csv_rd.iloc[i][0])
                self.face_name_known_list.append(csv_rd.iloc[i][1])
                self.name_type_list[str(csv_rd.iloc[i][1])] = str(csv_rd.iloc[i][0])
                for j in range(2, 130):
                    if csv_rd.iloc[i][j] == '':
                        features_someone_arr.append('0')
                    else:
                        features_someone_arr.append(csv_rd.iloc[i][j])
                self.face_features_known_list.append(features_someone_arr)
            logging.info("Faces in Database： %d", len(self.face_features_known_list))
            return 1
        else:
            logging.warning("'features_all.csv' not found!")
            logging.warning("Please run 'get_faces_from_camera.py' "
                            "and 'features_extraction_to_csv.py' before 'face_reco_from_camera.py'")
            return 0

    def update_fps(self):
        now = time.time()
        # 每秒刷新 fps / Refresh fps per second
        if str(self.start_time).split(".")[0] != str(now).split(".")[0]:
            self.fps_show = self.fps
        self.start_time = now
        self.frame_time = now - self.frame_start_time
        self.fps = 1.0 / self.frame_time
        self.frame_start_time = now

    @staticmethod
    # 计算两个128D向量间的欧式距离 / Compute the e-distance between two 128D features
    def return_euclidean_distance(feature_1, feature_2):
        feature_1 = np.array(feature_1)
        feature_2 = np.array(feature_2)
        dist = np.sqrt(np.sum(np.square(feature_1 - feature_2)))
        return dist

    # 使用质心追踪来识别人脸 / Use centroid tracker to link face_x in current frame with person_x in last frame
    def centroid_tracker(self):
        for i in range(len(self.current_frame_face_centroid_list)):
            e_distance_current_frame_person_x_list = []
            # 对于当前帧中的人脸1, 和上一帧中的 人脸1/2/3/4/.. 进行欧氏距离计算 / For object 1 in current_frame, compute e-distance with
            # object 1/2/3/4/... in last frame
            for j in range(len(self.last_frame_face_centroid_list)):
                self.last_current_frame_centroid_e_distance = self.return_euclidean_distance(
                    self.current_frame_face_centroid_list[i], self.last_frame_face_centroid_list[j])

                e_distance_current_frame_person_x_list.append(
                    self.last_current_frame_centroid_e_distance)

            last_frame_num = e_distance_current_frame_person_x_list.index(
                min(e_distance_current_frame_person_x_list))
            self.current_frame_face_name_list[i] = self.last_frame_face_name_list[last_frame_num]

    # 生成的 cv2 window 上面添加说明文字 / putText on cv2 window
    def draw_note(self, img_rd):
        # 添加说明 / Add some info on windows
        cv2.putText(img_rd, "Face Recognizer with OT", (20, 40), self.font, 1, (255, 255, 255), 1, cv2.LINE_AA)
        cv2.putText(img_rd, "Frame:  " + str(self.frame_cnt), (20, 100), self.font, 0.8, (0, 255, 0), 1,
                    cv2.LINE_AA)
        cv2.putText(img_rd, "FPS:    " + str(self.fps.__round__(2)), (20, 130), self.font, 0.8, (0, 255, 0), 1,
                    cv2.LINE_AA)
        cv2.putText(img_rd, "Faces:  " + str(self.current_frame_face_cnt), (20, 160), self.font, 0.8, (0, 255, 0), 1,
                    cv2.LINE_AA)
        cv2.putText(img_rd, "Q: Quit", (20, 450), self.font, 0.8, (255, 255, 255), 1, cv2.LINE_AA)
        print("进入了画图----------------------------")
        for i in range(len(self.current_frame_face_name_list)):
            img_rd = cv2.putText(img_rd, "face:" + str(i + 1), tuple(
                [int(self.current_frame_face_centroid_list[i][0]), int(self.current_frame_face_centroid_list[i][1])]),
                                 self.font,
                                 0.8, (255, 190, 0),
                                 1,
                                 cv2.LINE_AA)
        return img_rd

    def run(self):
        cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)  # Get video stream from camera
        self.process(cap)

        cap.release()
        cv2.destroyAllWindows()

    """
    视频流处理写法
    """

    # 处理获取的视频流, 进行人脸识别 / Face detection and recognition wit OT from input video stream
    def process(self, stream):
        # 1. 读取存放所有人脸特征的 csv / Get faces known from "features.all.csv"
        if self.get_face_database():

            print("当前录入的人脸有:", self.name_type_list)
            while stream.isOpened():
                self.frame_cnt += 1
                logging.debug("Frame " + str(self.frame_cnt) + " starts")
                flag, img_rd = stream.read()
                img_rd = cv2.flip(img_rd, 1)
                kk = cv2.waitKey(1)

                emo_list = []
                img_rd = cv2.resize(img_rd, (640, 480))
                process_frame.t1 = 0
                process_frame(img_rd, emo_list)
                print("检测到的所有表情")
                print(emo_list)

                face_list = []

                # 2. 检测人脸 / Detect faces for frame X
                faces = detector(img_rd, 0)

                # 3. 更新人脸计数器 / Update cnt for faces in frames
                self.last_frame_face_cnt = self.current_frame_face_cnt
                self.current_frame_face_cnt = len(faces)

                # 4. 更新上一帧中的人脸列表 / Update the face name list in last frame
                self.last_frame_face_name_list = self.current_frame_face_name_list[:]

                # 5. 更新上一帧和当前帧的质心列表 / update frame centroid list
                self.last_frame_face_centroid_list = self.current_frame_face_centroid_list
                self.current_frame_face_centroid_list = []

                # 6.1 如果当前帧和上一帧人脸数没有变化 / if cnt not changes
                if (self.current_frame_face_cnt == self.last_frame_face_cnt) and (
                        self.reclassify_interval_cnt != self.reclassify_interval):
                    logging.debug(
                        "scene 1: 当前帧和上一帧相比没有发生人脸数变化 / No face cnt changes in this frame!!!")

                    self.current_frame_face_position_list = []

                    if "unknown" in self.current_frame_face_name_list:
                        logging.debug("  有未知人脸, 开始进行 reclassify_interval_cnt 计数")
                        self.reclassify_interval_cnt += 1

                    if self.current_frame_face_cnt != 0:
                        for k, d in enumerate(faces):
                            self.current_frame_face_position_list.append(tuple(
                                [faces[k].left(), faces[k].top() - 5]))
                            self.current_frame_face_centroid_list.append(
                                [int(faces[k].left() + faces[k].right()) / 2,
                                 int(faces[k].top() + faces[k].bottom()) / 2])

                            img_rd = cv2.rectangle(img_rd,
                                                   tuple([d.left(), d.top()]),
                                                   tuple([d.right(), d.bottom()]),
                                                   (255, 255, 255), 2)

                    # 如果当前帧中有多个人脸, 使用质心追踪 / Multi-faces in current frame, use centroid-tracker to track
                    if self.current_frame_face_cnt != 1:
                        self.centroid_tracker()

                    for i in range(self.current_frame_face_cnt):
                        # 6.2 Write names under ROI
                        charac = self.name_type_list[self.current_frame_face_name_list[i]]
                        name = self.current_frame_face_name_list[i]
                        text = charac + name

                        face_list.append((self.current_frame_face_position_list[i][0], charac, name))
                        """
                        这里是第二次画图，outText，这就是最终显示到输出视频流上的frame的东西

                        """
                        img_rd = cv2.putText(img_rd,
                                             text,
                                             self.current_frame_face_position_list[i], self.font, 0.8, (0, 255, 255), 1,
                                             cv2.LINE_AA)
                    res = elderSmileEvent(emo_list, face_list)
                    print("当前返回的事件类型是:", res)
                    """
                    这里的意思是同意跳转到最终的视频帧的处理，即写上相关的附加信息
                    """
                    self.draw_note(img_rd)

                # 6.2 如果当前帧和上一帧人脸数发生变化 / If cnt of faces changes, 0->1 or 1->0 or ...
                else:
                    logging.debug("scene 2: 当前帧和上一帧相比人脸数发生变化 / Faces cnt changes in this frame")
                    self.current_frame_face_position_list = []
                    self.current_frame_face_X_e_distance_list = []
                    self.current_frame_face_feature_list = []
                    self.reclassify_interval_cnt = 0

                    # 6.2.1 人脸数减少 / Face cnt decreases: 1->0, 2->1, ...
                    if self.current_frame_face_cnt == 0:
                        logging.debug("  scene 2.1 人脸消失, 当前帧中没有人脸 / No faces in this frame!!!")
                        # clear list of names and features
                        self.current_frame_face_name_list = []
                    # 6.2.2 人脸数增加 / Face cnt increase: 0->1, 0->2, ..., 1->2, ...
                    else:
                        logging.debug(
                            "  scene 2.2 出现人脸, 进行人脸识别 / Get faces in this frame and do face recognition")
                        self.current_frame_face_name_list = []
                        for i in range(len(faces)):
                            shape = predictor(img_rd, faces[i])
                            self.current_frame_face_feature_list.append(
                                face_reco_model.compute_face_descriptor(img_rd, shape))
                            self.current_frame_face_name_list.append("unknown")

                        # 6.2.2.1 遍历捕获到的图像中所有的人脸 / Traversal all the faces in the database
                        for k in range(len(faces)):
                            logging.debug("  For face %d in current frame:", k + 1)
                            self.current_frame_face_centroid_list.append(
                                [int(faces[k].left() + faces[k].right()) / 2,
                                 int(faces[k].top() + faces[k].bottom()) / 2])

                            self.current_frame_face_X_e_distance_list = []

                            # 6.2.2.2 每个捕获人脸的名字坐标 / Positions of faces captured
                            self.current_frame_face_position_list.append(tuple(
                                [faces[k].left(), faces[k].top() + 5]))

                            # 6.2.2.3 对于某张人脸, 遍历所有存储的人脸特征
                            # For every faces detected, compare the faces in the database
                            for i in range(len(self.face_features_known_list)):
                                # 如果 q 数据不为空
                                if str(self.face_features_known_list[i][0]) != '0.0':
                                    e_distance_tmp = self.return_euclidean_distance(
                                        self.current_frame_face_feature_list[k],
                                        self.face_features_known_list[i])
                                    logging.debug("      with person %d, the e-distance: %f", i + 1, e_distance_tmp)
                                    self.current_frame_face_X_e_distance_list.append(e_distance_tmp)
                                else:
                                    # 空数据 person_X
                                    self.current_frame_face_X_e_distance_list.append(999999999)

                            # 6.2.2.4 寻找出最小的欧式距离匹配 / Find the one with minimum e distance
                            similar_person_num = self.current_frame_face_X_e_distance_list.index(
                                min(self.current_frame_face_X_e_distance_list))

                            if min(self.current_frame_face_X_e_distance_list) < 0.4:
                                self.current_frame_face_name_list[k] = self.face_name_known_list[similar_person_num]

                                logging.debug("  Face recognition result: %s",
                                              self.face_name_known_list[similar_person_num])
                            else:
                                logging.debug("  Face recognition result: Unknown person")

                        # 7. 生成的窗口添加说明文字 / Add note on cv2 window
                        self.draw_note(img_rd)

                        # cv2.imwrite("debug/debug_" + str(self.frame_cnt) + ".png", img_rd) # Dump current frame
                        # image if needed

                # 8. 按下 'q' 键退出 / Press 'q' to exit
                if kk == ord('q'):
                    break

                self.update_fps()

                cv2.namedWindow("camera", 1)
                cv2.imshow("camera", img_rd)

                logging.debug("Frame ends\n\n")

                res = elderSmileEvent(emo_list, face_list)
                print(">>>>>>>>>>>>这是后来的", res)
                # return "woshi"

    """
    这里是新写的，只对frame进行处理
    """

    def processFrame(self, frame, event):
        # 1. 读取存放所有人脸特征的 csv / Get faces known from "features.all.csv"
        if self.get_face_database():
            frame = frame[0]
            print("当前录入的人脸有:", self.name_type_list)
            self.frame_cnt += 1
            logging.debug("Frame " + str(self.frame_cnt) + " starts")
            frame = cv2.flip(frame, 1)
            cv2.waitKey(1)

            emo_list = []
            frame = cv2.resize(frame, (640, 480))
            process_frame.t1 = 0
            process_frame(frame, emo_list)
            print("检测到的所有表情")
            print(emo_list)

            face_list = []

            # 2. 检测人脸 / Detect faces for frame X
            faces = detector(frame, 0)

            # 3. 更新人脸计数器 / Update cnt for faces in frames
            self.last_frame_face_cnt = self.current_frame_face_cnt
            self.current_frame_face_cnt = len(faces)

            # 4. 更新上一帧中的人脸列表 / Update the face name list in last frame
            self.last_frame_face_name_list = self.current_frame_face_name_list[:]

            # 5. 更新上一帧和当前帧的质心列表 / update frame centroid list
            self.last_frame_face_centroid_list = self.current_frame_face_centroid_list
            self.current_frame_face_centroid_list = []

            # 6.1 如果当前帧和上一帧人脸数没有变化 / if cnt not changes
            if (self.current_frame_face_cnt == self.last_frame_face_cnt) and (
                    self.reclassify_interval_cnt != self.reclassify_interval):
                logging.debug(
                    "scene 1: 当前帧和上一帧相比没有发生人脸数变化 / No face cnt changes in this frame!!!")

                self.current_frame_face_position_list = []

                if "unknown" in self.current_frame_face_name_list:
                    logging.debug("  有未知人脸, 开始进行 reclassify_interval_cnt 计数")
                    self.reclassify_interval_cnt += 1

                if self.current_frame_face_cnt != 0:
                    for k, d in enumerate(faces):
                        self.current_frame_face_position_list.append(tuple(
                            [faces[k].left(), faces[k].top() - 5]))
                        self.current_frame_face_centroid_list.append(
                            [int(faces[k].left() + faces[k].right()) / 2,
                             int(faces[k].top() + faces[k].bottom()) / 2])

                        frame = cv2.rectangle(frame,
                                              tuple([d.left(), d.top()]),
                                              tuple([d.right(), d.bottom()]),
                                              (255, 255, 255), 2)

                # 如果当前帧中有多个人脸, 使用质心追踪 / Multi-faces in current frame, use centroid-tracker to track
                if self.current_frame_face_cnt != 1:
                    self.centroid_tracker()

                for i in range(self.current_frame_face_cnt):
                    # 6.2 Write names under ROI
                    charac = self.name_type_list[self.current_frame_face_name_list[i]]
                    name = self.current_frame_face_name_list[i]
                    text = charac + name

                    face_list.append((self.current_frame_face_position_list[i][0], charac, name))
                    """
                    这里是第二次画图，outText，这就是最终显示到输出视频流上的frame的东西
    
                    """
                    frame = cv2.putText(frame,
                                        text,
                                        self.current_frame_face_position_list[i], self.font, 0.8, (0, 255, 255), 1,
                                        cv2.LINE_AA)
                    print("人脸的text", text)
                res = elderSmileEvent(emo_list, face_list)
                print("帧率处理中当前返回 的事件类型是:", res)
                """
                这里的意思是同意跳转到最终的视频帧的处理，即写上相关的附加信息
                """
                # self.draw_note(frame)

            # 6.2 如果当前帧和上一帧人脸数发生变化 / If cnt of faces changes, 0->1 or 1->0 or ...
            else:
                logging.debug("scene 2: 当前帧和上一帧相比人脸数发生变化 / Faces cnt changes in this frame")
                self.current_frame_face_position_list = []
                self.current_frame_face_X_e_distance_list = []
                self.current_frame_face_feature_list = []
                self.reclassify_interval_cnt = 0

                # 6.2.1 人脸数减少 / Face cnt decreases: 1->0, 2->1, ...
                if self.current_frame_face_cnt == 0:
                    logging.debug("  scene 2.1 人脸消失, 当前帧中没有人脸 / No faces in this frame!!!")
                    # clear list of names and features
                    self.current_frame_face_name_list = []
                # 6.2.2 人脸数增加 / Face cnt increase: 0->1, 0->2, ..., 1->2, ...
                else:
                    logging.debug(
                        "  scene 2.2 出现人脸, 进行人脸识别 / Get faces in this frame and do face recognition")
                    self.current_frame_face_name_list = []
                    for i in range(len(faces)):
                        shape = predictor(frame, faces[i])
                        self.current_frame_face_feature_list.append(
                            face_reco_model.compute_face_descriptor(frame, shape))
                        self.current_frame_face_name_list.append("unknown")

                    # 6.2.2.1 遍历捕获到的图像中所有的人脸 / Traversal all the faces in the database
                    for k in range(len(faces)):
                        logging.debug("  For face %d in current frame:", k + 1)
                        self.current_frame_face_centroid_list.append(
                            [int(faces[k].left() + faces[k].right()) / 2,
                             int(faces[k].top() + faces[k].bottom()) / 2])

                        self.current_frame_face_X_e_distance_list = []

                        # 6.2.2.2 每个捕获人脸的名字坐标 / Positions of faces captured
                        self.current_frame_face_position_list.append(tuple(
                            [faces[k].left(), faces[k].top() + 5]))

                        # 6.2.2.3 对于某张人脸, 遍历所有存储的人脸特征
                        # For every faces detected, compare the faces in the database
                        for i in range(len(self.face_features_known_list)):
                            # 如果 q 数据不为空
                            if str(self.face_features_known_list[i][0]) != '0.0':
                                e_distance_tmp = self.return_euclidean_distance(
                                    self.current_frame_face_feature_list[k],
                                    self.face_features_known_list[i])
                                logging.debug("      with person %d, the e-distance: %f", i + 1, e_distance_tmp)
                                self.current_frame_face_X_e_distance_list.append(e_distance_tmp)
                            else:
                                # 空数据 person_X
                                self.current_frame_face_X_e_distance_list.append(999999999)

                        # 6.2.2.4 寻找出最小的欧式距离匹配 / Find the one with minimum e distance
                        similar_person_num = self.current_frame_face_X_e_distance_list.index(
                            min(self.current_frame_face_X_e_distance_list))

                        if min(self.current_frame_face_X_e_distance_list) < 0.4:
                            self.current_frame_face_name_list[k] = self.face_name_known_list[similar_person_num]

                            logging.debug("  Face recognition result: %s",
                                          self.face_name_known_list[similar_person_num])
                        else:
                            logging.debug("  Face recognition result: Unknown person")

                    # 7. 生成的窗口添加说明文字 / Add note on cv2 window
                    self.draw_note(frame)
            event = elderSmileEvent(emo_list, face_list)

            self.update_fps()

            return frame


def elderSmileEvent(emo_list, face_list):
    min_difference = float('inf')  # 初始化最小差值为正无穷大
    res = []
    for tuple1 in face_list:
        if str(tuple1[1]) == "elder":

            for tuple2 in emo_list:
                difference = abs(tuple1[0] - tuple2[0])  # 计算两个元组第一个元素的差值
                if difference < min_difference:
                    min_difference = difference
                    if tuple2[1] != "Happy":
                        elder_smile_count[tuple1[2]] = 0
                    else:
                        if elder_smile_count[tuple1[2]] is None:
                            elder_smile_count[tuple1[2]] = 0
                        elder_smile_count[tuple1[2]] += 1
                    if elder_smile_count[tuple1[2]] >= smile_limit:
                        res.append((tuple1[1], tuple1[2], tuple2[1], elder_smile_count[tuple1[2]]))

    return res


def main():
    logging.basicConfig(level=logging.INFO)
    Face_Recognizer_con = Face_emotion_detect()
    Face_Recognizer_con.run()


if __name__ == '__main__':
    main()

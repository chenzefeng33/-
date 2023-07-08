import cv2
import mediapipe as mp
import math
import time

# 初始化 MediaPipe 的姿势估计模块
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# 定义动作阈值和关键点索引

# 全局变量
prev_pose_landmarks = None
prev_time = None


def main():
    # 打开视频文件
    # video_path = 'video.mp4'
    # cap = cv2.VideoCapture(video_path)
    cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

    # 初始化姿势估计器
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            # 读取视频帧
            success, image = cap.read()
            if not success:
                break

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

            # 显示带有姿势估计结果和动作提示的图像
            cv2.namedWindow("Video",cv2.WINDOW_NORMAL)
            cv2.imshow('Video', image)

            # 按下 'q' 键退出循环
            if cv2.waitKey(1) & 0xFF == ord(' '):
                break

    # 释放视频文件和窗口
    cap.release()
    cv2.destroyAllWindows()


def draw_text(image, text, bounding_box):
    # 计算文本的位置
    x = bounding_box[0][0]
    y = bounding_box[0][1] - 10

    cv2.putText(image, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)


def is_person_standing(pose_landmarks):
    STANDING_THRESHOLD = 0.35
    left_ankle = pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ANKLE]
    right_ankle = pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ANKLE]
    left_hip = pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP]
    right_hip = pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP]
    left_shoulder = pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER]
    right_shoulder = pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER]

    # 计算脚踝和骨盆之间的垂直距离
    ankle_to_hip_distance = abs(left_ankle.y - left_hip.y) + abs(right_ankle.y - right_hip.y)

    # 计算肩膀和骨盆之间的垂直距离
    shoulder_to_hip_distance = abs(left_shoulder.y - left_hip.y) + abs(right_shoulder.y - right_hip.y)

    # 判断垂直距离是否小于阈值，同时保证肩膀和骨盆之间的距离足够接近（站立时，上半身通常是挺直的）
    is_standing = ankle_to_hip_distance > STANDING_THRESHOLD and shoulder_to_hip_distance > STANDING_THRESHOLD

    return is_standing


def is_person_sitting(pose_landmarks):
    SITTING_THRESHOLD = 0.55
    left_ankle = pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ANKLE]
    right_ankle = pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ANKLE]
    left_hip = pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP]
    right_hip = pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP]
    left_shoulder = pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER]
    right_shoulder = pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER]

    # 计算脚踝和骨盆之间的垂直距离
    ankle_to_hip_distance = abs(left_ankle.y - left_hip.y) + abs(right_ankle.y - right_hip.y)

    # 计算肩膀和骨盆之间的垂直距离
    # shoulder_to_hip_distance = abs(left_shoulder.y - left_hip.y) + abs(right_shoulder.y - right_hip.y)

    # 判断垂直距离是否小于阈值，同时保证肩膀和骨盆之间的距离较大（坐姿时，上半身通常会有弯曲）
    is_sitting = ankle_to_hip_distance < SITTING_THRESHOLD \
        # and shoulder_to_hip_distance < SITTING_THRESHOLD

    return is_sitting


def is_person_laying(pose_landmarks):
    LAYING_THRESHOLD = 0.35
    left_ankle = pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ANKLE]
    right_ankle = pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ANKLE]
    left_shoulder = pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER]
    right_shoulder = pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER]

    # 计算脚踝和肩膀之间的垂直距离
    ankle_to_shoulder_distance = abs(left_ankle.y - left_shoulder.y) + abs(right_ankle.y - right_shoulder.y)

    # 判断垂直距离是否大于阈值，同时保证肩膀和脚踝之间的距离足够接近（躺姿时，上半身通常是平躺的）
    is_laying = ankle_to_shoulder_distance < LAYING_THRESHOLD and ankle_to_shoulder_distance < LAYING_THRESHOLD * 2

    return is_laying


def is_person_falling(pose_landmarks):
    FALLING_ANGLE_THRESHOLD = 60  # 倾斜角度阈值，单位：度
    FALLING_VELOCITY_THRESHOLD = 10  # 速度阈值，单位：m/s

    left_shoulder = pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER]
    right_shoulder = pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER]
    left_hip = pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP]
    right_hip = pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP]

    # 计算肩膀和骨盆的倾斜角度
    shoulder_hip_angle = calculate_angle(left_shoulder, right_shoulder, left_hip, right_hip)

    # 获取关键点速度
    velocity = calculate_velocity(pose_landmarks)

    # 判断肩膀和骨盆的倾斜角度是否大于阈值，同时速度小于阈值（跌倒时，上半身通常会有较大倾斜，并且速度较慢）
    is_falling = velocity > FALLING_VELOCITY_THRESHOLD and shoulder_hip_angle > FALLING_ANGLE_THRESHOLD

    return is_falling


def calculate_angle(point1, point2, point3, point4):
    angle_rad = math.atan2(point4.y - point3.y, point4.x - point3.x) - math.atan2(point2.y - point1.y,
                                                                                  point2.x - point1.x)
    angle_deg = math.degrees(angle_rad)

    # 处理角度超出0-360范围的情况
    if angle_deg < 0:
        angle_deg += 360
    elif angle_deg >= 360:
        angle_deg -= 360

    return angle_deg


def calculate_velocity(pose_landmarks):
    global prev_pose_landmarks, prev_time

    if prev_pose_landmarks is None:
        prev_pose_landmarks = pose_landmarks
        prev_time = time.time()
        return 0.0

    current_time = time.time()
    time_interval = current_time - prev_time

    displacement = 0.0

    for i in range(len(pose_landmarks.landmark)):
        dx = pose_landmarks.landmark[i].x - prev_pose_landmarks.landmark[i].x
        dy = pose_landmarks.landmark[i].y - prev_pose_landmarks.landmark[i].y
        dz = pose_landmarks.landmark[i].z - prev_pose_landmarks.landmark[i].z
        displacement += math.sqrt(dx * dx + dy * dy + dz * dz)

    velocity = displacement / time_interval

    prev_pose_landmarks = pose_landmarks
    prev_time = current_time

    return velocity


def get_pose_bounding_box(pose_landmarks, image_height, image_width):
    # 获取人物姿势的最大和最小坐标
    min_x, min_y = image_width, image_height
    max_x, max_y = 0, 0

    for landmark in pose_landmarks.landmark:
        x, y = int(landmark.x * image_width), int(landmark.y * image_height)
        if x < min_x:
            min_x = x
        if x > max_x:
            max_x = x
        if y < min_y:
            min_y = y
        if y > max_y:
            max_y = y

    # 添加一些额外的空白区域来增加边界框的大小
    margin = 20
    min_x -= margin
    min_y -= margin
    max_x += margin
    max_y += margin

    return (min_x, min_y), (max_x, max_y)


if __name__ == "__main__":
    main()

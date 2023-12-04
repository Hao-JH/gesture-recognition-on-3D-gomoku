import cv2
import mediapipe as mp
import cmath
import numpy as np
import matplotlib.pyplot as plt
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


def gesture_func():
    hand_landmarks = [(0.1, 0.2, 0.3), (0.2, 0.3, 0.4)]


    gesture = ["none","one","two","three","four","five","six","seven","eight","nine","ten"]
    flag = 0

    mp_drawing = mp.solutions.drawing_utils
    mp_hands = mp.solutions.hands

    hands = mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.75,
            min_tracking_confidence=0.75)

    cap = cv2.VideoCapture(0)
    z_cor = []
    y_cor = []
    x_cor = []
    model_path = 'gesture_recognizer.task'
    # base_options = python.BaseOptions(model_asset_path=model_path)
    # options = vision.GestureRecognizerOptions(base_options=base_options)
    # recognizer = vision.GestureRecognizer.create_from_options(options)
    while True:
        flag = 0
        ret,frame = cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # 因为摄像头是镜像的，所以将摄像头水平翻转
        # 不是镜像的可以不翻转
        frame= cv2.flip(frame,1)
        results = hands.process(frame)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    #    if results.multi_handedness:
    #        for hand_label in results.multi_handedness:
    #            print(hand_label)
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                #print('hand_landmarks:', hand_landmarks)
                #计算关键点的距离，用于判断手指是否伸直
                # print(hand_landmarks.landmark[0])
                z_cor.append(np.mean([i.z for i in hand_landmarks.landmark])+hand_landmarks.landmark[8].z)
                y_cor.append(np.mean([i.y for i in hand_landmarks.landmark])+hand_landmarks.landmark[8].y)
                x_cor.append(np.mean([i.x for i in hand_landmarks.landmark])+hand_landmarks.landmark[8].x)
                p0_x = hand_landmarks.landmark[0].x
                p0_y = hand_landmarks.landmark[0].y
                p5_x = hand_landmarks.landmark[5].x
                p5_y = hand_landmarks.landmark[5].y
                distance_0_5 = pow(p0_x-p5_x,2)+pow(p0_y-p5_y,2)
                base = distance_0_5 / 0.6
                
                p4_x = hand_landmarks.landmark[4].x
                p4_y = hand_landmarks.landmark[4].y
                distance_5_4 = pow(p5_x-p4_x,2)+pow(p5_y-p4_y,2)
                
                p8_x = hand_landmarks.landmark[8].x
                p8_y = hand_landmarks.landmark[8].y
                distance_0_8 = pow(p0_x-p8_x,2)+pow(p0_y-p8_y,2)
                
                p12_x = hand_landmarks.landmark[12].x
                p12_y = hand_landmarks.landmark[12].y
                distance_0_12 = pow(p0_x-p12_x,2)+pow(p0_y-p12_y,2)
                
                p16_x = hand_landmarks.landmark[16].x
                p16_y = hand_landmarks.landmark[16].y
                distance_0_16 = pow(p0_x-p16_x,2)+pow(p0_y-p16_y,2)
                
                p20_x = hand_landmarks.landmark[20].x
                p20_y = hand_landmarks.landmark[20].y
                distance_0_20 = pow(p0_x-p20_x,2)+pow(p0_y-p20_y,2)
                
                
                if distance_0_8 > base:
                    flag += 1
                if distance_0_12 > base:
                    flag += 1
                if distance_0_16 > base:
                    flag += 1
                if distance_0_20 > base:
                    flag += 1
                if distance_5_4 > base*0.3:
                    flag += 1
                if flag>=10:
                    flag = 10
                # 关键点可视化
                mp_drawing.draw_landmarks(frame, 
                                        hand_landmarks, 
                                        mp_hands.HAND_CONNECTIONS)
                
            
        cv2.putText(frame,gesture[flag],(50,50),0,1.3,(0,0,255),3)
        cv2.imshow('MediaPipe Hands', frame)
        # if cv2.waitKey(1) & 0xFF == 27:
        #     break
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    cap.release()
    cv2.destroyAllWindows()


    # 绘制折线图
    plt.plot(z_cor)
    plt.plot(x_cor)
    plt.plot(y_cor)
    # 显示图形
    plt.show()

if __name__ == "__main__":
    gesture_func()
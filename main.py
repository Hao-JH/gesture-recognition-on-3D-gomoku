


import pygame as pg
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

from draw.draw_cube import wireCube,drawCubeGrid,draw_sphere,draw_material_sphere
from draw.pyramid import wirePyramid
from draw.axes import drawAxes
from draw.chessboard import Chessboard
# from draw.background import draw_background
import cv2
import mediapipe as mp
import cmath
import numpy as np
import matplotlib.pyplot as plt
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from collections import deque

import threading
import time

cb = Chessboard(5)

angle_x = 0  # 初始化视角的旋转角度（绕x轴）
angle_y = 0  # 初始化视角的旋转角度（绕y轴）
rotate = False  # 标记是否开始旋转视角

eye_x = 0  # 初始化视角的x坐标
eye_y = 0  # 初始化视角的y坐标
eye_z = 5  # 初始化视角的z坐标

cur_pos_x = 0
cur_pos_y = 0
cur_pos_z = 0

cur_hand_pos_x = 0
cur_hand_pos_y = 0
cur_hand_pos_z = 0

cur_stone_pos_x,cur_stone_pos_y,cur_stone_pos_z = 0,0,0

exit_event = threading.Event()

def game():
    pg.init()
    display = (800, 600)
    pg.display.set_mode(display, DOUBLEBUF | OPENGL)

    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)

    glTranslatef(0.0, 0.0, -5)

    global cb

    # angle_x = 0  # 初始化视角的旋转角度（绕x轴）
    # angle_y = 0  # 初始化视角的旋转角度（绕y轴）
    # rotate = False  # 标记是否开始旋转视角
    global angle_x,angle_y,rotate

    global eye_x,eye_y,eye_z

    global cur_pos_x,cur_pos_y,cur_pos_z
    
    
    key_states = {pg.K_LEFT: False, pg.K_RIGHT: False, pg.K_UP: False, pg.K_DOWN: False, pg.K_w: False, pg.K_s: False}

    while True:

        if cb.check_and_update() != -1:
            winner = cb.check_and_update()
            if winner == 0:
                winner_text = "white player win"
            elif winner == 1:
                winner_text = "black player win"
            else:
                winner_text = " draw."
            screen = pg.display.set_mode((200, 100))
            font = pg.font.Font(None, 36)
            text = font.render(winner_text, 1, (255, 255, 255))
            textpos = text.get_rect(centerx=100, centery=50)
            screen.blit(text, textpos)
            pg.display.flip()
            waiting_for_close = True
            while waiting_for_close:
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        waiting_for_close = False
                    running = False
            exit_event.set() 
            pg.quit()
            exit()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit_event.set()
                pg.quit()
                quit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:  # 按下鼠标左键开始旋转视角
                    rotate = True
                elif event.button == 3:  # 按下鼠标右键获取鼠标位置
                    mouse_x, mouse_y = pg.mouse.get_pos()  # Get x and y coordinates separately
                    cb.add_stone(cur_pos_x,cur_pos_y,cur_pos_z,eye_x,eye_y,eye_z-5,angle_x,angle_y)
                    # cb.add_stone(temp,0,0,0,0,0,angle_x,angle_y)

                elif event.button == 4:  # 鼠标滚轮向上滚动
                    eye_z -= 0.3
                elif event.button == 5:  # 鼠标滚轮向下滚动
                    eye_z += 0.3
            elif event.type == pg.MOUSEBUTTONUP:
                if event.button == 1:  # 松开鼠标左键停止旋转视角
                    rotate = False
            elif event.type == pg.MOUSEMOTION:
                if rotate:  # 当鼠标在移动时，根据鼠标的移动来改变视角的旋转角度
                    x, y = event.rel
                    angle_x += y  # 根据鼠标在y轴上的移动改变绕x轴的旋转角度
                    angle_y += x  # 根据鼠标在x轴上的移动改变绕y轴的旋转角度
                    if angle_x>90:
                        angle_x = 90
                    if angle_x<-90:
                        angle_x = -90
            elif event.type == pg.KEYDOWN:
                if event.key in key_states:
                    key_states[event.key] = True
            elif event.type == pg.KEYUP:
                if event.key in key_states:
                    key_states[event.key] = False
            
        
        if key_states[pg.K_LEFT]:  # 按下左箭头键，视角向左平移
            eye_x -= 0.1
        if key_states[pg.K_RIGHT]:  # 按下右箭头键，视角向右平移
            eye_x += 0.1
        if key_states[pg.K_UP]:  # 按下上箭头键，视角向上平移
            eye_y += 0.1
        if key_states[pg.K_DOWN]:  # 按下下箭头键，视角向下平移
            eye_y -= 0.1
        if key_states[pg.K_w]:  # 按下W键，视角向上移动
            eye_z -= 0.1
        if key_states[pg.K_s]:  # 按下S键，视角向下移动
            eye_z += 0.1

        cb.current_stone_pos(cur_pos_x,cur_pos_y,cur_pos_z,eye_x,eye_y,eye_z-5,angle_x,angle_y)

        glClearColor(0.8, 0.6, 0.4, 1.0)  # 设置背景颜色为灰色

        

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glEnable(GL_DEPTH_TEST)
        

        glPushMatrix()

        glPushMatrix()  
        glTranslatef(-eye_x, -eye_y, -eye_z)
        glRotatef(angle_x, 1, 0, 0)  
        glRotatef(angle_y, 0, 1, 0)
        cb.drawChessboard()
        # drawAxes()
        glPopMatrix()  
        # drawAxes()
        glPopMatrix()
        # drawAxes()
        pg.display.flip()
        pg.time.wait(10)


def gesture_func():

    global angle_x,angle_y,rotate

    global eye_x,eye_y,eye_z

    global cur_pos_x,cur_pos_y,cur_pos_z

    global cur_stone_pos_x,cur_stone_pos_y,cur_stone_pos_z

    hand_landmarks = [(0.1, 0.2, 0.3), (0.2, 0.3, 0.4)]


    gesture = ["none","one","two","three","four","five","six","seven","eight","nine","ten"]
    flag = 0
    last_flag = 0
    pos_x = 0
    pos_y = 0
    pos_z = 0

    # pos_z_arr = []
    queue_z = deque(maxlen=30)

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

    last_flag = -1

    while True:

        if exit_event.is_set():  # 检测是否收到结束信号
            break
        # angle_x += 1

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
                cur_z = np.mean([i.z for i in hand_landmarks.landmark])
                cur_y = np.mean([i.y for i in hand_landmarks.landmark])
                cur_x = np.mean([i.x for i in hand_landmarks.landmark])
                z_cor.append(cur_z)
                y_cor.append(cur_y)
                x_cor.append(cur_x)


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

            if last_flag == 2 and flag != 2:
                cb.add_stone(cur_pos_x,cur_pos_y,cur_pos_z,eye_x,eye_y,eye_z-5,angle_x,angle_y)
                
            
            
            
            if flag == 5:
                # print(flag)
                # print(last_flag)
                if last_flag != 5:
                    print(last_flag)
                    pos_x = cur_x
                    pos_y = cur_y
                    pos_z = cur_z
                    last_flag = 5
                    print('update'+str(last_flag))
                else:
                    print(cur_y - pos_y)
                    angle_x += (cur_y - pos_y)*500
                    angle_y += (cur_x - pos_x)*500
                    pos_x = cur_x
                    pos_y = cur_y
                    pos_z = cur_z
                    last_flag = 5
            
            if flag == 2:
                if last_flag != 2:
                    cur_hand_pos_x = cur_x
                    cur_hand_pos_y = cur_y
                    cur_hand_pos_z = cur_z
                    queue_z.clear()
                    cur_pos_x = 0
                    cur_pos_y = 0
                    cur_pos_z = 0
                    last_flag = 2
                else:
                    cur_pos_y += (cur_y - cur_hand_pos_y)*25
                    cur_pos_x += (cur_x - cur_hand_pos_x)*25
                    queue_z.append(cur_z - cur_hand_pos_z)
                    cur_pos_z += (sum(queue_z))*20
                    cur_hand_pos_x = cur_x
                    cur_hand_pos_y = cur_y
                    cur_hand_pos_z = cur_z
                    last_flag = 2

            if flag == 3:
                # print(flag)
                # print(last_flag)
                if last_flag != 3:
                    print(last_flag)
                    pos_x = cur_x
                    pos_y = cur_y
                    pos_z = cur_z
                    queue_z.clear()
                    last_flag = 3
                    print('update'+str(last_flag))
                else:
                    print(cur_y - pos_y)
                    eye_y += (cur_y - pos_y)*25
                    eye_x += (cur_x - pos_x)*25
                    queue_z.append(cur_z - pos_z)
                    eye_z += (sum(queue_z))*20
                    pos_x = cur_x
                    pos_y = cur_y
                    pos_z = cur_z
                    last_flag = 3


                # 关键点可视化
                mp_drawing.draw_landmarks(frame, 
                                        hand_landmarks, 
                                        mp_hands.HAND_CONNECTIONS)
                

            
        # cv2.putText(frame,gesture[flag],(50,50),0,1.3,(0,0,255),3)
        cv2.imshow('MediaPipe Hands', frame)
        # if cv2.waitKey(1) & 0xFF == 27:
        #     break
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    cap.release()
    cv2.destroyAllWindows()



if __name__ == "__main__":
    # game()
    # gesture_func()

    thread1 = threading.Thread(target=game)
    thread2 = threading.Thread(target=gesture_func)

    # 启动线程
    thread1.start()
    thread2.start()

    # 等待线程结束
    thread1.join()
    thread2.join()
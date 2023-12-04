from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import sys
import os

import math

# 将当前文件所在的目录添加到 Python 搜索路径中
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from draw_cube import draw_sphere,draw_sphere_with_light_default

import numpy as np


class Chessboard:
    size = 2

    black_or_white = 1 #1:black 0:white
    black = []

    points = []
    edges = []
    stone = []
    cur_pos = [0,0,0]

    def __init__(self,size=2):
        self.size = size
        self.points = [(x, y, z) for x in range(size) for y in range(size) for z in range(size)]
        self.black = [-1 for x in range(size) for y in range(size) for z in range(size)]

        # 生成所有边的坐标
        for x in range(self.size):
            for y in range(self.size):
                for z in range(self.size):
                    index = x + y * self.size + z * self.size*self.size  # 计算点在points列表中的索引
                    if x < size-1:
                        self.edges.append((index, index+1))
                    if y < size-1:
                        self.edges.append((index, index+size))
                    if z < size-1:
                        self.edges.append((index, index+size*size))
        
        print(self.points)
    
    
    def transform_coordinates(self,x, y, z, eye_x, eye_y, eye_z, angle_x, angle_y):
    # 平移变换
        x1 = x + eye_x
        y1 = y + eye_y
        z1 = z + eye_z

        # 绕x轴旋转
        x2 = x1
        y2 = y1 * math.cos(math.radians(-angle_x)) - z1 * math.sin(math.radians(-angle_x))
        z2 = y1 * math.sin(math.radians(-angle_x)) + z1 * math.cos(math.radians(-angle_x))

        # 绕y轴旋转
        x_new = x2 * math.cos(math.radians(-angle_y)) + z2 * math.sin(math.radians(-angle_y))
        z_new = -x2 * math.sin(math.radians(-angle_y)) + z2 * math.cos(math.radians(-angle_y))

        return x_new, y2, z_new

    
    def add_stone(self,x,y,z,eye_x,eye_y,eye_z,angle_x,angle_y):
        new_x, new_y, new_z = self.transform_coordinates(x,y,z,eye_x,eye_y,eye_z,angle_x,angle_y)
        new_x = new_x + (self.size-1)/2
        new_y = new_y + (self.size-1)/2
        new_z = new_z + (self.size-1)/2
        # 计算距离
        distances = [np.linalg.norm(np.array(vertex) - np.array([new_x, new_y, new_z])) for vertex in self.points]
        # print(distances)
        # 找到最近的点
        closest_point = self.points[np.argmin(distances)]

        # self.stone.append((new_x, new_y, new_z))
        if closest_point not in self.stone:
            self.stone.append(closest_point)
            # print(closest_point[0],closest_point[1],closest_point[2])
            matching_index = next((i for i, point in enumerate(self.points) if point == closest_point), None)
            self.black[matching_index] = self.black_or_white
            
            if self.black_or_white == 1:
                self.black_or_white = 0
            else:
                self.black_or_white = 1


        print(self.stone)

    
    def current_stone_pos(self,x,y,z,eye_x,eye_y,eye_z,angle_x,angle_y):
        new_x, new_y, new_z = self.transform_coordinates(x,y,z,eye_x,eye_y,eye_z,angle_x,angle_y)
        new_x = new_x + (self.size-1)/2
        new_y = new_y + (self.size-1)/2
        new_z = new_z + (self.size-1)/2
        # 计算距离
        distances = [np.linalg.norm(np.array(vertex) - np.array([new_x, new_y, new_z])) for vertex in self.points]
        closest_point = self.points[np.argmin(distances)]
        self.cur_pos = list(closest_point)

    def draw_current_pos(self):
        glPushMatrix()  # 保存当前的模型视图矩阵
        glTranslatef(self.cur_pos[0], self.cur_pos[1], self.cur_pos[2])  # 平移坐标系到指定位置
        glColor3f(1.0, 0.0, 0.0)
        draw_sphere(0.05, 20, 20) # 绘制小球，你需要实现这个函数来绘制小球
        glPopMatrix()  # 恢复之前保存的模型视图矩阵

    
    def all_stone(self):
        # for coord in self.stone:
        #     glPushMatrix()  # 保存当前的模型视图矩阵
        #     glTranslatef(coord[0], coord[1], coord[2])  # 平移坐标系到指定位置
            
        #     draw_sphere(0.3, 20, 20) # 绘制小球，你需要实现这个函数来绘制小球
        #     glPopMatrix()  # 恢复之前保存的模型视图矩阵

        for p in range(len(self.points)):
            if self.black[p] == -1:
                continue
            glPushMatrix()  # 保存当前的模型视图矩阵
            glPushAttrib(GL_CURRENT_BIT)
            glTranslatef(self.points[p][0], self.points[p][1], self.points[p][2])  # 平移坐标系到指定位置
            if self.black[p] == 1:
                glColor3f(0.5,0.5,0.5)
            if self.black[p] == 0:
                glColor3f(1,1,1)
            # draw_sphere(0.3, 20, 20) # 绘制小球，你需要实现这个函数来绘制小球
            draw_sphere_with_light_default(0.3,20,20,[self.points[p][0], self.points[p][1], self.points[p][2]])
            glPopMatrix()  # 恢复之前保存的模型视图矩阵
            glPopAttrib()


    def all_point(self):

        for p in range(len(self.points)):
            glPushMatrix()  
            glPushAttrib(GL_CURRENT_BIT)
            glTranslatef(self.points[p][0], self.points[p][1], self.points[p][2]) 
            draw_sphere(0.02, 20, 20)
            glPopMatrix()  
            glPopAttrib()

    
    def cb_wire(self):
        glBegin(GL_LINES)
        for cubeEdge in self.edges:
            for cubeVertex in cubeEdge:
                glVertex3fv(self.points[cubeVertex])
        glEnd()

    
    def drawChessboard(self):
        glLineWidth(0.2) 
        glColor3f(0.5, 0.5, 0.5)
        
        glPushMatrix()

        glTranslatef(-(self.size-1)/2,-(self.size-1)/2,-(self.size-1)/2)
        
        self.all_stone()
        self.all_point()
        self.cb_wire()
        self.draw_current_pos()
        
        glPopMatrix()
        
    
    def check_and_update(self):
        # 检查x轴方向
        for x in range(self.size - 4):
            for y in range(self.size):
                for z in range(self.size):
                    if all(self.black[(x+i)*self.size*self.size + y*self.size + z] == 1 for i in range(5)):
                        return 1  # 黑色获胜
                    elif all(self.black[(x+i)*self.size*self.size + y*self.size + z] == 0 for i in range(5)):
                        return 0  # 白色获胜

        # 检查y轴方向
        for x in range(self.size):
            for y in range(self.size - 4):
                for z in range(self.size):
                    if all(self.black[x*self.size*self.size + (y+i)*self.size + z] == 1 for i in range(5)):
                        return 1  # 黑色获胜
                    elif all(self.black[x*self.size*self.size + (y+i)*self.size + z] == 0 for i in range(5)):
                        return 0  # 白色获胜

        # 检查z轴方向
        for x in range(self.size - 4):
            for y in range(self.size):
                for z in range(self.size):
                    if all(self.black[(x)*self.size*self.size + y*self.size + z+i] == 1 for i in range(5)):
                        return 1  # 黑色获胜
                    elif all(self.black[(x)*self.size*self.size + y*self.size + z+i] == 0 for i in range(5)):
                        return 0  # 白色获胜

        # 检查斜向方向
        for x in range(self.size - 4):
            for y in range(self.size - 4):
                for z in range(self.size - 4):
                    if all(self.black[(x+i)*self.size*self.size + (y+i)*self.size + (z+i)] == 1 for i in range(5)):
                        return 1  # 黑色获胜
                    elif all(self.black[(x+i)*self.size*self.size + (y+i)*self.size + (z+i)] == 0 for i in range(5)):
                        return 0  # 白色获胜


        # 检查平面上的对角线方向
        for x in range(self.size - 4):
            for y in range(self.size - 4):
                for z in range(self.size - 4):
                    if all(self.black[(x+i)*self.size*self.size + (y+i)*self.size + (z+i)] == 1 for i in range(5)):
                        return 1  # 黑色获胜
                    elif all(self.black[(x+i)*self.size*self.size + (y+i)*self.size + (z+i)] == 0 for i in range(5)):
                        return 0  # 白色获胜

        # 检查平局
        if all(self.black[i] != -1 for i in range(self.size * self.size * self.size)):
            return 2  # 平局

        return -1  # 没有获胜者

    


def draw():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    glTranslatef(0.0, 0.0, -20.0)  # 将场景沿 z 轴负方向移动
    glRotatef(45, 1, 1, 0)  # 绕 x 轴和 y 轴旋转

    cb = Chessboard(3)
    cb.drawChessboard()

    glFlush()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(500, 500)
    glutCreateWindow(b"3D Cube Grid")

    glClearColor(1.0, 1.0, 1.0, 0.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 1, 0.1, 50)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(10, 10, 10, 0, 0, 0, 0, 1, 0)

    glEnable(GL_DEPTH_TEST)

    glutDisplayFunc(draw)
    glutMainLoop()



if __name__ == "__main__":
    main()
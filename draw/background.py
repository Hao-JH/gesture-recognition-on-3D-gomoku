import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys
import os
from PIL import Image
import math

# 将当前文件所在的目录添加到 Python 搜索路径中
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)


from axes import drawAxes

# 加载背景贴图


# 绘制背景贴图
def draw_background():
    background_texture = glGenTextures(1)
    background_image = Image.open('pic/background.jpg')
    background_image = background_image.transpose(Image.FLIP_TOP_BOTTOM)  # 翻转图片（因为OpenGL坐标系的原点在左下角）
    background_data = background_image.tobytes("raw", "RGBX", 0, -1)

    glBindTexture(GL_TEXTURE_2D, background_texture)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, background_image.width, background_image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, background_data)

    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, background_texture)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0)
    glVertex3f(-10.0, -10.0,0)
    glTexCoord2f(1, 0)
    glVertex3f(-10.0,10.0,0)
    glTexCoord2f(1, 1)
    glVertex3f(10.0, 10.0,0)
    glTexCoord2f(0, 1)
    glVertex3f(10.0, -10.0,0)
    glEnd()
    glDisable(GL_TEXTURE_2D)


def draw_cube():
    # 绘制一个彩色立方体
    glBegin(GL_QUADS)
    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(1.0, 1.0, -1.0)
    glVertex3f(-1.0, 1.0, -1.0)
    glVertex3f(-1.0, 1.0, 1.0)
    glVertex3f(1.0, 1.0, 1.0)

    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(1.0, -1.0, 1.0)
    glVertex3f(-1.0, -1.0, 1.0)
    glVertex3f(-1.0, -1.0, -1.0)
    glVertex3f(1.0, -1.0, -1.0)

    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(1.0, 1.0, 1.0)
    glVertex3f(-1.0, 1.0, 1.0)
    glVertex3f(-1.0, -1.0, 1.0)
    glVertex3f(1.0, -1.0, 1.0)

    glColor3f(1.0, 1.0, 0.0)
    glVertex3f(1.0, -1.0, -1.0)
    glVertex3f(-1.0, -1.0, -1.0)
    glVertex3f(-1.0, 1.0, -1.0)
    glVertex3f(1.0, 1.0, -1.0)

    glColor3f(0.0, 1.0, 1.0)
    glVertex3f(-1.0, 1.0, 1.0)
    glVertex3f(-1.0, 1.0, -1.0)
    glVertex3f(-1.0, -1.0, -1.0)
    glVertex3f(-1.0, -1.0, 1.0)

    glColor3f(1.0, 0.0, 1.0)
    glVertex3f(1.0, 1.0, -1.0)
    glVertex3f(1.0, 1.0, 1.0)
    glVertex3f(1.0, -1.0, 1.0)
    glVertex3f(1.0, -1.0, -1.0)
    glEnd()

def main():
    # 初始化Pygame
    pygame.init()
    display = (800, 600)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)


    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    x=0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # glRotatef(1, 3, 1, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        glPushMatrix()
        drawAxes()
        glPopMatrix()
        glPushMatrix()
        # glRotatef(45, 1, 1, 1)
        glTranslatef(0,0,1)
        draw_background()  # 渲染背景贴图
        glPopMatrix()
        glPushMatrix()
        glRotatef(x, 3, 1, 1)
        # draw_cube()  # 绘制立方体
        glPopMatrix()
        x +=1
        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == "__main__":
    main()
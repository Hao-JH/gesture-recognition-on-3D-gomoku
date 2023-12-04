from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

def wirePyramid():
    glLineWidth(1)  # 设置线宽为1
    glColor3f(0.0, 1.0, 1.0)  # 设置颜色为白色
    glBegin(GL_LINES)
    # 底面
    glVertex3f(-1, -1, -1)
    glVertex3f(1, -1, -1)

    glVertex3f(1, -1, -1)
    glVertex3f(1, 1, -1)

    glVertex3f(1, 1, -1)
    glVertex3f(-1, 1, -1)

    glVertex3f(-1, 1, -1)
    glVertex3f(-1, -1, -1)

    # 侧面
    glVertex3f(-1, -1, -1)
    glVertex3f(0, 0, 1)

    glVertex3f(1, -1, -1)
    glVertex3f(0, 0, 1)

    glVertex3f(1, 1, -1)
    glVertex3f(0, 0, 1)

    glVertex3f(-1, 1, -1)
    glVertex3f(0, 0, 1)
    glEnd()
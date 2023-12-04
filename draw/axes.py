from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

def drawAxes():
    glBegin(GL_LINES)
    # x轴为红色
    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(0, 0, 0)
    glVertex3f(5, 0, 0)
    # y轴为绿色
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0, 0, 0)
    glVertex3f(0, 5, 0)
    # z轴为蓝色
    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0, 0, 0)
    glVertex3f(0, 0, 5)
    glEnd()
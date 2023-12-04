from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np
from math import acos, sqrt, pi

mouseDown = False


rotation_matrix = np.identity(4)

xrot = 0.0
yrot = 0.0

real_xrot = 0.0
real_yrot = 0.0
real_zrot = 0.0

xdiff = 0.0
ydiff = 0.0

zoom = 1.0

movex = 0.0
movey = 0.0
movez = 0.0

# 绘制正方体
def drawBox():
    glBegin(GL_QUADS)

    glColor3f(1.0, 0.0, 0.0)
    # FRONT
    glVertex3f(-0.5, -0.5, 0.5)
    glVertex3f(0.5, -0.5, 0.5)
    glVertex3f(0.5, 0.5, 0.5)
    glVertex3f(-0.5, 0.5, 0.5)
    # BACK
    glVertex3f(-0.5, -0.5, -0.5)
    glVertex3f(-0.5, 0.5, -0.5)
    glVertex3f(0.5, 0.5, -0.5)
    glVertex3f(0.5, -0.5, -0.5)

    glColor3f(0.0, 1.0, 0.0)
    # LEFT
    glVertex3f(-0.5, -0.5, 0.5)
    glVertex3f(-0.5, 0.5, 0.5)
    glVertex3f(-0.5, 0.5, -0.5)
    glVertex3f(-0.5, -0.5, -0.5)
    # RIGHT
    glVertex3f(0.5, -0.5, -0.5)
    glVertex3f(0.5, 0.5, -0.5)
    glVertex3f(0.5, 0.5, 0.5)
    glVertex3f(0.5, -0.5, 0.5)

    glColor3f(0.0, 0.0, 1.0)
    # TOP
    glVertex3f(-0.5, 0.5, 0.5)
    glVertex3f(0.5, 0.5, 0.5)
    glVertex3f(0.5, 0.5, -0.5)
    glVertex3f(-0.5, 0.5, -0.5)
    # BOTTOM
    glVertex3f(-0.5, -0.5, 0.5)
    glVertex3f(-0.5, -0.5, -0.5)
    glVertex3f(0.5, -0.5, -0.5)
    glVertex3f(0.5, -0.5, 0.5)
    glEnd()

# 绘制函数
def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluLookAt(
        0.0, 0.0,3.0 * zoom,
        0.0 - movex, 0.0 + movey, 0.0,
        0.0, 1.0, 0.0)
    
    glRotatef(xrot, 1.0, 0.0, 0.0)
    glRotatef(yrot, 0.0, 1.0, 0.0)

    drawBox()

    glFlush()
    glutSwapBuffers()

def resize(w, h):
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    glViewport(0, 0, w, h)

    gluPerspective(45.0, 1.0 * w / h, 1.0, 100.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

# 鼠标事件
def mouse(button, state, x, y):
    global mouseDown, xdiff, ydiff
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        mouseDown = True
        xdiff = x - yrot
        ydiff = -y + xrot
        print("xdiff:", xdiff, "\tydiff:", ydiff)
    else:
        mouseDown = False

# 鼠标移动事件
def mouseMotion(x, y):
    global xrot, yrot,real_xrot,real_yrot,real_zrot,rotation_matrix
    if mouseDown:
        yrot = x - xdiff
        xrot = y + ydiff
        if xrot<-90:
            xrot = -90
        elif xrot>90:
            xrot = 90
        print("yrot:", yrot, "\txrot:", xrot)
        
        glutPostRedisplay()

# 键盘事件
def keyboard(key, x, y):
    global zoom
    if key == b'\x1b':
        sys.exit(0)
    elif key == b' ':
        zoom = 1.0
    elif key == b'\r':
        xrot = 0.0
        yrot = 0.0
        zoom = 1.0
    elif key == b's':
        zoom += 0.01
    elif key == b'w':
        zoom -= 0.01
        if zoom < 0.1:
            zoom = 0.1
    print(zoom)
    glutPostRedisplay()

def specialFunc(key, x, y):
    global movey,movex
    if key == GLUT_KEY_UP:
        movey += 0.1
    elif key == GLUT_KEY_DOWN:
        movey -= 0.1
    elif key == GLUT_KEY_LEFT:
        movex +=0.1
    elif key == GLUT_KEY_RIGHT:
        movex -=0.1
    glutPostRedisplay()

if __name__ == "__main__":
    glutInit()
    glutInitWindowPosition(50, 50)
    glutInitWindowSize(500, 500)
    glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE)
    glutCreateWindow("demo")
    glutDisplayFunc(display)
    glutMouseFunc(mouse)
    glutMotionFunc(mouseMotion)
    glutReshapeFunc(resize)
    glutKeyboardFunc(keyboard)
    glutSpecialFunc(specialFunc)

    glClearColor(0.93, 0.93, 0.93, 0.0)

    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)
    glClearDepth(1.0)

    glutMainLoop()


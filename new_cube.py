from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys

mouseDown = False
xrot = 0.0
yrot = 0.0
xdiff = 0.0
ydiff = 0.0

def drawBox():
    glBegin(GL_QUADS)
    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(-0.5, -0.5, 0.5)
    glVertex3f(0.5, -0.5, 0.5)
    glVertex3f(0.5, 0.5, 0.5)
    glVertex3f(-0.5, 0.5, 0.5)

    # ... Define other vertices and colors for the box ...

    glEnd()

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    gluLookAt(0.0, 0.0, 3.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
    glRotatef(xrot, 1.0, 0.0, 0.0)
    glRotatef(yrot, 0.0, 1.0, 0.0)
    drawBox()
    glutSwapBuffers()

def resize(w, h):
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glViewport(0, 0, w, h)
    gluPerspective(45.0, 1.0 * w / h, 1.0, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def mouse(button, state, x, y):
    global mouseDown, xdiff, ydiff, xrot, yrot
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        mouseDown = True
        xdiff = x - yrot
        ydiff = -y + xrot
    else:
        mouseDown = False

def mouseMotion(x, y):
    global xrot, yrot
    if mouseDown:
        yrot = x - xdiff
        xrot = y + ydiff
        glutPostRedisplay()

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE)
    glutInitWindowSize(500, 500)
    glutCreateWindow(b"OpenGL in PyOpenGL")

    glutDisplayFunc(display)
    glutReshapeFunc(resize)
    glutMouseFunc(mouse)
    glutMotionFunc(mouseMotion)

    glClearColor(0.93, 0.93, 0.93, 1.0)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)
    glClearDepth(1.0)

    glutMainLoop()

if __name__ == "__main__":
    main()
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

cubeVertices = ((1, 1, 1), (1, 1, -1), (1, -1, -1), (1, -1, 1), (-1, 1, 1), (-1, -1, -1), (-1, -1, 1), (-1, 1, -1))
cubeEdges = ((0, 1), (0, 3), (0, 4), (1, 2), (1, 7), (2, 5), (2, 3), (3, 6), (4, 6), (4, 7), (5, 6), (5, 7))
cubeQuads = ((0, 3, 6, 4), (2, 5, 6, 3), (1, 2, 5, 7), (1, 0, 4, 7), (7, 4, 6, 5), (2, 3, 0, 1))

def wireCube():
    glBegin(GL_LINES)
    for cubeEdge in cubeEdges:
        for cubeVertex in cubeEdge:
            glVertex3fv(cubeVertices[cubeVertex])
    glEnd()

def solidCube():
    glBegin(GL_QUADS)
    for cubeQuad in cubeQuads:
        for cubeVertex in cubeQuad:
            glVertex3fv(cubeVertices[cubeVertex])
    glEnd()

def drawCubeGrid(size = 2):
    glLineWidth(0.2)  # 设置线宽为1
    glColor3f(0.5, 0.5, 0.5)
    for x in range(size):
        for y in range(size):
            for z in range(size):
                glPushMatrix()
                glTranslatef(x * 2 - size+1, y * 2 - size+1, -z * 2 + size-1)  # 根据网格位置进行平移，每个立方体之间间隔为2
                wireCube()
                glPopMatrix()

def draw_sphere():
    quadric = gluNewQuadric()
    gluQuadricNormals(quadric, GLU_SMOOTH)
    gluQuadricTexture(quadric, GL_TRUE)
    gluSphere(quadric, 1, 30, 30)
    gluDeleteQuadric(quadric)

def draw_sphere(radius, slices, stacks):
    quadric = gluNewQuadric()
    gluQuadricTexture(quadric, GL_TRUE)
    gluSphere(quadric, radius, slices, stacks)
    gluDeleteQuadric(quadric)



def draw_sphere_with_light_default(radius, slices, stacks, position):
    color = [1.0, 0.0, 0.0, 1.0]
    light_ambient = [0.2, 0.2, 0.2, 1.0]  # 光源的环境光颜色
    light_diffuse = [1.0, 1.0, 1.0, 1.0]  # 光源的漫反射颜色
    light_specular = [1.0, 0.0, 0.0, 1.0]
    draw_sphere_with_light(radius, slices, stacks, color, position, light_ambient, light_diffuse, light_specular)


def draw_sphere_with_light(radius, slices, stacks, color, position, light_ambient, light_diffuse , light_specular):
    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)  
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)  
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
    glLightfv(GL_LIGHT0, GL_POSITION, position)  

    glEnable(GL_COLOR_MATERIAL)  
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)  
    # glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, color)  
    # glMaterialf(GL_FRONT, GL_SHININESS, 50.0)

    glMaterialfv(GL_FRONT, GL_DIFFUSE, color)
    glMaterialfv(GL_FRONT, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])  
    glMaterialf(GL_FRONT, GL_SHININESS, 50.0)

    glEnable(GL_LIGHTING)  
    glEnable(GL_LIGHT0)  

    quadric = gluNewQuadric()
    gluQuadricTexture(quadric, GL_TRUE)
    glPushMatrix()
    # glTranslatef(position[0], position[1], position[2])
    gluSphere(quadric, radius, slices, stacks)
    glPopMatrix()
    gluDeleteQuadric(quadric)

    glDisable(GL_COLOR_MATERIAL)  
    glDisable(GL_LIGHTING) 


def draw_material_sphere():
    quadric = gluNewQuadric()
    gluQuadricNormals(quadric, GLU_SMOOTH)
    gluQuadricTexture(quadric, GL_TRUE)
    
    # 设置轻微漫反射效果
    ambient = [0.2, 0.2, 0.2, 1.0]
    glMaterialfv(GL_FRONT, GL_AMBIENT, ambient)
    
    gluSphere(quadric, 1, 30, 30)
    gluDeleteQuadric(quadric)


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

def draw():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    glTranslatef(0.0, 0.0, -20.0)  # 将场景沿 z 轴负方向移动
    glRotatef(45, 1, 1, 0)  # 绕 x 轴和 y 轴旋转

    drawCubeGrid()

    glFlush()

if __name__ == "__main__":
    main()
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

def draw_sphere_with_light(radius, slices, stacks, color, position, light_ambient, light_diffuse):
    glEnable(GL_LIGHTING)  # 启用光照
    glEnable(GL_LIGHT0)  # 启用光源0
    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)  # 设置光源0的环境光属性
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)  # 设置光源0的漫反射光属性
    glLightfv(GL_LIGHT0, GL_POSITION, position)  # 设置光源0的位置

    glEnable(GL_COLOR_MATERIAL)  # 启用颜色材质
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)  # 设置颜色材质属性

    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, color)  # 设置球体的漫反射颜色

    quadric = gluNewQuadric()
    gluQuadricTexture(quadric, GL_TRUE)
    glPushMatrix()
    glTranslatef(position[0], position[1], position[2])
    gluSphere(quadric, radius, slices, stacks)
    glPopMatrix()
    gluDeleteQuadric(quadric)

    glDisable(GL_COLOR_MATERIAL)  # 关闭颜色材质
    glDisable(GL_LIGHTING)  # 关闭光照

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)

    light_ambient = [0.2, 0.2, 0.2, 1.0]  # 光源的环境光颜色
    light_diffuse = [1.0, 1.0, 1.0, 1.0]  # 光源的漫反射颜色

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glRotatef(1, 3, 1, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        draw_sphere_with_light(1, 30, 30, [1.0, 0.0, 0.0, 1.0], [0, 0, 0], light_ambient, light_diffuse)
        draw_sphere_with_light(0.5, 20, 20, [1.0, 0.0, 0.0, 1.0], [1, 1, 1], light_ambient, light_diffuse)
        draw_sphere_with_light(0.7, 25, 25, [1.0, 0.0, 0.0, 1.0], [-1, -1, -1], light_ambient, light_diffuse)

        pygame.display.flip()
        pygame.time.wait(10)

main()
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

# Глобальная переменная для задания точности цилиндра
accurance = 10

# Функция для создания круга вершин
def get_circle(r, segments, height):
    # Возвращает круг вершин с радиусом r, количеством сегментов segments и высотой height
    return [[r * np.cos(2 * np.pi * i / segments), height, r * np.sin(2 * np.pi * i / segments)] for i in range(segments)]

# Функция для генерации вершин цилиндра
def generate_cylinder_vertices(h, r, n_segments):
    # Генерирует вершины для цилиндра с высотой h, радиусом r и количеством сегментов n_segments
    vertices = []
    for i in range(2):  # Два круга: верхний и нижний
        y = h * (i % 2)  # 0 для нижнего круга, h для верхнего
        vertices += get_circle(r, n_segments, y)
    return np.array(vertices)

# Функция для генерации граней цилиндра
def generate_cylinder_faces(n_segments):
    # Генерирует грани для цилиндра на основе количества сегментов
    faces = []
    for i in range(n_segments):
        current_bottom = i
        current_top = i + n_segments
        next_bottom = (i + 1) % n_segments
        next_top = (i + 1) % n_segments + n_segments

        # Боковые стороны
        faces.append([current_bottom, next_bottom, next_top])
        faces.append([current_bottom, next_top, current_top])
    return np.array(faces)

# Функция для расчета нормалей
def calculate_normals(vertices, faces):
    # Вычисляет нормали для каждой грани, используя вершины
    norms = []
    for face in faces:
        v1 = np.array(vertices[face[0]]) - np.array(vertices[face[1]])
        v2 = np.array(vertices[face[0]]) - np.array(vertices[face[2]])
        norm = np.cross(v1, v2)
        if np.linalg.norm(norm) != 0:
            norm = norm / np.linalg.norm(norm)
        norms.append(norm)
    return np.array(norms)

def draw(verts, faces, norms):
    # Рисует цилиндр с заданными вершинами, гранями и нормалями
    glBegin(GL_TRIANGLES)
    for i, face in enumerate(faces):
        glNormal3fv(norms[i])
        for vertex in face:
            glVertex3fv(verts[vertex])
    glEnd()

def main():
    global accurance

    pygame.init()
    display = (1280, 780)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    # Настройка освещения
    glEnable(GL_LIGHTING)
    reflect_lvl = 0.0
    glLightfv(GL_LIGHT0, GL_POSITION, [0.5, 5, -10, 1])
    glLightfv(GL_LIGHT0, GL_AMBIENT, [reflect_lvl, reflect_lvl, reflect_lvl, 1])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [1, 0.3, 0.6, reflect_lvl])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [reflect_lvl]*4)
    glEnable(GL_LIGHT0)

    # Настройка материала
    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, [1.0, 1.0, 1.0, reflect_lvl])
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [1.0, 1.0, 1.0, reflect_lvl])
    glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, [50])

    glEnable(GL_DEPTH_TEST)

    # Настройка матрицы проекции
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, -1.65, -5)

    # Параметры цилиндра
    r = 1  # Радиус
    h = 2  # Высота
    n_segments = accurance

    # Генерация цилиндра
    vertices = generate_cylinder_vertices(h, r, n_segments)
    faces = generate_cylinder_faces(n_segments)
    norms = calculate_normals(vertices, faces)

    draging = False
    last_m = [0, 0]

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:            
                    draging = True
                    last_m = event.pos

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:            
                    draging = False

            elif event.type == pygame.MOUSEMOTION:
                if draging:
                    mouse_x, mouse_y = event.pos
                    rot = np.array([0, 0])
                    rot[0] = last_m[0] - mouse_x
                    last_m = [mouse_x, mouse_y]
                    glRotatef(-360 * (rot[0]/display[0]), 0, 1, 0)

            # Управление точностью и отражающей способностью
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and accurance < 35:
                    accurance += 2
                    vertices = generate_cylinder_vertices(h, r, accurance)
                    faces = generate_cylinder_faces(accurance)
                    norms = calculate_normals(vertices, faces)

                elif event.key == pygame.K_DOWN and accurance > 4:
                    accurance -= 2
                    vertices = generate_cylinder_vertices(h, r, accurance)
                    faces = generate_cylinder_faces(accurance)
                    norms = calculate_normals(vertices, faces)

                elif event.key == pygame.K_LEFT and reflect_lvl > 0.1:
                    reflect_lvl -= 0.1
                    glLightfv(GL_LIGHT0, GL_AMBIENT, [reflect_lvl, reflect_lvl, reflect_lvl, 1])
                    glLightfv(GL_LIGHT0, GL_DIFFUSE, [1, 0.3, 0.6, reflect_lvl])
                    glLightfv(GL_LIGHT0, GL_SPECULAR, [reflect_lvl, reflect_lvl, reflect_lvl, reflect_lvl])
                    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, [1.0, 1.0, 1.0, reflect_lvl])
                    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [1.0, 1.0, 1.0, reflect_lvl])
                    
                elif event.key == pygame.K_RIGHT and reflect_lvl < 0.5:
                    reflect_lvl += 0.1
                    glLightfv(GL_LIGHT0, GL_AMBIENT, [reflect_lvl, reflect_lvl, reflect_lvl, 1])
                    glLightfv(GL_LIGHT0, GL_DIFFUSE, [1, 0.3, 0.6, reflect_lvl])
                    glLightfv(GL_LIGHT0, GL_SPECULAR, [reflect_lvl]*4)
                    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, [1.0, 1.0, 1.0, reflect_lvl])
                    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [1.0, 1.0, 1.0, reflect_lvl])

        keypress = pygame.key.get_pressed()
        if keypress[pygame.K_w]:
            glTranslatef(0, 0.1, 0.0)
        if keypress[pygame.K_s]:
            glTranslatef(0, -0.1, 0.0)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        draw(vertices, faces, norms)
        
        pygame.display.flip()
        pygame.time.wait(40)

    pygame.quit()

if __name__ == "__main__":
    main()

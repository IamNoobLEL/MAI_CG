import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# Золотое сечение
phi = (1 + np.sqrt(5)) / 2

# Вершины додекаэдра
vertices = np.array([
    [1, 1, -1],
    [phi, 0, -1 / phi],
    [1, -1, -1],
    [0, -1/phi, -phi],
    [0, 1/phi, -phi],
    [1, 1, 1],
    [1, -1, 1],
    [-1, -1, -1],
    [-1, -1, 1],
    [-1, 1, -1],
    [-1, 1, 1],
    [0, 1/phi, phi],
    [0, -1/phi, phi],
    [1/phi, phi, 0],
    [1/phi, -phi, 0],
    [-1/phi, phi, 0],
    [-1/phi, -phi, 0],
    [phi, 0, 1/phi],
    [-phi, 0, 1/phi],
    [-phi, 0, -1/phi]
])

# Грани додекаэдра
faces = np.array([
    [0, 1, 2, 3, 4],
    [3, 4, 9, 19, 7],
    [3, 2, 14, 16, 7],
    [0, 4, 9, 15, 13],
    [15, 13, 5, 11, 10],
    [11, 10, 18, 8, 12],
    [18, 8, 16, 7, 19],
    [18, 19, 9, 15, 10],
    [14, 16, 8, 12, 6],
    [12, 6, 17, 5, 11],
    [6, 17, 1, 2, 14],
    [17, 1, 0, 13, 5]
])

def rotation_matrix(alpha, beta, gamma):
    """
    Создает матрицу вращения для заданных углов Эйлера: alpha, beta, gamma.
    Углы задаются в радианах.
    """
    # Вращение вокруг оси X
    Rx = np.array([
        [1, 0, 0],
        [0, np.cos(alpha), -np.sin(alpha)],
        [0, np.sin(alpha), np.cos(alpha)]
    ])

    # Вращение вокруг оси Y
    Ry = np.array([
        [np.cos(beta), 0, np.sin(beta)],
        [0, 1, 0],
        [-np.sin(beta), 0, np.cos(beta)]
    ])

    # Вращение вокруг оси Z
    Rz = np.array([
        [np.cos(gamma), -np.sin(gamma), 0],
        [np.sin(gamma), np.cos(gamma), 0],
        [0, 0, 1]
    ])

    # Общая матрица вращения
    return Rz @ Ry @ Rx

def scale_vertices(vertices, scale):
    """
    Масштабирует вершины на заданный коэффициент.
    """
    return vertices * scale

def draw_dodecahedron_3d(vertices, faces):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Рисуем линии для каждой грани
    for face in faces:
        face_vertices = np.array([vertices[index] for index in face])
        # Добавляем первую вершину в конец, чтобы замкнуть грань
        face_vertices = np.append(face_vertices, [face_vertices[0]], axis=0)
        ax.plot(face_vertices[:, 0], face_vertices[:, 1], face_vertices[:, 2], color='k')

    # Настройка параметров отображения
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_xlim([-2, 2])
    ax.set_ylim([-2, 2])
    ax.set_zlim([-2, 2])
    ax.set_title('3D Dodecahedron')

    plt.show()

def calculate_face_depth(vertices, face):
    """
    Вычисляет среднюю глубину (z-координату) для грани.
    """
    return np.mean([vertices[index][2] for index in face])

def draw_dodecahedron_3d_with_culling(vertices, faces):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Сортировка граней по средней глубине
    faces_sorted = sorted(faces, key=lambda face: calculate_face_depth(vertices, face), reverse=True)

    # Рисуем грани в порядке от самых дальних до самых ближних
    for face in faces_sorted:
        polygon = [vertices[index] for index in face]
        poly3d = [[vertices[index] for index in face]]
        ax.add_collection3d(Poly3DCollection(poly3d, facecolors='cyan', linewidths=1, edgecolors='r', alpha=.25))

    # Настройка параметров отображения
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_xlim([-2, 2])
    ax.set_ylim([-2, 2])
    ax.set_zlim([-2, 2])
    ax.set_title('3D Dodecahedron with Culling')

    plt.show()

def orthographic_projection(vertices):
    """
    Производит ортографическую проекцию вершин, отбрасывая z-координату.
    """
    return vertices[:, :2]

def isometric_projection(vertices):
    """
    Производит изометрическую проекцию вершин.
    """
    # Вращаем вокруг оси X и Z для получения изометрической проекции
    alpha = np.arctan(1/np.sqrt(2))  # Примерно 35.264 градусов
    gamma = np.radians(45)  # 45 градусов
    rotated_vertices = vertices @ rotation_matrix(alpha, 0, gamma)
    # Применяем ортографическую проекцию
    return orthographic_projection(rotated_vertices)

def draw_2d_projection(vertices, faces, title='Projection'):
    """
    Рисует 2D проекцию додекаэдра.
    """
    fig, ax = plt.subplots()
    
    # Рисуем линии для каждой грани
    for face in faces:
        face_vertices = np.array([vertices[index] for index in face])
        # Добавляем первую вершину в конец, чтобы замкнуть грань
        face_vertices = np.append(face_vertices, [face_vertices[0]], axis=0)
        ax.plot(face_vertices[:, 0], face_vertices[:, 1], color='k')

    # Настройка параметров отображения
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_aspect('equal')
    ax.set_title(title)

    plt.show()

# Пример использования функций вращения и масштабирования
rotated_vertices = vertices @ rotation_matrix(np.radians(30), np.radians(30), np.radians(30))
scaled_vertices = scale_vertices(rotated_vertices, 1.5)

scale_factor = 1.0

def redraw_figure(scale):
    plt.clf()  # Очищаем текущую фигуру
    scaled_vertices = scale_vertices(vertices, scale)
    draw_dodecahedron_3d_with_culling(scaled_vertices, faces)
    plt.draw()

def on_key(event):
    global scale_factor
    if event.key == '+':
        scale_factor *= 1.1  # Увеличиваем масштаб
    elif event.key == '-':
        scale_factor /= 1.1  # Уменьшаем масштаб
    redraw_figure(scale_factor)

#база
draw_dodecahedron_3d(scaled_vertices, faces)

# Рисуем додекаэдр в 3D с удалением невидимых линий
draw_dodecahedron_3d_with_culling(vertices, faces)

# Рисуем ортографическую проекцию
orthographic_vertices = orthographic_projection(vertices)
draw_2d_projection(orthographic_vertices, faces, title='Orthographic Projection')

# Рисуем изометрическую проекцию
isometric_vertices = isometric_projection(vertices)
draw_2d_projection(isometric_vertices, faces, title='Isometric Projection')

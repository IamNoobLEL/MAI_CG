import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.colors import LightSource

# Функция для создания круга вершин с заданным радиусом и количеством сегментов
def get_circle(r, segments, height):
    return [[r * np.cos(2 * np.pi * i / segments), r * np.sin(2 * np.pi * i / segments), height] for i in range(segments + 1)]

# Функция для создания вершин цилиндра с использованием круглых слоев
def generate_cylinder_vertices(h, r, n_segments):
    vertices = []
    for i in range(n_segments + 1):
        z = h * i / n_segments
        vertices += get_circle(r, n_segments, z)
    return np.array(vertices)

# Функция для создания граней цилиндра
def generate_cylinder_faces(n_segments):
    faces = []
    for i in range(n_segments):
        for j in range(n_segments):
            current = i * (n_segments + 1) + j
            next = current + (n_segments + 1)
            faces += [
                [current, current + 1, next],
                [current + 1, next + 1, next]
            ]
    return faces

# Функция для рисования барреля с использованием освещения от LightSource
def draw_barrel(vertices, faces, ax, light_azimuth, light_altitude):
    ax.clear()
    ls = LightSource(azdeg=light_azimuth, altdeg=light_altitude)
    shaded = np.zeros((len(faces), 3))
    for i, face in enumerate(faces):
        normals = np.cross(vertices[face[1]] - vertices[face[0]],
                           vertices[face[2]] - vertices[face[0]])
        normals /= np.linalg.norm(normals)
        shaded[i] = ls.shade_normals(normals)
    collection = Poly3DCollection(vertices[faces], facecolors=shaded, linewidths=0.5, edgecolors=(0, 0, 0, 0.3))
    ax.add_collection3d(collection)
    ax.auto_scale_xyz([-r, r], [-r, r], [0, h])
    plt.draw()

# Обновление визуализации барреля на основе ползунков
def update(val):
    global n_segments, light_azimuth, light_altitude
    n_segments = int(slider_segments.val)
    light_azimuth = slider_light.val
    light_altitude = 90 - abs(slider_light.val - 180)  # Корректировка высоты освещения на основе азимута
    vertices = generate_cylinder_vertices(h, r, n_segments)
    faces = generate_cylinder_faces(n_segments)
    draw_barrel(vertices, faces, ax, light_azimuth, light_altitude)

# Параметры барреля
h, r = 15, 3  # Высота и радиус цилиндрического барреля

# Начальные параметры источника света
light_azimuth = 45
light_altitude = 30

# Настройка графика
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Начальное количество сегментов
n_segments = 20

# Ползунок для количества сегментов
ax_slider_segments = plt.axes([0.25, 0.01, 0.65, 0.03], facecolor='lightgoldenrodyellow')
slider_segments = Slider(ax_slider_segments, 'Сегменты', 4, 40, valinit=n_segments, valstep=1)
slider_segments.on_changed(update)

# Объединенный ползунок для азимута и высоты освещения
ax_slider_light = plt.axes([0.25, 0.05, 0.65, 0.03], facecolor='lightgoldenrodyellow')
slider_light = Slider(ax_slider_light, 'Азимут и высота освещения', 0, 360, valinit=light_azimuth, valstep=1)
slider_light.on_changed(update)

# Начальная отрисовка
update(0)

plt.show()

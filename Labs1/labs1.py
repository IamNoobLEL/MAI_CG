import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider


fig, ax = plt.subplots(figsize=(7, 7), subplot_kw={'projection': 'polar'})
plt.subplots_adjust(left=0.1, bottom=0.25)


a_init = 1.0
phi = np.linspace(0, 2*np.pi, 1000)
rho = a_init * np.sin(6 * phi)


line, = ax.plot(phi, rho)


ax.set_rorigin(0)
ax.set_rlim(0, max(abs(rho)) + 0.5)


ax.grid(True, color='black', linestyle='-', linewidth=0.5)
ax.spines['polar'].set_visible(True)
ax.spines['polar'].set_linewidth(2)


rmax = max(abs(rho)) + 0.5
ax.annotate("", xy=(0, rmax), xytext=(0, rmax - 0.5), 
            arrowprops=dict(arrowstyle="->", color="k"))
ax.annotate("", xy=(np.pi/2, rmax), xytext=(np.pi/2, rmax - 0.5), 
            arrowprops=dict(arrowstyle="->", color="k"))


ax_slider = plt.axes([0.1, 0.1, 0.65, 0.03], facecolor='lightgoldenrodyellow')
slider = Slider(ax_slider, 'a', -10.0, 10.0, valinit=a_init)


def update(val):
    a = slider.val
    rho_new = a * np.sin(6 * phi)
    line.set_ydata(rho_new)
    
    
    ax.set_rlim(0, max(abs(rho_new)) + 0.5)
    fig.canvas.draw_idle()

slider.on_changed(update)

plt.show()

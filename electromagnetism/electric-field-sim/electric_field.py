
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.widgets import Slider, Button
from matplotlib.patches import Circle
 
# --- Grid setup ---
GRID_N = 80
grid_range = 3.0
x, y = np.meshgrid(np.linspace(-grid_range, grid_range, GRID_N),
                   np.linspace(-grid_range, grid_range, GRID_N))
 
# --- Initial charge config ---
# Each charge: [x, y, magnitude]
charges = [
    [-1.0,  0.0,  1.0],
    [ 1.0,  0.0, -1.0],
]
 
probe_point = [0.0, 0.0]  # where we measure field strength
 
def compute_field(charges):
    Ex, Ey = np.zeros_like(x), np.zeros_like(y)
    for cx, cy, q in charges:
        dx, dy = x - cx, y - cy
        r = np.sqrt(dx**2 + dy**2)
        r = np.maximum(r, 0.05)
        Ex += q * dx / r**3
        Ey += q * dy / r**3
    return Ex, Ey
 
def field_at_point(charges, px, py):
    Ex, Ey = 0.0, 0.0
    for cx, cy, q in charges:
        dx, dy = px - cx, py - cy
        r = np.sqrt(dx**2 + dy**2)
        r = max(r, 0.05)
        Ex += q * dx / r**3
        Ey += q * dy / r**3
    return Ex, Ey
 
# --- Figure layout ---
fig = plt.figure(figsize=(14, 9), facecolor='#0d0d1a')
fig.suptitle('⚡ Interactive Electric Field Simulator', 
             color='#e0e0ff', fontsize=15, fontweight='bold', y=0.98)
 
gs = gridspec.GridSpec(2, 2, figure=fig, 
                        left=0.05, right=0.95,
                        top=0.93, bottom=0.32,
                        wspace=0.3, hspace=0.4)
 
ax_main = fig.add_subplot(gs[:, 0])   # main field plot (spans both rows)
ax_info = fig.add_subplot(gs[0, 1])   # field strength info
ax_vec  = fig.add_subplot(gs[1, 1])   # vector arrow at probe
 
for ax in [ax_main, ax_info, ax_vec]:
    ax.set_facecolor('#0d0d1a')
 
# --- Sliders area ---
slider_color = '#1a1a3a'
label_color  = '#a0a0dd'
 
# Charge 1 sliders
ax_c1x = fig.add_axes([0.05, 0.22, 0.25, 0.025]); ax_c1x.set_facecolor(slider_color)
ax_c1y = fig.add_axes([0.05, 0.17, 0.25, 0.025]); ax_c1y.set_facecolor(slider_color)
ax_c1q = fig.add_axes([0.05, 0.12, 0.25, 0.025]); ax_c1q.set_facecolor(slider_color)
 
# Charge 2 sliders
ax_c2x = fig.add_axes([0.38, 0.22, 0.25, 0.025]); ax_c2x.set_facecolor(slider_color)
ax_c2y = fig.add_axes([0.38, 0.17, 0.25, 0.025]); ax_c2y.set_facecolor(slider_color)
ax_c2q = fig.add_axes([0.38, 0.12, 0.25, 0.025]); ax_c2q.set_facecolor(slider_color)
 
# Probe sliders
ax_px  = fig.add_axes([0.71, 0.22, 0.25, 0.025]); ax_px.set_facecolor(slider_color)
ax_py  = fig.add_axes([0.71, 0.17, 0.25, 0.025]); ax_py.set_facecolor(slider_color)
 
# Reset button
ax_btn = fig.add_axes([0.45, 0.05, 0.10, 0.04])
 
kw = dict(color='#7070cc', track_color='#2a2a4a')
 
s_c1x = Slider(ax_c1x, 'Q1  x', -2.5, 2.5, valinit=charges[0][0], **kw)
s_c1y = Slider(ax_c1y, 'Q1  y', -2.5, 2.5, valinit=charges[0][1], **kw)
s_c1q = Slider(ax_c1q, 'Q1  q', -3.0, 3.0, valinit=charges[0][2], **kw)
 
s_c2x = Slider(ax_c2x, 'Q2  x', -2.5, 2.5, valinit=charges[1][0], **kw)
s_c2y = Slider(ax_c2y, 'Q2  y', -2.5, 2.5, valinit=charges[1][1], **kw)
s_c2q = Slider(ax_c2q, 'Q2  q', -3.0, 3.0, valinit=charges[1][2], **kw)
 
s_px  = Slider(ax_px,  'Probe x', -2.5, 2.5, valinit=probe_point[0], **kw)
s_py  = Slider(ax_py,  'Probe y', -2.5, 2.5, valinit=probe_point[1], **kw)
 
# Label the slider sections
for ax_label, text, xpos in [
    (fig, 'CHARGE 1', 0.115),
    (fig, 'CHARGE 2', 0.445),
    (fig, 'PROBE POINT', 0.765),
]:
    ax_label.text(xpos, 0.265, text, transform=fig.transFigure,
                  color='#7070cc', fontsize=9, fontweight='bold', ha='center')
 
for ax_s in [ax_c1x, ax_c1y, ax_c1q, ax_c2x, ax_c2y, ax_c2q, ax_px, ax_py]:
    ax_s.tick_params(colors=label_color, labelsize=7)
    ax_s.xaxis.label.set_color(label_color)
 
btn_reset = Button(ax_btn, 'Reset', color='#2a2a5a', hovercolor='#4a4a8a')
btn_reset.label.set_color('#e0e0ff')
 
# --- Draw function ---
stream_obj = [None]
probe_dot  = [None]
info_text  = [None]
arrow_obj  = [None]
 
def draw(val=None):
    charges[0] = [s_c1x.val, s_c1y.val, s_c1q.val]
    charges[1] = [s_c2x.val, s_c2y.val, s_c2q.val]
    probe_point[0] = s_px.val
    probe_point[1] = s_py.val
 
    Ex, Ey = compute_field(charges)
    magnitude = np.sqrt(Ex**2 + Ey**2)
    log_mag = np.log1p(magnitude)
 
    ax_main.cla()
    ax_main.set_facecolor('#0d0d1a')
    ax_main.streamplot(x, y, Ex, Ey,
                       color=log_mag, cmap='plasma',
                       density=2.0, linewidth=0.8, arrowsize=1.2)
 
    for i, (cx, cy, q) in enumerate(charges):
        color  = '#ff4444' if q >= 0 else '#4488ff'
        label  = f'+{q:.1f}' if q >= 0 else f'{q:.1f}'
        circle = Circle((cx, cy), 0.12, color=color, zorder=5)
        ax_main.add_patch(circle)
        ax_main.text(cx, cy + 0.22, label, color=color,
                     ha='center', fontsize=9, fontweight='bold', zorder=6)
 
    # Probe point
    px, py = probe_point
    ax_main.plot(px, py, 'X', color='#00ffaa', markersize=10, zorder=7)
    ax_main.text(px + 0.1, py + 0.2, 'probe', color='#00ffaa', fontsize=8, zorder=8)
 
    ax_main.set_xlim(-grid_range, grid_range)
    ax_main.set_ylim(-grid_range, grid_range)
    ax_main.set_title('Electric Field Lines', color='#e0e0ff', fontsize=11)
    ax_main.tick_params(colors='#555577')
    ax_main.set_xlabel('x', color='#7070aa')
    ax_main.set_ylabel('y', color='#7070aa')
    for spine in ax_main.spines.values():
        spine.set_edgecolor('#333355')
 
    # --- Info panel ---
    Epx, Epy = field_at_point(charges, px, py)
    E_mag  = np.sqrt(Epx**2 + Epy**2)
    E_angle = np.degrees(np.arctan2(Epy, Epx))
 
    ax_info.cla()
    ax_info.set_facecolor('#0d0d1a')
    ax_info.axis('off')
    ax_info.set_title('Field at Probe', color='#e0e0ff', fontsize=10)
 
    lines = [
        ('Position',  f'({px:.2f},  {py:.2f})'),
        ('Ex',        f'{Epx:+.3f}'),
        ('Ey',        f'{Epy:+.3f}'),
        ('|E|',       f'{E_mag:.3f}'),
        ('Angle',     f'{E_angle:.1f}°'),
    ]
    for i, (label, value) in enumerate(lines):
        ax_info.text(0.05, 0.85 - i*0.17, label + ':', color='#7070cc',
                     fontsize=10, transform=ax_info.transAxes)
        ax_info.text(0.55, 0.85 - i*0.17, value, color='#00ffaa',
                     fontsize=10, fontweight='bold', transform=ax_info.transAxes)
 
    # --- Vector panel ---
    ax_vec.cla()
    ax_vec.set_facecolor('#0d0d1a')
    ax_vec.set_title('Field Vector', color='#e0e0ff', fontsize=10)
    ax_vec.set_xlim(-1.5, 1.5)
    ax_vec.set_ylim(-1.5, 1.5)
    ax_vec.set_aspect('equal')
    ax_vec.tick_params(colors='#555577', labelsize=7)
    for spine in ax_vec.spines.values():
        spine.set_edgecolor('#333355')
 
    norm = E_mag if E_mag > 0 else 1
    ux, uy = Epx / norm, Epy / norm
    ax_vec.annotate('', xy=(ux, uy), xytext=(0, 0),
                    arrowprops=dict(arrowstyle='->', color='#00ffaa',
                                    lw=2.5, mutation_scale=20))
    ax_vec.plot(0, 0, 'o', color='#00ffaa', markersize=5)
    ax_vec.axhline(0, color='#333355', lw=0.5)
    ax_vec.axvline(0, color='#333355', lw=0.5)
    ax_vec.set_xlabel('x', color='#7070aa', fontsize=8)
    ax_vec.set_ylabel('y', color='#7070aa', fontsize=8)
 
    fig.canvas.draw_idle()
 
def reset(event):
    s_c1x.reset(); s_c1y.reset(); s_c1q.reset()
    s_c2x.reset(); s_c2y.reset(); s_c2q.reset()
    s_px.reset();  s_py.reset()
 
for s in [s_c1x, s_c1y, s_c1q, s_c2x, s_c2y, s_c2q, s_px, s_py]:
    s.on_changed(draw)
 
btn_reset.on_clicked(reset)
 
draw()
plt.show()
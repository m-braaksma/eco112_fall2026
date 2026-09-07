"""Generate the ECO 112 sidebar logo and favicon.

Run directly: python assets/generate_logo.py
Outputs (sidebar_logo.png, favicon.ico) land next to this script and are
referenced from _quarto.yml. Tweak colors/curve/points below and re-run.

The sidebar background is dark maroon (SIDEBAR_BG), so both assets use
light/gold line colors on a transparent background. The favicon has no
fine detail (no gridlines, thick strokes) since it needs to read at a
16-32px browser tab size.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from pathlib import Path
from PIL import Image

OUT_DIR = Path(__file__).parent

# ----------------------------------------------------------------------
# Colors
# ----------------------------------------------------------------------

SIDEBAR_BG = "#660033"    # matches website.sidebar.background in _quarto.yml
MAROON = "#660033"
GOLD = "#e8c05a"          # trend line / accent
WHITE = "#ffffff"
SILVER = "#c9c2c4"        # scattered "data" points


def _growth_curve(x0, x1, y0, amp=0.22, slope=0.42, n=100, phase_origin=None):
    # phase_origin anchors the sine/slope so a second call over a different
    # x-range (e.g. scatter points) still lands on the same curve as the
    # main line, instead of each call restarting its own phase at x0.
    origin = x0 if phase_origin is None else phase_origin
    x = np.linspace(x0, x1, n)
    y = y0 + slope * (x - origin) + amp * np.sin((x - origin) * 2.2)
    return x, y


def new_fig(square=6):
    fig, ax = plt.subplots(figsize=(square, square), facecolor="none")
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


def save(fig, name, pad=0.02):
    fig.savefig(OUT_DIR / name, dpi=300, bbox_inches="tight", pad_inches=pad, transparent=True)
    plt.close(fig)


# ----------------------------------------------------------------------
# Sidebar logo: "ECO 112" wordmark with a fitted trend line running
# through a scatter of "data" points underneath
# ----------------------------------------------------------------------

fig, ax = new_fig()
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.text(5, 6.6, "ECO", fontsize=30, ha="center", va="bottom",
        color=WHITE, family="sans-serif", fontweight="light")
ax.text(5, 6.5, "112", fontsize=54, ha="center", va="top",
        color=WHITE, family="sans-serif", fontweight="bold")

curve_x0 = 1.8
x, y = _growth_curve(curve_x0, 8.2, 1.7, n=80)

rng = np.random.default_rng(7)
x_scatter, y_fit_at_scatter = _growth_curve(curve_x0, 8.2, 1.7, n=16)
y_scatter = y_fit_at_scatter + rng.normal(0, 0.35, size=x_scatter.size)
ax.scatter(x_scatter, y_scatter, color=SILVER, s=22, alpha=0.85, zorder=2)

ax.plot(x, y, color=GOLD, linewidth=4, solid_capstyle="round", zorder=3)
save(fig, "sidebar_logo.png")

# ----------------------------------------------------------------------
# Favicon: a maroon disc with a white ring and a gold rising line, no
# gridlines or scatter, simple enough to survive a 16px browser tab
# ----------------------------------------------------------------------

fig, ax = new_fig(square=4)
ax.set_xlim(1.6, 8.4)
ax.set_ylim(1.6, 8.4)
ax.add_patch(Circle((5, 5), 3.4, facecolor=MAROON, edgecolor="none", zorder=0))
ax.add_patch(Circle((5, 5), 2.9, fill=False, linewidth=4.5, edgecolor=WHITE, alpha=0.95))
fx, fy = _growth_curve(2.4, 7.6, 4.1, amp=0.18, slope=0.28)
ax.plot(fx, fy, color=GOLD, linewidth=5.5, alpha=0.98, solid_capstyle="round", zorder=3)
save(fig, "favicon_source.png", pad=0)

favicon_img = Image.open(OUT_DIR / "favicon_source.png").convert("RGBA")
favicon_img.save(OUT_DIR / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])
(OUT_DIR / "favicon_source.png").unlink()

print("Wrote sidebar_logo.png and favicon.ico to", OUT_DIR)

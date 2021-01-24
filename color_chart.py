# generates a color-chart used for data collection
# 1-20-21

# == imports == #
import numpy as np
from dg_tools import ColorTools as ct

# == main == #
colors = []
ncols = 15 #14 color cols & 1 gray-scale col
nrows = 10
hue = np.linspace(0,350, num = ncols-1) # red - magenta/pink
light = np.linspace(0.1,0.9, num = nrows)

# main colors
main_colors = []
for l in light:
    for h in hue:
        main_colors.append(ct.hsl_to_rgb(h,1,l))

# gray-scale column
gray = []
for l in np.linspace(0,1, num = nrows):
    gray.append(ct.hsl_to_rgb(0,0,l))

# concatenate
# note: colors is a 1d item array
i = 0
for rowx in range(nrows):
    for colx in range(ncols):
        if colx == ncols-1:
            colors.append(gray[rowx])
        else: 
            colors.append(main_colors[i])
            i += 1

ct.plot_colors(colors,(nrows,ncols),save_path='graphs/color_chart')

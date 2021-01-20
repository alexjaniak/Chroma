"""generates a color-chart used for data collection"""

# == imports ==
import string
import matplotlib.pyplot as plt
import numpy as np

# == functions ==
 
# converts hsl to rgb
def hsl_to_rgb(h: 'hue', s: 'saturation', l: 'lightness') -> '[r,g,b]': 
    # h∈[0,365], s∈[0,1], l∈[0,1]
    # returns rgb conversion where r, g, b ∈ [0,255]
    r, g, b = 0, 0, 0
    
    c = (1-abs(2*l-1))*s #chroma
    hp = h/60
    x = c * (1-abs(hp%2-1))
    m = l - 0.5*c
    
    if 0 <= hp <= 1:
        r, g, b = c, x, 0
    elif 1 < hp <= 2:
        r, g, b = x, c, 0
    elif 2 < hp <= 3:
        r, g, b = 0, c, x
    elif 3 < hp <= 4:
        r, g, b = 0, x, c
    elif 4 < hp <= 5:
        r, g, b = x, 0, c
    elif 5 < hp < 6:
        r, g, b = c, 0, x
    
    rgb = (np.array([r,g,b])+m)*255
    return np.ceil(rgb).astype(int)

# display a grid of colors using mpl subplots
# originally designed for a jupyter notebook 
def plot_colors(colors: '[[r,g,b]]', grid:'(rows,cols)' = (1,1), axis = True, save_path=None):
    
    # if single cell 
    if grid == (1,1):
        plt.imshow([[colors[0]]])
        plt.axis('off')
        
    else:
        # assumed rows*cols == len(colors)
        i = 0
        nrows, ncols = grid
        fig, axs = plt.subplots(nrows, ncols)
        col_labels = list(string.ascii_lowercase)
        row_labels = list(range(1,nrows+1))
        
        # if single col or row
        if nrows == 1 or ncols == 1: 
            nimgs = ncols if nrows == 1 else nrows
            for imgx in range(nimgs):
                axs[imgx].imshow([[colors[i]]])
                if not axis: axs[imgx].axis('off')
                i += 1
        else:
            for rowx in range(nrows):
                for colx in range(ncols):
                    ax = axs[rowx,colx]
                    ax.imshow([[colors[i]]])
                    
                    if not axis: ax.axis('off')
                    else: 
                        ax.tick_params(axis='both', which='both',length=0)
                        ax.set_xticks([0])
                        ax.set_yticks([0])
                        
                        if rowx != 0:
                            ax.set_xticklabels([])
                        else:
                            ax.xaxis.tick_top()
                            ax.set_xticklabels([col_labels[colx]])
                            
                        if colx != 0:
                            ax.set_yticklabels([])
                        else:
                            ax.set_yticklabels([row_labels[rowx]])                
                    i += 1

    fig.patch.set_facecolor('white')           
    if save_path: plt.savefig(save_path, dpi=300)
    plt.show()

# == main ==
main_colors = []
ncols = 15 #14 color cols & 1 gray-scale col
nrows = 10
hue = np.linspace(0,350, num = ncols-1) # red - magenta/pink
light = np.linspace(0.1,0.9, num = nrows)

# main colors
for l in light:
    for h in hue:
        main_colors.append(hsl_to_rgb(h,1,l))

# gray-scale column
gray = []
for l in np.linspace(0,1, num = nrows):
    gray.append(hsl_to_rgb(0,0,l))

# concatenate
# note: colors is a 1d item array
colors = []
i = 0
for rowx in range(nrows):
    for colx in range(ncols):
        if colx == ncols-1:
            colors.append(gray[rowx])
        else: 
            colors.append(main_colors[i])
            i += 1

plot_colors(colors,(nrows,ncols),save_path='graphs/color_chart')

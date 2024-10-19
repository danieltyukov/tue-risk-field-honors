IMAGE_SIZE = 150*2
import numpy as np
import matplotlib.pyplot as plt
import itertools

plt.ion()
#plt.switch_backend('agg')

fig1, ax1 = plt.subplots()
fig1.set_size_inches(12,12)
ax1.set_title("Scalar risk field Map",fontsize=25, fontweight = 'bold')
ax1.set_xlabel('X/cm',fontsize = 16 )
ax1.set_ylabel('Y/cm',fontsize = 16 )



# set the color scale with vmin/vman
array = np.zeros(shape=(IMAGE_SIZE, IMAGE_SIZE), dtype=np.uint8)
axim2 = ax1.imshow(array, vmin=0, vmax=120, cmap='jet', extent=[-IMAGE_SIZE/2, IMAGE_SIZE/2, -IMAGE_SIZE/2, IMAGE_SIZE/2])
cbar = fig1.colorbar(axim2, ax=ax1)
cbar.set_label('Risk Level', rotation=270, labelpad=20, fontsize=16)



def view(grid):
    show_grid(grid)


del array



def show_grid(grid):    
    axim2.set_data(grid)
    fig1.canvas.flush_events()





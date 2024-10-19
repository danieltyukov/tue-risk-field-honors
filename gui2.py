import numpy as np
import pygame

IMAGE_SIZE = 150 * 2
GRID_SIZE = 300  # Adjust this if necessary

pygame.init()
screen = pygame.display.set_mode((IMAGE_SIZE, IMAGE_SIZE))
pygame.display.set_caption("Scalar risk field Map")

def show_grid(grid):
    # Ensure the grid is a NumPy array and has the correct data type
    if isinstance(grid, list):
        grid = np.array(grid, dtype=np.uint8)
    else:
        grid = grid.astype(np.uint8)
    
    # Scale the grid values to fit in the range [0, 255]
    grid = (grid / np.max(grid) * 255).astype(np.uint8)

    # Create a surface from the grid array
    surface = pygame.surfarray.make_surface(grid.T)
    screen.blit(surface, (0, 0))
    pygame.display.flip()

def close_display():
    pygame.quit()

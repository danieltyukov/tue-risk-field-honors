IMAGE_SIZE = 100
import numpy as np
import matplotlib.pyplot as plt
import itertools
from vector import *
from gui import *
import time
import cProfile
import pstats
""" Constants """
v_o = 24.2 # m/s  This is the speed of the traditional vechicle, assuming its only in one direction moving straight
epsilon0 = 0.1
epsilon1 = 1/(-np.log(epsilon0**2))**0.5
epsilon2 = 0.2420
epsilon3 = 5
epsilon4 = 0.05
epsilon5 = 0.0001
epsilon6=100



#Safe distance d calculation
# v_o : Traditional vehicle speed
# V_i = {x: v_i_x, y: v_i_y}
# d_i = {x: d_i_x, y: d_i_y}

calc_d_i = lambda v_o, V_i: Vector(  3*(v_o + np.abs(V_i.x))    ,   3*(v_o + np.abs(V_i.y)))



#Beta calculation
calc_beta_i = lambda d_i, v_o, V_i, epsilon2, epsilon3, epsilon4 : Vector(np.log(d_i.x *(v_o - np.abs(V_i.x) - epsilon2) / (2 * (np.abs(V_i.x + epsilon2)))), np.log(d_i.y * (epsilon3 - np.abs(V_i.y) - epsilon4) / (2 * (np.abs(V_i.y + epsilon4)))))

#Alpha calculation
calc_alpha_i = lambda V_i, v_o, epsilon1, epsilon2,epsilon3, epsilon4: Vector( epsilon1 * np.log((v_o + np.abs(V_i.x) + epsilon2) / (v_o - np.abs(V_i.x) - epsilon2)) , epsilon1 * np.log((epsilon3 + np.abs(V_i.y) + epsilon4) / (epsilon3 - np.abs(V_i.y) - epsilon4)))

#delta calculation
calc_delta_i = lambda V_i, P_i, P, exp_beta_i: Vector(
    np.sign(V_i.x) * (P.x - P_i.x) + exp_beta_i.x,
    np.sign(V_i.y) * (P.y - P_i.y) + exp_beta_i.y  
)
 
#Risk function 
# alpha = [x:alpha_x, y:alpha_y]
# beta = [x:beta_x, y:beta_y]
# delta = [x:delta_x, y:delta_y]
# pos = [x: pos_x, y = pos_y]
f_i = lambda delta, alpha, beta : np.exp(-0.5 * ((np.log(delta.x) - beta.x )/ alpha.x) ** 2) * np.exp(-0.5 * ((np.log(delta.y) - beta.y )/ alpha.y) ** 2)







calc_time = []
disp_time = []



disp_time_total = []



def main():
    for x_moving in range(40,70,2):
        #create a moving car:
        P_1 = Vector(x_moving,60)
        V_1 = Vector(6,0.1)

        #preform calculations:
        
        d_1 = calc_d_i(v_o,V_1)
        beta_1 = calc_beta_i(d_1,v_o,V_1,epsilon2,epsilon3,epsilon4)
        exp_beta_i = Vector(np.exp(beta_1.x), np.exp(beta_1.y))
        
        alpha_1 = calc_alpha_i(V_1,v_o,epsilon1,epsilon2,epsilon3,epsilon4)
        
        grid_size = 300
        grid_size = 300
        grid = [[0 for x in range(grid_size)] for y in range(grid_size)]
        t1 = time.time()






        
        for x, y in itertools.product(range(300), range(300)):
            
            delta_1 = calc_delta_i(V_1,P_1,Vector(x,y), exp_beta_i)
            grid[y][x] = epsilon6 * f_i(delta_1,alpha_1,beta_1) if (delta_1.x > 0 and delta_1.y >0) else epsilon5
            
        


        t2 = time.time()
        calc_time.append(t2-t1)

        t3 = time.time()
        show_grid(grid)
        t4 = time.time()
        disp_time.append(t4-t3)
        print(f"Display update time:{np.mean(disp_time)}, calculation time: {np.mean(calc_time)}")
        disp_time_total.append(np.mean(disp_time))




if __name__ == '__main__':
    cProfile.run('main()', 'profiling_results')

    # Load the profiling results
    p = pstats.Stats('profiling_results')
    p.strip_dirs().sort_stats('cumtime').print_stats(100)






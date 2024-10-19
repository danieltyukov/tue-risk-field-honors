IMAGE_SIZE = 100
import numpy as np
import matplotlib.pyplot as plt
import itertools
from vector import *
import time
from multiprocessing import Pool, cpu_count
import pdb
from numba import njit, prange

""" Constants """
v_o = 24.2 # m/s  This is the speed of the traditional vechicle, assuming its only in one direction moving straight
epsilon0 = 0.1
epsilon1 = 1/(-np.log(epsilon0**2))**0.5
epsilon2 = 0.2420
epsilon3 = 2
epsilon4 = 0.05
epsilon5 = 0.0001
epsilon6=100

#second_constant = 0.5 #for three second rule 3
seperation_d = 2# seperation distance


#Safe distance d calculation
# v_o : Traditional vehicle speed
# V_i = {x: v_i_x, y: v_i_y}
# d_i = {x: d_i_x, y: d_i_y}


@njit(fastmath=True)
def calc_d_i(v_o, V_i, second_constant):
    return np.array([second_constant * (v_o + np.abs(V_i[0])), second_constant * (v_o + np.abs(V_i[1]))])



#Beta calculation
@njit(fastmath=True)
def calc_beta_i(d_i, v_o, V_i, epsilon2, epsilon3, epsilon4):
    return np.array([np.log(d_i[0] * (v_o - np.abs(V_i[0]) - epsilon2) / (2 * (np.abs(V_i[0] + epsilon2)))),
                     np.log(d_i[1] * (epsilon3 - np.abs(V_i[1]) - epsilon4) / (2 * (np.abs(V_i[1] + epsilon4))))])

#Alpha calculation
@njit(fastmath=True)
def calc_alpha_i(V_i, v_o, epsilon1, epsilon2, epsilon3, epsilon4):
    return np.array([epsilon1 * np.log((v_o + np.abs(V_i[0]) + epsilon2) / (v_o - np.abs(V_i[0]) - epsilon2)),
                     epsilon1 * np.log((epsilon3 + np.abs(V_i[1]) + epsilon4) / (epsilon3 - np.abs(V_i[1]) - epsilon4))])

#delta calculation
@njit(fastmath=True)
def calc_delta_i(V_i, P_i, P, exp_beta_i):
    return np.array([np.sign(V_i[0]) * (P[0] - P_i[0]) + exp_beta_i[0],
                     np.sign(V_i[1]) * (P[1] - P_i[1]) + exp_beta_i[1]])

#Risk function 
# alpha = [x:alpha_x, y:alpha_y]
# beta = [x:beta_x, y:beta_y]
# delta = [x:delta_x, y:delta_y]
# pos = [x: pos_x, y = pos_y]
@njit(fastmath=True)
def f_i(delta, alpha, beta):
    return np.exp(-0.5 * ((np.log(delta[0]) - beta[0]) / alpha[0])**2) * np.exp(-0.5 * ((np.log(delta[1]) - beta[1]) / alpha[1])**2)




@njit(parallel=True, fastmath=True)
def calc_y(V_1, P_1, x,exp_beta_i, epsilon2, epsilon3, epsilon4, epsilon5, epsilon6, second_constant,grid,alpha_1,beta_1 ):
    for y in range(300):
        delta_1 = calc_delta_i(V_1, P_1, np.array([x, y]), exp_beta_i)
        grid[299-y][x] += epsilon6 * f_i(delta_1, alpha_1, beta_1) if (delta_1[0] > 0 and delta_1[1] > 0) else epsilon5



@njit(parallel=True, fastmath=True)
def calculate_grid(grid, v_o, V_1, P_1, epsilon2, epsilon3, epsilon4, epsilon5, epsilon6, second_constant):
    d_1 = calc_d_i(v_o, V_1, second_constant)
    beta_1 = calc_beta_i(d_1, v_o, V_1, epsilon2, epsilon3, epsilon4)
    print(f"second_constant is {second_constant}")
    exp_beta_i = np.exp(beta_1)
    alpha_1 = calc_alpha_i(V_1, v_o, epsilon1, epsilon2, epsilon3, epsilon4)

    for x in range(300):
        calc_y(V_1, P_1, x,exp_beta_i, epsilon2, epsilon3, epsilon4, epsilon5, epsilon6, second_constant,grid,alpha_1,beta_1)
        





def calc_risk(obstacles):
    grid_size = 300
    grid = np.zeros((grid_size, grid_size))
    for obs in obstacles:
        x_pos = obs[0]
        y_pos = obs[1]
        size = obs[2]
        second_constant = size * 0.1
        #print("will calc risk")
        #create a moving car:
        x_pos = x_pos + 150
        y_pos = y_pos + 150 
        P_1 = np.array([x_pos,y_pos])
        V_1 = np.array([0.01,0.01]) 
        #preform calculations:
        calculate_grid(grid, v_o, V_1, P_1, epsilon2, epsilon3, epsilon4, epsilon5, epsilon6, second_constant)
    return grid

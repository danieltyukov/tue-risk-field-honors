import numpy as np
import time
import cProfile
import pstats
from numba import njit, prange
from vector import *
from gui import *

# Constants
v_o = 24.2  # m/s
epsilon0 = 0.1
epsilon1 = 1 / (-np.log(epsilon0**2))**0.5
epsilon2 = 0.2420
epsilon3 = 5
epsilon4 = 0.05
epsilon5 = 0.0001
epsilon6 = 100

# Calculation functions
@njit(fastmath=True)
def calc_d_i(v_o, V_i):
    return np.array([3 * (v_o + np.abs(V_i[0])), 3 * (v_o + np.abs(V_i[1]))])

@njit(fastmath=True)
def calc_beta_i(d_i, v_o, V_i, epsilon2, epsilon3, epsilon4):
    return np.array([np.log(d_i[0] * (v_o - np.abs(V_i[0]) - epsilon2) / (2 * (np.abs(V_i[0] + epsilon2)))),
                     np.log(d_i[1] * (epsilon3 - np.abs(V_i[1]) - epsilon4) / (2 * (np.abs(V_i[1] + epsilon4))))])

@njit(fastmath=True)
def calc_alpha_i(V_i, v_o, epsilon1, epsilon2, epsilon3, epsilon4):
    return np.array([epsilon1 * np.log((v_o + np.abs(V_i[0]) + epsilon2) / (v_o - np.abs(V_i[0]) - epsilon2)),
                     epsilon1 * np.log((epsilon3 + np.abs(V_i[1]) + epsilon4) / (epsilon3 - np.abs(V_i[1]) - epsilon4))])

@njit(fastmath=True)
def calc_delta_i(V_i, P_i, P, exp_beta_i):
    return np.array([np.sign(V_i[0]) * (P[0] - P_i[0]) + exp_beta_i[0],
                     np.sign(V_i[1]) * (P[1] - P_i[1]) + exp_beta_i[1]])

@njit(fastmath=True)
def f_i(delta, alpha, beta):
    return np.exp(-0.5 * ((np.log(delta[0]) - beta[0]) / alpha[0])**2) * np.exp(-0.5 * ((np.log(delta[1]) - beta[1]) / alpha[1])**2)



@njit(parallel=True, fastmath=True)
def matrix_calc(grid, v_o, V_1, P_1, epsilon2, epsilon3, epsilon4, epsilon5, epsilon6 ,d_1,beta_1,exp_beta_i,alpha_1):
    for x in range(300):
        for y in range(300):
            delta_1 = calc_delta_i(V_1, P_1, np.array([x, y]), exp_beta_i)
            grid[y][x] = epsilon6 * f_i(delta_1, alpha_1, beta_1) if (delta_1[0] > 0 and delta_1[1] > 0) else epsilon5



@njit(fastmath=True)
def calculate_grid(grid, v_o, V_1, P_1, epsilon2, epsilon3, epsilon4, epsilon5, epsilon6):
    d_1 = calc_d_i(v_o, V_1)
    beta_1 = calc_beta_i(d_1, v_o, V_1, epsilon2, epsilon3, epsilon4)
    exp_beta_i = np.exp(beta_1)
    alpha_1 = calc_alpha_i(V_1, v_o, epsilon1, epsilon2, epsilon3, epsilon4)
    matrix_calc(grid, v_o, V_1, P_1, epsilon2, epsilon3, epsilon4, epsilon5, epsilon6,d_1,beta_1,exp_beta_i,alpha_1)
   
calc_time = []
disp_time = []
disp_time_total = []

def main():
    for x_moving in range(40, 70, 2):
        P_1 = np.array([x_moving, 60])
        V_1 = np.array([6, 0.1])

        grid_size = 300
        grid = np.zeros((grid_size, grid_size))

        t1 = time.time()
        calculate_grid(grid, v_o, V_1, P_1, epsilon2, epsilon3, epsilon4, epsilon5, epsilon6)
        t2 = time.time()
        calc_time.append(t2 - t1)

        t3 = time.time()
        show_grid(grid)
        t4 = time.time()
        disp_time.append(t4 - t3)
        print(f"Display update time: {np.mean(disp_time)}, calculation time: {np.mean(calc_time)}")
        disp_time_total.append(np.mean(disp_time))

if __name__ == '__main__':
    cProfile.run('main()', 'profiling_results')

    p = pstats.Stats('profiling_results')
    p.strip_dirs().sort_stats('cumtime').print_stats(100)

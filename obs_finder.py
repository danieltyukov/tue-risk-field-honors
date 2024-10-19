from risk_field import *
import math
import pdb
import matplotlib.pyplot as plt

def test_graph(objs):
    x_arr = [obj[0] for obj in objs]
    y_arr = [obj[1] for obj in objs]
    plt.scatter(x_arr,y_arr,marker = 'x', c='r')
    plt.xlim([-150,150])
    plt.ylim([-150,150])
    plt.show()

def parse_data(data):
    objs = []
    angle_min = data["angle_min"]
    increment = data["angle_increment"]
    flag = False
    alpha1 = 0
    radius = 0
    count = 0
    for i in range(len(data["ranges"])):
        if (int(data["ranges"][i]*100) < 160) and (int(data["ranges"][i]*100) > 15):
            if not flag:
                alpha1 = angle_min + i*increment
                radius = data["ranges"][i]*100
                flag = True
            else:
                count+=1
        else:
            if flag and count > 4:
                print(count)
                angle = 0.5*(angle_min + i*increment + alpha1)
                x = radius * math.sin(angle)
                y = radius * math.cos(angle)
                size = 2 * radius * math.tan(0.5 * count * increment)
                objs.append(np.array([x,y,size]))
                
                #print(f"X: {x} cm, Y: {y} cm")
                t1 = time.time()
                #grid = calc_risk(x,y)
                #print(f"Calc time was {time.time() - t1}")
            flag = False
            count = 0
    return objs
    
import socket
from risk_field import *
import pdb
import network
from obs_finder import parse_data

"""
def parse_data(data):
    
    try:
        
        x = int(data[0]*100) 
        y = int(data[1]*100)   
        print(f"X: {x} cm, Y: {y} cm")
        t1 = time.time()
        grid = calc_risk(x,y)
        print(f"Calc time was {time.time() - t1}")
        show_grid(grid)
    except Exception as e:
        print(f"Exception {e} data is {data}")    
 """
def start_server(host='10.128.7.82', port=8584):
    config_net = network.network_config
    config_net['HOST'] = host
    conn = network.network_object(config_net)
    print(f"Server started, waiting for connections on {host}:{port}...")

    while True:
        print(f"Connection established with")

        try:
            while True:
                data, name_clase = conn.recv_object()
                conn.send_object("send recieved")
                if name_clase == Exception:
                    print(data)
                    break
                #print(f"Received data: {data}")
                t1 = time.time()
                obstacles = parse_data(data)
                risk_field = calc_risk(obstacles)
                show_grid(risk_field)
                print(f"Calc time was {time.time() - t1}")
                del risk_field
        except ConnectionResetError:
            print("Connection lost, waiting for new connection...")
        finally:
            conn.stop_network()
        if name_clase == Exception: break

if __name__ == "__main__":
    from gui import *
    start_server()

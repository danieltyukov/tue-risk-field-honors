import configparser
import concurrent.futures
import pickle
import socket

#from dataclasses import dataclass, field

network_config: dict ={
    'PORT': 8584,
    'HOST': '127.0.0.1',
    'CONNECT': '127.0.0.1',
    'server': True
}

class network_object:

    def __init__(self, config: dict = None) -> None:
        self.config = config
        self.kill = False
        if self.config == None:
            self.config = self.get_config_File()
        print('config done')
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.thread_Executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)

        if self.config['server']:
            self.config_socket()
            self.accept_connect()
        else:
            self.connect_socket()
        print('stream done')

    
    def get_config_File(self) -> dict:
        try:
            configParser = configparser.ConfigParser()
            configParser.read('networkconfig.ini')
            networkConfig = configParser['network']
            config = network_config.copy()
            config['PORT'] = networkConfig.getint('PORT',config['PORT'])
            config['HOST'] = networkConfig.get('HOST',config['HOST'])
            config['CONNECT'] = networkConfig.get('CONNECT',config['CONNECT'])
            config['server'] = networkConfig.getboolean('server',config['server'])
            return config
        except Exception as Error:
            print(f'error in config error:{Error}')
            return network_config

    #sets the socket up to accept incoming connections
    def config_socket(self) -> bool:
        try:
            self.socket.bind((self.config['HOST'],self.config['PORT']))
            return True
        except OSError as error:
            print(f'cannot config socket error:{error}')
            return False

    def accept_connect(self) -> str:
        try:
            self.socket.listen()
            self.conn, self.addr = self.socket.accept()
            self.stream = self.conn.makefile('rwb')
            #self.future = self.thread_Executor.submit(self.recv_object)
            return self.addr
        except Exception as error:
            print(f'could not accept connection error: {error}')
            return None

    def connect_socket(self) -> bool:
        try:
            self.socket.connect((self.config['HOST'],self.config['PORT']))
            self.conn = self.socket
            self.stream = self.conn.makefile('rwb')
            #self.future = self.thread_Executor.submit(self.recv_object)
            return True
        except Exception as error:
            print(f'could not connect error: {error}')
            return False

    def recv_object(self) -> tuple[object,str]:
        try:
            recv_object = pickle.load(self.stream)
            return (recv_object, type(recv_object))
        except Exception as error:
            print(f'could not recv object error:{error}')
            return (error, Exception)
    
    def recv_nonBlock_object(self) -> tuple[object,object]: #not working
        try:
            return
            if self.future.done():
                data = self.future.result()
                self.future = self.thread_Executor.submit(self.recv_object)
                return data
            else:
                return (None,None)
        except concurrent.futures.CancelledError as Error:
            print(f'Error in recv_nonBlock_object Error:{Error}')
            data = self.future.cancel()
            self.future = self.thread_Executor.submit(self.recv_object)
            return (data,data)

    
    def send_object(self,send_object: object) -> bool:
        try:
            pickle.dump(send_object, self.stream)
            self.stream.flush()
            return True
        except Exception as error:
            print(f'could not send object error:{error}')
            
    
    def stop_network(self) -> None:
        print('closing conn')
        self.conn.close()
        print('closing socket')
        self.socket.close()
        return
import socket

class Client:
    def __init__(self, host, x, y, angle, mapName):
        self.host = host
        self.port = 31415
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))
        #self.sock.send('Connected to server'.encode('utf-8'))
        #self.listen(x, y, angle, mapName)

    def listen(self, x, y, angle, mapName, est, name):
        if est:
            mxg = f'establish,{name},{x},{y},{angle},{mapName}'
            self.sock.send(mxg.encode('utf-8'))
        self.sock.settimeout(0.1)
        #print("E")
        try:
            data = self.sock.recv(1024).decode('utf-8')
            if data == 'exit':
                self.sock.close()
                print('Closed connection to server')
            else:
                return data
        except:
            return None

    def sendUpdate(self, x, y, angle, mapName):
        # clear the buffer
        self.sock.setblocking(False)
        try:
            while True:
                self.sock.recv(1024)
        except:
            pass
        self.sock.send(f'update,{x},{y},{angle},{mapName}'.encode('utf-8'))
        
        self.sock.settimeout(0.1)
        try:
            response = self.sock.recv(1024).decode('utf-8')
            if response == 'exit':
                self.sock.close()
                print('Closed connection to server')
            else:
                return response
        except:
            return None

    def sendHit(self, enemy):
        self.sock.send(f'hit,{enemy}'.encode('utf-8'))

    def sendShootPlayer(self, enemy):
        self.sock.settimeout(0.1)
        try:
            self.sock.send(f'shootPlayer,{enemy}'.encode('utf-8'))
        except:
            self.sendShootPlayer(enemy)

if __name__ == '__main__':
    client = Client()
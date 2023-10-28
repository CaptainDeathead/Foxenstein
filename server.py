import socket
import keyboard
import sys

class Client:
    def __init__(self, x, y, angle, name, client, address, mapName):
        self.x = x
        self.y = y
        self.angle = angle
        self.name = name
        self.hp = 5
        self.kills = 0
        self.deaths = 0
        self.client = client
        self.address = address
        self.mapName = mapName
        
    def update(self, x, y, angle, mapName):
        self.x = x
        self.y = y
        self.angle = angle
        self.mapName = mapName

    def hit(self, enemy):
        print(self.hp)
        self.hp -= 1
        if self.hp <= 0:
            enemy.kills += 1
            self.deaths += 1
            self.hp = 5

    def shootPlayer(self, enemy):
        print(enemy)
        enemy.hit(self)

class Server:
    def __init__(self, numPlayers):
        self.host = '192.168.0.30'
        self.port = 31415
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.sock.listen(1)
        self.clients = []
        self.numPlayers = numPlayers

    def listen(self):
        while len(self.clients) < self.numPlayers:
            client, address = self.sock.accept()
            print(f'Connected to {address}')
            #client.send('Connected to server'.encode('utf-8'))
            self.handleClient(client, address)

        print(len(self.clients), self.numPlayers)
        self.handleClients()

    def handleClients(self):
        print("TEJ")
        while True:
            mxg = []
            for client in self.clients:
                self.handleClient(client.client, client.address)
                mxg.append(f'{client.address[0]},{client.x},{client.y},{client.angle},{client.mapName},{client.hp}')
            
            self.sendAll(str(mxg))

    def handleClient(self, client, address):
        try:
            # timeout the recv function so that it doesn't block the program
            client.settimeout(0.1)
            data = client.recv(1024).decode('utf-8')
            #print(data)
            
            if 'establish' in data:
                print("established")
                name = data.split(',')[1]
                x = data.split(',')[2]
                y = data.split(',')[3]
                angle = data.split(',')[4]
                mapName = data.split(',')[5]
                self.clients.append(Client(x, y, angle, name, client, address, mapName))
                i = self.clients.index(self.clients[-1])
                print(f'Added {name} to clients')
            elif data == 'exit':
                client.close()
                self.clients.pop(i)
                print(f'Closed connection to {address}')
            else:
                identifier = data.split(',')[0]
                if identifier == 'update':
                    x = data.split(',')[1]
                    y = data.split(',')[2]
                    angle = data.split(',')[3]
                    mapName = data.split(',')[4]
                    mxg = []
                    for c in self.clients:
                        if c.address == address:
                            c.update(x, y, angle, mapName)
                        mxg.append(f'{c.address},{c.x},{c.y},{c.angle},{c.mapName},{c.hp}')
                    # send it back to just the client that sent it
                    #client.send(mxg.encode('utf-8'))

                elif identifier == 'hit':
                    enemy = data.split(',')[1]
                    for c in self.clients:
                        if c.address == enemy:
                            c.hit()
                elif identifier == 'shootPlayer':
                    enemy = data.split(',')[1]
                    for c in self.clients:
                        if c.address[0] == enemy:
                            #print(c.hp)
                            c.hp -= 1
                            if c.hp == 0:
                                self.clients.pop(self.clients.index(c))
                                #self.clients[i].kills += 1
                                print(len(self.clients))
                                if len(self.clients) == 1:
                                    print(f"Game over! {self.clients[0].name} won!")
                                    sys.exit()

        except:
            pass
            #client.close()
            #print(f'Closed connection to {address}')

    def sendAll(self, data):
        for client in self.clients:
            #client.send(data.encode('utf-8'))
            try:
                client.client.send(data.encode('utf-8'))
            except ConnectionResetError:
                self.clients.pop(self.clients.index(client))
                print(f'Closed connection to {client.address}')
                if len(self.clients) == 0:
                    print("No clients left")
                    sys.exit()
            except TimeoutError:
                pass

if __name__ == '__main__':
    server = Server(int(sys.argv[1]))
    server.listen()
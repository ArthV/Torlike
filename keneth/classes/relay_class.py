""" client and server classes """
from classes.server_class import Server
from classes.client_class import Client
from _thread import start_new_thread


class Relay:
    """ relay class """

    def __init__(self, listen_host, listen_port, foward_list):
        """ server constructor """
        self.listen_host = listen_host
        self.listen_port = listen_port
        self.foward_list = foward_list
        self.neighbors = []
        self.server = Server(self.listen_host, self.listen_port)
        for foward in self.foward_list:
            self.neighbors.append(
                Client(
                    foward['foward_host'], foward['foward_port']
                )
            )

    def start_connection(self):
        """ start connection """
        # self.server.start_connection()
        for neighbor in self.neighbors:
            neighbor.start_connection()
        while True:
            self.server.incoming_conn, self.server.incoming_addr = self.server.socket.accept()
            print('Connected to: %s:%i' %
                  (self.server.incoming_addr[0], self.server.incoming_addr[1]))
            start_new_thread(self.listen_and_foward, ())

    def listen_and_foward(self):
        """ listen and foward """
        while True:
            # get data from the client
            data = self.server.incoming_conn.recv(1024).decode()
            if not data:
                break
            print("Connection from: %s, data: %s" %
                  (self.server.incoming_addr, str(data)))
            # send data to the server
            print("sending: %s" % (str(data)))
            message = str(data).split(",")  # Data,port,port,port
            print(message)
            hops = len(message) - 1
            print("hops size: %i" % (hops))
            if hops > 0:
                neighbors_size = len(self.neighbors)
                print("size: %i, next hop: %s" % (neighbors_size, message[1]))
                if neighbors_size > 1:  # has more than 1 neighbor
                    for neighbor in self.neighbors:
                        if neighbor.port == int(message[1]):
                            print("is redirecting to the right neighbor: %i" %
                                  (neighbor.port))
                            new_data = message[0]
                            if hops > 1:
                                for i in range(1, hops):
                                    new_data += "," + message[i + 1]
                                data = neighbor.send_message(new_data.encode())
                            else:
                                data = neighbor.send_message(new_data.encode())
                            break
                else:
                    final_data = str(message[0])
                    data = self.neighbors[0].send_message(final_data.encode())
            else:
                final_data = str(message[0])
                data = self.neighbors[0].send_message(final_data.encode())
            print("Connection to: %s, data: %s" %
                  (self.server.incoming_addr, str(data)))
            # responding to client
            self.server.incoming_conn.send(data.encode())

        self.server.close_connection()
        for neighbor in self.neighbors:
            neighbor.close_connection()
        # self.client.close_connection()

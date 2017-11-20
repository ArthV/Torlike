""" client and server classes """
from classes.server_class import Server
from classes.client_class import Client


class Relay:
    """ relay class """

    def __init__(self, listen_host, listen_port, foward_host, foward_port):
        """ server constructor """
        self.listen_host = listen_host
        self.listen_port = listen_port
        self.foward_host = foward_host
        self.foward_port = foward_port
        self.server = Server(self.listen_host, self.listen_port)
        self.client = Client(self.foward_host, self.foward_port)

    def start_connection(self):
        """ start connection """
        self.server.start_connection()
        self.client.start_connection()

    def listen_and_foward(self):
        """ listen and foward """
        while True:
            # get the data from the client
            data = self.server.incoming_conn.recv(1024).decode()
            if not data:
                break
            print("Connection from: %s, data: %s" %
                  (self.server.incoming_addr, str(data)))
            # send the data to the server
            print("sending: %s" % (str(data)))
            data = self.client.send_message(data)
            print("Connection to: %s, data: %s" %
                  (self.server.incoming_addr, str(data)))
            self.server.incoming_conn.send(data.encode())

        self.server.close_connection()
        self.client.close_connection()

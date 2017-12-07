""" to use sockets"""
import socket


class Client:
    """ This class is used to start a new client socket in order to connect to 
        a particular server which is listening.
    """

    def __init__(self, host, port):
        """ This is where the new socket instance is created.
            Parameters
            ----------
            host : string
                The host where the server is bound.
            port : int
                The por where the server is bound.
            Returns
            -------
            new Client Object
        """
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start_connection(self):
        """ connect the socket to the server, using the previously setted
            paramaters
        """
        self.socket.connect((self.host, self.port))
        print("starting connection with: %s:%s" % (self.host, self.port))

    def send_message(self, message):
        """ send message """
        print("sending %s to: %s:%s" % (str(message), self.host, self.port))
        self.socket.send(message)
        data = self.socket.recv(1024).decode()
        return data

    def close_connection(self):
        """ close connection """
        self.socket.close()

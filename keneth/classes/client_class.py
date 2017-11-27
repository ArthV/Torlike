""" to use sockets"""
import socket


class Client:
    """ client class """

    def __init__(self, host, port):
        """ server constructor """
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.incoming_conn = None
        self.incoming_addr = None

    def start_connection(self):
        """ start connection """
        self.socket.connect((self.host, self.port))
        print("starting connection with: %s:%s" % (self.host, self.port))

    def send_message(self, message):
        """ send message """
        print("sending %s to: %s:%s" % (str(message), self.host, self.port))
        self.socket.send(message)
        data = self.socket.recv(1024).decode()
        #data = self.socket.recv(1024)
        return data

    def close_connection(self):
        """ close connection """
        self.socket.close()

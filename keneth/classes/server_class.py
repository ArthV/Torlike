""" to use sockets"""
import socket
from _thread import start_new_thread


class Server:
    """ server class """

    def __init__(self, host, port):
        """ server constructor """
        self.host = host
        self.port = port
        self.incoming_conn = None
        self.incoming_addr = None
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.bind((self.host, self.port))
        except socket.error as ex_message:
            print(str(ex_message))
        self.socket.listen(5)
        print("starting connection at: %s:%s" % (self.host, self.port))

    def start_connection(self):
        """ starting connection """
        while True:
            self.incoming_conn, self.incoming_addr = self.socket.accept()
            print('Connected to: %s:%i' %
                  (self.incoming_addr[0], self.incoming_addr[1]))
            start_new_thread(self.listen_for_messages, ())

    def listen_for_messages(self):
        """ reading message until no data"""
        while True:
            data = self.incoming_conn.recv(1024).decode()
            if not data:
                break
            print("from connected  user: " + str(data))

            data = str(data).upper()
            print("sending: " + str(data))
            self.incoming_conn.send(data.encode())
        self.close_connection()

    def close_connection(self):
        """ closing connection """
        self.incoming_conn.close()

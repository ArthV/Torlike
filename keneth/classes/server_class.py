""" to use sockets"""
import socket


class Server:
    """ server class """

    def __init__(self, host, port):
        """ server constructor """
        self.host = host
        self.port = port
        self.socket = socket.socket()
        self.incoming_conn = None
        self.incoming_addr = None

    def start_connection(self):
        """ starting connection """
        print("starting connection at: %s:%s" % (self.host, self.port))
        self.socket.bind((self.host, self.port))
        self.socket.listen(1)
        print("server is listening")
        self.incoming_conn, self.incoming_addr = self.socket.accept()
        print("Connection from: %s" % (str(self.incoming_addr)))

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

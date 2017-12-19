""" to use sockets"""
import socket
from _thread import start_new_thread
from MessageFactory import MessageFactory, Object, MessageBase


class Server:
    """ server class """

    def __init__(self, host, port):
        """ This is where the new socket instance is created.
            Parameters
            ----------
            host : string
                The host where the server will be bound.
            port : int
                The por where the server will be bound.
            Returns
            -------
            new Server Object
        """
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
            print(
                'Connected to: %s:%i' % (
                    self.incoming_addr[0], self.incoming_addr[1])
            )
            start_new_thread(self.listen_for_messages, ())

    def listen_for_messages(self):
        """ reading message until no data"""
        while True:
            data = self.incoming_conn.recv(1024)
            if not data:
                break
            print(
                "I'm: %s:%i I've received a message from %s:%i" %
                (
                    self.host,
                    self.port,
                    self.incoming_addr[0],
                    self.incoming_addr[1]
                )
            )
            # Here we have to get the message and based on the type do something
            version, message_type, length = MessageBase.get_type_version_length(
                data.decode()
            )
            print(
                "The message version is: %s, type: %s, length: %s" %
                (version, message_type, length)
            )
            if message_type == 0:  # KEY_INIT
                self.send_key(data)
            elif message_type == 2:  # MESSAGE_RELAY
                self.respond(data)
            else:  # Build an error message
                self.send_error(data)

        self.close_connection()

    def close_connection(self):
        """ closing connection """
        self.incoming_conn.close()

    def decrypt(self, message):
        """ Use the own key and apply the AES decypher algorithm """
        return message

    def send_key(self, message):
        """ reply with the key  """
        # generate the key
        message_shell = MessageFactory.get_empty_message('KEY_INIT')
        key_init_message = message_shell.decode(message)
        print('Key_init message')
        print(
            'type: %i, version: %i, key_id: %s, g:%s, p:%s, A:%s' %
            (
                key_init_message.type, key_init_message.version,
                key_init_message.key_id, key_init_message.g,
                key_init_message.p, key_init_message.A
            )
        )
        # Here we have to build a new message to reply to the client
        message_object = Object()
        message_object.version = 1
        message_object.key_id = 'test'
        message_object.B = 'test'
        message = MessageFactory.get_message('KEY_REPLY', message_object)
        self.incoming_conn.send(message.encode())

    def send_error(self, message):
        """ reply with an error if the message is malformed """
        message_object = Object()
        message_object.version = 1
        message_object.error_code = 1
        message = MessageFactory.get_message('ERROR', message_object)
        self.incoming_conn.send(message.encode())

    def respond(self, message):
        """ decrypt the message and respond to the client """
        message_shell = MessageFactory.get_empty_message('MESSAGE_RELAY')
        relay_message = message_shell.decode(message)
        decrypted_message = self.decrypt(relay_message.message)
        payload = ''
        response_message = "I've received the message"
        self.incoming_conn.send(response_message.encode())

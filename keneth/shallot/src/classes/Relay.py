""" client and server classes """
from _thread import start_new_thread
import Server
import Client
from MessageFactory import MessageFactory, Object, MessageBase


class Relay:
    """ relay class """

    def __init__(self, listen_host, listen_port, forward_list):
        """ This is where the new socket instance is created.
            Parameters
            ----------
            listen_host : string
                The host where the server will be bound.
            listen_port : int
                The por where the server will be bound.
            forward_list : dictionary list
                The nodes list who are next to this relay.
            Returns
            -------
            new Relay Object
        """
        self.listen_host = listen_host
        self.listen_port = listen_port
        self.neighbors = forward_list
        self.server = Server.Server(self.listen_host, self.listen_port)

    def start_connection(self):
        """ start connection """
        while True:
            self.server.incoming_conn, self.server.incoming_addr = self.server.socket.accept()
            print(
                'Connected to: %s:%i' % (
                    self.server.incoming_addr[0], self.server.incoming_addr[1]
                )
            )
            start_new_thread(self.listen_and_forward, ())

    def listen_and_forward(self):
        """ listen and forward """
        while True:
            # get data from the client
            data = self.server.incoming_conn.recv(1024) # Check if is enough
            if not data:
                break
            print(
                "I'm: %s:%i I've received a message from %s:%i" %
                (
                    self.server.host,
                    self.listen_port,
                    self.server.incoming_addr[0],
                    self.server.incoming_addr[1]
                )
            )
            # know the type of message
            version, message_type, length = MessageBase.get_type_version_length(
                data.decode()
            )
            print(
                "The message version is: %s, type: %s, length: %s" %
                (version, message_type, length)
            )
            # Here we have to get the message and based on the type do something

            if message_type == 0:  # KEY_INIT
                self.send_key(data)
            elif message_type == 2:  # MESSAGE_RELAY
                self.forward_message(data)
            else:  # Build an error message
                self.send_error(data)

        self.server.close_connection()

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
        self.server.incoming_conn.send(message.encode())

    def send_error(self, message):
        """ reply with an error if the message is malformed """
        message_object = Object()
        message_object.version = 1
        message_object.error_code = 1
        message = MessageFactory.get_message('ERROR', message_object)
        self.server.incoming_conn.send(message.encode())

    def forward_message(self, message):
        """ decrypt the message and send to the next hop """
        message_shell = MessageFactory.get_empty_message('MESSAGE_RELAY')
        relay_message = message_shell.decode(message)
        decrypted_message = self.decrypt(relay_message.message)
        decrypted_next_hop = self.decrypt(relay_message.next_hop).split(':')
        next_hop_host = decrypted_next_hop[0]
        next_hop_port = int(decrypted_next_hop[1])
        payload = decrypted_message
        client = Client.Client(next_hop_host, next_hop_port)
        client.start_connection()
        print("is redirecting to the next hop: %i" % (next_hop_port))
        answer = client.send_message(payload)  # Waiting for an answer
        self.server.incoming_conn.send(answer)  # Anwering the incom connection
        client.close_connection() # closing the connection after respond
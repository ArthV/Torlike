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
            #data = self.server.incoming_conn.recv(1024).decode()
            data = self.server.incoming_conn.recv(1024)
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
                data
            )
            print(
                "The message version is: %s, type: %s, length: %i" %
                (version, message_type, length)
            )
            # Here we have to get the message and based on the type do something

            if version == 0:  # KEY_INIT
                self.send_key(data)
            elif version == 2:  # MESSAGE_RELAY
                self.forward_message(data)
            else:  # Build an error message
                self.send_error(data)
            '''
            # send data to the server
            print("sending: %s" % (str(data)))
            message = str(data).split(",")  # Data,port,port,port
            print(message)
            hops = len(message) - 1
            print("hops size: %i" % (hops))
            if hops > 0:
                neighbors_size = len(self.neighbors)
                print(
                    "neighbors size: %i, next hop: %s" %
                    (neighbors_size, message[1])
                )
                if neighbors_size > 1:  # has more than 1 neighbor
                    for neighbor in self.neighbors:
                        if int(neighbor['forward_port']) == int(message[1]):
                            client = Client(
                                neighbor['forward_host'],
                                neighbor['forward_port']
                            )
                            client.start_connection()
                            print(
                                "is redirecting to the right neighbor: %i" %
                                (neighbor['forward_port'])
                            )
                            new_data = message[0]
                            if hops > 1:
                                for i in range(1, hops):
                                    new_data += "," + message[i + 1]
                                data = client.send_message(new_data.encode())
                            else:
                                data = client.send_message(new_data.encode())
                            break
                else:
                    client = Client(
                        self.neighbors[0]['forward_host'],
                        self.neighbors[0]['forward_port']
                    )
                    client.start_connection()
                    final_data = str(message[0])
                    data = client.send_message(final_data.encode())
            else:
                client = Client(
                    self.neighbors[0]['forward_host'],
                    self.neighbors[0]['forward_port']
                )
                client.start_connection()
                final_data = str(message[0])
                data = client.send_message(final_data.encode())
            print(
                "Connection to: %s, data: %s" %
                (self.server.incoming_addr, str(data))
            )
            # responding to client
            self.server.incoming_conn.send(data.encode())
            print(
                "Closing connection with : %s:%i" % (
                    self.server.incoming_addr[0],
                    self.server.incoming_addr[1]
                )
            )
            client.close_connection()
            '''
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
        next_hop_host = ''
        next_hop_port = 0
        payload = ''
        client = Client.Client(next_hop_host, next_hop_port)
        client.start_connection()
        print("is redirecting to the next hop: %i" % (next_hop_port))
        answer = client.send_message(payload.encode())
        self.server.incoming_conn.send(answer.encode())
        client.close_connection()

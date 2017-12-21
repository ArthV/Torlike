""" client and server classes """
from _thread import start_new_thread
import Server
import Client
from random import *
from MessageFactory import MessageFactory, Object, MessageBase
from EllipticCurve import EllipticCurve, EllipticCurvePoint, EllipticCurveNeutralEl
from FiniteField import FiniteField
from Crypto.Cipher import AES


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

        # Security object
        self.elliptic_curve = ''
        self.elliptic_point = ''
        self.A = ''
        self.B = ''
        self.C = ''


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
                data[0:8].decode()
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
        c = self.C
        key = ''
        len_x = 8 if len(c.x.coeffs) > 8 else len(c.x.coeffs)
        len_y = 8 if len(c.y.coeffs) > 8 else len(c.y.coeffs)
        for i in range(len_x):
            key += str(c.x.coeffs[i])
        for i in range(len_y):
            key += str(c.y.coeffs[i])

        encoded_key = (MessageBase.add_padding(key, 16)).encode()  # The AES algorithm only manipulates bytes
        cipher = AES.new(encoded_key)

        #message = message.decode()
        decrypted_message = cipher.decrypt(message)
        for i in range(len(decrypted_message)):
            if decrypted_message[i:i+1] == b'|':
                next_hop = decrypted_message[0:i]
                next_message = decrypted_message[i+1:]
                break
        next_hop = str(next_hop, encoding='utf-8')
        next_hop = (MessageBase.remove_padding(next_hop)).split(':')

        return next_message, next_hop

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
        message_object.key_id = key_init_message.key_id

        # We know want to calculate B
        # Let's workout the ellipticCurve and the elliptic point
        elliptic_curve_coeffs = key_init_message.p.split(':')
        a = FiniteField(FiniteField.get_coeffs_from_int(int(elliptic_curve_coeffs[0])))
        b = FiniteField(FiniteField.get_coeffs_from_int(int(elliptic_curve_coeffs[1])))

        elliptic_point_coeffs = key_init_message.g.split(':')
        x = FiniteField(FiniteField.get_coeffs_from_int(int(elliptic_point_coeffs[0])))
        y = FiniteField(FiniteField.get_coeffs_from_int(int(elliptic_point_coeffs[1])))
        self.elliptic_curve = EllipticCurve(a, x, y)
        self.elliptic_curve.b = b
        self.elliptic_point = EllipticCurvePoint(x, y, self.elliptic_curve)

        A_coeffs = key_init_message.A.split(':')
        A_x = FiniteField(FiniteField.get_coeffs_from_int(int(A_coeffs[0])))
        A_y = FiniteField(FiniteField.get_coeffs_from_int(int(A_coeffs[1])))
        self.A = EllipticCurvePoint(A_x, A_y, self.elliptic_curve)

        n = randint(1000, 5000)
        self.B = n*self.elliptic_point

        # let's calculate the key use to cipher
        self.C = n*self.A

        # Debug
        print('C Value')
        print(self.C)
        message_object.B = self.B.get_byte_string_from_coeffs()
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

        # relay_message = message_shell.decode(message)
        decrypted_message, next_hop = self.decrypt(message[8:])

        message_object = Object()
        message_object.version = 1
        message_object.key_id = 'id'
        message_object.message = decrypted_message
        new_message = MessageFactory.get_message(
            'MESSAGE_RELAY', message_object
        )

        next_hop_host = next_hop[0]
        next_hop_port = int(next_hop[1])
        payload = new_message.encode()
        client = Client.Client(next_hop_host, next_hop_port)
        client.start_connection()
        print("is redirecting to the next hop: %i" % (next_hop_port))
        answer = client.send_message(payload)  # Waiting for an answer
        self.server.incoming_conn.send(answer)  # Anwering the incom connection
        client.close_connection() # closing the connection after respond

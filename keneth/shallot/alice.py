""" client class """
import sys
from random import *
sys.path.append("classes")
import Client
from MessageFactory import MessageFactory, Object
from EllipticCurve import EllipticCurve, EllipticCurvePoint, EllipticCurveNeutralEl
from FiniteField import FiniteField

KEY_MAP = dict()


def negociate_keys():
    """ Negociating the keys with all the nodes in the network """

    # Instead of hardocode has to be read from the topology file.
    nodes = [
        {'host': 'localhost', 'port': 5000, 'id': 1},
        {'host': 'localhost', 'port': 5001, 'id': 2},
        {'host': 'localhost', 'port': 5002, 'id': 3},
        {'host': 'localhost', 'port': 5003, 'id': 4},
        {'host': 'localhost', 'port': 5004, 'id': 5},
        {'host': 'localhost', 'port': 5005, 'id': 6},
        {'host': 'localhost', 'port': 5010, 'id': 7}
    ]
    # Do a loop for each relay and bob to negociate the keys
    for node in nodes:
        # start the connection
        conn = Client.Client(node['host'], node['port'])
        conn.start_connection()
        # negociate the key here
        message_object = Object()
        message_object.version = 1
        message_object.type = 1
        message_object.key_id = str(node['id'])

        # Let's generate a random x y and a coeff
        x = FiniteField([randint(0, 1) for i in range(7)])
        y = FiniteField([randint(0, 1) for i in range(7)])
        a = FiniteField([randint(0, 1) for i in range(7)])

        # let's define the elliptic curve
        curve = EllipticCurve(a, x, y)

        # Let's workout the coeff b of the elliptic curve
        curve.workout_b()

        # Let's find a point which belong to the elliptical curve
        while True:
            g = EllipticCurvePoint(x, y, curve)
            if type(g) is not EllipticCurveNeutralEl:
                break
        # Let's calculate the good A factor
        n = randint(1000, 5000)
        A = n*g

        # Let's build the KEY_MAP with every information about EllipticCurve

        # Let's turn the Array of bits into string in order to send it through the network
        a_str = str(int(FiniteField.get_byte_string_from_coeffs(a.coeffs), 2))
        b_str = str(int(FiniteField.get_byte_string_from_coeffs(curve.b.coeffs), 2))

        message_object.g = g.get_byte_string_from_coeffs()
        message_object.p = a_str + ':' + b_str
        message_object.A = A.get_byte_string_from_coeffs()

        key_init_message = MessageFactory.get_message(
            'KEY_INIT', message_object
        )
        key_reply = conn.send_message(key_init_message.encode())
        # receive the key here
        to_decode = MessageFactory.get_empty_message('KEY_REPLY')
        key_reply_message = to_decode.decode(key_reply)
        # Let's retrieve the key

        B_coeffs = key_reply_message.B.split(':')
        B_x = FiniteField(FiniteField.get_coeffs_from_int(int(B_coeffs[0])))
        B_y = FiniteField(FiniteField.get_coeffs_from_int(int(B_coeffs[1])))

        B = EllipticCurvePoint(B_x, B_y, curve)

        C = n*B
        KEY_MAP[node['id']] = {'A': A, 'g': g, 'n': n, 'curve': curve, 'C': C}

        print('Key_reply message')
        print(
            'type: %i, version: %i, key_id: %s, B:%s, C:%s' %
            (
                key_reply_message.type, key_reply_message.version,
                key_reply_message.key_id, key_reply_message.B, C
            )
        )
        host_id = node['host'] + ':' + str(node['port'])
        # close the connection
        conn.close_connection()
    print(" The keys have been negociated")


def random_dijkstra():
    """ calculate the random path """
    random_path = [
        {'host': 'localhost', 'port': 5000},
        {'host': 'localhost', 'port': 5001},
        {'host': 'localhost', 'port': 5002},
        {'host': 'localhost', 'port': 5003},
        {'host': 'localhost', 'port': 5004},
        {'host': 'localhost', 'port': 5005},
        {'host': 'localhost', 'port': 5006}
    ]
    random_path.append({'host': 'localhost', 'port': 5010})  # Bob
    return random_path


def encrypt(message):
    """ Encrypt the message using the node key """
    return message


def build_shallot(message):
    """ build the shallot """
    path = random_dijkstra()
    prev_message = None
    for node in reversed(path):
        if prev_message is None:
            message_object = Object()
            message_object.version = 1
            message_object.key_id = 'keyid'
            message_object.next_hop = encrypt(
                node['host'] + ':' + str(node['port'])
            )
            message_object.message = encrypt(message)
            final_message = MessageFactory.get_message(
                'MESSAGE_RELAY', message_object
            )
        else:
            message_object = Object()
            message_object.version = 1
            message_object.key_id = 'keyid'
            message_object.next_hop = encrypt(
                node['host'] + ':' + str(node['port'])
            )
            message_object.message = encrypt(prev_message)
            final_message = MessageFactory.get_message(
                'MESSAGE_RELAY', message_object
            )
        prev_message = final_message

    return prev_message, path


def send_message():
    """ send message to bob """
    # Instead of hardocode has to be read from the topology file.
    # alice = Client.Client("localhost", 5000)
    # alice.start_connection()
    message = input(" -> ")
    while message != 'q':
        shallot_message, path = build_shallot(message)
        alice = Client.Client(path[0]['host'], path[0]['port'])
        data = alice.send_message(shallot_message.encode())
        print('Received from server: %s' % (data))
        alice.close_connection()
        message = input(" -> ")
    # alice.close_connection()


def main():
    """ main execution """
    # negociate the keys
    negociate_keys()
    # send messages
    send_message()


if __name__ == "__main__":
    sys.exit(main())

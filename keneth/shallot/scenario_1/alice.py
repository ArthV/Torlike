""" client class """
import sys
sys.path.append("../classes/")
import Client
from MessageFactory import MessageFactory, MessageBase, Object

def negociate_keys():
    """ Negociating the keys with all the nodes in the network """

    # Instead of hardocode has to be read from the topology file.
    nodes = [
        {'host': 'localhost', 'port': 5000},
        {'host': 'localhost', 'port': 5001},
        {'host': 'localhost', 'port': 5002},
        {'host': 'localhost', 'port': 5003},
        {'host': 'localhost', 'port': 5004},
        {'host': 'localhost', 'port': 5005},
        {'host': 'localhost', 'port': 5010}
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
        message_object.key_id = 'a'
        message_object.g = 'test'
        message_object.p = 'test'
        message_object.A = 'test'
        key_init_message = MessageFactory.get_message(
            'KEY_INIT', message_object
        )
        key_reply = conn.send_message(key_init_message.encode())
        # receive the key here
        to_decode = MessageFactory.get_empty_message('KEY_REPLY')
        key_reply_message = to_decode.decode(key_reply)
        print('Key_reply message')
        print(
            'type: %i, version: %i, key_id: %s, B:%s' %
            (
                key_reply_message.type, key_reply_message.version,
                key_reply_message.key_id, key_reply_message.B
            )
        )
        # close the connection
        conn.close_connection()
    print(" The keys have been negociated")


def main():
    """ main execution """

    # negociate the keys
    negociate_keys()

    # Instead of hardocode has to be read from the topology file.
    alice = Client.Client("localhost", 5000)
    alice.start_connection()
    message = input(" -> ")
    while message != 'q':
        data = alice.send_message(message.encode())
        print('Received from server: %s' % (data))
        message = input(" -> ")
    alice.close_connection()


if __name__ == "__main__":
    sys.exit(main())

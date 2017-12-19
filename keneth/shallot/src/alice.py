""" client class """
import sys
sys.path.append("classes")
import Client
from MessageFactory import MessageFactory, Object
from Loader import Loader
from Dijkstra import Graph

Loader.load_topo_init()
KEY_MAP = dict()
MY_ADDRESS = Loader.get_my_address('alice')
BOB_ADDRESS = Loader.get_my_address('bob')
TOPOLOGY = Loader.HOSTS_TABLE


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
        host_id = node['host'] + ':' + str(node['port'])
        KEY_MAP.update({'host': host_id, 'key': key_reply_message.key_id})
        # close the connection
        conn.close_connection()
    print(" The keys have been negociated")


def random_dijkstra():
    """ calculate the random path """
    Graph.random_dijkstra(TOPOLOGY)
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
            message_object.message = encrypt(message)  # next hop
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
        # alice.socket.bind()
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

""" relay class """
from multiprocessing.dummy import Pool as ThreadPool
import sys
sys.path.append("../classes/")
import relay_class


def create_relay(listen_host, listen_port, forward_list):
    """ create relays """
    relay = relay_class.Relay(
        listen_host, listen_port, forward_list
    )
    relay.start_connection()


forward_list_1 = [
    {'foward_host': '127.0.0.1', 'foward_port': 5001},
    {'foward_host': '127.0.0.1', 'foward_port': 5002}
]
foward_list_2 = [
    {'foward_host': '127.0.0.1', 'foward_port': 5000},
    {'foward_host': '127.0.0.1', 'foward_port': 5003},
    {'foward_host': '127.0.0.1', 'foward_port': 5004}
]
forward_list_3 = [
    {'foward_host': '127.0.0.1', 'foward_port': 5000},
    {'foward_host': '127.0.0.1', 'foward_port': 5003},
    {'foward_host': '127.0.0.1', 'foward_port': 5005}
]
foward_list_4 = [
    {'foward_host': '127.0.0.1', 'foward_port': 5001},
    {'foward_host': '127.0.0.1', 'foward_port': 5002},
    {'foward_host': '127.0.0.1', 'foward_port': 5004},
    {'foward_host': '127.0.0.1', 'foward_port': 5005}
]
forward_list_5 = [
    {'foward_host': '127.0.0.1', 'foward_port': 5001},
    {'foward_host': '127.0.0.1', 'foward_port': 5003},
    {'foward_host': '127.0.0.1', 'foward_port': 5006},
]
foward_list_6 = [
    {'foward_host': '127.0.0.1', 'foward_port': 5002},
    {'foward_host': '127.0.0.1', 'foward_port': 5003},
    {'foward_host': '127.0.0.1', 'foward_port': 5006},
    {'foward_host': '127.0.0.1', 'foward_port': 5010}
]
foward_list_7 = [
    {'foward_host': '127.0.0.1', 'foward_port': 5004},
    {'foward_host': '127.0.0.1', 'foward_port': 5005},
    {'foward_host': '127.0.0.1', 'foward_port': 5010}
]
relay_list = [("127.0.0.1", 5000, forward_list_1),
              ("127.0.0.1", 5001, foward_list_2),
              ("127.0.0.1", 5002, forward_list_3),
              ("127.0.0.1", 5003, foward_list_4),
              ("127.0.0.1", 5004, forward_list_5),
              ("127.0.0.1", 5005, foward_list_6),
              ("127.0.0.1", 5006, foward_list_7)]

pool = ThreadPool(len(relay_list))
results = pool.starmap(create_relay, relay_list)
pool.close()
pool.join()

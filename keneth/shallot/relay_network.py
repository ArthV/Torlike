
from multiprocessing.dummy import Pool as ThreadPool
import sys
sys.path.append("classes")
import Relay


def create_relay(listen_host, listen_port, forward_list):
    """ create relays """
    relay = Relay.Relay(
        listen_host, listen_port, forward_list
    )
    relay.start_connection()


def read_topology():
    """ Read the whole topology from the file """

    forward_list_1 = [
        {'forward_host': 'localhost', 'forward_port': 5001},
        {'forward_host': 'localhost', 'forward_port': 5002},
        {'forward_host': 'localhost', 'forward_port': 5003}
    ]
    forward_list_2 = [
        {'forward_host': 'localhost', 'forward_port': 5004}
    ]
    forward_list_3 = [
        {'forward_host': 'localhost', 'forward_port': 5010}
    ]
    forward_list_4 = [
        {'forward_host': 'localhost', 'forward_port': 5005}
    ]
    forward_list_5 = [
        {'forward_host': 'localhost', 'forward_port': 5010}
    ]
    forward_list_6 = [
        {'forward_host': 'localhost', 'forward_port': 5010}
    ]
    relay_list = [
        ("localhost", 5000, forward_list_1),
        ("localhost", 5001, forward_list_2),
        ("localhost", 5002, forward_list_3),
        ("localhost", 5003, forward_list_4),
        ("localhost", 5004, forward_list_5),
        ("localhost", 5005, forward_list_6)
    ]

    return relay_list


def main():
    """ main execution """
    relay_list = read_topology()
    pool = ThreadPool(len(relay_list))
    pool.starmap(create_relay, relay_list)
    pool.close()
    pool.join()


if __name__ == "__main__":
    sys.exit(main())

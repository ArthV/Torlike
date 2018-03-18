""" relay class """
from multiprocessing.dummy import Pool as ThreadPool
import sys
sys.path.append("classes")
import Relay
from Loader import Loader


def create_relay(listen_host, listen_port, forward_list):
    """ create relays """
    relay = Relay.Relay(
        listen_host, listen_port, forward_list
    )
    relay.start_connection()


def read_topology():
    """ Read the whole topology from the file """

    Loader.load_topo_init()
    relay_list = []

    for key, node in Loader.HOSTS_TABLE.items():
        if 'relay' in node['name'].lower():
            neighbors = []
            for neighbor in node['neighbors']:
                host, port = neighbor.split(':')
                neighbors.append({'forward_host': host, 'forward_port': port})
            relay_list.append((node['host'], node['port'], neighbors))
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

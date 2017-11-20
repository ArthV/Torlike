""" relay class """
from multiprocessing.dummy import Pool as ThreadPool
from classes import relay_class


def create_relay(listen_host, listen_port, foward_host, foward_port):
    """ create realys """
    relay = relay_class.Relay(
        listen_host, listen_port, foward_host, foward_port
    )
    relay.start_connection()
    relay.listen_and_foward()


# Create two threads as follows
relay_list = [("127.0.0.1", 5000, "127.0.0.1", 5001),
              ("127.0.0.1", 5001, "127.0.0.1", 5002),
              ("127.0.0.1", 5002, "127.0.0.1", 5003)]

ThreadPool().starmap(create_relay, relay_list)

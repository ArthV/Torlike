""" server class """
import sys
sys.path.append("classes")
import Server
from Loader import Loader


def main():
    """ main execution """
    host, port = Loader.get_my_address('bob')
    bob = Server.Server(host, port)
    bob.start_connection()


if __name__ == "__main__":
    sys.exit(main())

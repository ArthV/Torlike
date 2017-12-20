""" sys library """
import sys


class Loader:
    """ This is the class to read the different ini files. """
    HOST_INI = '../config/host.ini'
    TOPOLOGY_INIT = '../config/topology.ini'
    HOSTS_TABLE = dict()

    @staticmethod
    def load_host_init():
        """ This method receive a option parameter, based on the paremeter you
            will have the host ini or topology ini
            ----------
            host : string
                will load the host ini file.
            topology : int
                will load the topology file.
            Returns
            -------
            a dictionary with the infomration
        """
        host_ini_file = open(Loader.HOST_INI, 'r')

        i = 0
        bob_line = None
        while True:
            line = host_ini_file.readline().rstrip()
            if line == '':
                host, port = bob_line.split(' ')
                Loader.HOSTS_TABLE.update(
                    {
                        host + ':' + str(port): {
                            'name': 'bob', 'host': host, 'port': int(port),
                            'id': i, 'neighbors': []
                        }
                    }
                )
                break
            if 'bob' in line.lower():
                # print('entra a bob')
                bob_line = host_ini_file.readline().rstrip()
                continue
            elif "alice" in line.lower():
                # print("entra alice")
                line = host_ini_file.readline().rstrip()
                host, port = line.split(' ')
                Loader.HOSTS_TABLE.update(
                    {
                        host + ':' + str(port): {
                            'name': 'alice', 'host': host, 'port': int(port),
                            'id': i, 'neighbors': []
                        }
                    }
                )
                i += 1
                continue
            elif "relays" in line.lower():
                continue
            host, port = line.split(' ')
            Loader.HOSTS_TABLE.update(
                {
                    host + ':' + str(port): {
                        'name': 'relay_' + str(i), 'host': host, 'port': int(port),
                        'id': i, 'neighbors': []
                    }
                }
            )
            i += 1

        # print(Loader.HOSTS_TABLE)

    @staticmethod
    def load_topo_init():
        """ topology file reading """
        Loader.load_host_init()
        topo_ini_file = open(Loader.TOPOLOGY_INIT, 'r')
        while True:
            line = topo_ini_file.readline().rstrip()
            if line == '':
                break
            if 'topology' in line.lower():
                continue
            # do something with the topology
            neighbors = line.split(' ')
            host_port = neighbors[0]
            Loader.HOSTS_TABLE[host_port]['neighbors'] = neighbors[1:] # removing itself address
        # print(Loader.HOSTS_TABLE)

    @staticmethod
    def get_my_address(name):
        """ Get address by name """
        Loader.load_host_init()
        for key, value in Loader.HOSTS_TABLE.items():
            if value['name'] == name:
                return value['host'], value['port']


def main():
    """ main """
    Loader.load_host_init()


if __name__ == "__main__":
    sys.exit(main())

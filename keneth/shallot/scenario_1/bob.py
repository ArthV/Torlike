""" server class """
import sys
#sys.path.append("../classes/") 
import Server



def main():
    """ main execution """
    bob = Server.Server("localhost", 5010)
    bob.start_connection()


if __name__ == "__main__":
    print (sys.path)
    sys.exit(main())

""" client class """
import sys
sys.path.append("../classes/")
import client_class

alice = client_class.Client("127.0.0.1", 5000)
alice.start_connection()
message = input(" -> ")
while message != 'q':
    data = alice.send_message(message.encode())
    print('Received from server: %s' % (data))
    message = input(" -> ")
alice.close_connection()

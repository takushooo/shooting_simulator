from NetworkManager import NetworkManager
from time import sleep

if __name__ == '__main__' :
	nm = NetworkManager(NetworkManager.MODE_CLIENT_SERVER, NetworkManager.ROLL_CLIENT,'127.0.0.1', 50007)
	nm.client_open()
	nm.transmit_data(NetworkManager.DST_SERVER, "HELLO WORLD")


	while True:
		sleep(1)

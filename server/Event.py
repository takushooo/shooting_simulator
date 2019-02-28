# coding:utf-8

import pickle

class Event():
	
	SERVER_CLOSE = 0
	CLIENT_REQUEST_SHORT_ADDRESS = 4
	SERVER_SEND_SHORT_ADDRESS = 5
	PLAYER_DISCONNEC = 30

	CLIENT_ASSOCIATION_REQUEST = 10
	SERVER_ASSOCIATION_RESPONSE = 11
	CLIENT_SEND_GAMEDATA = 15
	SERVER_SEND_GAMEDATA = 20


	def __init__(self, dst, src, msg, payload):
		raw_data = {'dst':dst, 'src': src, 'msg': msg, 'payload': payload}
		self.pickled_data = pickle.dumps(raw_data)

	@staticmethod
	def unpickle(pickled_data):
		return pickle.loads(pickled_data)

if __name__ == '__main__':
	print('test')
# coding:utf-8

import socket
import threading
from const import MAX_USER
from time import sleep
from Event import Event

class NetworkManager():

	MODE_CLIENT_SERVER = 0
	MODE_P2P = 1

	ROLL_SERVER = 0
	ROLL_CLIENT = 1

	DST_ALL = -10
	DST_SERVER = 0

	def __init__(self, mode, roll, server_ip, port):
		self.mode = mode
		self.roll = roll
		self.server_ip = server_ip
		self.port = port
		self.connection_list = [] #辞書 (接続判定，コネクション，アドレス)
		self.receive_data_que = []
		self.server_info = {'empty':False, 'short_address': 0 ,'connection': None, 'ip_address': None}
		self.my_short_address = -1

		for i in range(MAX_USER): # サーバーのshort_addressは0
			dic = {'empty':True, 'short_address': i+1 ,'connection': None, 'ip_address': None}
			self.connection_list.append(dic)

		if self.roll == self.ROLL_SERVER:
			self.my_short_address = 0


	def transmit_data(self, dst, msg, payload=None ):
		raw_data = {'dst':dst, 'src': self.my_short_address, 'msg': msg, 'payload': payload}
		pickled_data = Event(dst, self.my_short_address, msg, payload).pickled_data

		if dst == self.DST_ALL:
			for c in self.connection_list:
				if not c['empty'] and c['short_address'] != self.my_short_address:
					c['connection'].send(pickled_data)
		elif dst == self.DST_SERVER:
			self.server_info['connection'].send(pickled_data)
		elif dst != self.my_short_address:
			conn = [x['connection'] for x in list if x['short_address'] == 'dst']
#			addr = [x['ip_address'] for x in list if x['short_address'] == 'dst']
			conn.send(pickled_data)


	def receive_data():
		ret =  self.receive_data_que.copy()
		self.receive_data_que.clear()
		return ret


	def server_open(self):
		# AF = IPv4 という意味
		# TCP/IP の場合は、SOCK_STREAM を使う
		server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		# IPアドレスとポートを指定
		server_socket.bind((self.server_ip, self.port))
		# 8ユーザーまで接続を許可
		server_socket.listen(MAX_USER*2)
		# スレッドでクライアント待ち受け処理を走らせる
		thread = threading.Thread(target=self.server_listen_therad, args=(server_socket,), daemon=True)
		thread.start()


	def server_listen_therad(self, server_socket):
		server_socket.listen(MAX_USER)
		# connection するまで待つ
		while True:
			try:	
				# 誰かがアクセスしてきたら、コネクションとアドレスを入れる
				conn, addr = server_socket.accept()
			except KeyboardInterrupt:
				break
			# アドレス確認
			print(f'[Connect]{addr}')
			# ショートアドレスを割り当てて，クライアントを記録する
			client_info = ''
			for c in self.connection_list:
				if c['empty']:
					c['ip_address'] = addr
					c['connection'] = conn
					c['empty'] = False
					client_info = c
					break
			print(client_info['connection'])
			# 受信処理を行うスレッド作成
			thread = threading.Thread(target=self.server_recieve_thread, args=(client_info,), daemon=True)
			thread.start()


	def server_close(self):
		self.transmit_data(DST_ALL, EVENT.SERVER_CLOSE)
		sleep(1)
		for c in self.connection_list:
			if not c['empty'] and c['short_address'] != self.my_short_address:
				self.disconnect_client(c)

	def server_disconnect_client(self, client_info):
		print(f'[Disconnect]{client_info["ip_address"]}')
		client_info['connection'].close()
		client_info['empty'] = True


	def client_open(self):
		print('Connecting server...')
		# クライアントソケット作成(IPv4, TCP)
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			# サーバソケットへ接続しに行く(サーバのホスト名, ポート番号)
			s.connect((self.server_ip, self.port))
			self.server_info['connection'] = s
			print('Connected')
			# 受信処理を行うスレッド作成
			thread = threading.Thread(target=self.client_recive_thread, daemon=True)
			thread.start()
		except ConnectionRefusedError:
			# 接続先のソケットサーバが立ち上がっていない場合、
			# 接続拒否になることが多い
			print('Connecting request is rejected')
			# P2Pなら自分が基準器(ホスト)になる処理

	def server_recieve_thread(self, client_info):
		short_addr = client_info['short_address']
		conn = client_info['connection']
		addr = client_info['ip_address']
		while True:
			try:
				# クライアントからデータを受け取る
				pickled_data = conn.recv(10240)
			except ConnectionRasetError:
				# クライアント側でプログラムを強制終了させた場合
				self.server_disconnect_client(client_info)
				break

			if not pickled_data:
				# データがない場合接続を切る
				self.server_disconnect_client(client_info)
				break
			else:
				raw_data = Event.unpickle(pickled_data)
				self.receive_data_que.append(raw_data)
				


	def client_recive_thread(self):
		client_socket = self.server_info['connection']
		while True:
			try:
				# サーバーからから送信されたメッセージを 1024 バイトずつ受信
				pickled_data = client_socket.recv(10240)
				print(pickled_data)
				raw_data = Event.unpickle(pickled_data)
				self.receive_data_que.append(raw_data)

			except ConnectionRefusedError:
				print('ConnectionRefusedError')
				# 接続先のソケットサーバが立ち上がっていない場合、
				# 接続拒否になることが多い
				break
			except ConnectionResetError:
				print('ConnectionResetError')



if __name__ == '__main__' :
	nm = NetworkManager(NetworkManager.MODE_CLIENT_SERVER, NetworkManager.ROLL_SERVER,'127.0.0.1', 50007)
	nm.server_open()

	while True:
		sleep(1)



import tkinter as tk
import math
from ClientModel import ClientModel
from BulletManager import BulletManager
from const import FPS, VIEW_FPS, FIELD_WIDTH, FIELD_HEIGHT
import socket
import threading
import pickle

class GameServer:
	def __init__(self):
		self.host = '127.0.0.1'
		self.port = 50007
		self.clients = []
		self.player = 1 # 0はサーバー，1以降がクライアント

	def openServer(self):
		# AF = IPv4 という意味
		# TCP/IP の場合は、SOCK_STREAM を使う
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		# IPアドレスとポートを指定
		s.bind((self.host, self.port))
		# 8ユーザーまで接続を許可
		s.listen(10)
		# connection するまで待つ
		while True:
			try:	
				# 誰かがアクセスしてきたら、コネクションとアドレスを入れる
				conn, addr = s.accept()
			except KeyboardInterrupt:
				break
			# アドレス確認
			print(f'[Connect]{addr}')
			# クライアント追加
			self.clients.append((conn,addr))
			# スレッドでサーバー処理を走らせる
			thread = threading.Thread(target=self.handler, args=(conn, addr), daemon=True)
			thread.start()

	def closeServer(self, conn, addr):
		print(f'[Disconnect]{addr}')
		conn.close()
		self.clients.remove((conn,addr))

	def createData(self,msg='',id=0, data=None):
		raw_data = {'message':msg, 'id':id, 'data':data}
		return pickle.dumps(raw_data)

	def handler(self, conn, addr):
		while True:
			try:
				# クライアントからデータを受け取る
				pickled_data = conn.recv(1024)
			except ConnectionRasetError:
				# クライアント側でプログラムを強制終了させた場合
				self.closeServer(conn,addr)
				break
			
			if not pickled_data:
				# データがない場合接続を切る
				self.closeServer(conn,addr)
				break
			else:
				raw_data = pickle.loads(pickled_data)
				msg = raw_data['message']
				if msg == 'RequestAttend':
					response = self.createData('ResponseAttend', self.player)
					conn.sendto(response,addr)
					print(f'Send [ResponseAttend {self.player}]')
					self.player += 1
				if msg == 'SendGameData':
					gamedata = raw_data['data']
					print(f'id:{raw_data["id"]}, x:{gamedata[0]}, y:{gamedata[1]}')

					self.createData('ResponseAttend', self.player, )
					for client in self.clients:
					try:
						client[0].sendto(data,client[1])
					except ConnectionResetError:
						break
				#print('data : {}, addr: {}'.format(raw_data, addr))
#				#クライアントにデータを返す(b -> byte でないといけない)
#				for client in self.clients:
#					try:
#						client[0].sendto(data,client[1])
#					except ConnectionResetError:
#						break


if __name__ == '__main__' :
	server = GameServer()
	server.openServer()
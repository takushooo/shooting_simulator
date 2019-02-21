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
		self.server_id = 0

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

	def createData(self,msg='',dst_id=0, src_id=0, data=None):
		raw_data = {'message':msg, 'dst_id':dst_id, 'src_id':src_id, 'data':data}
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
				# サーバー宛のメッセージなら
				if raw_data['dst_id'] == 0:
					msg = raw_data['message']
					if msg == 'RequestAttend':
						# 参加リクエストへの返答ではデータはなし
						send_data = self.createData('ResponseAttend', self.player, self.server_id)
						conn.sendto(send_data,addr)
						print(f'Send [ResponseAttend {self.player}]')

						# 新規プレイヤーに対して初期値をあたえて，全員に参加を知らせる
						# このデータ形式はControllerの通信データ形式に沿ったもの
						#
						sendData = {}
						player_id = self.player
						x = 200
						y = 200
						point = 0
						state = 1
						sendData['player'] = (player_id, x, y, point, state)
						send_data = self.createData('NewPlayerAttend', self.server_id, self.server_id, sendData)
						# 新規プレイヤーの参加通知をブロードキャスト
						for client in self.clients:
							try:
								client[0].sendto(send_data,client[1])
							except ConnectionResetError:
								break

						# プレイヤーIDを1増やす
						#これだと無限に増えていってしまうため，使っていないIDを使うよう変更して
						self.player += 1

					if msg == 'SendGameData':
						gamedata = raw_data['data']
						print(gamedata)
#						print(f'id:{gamedata[0]}, x:{gamedata[1]}, y:{gamedata[2]}')

						# 各クライアントに送信
						# この前に当たり判定やらなんやら加え入れてデータを変更する
						send_data = self.createData('SendGameData', self.server_id, self.server_id, gamedata)
						for client in self.clients:
							try:
								client[0].sendto(send_data,client[1])
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
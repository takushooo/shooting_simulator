# coding:utf-8

import tkinter as tk
import math	
from const import FPS, VIEW_FPS, FIELD_WIDTH, FIELD_HEIGHT
import socket
import threading
import pickle
from ServerModel import ServerModel
from ServerView import ServerView
from time import sleep
import argparse


class Server:
	def __init__(self):
		self.host = '0.0.0.0'
		self.port = 50007
		self.clients = []
		self.player = 1 # 0はサーバー，1以降がクライアント
		self.server_id = 0
		self.model = ServerModel()

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

	def update(self):
		self.model.checkCollision()

	def handler(self, conn, addr):
		while True:
			try:
				# クライアントからデータを受け取る
				pickled_data = conn.recv(4024)
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
						direction = 0
						sendData['player'] = (player_id, x, y, point, state, direction)
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
						modeldata = raw_data['data']
						self.model.load_data(modeldata)
						gamedata =  self.model.dump_data(modeldata)
						#print(f'game{gamedata}')

						# 各クライアントに送信
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
	##############################
	#Read ArgOption
	#Override config setting in INI File
	##############################
	p = argparse.ArgumentParser()
	p.add_argument('-v', '--view',default=False,action='store_true',help='Show server view')

	config = {} #設定データは辞書で保持
	args = p.parse_args()
	if args.view :
		config['view'] = args.view
	else:
		config['view'] = False

	server = Server()
	thread = threading.Thread(target=server.openServer, daemon=False)
	thread.start()

	if config['view']:
		# ウィンドウを作成
		window = tk.Tk()
		view = ServerView(window, server.model.players, server.model.bullets)
	
	def update():
		server.update()
		view.update()
		# 1000/FPS_VIEW ミリ秒間隔で再実行
		window.after(int(1000//VIEW_FPS), update)

	if config['view']:
		update()
		window.mainloop()
	else:
		# sleepは秒単位
		sleep_time = 1/60
		while True:
			server.update()
			sleep(sleep_time)


# coding:utf-8

from KeyInput import KeyInput
from NetworkManager import NetworkManager as NM
from ClientView import ClientView
from ClientAction import ClientAction
from Player import Player
from Event import Event
from const import *
import argparse
import threading
import tkinter as tk
import math
from time import sleep


class Client:

	INIT_GAME = 10
	ASSOCIATING = 20
	GAME_MODE = 30

	def __init__(self, config, window) :
		# ゲーム内データの生成
		self.config = config
		self.window = window
		self.data = {}
		self.own_data = {}
		self.game_state = self.INIT_GAME

		# 各インスタンスの生成
		self.net = NM(NM.MODE_CLIENT_SERVER, NM.ROLL_CLIENT, '127.0.0.1', 50007)
		self.keyinput = KeyInput(self.window)
		self.action = ClientAction(self.keyinput)
		self.player = ''

#		self.model = Player(0,0,100,100,30,self.keyinput)

	def update(self):
		if self.game_state == self.INIT_GAME:
			thread = threading.Thread(target=self.net.client_open(), daemon=False)
			thread.start()
			self.game_state = self.ASSOCIATING
		elif self.game_state == self.ASSOCIATING:
			received_data = self.net.receive_data()
			# SERVER_ASSOCIATION_RESPONSE メッセージが受信できているならば
			if Event.SERVER_ASSOCIATION_RESPONSE in [d.get('msg') for d in received_data]:
				for r in received_data:
					if r['msg'] == Event.SERVER_ASSOCIATION_RESPONSE:
						self.player = Player(r['dst'])
						self.player.set_received_data(r['payload'])
						print(r['payload'])
						self.game_state = self.GAME_MODE
						break
			else:
				self.net.transmit_data(NM.DST_SERVER, Event.CLIENT_ASSOCIATION_REQUEST)
		elif self.game_state == self.GAME_MODE:
			received_data = self.net.receive_data()
			self.update_model(received_data)
					
		else:
			print(f'[LOG] Invelid state happened: {self.game_state}')


	def check_transmit_data(self, data):
		if 'move_flag' not in data: exit()

	def update_model(self, received_data):
		# アップデート順番は大事
		self.keyinput.update()
		for r in received_data:
			self.player.set_received_data(r['payload'])
		transmit_data = self.action.update()
		self.check_transmit_data(transmit_data)
		transmit_data['player_id'] = self.player.player_id # あえてActionの外でつける(いたずら阻止)
		self.net.transmit_data(NM.DST_SERVER, Event.CLIENT_SEND_GAMEDATA, transmit_data)

	def update_view(self):
		self.view.update()
		# 1000/FPS_VIEW ミリ秒間隔で再実行
		self.window.after(int(1000//VIEW_FPS), self.update_view)
'''
		tmp_player_id = self.nc.player_id
		if self.config['manual']:
			self.keyinput = KeyInput(self.window)
		else:
			# オートモード
			self.keyinput = AutoKeyInput(self.window, tmp_player_id, self.data)
		# Neworkコントローラで設定された初期値を渡す(*でタプル展開)
		self.cm = ClientModel(self.window, self.keyinput, *(self.nc.selfdata))
		self.bm = BulletManager(self.window)
		self.init_data()
		# ビューの生成

		# 最初の1回(update内で再帰的にupdateが呼ばれてループとなる)
'''
		# モデルとビューは更新頻度(TickRate, FPS)が異なるので別々に呼ぶ
#		self.update_view()
#		self.window.mainloop()


if __name__ == '__main__' :
	##############################
	#Read ArgOption
	#Override config setting in INI File
	##############################
	p = argparse.ArgumentParser()
	p.add_argument('-m', '--manual',default=False,action='store_true',help='Change control mode manual')
	p.add_argument('-ud','--uplinkdelay',help='Uplink delay: Set uplink delay [ms]')
	p.add_argument('-dd','--downlinkdelay',help='Downlink delay: Set downlink delay [ms]')

	config = {} #設定データは辞書で保持
	args = p.parse_args()
	if args.manual :
		config['manual'] = args.manual
	else:
		config['manual'] = False
	if args.uplinkdelay :
		config['uplinkdelay'] = float(args.uplinkdelay)
	else:
		config['uplinkdelay'] = 0.0
	if args.downlinkdelay :
		config['downlinkdelay'] = float(args.downlinkdelay)
	else:
		config['downlinkdelay'] = 0.0


	window = tk.Tk()
	game = Client(config, window)
	view = ClientView(window, game.data, 0,game.config)



	def update():
		game.update()
		view.update()
		# 1000/FPS_VIEW ミリ秒間隔で再実行
		window.after(int(1000//FPS), update)

	update()
	window.mainloop()


#	def game_update(game):
#		sleep_time = 1/FPS
#		while True:
#			game.update_model()
#			sleep(sleep_time)
#			game.update_model()

	
#	thread = threading.Thread(target=game_update, args=(game,), daemon=False)
#	thread.start()



	

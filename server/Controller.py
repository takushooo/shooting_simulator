# coding:utf-8

import tkinter as tk
import math
from KeyInput import KeyInput
from ClientModel import ClientModel
from View import View
from BulletManager import BulletManager
from AutoKeyInput import AutoKeyInput
from NetworkClient import NetworkClient
from const import FPS, VIEW_FPS, FIELD_WIDTH, FIELD_HEIGHT
import pickle
import argparse
from threading import Timer

# init多すぎなので分けたい

class Controller:
	def __init__(self, config) :
		# ゲーム内データの生成
	    self.config = config
	    self.data = {}
	    # ウィンドウオブジェクトを作成
	    self.window = tk.Tk()

	    # 各インスタンスの生成
	    self.nc = NetworkClient()
	    print(f'[DEBUG] selfData: {self.nc.selfdata}')
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
	    self.view = View(self.window, self.data, self.cm.id, self.config)
	    # 最初の1回(update内で再帰的にupdateが呼ばれてループとなる)
	    # モデルとビューは更新頻度(TickRate, FPS)が異なるので別々に呼ぶ
	    self.update_model()
	    self.update_view()
	    self.window.mainloop()


	def init_data(self):
		self.data[f'bullets{self.cm.id}'] = {}
		self.data[f'player{self.cm.id}'] = {}
		self.data[f'player{self.cm.id}']['id'] = self.cm.id
		self.data[f'player{self.cm.id}']['x'] = self.cm.x
		self.data[f'player{self.cm.id}']['y'] = self.cm.y
		self.data[f'player{self.cm.id}']['point'] = self.cm.point
		self.data[f'player{self.cm.id}']['state'] = self.cm.state


	def create_packet(self):
		# プレイヤーと弾丸の情報をタプルにして送信する
		# タプルの構成を変更した場合，Serverの初期値設定の項目も変更すること
		sendData = {}
		sendData['player'] = (self.cm.id, self.cm.x, self.cm.y, self.cm.point, self.cm.state)

		sendData['bullets_id'] = self.cm.id
		sendData['bullets'] = []
		for b in self.bm.bulletList:
			bullet = (b.x, b.y, b.v, b.radian)
			sendData['bullets'].append(bullet)

		

		return sendData


	def set_sendData(self, sendData):
		self.nc.send_data(sendData)


	def set_recievedlData(self, receiveData):
		gamedata = receiveData
		for i in range(20):
			# gamedataのキーにplayer{i}が存在しているなら
			if f'player{i}' in gamedata:
				player_data = gamedata[f'player{i}']
				# 新規プレイヤーなら辞書を追加
				if f'player{i}' not in self.data:
					self.data[f'player{i}'] = {}
				self.data[f'player{i}']['id'] = player_data[0]
				self.data[f'player{i}']['point'] = player_data[3]
				self.data[f'player{i}']['state'] = player_data[4]
				# 自分の座標データはクライアントのものを用いるので更新しない（敵の情報だけ更新）
				if i != self.cm.id:
					self.data[f'player{i}']['x'] = player_data[1]
					self.data[f'player{i}']['y'] = player_data[2]

		for i in range(20):
			# 弾丸も同様に設定
			if f'bullets{i}' in gamedata and i != self.cm.id:
				# 一旦消して再設定する
				self.data[f'bullets{i}'] = []
				for b in gamedata[f'bullets{i}']:
					bullet = {'id': i, 'x': b[0],'y': b[1], 'v': b[2], 'radian': b[3]}
					self.data[f'bullets{i}'].append(bullet)

				self.cm.point = self.data[f'player{self.cm.id}']['point']



	def update_model(self):
		# アップデート順番は大事
		self.keyinput.update()
		self.cm.update()
		self.bm.update()

		# モデルデータの更新
		# ここで扱っているのは描画に必要な情報のみ
		# 内部モデルClientModel(cm)には触れない
		recieveData = self.nc.update().copy() #帰り値が辞書型なのでコピーをとっておく
		# ネットワークの下り遅延 ミリ秒指定
		if self.config['downlinkdelay'] > 0:
			timer = Timer(self.config['downlinkdelay']/1000, self.set_recievedlData, (recieveData, ))
			timer.start()
		else:
			self.set_recievedlData(recieveData)

		# ネットワークの上り遅延 ミリ秒指定
		sendData = self.create_packet()
		if self.config['uplinkdelay'] > 0:
			timer = Timer(self.config['uplinkdelay']/1000, self.set_sendData, (sendData, ))
			timer.start()
		else:
			self.set_sendData(sendData)
		
		######
		# 自プレイヤーの位置はと弾はクライアントのものを使って描画する
		#self.data[f'player{self.cm.id}'] = {}
		#self.data[f'player{self.cm.id}']['id'] = self.cm.id
		self.data[f'player{self.cm.id}']['x'] = self.cm.x
		self.data[f'player{self.cm.id}']['y'] = self.cm.y
		#self.data[f'player{self.cm.id}']['point'] = self.cm.point
		#self.data[f'player{self.cm.id}']['state'] = self.cm.state
		# 弾も同様
		self.data[f'bullets{self.cm.id}'] = []
		for b in self.bm.bulletList:
			bullet = {'id': self.cm.id, 'x':b.x ,'y': b.y, 'v': b.v, 'radian': b.radian}
			self.data[f'bullets{self.cm.id}'].append(bullet)


		# 1000/FPS ミリ秒間隔で再実行
		self.window.after(int(1000//FPS), self.update_model)

	def update_view(self):
		self.view.update()
		# 1000/FPS_VIEW ミリ秒間隔で再実行
		self.window.after(int(1000//VIEW_FPS), self.update_view)

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

	geme = Controller(config)
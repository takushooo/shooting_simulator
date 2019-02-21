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

class Controller:
	def __init__(self, flag) :
		# ウィンドウを作成
	    self.window = tk.Tk()
	    self.window.resizable(width=False, height=False)
	    self.window.title('Shooting Simulator - Jkawe')

#	    self.autoButton = 

	    # 描画領域を作成
	    self.canvas = tk.Canvas(self.window, width=FIELD_WIDTH, height=FIELD_HEIGHT)
	    self.nc = NetworkClient()
	    print(self.nc.selfdata)
	    tmp_player_id = self.nc.player_id

	    if flag == True :
	    	self.keyinput = KeyInput(self.window)
	    else:
	    	self.keyinput = AutoKeyInput(self.window, tmp_player_id)
	    
	    # Neworkコントローラで設定された初期値を渡す(*でタプル展開)
	    self.cm = ClientModel(self.window, self.keyinput, *(self.nc.selfdata))
	    self.bm = BulletManager(self.window)

	    self.data = {}
	    self.init_data()
	    #canvasを渡すことに注意．詳しくはView.py
	    self.view = View(self.canvas, self.data)

	    # 最初の1回(update内で再帰的にupdateが呼ばれてループとなる)
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


	def update_model(self):
		# アップデート順番は大事
		self.keyinput.update(self.data)
		self.cm.update()
		self.bm.update()

		# ネットワークデータの更新
		# ここで扱っているのは描画に必要な情報のみ
		# 内部モデルには触れない
		gamedata = self.nc.update()
		for i in range(20):
			# gamedataのキーにplayer{i}が存在していたら
			if f'player{i}' in gamedata:
				plalyer_data = gamedata[f'player{i}']
				self.data[f'player{i}'] = {}
				self.data[f'player{i}']['id'] = plalyer_data[0]
				self.data[f'player{i}']['x'] = plalyer_data[1]
				self.data[f'player{i}']['y'] = plalyer_data[2]
				self.data[f'player{i}']['point'] = plalyer_data[3]
				self.data[f'player{i}']['state'] = plalyer_data[4]
		
		for i in range(20):
			# 弾丸も同様に設定
			if f'bullets{i}' in gamedata:
				# 一旦消して再設定する
				self.data[f'bullets{i}'] = []
				for b in gamedata[f'bullets{i}']:
					bullet = {'id': i, 'x': b[0],'y': b[1], 'v': b[2], 'radian': b[3]}
					self.data[f'bullets{i}'].append(bullet)


		# 自分の位置だけはクライアントのものを使って描画する
		self.data[f'player{self.cm.id}'] = {}
		self.data[f'player{self.cm.id}']['id'] = self.cm.id
		self.data[f'player{self.cm.id}']['x'] = self.cm.x
		self.data[f'player{self.cm.id}']['y'] = self.cm.y
		self.data[f'player{self.cm.id}']['point'] = self.cm.point
		self.data[f'player{self.cm.id}']['state'] = self.cm.state

		# 弾も同様に自分のものはクライアントの情報を使って描画する
		self.data[f'bullets{self.cm.id}'] = []
		for b in self.bm.bulletList:
			bullet = {'id': self.cm.id, 'x':b.x ,'y': b.y, 'v': b.v, 'radian': b.radian}
			self.data[f'bullets{self.cm.id}'].append(bullet)
		
		# プレイヤーと弾丸の情報をタプルにして送信する
		# タプルの構成を変更した場合，Serverの初期値設定の項目も変更すること
		sendData = {}
		sendData['player'] = (self.data[f'player{self.cm.id}']['id'], self.data[f'player{self.cm.id}']['x'], self.data[f'player{self.cm.id}']['y']
			, self.data[f'player{self.cm.id}']['point'] , self.data[f'player{self.cm.id}']['state'])

		sendData['bullets_id'] = self.cm.id
		sendData['bullets'] = []
		for b in self.bm.bulletList:
			bullet = (b.x, b.y, b.v, b.radian)
			sendData[f'bullets'].append(bullet)
		self.nc.send_data(sendData)

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
#	p.add_argument("--roundSpeed",help="Phase shift value using roundrobin")
	p.add_argument("--manual",default=False,action="store_true")

	args = p.parse_args()
#	if args.roundSpeed :
#	    roundSpeed = int(args.roundSpeed)


	geme = Controller(args.manual)
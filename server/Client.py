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

class Controller:
	def __init__(self) :
		# ウィンドウを作成
	    self.window = tk.Tk()
	    self.window.resizable(width=False, height=False)
	    # 描画領域を作成
	    self.canvas = tk.Canvas(self.window, width=FIELD_WIDTH, height=FIELD_HEIGHT)
	    self.nc = NetworkClient()
	    player_id = self.nc.player_id

#	    self.keyinput = KeyInput(self.window)
	    self.keyinput = AutoKeyInput(self.window)
	    self.cm = ClientModel(self.window, self.keyinput, 0, 200, 200)	    #canvasを渡すことに注意．詳しくはView.py
	    self.bm = BulletManager(self.window)

	    self.data = {}
	    self.init_data()
	    self.view = View(self.canvas, self.data)

	    # 最初の1回(update内で再帰的にupdateが呼ばれてループとなる)
	    self.update_model()
	    self.update_view()
	    self.window.mainloop()

	def init_data(self):
		self.data['id'] = self.cm.id # idは不変
		self.data['x'] = self.cm.x
		self.data['y'] = self.cm.y


	def update_model(self):
		# アップデート順番は大事
		self.keyinput.update()
		self.cm.update()
		self.bm.update()

		# data辞書の更新
		self.data['x'] = self.cm.x
		self.data['y'] = self.cm.y
		self.data['bullets'] = self.bm.bulletList

		data = (self.data['x'], self.data['y'])
		self.nc.send_data(data)

		# 1000/FPS ミリ秒間隔で再実行
		self.window.after(int(1000//FPS), self.update_model)

	def update_view(self):
		self.view.update()
		# 1000/FPS_VIEW ミリ秒間隔で再実行
		self.window.after(int(1000//VIEW_FPS), self.update_view)

if __name__ == '__main__' :
	geme = Controller()
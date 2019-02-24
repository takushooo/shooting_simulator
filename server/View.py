# coding:utf-8

import tkinter as tk
from const import FIELD_HEIGHT, FIELD_WIDTH, PLAYER_SIZE, PLAYER_COLORS, BACKGROUND_COLOR, BULLET_SIZE, BULLET_COLORS, LISTBOX_WIDTH

class View:
	def __init__(self, window, data, player_id, config):
		# ウィンドウの設定
		self.window = window
		self.player_id = player_id
		self.config = config
		self.data = data
		
		self.window.resizable(width=False, height=False)
		self.window.title(f'Shooting Simulator - Player {player_id}')
		self.window.geometry(f'{FIELD_WIDTH + LISTBOX_WIDTH}x{FIELD_HEIGHT}')
		# 描画領域を作成
		self.canvas = tk.Canvas(self.window, width=FIELD_WIDTH, height=FIELD_HEIGHT)
		self.canvas.create_rectangle(0, 0, FIELD_WIDTH, FIELD_HEIGHT, fill=BACKGROUND_COLOR)
		self.canvas.pack(side=tk.LEFT)
		# メッセージビュアーの設定
		self.player_log = tk.StringVar()
		self.message = tk.Message(self.window,textvariable=self.player_log, anchor=tk.N ,width=LISTBOX_WIDTH, justify=tk.LEFT)
		# self.player_log.set("Name ID\t\tDamage")
		self.message.pack(side=tk.LEFT) #左から詰めるオプション

		# プレイヤーの描写
		# oval(x1,y1,x2,y2) x1y1からx2y2の長方形内に収まる円を描く
		# プログラム内では円の中心に座標点を置くので微修正する

		for i in range(20):
			# gamedataのキーにplayer{i}が存在していたら
			if f'player{i}' in self.data:
				player = self.data[f'player{i}']
				self.canvas.create_oval(player['x']-PLAYER_SIZE//2, player['y']-PLAYER_SIZE//2, player['x']+PLAYER_SIZE//2, player['y']+PLAYER_SIZE//2, tag=f'player{player["id"]}',fill=PLAYER_COLORS[player["id"]])


	def update(self):
		# 一旦全て消す
		self.canvas.delete("all")
		self.canvas.create_rectangle(0, 0, FIELD_WIDTH, FIELD_HEIGHT, fill=BACKGROUND_COLOR)
#		self.canvas.delete(f'player{self.data["id"]}')
		self.player_update()
		self.bullet_update()
		self.message_update()

	def player_update(self):
		for i in range(20):
			# gamedataのキーにplayer{i}が存在していたら
			if f'player{i}' in self.data:
				player = self.data[f'player{i}']
				self.canvas.create_oval(player['x']-PLAYER_SIZE//2, player['y']-PLAYER_SIZE//2, player['x']+PLAYER_SIZE//2, player['y']+PLAYER_SIZE//2, tag=f'player{player["id"]}',fill=PLAYER_COLORS[player["id"]])

	def bullet_update(self):
		for i in range(20):
			# gamedataのキーにplayer{i}が存在していたら
			if f'bullets{i}' in self.data:
				for b in self.data[f'bullets{i}']:
					self.canvas.create_oval(b['x']-BULLET_SIZE//2, b['y']-BULLET_SIZE//2, b['x']+BULLET_SIZE//2, b['y']+BULLET_SIZE//2 ,fill=BULLET_COLORS[b["id"]])

	def message_update(self):
		textlist = []
		textlist.append(f'You are Player {self.player_id}({PLAYER_COLORS[self.player_id]})')
		textlist.append(f'Uplink Delay:\t{self.config["uplinkdelay"]} (ms)')
		textlist.append(f'Downlink Delay:\t{self.config["downlinkdelay"]} (ms)')
		textlist.append("--------------------")		
		textlist.append("Name\t\tDamage")
		for i in range(20):
			# gamedataのキーにplayer{i}が存在していたら
			if f'player{i}' in self.data:
				player = self.data[f'player{i}']
				textlist.append(f'Player {player["id"]}({PLAYER_COLORS[i]})\t{player["point"]}')

		self.player_log.set('\n'.join(textlist))

if __name__ == '__main__' :
    print('test')

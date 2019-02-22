# coding:utf-8

import tkinter as tk
from const import FIELD_HEIGHT, FIELD_WIDTH, PLAYER_SIZE, PLAYER_COLORS, BACKGROUND_COLOR, BULLET_SIZE, BULLET_COLORS, LISTBOX_WIDTH, VIEW_FPS

class ServerView:
	def __init__(self, window, player_data, bullets_data):
		# ウィンドウの設定
		self.window = window
		self.window.resizable(width=False, height=False)
		self.window.title('Shooting Simulator - Server')
		self.window.geometry(f'{FIELD_WIDTH + LISTBOX_WIDTH}x{FIELD_HEIGHT}')
		# 描画領域を作成
		self.canvas = tk.Canvas(self.window, width=FIELD_WIDTH, height=FIELD_HEIGHT)
		self.canvas.create_rectangle(0, 0, FIELD_WIDTH, FIELD_HEIGHT, fill=BACKGROUND_COLOR)
		self.canvas.pack(side=tk.LEFT)
		self.player_data = player_data
		self.bullets_data = bullets_data

		self.player_log = tk.StringVar()
		self.message = tk.Message(self.window,textvariable=self.player_log, anchor=tk.N ,width=LISTBOX_WIDTH, justify=tk.LEFT)
		self.player_log.set("Name ID\t  Damage")
		self.message.pack(side=tk.LEFT) #左から詰めるオプション
		

		# プレイヤーの描写
		# oval(x1,y1,x2,y2) x1y1からx2y2の長方形内に収まる円を描く
		# プログラム内では円の中心に座標点を置くので微修正する

		for i in range(20):
			# gamedataのキーにplayer{i}が存在していたら
			if f'player{i}' in self.player_data:
				player = self.player_data[f'player{i}']
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
			if f'player{i}' in self.player_data:
				player = self.player_data[f'player{i}']
				self.canvas.create_oval(player['x']-PLAYER_SIZE//2, player['y']-PLAYER_SIZE//2, player['x']+PLAYER_SIZE//2, player['y']+PLAYER_SIZE//2, tag=f'player{player["id"]}',fill=PLAYER_COLORS[player["id"]])

	def bullet_update(self):
		for b in self.bullets_data:
			self.canvas.create_oval(b['x']-BULLET_SIZE//2, b['y']-BULLET_SIZE//2, b['x']+BULLET_SIZE//2, b['y']+BULLET_SIZE//2 ,fill=BULLET_COLORS[b["id"]])

	def message_update(self):
		textlist = ["Name\t  Damage"]
		for i in range(20):
			# gamedataのキーにplayer{i}が存在していたら
			if f'player{i}' in self.player_data:
				player = self.player_data[f'player{i}']
				textlist.append(f'Player {player["id"]}\t  {player["point"]}')

		self.player_log.set('\n'.join(textlist))

if __name__ == '__main__' :
    print('test')
    geme = Controller()
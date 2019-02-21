import tkinter as tk
from const import FIELD_HEIGHT, FIELD_WIDTH, PLAYER_SIZE, PLAYER_COLORS, BACKGROUND_COLOR, BULLET_SIZE, BULLET_COLORS

class View:
	def __init__(self, canvas, data):
		# 描画しかしないのでcanvasだけでよい
		# windowオブジェクトはイベントの割り当てなどに必要だが描画クラスでは使わない
		self.canvas = canvas
		self.canvas.create_rectangle(0, 0, FIELD_WIDTH, FIELD_HEIGHT, fill=BACKGROUND_COLOR)
		self.canvas.pack()
		self.data = data

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

	def player_update(self):
		for i in range(20):
			# gamedataのキーにplayer{i}が存在していたら
			if f'player{i}' in self.data:
				player = self.data[f'player{i}']
				self.canvas.create_oval(player['x']-PLAYER_SIZE//2, player['y']-PLAYER_SIZE//2, player['x']+PLAYER_SIZE//2, player['y']+PLAYER_SIZE//2, tag=f'player{player["id"]}',fill=PLAYER_COLORS[player["id"]])

	def bullet_update(self):
		for b in self.data['bullets']:
			self.canvas.create_oval(b.x-BULLET_SIZE//2, b.y-BULLET_SIZE//2, b.x+BULLET_SIZE//2, b.y+BULLET_SIZE//2 ,fill=BULLET_COLORS)


if __name__ == '__main__' :
    print('test')

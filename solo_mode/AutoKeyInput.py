import tkinter as tk
from const import KEY_UP, KEY_DOWN, KEY_RIGHT, KEY_LEFT, KEY_SHOT, CPU_MOVE
import random
# 使い方

class AutoKeyInput:
	# ウィンドウオブジェクトにキー入力のイベントを設定
	def __init__(self, window):
		self.window = window
		self.keyList = [KEY_UP, KEY_DOWN, KEY_RIGHT, KEY_LEFT, KEY_SHOT]
		self.pressStatus = {}
		self.pressTime = {}
		self.mouseX = 0
		self.mouseY = 0
		self.moveTimer = 0

		for key in self.keyList:
			self.pressStatus[key] = False
			self.pressTime[key] = 0


	def mouse(self):
			# マウスは常に他の敵の位置にする
			self.mouseX = event.x
			self.mouseY = event.y

	def auto(self):
		# ショットキーは常に押しっぱなし
		self.pressStatus[KEY_SHOT] = True
		# 移動タイマーが0未満なら移動方向を変える
		if self.moveTimer < 0 :
			#一旦入力をOFFに
			for key in self.keyList:
				self.pressStatus[key] = False

			#方向を8方向からランダムで決定
			while True:
				# 0-3の乱数を生成
				direct1 = random.randrange(0,4)
				# 0-1の乱数を生成
				if random.randrange(0,2) == 0:
					# 50%の確率で上下左右移動，direct1のキーをONに
					self.pressStatus[self.keyList[direct1]] = True
					break
				else:
					# 50%の確率で斜め移動，0-3の乱数を生成
					direct2 = random.randrange(0,4)
					if direct1 != direct2:
						self.pressStatus[self.keyList[direct1]] = True
						self.pressStatus[self.keyList[direct2]] = True
						break
			#移動時間を決定
			#平均CPU_MOVE，標準偏差CPU_MOVE/5のガウス分布に従う
			self.moveTimer = int(random.gauss(CPU_MOVE, CPU_MOVE/5))
		
		else:
			#moveTimerがまだ残っているなら
			self.moveTimer -= 1

	# アップデート関数，メインループ内で呼び出し必須
	def update(self):
		self.auto()
		for key in self.keyList:
			if self.pressStatus[key] == True: 
				self.pressTime[key] += 1
			else:
				self.pressTime[key] = 0


if __name__ == '__main__' :
	window = tk.Tk()
	window.resizable(width=False, height=False)
	canvas = tk.Canvas(window, width=400, height=400)
	canvas.create_rectangle(0, 0, 400, 400, fill='black')
	canvas.pack()
	keyinput = AutoKeyInput(window)	
	def update():
		# 1000/FPS ミリ秒間隔で実行
		window.after(int(1000//30), update)
		keyinput.update()
		# キーデバッグ
		for key in keyinput.keyList:
			pressTime = keyinput.pressTime[key]
			if pressTime > 0:
				print(f'{key} press {pressTime} ms')

	update() # 最初の1回(	update内で再帰的にupdateが呼ばれてループとなる)
	window.mainloop()
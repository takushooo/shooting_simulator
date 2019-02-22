# coding:utf-8

import tkinter as tk
from const import KEY_UP, KEY_DOWN, KEY_RIGHT, KEY_LEFT, KEY_SHOT

# 使い方
# ウィンドウオブジェクト(tkinter.Tk()で取得)を与えてインスタンス化
# 各KEYは押され続けているチックタイムを所持
# if INPUT_KEY.up > 0 で押されているかどうかを判定
class KeyInput:
	# ウィンドウオブジェクトにキー入力のイベントを設定
	def __init__(self, window):
		self.window = window
		self.keyList = [KEY_UP, KEY_DOWN, KEY_RIGHT, KEY_LEFT, KEY_SHOT]
		self.pressStatus = {}
		self.pressTime = {}
		self.mouseX = 0
		self.mouseY = 0

		for key in self.keyList:
			self.pressStatus[key] = False
			self.pressTime[key] = 0

		self.setBindings()

		
	def setBindings(self):
		# 各KEYのイベントをウィンドウオブジェクトにバインド
		for char in self.keyList:
			self.window.bind(f'<KeyPress-{char}>', self.pressed)
			self.window.bind(f'<KeyRelease-{char}>', self.released)
		self.window.bind('<Motion>', self.mouse)

	def mouse(self,event):
			self.mouseX = event.x
			self.mouseY = event.y

	def pressed(self, event):
		self.pressStatus[event.keysym] = True

	def released(self, event):
		self.pressStatus[event.keysym] = False
		
	# アップデート関数，メインループ内で呼び出し必須
	def update(self,gamedata=None):
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
	keyinput = KeyInput(window)	
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
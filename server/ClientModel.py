import tkinter as tk
import math
import KeyInput
from const import KEY_UP, KEY_DOWN, KEY_RIGHT, KEY_LEFT, KEY_SHOT, FIELD_HEIGHT, FIELD_WIDTH, PLAYER_VELOCITY, SHOOT_COOLTIME


class ClientModel:
	# プレイヤーの生成に必要な情報
	# ID：プレイヤー固有のID，0から始まる．ホストやサーバーが決定する
	# x,y：プレイヤーの初期位置
	def __init__(self, window, keyinput, id, x, y, point, state, direction):
		self.window = window
		self.id = id
		self.x = x
		self.y = y
		self.keyinput = keyinput
		self.point = point  # 得点
		self.state = state # 状態
		self.direction = direction
		self.cooltime = 0

	# return theta
	def mouseDirection(self):
		return math.atan2(self.keyinput.mouseY - self.y, self.keyinput.mouseX - self.x)

	def update(self):
		self.move()
		self.shoot()
		self.direction = self.mouseDirection()

	def shoot(self):
		if self.keyinput.pressTime[KEY_SHOT] > 0:
			if self.cooltime > SHOOT_COOLTIME:
				# マウスが向いている方向の角度を取得
				theta = self.mouseDirection()
				theta_count = int(theta/(2*math.pi/10000))

				# <ShotBullet>のイベントを生成する，ユーザーID，発射方向を追加で載せる
				# state,x,y,timeの本来の使いみちは違うが苦肉の策として使用する（誰かイベントハンドラ自作して）
				# このイベントはBulletManagerで受理される		
				# state: プレイヤーID
				# x, y: プレイヤーの座標 
				# time: 発射方向(tan/(2pi/10000))
	 			# 仮想イベントは二重括弧でくくらないとエラーがでる
				self.window.event_generate('<<ShootBullet>>', state=self.id, x=self.x, y=self.y, time=theta_count)
				self.cooltime = 0
			else:
				self.cooltime += 1


	def move(self):
		# 斜め移動に対応するために，移動差分を求めてから移動をおこなう
		# d = difference
		dx = 0.0
		dy = 0.0
		if self.keyinput.pressTime[KEY_UP] > 0:
			dy += -1
		if self.keyinput.pressTime[KEY_DOWN] > 0:
			dy += 1
		if self.keyinput.pressTime[KEY_RIGHT] > 0:
			dx += 1
		if self.keyinput.pressTime[KEY_LEFT] > 0:
			dx += -1

		# 斜め移動しているならルート2で割る
		if abs(dx+dy) > 1.0:
			dx = dx / math.sqrt(2)
			dy = dy / math.sqrt(2)

		# プレイヤーの移動速度をかけて，実際に移動させる
		self.x += PLAYER_VELOCITY * dx
		self.y += PLAYER_VELOCITY * dy

		# 壁を超えて反対側に来れるように調整
		self.x = (self.x + FIELD_WIDTH) % FIELD_WIDTH
		self.y = (self.y + FIELD_HEIGHT) % FIELD_HEIGHT

		# 壁を超えて進めないように処理
'''		if self.x > FIELD_WIDTH:
			self.x = FIELD_WIDTH
		if self.x < 0:
			self.x = 0
		if self.y > FIELD_HEIGHT:
			self.y = FIELD_HEIGHT
		if self.y < 0:
			self.y = 0'''
		



if __name__ == '__main__' :
	window = tk.Tk()
	window.resizable(width=False, height=False)
	canvas = tk.Canvas(window, width=400, height=400)
	canvas.create_rectangle(0, 0, 400, 400, fill='black')
	canvas.pack()
	keyinput = KeyInput(window)	
	def update():
		# 1000/FPS ミリ秒間隔で実行
		window.after(int(1000//FPS), update)
		keyinput.update()
		# キーデバッグ
		for key in keyinput.keyList:
			pressTime = keyinput.pressTime[key]
			if pressTime > 0:
				print(f'{key} press {pressTime} ms')

	update() # 最初の1回(	update内で再帰的にupdateが呼ばれてループとなる)
	window.mainloop()

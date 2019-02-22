# coding:utf-8

import tkinter as tk
import math
import KeyInput
from const import PLAYER_SIZE, BULLET_SIZE, BULLET_POINT


class ServerModel:
	# プレイヤーの生成に必要な情報
	# ID：プレイヤー固有のID，0から始まる．ホストやサーバーが決定する
	# x,y：プレイヤーの初期位置
	def __init__(self):
		self.players = {}
		self.bullets = []


#	def update(self, gamedata):
#		self.load_data(gamedata)
#		self.checkCollision()
#		return self.dump_data(gamedata)


	# raw_dataを打ち込むとモデルに格納する関数
	def load_data(self, data):
		player_data = data['player']
		bullets_data = data['bullets']
		player_id = data['bullets_id']

		# IDがリストになければ新規登録プレイヤー
		if f'player{player_id}' not in self.players.keys():
			self.players[f'player{player_id}'] = {}
			self.players[f'player{player_id}']['id'] = player_data[0]
			self.players[f'player{player_id}']['x'] = player_data[1]
			self.players[f'player{player_id}']['y'] = player_data[2]
			self.players[f'player{player_id}']['point'] = player_data[3]
			self.players[f'player{player_id}']['state'] = player_data[4]
		else:
			self.players[f'player{player_id}']['id'] = player_data[0]
			self.players[f'player{player_id}']['x'] = player_data[1]
			self.players[f'player{player_id}']['y'] = player_data[2]
			# pointとstateはサーバーのものを使用する
			# 普通のゲームでも同様だと思う．(本当はx.yもキー入力情報から求めたいが．．．)



		# 弾は該当するIDの弾を全て消してから再設定する
		# 弾はプレイやーと異なり，クライアント毎にラベルはつけない
		# bullet[:]とするとforループの中でremoveできる
		for b in self.bullets[:]:
			if b['id'] == player_id:
				self.bullets.remove(b)
				continue
		for b in bullets_data:
			bullet = {'id': player_id, 'x': b[0],'y': b[1], 'v': b[2], 'radian': b[3]}
			self.bullets.append(bullet)

	# loadの逆のことを行ってReturnする
	def dump_data(self,data):
		player_id = data['bullets_id']
		dump_data = {}
		dump_data['player'] = (self.players[f'player{player_id}']['id'], self.players[f'player{player_id}']['x'], self.players[f'player{player_id}']['y'], 
			self.players[f'player{player_id}']['point'], self.players[f'player{player_id}']['state'])

		dump_data['bullets_id'] = player_id
		dump_data['bullets'] = []
		for b in self.bullets:
			if b['id'] == player_id:
				bullet = (b['x'], b['y'], b['v'], b['radian'])
				dump_data['bullets'].append(bullet)
		return dump_data

	# 全てのプレイヤー，弾の組み合わせについて衝突判定
	def checkCollision(self):
		for player in self.players.values():
			for bullet in self.bullets[:]: #[:]することでforループの中でremoveできる
				# 自分で撃った弾にはあたらない
#				print(bullet)
				if player['id'] != bullet['id']:
					if self.checkBalletPlayerCollision(player, bullet):
						# 衝突処理
						player['point'] += BULLET_POINT
#						print(f'Player {player["id"]} is {player["point"]} damaged')
						# スレッドで実行しているのでなくなることがある
						# なくしたい
						if bullet in self.bullets:
							self.bullets.remove(bullet)
							continue

	# ある弾とあるプレイヤーが次１ステップのうちに衝突するかどうか
	# 弾のワープに対応するため，1ピクセルづつ動かして検証する（もっと頭いい方法あるはず）
	def checkBalletPlayerCollision(self, player, bullet):
		for i in range(int(bullet['v'])):
			#print(bullet['radian'])
			tmpx = bullet['x']+ math.cos(bullet['radian']) * i
			tmpy = bullet['y']+ math.sin(bullet['radian']) * i
			dist = math.sqrt(math.pow(player['x'] - tmpx, 2) + math.pow(player['y'] - tmpy, 2))
			if dist < (PLAYER_SIZE + BULLET_SIZE):
				return True
		return False


if __name__ == '__main__' :
	model = ServerModel()
	print("test")
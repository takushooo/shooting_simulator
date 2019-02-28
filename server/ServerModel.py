# coding:utf-8

import math
from Player import Player
from const import *



class ServerModel:

	def __init__(self):
		self.entire_data = {'players':[], 'bullets':[]}


	def set_init_data(self, new_player_data):
		self.entire_data['players'].append(new_player_data)

	def delete_player(self, player_id):
		players = [x for x in self.entire_data['players'] if x.player_id == player_id]
		player = players[0] if len(players) else ''
		if player != '':
			self.entire_data['players'].remove(player)

	def update_entire_data(self, received_data):
		players = [x for x in self.entire_data['players'] if x.player_id == received_data['player_id']]
		player = players[0] if len(players) else ''
		if player != '':
			player.update(received_data)
		else:
			print("[LOG] Invalid Player ID")
			exit()




#	def update(self, gamedata):
#		self.load_data(gamedata)
#		self.checkCollision()
#		return self.dump_data(gamedata)



'''
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
			#print(bullet['direction'])
			tmpx = bullet['x']+ math.cos(bullet['direction']) * i
			tmpy = bullet['y']+ math.sin(bullet['direction']) * i
			dist = math.sqrt(math.pow(player['x'] - tmpx, 2) + math.pow(player['y'] - tmpy, 2))
			if dist < (PLAYER_SIZE + BULLET_SIZE):
				return True
		return False
'''

if __name__ == '__main__' :
	model = ServerModel()
	print("test")
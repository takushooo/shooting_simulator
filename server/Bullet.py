# coding:utf-8
import math

class Bullet():
	STATUS_DEAD = 0
	STATUS_ALIVE = 10
	STATUS_NO_DAMAGE = 20
	STATUS_NO_COLLISION = 30
	STATUS_HIT = 40
	STATUS_CREATE = 50

	# player_id,  team_id: 弾を撃ったプレイヤー個人，チームのID
	# bullet_id: 弾のID
	# x,y,directionm,velocity: 弾の初期位置，方向(radian),速度
	# damage: 弾が当たった場合のダメージ
	# 
	def __init__(self, player_id, team_id, bullet_kind, bullet_id, x, y, direction, velocity, damage):
		self.player_id = player_id
		self.team_id = team_id
		self.bullet_kind = bullet_kind
		self.bullet_id = bullet_id
		self.x = x
		self.y = y
		self.velocity = velocity
		self.direction = direction
		self.point = point
		self.life_time = 0
		self.dx = math.cos(direction) * velocity
		self.dy = math.sin(direction) * velocity


		def update(self):
			self.x += self.dx
			self.y += self.dy
			self.life_time += 1


			if __name__ == '__main__':
				print('test')
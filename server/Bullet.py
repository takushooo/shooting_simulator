# coding:utf-8

import math

class Bullet():
    def __init__(self, player_id, id, x, y, direction, v, point):
        self.player_id = player_id
        self.id = id
        self.direction = direction
        self.point = point
        self.x = x
        self.y = y
        self.v = v
        self.dx = math.cos(direction) * v
        self.dy = math.sin(direction) * v

    def update(self):
        self.x += self.dx
        self.y += self.dy

if __name__ == '__main__':
    print('test')
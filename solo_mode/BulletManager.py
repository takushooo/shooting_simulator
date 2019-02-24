from const import BULLET_SIZE, BULLET_VELOCITY, BULLET_POINT, BULLET_COLORS, FIELD_WIDTH, FIELD_HEIGHT
import math
from Bullet import Bullet

class BulletManager():
    def __init__(self, window):
        self.window = window
        self.window.bind('<<ShootBullet>>', self.createBullet)
        self.bulletList = []
        self.id = 0

    def createBullet(self,event):
        # ClientModelから来たイベント
        # イベントで値を渡す苦肉の策として．．．
        # state: プレイヤーID
        # x, y: プレイヤーの座標 
        # time: 発射方向(tan/(2pi/10000))
        player_id = event.state
        x = event.x
        y = event.y
        theta = (2*math.pi/10000)*event.time
        newBullet = Bullet(player_id, self.id, x, y, theta, BULLET_VELOCITY, BULLET_POINT)
        self.bulletList.append(newBullet)

    def deleteBullet(self,bullet):
        self.bulletList.remove(bullet)


    def update(self):
        for b in self.bulletList:
            b.update()
            magin = 50
            if b.x < -magin or FIELD_WIDTH+magin < b.x or b.y < -magin or FIELD_HEIGHT+magin < b.y:
                self.deleteBullet(b)
                continue
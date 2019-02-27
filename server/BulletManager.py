# coding:utf-8
import math
import Bullet
from const import (BULLET_SIZE_NOMAL,
    FIELD_WIDTH,
    FIELD_HEIGHT,
    BULLET_VELOCITY_NOMAL,
    BULLET_VELOCITY_BOMB,
    BULLET_VELOCITY_GRANADE,
    BULLET_VELOCITY_SMOKE,
    BULLET_LIFE_NOMAL,
    BULLET_LIFE_BOMB,
    BULLET_LIFE_GRANADE,
    BULLET_LIFE_SMOKE,
    BULLET_COOLTIME_BOMB,
    BULLET_COOLTIME_GRANADE,
    BULLET_COOLTIME_SMOKE,
    BULLET_RELOADTIME_NOMAL,
    BULLET_RELOADTIME_BOMB,
    BULLET_RELOADTIME_GRAMANE,
    BULLET_RELOADTIME_SMAKE,
    BULLET_MAGAZINE_NOMAL,
    BULLET_MAGAZINE_BOMB,
    BULLET_MAGAZINE_GRANADE,
    BULLET_MAGAZINE_SMAKE,
    BULLET_DAMAGE_NOMAL,
    BULLET_SIZE_NOMAL)

class BulletManager():
    MAX_BULLET = 100000

    # ショットの種類
    BULLET_KIND_NOMAL = 0
    BULLET_KIND_BOMB = 10
    BULLET_KIND_GRENADE = 20
    BULLET_KIND_SMOKE = 30
    def __init__(self):
        self.bullet_list = []
        self.player_id = player_id
        self.setting_id = 0

        self.bullet_configurarion = {}
        self.bullet_configurarion[self.BULLET_KIND_NOMAL] = {'damage': BULLET_DAMAGE_NOMAL, 'velocity': BULLET_VELOCITY_NOMAL}
        self.bullet_configurarion[self.BULLET_KIND_BOMB] = {'damage': BULLET_DAMAGE_BOMB, 'velocity': BULLET_VELOCITY_BOMB}

    def createBullet(self, player_id, team_id, bullet_kind,  x, y, direction):
        self.setting_id = self.setting_id%MAX_BULLET
        new_bullet = Bullet(player_id, team_id, bullet_kind, bullet_id, x, y, direction, self.bullet_configurarion[bullet_kind]['velocity'], self.bullet_configurarion[bullet_kind]['damage'])
        self.bullet_list.append(new_bullet)
        self.setting_id += 1

    def deleteBullet(self,bullet):
        self.bullet_list.remove(bullet)

    def update(self):
        for b in self.bullet_list:
            b.update()
            magin = 50
            if b.x < -magin or FIELD_WIDTH+magin < b.x or b.y < -magin or FIELD_HEIGHT+magin < b.y:
                self.deleteBullet(b)
                continue


if __name__ == '__main__':
    print('test')
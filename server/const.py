# coding:utf-8
BASE_FPS = 30 # BASE_FPSを基準として移動体の速度を変化させる
FPS = 60
VIEW_FPS = 60
FIELD_HEIGHT = 300
FIELD_WIDTH = 300

KEY_UP = 'w'
KEY_DOWN = 's'
KEY_RIGHT = 'd'
KEY_LEFT = 'a'
KEY_SHOT = 'space'

PLAYER_SIZE = 20
# IDゼロ版はサーバーなので空にしておく
PLAYER_COLORS = ['', 'Red', 'Cyan', 'Lime', 'White', 'Coral', 'Gold', 'Thistle', 'Azure', 'Orange']
BACKGROUND_COLOR = 'black'
# 30 FPSを基本として1フレームあたりの速度を調整 
PLAYER_VELOCITY = 8 * (BASE_FPS/FPS) 
# ショットの間隔フレーム = FPS/1秒あたりのショットの連射数
SHOOT_COOLTIME = (FPS/10)  
BULLET_VELOCITY = 80 * (BASE_FPS/FPS) 
BULLET_POINT = 1
BULLET_SIZE = 6
BULLET_COLORS = ['', 'Red', 'Cyan', 'Lime', 'White', 'Coral', 'Gold', 'Thistle', 'Azure', 'Orange']

#CPUの移動フレーム頻度(平均n秒に1回) 30FPS基準
CPU_MOVE = FPS * 0.5

#リストボックスの高さはFIELD_HEIGHTと同じ
LISTBOX_WIDTH = 200

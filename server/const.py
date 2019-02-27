# coding:utf-8
BASE_FPS = 30 # BASE_FPSを基準として移動体の速度を変化させる
FPS = 60
VIEW_FPS = 60
FIELD_HEIGHT = 300
FIELD_WIDTH = 300
MAX_USER = 9

KEY_UP = 'w'
KEY_DOWN = 's'
KEY_RIGHT = 'd'
KEY_LEFT = 'a'
KEY_SHOT = 'space'
KEY_BOMB = 'b'
KEY_GRANADE = 'g'
KEY_SMAKE = 't'
KEY_LOOK_RIGHT = 'k'
KEY_LOOK_LEFT = 'j'


PLAYER_SIZE = 20
# IDゼロ版はサーバーなので空にしておく
PLAYER_COLORS = ['', 'Red', 'Cyan', 'Lime', 'White', 'Coral', 'Gold', 'Thistle', 'Azure', 'Orange']
BACKGROUND_COLOR = 'black'
# 30 FPSを基本として1フレームあたりの速度を調整 
PLAYER_VELOCITY = 8 * (BASE_FPS/FPS) 

BULLET_COLORS = ['', 'Red', 'Cyan', 'Lime', 'White', 'Coral', 'Gold', 'Thistle', 'Azure', 'Orange']
BULLET_LIFE_NOMAL = FPS * 30 #bullet の生存時間

BULLET_VELOCITY_NOMAL = 50 * (BASE_FPS/FPS)
BULLET_VELOCITY_BOMB = 16 * (BASE_FPS/FPS)
BULLET_VELOCITY_GRANADE = 25 * (BASE_FPS/FPS)
BULLET_VELOCITY_SMOKE = 25 * (BASE_FPS/FPS)

BULLET_LIFE_NOMAL = FPS * 5 # 通常のショットが消えるまでの時間
BULLET_LIFE_BOMB = FPS * 2 # ボムが消えるまでの時間
BULLET_LIFE_GRANADE = FPS * 2 # グレネードの爆発までの時間
BULLET_LIFE_SMOKE = FPS * 4 # スモークが消えるまでの時間

# ショットの間隔フレーム = FPS/1秒あたりのショットの連射数
BULLET_COOLTIME_NOMAL = (FPS/10)
BULLET_COOLTIME_BOMB = (FPS/1)
BULLET_COOLTIME_GRANADE = (FPS/0.5)
BULLET_COOLTIME_SMOKE = (FPS/0.5)

# ショットのリロード間隔
BULLET_RELOADTIME_NOMAL = FPS * 4
BULLET_RELOADTIME_BOMB = FPS * 5
BULLET_RELOADTIME_GRAMANE = FPS * 7
BULLET_RELOADTIME_SMAKE = FPS * 7

# ショットのリロード数
BULLET_MAGAZINE_NOMAL = 30
BULLET_MAGAZINE_BOMB = 3
BULLET_MAGAZINE_GRANADE = 2
BULLET_MAGAZINE_SMAKE = 2

# ショットのダメージ
BULLET_DAMAGE_NOMAL = 1

# ショットのサイズ
BULLET_SIZE_NOMAL = 6

#CPUの移動フレーム頻度(平均n秒に1回) 30FPS基準
CPU_MOVE = FPS * 0.5

#リストボックスの高さはFIELD_HEIGHTと同じ
LISTBOX_WIDTH = 200

# imageファイルのパス
BULLET_IMAGE_PATH = "../img/bullet.png"
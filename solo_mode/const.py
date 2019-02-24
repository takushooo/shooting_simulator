BASE_FPS = 30
FPS = 20
VIEW_FPS = 144
FIELD_HEIGHT = 400
FIELD_WIDTH = 400

KEY_UP = 'w'
KEY_DOWN = 's'
KEY_RIGHT = 'd'
KEY_LEFT = 'a'
KEY_SHOT = 'space'

PLAYER_SIZE = 20
PLAYER_COLORS = ['red', 'green', 'white', 'orange']
BACKGROUND_COLOR = 'black'
# 30 FPSを基本として1フレームあたりの速度を調整 
PLAYER_VELOCITY = 8 * (BASE_FPS/FPS) 
# ショットの間隔フレーム = FPS/1秒あたりのショットの連射数
SHOOT_COOLTIME = (FPS/5)  
BULLET_VELOCITY = 40
BULLET_POINT = 1
BULLET_SIZE = 6
BULLET_COLORS = 'yellow'

#WIDTH = 200
#HEIGHT = 200

#CPUの移動フレーム頻度(平均n秒に1回) 30FPS基準
CPU_MOVE = FPS * 0.5

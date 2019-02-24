# shooting_simulator
ネットワーク伝送路の遅延を実体験するための見下ろしシューティングシミュレータです．
- 実行環境： Python3.6以上

# 遊び方
## サーバー・クライアント方式
1. serverフォルダ内のServer.pyをサーバー機で実行する
2. serverフォルダ内のClient.pyをクライアント機で実行する．

## P2P方式
今後実装予定


# 実行オプション
## Client.py
- -h, -help: コマンドオプションの表示
- -dd [DELAYTIME], -downlinkdelay [DELAYTIME]: 下り回線の遅延(ミ秒指定)
- -ud [DELAYTIME], -uplinkdelay [DELAYTIME]: 上り回線の遅延(ミリ秒指定)
- -ip [IP_ADDRESS]: 接続先サーバーのIPアドレス設定
- -m, --manual: 手動操作モードで実行
-- 移動: WASD
-- 射撃: スペースで発射，マウスで方向指定
-- キーコンフィグは設定ファイル書き換えで可能

## Server.py
- -h, -help: コマンドオプションの表示
- -v, --view: サーバービューの表示

# 実行パラメータ(const.py)

## ゲーム関係
- BASE_FPS: ゲームの基準FPS (変更非推奨)
- FPS: ゲームの更新頻度，チックレート
- VIEW_FPS: 画面の更新頻度，リフレッシュレート
- FIELD_HEIGHT: ゲームフィールドの高さ
- FIELD_WIDTH: ゲームフィールドの幅
- BACKGROUND_COLOR: ゲーム背景の色
- LISTBOX_WIDTH: ログメッセージボックスの幅(高さはFIELD_HEIGHTと同じ)

## 操作関係
- KEY_UP: 上移動キー
- KEY_DOWN: 下移動キー
- KEY_RIGHT: 右移動キー
- KEY_LEFT: 左移動キー
- KEY_SHOT: ショットキー

## プレイヤー関係
- PLAYER_SIZE: プレイヤーの当たり判定サイズ（直径）
- PLAYER_COLORS: プレイヤーのカラー
- PLAYER_VELOCITY: BASE_FPSにおける１フレーム辺りのプレイヤー移動値 (BASE_FPSとFPSによって動的変動)
- CPU_MOVE = CPUプレイヤーの制御間隔 (秒)

## ショット関係
- SHOOT_COOLTIME: １秒間に打てる弾の数  
- BULLET_VELOCITY:  BASE_FPSにおける１フレーム辺りのショットの移動値 (BASE_FPSとFPSによって動的変動)
- BULLET_POINT: ショットのダメージ値
- BULLET_SIZE: ショットのサイズ(直径)
- BULLET_COLORS: ショットのカラー

# CPUの移動モデル
AutoKeyInput.pyを編集することで制御可能

## 移動モデル
### randomGaussWalk()
実装上もっとも簡単で見栄えがよい実装．解析には不向きかも
- 平均n秒，標準偏差n/4秒のガウス分布にしたがったランダム時間毎に移動方向を変更
- 移動方向は1/2の確率で十字方向に，2/6の確率で斜め方向に，1/6の確率で静止

## 射撃モデル
### centerShoot()
- その時点の敵の位置 (遅延に影響される情報)を常に射撃


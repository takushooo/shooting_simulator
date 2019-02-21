import socket
import threading
import random
import pickle

# ゲーム参加の流れ
# C -> S| RequestAttend: サーバーに参加要求
# S -> C| ResponseAtteend [宛先ID] [サーバーID(0)]: サーバーからの応答，プレイヤーIDが付与される

# S -> C| SendClientData [プレイヤーID] [データ]
# C -> S| SendServerData [プレイヤーID] [データ]


class NetworkClient():
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 50007
        self.socket = ''
        self.number = 1
        self.player_id = 0
        self.gamedata = {}
        self.selfdata  = None
        self.socket_client_up()


    def socket_client_up(self):
        print('Connecting server...')
        # クライアントソケット作成(IPv4, TCP)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            # サーバソケットへ接続しに行く(サーバのホスト名, ポート番号)
            self.socket.connect((self.host, self.port))
            print('Connected')
            # クライアントからメッセージを送る
            self.send_message(self.createData('RequestAttend', 0))
            while True:
                try:
                    # クライアントから送信されたメッセージを 1024 バイトずつ受信
                    pickled_data = self.socket.recv(1024)
                    raw_data = pickle.loads(pickled_data)
                    if raw_data['message'] == 'ResponseAttend':
                        self.player_id = int(raw_data['dst_id'])
                        print(f'Get PlayerID: {self.player_id}')

                    # 自分のプレイヤー情報をサーバーに初期化してもらう
                    if raw_data['message'] == 'NewPlayerAttend':
                        # (自分を含めて)新規参加がいたならば，プレイヤー情報を新規作成
                        player_data = raw_data['data']['player']
                        self.gamedata[f'player{player_data[0]}'] = player_data
                        # 自分の情報はselfdataにも格納しておく
                        if player_data[0] == self.player_id:
                            self.selfdata = player_data
                            break

                except ConnectionRefusedError:
                    print('ConnectionRefusedError')
                    # 接続先のソケットサーバが立ち上がっていない場合、
                    # 接続拒否になることが多い
                    break
                except ConnectionResetError:
                    print('ConnectionResetError')
                    break
            # スレッド作成
            thread = threading.Thread(target=self.handler, daemon=True)
            # スレッドスタート
            thread.start()

        except ConnectionRefusedError:
            # 接続先のソケットサーバが立ち上がっていない場合、
            # 接続拒否になることが多い
            print('Connecting request is rejected')
            # P2Pなら自分が基準器(ホスト)になる処理

    def createData(self,msg='',dst_id=0, src_id=0, data=None):
        raw_data = {'message':msg, 'dst_id':dst_id, 'src_id':src_id, 'data':data}
        return pickle.dumps(raw_data)

    # ゲーム情報をおくるための関数
    # GameMainで呼び出される
    def send_data(self,gamedata):
        msg = 'SendGameData'
        dst_id = 0 # サーバー宛
        src_id = self.player_id
        pickled_data = self.createData(msg, dst_id, src_id, gamedata)
        self.send_message(pickled_data)


    def send_message(self,pickled_data):
#        try:
            # メッセージ送信
        self.socket.send(pickled_data)
#        except ConnectionRefusedError:
            # 接続先のソケットサーバが立ち上がっていない場合、
            # 接続拒否になることが多い
#        except ConnectionResetError:

    def update(self):
        return self.gamedata

    def handler(self):
        while True:
            try:
                # クライアントから送信されたメッセージを 1024 バイトずつ受信
                pickled_data = self.socket.recv(1024)
                raw_data = pickle.loads(pickled_data)
                # SendDataはとりあえず受信する
                if raw_data['message'] == 'SendGameData':
                    # プレイヤー情報が含まれているならば
                    if 'player' in raw_data['data']:
                        player_data = raw_data['data']['player']
                        self.gamedata[f'player{player_data[0]}'] = player_data
                        # 自分の情報はselfdataにも格納しておく
                        if player_data[0] == self.player_id:
                            self.selfdata = player_data
                    # 弾丸情報が含まれているならば
                    if 'bullets' in raw_data['data']:
                        bullets_id = raw_data['data']['bullets_id']
                        bullets_data = raw_data['data']['bullets']
                        self.gamedata[f'bullets{bullets_id}'] = bullets_data

                if raw_data['message'] == 'NewPlayerAttend':
                    print(raw_data)
                    # (自分を含めて)新規参加がいたならば，プレイヤー情報を新規作成
                    player_data = raw_data['data']['player']
                    self.gamedata[f'player{player_data[0]}'] = player_data
                    # 自分の情報はselfdataにも格納しておく
                    if player_data[0] == self.player_id:
                        self.selfdata = player_datas


            except ConnectionRefusedError:
                # 接続先のソケットサーバが立ち上がっていない場合、
                # 接続拒否になることが多い
                break
            except ConnectionResetError:
                break


if __name__ == "__main__":
    sc = NetworkClient()
    # これだけだとメインスレッドが落ちるので，初期通信しかできない
    # ゲームと組み合わせれば問題ない
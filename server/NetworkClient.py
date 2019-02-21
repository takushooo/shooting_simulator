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
                    msg = raw_data['message']
                    if msg == 'ResponseAttend':
                        self.player_id = int(raw_data['dst_id'])
                        print(f'Get PlayerID: {self.player_id}')
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


    def handler(self):
        while True:
            try:
                # クライアントから送信されたメッセージを 1024 バイトずつ受信
                pickled_data = self.socket.recv(1024)
                raw_data = pickle.loads(pickled_data)
                print(raw_data)
                print(self.player_id)
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
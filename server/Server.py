# coding:utf-8

import tkinter as tk
import math	
from const import FPS, VIEW_FPS, FIELD_WIDTH, FIELD_HEIGHT
import threading
#from ServerModel import ServerModel
#from ServerView import ServerView
from time import sleep
import argparse
from NetworkManager import NetworkManager as NM
from ServerModel import ServerModel as SM
from ServerView import ServerView
from Player import Player
from Event import Event



if __name__ == '__main__' :
	##############################
	#Read ArgOption
	#Override config setting in INI File
	##############################
	p = argparse.ArgumentParser()
	p.add_argument('-v', '--view',default=False,action='store_true',help='Show server view')

	config = {} #設定データは辞書で保持
	args = p.parse_args()
	if args.view :
		config['view'] = args.view
	else:
		config['view'] = False

	net = NM(NM.MODE_CLIENT_SERVER, NM.ROLL_SERVER, '127.0.0.1', 50007)
	model = SM()

	thread = threading.Thread(target=net.server_open, daemon=False)
	thread.start()
	window = tk.Tk()
	view = ServerView(window, model.entire_data)


	def update():
		view.update()
		receive_data = net.receive_data()
		for r in receive_data:
			if r['msg'] == Event.CLIENT_ASSOCIATION_REQUEST:
				new_player_data = Player(r['src']) #リクエスト元のショートアドレスをプレイやIDにする
				model.set_init_data(new_player_data) # モデルデータの初期化
				transmit_data = new_player_data.dumps_player_data()
				net.transmit_data(r['src'], Event.SERVER_ASSOCIATION_RESPONSE, transmit_data)
			if r['msg'] == Event.CLIENT_SEND_GAMEDATA:
				model.update_entire_data(r['payload'])
		if len(net.disconnect_now) != 0: # 切断したクライアントがいるなら
			for player_id in net.disconnect_now[:]:
				model.delete_player(player_id)
				net.disconnect_now.remove(player_id)

		window.after(int(1000//FPS), update)

	
	update()
	window.mainloop()

#	sleep_time = 1/FPS
#	while True:
#		update()
#		sleep(sleep_time)


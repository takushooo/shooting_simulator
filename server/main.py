# coding:utf-8

from Controller import Controller
import argparse

if __name__ == '__main__' :
	##############################
	#Read ArgOption
	#Override config setting in INI File
	##############################
	p = argparse.ArgumentParser()
	p.add_argument('-m', '--manual',default=False,action='store_true',help='Change control mode manual')
	p.add_argument('-ud','--uplinkdelay',help='Uplink delay: Set uplink delay [ms]')
	p.add_argument('-dd','--downlinkdelay',help='Downlink delay: Set downlink delay [ms]')
	p.add_argument('-ip',help='IP address')

	config = {} #設定データは辞書で保持
	args = p.parse_args()
	if args.manual :
		config['manual'] = args.manual
	else:
		config['manual'] = False
	if args.uplinkdelay :
		config['uplinkdelay'] = float(args.uplinkdelay)
	else:
		config['uplinkdelay'] = 0.0
	if args.downlinkdelay :
		config['downlinkdelay'] = float(args.downlinkdelay)
	else:
		config['downlinkdelay'] = 0.0
	if args.ip :
		config['ip'] = str(args.ip)
	else:
		config['ip'] = 'localhost'

	geme = Controller(config)
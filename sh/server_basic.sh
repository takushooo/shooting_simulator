#!/bin/bash

echo 'Player 1: ud 0, dd, 0'
echo 'Player 2: ud 1000, dd, 0'
echo 'Player 3: ud 0, dd, 1000'
echo 'Player 4: ud 1000, dd, 1000'

python ../server/Client.py &
sleep 1
python ../server/Client.py -ud 2000 &
sleep 1
python ../server/Client.py -dd 2000 &
sleep 1
python ../server/Client.py -ud 2000 -dd 2000 &
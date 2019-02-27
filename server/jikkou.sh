echo 'Player 1: ud 0, dd, 0'
echo 'Player 2: ud 2000, dd, 0'
echo 'Player 3: ud 0, dd, 2000'
echo 'Player 4: ud 2000, dd, 2000'

python Client.py &
python Client.py -ud 2000 &
python Client.py -dd 2000 &
python Client.py -ud 2000 -dd 2000 &

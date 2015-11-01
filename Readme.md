[![Build Status](https://travis-ci.org/danieljabailey/GameStarter.svg)](https://travis-ci.org/danieljabailey/GameStarter)
[![Coverage Status](https://coveralls.io/repos/danieljabailey/GameStarter/badge.svg?branch=master)](https://coveralls.io/r/danieljabailey/GameStarter?branch=master)

To see a demo of the game start, clone, ensure py files are executable (`chmod +x *.py`) and then run `./gamestart.py`.

There are also some test cases that test that the class handles some simple invalid configurations correctly and that it can handle the various imperfections of the humans that want to start a game. Run the tests with `./gamestart_test.py`

To use this code:

- import it
```python
	from gamestart import GameStarter
```

- instantiate the `GameStarter` class
```python
	gs = GameStarter(max players, activation threshold, start threshold, grace time)
	#eg...
	gs = GameStarter(4, 2.0, 5.0, 0.5)
```

- then report whenever a player pushes or releases a button:
```python
	gs.push(0)	#report button push for first player
	gs.release(1)	#report button release for second player
```

- regularly update the internal timer at the desired resolution:
```python
	gs.timeStep(0.05) #Step 0.05 seconds, call this every 0.05 seconds (for example)
```

- then you can see if you have enough players ready like so:
```python
	if gs.shouldStart() : #we have enough players to start
```

- you can get an exact number with this:
```python
	gs.totalStartablePlayers()
```

- and you can loop through all players to see if each one is joining in:
```python
	for i in range(4):
		if gs.isStartablePlayer(i):
			#add player i to game
```


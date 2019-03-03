[![Build Status](https://travis-ci.org/danieljabailey/GameStarter.svg)](https://travis-ci.org/danieljabailey/GameStarter)
[![Coverage Status](https://coveralls.io/repos/danieljabailey/GameStarter/badge.svg?branch=master&service=github)](https://coveralls.io/r/danieljabailey/GameStarter?branch=master)

To see a demo of the game start, clone, then run `python3 -m GameStarter.gamestart`

There are also some test cases that test that the class handles some simple invalid configurations correctly and that it can handle the various imperfections of the humans that want to start a game. Run the tests with `python -m GameStarter.gamestart_test`

To use this code:

- import it
```python
	from GameStarter import GameStarter
```

- instantiate the `GameStarter` class
```python
	gs = GameStarter(total start delay, delay to join game, delay to leave game)
	#eg...
	gs = GameStarter(5.0, 2.0, 0.5)
```

- then report whenever a player pushes or releases a button:
```python
	gs.player(0).push()	#report button push for first player
	gs.player(1).release()	#report button release for second player
```

- regularly update the internal timer at the desired resolution:
```python
	gs.step_time(0.05) #Step 0.05 seconds, call this every 0.05 seconds (for example)
```

- then you can see if you have enough players ready like so:
```python
	if gs.should_start : #we have enough players to start
```

- you can determine which players have joined using:
```python
	gs.joined_players
```

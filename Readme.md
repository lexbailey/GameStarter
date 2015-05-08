To see a demo of the game start, clone, ensure py files are exacutable (`chmod +x *.py`) and then run `./gamestart.py`.

There are also some test cases that test that the class handles some simple invalid configurations correctly and that it can handle the various imperfections of the humans that want to start a game.

To use this code:

- import it
	from gamestart import GameStarter

- instantiate the `GameStarter` class
	gs = GameStarter(max players, activation threshold, start threshold)
	#eg...
	gs = GameStarter(4, 2.0, 5.0)

- then report whenever a player pushes or releases a button:
	gs.push(0)	#report button push for first player
	gs.release(1)	#report button release for second player

- regularly update the internal timer at the desired resolution:
	gs.timeStep(0.05) #Step 0.05 seconds, call this every 0.05 seconds (for example)

- then you can see if you have enough players ready like so:
	if gs.shouldStart() : #we have enough players to start

- you can get an exact number with this:
	gs.totalStartablePlayers()

- and you can loop throug all players to see if each one is joining in:
	for i in range(4):
		if gs.isStartablePlayer(i):
			#add player i to game

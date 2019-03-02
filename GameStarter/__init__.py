#!/usr/bin/env python

import sys
import time

class GamePlayer:

	#GamePlayer init
	def __init__(self, activeLevel, startLevel, graceLevel):
		#Store level boundaries
		self.activeLevel = activeLevel
		self.startLevel = startLevel
		self.graceLevel = graceLevel
		self.reset()

	def reset(self):
		#Start at 0 level
		self.level = 0.0
		#Assume button is not pushed
		self.pushed = False
		#Start inactive
		self.active = False

	#Take a time step, increment or decrement depending on button pushed state
	def timeStep(self, time):
		if time <= 0.0:
			raise Exception('Invalid time step')
		if self.pushed:
			# Button is pushed - increment the level, but not past startLevel
			self.level = min( self.level + time, self.startLevel )
			#Set active on the way up
			if self.level >= self.activeLevel:
				self.active = True
		if not self.pushed:
			# Button not pushed
			# Drop to graceLevel, so letting go takes effect quicker
			if self.level > self.graceLevel:
				self.level = self.graceLevel

			# Decrement level, but don't go beyond zero
			self.level = max( self.level - time, 0.0 )
			#Unset active on the way down
			if self.level <= 0.0:
				self.active = False

	#Get current state
	@property
	def state(self):
		# Computed state is quite simple
		if self.start:
			return 'START'
		elif self.active:
			return 'ACTIVE'
		elif self.wait:
			return 'WAIT'
		return 'OUT'

	@property
	def start(self):
		return (self.level >= self.startLevel)

	@property
	def wait(self):
		return (self.level > 0.0)

class GameStarter:

	#Initialise game starter
	def __init__(self, _unused_was_maxPlayers_, activeLevel, startLevel, graceLevel):
		activeLevel = float(activeLevel)
		startLevel = float(startLevel)
		graceLevel = float(graceLevel)
		#Raise error if startLevel or activeLevel is invalid
		if (activeLevel <= 0.0):
			raise Exception('activeLevel must be positive')
		if (activeLevel >= startLevel):
			raise Exception('activeLevel must be less than startLevel')

		self.resetAll()
		def newPlayer():
			return GamePlayer(activeLevel, startLevel, graceLevel)
		self.newPlayer = newPlayer

	def resetAll(self):
		self.players = {}

	#get total number of players in given state
	def totalInState(self, state):
		return len(self.playersInState(state))

	#Check if a player will be active in this game
	def isStartablePlayer(self, player_id):
		return self.players[player_id].active

	def playersInState(self, state):
		return [id for id, pl in self.players.items() if pl.state == state]

	#Get total number of startable players
	def totalStartablePlayers(self):
		return len(self.playersInState('START'))

	#Decide if a game is ready to start
	def shouldStart(self):
		#You should start if you have:
		# - at least two startable players
		# - at least one player who has reached the start state
		# - no players who have recently pressed (in)
		return (self.totalStartablePlayers() > 1) and (self.totalInState('START') > 0) and (self.totalInState('WAIT') == 0)

	def getPlayer(self, player_id):
		if player_id not in self.players:
			self.players[player_id] = self.newPlayer()
		return self.players[player_id]

	#Push the given player's button
	def push(self, player_id):
		self.getPlayer(player_id).pushed = True

	#Release the given player's button
	def release(self, player_id):
		self.getPlayer(player_id).pushed = False

	#Check if the given player's button is pressed
	def isPushed(self, player_id):
		self.getPlayer(player_id).pushed

	#Step all players by given time
	def timeStep(self, time):
		if (type(time) != float) or (time <= 0.0):
			raise Exception('GameStarter.timeStep: time step must be a positive float.')

		for pl in self.players.values():
			pl.timeStep(time)

	#Get the level of the given player
	def getLevel(self, playerID):
		return self.getPlayer(playerID).level

	#Get the state of the given player
	def getState(self, playerID):
		return self.getPlayer(playerID).state

def main():

	#Visual test of GameStarter

	#Set level thresholds here
	activeLevel = 2.0
	startLevel = 5.0
	graceLevel = 1.0

	#Bar scale is number of characters that represent one second on the visualisation
	barScale = 20

	#Some maths for the time bar graphics
	activeBar = int(activeLevel * barScale)
	startBar = int(startLevel * barScale)
	activeBarString = '-' * (activeBar-1) + '|'
	startBarString = '-' * (startBar-activeBar-1) + '|'

	#Get an instance of GameStarter with four players
	starter = GameStarter(4, activeLevel, startLevel, graceLevel)

	#Print header for graphics
	print('ID|' + activeBarString + startBarString)
	#Pad lines ready for cursor moving back
	for i in range(4):
		print('')

	#Begin with players two and four pressed
	starter.push(1)
	starter.push(3)
	start = False
	totTime = 0.0;
	while (not start):

		#Set specific times for events to happen here
		if totTime > 3.0:
			starter.release(1)
		if totTime > 5.2:
			starter.push(0)
		if totTime > 6.0:
			starter.push(1)
		if totTime > 6.4:
			starter.push(2)
		#End of event timings

		#Do time calculations
		time.sleep(0.05)
		starter.timeStep(0.05)
		totTime += 0.05
		#Decide if game can start
		start = starter.shouldStart()

		#Step back four lines
		sys.stdout.write("\x1B[4A")
		#Print graphs
		for i in range(4):
			thislevel = starter.getLevel(i)
			print("%d |%s%s %s %s" % (i, ("#" * int(thislevel*barScale)), (" " * (int(barScale*startLevel)-int(barScale*thislevel))), starter.getState(i), str(starter.isPushed(i)) + '   '))

	#When game should start, get number of players in, print IDs
	numPlayersIn = 0

	print("Ready to start. Players:")
	for i in range(4):
		if starter.isStartablePlayer(i):
			numPlayersIn = numPlayersIn +1
			print("\tPlayer %d" % i)

	print("Start game with %d players." % numPlayersIn)

if __name__ == '__main__':
	main()

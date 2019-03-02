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
	def __init__(self, maxPlayers, activeLevel, startLevel, graceLevel):
		#Raise error if number of players is too low
		if type(maxPlayers) != int:
			raise Exception('GameStarter.__init__: maxPlayers must be an integer greater than 2 (At least two players are required).')
		if maxPlayers < 2:
			raise Exception('GameStarter.__init__: maxPlayers must be an integer greater than 2 (At least two players are required). Attempted to init GameStarter with %d players.' % maxPlayers)
		#Raise error if startLevel or activeLevel is invalid
		if ((type(activeLevel) != float) or (type(startLevel) != float)):
			raise Exception('GameStarter.__init__: activeLevel must be a float greater than 0, startLevel must be a float greater than activeLevel.')
		if ((activeLevel <= 0.0) or (startLevel <= activeLevel)):
			raise Exception('GameStarter.__init__: activeLevel must be a float greater than 0, startLevel must be a float greater than activeLevel. (Active: %f, Start: %f)' % (activeLevel, startLevel))
		#Store maximum number of players
		self.maxPlayers = maxPlayers
		#Create this number of players
		self.players = [ GamePlayer(activeLevel, startLevel, graceLevel) for i in range(self.maxPlayers)]

	def resetAll(self):
		for pl in self.players:
			pl.reset()

	#get total number of players in given state
	def totalInState(self, state):
		return len(self.playersInState(state))

	#Check if a player will be active in this game
	def isStartablePlayer(self, player_id):
		return self.players[player_id].active

	def playersInState(self, state):
		return [id for id, pl in enumerate(self.players) if pl.state == state]

	#Get total number of startable players
	def totalStartablePlayers(self):
		return sum(1 for player in self.players if player.start)

	#Decide if a game is ready to start
	def shouldStart(self):
		#You should start if you have:
		# - at least two startable players
		# - at least one player who has reached the start state
		# - no players who have recently pressed (in)
		return (self.totalStartablePlayers() > 1) and (self.totalInState('START') > 0) and (self.totalInState('WAIT') == 0)

	
	#Push the given player's button
	def push(self, player_id):
		self.players[player_id].pushed = True

	#Release the given player's button
	def release(self, player_id):
		self.players[player_id].pushed = False

	#Check if the given player's button is pressed
	def isPushed(self, player_id):
		return self.players[player_id].pushed

	#Step all players by given time
	def timeStep(self, time):
		if (type(time) != float) or (time <= 0.0):
			raise Exception('GameStarter.timeStep: time step must be a positive float.')

		for i in range(self.maxPlayers):
			self.players[i].timeStep(time)

	#Get the level of the given player
	def getLevel(self, playerID):
		return self.players[playerID].level

	#Get the state of the given player
	def getState(self, playerID):
		return self.players[playerID].state

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
		







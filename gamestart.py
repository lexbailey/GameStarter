#!/usr/bin/env python

import sys
import time

class GamePlayer:
	
	#GamePlayer init
	def __init__(self, activeLevel, startLevel):
		#Store level boundaries
		self.activeLevel = activeLevel
		self.startLevel = startLevel
		#Start in the 'OUT' state
		self.state = 'OUT'
		#Start at 0 level
		self.level = 0.0
		#Assume button is not pushed
		self.pushed = False

	#inc, called when button is pushed and time is stepped
	def inc(self, time):
		if self.pushed:
			#Validate time
			if time <= 0.0:
				raise Exception('Invalid time step')
		
			#This is an increment, if we are out, get in
			if self.state == 'OUT':
				self.state = 'IN'

			#Increment the level
			self.level = self.level + time

			#Limit the level to the maximum level
			if self.level >= self.startLevel:
				self.level = self.startLevel

			#If we are in and we reach the active level, activate
			if self.state == 'IN' and self.level >= self.activeLevel:
				self.state = 'ACTIVE'

			#If we are active and reach the start level, start
			if self.state == 'ACTIVE' and self.level >= self.startLevel:
				self.state = 'START'

	#dec, called when button is pushed and time is stepped
	def dec(self, time):
		if not self.pushed:
			#Validate time
			if time <= 0.0:
				raise Exception('Invalid time step')

			#Decrement level
			self.level = self.level - time

			#If level reaches 0, drop out
			if self.level <= 0.0:
				self.level = 0.0 #min limit to 0
				self.state = 'OUT'

			#Anyone who had not reached active should drop out as soon as they release
			if (self.state == 'IN'):
				self.state = 'OUT'
				self.level = 0.0

			#Anyone who drops below active should drop out completely
			if (self.state == 'ACTIVE') and (self.level < self.activeLevel):
				self.state = 'OUT'
				self.level = 0.0

			
	#Take a time step, increment or decrement depending on button pushed state
	def timeStep(self, time):
		if self.pushed:
			#Button is pushed, increment
			self.inc(time)
		if not self.pushed:
			#Button not pushed, decrement
			self.dec(time)

	#Set button state to pushed
	def push(self):
		self.pushed = True
		
	#Set button state to not pushed
	def release(self):
		self.pushed = False

	#Get button state
	def isPushed(self):
		return self.pushed

	#Get current level
	def getLevel(self):
		return self.level

	#Get current state
	def getState(self):
		return self.state

class GameStarter:

	#Initialise game starter
	def __init__(self, maxPlayers, activeLevel, startLevel):
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
		self.players = [ GamePlayer(activeLevel, startLevel) for i in range(self.maxPlayers)]

	#get total number of players in given state
	def totalInState(self, state):
		tot = 0
		for i in range(self.maxPlayers):
			if self.players[i].getState() == state:
				tot = tot+1;
		return tot

	#Check if a player is able to start in this game
	def isStartablePlayer(self, player_id):
		#A player will join a game when it starts if they are in START or ACTIVE state and have their button pushed
		return ((self.getState(player_id) == 'START') or (self.getState(player_id) == 'ACTIVE')) and self.isPushed(player_id)

	#Get total number of startable players
	def totalStartablePlayers(self):
		total = 0
		for i in range(self.maxPlayers):
			if self.isStartablePlayer(i):
				total = total + 1
		return total

	#Decide if a game is ready to start
	def shouldStart(self):
		#You should start if you have:
		# - at least two startable players
		# - at least one player who has reached the start state
		# - no players who have recently pressed (in)
		return (self.totalStartablePlayers() > 1) and (self.totalInState('START') > 0) and (self.totalInState('IN') == 0)

	
	#Push the given player's button
	def push(self, player_id):
		self.players[player_id].push()

	#Release the given player's button
	def release(self, player_id):
		self.players[player_id].release()

	#Check if the given player's button is pressed
	def isPushed(self, player_id):
		return self.players[player_id].isPushed()

	#Step all players by given time
	def timeStep(self, time):
		if (type(time) != float) or (time <= 0.0):
			raise Exception('GameStarter.timeStep: time step must be a positive float.')

		for i in range(self.maxPlayers):
			self.players[i].timeStep(time)

	#Get the level of the given player
	def getLevel(self, playerID):
		return self.players[playerID].getLevel()

	#Get the state of the given player
	def getState(self, playerID):
		return self.players[playerID].getState()

if __name__ == '__main__':

	#Visual test of GameStarter

	#Set level thresholds here
	activeLevel = 2.0
	startLevel = 5.0

	#Bar scale is number of characters that represent one second on the visualisation
	barScale = 20

	#Some maths for the time bar graphics
	activeBar = int(activeLevel * barScale)
	startBar = int(startLevel * barScale)
	activeBarString = '-' * (activeBar-1) + '|'
	startBarString = '-' * (startBar-activeBar-1) + '|'

	#Get an instance of GameStarter with four players
	starter = GameStarter(4, activeLevel, startLevel)

	#Print header for graphics
	print 'ID|' + activeBarString + startBarString
	#Pad lines ready for cursor moving back
	for i in range(4):
		print '' 

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
			print "%d |%s%s %s %s" % (i, ("#" * int(thislevel*barScale)), (" " * (int(barScale*startLevel)-int(barScale*thislevel))), starter.getState(i), str(starter.isPushed(i)) + '   ')

	#When game should start, get number of players in, print IDs
	numPlayersIn = 0

	print "Ready to start. Players:"
	for i in range(4):
		if starter.isStartablePlayer(i):
			numPlayersIn = numPlayersIn +1
			print "\tPlayer %d" % i

	print "Start game with %d players." % numPlayersIn
		







#!/usr/bin/env python

import sys
import time

class GamePlayer:

	#GamePlayer init
	def __init__(self, join_delay, _unused_was_startLevel_, leave_delay):
		self.join_delay = float(join_delay)
		self.leave_delay = float(leave_delay)
		self.pushed = False
		self.joined = False
		self.delay = self.join_delay

	#Take a time step, increment or decrement depending on button pushed state
	def step_time(self, time):
		if time <= 0.0:
			raise Exception('Invalid time step')

		if self.pushed != self.joined:
			self.delay -= time
			if self.delay <= 0:
				self.joined = self.pushed

		if self.pushed == self.joined:
			self.delay = self.leave_delay if self.joined else self.join_delay

	@property
	def waiting(self):
		return False if self.pushed == self.joined else (self.delay > 0.0)

	def push(self):
		self.pushed = True

	def release(self):
		self.pushed = False

class GameStarter:

	#Initialise game starter
	def __init__(self, _unused_was_maxPlayers_, join_delay, total_start_delay, leave_delay):
		self.start_delay = float(total_start_delay) - float(join_delay) #FIXME Backward compatibility...
		self.reset()
		def newPlayer():
			return GamePlayer(join_delay, None, leave_delay)
		self.newPlayer = newPlayer

	def reset(self):
		self.players = {}
		self.delay = self.start_delay

	@property
	def joined_players(self):
		return [id for id, pl in self.players.items() if pl.joined]

	@property
	def waiting_players(self):
		return [id for id, pl in self.players.items() if pl.waiting]

	@property
	def counting(self):
		return len(self.joined_players) >= 2

	@property
	def ready(self):
		return self.delay <= 0

	@property
	def waiting(self):
		return len(self.waiting_players) > 0

	#Decide if a game is ready to start
	@property
	def should_start(self):
		#You should start if:
		# - the countdown has finished
		# - no players are waiting (holding the launch)
		return self.ready and not self.waiting

	def player(self, player_id):
		if player_id not in self.players:
			self.players[player_id] = self.newPlayer()
		return self.players[player_id]

	#Step all players by given time
	def step_time(self, time):
		time = float(time)
		if (time <= 0.0):
			raise Exception('time must be positive')

		for pl in self.players.values():
			pl.step_time(time)
		if(self.counting):
			self.delay -= time
		else:
			self.delay = self.start_delay

def main():

	#Visual test of GameStarter

	#Set level thresholds here
	activeLevel = 2.0
	startLevel = 5.0
	graceLevel = 1.0

	#Bar scale is number of characters that represent one second on the visualisation
	barScale = 60

	#Get an instance of GameStarter with four players
	starter = GameStarter(4, activeLevel, startLevel, graceLevel)

	#Print header for graphics
	print()
	print('ID|' + '-' * (barScale-1) + '|')
	#Pad lines ready for cursor moving back
	for i in range(4):
		print('')

	#Begin with players two and four pressed
	starter.player(1).push()
	starter.player(3).push()
	start = False
	totTime = 0.0;
	while (not start):

		#Set specific times for events to happen here
		if totTime > 3.0:
			starter.player(1).release()
		if totTime > 5.2:
			starter.player(0).push()
		if totTime > 6.0:
			starter.player(1).push()
		if totTime > 6.4:
			starter.player(2).push()
		#End of event timings

		#Do time calculations
		time.sleep(0.05)
		starter.step_time(0.05)
		totTime += 0.05
		#Decide if game can start
		start = starter.should_start

		#Step back four lines
		sys.stdout.write("\x1B[4A")
		#Print graphs
		for i in range(4):
			player = starter.player(i)
			level = (player.delay / player.leave_delay) if player.joined else (1.0 - player.delay / player.join_delay)
			bar_segs = int(barScale * level)
			format = ("%d |%-" + str(barScale) + "s %6s %8s")
			state = 'WAIT' if player.waiting else 'JOINED' if player.joined else 'OUT'
			pushed = 'PUSHED' if player.pushed else 'RELEASED'
			print(format % (i, "#" * bar_segs, state, pushed))

	print("Ready to start. Players:")
	for id in starter.joined_players:
		print("\tPlayer %d" % id)

	print("Start game with %d players." % len(starter.joined_players))

if __name__ == '__main__':
	main()

#!/usr/bin/env python

import unittest
import gamestart
from gamestart import GameStarter, GamePlayer

class TestStartButtons(unittest.TestCase):
	def setUp(self):
		pass

	def tearDown(self):
		pass

	def test_player_init(self):
		#Ensure that the player can be instantiated and does sensible things
		#Note that this class should only be instantiated by the GameStarter and so has less validity check on its inputs
		pl = GamePlayer(1.0, 2.0)
		self.assertEquals(0.0, pl.getLevel())
		self.assertEquals("OUT", pl.getState())
		self.assertEquals(False, pl.isPushed())

	def test_player_timing(self):
		#Ensure that the player can be instantiated and does sensible things
		#Note that this class should only be instantiated by the GameStarter and so has less validity check on its inputs
		pl = GamePlayer(1.0, 2.0)
		pl.timeStep(0.5)
		self.assertEquals("OUT", pl.getState())
		self.assertEquals(False, pl.isPushed())
		self.assertEquals(0.0, pl.getLevel())

		pl.push()
		self.assertEquals(True, pl.isPushed())

		pl.timeStep(0.51)
		self.assertEquals("WAIT", pl.getState())
		level = pl.getLevel()
		self.assertTrue((0.509<level) and (level < 0.511))

		pl.timeStep(0.5)
		self.assertEquals("ACTIVE", pl.getState())
		level = pl.getLevel()
		self.assertTrue((1.009<level) and (level < 1.011))

		pl.timeStep(1.0)
		self.assertEquals("START", pl.getState())
		level = pl.getLevel()
		self.assertTrue((1.99<level) and (level < 2.01))

	def test_player_invalid_time_step(self):
		pl = GamePlayer(1.0, 2.0)
		invalidTimes = [0, 0.0, -1, -1.0]
		for invalidTime in invalidTimes:
			pl.push()
			self.assertRaises(Exception, pl.timeStep, invalidTime)
			pl.release()
			self.assertRaises(Exception, pl.timeStep, invalidTime)

	def test_invalid_players(self):
		#It is invalid to have only one player. This should raise an exception. As should a negative number.
		invalidInputs = [1, 0, -1, None, False, True, "2", "foo"]
		for invalidInput in invalidInputs:
			try:
				gs = GameStarter(invalidInput, 1.0, 2.0)
				self.fail('Started with 1 player')
			except Exception as e:
				errorMsg = 'GameStarter.__init__: maxPlayers must be an integer greater than 2 (At least two players are required).'
				self.assertEqual(errorMsg, str(e)[0:len(errorMsg)])

	def test_invalid_levels(self):
		#It is invalid to have a negative active level threshold. This should raise an exception, as should invalid types.
		invalidInputs = [(-1.0, 2.0), (1.0, 0.5), (1.0, -23.0), (2, 1), (1, 0), (-3, -1), (None, None), (True, True), (False, True), ("1", "2")]
		for invalidInput in invalidInputs:
			try:
				gs = GameStarter(2, invalidInput[0], invalidInput[1])
				self.fail('Started with invalid levels')
			except Exception as e:
				errorMsg = 'GameStarter.__init__: activeLevel must be a float greater than 0, startLevel must be a float greater than activeLevel.'
				self.assertEqual(errorMsg, str(e)[0:len(errorMsg)])

	def test_invalid_time_step(self):
		#It is invalid to have a negative time step. This should raise an exception
		invalidInputs = [-1, -1.0, -99999, "foo", "-23", "34", "12.34", None, True, False]
		for invalidInput in invalidInputs:
			try:
				gs = GameStarter(2, 1.0, 2.0)
				gs.timeStep(invalidInput)
				self.fail('Invalid time step allowed')
			except Exception as e:
				errorMsg = 'GameStarter.timeStep: time step must be a positive float.'
				self.assertEqual(errorMsg, str(e)[0:len(errorMsg)])

	def test_total_state_zero(self):
		#totalInState should never raise an exception, it should always be 0 for an invalid input
		testInputs = ["foo", 1, 2, None, True, False]
		for testInput in testInputs:
			gs = GameStarter(2, 1.0, 2.0)
			self.assertEqual(0, gs.totalInState(testInput))

	def test_total_state_correct(self):
		testInputs = [2, 3, 4, 5, 6, 10, 999]
		for testInput in testInputs:
			gs = GameStarter(testInput, 1.0, 2.0)
			self.assertEqual(testInput, gs.totalInState("OUT"))

	def test_two_player_start(self):
		#test that two players can start a game
		try:
			gs = GameStarter(2, 1.0, 2.0)
		except Exception as e:
			self.fail('Exception during __init__')
		#Both players push
		gs.push(0)
		gs.push(1)
		#Wait for three seconds
		gs.timeStep(3.0)
		#By now, shouldStart must be true and there should be 2 startable players
		self.assertTrue(gs.shouldStart())
		self.assertEqual(2, gs.totalStartablePlayers())

	def test_single_player_cant_start(self):
		#test that single players cannot start a game
		try:
			gs = GameStarter(2, 1.0, 2.0)
		except Exception as e:
			self.fail('Exception during __init__')
		#One player pushes
		gs.push(0)
		#Wait for three seconds
		gs.timeStep(3.0)
		#shouldStart must be false
		self.assertFalse(gs.shouldStart())

	def test_player_can_drop_out(self):
		#test that a player can go below active and drop out of the round start
		try:
			gs = GameStarter(2, 1.0, 2.0)
		except Exception as e:
			self.fail('Exception during __init__')
		#One player pushes
		gs.push(0)
		#Wait for three seconds
		gs.timeStep(3.0)
		#player has peaked at 2 seconds, let go of the button
		gs.release(0)
		#1.5 seconds later and they should already be out
		gs.timeStep(1.5)
		self.assertEqual("OUT", gs.getState(0))
		self.assertEqual(0.0, gs.getLevel(0))


	def test_two_player_start_with_four_player_game(self):
		#test that two players can start a game
		try:
			gs = GameStarter(4, 1.0, 2.0)
		except Exception as e:
			self.fail('Exception during __init__')
		#Both players push
		gs.push(0)
		gs.push(1)
		#Wait for two seconds
		gs.timeStep(2.0)
		#By now, shouldStart must be true and there should be 2 startable players
		self.assertTrue(gs.shouldStart())
		self.assertEqual(2, gs.totalStartablePlayers())

	def test_button_spam_filtering(self):
		#test that two players can start a game even when someone is button spamming
		try:
			gs = GameStarter(4, 1.0, 2.0)
		except Exception as e:
			self.fail('Exception during __init__')
		#Both players push
		gs.push(0)
		gs.push(1)
		#Wait for 1.5 seconds (nearly there)
		gs.timeStep(1.5)
		#player three then spams
		gs.push(2)
		gs.timeStep(0.7)
		gs.release(2)
		gs.timeStep(0.5)
		#By now, shouldStart must be true and there should be 2 startable players
		self.assertTrue(gs.shouldStart())
		self.assertEqual(2, gs.totalStartablePlayers())
		#Do more buttom mashing to see if the filter still works after this
		gs.push(2)
		gs.timeStep(0.7)
		gs.release(2)
		gs.timeStep(0.5)
		gs.push(2)
		gs.timeStep(0.7)
		gs.release(2)
		gs.timeStep(0.5)
		#shouldStart must stil be true and there should still be 2 startable players
		self.assertTrue(gs.shouldStart())
		self.assertEqual(2, gs.totalStartablePlayers())

	def test_late_joiners(self):
		#test that for players can start a game even when some people take a while to join in
		try:
			gs = GameStarter(4, 1.0, 2.0)
		except Exception as e:
			self.fail('Exception during __init__')
		#One players pushes
		gs.push(0)
		#Wait for 3 seconds (player 1 fully ready)...
		gs.timeStep(3.0)
		#Player two joins in
		gs.push(1)
		#a little later...
		gs.timeStep(0.8)
		#player three then joins
		gs.push(2)
		#later still..
		gs.timeStep(0.7)
		#player four pushes too
		gs.push(3)
		#another two seconds...
		gs.timeStep(2.0)
		#and now, shouldStart must be true and there should be 4 startable players
		self.assertTrue(gs.shouldStart())
		self.assertEqual(4, gs.totalStartablePlayers())

	def test_dodgy_button(self):
		#test that a dodgy button that flickers on and off sometimes doesn't cause problems
		#this also simulates people who fail to keep their hand on the button persistently
		try:
			gs = GameStarter(2, 1.0, 20.0) #note 20 second start time on this one
		except Exception as e:
			self.fail('Exception during __init__')
		#Both players push
		gs.push(0)
		gs.push(1)
		#Wait for 1.5 seconds (nearly there)...
		gs.timeStep(1.5)
		#Player two goes dodgy
		gs.release(1)
		gs.timeStep(0.1)
		gs.push(1)
		gs.timeStep(0.3)
		gs.release(1)
		gs.timeStep(0.2)
		gs.push(1)
		gs.timeStep(0.7)
		gs.release(1)
		gs.timeStep(0.04)
		gs.push(1)
		gs.timeStep(10.8)
		gs.release(1)
		gs.timeStep(0.2)
		gs.push(1)
		gs.timeStep(0.7)
		gs.release(1)
		gs.timeStep(0.04)
		gs.push(1)
		gs.timeStep(20.0) #long one to make sure

		#shouldStart must be true and there should be 2 startable players
		self.assertTrue(gs.shouldStart())
		self.assertEqual(2, gs.totalStartablePlayers())
		
	def test_main_run(self):
		gamestart.main()
		

if __name__ == '__main__':
    unittest.main()






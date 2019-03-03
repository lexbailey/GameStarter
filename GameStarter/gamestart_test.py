#!/usr/bin/env python

import unittest
from GameStarter import GameStarter, GamePlayer, main

class TestStartButtons(unittest.TestCase):
	def setUp(self):
		pass

	def tearDown(self):
		pass

	def test_player_init(self):
		#Ensure that the player can be instantiated and does sensible things
		#Note that this class should only be instantiated by the GameStarter and so has less validity check on its inputs
		pl = GamePlayer(1.0, 2.0, 0.5)
		self.assertEqual(0.0, pl.level)
		self.assertFalse(pl.joined)
		self.assertEqual(False, pl.pushed)

	def test_player_timing(self):
		#Ensure that the player can be instantiated and does sensible things
		#Note that this class should only be instantiated by the GameStarter and so has less validity check on its inputs
		pl = GamePlayer(1.0, 2.0, 0.5)
		pl.timeStep(0.5)
		self.assertFalse(pl.joined)
		self.assertEqual(False, pl.pushed)
		self.assertEqual(0.0, pl.level)

		pl.pushed = True
		self.assertEqual(True, pl.pushed)

		pl.timeStep(0.51)
		self.assertTrue(pl.waiting)
		level = pl.level
		self.assertTrue((0.509<level) and (level < 0.511))

		pl.timeStep(0.5)
		self.assertTrue(pl.joined)
		level = pl.level
		self.assertTrue((0.999 < level) and (level < 1.001))

	def test_player_invalid_time_step(self):
		pl = GamePlayer(1.0, 2.0, 0.5)
		invalidTimes = [0, 0.0, -1, -1.0]
		for invalidTime in invalidTimes:
			pl.pushed = True
			self.assertRaises(Exception, pl.timeStep, invalidTime)
			pl.pushed = False
			self.assertRaises(Exception, pl.timeStep, invalidTime)

	def test_invalid_levels(self):
		#It is invalid to have a negative active level threshold. This should raise an exception, as should invalid types.
		invalidInputs = [(-1.0, 2.0, 0.5), (1.0, 0.5, 0.2), (1.0, -23.0, 0.5), (2, 1, 3), (1, 0, 4), (-3, -1, -4), (None, None, None), (True, True, True), (False, True, False), ("1", "2", "7")]
		for invalidInput in invalidInputs:
			try:
				gs = GameStarter(2, *invalidInput)
				self.fail('Started with invalid levels')
			except Exception as e:
				pass

	def test_invalid_time_step(self):
		#It is invalid to have a negative time step. This should raise an exception
		invalidInputs = [-1, -1.0, -99999, "foo", "-23", "34", "12.34", None, True, False]
		for invalidInput in invalidInputs:
			try:
				gs = GameStarter(2, 1.0, 2.0, 0.5)
				gs.timeStep(invalidInput)
				self.fail('Invalid time step allowed')
			except Exception as e:
				errorMsg = 'GameStarter.timeStep: time step must be a positive float.'
				self.assertEqual(errorMsg, str(e)[0:len(errorMsg)])

	def test_total_state_correct(self):
		testInputs = [2, 3, 4, 5, 6, 10, 999]
		for testInput in testInputs:
			gs = GameStarter(testInput, 1.0, 2.0, 0.5)
			self.assertEqual([], gs.joined_players)
			self.assertEqual([], gs.waiting_players)
			self.assertFalse(gs.ready)

	def test_player_state_correct(self):
		testInputs = [2, 3, 4, 5, 6, 10, 999]
		for testInput in testInputs:
			gs = GameStarter(testInput, 1.0, 2.0, 0.5)
			self.assertEqual([], gs.joined_players)
			self.assertEqual([], gs.waiting_players)
			self.assertFalse(gs.ready)

	def test_total_state_postreset(self):
		testInputs = [2, 3, 4, 5, 6, 10, 999]
		for testInput in testInputs:
			gs = GameStarter(testInput, 1.0, 2.0, 0.5)
			gs.player(0).release()
			gs.player(1).push()
			gs.timeStep(1.5)
			self.assertEqual([1], gs.joined_players)
			gs.resetAll()
			self.assertEqual([], gs.joined_players)
			self.assertEqual([], gs.waiting_players)
			self.assertFalse(gs.ready)

	def test_two_player_start(self):
		#test that two players can start a game
		try:
			gs = GameStarter(2, 1.0, 2.0, 0.5)
		except Exception as e:
			self.fail('Exception during __init__')
		#Both players push
		gs.player(0).push()
		gs.player(1).push()
		#Wait for three seconds
		gs.timeStep(3.0)
		#By now, shouldStart must be true and there should be 2 startable players
		self.assertTrue(gs.shouldStart())
		self.assertEqual(2, len(gs.joined_players))

	def test_single_player_cant_start(self):
		#test that single players cannot start a game
		try:
			gs = GameStarter(2, 1.0, 2.0, 0.5)
		except Exception as e:
			self.fail('Exception during __init__')
		#One player pushes
		gs.player(0).push()
		#Wait for three seconds
		gs.timeStep(3.0)
		#shouldStart must be false
		self.assertFalse(gs.shouldStart())

	def test_player_can_drop_out(self):
		#test that a player can go below active and drop out of the round start
		try:
			gs = GameStarter(2, 1.0, 2.0, 0.5)
		except Exception as e:
			self.fail('Exception during __init__')
		#One player pushes
		gs.player(0).push()
		#Wait for three seconds
		gs.timeStep(3.0)
		#player has peaked at 2 seconds, let go of the button
		gs.player(0).release()
		#1.5 seconds later and they should already be out
		gs.timeStep(1.5)
		self.assertFalse(gs.player(0).joined)
		self.assertEqual(0.0, gs.player(0).level)


	def test_two_player_start_with_four_player_game(self):
		#test that two players can start a game
		try:
			gs = GameStarter(4, 1.0, 2.0, 0.5)
		except Exception as e:
			self.fail('Exception during __init__')
		#Both players push
		gs.player(0).push()
		gs.player(1).push()
		#Wait for two seconds
		gs.timeStep(2.0)
		#By now, shouldStart must be true and there should be 2 startable players
		self.assertTrue(gs.shouldStart())
		self.assertEqual(2, len(gs.joined_players))

	def test_button_spam_filtering(self):
		#test that two players can start a game even when someone is button spamming
		try:
			gs = GameStarter(4, 1.0, 2.0, 0.5)
		except Exception as e:
			self.fail('Exception during __init__')
		#Both players push
		gs.player(0).push()
		gs.player(1).push()
		#Wait for 1.5 seconds (nearly there)
		gs.timeStep(1.5)
		#player three then spams
		gs.player(2).push()
		gs.timeStep(0.7)
		gs.player(2).release()
		gs.timeStep(0.5)
		#By now, shouldStart must be true and there should be 2 startable players
		self.assertTrue(gs.shouldStart())
		self.assertEqual(2, len(gs.joined_players))
		#Do more buttom mashing to see if the filter still works after this
		gs.player(2).push()
		gs.timeStep(0.7)
		gs.player(2).release()
		gs.timeStep(0.5)
		gs.player(2).push()
		gs.timeStep(0.7)
		gs.player(2).release()
		gs.timeStep(0.5)
		#shouldStart must stil be true and there should still be 2 startable players
		self.assertTrue(gs.shouldStart())
		self.assertEqual(2, len(gs.joined_players))

	def test_late_joiners(self):
		#test that for players can start a game even when some people take a while to join in
		try:
			gs = GameStarter(4, 1.0, 2.0, 0.5)
		except Exception as e:
			self.fail('Exception during __init__')
		#One players pushes
		gs.player(0).push()
		#Wait for 3 seconds (player 1 fully ready)...
		gs.timeStep(3.0)
		#Player two joins in
		gs.player(1).push()
		#a little later...
		gs.timeStep(0.8)
		#player three then joins
		gs.player(2).push()
		#later still..
		gs.timeStep(0.7)
		#player four pushes too
		gs.player(3).push()
		#another two seconds...
		gs.timeStep(2.0)
		#and now, shouldStart must be true and there should be 4 startable players
		self.assertTrue(gs.shouldStart())
		self.assertEqual(4, len(gs.joined_players))

	def test_dodgy_button(self):
		#test that a dodgy button that flickers on and off sometimes doesn't cause problems
		#this also simulates people who fail to keep their hand on the button persistently
		try:
			gs = GameStarter(2, 1.0, 20.0, 0.5) #note 20 second start time on this one
		except Exception as e:
			self.fail('Exception during __init__')
		#Both players push
		gs.player(0).push()
		gs.player(1).push()
		#Wait for 1.5 seconds (nearly there)...
		gs.timeStep(1.5)
		#Player two goes dodgy
		gs.player(1).release()
		gs.timeStep(0.1)
		gs.player(1).push()
		gs.timeStep(0.3)
		gs.player(1).release()
		gs.timeStep(0.2)
		gs.player(1).push()
		gs.timeStep(0.7)
		gs.player(1).release()
		gs.timeStep(0.04)
		gs.player(1).push()
		gs.timeStep(10.8)
		gs.player(1).release()
		gs.timeStep(0.2)
		gs.player(1).push()
		gs.timeStep(0.7)
		gs.player(1).release()
		gs.timeStep(0.04)
		gs.player(1).push()
		gs.timeStep(20.0) #long one to make sure

		#shouldStart must be true and there should be 2 startable players
		self.assertTrue(gs.shouldStart())
		self.assertEqual(2, len(gs.joined_players))

	def test_main_run(self):
		main()


if __name__ == '__main__':
    unittest.main()

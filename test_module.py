from RPS import player
from RPS_game import play, mrugesh, abbey, quincy, kris
import unittest

class UnitTests(unittest.TestCase):

    def test_player_vs_quincy(self):
        result = play(player, quincy, 1000)
        self.assertTrue(result["p1"] > 0.6 * 1000, "Expected player to defeat quincy at least 60% of the time.")

    def test_player_vs_abbey(self):
        result = play(player, abbey, 1000)
        self.assertTrue(result["p1"] > 0.6 * 1000, "Expected player to defeat abbey at least 60% of the time.")

    def test_player_vs_kris(self):
        result = play(player, kris, 1000)
        self.assertTrue(result["p1"] > 0.6 * 1000, "Expected player to defeat kris at least 60% of the time.")

    def test_player_vs_mrugesh(self):
        result = play(player, mrugesh, 1000)
        self.assertTrue(result["p1"] > 0.6 * 1000, "Expected player to defeat mrugesh at least 60% of the time.")

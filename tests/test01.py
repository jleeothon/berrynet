import os
import unittest

import berrynet

class TestParser(unittest.TestCase):

    def setUp(self):
        self.network = berrynet.Network()

    def test_loader(self):
        berrynet.load_network(self.network, "./tests/rain.json")
        # print(self.network.verbose())

    def test_sanity_checks(self):
        berrynet.load_network(self.network, "./tests/rain.json")
        for node in self.network.nodes.values():
            for v, cps in node.distribution.items():
                cps.check_sanity()

    def test_marginal_probability_Rained(self):
        berrynet.load_network(self.network, "./tests/rain.json")
        solver = berrynet.NaiveSolver(self.network)
        p = solver.marginal_probability(Rained="Yes")
        print("P(Rained=Yes) =", p)
        p = solver.marginal_probability(Rained="No")
        print("P(Rained=No) =", p)

    def test_marginal_probability_WetGrass_yes(self):
        berrynet.load_network(self.network, "./tests/rain.json")
        solver = berrynet.NaiveSolver(self.network)
        p = solver.marginal_probability(WetGrass="Yes")
        print("P(WetGrass=Yes) =", p)
        p = solver.marginal_probability(WetGrass="No")
        print("P(WetGrass=No) =", p)

    def test_marginal_probability_Sprinkler_yes(self):
        berrynet.load_network(self.network, "./tests/rain.json")
        solver = berrynet.NaiveSolver(self.network)
        p = solver.marginal_probability(Sprinkler="Yes")
        print("P(Sprinkler=Yes) =", p)
        p = solver.marginal_probability(Sprinkler="No")
        print("P(Sprinkler=No) =", p)

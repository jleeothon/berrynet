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


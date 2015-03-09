import json
from berrynet import *


__all__ = ["load_network"]


# JSON objects are denoted by jCameCase
# network objects are denoted with_underscores


def load_network(network, filename):
    nodes = None
    with open(filename, "r") as f:
        nodes = json.load(f)

    for jNode in nodes:
        name = jNode["name"]
        if name not in network.nodes:
            node = Node(name)
            network.nodes[name] = node
            distribution = jNode.get("distribution")
            if distribution is None:
                raise Exception("Node \"%s\" has no distribution" % name)
            for value in distribution:
                node.values.add(value)
        else:
            raise Exception("Node repeated: %s" % name)

    for jNode in nodes:
        node = network.nodes[jNode["name"]]
        if "parents" in jNode:
            for jParent in jNode["parents"]:
                parent = network.nodes.get(jParent)
                if parent is None:
                    raise Exception("Node not found: %s" % jParent)
                node.parents[jParent] = parent

    for jNode in nodes:
        node = network.nodes[jNode["name"]]
        jDistribution = jNode["distribution"]
        if not isinstance(jDistribution, dict):
            raise TypeError("\"distribution\" in \"%s\"must be an object" % node.name)
        for jValue, jCps in jDistribution.items():
            if not isinstance(jCps, list):
                raise TypeError("The set of conditional probabilities"
                    "for \"%s\"=>\"%s\" must be a list" % node.name, jValue)
            cps = ConditionalProbabilitySet(node, jValue)
            for jCp in jCps:
                probability = jCp["probability"]
                eventSet = EventSet(node)
                for jParent, jParentValue in jCp["conditions"].items():
                    eventSet[jParent] = jParentValue
                cp = ConditionalProbability(node, jValue, eventSet, probability)
                cps.add(cp)
            node.distribution[jValue] = cps

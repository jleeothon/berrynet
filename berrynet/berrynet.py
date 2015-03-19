import collections
import os
from operator import methodcaller
from operator import attrgetter
from functools import reduce
from itertools import product

__all__ = [
    "ConditionalProbabilitySet",
    "ConditionalProbability",
    "Network",
    "Node",
    "ValueDistribution",
    "EventSet",
]


class Network(object):
    
    def __init__(self):
        self.nodes = dict()

    def __repr__(self):
        return "; ".join(map(repr, self.nodes.values()))

    def verbose(self):
        return "\n".join(map(methodcaller("verbose"), self.nodes.values()))

    def query(self, query_node, **evidences):
        pass


class Node(object):

    def __init__(self, name):
        """Creates a new Node instance
        Contains a string name (just it cannot be "%").
        
        - ``parents`` is a set of Node objects.
        
        - ``values`` is a set of str objects.
        
        - ``probabilities`` is a ``set`` of ConditionalProbability objects
        where all combinations of parents' values are described.
        """
        self.name = name
        self.parents = dict()
        self.values = set()
        self.distribution = ValueDistribution(self)

    def __str__(self):
        return self.name

    def __repr__(self):
        return "%s (%s)" % (self.name,
            " & ".join(map(attrgetter("name"), self.parents.values())))

    def verbose(self):
        return "%s\n%s" % (repr(self), self.distribution.verbose())


class ValueDistribution(dict):
    """
    A dictionary where keys are the possible values of a variable node,
    values are a set of conditional probabilities
    (``ConditionalProbabilitySet`` object).

    Key is a str.

    Value is ConditionalProbabilitySet.
    """

    def __init__(self, node):
        if not isinstance(node, Node):
            raise TypeError("Expected Node, have %s" % type(node))
        self.node = node
        super().__init__()
    
    def __setitem__(self, key, value):
        if not isinstance(key, str):
            raise TypeError("Key is not of type str, have %s" % (key, type(key)))
        if not isinstance(value, ConditionalProbabilitySet):
            raise TypeError("Value is not of type ConditionalProbabilitySet,"
                "have %s" % (value, type(value)))
        if not key in self.node.values:
            raise Exception("Key \"%s\" not in node \"%s\"" % (key, self.node.name))
        super().__setitem__(key, value)

    def verbose(self):
        s = ""
        for v, cps in self.items():
            s += "    %s\n%s\n" % (v, cps.verbose())
        return s


class ConditionalProbabilitySet(set):
    """
    A collection or conditional probabilities
    """

    def __init__(self, node, node_value):
        self.node = node
        self.node_value = node_value
        super().__init__()

    
    def add(self, item):
        super().add(item)

    def __repr__(self):
        return "[%s]" % ",".join(map(repr, self))

    def verbose(self):
        s = ""
        for cp in self:
            s += "%s\n" % cp.verbose()
        return s

    def check_sanity(self):
        expected_parentvalues = []
        for p in self.node.parents.values():
            values = []
            for v in p.values:
                values.append({p.name: v})
            expected_parentvalues.append(values)
        _eventset = [p for p in product(*expected_parentvalues)]
        def combinemap(x, y):
            x.update(y)
            return x
        _eventset = [reduce(combinemap, c, dict()) for c in _eventset]
        for event in map(attrgetter("events"), self):
            event = event.dict()
            assert event in _eventset, ("%s not found in the "
                "expected conditional distributions for %s=%s: %s" % (
                    event, self.node.name, self.node_value, _eventset
                    ))
            _eventset.remove(event)
        assert _eventset == [], "pending events found: %s" % _eventset


class ConditionalProbability(object):
    """
    node_value is the value of the node for which these events have the said probability.

    Key is a EventSet.

    Value is a number between 0 and 1.
    """

    def __init__(self, node, node_value, events, probability):
        self.node = node
        self.node_value = node_value
        self.events = events
        self.probability = probability

    def _setitem__(self, key, value):
        if not isinstance(key, EventSet):
            raise TypeError("Key expected EventSet")
        if not isinstance(value, (int, float)):
            raise TypeError("Value expected number")
        elif value < 0 or value > 1:
            raise Exception("%d is not between 0 and 1" % value)
        super().__setitem__(key, value)

    def verbose(self):
        return "P(%s=%s | %s) = %.2f" % (
            self.node.name,
            self.node_value,
            self.events.verbose(),
            self.probability)

    def __repr__(self):
        return repr(self.events)


class EventSet(dict):
    """
    """

    def __init__(self, node):
        self.node = node

    def __setitem__(self, key, value):
        """
        Key is a string but becomes automatically resolved 
        """
        _key = key
        if not isinstance(key, Node):
            if isinstance(key, str):
                _key = self.node.parents[key]
            else:
                raise TypeError("Key should be Node or str, have %s" % type(key))
        elif key not in self.node.parents:
            raise Exception("%s not in parents of %s" % (str(key), self.node))
        if not isinstance(value, str):
            raise TypeError("Value should be str, have %s" % type(value))
        super().__setitem__(_key, value)

    def verbose(self):
        s = "{"
        s += " & ".join([("%s=%s" % (k, v)) for k, v in self.items()])
        s += "}"
        return s

    def __repr__(self):
        return self.verbose()

    def dict(self):
        return {k.name: v for k, v in self.items()}

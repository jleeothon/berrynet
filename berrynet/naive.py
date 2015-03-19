__all__ = ["NaiveSolver"]

class NaiveSolver(object):

    def __init__(self, network):
        self.network = network
        self._marginal_probabilities = dict()

    def marginal_probability(self, **kwargs):
        """
        Use like solver.marginal_probability(a="a")
        """
        if len(kwargs) != 1:
            raise Exception("Provide only one variable and one value")
        variable = [k for k in kwargs.keys()][0]
        value = [v for v in kwargs.values()][0]
        mp = self._marginal_probabilities.get(variable)
        if mp is None:
            node = self.network.nodes.get(variable)
            if node is None:
                raise Exception("%s is not a variable in the network", variable)
            cps = node.distribution.get(value)
            if cps is None:
                raise Exception("%s is not a value of %s", value, variable)
            p = 0
            for cp in cps:
                q = 1
                for pvar, pval in cp.events.items():
                    r = self.marginal_probability(**{pvar.name:pval})
                    q *= r
                p += cp.probability * q
            mp = p
        return mp

    def conditional_probability(**kwargs):
        """
        Use in conjunction to ``ConditionedProbability.given``.
        """
        if len(kwargs) != 1:
            raise Exception("Use only one node to query")
        variable = variable = [k for k in kwargs.keys()][0]
        value = [v for v in kwargs.values()][0]
        return ConditionedProbability(**{variable: value})
        
class ConditionedProbability(NaiveSolver):

    def __init__(self, variable, value):
        self.variable = variable # a Node, not str
        self.value = value

    def given(**kwargs):
        pass



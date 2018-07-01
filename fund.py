class Fund:

    def __init__(self, name, parent=""):
        self.name = name
        self.parent = parent
        self.has_child = False
        self.mv = 0
        self.agg_mv = 1
        self.weight = 0.0

    def __repr__(self):
        return "name: {}, parent: {}, mv: {}".format(self.name, self.parent, self.mv)

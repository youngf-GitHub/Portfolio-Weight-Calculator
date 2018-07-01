
from fund import Fund


class Calculator:

    def __init__(self, start_file_name, end_file_name):

        self.start_file = start_file_name
        self.end_file = end_file_name

        self.start_market_tree_map = {}
        self.end_market_tree_map = {}

        self.current_file_name = start_file_name
        self._load_fund_data(self.start_market_tree_map)

        self.current_file_name = end_file_name
        self._load_fund_data(self.end_market_tree_map)

    def __repr__(self):
        return "start_file: {} ({}), end_file: {} ({})".format(
            self.start_file, len(self.start_market_tree_map), self.end_file, len(self.end_market_tree_map))

    def _load_fund_data(self, tree_map):

        if self.current_file_name == "":
            return

        with open(self.current_file_name, 'r') as f:

            for line in list(line for line in (l.strip() for l in f) if line):

                try:
                    parent_name, child_name, mv = line.strip().split(',')

                    parent_name = parent_name.strip()
                    child_name = child_name.strip()
                    mv = mv.strip()

                    parent = tree_map.get(parent_name)
                    if parent is None:
                        parent = Fund(parent_name)
                        tree_map[parent_name] = parent

                    parent.has_child = True

                    child = tree_map.get(child_name)
                    if child is None:
                        child = Fund(child_name, parent_name)
                        tree_map[child_name] = child

                    child.parent, child.mv = parent_name, int(mv)

                except ValueError as e:
                    raise ValueError("{}".format(e.args), "{}".format(line))

                except FileNotFoundError:
                    raise FileNotFoundError("file {} not found".format(self.current_file_name))

        for name, root in tree_map.items():
            if root.parent == "":
                self._validate(tree_map, root)

    def _validate(self, tree_map, root):

        root.agg_mv = 0

        if not root.has_child:
            root.agg_mv = root.mv
            return root.agg_mv

        for name, pf in tree_map.items():
            if pf.parent == root.name:
                root.agg_mv += self._validate(tree_map, pf)

        if root.agg_mv != root.mv and root.parent != "":
            raise ValueError("{} MV={}, AggrMV={}".format(root.name, root.mv, root.agg_mv),
                             "{}".format(self.current_file_name))

        elif root.parent == "":
            root.mv = root.agg_mv

        return root.agg_mv

    def _find_all_base_funds(self, tree_map, root):

        base_funds = []

        if not root.has_child:
            base_funds.append(root.name)
            return base_funds

        for name, fund in tree_map.items():
            if fund.parent == root.name:
                base_funds.extend(self._find_all_base_funds(tree_map, fund))

        return base_funds

    def print_start_pf_ratio(self):

        for name, root in self.start_market_tree_map.items():
            if root.parent == "":
                base_funds = self._find_all_base_funds(self.start_market_tree_map, root)

                for key in base_funds:

                    if root.agg_mv == 0:
                        root.agg_mv = 1

                    self.start_market_tree_map.get(key).weight = self.start_market_tree_map.get(key).mv / root.agg_mv
                    print("%s,%s,%.3f" % (root.name, key, self.start_market_tree_map.get(key).weight))

    def print_weighted_return(self):

        for name, fund in self.end_market_tree_map.items():

            if fund.parent == "":
                if self.start_market_tree_map.get(name) is None or self.start_market_tree_map.get(name).parent != "":
                    raise ValueError("{}, {}".format(self.start_file, self.end_file), "does not match.")

                v = self.start_market_tree_map.get(name).agg_mv
                increase = self.end_market_tree_map.get(name).agg_mv - self.start_market_tree_map.get(name).agg_mv

                if v == 0:
                    v = 1

                print("weighted return of %s: %.2f %s" % (name, float(increase / v * 100), "%"))

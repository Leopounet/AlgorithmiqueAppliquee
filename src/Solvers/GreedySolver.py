class GreedySolver:

    def __init__(self, graph):
        self.graph = graph
        self.max_uncovered = graph.max_deg_index
        self.max_current = 0
        self.compensation = int((self.graph.dominant_value + 1) / 2)

    def remove_uncovered(self, index):
        tmp_max_uncovered = 0
        val1 = self.graph.edges[index]
        for i in range(len(self.graph.edges)):
            self.graph.edges[i] = ((val1 ^ self.graph.edges[i]) + self.compensation) & self.graph.edges[i]
            count = bin(self.graph.edges[i]).count('1')
            if count > self.max_current:
                tmp_max_uncovered = i
                self.max_current = count
        self.max_uncovered = tmp_max_uncovered

    def _solve(self, dom_val, def_list, depth=0):
        if dom_val == self.graph.dominant_value:
            return def_list

        def_list.append(self.max_uncovered)
        dom_val = dom_val | self.graph.edges[self.max_uncovered]
        self.max_current = 0
        self.remove_uncovered(self.max_uncovered)

        return self._solve(dom_val, def_list, depth+1)

    def sum_all(self, index, def_list, edges):
        s = 0
        for j in range(len(def_list)):
            if j != index:
                s = s | edges[def_list[j]]
        return s

    def purge(self, def_list, edges):
        new_list = []
        changed = False
        for i in range(len(def_list)):
            s = self.sum_all(i, def_list, edges)
            d = edges[def_list[i]]


            if s | d != s :
                new_list.append(def_list[i])
            else:
                changed = True
        return (new_list.copy(), changed)

    def has_solution(self):
        s = 0
        for e in self.graph.edges:
            s = s | e
        return s == self.graph.dominant_value

    def solve(self, params):
        if not self.has_solution():
            return None
        edges = self.graph.edges.copy()
        res = self._solve(0, [])
        changed = True
        while changed:
            res, changed = self.purge(res, edges)
        return self.graph.index_list_to_defenders(res)

    def sort(self, compare_func):
        arrays = [self.graph.deg, self.graph.defenders, self.graph.edges]
        self.graph.bubble_sort(arrays, compare_func)

    def print_b(self, val):
        print(str(bin(val))[2:])
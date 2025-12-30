class Node():
    def __init__(self, state, parent, action):
        self.state = state          # person_id
        self.parent = parent        # parent Node
        self.action = action        # (movie_id, person_id)


class StackFrontier():
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        node = self.frontier[-1]
        self.frontier = self.frontier[:-1]
        return node


class QueueFrontier(StackFrontier):
    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        node = self.frontier[0]
        self.frontier = self.frontier[1:]
        return node

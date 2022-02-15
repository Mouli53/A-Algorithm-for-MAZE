from collections import deque
import heapq
import time


class Hanoi:  # Hanoi representation
    def __init__(self, n):
        self.n = n
        self.pegs = 4
        self.stacks = list()  # define empty stacks
        for i in range(self.pegs):
            self.stacks.append(list())

    def fill_initial_state(self):  # convert to the initial state
        for i in range(self.n, 0, -1):
            self.stacks[0].append(i)

    def is_goal_state(self):  # determine whether it is goal state or not
        return len(self.stacks[-1]) == self.n

    def to_string(self):  # convert hanoi to string (to make it hashable)
        ret = ''
        for i in range(self.pegs):
            if i != 0:
                ret += '*'
            ret += '+'.join(map(str, self.stacks[i]))
        return ret

    def from_string(self, string):  # convert string to hanoi
        parts = string.split('*')
        assert len(parts) == self.pegs
        for i, part in enumerate(parts):
            if len(part.split('+')[0]) > 0:
                self.stacks[i] = list(map(int, part.split('+')))

    def get_possible_moves(self):  # get all possible moves from this hanoi state
        moves = list()
        for i in range(self.pegs):
            for j in range(self.pegs):
                if i == j:
                    continue
                if len(self.stacks[i]) == 0:
                    continue
                if len(self.stacks[j]) == 0 or self.stacks[i][-1] < self.stacks[j][-1]:
                    moves.append((i, j))
        return moves

    def apply_move(self, move):  # create a new state representing this state after applying the move
        new_state = Hanoi(self.n)
        new_state.from_string(self.to_string())
        new_state.stacks[move[1]].append(new_state.stacks[move[0]].pop())
        return new_state


def breadth_first_search(n):  # breadth first search implementation
    queue = deque()

    source_node = Hanoi(n)
    source_node.fill_initial_state()

    queue.append(source_node)
    visited = set()
    visited.add(source_node.to_string())
    parent = dict()
    parent[source_node.to_string()] = None
    goal = None
    while len(queue) > 0:
        node = queue.popleft()
        if node.is_goal_state():
            goal = node.to_string()
            break
        for move in node.get_possible_moves():
            child = node.apply_move(move)
            if child.to_string() not in visited:
                queue.append(child)
                visited.add(child.to_string())
                parent[child.to_string()] = (node.to_string(), move)

    moves = []
    while parent[goal] is not None:
        moves.append(parent[goal][1])
        goal = parent[goal][0]
    return moves[::-1]


def AStar(n, heuristic):  # A* implementation
    source_node = Hanoi(n)
    source_node.fill_initial_state()

    priority_queue = [(0, source_node.to_string())]
    parent = dict()
    parent[source_node.to_string()] = None
    goal = None
    cost = dict()
    cost[source_node.to_string()] = 0

    while len(priority_queue) > 0:
        _, node_str = heapq.heappop(priority_queue)
        node = Hanoi(n)
        node.from_string(node_str)
        if node.is_goal_state():
            goal = node_str
            break
        for move in node.get_possible_moves():
            child = node.apply_move(move)
            new_cost = cost[node_str] + 1
            if child.to_string() not in cost or new_cost < cost[child.to_string()]:
                cost[child.to_string()] = new_cost
                heapq.heappush(priority_queue, (new_cost + heuristic(child), child.to_string()))
                parent[child.to_string()] = (node.to_string(), move)

    moves = []
    while parent[goal] is not None:
        moves.append(parent[goal][1])
        goal = parent[goal][0]
    return moves[::-1]


def h1(hanoi):  # admissible since we have at least this amount of moves
    return hanoi.n - len(hanoi.stacks[-1])  # number of items which are not in the last stack


def h2(hanoi):
    return len(hanoi.stacks[0])  # number of items in the first stack


for i in range(3, 10):  # compare running time of BFS, A* h1 and A* h2
    start = time.time()
    breadth_first_search(i)
    end_bfs = time.time()
    AStar(i, h1)
    end_h1 = time.time()
    AStar(i, h2)
    end_h2 = time.time()
    print("n={}".format(i))
    print("BFS running time is seconds: {}".format(end_bfs - start))
    print("A* h1 running time is seconds: {}".format(end_h1 - end_bfs))
    print("A* h2 running time is seconds: {}".format(end_h2 - end_h1))

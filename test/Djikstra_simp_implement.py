from collections import deque, namedtuple

# simple python code implementing djikstra's algorithm - https://dev.to/mxl/dijkstras-algorithm-in-python-algorithms-for-beginners-dkc
# For understanding the code : learn about deque and namedtuple, sum and min functions applied over python set


#TESTING CODE FROM TUT
# we'll use infinity as a default distance to nodes.
inf = float('inf')
Edge = namedtuple('Edge', 'start, end, cost')


def make_edge(start, end, cost=1):
    return Edge(start, end, cost)

edges = [("a", "b", 7),  ("a", "c", 9),  ("a", "f", 14), ("b", "c", 10),
    ("b", "d", 15), ("c", "d", 11), ("c", "f", 2),  ("d", "e", 6),
    ("e", "f", 9)]

print(edges)

all_edges = [make_edge(*edge) for edge in edges]

print(all_edges)

all_edges_mod = all_edges[:]

print(all_edges_mod)

vertices = set(sum(([edge.start, edge.end] for edge in all_edges), []))

print(type(vertices))

neighbours = {vertex: set() for vertex in vertices}

for edge in all_edges:
    neighbours[edge.start].add((edge.end, edge.cost))

print(neighbours)
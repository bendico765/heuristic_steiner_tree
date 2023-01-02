# heuristic_steiner_tree
This package implements [Kou et al.](https://link.springer.com/article/10.1007/BF00288961) approximation 
algorithm to find an approximation of the optimal Steiner Tree of an undirected graph, allowing
the use of a user's defined heuristic function to compute the shortest paths among nodes by leveraging 
the [A* search framework](https://en.wikipedia.org/wiki/A*_search_algorithm). 

The [Steiner Tree problem](https://en.wikipedia.org/wiki/Steiner_tree_problem) is a famous NP-complete problem that, given 
an undirected graph with non-negative edge weights and a subset of 
vertices, usually referred to as terminals, asks to find a tree of minimum 
weight that contains all terminals (but may include additional 
vertices). Since it isn't know any algorithm capable of finding the 
optimal solution in polynomial time, many approximations have been made.

Note how NetworkX has already implemented a [function](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.approximation.steinertree.steiner_tree.html)
to return an approximation to the minimum Steiner tree of a graph, but the algorithm 
needs to compute the shortest path between each pair of nodes without allowing the exploitation of prior information.

## Installation
To install the latest version of the package just download (or clone) the current project,
open a terminal and run the following commands:
```shell
pip install -r requirements.txt
pip install .
```

## Example
Let's suppose we have a graph _g_ that resemble a grid, where each node can be
expressed using cartesian coordinates; this graph can easily be created
using the [grid_graph](https://networkx.org/documentation/stable/reference/generated/networkx.generators.lattice.grid_graph.html)
function of networkX. In this graph, it is possible to move
up, down, right and left, but not via the diagonals.

In $\mathbb{R}^{2}$ a useful heuristic function to estimate the distance between two points $(x_1, y_1)$ and $(x_2, y_2)$ 
is the [Taxicab (or Manhattan) Geometry](https://en.wikipedia.org/wiki/Taxicab_geometry), defined as $|x_{1} - x_{2}| + |y_{1} - y_{2}|$.

```python
>>> from heuristic_steiner_tree import kou_et_al
>>> import networkx as nx
>>> 
>>> def taxicab_distance(p1: tuple, p2:tuple) -> int:
...     x1, y1 = p1
...     x2, y2 = p2
...     return abs(x1 - x2) + abs(y1 - y2)
... 
>>> 
>>> g = nx.grid_graph((10,10))
>>> for (u, v) in g.edges(): # adding weights to edges
...     g[u][v]["weight"] = 1
... 
>>> terminal_nodes = [(0,0), (2,5), (1,7)]
>>> steiner_tree_approx = kou_et_al(g, taxicab_distance, terminal_nodes, "weight")
```

## Todo list
1. Make some tests
2. Implement newer and more efficient algorithms to approximate the optimal Steiner Tree
3. Write more fine-grained dependencies
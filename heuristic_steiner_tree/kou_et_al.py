import networkx as nx
import itertools as it
from typing import Callable


__all__ = ["kou_et_al"]


def get_complete_distance_graph(
		g_original: nx.Graph,
		terminal_nodes: list[object],
		heuristic_function: Callable[[object, object], float],
		weight: str = "weight"
) -> nx.Graph:
	"""
	Creates the complete graph of the terminal nodes, using the heuristic function to compute
	the distance among them by leveraging the A* star search.

	:param g_original: the original graph
	:param terminal_nodes: list of terminal nodes of the graph that have to be connected by a steiner tree
	:param heuristic_function: a function to evaluate the estimate of the distance from a node to the target.
	The function takes two nodes arguments and must return a number.
	:param weight: edge weights will be accessed via the edge attribute with this key (that is, the weight of the edge
	joining u to v will be g_original.edges[u, v][weight]). If no such edge attribute exists, the weight of the edge is
	assumed to be one
	:return: the complete distance graph among the terminal nodes
	"""
	g = nx.Graph()

	# adding terminal nodes
	g.add_nodes_from(terminal_nodes)

	# computing distances among terminals
	for (p1, p2) in it.combinations(terminal_nodes, 2):
		shortest_path_length = nx.shortest_paths.astar_path_length(g_original, p1, p2, heuristic_function, weight)
		g.add_edge(p1, p2, weight=shortest_path_length)

	return g


def remove_redundant_nodes(
		g_original: nx.Graph,
		terminal_nodes: list[object]
) -> nx.Graph:
	"""
	Prune the Steiner Tree by removing the non-terminal nodes so that all the leaves
	are terminals

	:param g_original: the graph to be pruned
	:param terminal_nodes: list of terminal nodes of the graph that have to be connected by a steiner tree
	:return: pruned approximation of the optimal Steiner Tree
	"""
	g = nx.Graph(g_original)

	# collecting all leaf non-terminal nodes
	leaf_non_terminal_nodes = [node for node in g.nodes() if g.degree(node) == 1 and node not in terminal_nodes]

	# retrace the chain of neighbors until a terminal node is encountered
	while leaf_non_terminal_nodes:
		for node in leaf_non_terminal_nodes[:]:
			neighbour = next(g.neighbors(node))  # get leaf neighbour
			if neighbour not in terminal_nodes:  # check if it is a terminal
				leaf_non_terminal_nodes.append(neighbour)

			leaf_non_terminal_nodes.remove(node)
			g.remove_node(node)

	return g


def kou_et_al(
		g_original: nx.Graph,
		heuristic_function: Callable[[object, object], float],
		terminal_points: list[object],
		weight: str = "weight"
) -> nx.Graph:
	"""
	Computes the approximation by Kou et. al of the minimum weight steiner tree of a graph using the distance function
	to compute the distances among points.

	:param g_original: the original graph
	:param heuristic_function: a function to evaluate the estimate of the distance from a node to the target.
	The function takes two nodes arguments and must return a number.
	:param terminal_points: list of terminal nodes of the graph that have to be connected by a steiner tree
	:param weight: edge weights will be accessed via the edge attribute with this key (that is, the weight of the edge
	joining u to v will be g_original.edges[u, v][weight]). If no such edge attribute exists, the weight of the edge is
	assumed to be one
	:return: approximation to the minimum steiner tree
	"""
	# costruct the complete undirected distance graph
	g1 = get_complete_distance_graph(g_original, terminal_points, heuristic_function, weight)

	# find the MST
	g2 = nx.minimum_spanning_tree(g1, weight)

	# use the MST as a guide to construct the subgraph of the original graph
	g3 = nx.Graph()

	# for each edge, search shortest from begin to target and add it to new graph
	for (start_node, end_node) in g2.edges():
		shortest_path = nx.shortest_paths.astar_path(g_original, start_node, end_node, heuristic_function, weight)

		for (edge_start, edge_end) in it.pairwise(shortest_path):
			g3.add_edge(edge_start, edge_end, weight=g_original[edge_start][edge_end][weight])

	# apply the MST on the sub graph
	g4 = nx.minimum_spanning_tree(g3, weight)

	# construct the steiner tree by pruning the MST of the subgraph
	g5 = remove_redundant_nodes(g4, terminal_points)

	return g5

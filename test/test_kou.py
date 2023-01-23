import networkx as nx
import itertools as it
import heuristic_steiner_tree
import random
import unittest
import math


class KouTests(unittest.TestCase):

	@staticmethod
	def __taxicab_distance(p1: tuple, p2: tuple) -> int:
		x1, y1 = p1
		x2, y2 = p2
		return abs(x1 - x2) + abs(y1 - y2)

	@staticmethod
	def __is_valid(g: nx.Graph, terminals: list[object]) -> bool:
		"""
		Checks if a given tree connects all the specified nodes

		:param g:
		:param terminals:

		:return: True if all the terminals are connected, false otherwise
		"""
		for (source, target) in it.combinations(terminals, 2):
			if not nx.has_path(g, source, target):
				return False
		return True

	def test_kou_et_al(self):
		for n in [1, 10, 20, 50, 100]:
			g = nx.grid_graph((n, n))
			for (u, v) in g.edges():
				g[u][v]["weight"] = 1

			# picking random terminals
			terminals = random.sample(list(g.nodes()), math.ceil(n*0.4))

			# getting steiner tree
			steiner_g = heuristic_steiner_tree.kou_et_al(
				g,
				KouTests.__taxicab_distance,
				terminals
			)

			# checking graph type
			self.assertIsInstance(steiner_g, nx.Graph)

			# checking that all terminals are connected
			self.assertTrue(
				KouTests.__is_valid(
					steiner_g, terminals
				)
			)

			# verify the presence of just one connected component
			self.assertTrue(
				len(list(nx.connected_components(steiner_g))) == 1
			)

			# checking there aren't any non-terminals as leafs
			for node in steiner_g.nodes():
				self.assertFalse(
					steiner_g.degree()[node] == 1 and node not in terminals
				)

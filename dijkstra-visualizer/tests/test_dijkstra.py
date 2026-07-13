import unittest
# Pruebas unitarias para el algoritmo de Dijkstra y la clase Graph
from src.algorithm.dijkstra import dijkstra
from src.algorithm.graph import Graph


# Clase de pruebas para el algoritmo de Dijkstra
class TestDijkstra(unittest.TestCase):

    def setUp(self):
        # Se crea un grafo de ejemplo para las pruebas
        self.graph = Graph()
        self.graph.add_edge('A', 'B', 1)
        self.graph.add_edge('A', 'C', 4)
        self.graph.add_edge('B', 'C', 2)
        self.graph.add_edge('B', 'D', 5)
        self.graph.add_edge('C', 'D', 1)

    def test_shortest_path(self):
        # Prueba que encuentra el camino más corto de A a D
        path, cost = dijkstra(self.graph, 'A', 'D')
        self.assertEqual(path, ['A', 'B', 'C', 'D'])
        self.assertEqual(cost, 4)

    def test_no_path(self):
        # Prueba el caso donde no existe camino entre los nodos
        self.graph.add_edge('E', 'F', 1)
        path, cost = dijkstra(self.graph, 'A', 'F')
        self.assertEqual(path, [])
        self.assertEqual(cost, float('inf'))

    def test_same_node(self):
        # Prueba el caso donde el nodo de inicio y fin es el mismo
        path, cost = dijkstra(self.graph, 'A', 'A')
        self.assertEqual(path, ['A'])
        self.assertEqual(cost, 0)


# Permite ejecutar las pruebas desde la línea de comandos
if __name__ == '__main__':
    unittest.main()
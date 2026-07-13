
# Pruebas unitarias para la clase Graph
from src.algorithm.graph import Graph

def test_graph_initialization():
    # Verifica que el grafo se inicializa vacío
    graph = Graph()
    assert graph.nodes == {}
    assert graph.edges == {}

def test_add_node():
    # Verifica que se puede agregar un nodo
    graph = Graph()
    graph.add_node("A")
    assert "A" in graph.nodes
    assert graph.nodes["A"] == {}

def test_add_edge():
    # Verifica que se puede agregar una arista entre dos nodos
    graph = Graph()
    graph.add_node("A")
    graph.add_node("B")
    graph.add_edge("A", "B", 5)
    assert "B" in graph.edges["A"]
    assert graph.edges["A"]["B"] == 5

def test_remove_node():
    # Verifica que se puede eliminar un nodo y sus aristas
    graph = Graph()
    graph.add_node("A")
    graph.add_node("B")
    graph.add_edge("A", "B", 5)
    graph.remove_node("A")
    assert "A" not in graph.nodes
    assert "A" not in graph.edges

def test_remove_edge():
    # Verifica que se puede eliminar una arista entre dos nodos
    graph = Graph()
    graph.add_node("A")
    graph.add_node("B")
    graph.add_edge("A", "B", 5)
    graph.remove_edge("A", "B")
    assert "B" not in graph.edges["A"]
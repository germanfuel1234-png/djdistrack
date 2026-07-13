class Graph:
    def __init__(self):
        # Diccionario para registrar los nodos del grafo
        # Formato: {nodo: {}}
        self.nodes = {}   # {node: {}} — registra existencia del nodo
        # Diccionario para registrar las aristas y sus pesos
        # Formato: {nodo: {vecino: peso}}
        self.edges = {}   # {node: {neighbor: weight}} — adyacencia

    def add_node(self, value):
        """
        Agrega un nodo al grafo si no existe.
        """
        if value not in self.nodes:
            self.nodes[value] = {}
            self.edges[value] = {}

    def add_edge(self, from_node, to_node, weight):
        """
        Agrega una arista entre dos nodos con un peso dado.
        Si los nodos no existen, los crea automáticamente.
        El grafo es no dirigido, por lo que agrega la arista en ambos sentidos.
        """
        # Auto-crear nodos si no existen
        if from_node not in self.nodes:
            self.add_node(from_node)
        if to_node not in self.nodes:
            self.add_node(to_node)
        self.edges[from_node][to_node] = weight
        self.edges[to_node][from_node] = weight  # grafo no dirigido

    def remove_node(self, node):
        """
        Elimina un nodo y todas sus aristas asociadas.
        """
        if node in self.nodes:
            del self.nodes[node]
            del self.edges[node]
            # Elimina referencias al nodo en las listas de vecinos
            for n in self.edges:
                self.edges[n].pop(node, None)

    def remove_edge(self, from_node, to_node):
        """
        Elimina la arista entre dos nodos (en ambos sentidos).
        """
        if from_node in self.edges:
            self.edges[from_node].pop(to_node, None)
        if to_node in self.edges:
            self.edges[to_node].pop(from_node, None)

    def get_neighbors(self, node):
        """
        Devuelve los vecinos y pesos de un nodo dado.
        """
        return self.edges[node].items() if node in self.edges else None

    def to_dict(self):
        """
        Convierte el grafo a un diccionario serializable con nodos y aristas.
        Útil para exportar el grafo, por ejemplo, a JSON.
        """
        seen = set()
        edge_list = []
        #el primer for Recorre cada nodo (a) y su diccionario de vecinos (neighbors)
        #el segundo for Recorre cada vecino (b) y su peso (w) en el diccionario de vecinos
        #key crea una tupla ordenada de los nodos (a, b) para evitar duplicados en un grafo no dirigido
        
        for a, neighbors in self.edges.items():
            for b, w in neighbors.items():
                key = tuple(sorted([a, b]))
                ##Si la tupla (key) no ha sido vista antes, se agrega a seen y se añade la arista a edge_list
                if key not in seen:
                    seen.add(key)
                    #agrega la arista a edge_list en formato [nodo1, nodo2, peso]
                    edge_list.append([a, b, w])
        return {"nodes": list(self.nodes.keys()), "edges": edge_list}

    def __iter__(self):
        """
        Permite iterar sobre los nodos del grafo.
        """
        return iter(self.nodes)

    def __contains__(self, node):
        """
        Permite usar 'in' para verificar si un nodo existe en el grafo.
        """
        return node in self.nodes

    def __getitem__(self, node):
        """
        Permite acceder a los vecinos de un nodo usando corchetes.
        Ejemplo: graph[node]
        """
        return self.edges[node]

    def __str__(self):
        """
        Representación en string del grafo (muestra las aristas).
        """
        return str(self.edges)
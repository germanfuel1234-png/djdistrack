def dijkstra(graph, start, end):
    """
    Implementación del algoritmo de Dijkstra.
    Devuelve (camino, costo_total) desde 'start' hasta 'end'.
    Si no hay camino, devuelve ([], inf).
    """
    import heapq  # módulo de la librería estándar para cola de prioridad (min-heap)

    # ── Validaciones de entrada ──────────────────────────────────────────────

    # Si alguno de los nodos no existe en el grafo, no tiene sentido continuar
    if start not in graph or end not in graph:
        return [], float('inf')

    # Caso trivial: origen y destino son el mismo nodo, costo 0
    if start == end:
        return [start], 0

    # ── Inicialización ───────────────────────────────────────────────────────

    # Distancia conocida más corta desde 'start' a cada nodo.
    # Se inicializa en infinito porque aún no sabemos cómo llegar a ninguno.
    #
    # [Técnico] Dict comprehension: la variable 'distances' es un diccionario
    # donde cada clave es un 'node' (str) obtenido iterando el grafo con for,
    # y cada valor es float('infinity') — un float IEEE-754 que representa +∞.
    # Equivale a escribir manualmente: distances['A'] = inf, distances['B'] = inf, ...
    distances = {node: float('infinity') for node in graph}

    # La distancia desde el inicio a sí mismo es 0
    distances[start] = 0

    # Cola de prioridad: lista de tuplas (distancia, nodo).
    # heapq siempre extrae el elemento con menor distancia primero.
    priority_queue = [(0, start)]

    # Diccionario para reconstruir el camino al final.
    # Guarda qué nodo precede a cada nodo en la ruta más corta encontrada.
    previous_nodes = {node: None for node in graph}

    # ── Bucle principal ──────────────────────────────────────────────────────

    # Continúa mientras haya nodos pendientes de explorar
    while priority_queue:

        # Extrae el nodo con la distancia acumulada más baja del heap
        current_distance, current_node = heapq.heappop(priority_queue)

        # Si llegamos al destino, ya tenemos la ruta más corta; salimos
        if current_node == end:
            break

        # Si este registro en el heap está desactualizado (hay otro más corto
        # ya registrado en 'distances'), se descarta y se sigue con el siguiente
        if current_distance > distances[current_node]:
            continue

        # Recorre todos los vecinos del nodo actual y sus pesos de arista
        for neighbor, weight in graph[current_node].items():

            # Distancia tentativa al vecino pasando por current_node
            distance = current_distance + weight

            # Solo actualiza si esta ruta es mejor que la conocida hasta ahora
            if distance < distances[neighbor]:
                distances[neighbor] = distance          # actualiza la distancia mínima
                previous_nodes[neighbor] = current_node  # registra el predecesor
                heapq.heappush(priority_queue, (distance, neighbor))  # encola con nueva prioridad

    # ── Comprobación de alcanzabilidad ───────────────────────────────────────

    # Si la distancia al destino sigue siendo infinito, no hay camino
    if distances[end] == float('infinity'):
        return [], float('inf')

    # ── Reconstrucción del camino ────────────────────────────────────────────

    path = []
    current_node = end  # empieza desde el destino y va hacia atrás

    # Sigue el rastro de predecesores hasta llegar al origen (None)
    while current_node is not None:
        path.append(current_node)              # añade el nodo al camino
        current_node = previous_nodes[current_node]  # salta al predecesor

    path.reverse()  # el camino quedó al revés (destino→origen), se invierte

    # Devuelve la lista ordenada de nodos y el costo total
    return path, distances[end]
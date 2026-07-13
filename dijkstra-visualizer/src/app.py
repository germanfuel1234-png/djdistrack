import heapq
import random
from flask import Flask, render_template, request, jsonify
from algorithm.graph import Graph

app = Flask(__name__)

# ── Ciudad simulada: grilla 13 x 8 intersecciones con jitter orgánico ──────
# Canvas destino: 800 x 560 px
random.seed(42)
_COLS, _ROWS   = 13, 8
_PAD_X, _PAD_Y = 50, 45
_CW,    _CH    = 800, 560

NODE_POSITIONS = {}
for _r in range(_ROWS):
    for _c in range(_COLS):
        _name = f"{_r}x{_c}"
        _bx = _PAD_X + _c * (_CW - 2 * _PAD_X) // (_COLS - 1)
        _by = _PAD_Y + _r * (_CH - 2 * _PAD_Y) // (_ROWS - 1)
        NODE_POSITIONS[_name] = {
            "x": _bx + random.randint(-8, 8),
            "y": _by + random.randint(-8, 8),
        }

EDGE_LIST = []
# Recorre todas las filas y columnas de la grilla para crear las aristas (calles) del grafo
for _r in range(_ROWS):
    for _c in range(_COLS):
        _n = f"{_r}x{_c}"  # Nombre del nodo/intersección actual, por ejemplo '3x5'
        # Si no es la última columna, intenta crear una calle horizontal hacia la derecha
        # random.random() > 0.06 introduce una probabilidad de que falte la calle (hace la ciudad menos regular)
        if _c < _COLS - 1 and random.random() > 0.06:   # calle horizontal
            # Agrega una arista desde el nodo actual al de la derecha, con peso aleatorio entre 1 y 14
            EDGE_LIST.append((_n, f"{_r}x{_c+1}", random.randint(1, 14)))
        # Si no es la última fila, intenta crear una calle vertical hacia abajo
        if _r < _ROWS - 1 and random.random() > 0.06:   # calle vertical
            # Agrega una arista desde el nodo actual al de abajo, con peso aleatorio entre 1 y 14
            EDGE_LIST.append((_n, f"{_r+1}x{_c}", random.randint(1, 14)))

graph = Graph()
# Recorre cada arista de la lista EDGE_LIST para construir el grafo
# Cada elemento de EDGE_LIST es una tupla con 3 valores: (a, b, w)
#   a: nodo de origen (por ejemplo, '2x3')
#   b: nodo de destino (por ejemplo, '2x4')
#   w: peso/costo de la arista (por ejemplo, 7)
# El for "for a, b, w in EDGE_LIST" descompone automáticamente cada tupla en sus tres partes
for a, b, w in EDGE_LIST:
    # Agrega la arista al grafo conectando a con b y asignando el peso w
    graph.add_edge(a, b, w)


@app.route('/')  # Decorador de Flask: indica que esta función responde a la ruta principal ('/') del sitio web
def index():
    # Prepara la lista de aristas en formato JSON para pasarla al template
    #Se está creando una nueva lista llamada edges_json.
    #compresion de lista ,lista adentro de otra lista
    #Cada elemento de EDGE_LIST es una tupla con tres elementos: (a, b, w).
    #El resultado es una lista de listas, donde cada sublista representa una arista con su nodo de origen, nodo de destino y peso.
    edges_json = [[a, b, w] for a, b, w in EDGE_LIST]
    # Renderiza la plantilla 'index.html' y le pasa los nodos y las aristas para que se puedan mostrar en la web
    return render_template('index.html', nodes=NODE_POSITIONS, edges=edges_json)

#es de web dcora el html en la ruta /run y acepta solo peticiones POST
@app.route('/run', methods=['POST'])
def run():
    data = request.get_json()
    start = data.get('start')
    end = data.get('end')
    #prueba de errores: si el nodo de inicio o el nodo de destino no están en el grafo, devuelve un error JSON con un mensaje y un código de estado 400 (Bad Request)

    if start not in graph or end not in graph:
        return jsonify({"error": "Nodo no válido"}), 400
    #Esta línea llama a la función _bidirectional_dijkstra_steps y guarda su resultado en tres variables:
    #steps: una lista con los pasos intermedios que siguió el algoritmo
    #path: una lista con los nodos que forman el camino más corto encontrado entre start y end.
    #cost: el costo total del camino más corto
    steps, path, cost = _bidirectional_dijkstra_steps(graph, start, end)

    if not path:
        return jsonify({"error": f"No hay camino de {start} a {end}"}), 200

    return jsonify({"steps": steps, "path": path, "cost": cost})

#Es una función que implementa el algoritmo de Dijkstra bidireccional.
#g: el grafo sobre el que se va a buscar el camino más corto
#start: el nodo de inicio.
#end: el nodo de destino.

def _bidirectional_dijkstra_steps(g, start, end):
    """
    Dijkstra Bidireccional: expande simultáneamente desde 'start' (hacia adelante)
    y desde 'end' (hacia atrás) hasta que las dos fronteras se encuentran.
    Devuelve (pasos, camino, costo_total).
    """

    # ── Búsqueda hacia adelante (desde start) ────────────────────────────────
    # dist_fwd = {n: float('inf') for n in g}
    #Crea un diccionario donde la clave es cada nodo del grafo y el valor es infinito. Representa la distancia mínima conocida desde el nodo de inicio hasta cada nodo (al principio, todas son infinitas).
    dist_fwd = {n: float('inf') for n in g}
    #Crea un diccionario donde la clave es cada nodo y el valor es None. Guarda el nodo anterior en el camino más corto encontrado hasta ese momento (sirve para reconstruir el camino al final).
    prev_fwd = {n: None for n in g}
    #La distancia desde el nodo de inicio hasta sí mismo es 0.
    dist_fwd[start] = 0
    #nicializa la cola de prioridad (heap) con una tupla (0, nodo de inicio). Aquí se irán guardando los nodos a explorar, priorizando los de menor distancia acumulada.
    pq_fwd = [(0, start)]
    #Crea un conjunto vacío para registrar los nodos que ya han sido visitados en la búsqueda hacia adelante.
    vis_fwd = set()

    # ── Búsqueda hacia atrás (desde end) ─────────────────────────────────────
    dist_bwd = {n: float('inf') for n in g}
    prev_bwd = {n: None for n in g}
    dist_bwd[end] = 0
    pq_bwd = [(0, end)]
    vis_bwd = set()

    #se crean vacias y se actualizan en la linea 142 "steps.append"
    steps = []
    best = float('inf')
    meeting = None

    def _relax_collect(pq, dist, prev, u):
        """
        Relaja (actualiza) las aristas que salen del nodo u:
        - Intenta mejorar la distancia conocida a cada vecino v de u.
        - Si encuentra un camino más corto, actualiza la distancia y el predecesor.
        - Añade los vecinos a la cola de prioridad para seguir explorando.
        - Devuelve la lista de aristas exploradas en este paso (para animación o depuración).
        """
        new_edges = []  # Lista para registrar las aristas exploradas desde u
        for v, w in g[u].items():  # Para cada vecino v de u y el peso w de la arista
            new_edges.append([u, v])  # Guarda la arista explorada para visualización
            new_d = dist[u] + w  # Calcula la nueva distancia potencial hasta v
            if new_d < dist[v]:  # Si este camino es más corto que el conocido hasta ahora
                dist[v] = new_d  # Actualiza la mejor distancia conocida hasta v
                prev[v] = u      # Guarda que el mejor camino a v viene desde u
                #heapq: es el módulo de Python que permite trabajar con colas de prioridad (heaps).
                #heappush: es la función que agrega un nuevo elemento a la cola de prioridad, manteniendo el orden.
                #pq: es la cola de prioridad (una lista que se usa como heap).
                #(new_d, v): es una tupla donde:
                #   - new_d: es la nueva distancia calculada hasta el nodo v.
                #   - v: es el nodo vecino que se va a explorar.
                heapq.heappush(pq, (new_d, v))  # Añade v a la cola de prioridad para explorar después
        return new_edges  # Devuelve la lista de aristas exploradas en este paso

    while pq_fwd or pq_bwd:

        # ── Un paso hacia adelante ────────────────────────────────────────────
        if pq_fwd:
            d, u = heapq.heappop(pq_fwd)
            if u not in vis_fwd:
                vis_fwd.add(u)
                new_e = _relax_collect(pq_fwd, dist_fwd, prev_fwd, u)

                steps.append({
                    "current_fwd":    u,
                    "current_bwd":    None,
                    "new_edges_fwd":  new_e,
                    "new_edges_bwd":  [],
                })

                if u in vis_bwd:
                    candidate = dist_fwd[u] + dist_bwd[u]
                    if candidate < best:
                        best = candidate
                        meeting = u

        # ── Un paso hacia atrás ───────────────────────────────────────────────
        if pq_bwd:
            d, u = heapq.heappop(pq_bwd)
            if u not in vis_bwd:
                vis_bwd.add(u)
                new_e = _relax_collect(pq_bwd, dist_bwd, prev_bwd, u)

                steps.append({
                    "current_fwd":    None,
                    "current_bwd":    u,
                    "new_edges_fwd":  [],
                    "new_edges_bwd":  new_e,
                })

                if u in vis_fwd:
                    candidate = dist_fwd[u] + dist_bwd[u]
                    if candidate < best:
                        best = candidate
                        meeting = u

        # ── Condición de parada ───────────────────────────────────────────────
        # Cuando la suma de los menores costes pendientes en ambos heaps
        # supera el mejor camino ya encontrado, no puede haber nada mejor.
        if pq_fwd and pq_bwd and meeting is not None:
            if pq_fwd[0][0] + pq_bwd[0][0] >= best:
                break

    if meeting is None or best == float('inf'):
        return steps, [], float('inf')

    # ── Reconstrucción del camino ─────────────────────────────────────────────
    # Mitad delantera: start → ... → meeting  (seguir prev_fwd hacia atrás y revertir)
    #Esta parte del código reconstruye el camino más corto desde el nodo de inicio hasta el nodo donde se encontraron las búsquedas (meeting):
    #Crea una lista vacía donde se irá guardando el camino.
    path_fwd = []
    #Comienza desde el nodo de encuentro (meeting)
    n = meeting
    #Mientras n no sea None (es decir, mientras haya un nodo válido):
#Avanza al nodo anterior en el camino más corto (usando el diccionario de predecesores prev_fwd).
    while n is not None:
        #Agrega el nodo actual a la lista del camino.
        path_fwd.append(n)
        #Avanza al nodo anterior en el camino más corto (usando el diccionario de predecesores prev_fwd).
        n = prev_fwd[n]
        #Al final, invierte la lista porque la reconstrucción va desde el nodo de encuentro hacia el inicio, y queremos el camino en orden correcto (de inicio a meeting).
    path_fwd.reverse()

    # Mitad trasera: meeting+1 → ... → end  (prev_bwd ya apunta hacia end)
    path_bwd = []
    n = prev_bwd[meeting]
    while n is not None:
        path_bwd.append(n)
        n = prev_bwd[n]

    return steps, path_fwd + path_bwd, best


if __name__ == '__main__':
    app.run(debug=True)
    #para montar servidor lan
    #app.run(host="0.0.0.0", port=5000, debug=True)
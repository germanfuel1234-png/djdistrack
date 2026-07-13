# Dijkstra Visualizer

Este proyecto es una aplicación web que implementa el algoritmo de Dijkstra para encontrar la ruta más corta en un grafo. Permite a los usuarios seleccionar un punto de partida y un punto de meta, visualizando cómo evoluciona el algoritmo en un mapa de calles.

## Estructura del Proyecto

```
dijkstra-visualizer
├── src
│   ├── algorithm
│   │   ├── dijkstra.py        # Implementación del algoritmo de Dijkstra
│   │   └── graph.py           # Definición de la estructura del grafo
│   ├── static
│   │   ├── css
│   │   │   └── styles.css      # Estilos CSS para la interfaz de usuario
│   │   └── js
│   │       ├── map.js          # Manejo de la visualización del mapa
│   │       └── visualizer.js    # Lógica para visualizar la expansión del algoritmo
│   ├── templates
│   │   └── index.html          # Plantilla HTML principal
│   ├── routes
│   │   └── api.py              # Manejo de las rutas de la API
│   └── app.py                  # Punto de entrada de la aplicación
├── tests
│   ├── test_dijkstra.py        # Pruebas unitarias para el algoritmo de Dijkstra
│   └── test_graph.py           # Pruebas unitarias para la clase Graph
├── requirements.txt            # Dependencias necesarias para el proyecto
└── README.md                   # Documentación del proyecto
```

## Instalación

1. Clona el repositorio:
   ```
   git clone <URL_DEL_REPOSITORIO>
   cd dijkstra-visualizer
   ```

2. Instala las dependencias:
   ```
   pip install -r requirements.txt
   ```

## Ejecución

Para ejecutar la aplicación, utiliza el siguiente comando:
```
python src/app.py
```

Luego, abre tu navegador y visita `http://127.0.0.1:5000` para acceder a la interfaz de usuario.

## Uso

1. Selecciona un punto de partida y un punto de meta en el mapa.
2. Haz clic en el botón para iniciar la visualización del algoritmo de Dijkstra.
3. Observa cómo se expande el algoritmo y se encuentra la ruta más corta.

## Contribuciones

Las contribuciones son bienvenidas. Si deseas contribuir, por favor abre un issue o envía un pull request.

## Licencia

Este proyecto está bajo la Licencia MIT.
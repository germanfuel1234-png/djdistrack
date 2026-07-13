from flask import Blueprint, request, jsonify
from algorithm.dijkstra import dijkstra
from algorithm.graph import Graph

api = Blueprint('api', __name__)

# In-memory graph for demonstration purposes
graph = Graph()

@api.route('/add_edge', methods=['POST'])
def add_edge():
    data = request.json
    graph.add_edge(data['from'], data['to'], data['weight'])
    return jsonify({"message": "Edge added successfully"}), 201

@api.route('/shortest_path', methods=['POST'])
def shortest_path():
    data = request.json
    start = data['start']
    end = data['end']
    path, distance = dijkstra(graph, start, end)
    return jsonify({"path": path, "distance": distance}), 200

@api.route('/get_graph', methods=['GET'])
def get_graph():
    return jsonify(graph.to_dict()), 200
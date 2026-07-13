const canvas = document.getElementById('mapCanvas');
const ctx = canvas.getContext('2d');
const nodes = [];
const edges = [];
let startNode = null;
let endNode = null;

function drawGraph() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    edges.forEach(edge => {
        ctx.beginPath();
        ctx.moveTo(edge.start.x, edge.start.y);
        ctx.lineTo(edge.end.x, edge.end.y);
        ctx.strokeStyle = '#ccc';
        ctx.stroke();
    });
    nodes.forEach(node => {
        ctx.beginPath();
        ctx.arc(node.x, node.y, 10, 0, Math.PI * 2);
        ctx.fillStyle = node === startNode ? 'green' : node === endNode ? 'red' : 'blue';
        ctx.fill();
        ctx.stroke();
    });
}

function addNode(x, y) {
    const newNode = { x, y };
    nodes.push(newNode);
    drawGraph();
}

function addEdge(start, end) {
    edges.push({ start, end });
    drawGraph();
}

function setStartNode(node) {
    startNode = node;
    drawGraph();
}

function setEndNode(node) {
    endNode = node;
    drawGraph();
}

function visualizeDijkstra() {
    // Implement the visualization of Dijkstra's algorithm here
    // This function will update the graph as the algorithm progresses
}

canvas.addEventListener('click', (event) => {
    const rect = canvas.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;
    const clickedNode = nodes.find(node => Math.hypot(node.x - x, node.y - y) < 10);

    if (!clickedNode) {
        addNode(x, y);
    } else {
        if (!startNode) {
            setStartNode(clickedNode);
        } else if (!endNode) {
            setEndNode(clickedNode);
        } else {
            // Optionally handle edge creation or other interactions
        }
    }
});

// Additional functions to handle edge creation and Dijkstra's algorithm visualization can be added here.
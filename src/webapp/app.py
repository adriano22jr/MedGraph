import utilities, flask, json
from flask_cors import cross_origin

app = flask.Flask(__name__, template_folder = "templateFiles", static_folder = "staticFiles")

@app.route("/meshterms_graph", methods = ["GET", "POST"])
@cross_origin()
def meshterms_graph():
    graph = utilities.extract_graph(filename = "data/graph_meshterms.pkl")
    
    graph_nodes = []
    for node in graph.nodes:
        graph_nodes.append({"id": str(node), "label": str(node)})
        
    graph_edges = []
    for edge in graph.edges(data = True):
        graph_edges.append({"source": str(edge[0]), "target": str(edge[1]), "label": str(edge[2]["weight"])})
    
    return json.dumps({"graph_nodes": graph_nodes, "graph_edges": graph_edges})

@app.route("/network", methods = ["GET", "POST"])
@cross_origin()
def network():
    graph = utilities.extract_graph(filename = "C:\\Users\\antho\\MedGraph\\src\\webapp\\data\\graph_ner.pkl")
    
    graph_nodes = []
    for node in graph.nodes:
        graph_nodes.append({"id": str(node), "label": str(node)})
        
    graph_edges = []
    for edge in graph.edges(data = True):
        graph_edges.append({"source": str(edge[0]), "target": str(edge[1]), "label": str(edge[2]["weight"])})

    return json.dumps({"graph_nodes": graph_nodes, "graph_edges": graph_edges})


if __name__ == "__main__":
    app.run(port = 5000, debug=True)
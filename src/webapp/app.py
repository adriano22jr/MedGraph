import utilities, flask, json
from flask_cors import cross_origin
from flask_visjs import VisJS4, Network

app = flask.Flask(__name__, template_folder = "templateFiles", static_folder = "staticFiles")
VisJS4().init_app(app)

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
def network():
    graph = utilities.extract_graph(filename = "data/graph_ner.pkl")

    network = Network("1500px", "1000px", directed = False)
    network.add_nodes(graph.nodes)

    count = 0

    for edge in graph.edges(data = True):
        if(count < 100):
            network.add_edge(int(edge[0]), int(edge[1]), title = edge[2]["weight"])
            print("Aggiunto l'arco: ", edge)
            count += 1

    return flask.render_template("ner_index.html", network = network)

if __name__ == "__main__":
    app.run(port = 5000, debug=True)
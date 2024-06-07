from flask_visjs import VisJS4, Network
import utilities, flask, time

app = flask.Flask(__name__, template_folder = "templateFiles", static_folder = "staticFiles")
VisJS4().init_app(app)

@app.route("/")
def index():
    graph = utilities.extract_graph(filename = "src/webapp/data/graph_meshterms.pkl")
    
    network = Network("650px", "1000px", directed = False)      
    network.add_nodes(graph.nodes)
    count = 0
    edges_set = frozenset(graph.edges)
    for edge in edges_set:
        print(count)
        count += 1
        if count > 10000: break
        network.add_edge(edge[0], edge[1], value = graph.get_edge_data(*edge)["weight"])
    return flask.render_template("index.html", network = network)


if __name__ == "__main__":
    app.run(port = 8080, debug=True)
    
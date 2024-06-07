import pymongo, networkx, pickle

def build_graph_from_meshterms(collection: pymongo.collection.Collection):
    graph = networkx.Graph()
    
    for document in collection.find():
        current_pmid = document["_id"]
        graph.add_node(current_pmid)
        
        for document2 in collection.find():
            count = 0
            if current_pmid != document2["_id"]:
                for key in document["mesh_terms"]:
                    if key in document2["mesh_terms"]: count += 1
            
            if count > 0:
                graph.add_edge(current_pmid, document2["_id"], weight = count)    

    return graph

def save_graph(filename: str, graph: networkx.Graph):
    file = open(filename, "wb")
    pickle.dump(graph, file)
    file.close()
    
def extract_graph(filename: str):
    file = open(filename, "rb")
    graph = pickle.load(file)
    file.close()
    return graph

if __name__ == "__main__":
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    database = client["MedGraph"]
    
    graph = build_graph_from_meshterms(collection = database["Dataset2000Entries"])
    save_graph(filename = "src/webapp/data/graph_meshterms.pkl", graph = graph)
    
    
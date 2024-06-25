import pymongo, networkx, pickle, json

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

def build_graph_from_labels():
    with open("data/entity_documents.json", "r") as f:
        data = json.load(f)

        pmid_to_labels = {}
        for pmid, values in data.items():
            pmid_to_labels[pmid] = set()
            
            for label in values.keys():
                entity = label.split(", ")[0]
                pmid_to_labels[pmid].add(entity)
                
    graph = networkx.Graph()
    graph.add_nodes_from(pmid_to_labels.keys())
    
    for pmid1 in pmid_to_labels:
        for pmid2 in pmid_to_labels:
            if pmid1 < pmid2:
                common_labels = pmid_to_labels[pmid1].intersection(pmid_to_labels[pmid2])        
                for item in common_labels:
                    graph.add_edge(pmid1, pmid2, weight = len(item))
    
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
    
    # graph = build_graph_from_meshterms(collection = database["Dataset2000Entries"])
     #save_graph(filename = "data/graph_meshterms.pkl", graph = graph)
    
    graph_ner = build_graph_from_labels()
    for edge in graph_ner.edges(data = True):
        print(edge)
        break
    save_graph(filename = "data/graph_ner.pkl", graph = graph_ner)
    
    
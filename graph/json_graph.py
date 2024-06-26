import json
from collections import defaultdict
import os

with open("entity_documents.json", 'r') as file:
    data = json.load(file)
    
    

'''"name": pmid,
"val": len(details),'''

# Creazione dei nodi
nodes = []
rootId = "25655077"
termkeys = []
for pmid, details in data.items():
    for key in details.keys():
        key = str(key).lower()
        termkeys.append(key)
        
    node = {
        "id": pmid,
        "collapsed": pmid != rootId,
        "childLinks": [],
        "val": len(details),
        "terms": list(set(termkeys))
    }
    nodes.append(node)
    termkeys = []

# Creazione dei link
links = []
terms_dict = defaultdict(list)

added_links = set()
for node in nodes:
    for term in node['terms']:
        for othernode in nodes:
            if term in othernode['terms']:
                if node['id'] != othernode['id'] and (node['id'], othernode['id'], term) not in added_links:
                    link = {
                        "source": node['id'],
                        "target": othernode['id'],
                        "term": term
                    }
                    links.append(link)
                    added_links.add((node['id'], othernode['id'], term))

print(len(links))



# Costruzione dell'output finale
output = {
    "nodes": nodes,
    "links": links
}

# Salva l'output in un nuovo file JSON
with open("output_file_json", 'w') as file:
    json.dump(output, file, indent=4)

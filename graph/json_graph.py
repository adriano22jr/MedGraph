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
for pmid, terms in data.items():
    '''for term in terms.keys():
        terms_dict[term].append(pmid)'''
    '''for node in nodes:
        
        link = {
                "source": source,
                "target": target,
                "term": term
        }
    links.append()'''
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

'''# Set per tenere traccia degli archi aggiunti (evita duplicati e auto-archi)
added_links = set()
for term, pmids in terms_dict.items():
    if len(pmids) > 1:
        for i in range(len(pmids)):
            for j in range(i + 1, len(pmids)):
                # Ordina i nodi per evitare duplicati invertiti
                source, target = sorted([pmids[i], pmids[j]])
                # Aggiungi l'arco solo se non è un auto-arco e non è già stato aggiunto
                if source != target and (source, target) not in added_links:
                    link = {
                        "source": source,
                        "target": target
                    }
                    links.append(link)
                    added_links.add((source, target))'''

# Costruzione dell'output finale
output = {
    "nodes": nodes,
    "links": links
}

# Salva l'output in un nuovo file JSON
with open("output_file_json", 'w') as file:
    json.dump(output, file, indent=4)

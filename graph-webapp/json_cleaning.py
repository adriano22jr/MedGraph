import json

def clean_nodes_and_links(filepath, output_file_path):
    with open(filepath, 'r') as file:
        data = json.load(file)
    
    def clean_dict(d, keys_to_remove):
        for key in keys_to_remove:
            if key in d:
                del d[key]

    keys_to_remove_from_nodes = ["val", "collapsed", "childLinks"]
    for node in data.get("nodes", []):
        clean_dict(node, keys_to_remove_from_nodes)

    keys_to_remove_from_links = ["term"]
    for link in data.get("links", []):
        clean_dict(link, keys_to_remove_from_links)

    with open(output_file_path, 'w') as file:
        json.dump(data, file, indent=4)

# Esempio di utilizzo
json_file_path = "graph-webapp/updated_output_file.json"
output_file_path = "graph-webapp/even_more_updated_output_file.json"
clean_nodes_and_links(json_file_path, output_file_path)
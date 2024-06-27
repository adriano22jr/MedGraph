from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from bson import ObjectId
import json

app = Flask(__name__, template_folder="templateFiles", static_folder="staticFiles")

# Configura la connessione a MongoDB
try:
    client = MongoClient("mongodb://localhost:27017/")
    db = client['MedGraph']
    collection = db['Dataset2000Entries']
    collection_authors = db['Authors']
except Exception as e:
    print("Errore nella connessione a MongoDB:", e)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def get_data():
    try:
        with open('graph/even_more_updated_output_file.json', 'r') as f:
            data = json.load(f)
        return jsonify(data)
    except Exception as e:
        print("Errore nel caricamento dei dati:", e)
        return jsonify({"error": "Errore nel caricamento dei dati"}), 500



@app.route('/node/<node_id>')
def get_node_details(node_id):
    try:
        node_id = int(node_id)
        node = collection.find_one({"_id": node_id}, {"title": 1, "Year": 1, "abstract": 1, "authors": 1})
        
        if node:
            # Recupera i dettagli degli autori
            author_ids = node.get('authors', [])
            authors = list(collection_authors.find({"_id": {"$in": [ObjectId(author_id) for author_id in author_ids]}}, {"_id": 0, "author": 1}))
            authors = [author['author'] for author in authors]
            node['authors'] = authors
            print(node)
            return jsonify(node)
        else:
            return jsonify({"error": "Node not found"}), 404
    except Exception as e:
        print("Errore nella ricerca del nodo:", e)
        return jsonify({"error": "Errore nella ricerca del nodo"}), 500

if __name__ == '__main__':
    app.run(debug=True)

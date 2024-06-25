const { readFile } = require('fs');
const request = require('request-promise');
const express = require('express');
const cors = require('cors'); // Add this line
const app = express();

app.use(cors()); // Add this line to enable CORS for all routes

app.get('/', (req, res) => {
    readFile('./index.html', 'utf-8', (err, html) => {
        if (err) {
            res.status(500).send("File not found!");
        }
        res.send(html);
    });
});

app.get('/meshterms_graph', (req, res) => {
    var options = { method: 'POST', uri: 'http://127.0.0.1:5000/meshterms_graph', json: true };
    request(options).then(function (parsedBody) {
        res.status(200).json({ nodes: parsedBody.graph_nodes, edges: parsedBody.graph_edges });
    }).catch(function (err) {
        console.log(err);
        res.status(500).send("Failed to fetch data");
    });
});

app.get('/ner_graph', (req, res) => {
    var options = { method: 'POST', uri: 'http://localhost:3000/ner_graph', json: true };
    request(options).then(function (parsedBody) {
        res.status(200).json({ nodes: parsedBody.graph_nodes, edges: parsedBody.graph_edges });
    }).catch(function (err) {
        console.log(err);
        res.status(500).send("Failed to fetch data");
    });
});

app.listen(process.env.PORT || 3000, () => console.log('Server is running on http://localhost:3000'));

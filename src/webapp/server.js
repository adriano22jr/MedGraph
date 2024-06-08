const {readFile} = require('fs');
var request = require('request-promise'); 
const express = require('express');
const app = express();


app.get('/', (request, response) => {
    readFile('./index.html', 'utf-8', (err, html) => {
        if(err){
            response.status(500).send("File not found!");
        }
        response.send(html);
    });
});

app.get('/meshterms_graph', (request, response) => {
    var options = {method: 'POST', uri: 'http://127.0.0.1:5000/meshterms_graph', json: true};
    var sendrequest = request(options).then(function (parsedBody) { 
        response.status(200).json({nodes: parsedBody["graph_nodes"], edges: parsedBody["graph_edges"]});
    }).catch(function (err) { 
        console.log(err); 
    });
});

app.listen(process.env.PORT || 3000, () => console.log('Server is running on http://localhost:3000'));
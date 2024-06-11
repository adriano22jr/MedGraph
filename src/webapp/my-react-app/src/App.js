import React, { useEffect, useState } from 'react';
import * as d3 from 'd3';
const App = () => {
    const [nodesCountVisible, setNodesCountVisible] = useState(false);
    const [edgesCountVisible, setEdgesCountVisible] = useState(false);

    const base_url = "/"

    useEffect(() => {
        
        const createGraph = (data) => {
            const width = 1920;
            const height = 1080;

            const svg = d3.select("#graph").append("svg")
                .attr("width", width)
                .attr("height", height)
                .call(d3.zoom().on("zoom", (event) => {
                    svg.attr("transform", event.transform);
                }))
                .append("g");

            const simulation = d3.forceSimulation(data.nodes)
                .force("link", d3.forceLink(data.edges).id(d => d.id))
                .force("center", d3.forceCenter(width / 2, height / 2))
                .force("charge", d3.forceManyBody().strength(-200));

            const link = svg.append("g")
                .attr("class", "links")
                .selectAll("line")
                .data(data.edges)
                .enter().append("line")
                .attr("stroke-width", 2)
                .attr("stroke", "#999");

            const node = svg.append("g")
                .attr("class", "nodes")
                .selectAll("circle")
                .data(data.nodes)
                .enter().append("circle")
                .attr("r", 5)
                .attr("fill", "#69b3a2")
                .call(d3.drag()
                    .on("start", dragstarted)
                    .on("drag", dragged)
                    .on("end", dragended))
                .on("mouseover", (event, d) => {
                    const [x, y] = d3.pointer(event);
                    svg.append("text")
                        .attr("x", x + 10)
                        .attr("y", y - 10)
                        .attr("id", "tooltip")
                        .attr("font-size", "12px")
                        .attr("fill", "#000")
                        .text(d.id);
                })
                .on("mouseout", () => {
                    svg.select("#tooltip").remove();
                });

            simulation
                .nodes(data.nodes)
                .on("tick", ticked);

            simulation.force("link")
                .links(data.edges);

            function ticked() {
                link
                    .attr("x1", d => d.source.x)
                    .attr("y1", d => d.source.y)
                    .attr("x2", d => d.target.x)
                    .attr("y2", d => d.target.y);

                node
                    .attr("cx", d => d.x)
                    .attr("cy", d => d.y);
            }

            function dragstarted(event, d) {
                if (!event.active) simulation.alphaTarget(0.3).restart();
                d.fx = d.x;
                d.fy = d.y;
            }

            function dragged(event, d) {
                d.fx = event.x;
                d.fy = event.y;
            }

            function dragended(event, d) {
                if (!event.active) simulation.alphaTarget(0);
                d.fx = null;
                d.fy = null;
            }
        };

        const getGraphData = async (event, endpoint) => {
            event.preventDefault();
            try {
                let response = await fetch(base_url + endpoint, {
                    method: "GET"
                });
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                let responseData = await response.text();
                try {
                    let data = JSON.parse(responseData);

                    setNodesCountVisible(true);
                    setEdgesCountVisible(true);

                    d3.select("#graph").select("svg").remove();

                    const gdata = {
                        nodes: data.graph_nodes,
                        edges: data.graph_edges,
                    };
                    createGraph(gdata);
                } catch (e) {
                    console.error("Failed to parse JSON:", responseData);
                    throw e;
                }
            } catch (error) {
                console.error("Failed to fetch graph data:", error);
            }
        };

        document.getElementById("get-graph-data-mesh").addEventListener("click", (event) => getGraphData(event, "meshterms_graph"));
        document.getElementById("get-graph-data-ner").addEventListener("click", (event) => getGraphData(event, "network"));
        document.getElementById("get-graph-test").addEventListener("click", async (event) => {
            event.preventDefault();
            try {
                let response = await fetch('https://assets.antv.antgroup.com/g6/60000.json');
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                let data = await response.json();

                d3.select("#graph").select("svg").remove();

                createGraph(data);
            } catch (error) {
                console.error("Failed to fetch test graph data:", error);
            }
        });
    }, []);

    return (
        <div>
            <form>
                <button id="get-graph-data-mesh">Click here to get graph from mesh terms</button>
                <button id="get-graph-data-ner">Click here to get graph from NER entities</button>
                <button id="get-graph-test">test 20k</button>
            </form>
            <h3 id="nodes-count" style={{ display: nodesCountVisible ? 'block' : 'none' }}>Nodes count: </h3>
            <h3 id="edges-count" style={{ display: edgesCountVisible ? 'block' : 'none' }}>Edges count: </h3>
            <div id="graph"></div>
        </div>
    );
};

export default App;

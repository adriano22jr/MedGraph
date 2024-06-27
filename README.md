# MedGraph 🧬

## What is MedGraph? 🤔

MedGraph is a project aimed at applying Knowledge Graphs in the domain of biomedical papers. To achieve this goal, MedGraph leverages Named Entity Recognition (NER) technologies to identify and classify entities mentioned in the abstracts of biomedical papers. These entities, along with their connections, are then represented in a knowledge graph.

The resulting graph not only facilitates the understanding of existing relationships between the papers but also allows for interactive and dynamic exploration of the data through a dedicated web app.

## How to run? ⚙️

In order to run the browser tool, please install the following libraries:

```sh
pip install -r requirements.txt
```

Then, run ```app.py``` and open the development server.

### ⚠️ Please keep in mind that, in order to correctly display nodes information, you need to be connect to the MedGraph database, currently local hosted. ⚠️

## Commands 🖱️

### Navigating the 3D Space 
- **Mouse-wheel**: Zoom.
- **Left-drag**: Rotate.
- **Right-drag**: Pan

### Nodes Interaction
- **Node Left-click**: Focus a node and show its links and details.
- **Node Right-click**: Opens the selected paper in a new tab (hyperlink to arxiv.org).

### Edges Interaction
- **Edge Left-click**: Shows infos on the selected link and the nodes connected by it.

## Credits 👨🏻‍👦🏻‍👦🏻

This project has been realized for the Fundamentals of Data Science and Machine Learning exam in University of Salerno by:

[Califano Adriano Emanuele](https://github.com/adriano22jr)

[Coccorullo David](https://github.com/davidcocc)

[Zunico Anthony](https://github.com/DJHeisenberg01)

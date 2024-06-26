from flask import Flask, render_template, jsonify
import json
app = Flask(__name__, template_folder="templateFiles", static_folder="staticFiles")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def get_data():
    with open('graph/even_more_updated_output_file.json', 'r') as f:
        data = json.load(f)
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)

    
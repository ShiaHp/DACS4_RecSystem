from flask import Flask, request, render_template
from elasticsearch import Elasticsearch
import pandas as pd
from flask_cors import CORS
import rec
es = Elasticsearch(hosts=["http://127.0.0.1:9200"])
print(f"Connected to ElasticSearch cluster `{es.info().body['cluster_name']}`")
movies_data = pd.read_csv('movie_dataset.csv', encoding="ISO-8859-1")
app = Flask(__name__)
CORS(app)
MAX_SIZE = 10

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/search")
def search_autocomplete():
    query = request.args["q"].lower()
    tokens = query
    clauses = {
                "match": {
                    "title": {
                        "query": tokens,
                        "fuzziness": 2,
                        "prefix_length": 1
                    }
                }
            }
    resp = es.search(index="movies",query=clauses, size=MAX_SIZE)
    print("Got %d Hits:" % resp['hits']['total']['value'])
    return [result['_source']['title'] for result in resp['hits']['hits']]
@app.route("/getReccommend")
def get_rec():
    query = request.args["q"].lower()
    tokens = query
    dataReturnFromRec = rec.getRef(movies_data, tokens)
    return dataReturnFromRec


if __name__ == "__main__":
    app.run(debug=True)

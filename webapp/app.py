from flask import Flask, request, jsonify
from cassandra.cluster import Cluster

cluster = Cluster(['cassandra'])
session = cluster.connect()
app = Flask(__name__)

@app.route('/')
def hello():
    name = request.args.get("name","World")
    str = "<p>Welcome to the cat facts API.</p> <p>You can query the api using the query like</p><p>URL/facts/10, URL/facts/5 etc</p>"
    return(str)


@app.route('/facts/<upvotes>')
def profile(upvotes):
    rows = session.execute( """Select * From facts.data where upvotes = '{}'""".format(upvotes))
    if len(rows)>0:
        return jsonify(rows)
    else:
        return('No record exist!')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

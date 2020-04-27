from flask import Flask, jsonify, request
from cassandra.cluster import Cluster
import json
import requests
cluster = Cluster(contact_points=['127.0.0.1'],port=9042)
session = cluster.connect()
app = Flask(__name__)

@app.route('/')
def hello():
    name = request.args.get("name","World")
    str1 = "<h1>Welcome to the cat facts API.</h1><br /><br />"
    str2 = "<p><h2>You can query the api using the url http://localhost/facts</h2></p><br />"
    str3 = "<p><h2>You can query the external api using the url http://localhost/facts/external</h2></p><br />"
    str4 = "<p><h2>Check the readme.md file for how to insert, update and delete a record</h2></p><br />"
    finalstr = str1 + str2 + str3 + str4

    return(finalstr)

# This is a call to get all data from local cassandra database.
# http://localhost:8080/facts
@app.route('/facts', methods=['GET'])
def facts():
    rows = session.execute( """Select * From facts.data""")
    result = []
    for record in rows:
        result.append({"id": record.id,"fact": record.fact,"type": record.type,"first_name": record.first_name,"last_name": record.last_name,"upvotes": record.upvotes})
    return jsonify(result)

# This is a call to external API.
# http://localhost:8080/facts/external
@app.route('/facts/external', methods=['GET'])
def external_api():
    url_template = 'https://cat-fact.herokuapp.com/facts'
    rates_url = url_template
    resp = requests.get(rates_url)
    if resp.ok:
        facts = resp.json()
        return jsonify(facts)
        # pprint(facts)
        # with open('facts.json', 'w') as json_file:
        #     json.dump(facts, json_file)
    else:
        print(resp.reason)

# To insert a record in local database
# curl -i -H "Content-Type: application/json" -X POST -d '{"id":245,"fact":"cats are cute","type":"cat","first_name":"first","last_name":"last","upvotes":10}' http://0.0.0.0:8080/facts/
@app.route('/facts/', methods=['POST'])
def create():
    session.execute("""INSERT INTO facts.data(id,fact,type,first_name,last_name,upvotes) VALUES ({},'{}','{}','{}','{}',{}) """.format(int(request.json['id']),request.json['fact'],request.json['type'],request.json['first_name'],request.json['last_name'],int(request.json['upvotes'])))
    return jsonify({'message':'created: /facts/{}'.format(request.json['id'])}),  201


# To update a record in local database
# To update number of votes (30) for a record with specific id (245)
# curl -i -H "Content-Type: application/json" -X PUT -d '{"id":245, "upvotes":30}' http://0.0.0.0:8080/facts/
@app.route('/facts/', methods=['PUT'])
def update():
    session.execute("""UPDATE facts.data SET upvotes= {} WHERE id={}""".format(int(request.json['upvotes']),int(request.json['id'])))
    return jsonify({'message':'updated: /facts/{}'.format(request.json['id'])}),  200



# To delete a record
# curl -i -H "Content-Type: application/json" -X DELETE -d '{"id":1}' http://0.0.0.0:8080/facts/

@app.route('/facts/', methods=['DELETE'])
def delete():
    session.execute("""DELETE FROM facts.data WHERE id={}""".format(int(request.json['id'])))
    return jsonify({'message':'deleted: /facts/{}'.format(request.json['id'])}),  200




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=443, ssl_context=('cert.pem', 'key.pem'))

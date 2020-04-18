from flask import Flask, render_template, request, jsonify
import json
import sys
import requests_cache
import requests
from pprint import pprint

app = Flask(__name__)

url_template = 'https://cat-fact.herokuapp.com/facts'

@app.route('/facts', methods=['GET'])
def facts():

    rates_url = url_template

    resp = requests.get(rates_url)

    if resp.ok:
        facts = resp.json()
        pprint(facts)
        with open('facts.json', 'w') as json_file:
            json.dump(facts, json_file)

    else:
        print(resp.reason)
    return jsonify(facts)     # return json file

if __name__=="__main__":
    app.run(port=8081, debug=True)


from flask import Flask, jsonify, json
with open('records.json') as f:
   all_records = json.load(f)
app = Flask(__name__)

@app.route('/records', methods=['GET'])
def get_all_records():
   return jsonify(all_records)




if __name__ == '__main__':
   app.run(debug=True)

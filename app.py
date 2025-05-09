from flask import Flask, request, jsonify
import csv
import io

app = Flask(__name__)

@app.route('/parse-csv', methods=['POST'])
def parse_csv():
    file = request.data
    decoded = file.decode("utf-8")
    sample = decoded[:1024]
    
    sniffer = csv.Sniffer()
    dialect = sniffer.sniff(sample)
    
    reader = csv.DictReader(io.StringIO(decoded), dialect=dialect)
    rows = list(reader)

    return jsonify(rows)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

from flask import Flask, request, jsonify
import csv
import io

app = Flask(__name__)

@app.route("/", methods=["POST"])
def parse_csv():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    uploaded_file = request.files['file']
    if uploaded_file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        # Try detecting the delimiter automatically
        content = uploaded_file.read().decode("utf-8", errors="ignore")
        sniffer = csv.Sniffer()
        dialect = sniffer.sniff(content.splitlines()[0])
        delimiter = dialect.delimiter

        # Reset file pointer
        uploaded_file.stream.seek(0)
        decoded_stream = io.StringIO(content)
        reader = csv.reader(decoded_stream, delimiter=delimiter)

        # Optional: skip header
        rows = list(reader)[1:]

        # Build response for testing
        return jsonify({
            "rows": rows[:5],  # return first 5 rows just to test
            "delimiter": delimiter
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


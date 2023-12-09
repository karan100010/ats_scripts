from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/data', methods=['GET'])
def get_data():
    # Replace this with your actual data or data retrieval logic
    data = {
        'value': 42,
        'timestamp': '2023-01-01T12:00:00',
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)

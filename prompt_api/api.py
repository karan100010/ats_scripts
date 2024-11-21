from flask import Flask, request, jsonify
import time
import re
from guidance import gen, select, system, user, assistant,models

app = Flask(__name__)


@app.route('/get_reply', methods=['POST'])
def genrate_next():
    





if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5015)

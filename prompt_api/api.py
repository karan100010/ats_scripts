from flask import Flask, request, jsonify
import time
import re
from guidance import gen, select, system, user, assistant,models

app = Flask(__name__)
model=models.Transformers("microsoft/Phi-3.5-mini-instruct")

@app.route('/get_reply', methods=['POST'])
def genrate_next():
    messages = request['messages']

# Check if the first message is from 'system' role
    if messages and messages[0]['role'] == 'system':
        system_message = messages[0]['content']
        # Write the system prompt at the top
        with system():
            model += f"""{system_message}"""
    role_messages = {}
    for message in parsed_data['messages']:
        role = message.get('role')
        if role not in role_messages:
            role_messages[role] = []
        role_messages[role].append(message['content'])
        for message in messages:
            role = message['role']
            content = message['content']
            if role == 'user':
                with user():
                    model += f"""{content}
        """
            elif role == 'assistant':
                with assistant():
                    model += f"""{content}
"""





if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5015)

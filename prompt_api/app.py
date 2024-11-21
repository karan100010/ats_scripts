import guidance
#from guidance import system, user, assistant,gen
from flask import Flask, request, jsonify
import time
import re
from guidance import gen, select, system, user, assistant,models

model=models.Transformers("microsoft/Phi-3.5-mini-instruct")

# app = Flask(__name__)

# @app.route('/get_reply', methods=['POST'])
# @guidance

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5015)

class ConversationAgent:
    def __init__(self, chat_model, name: str, instructions: str, context_turns: int = 2):
        self._chat_model = chat_model
        self._name = name
        self._instructions = instructions
        self._my_turns = []
        self._interlocutor_turns = []
        self._went_first = True
        self._context_turns = context_turns

    @property
    def name(self) -> str:
        return self._name
    
    def reply(self, interlocutor_reply = None) -> str:
        if interlocutor_reply is None:
            self._my_turns = []
            self._interlocutor_turns = []
            self._went_first = True
        else:
            self._interlocutor_turns.append(interlocutor_reply)

        # Get trimmed history
        my_hist = self._my_turns[(1-self._context_turns):]
        interlocutor_hist = self._interlocutor_turns[-self._context_turns:]

        # Set up the system prompt
        curr_model = self._chat_model
        with system():
            curr_model += f"Your name is {self.name}. {self._instructions}"
            if len(interlocutor_hist) == 0:
                curr_model += "Introduce yourself and start the conversation"
            elif len(interlocutor_hist) == 1:
                curr_model += "Introduce yourself before continuing the conversation"

        # Replay the last few turns
        for i in range(len(my_hist)):
            with user():
                curr_model += interlocutor_hist[i]
            with assistant():
                curr_model += my_hist[i]

        if len(interlocutor_hist) > 0:
            with user():
                curr_model += interlocutor_hist[-1]

        with assistant():
            curr_model += gen(name='response', max_tokens=100)
        time.sleep(2)

        self._my_turns.append(curr_model['response'])
        return curr_model['response']
    

class HumanAgent:
    def __init__(self, chat_model, name: str, instructions: str, context_turns: int = 2):
        self._chat_model = chat_model
        self._name = name
        self._instructions = instructions
        self._my_turns = []
        self._interlocutor_turns = []
        self._went_first = True
        self._context_turns = context_turns

    @property
    def name(self) -> str:
        return self._name
    
    def reply(self, interlocutor_reply = None) -> str:
        if interlocutor_reply is None:
            self._my_turns = []
            self._interlocutor_turns = []
            self._went_first = True
        else:
            self._interlocutor_turns.append(interlocutor_reply)

        # Get trimmed history
        my_hist = self._my_turns[(1-self._context_turns):]
        interlocutor_hist = self._interlocutor_turns[-self._context_turns:]

        # Set up the system prompt
        curr_model = self._chat_model
        with system():
            curr_model += f"Your name is {self.name}. {self._instructions}"
            if len(interlocutor_hist) == 0:
                curr_model += "Introduce yourself and start the conversation"
            elif len(interlocutor_hist) == 1:
                curr_model += "Introduce yourself before continuing the conversation"

        # Replay the last few turns
        for i in range(len(my_hist)):
            with user():
                curr_model += interlocutor_hist[i]
            with assistant():
                curr_model += my_hist[i]

        if len(interlocutor_hist) > 0:
            with user():
                curr_model += interlocutor_hist[-1]

        with assistant():
            curr_model += gen(name='response', max_tokens=100)
        time.sleep(2)

        self._my_turns.append(curr_model['response'])
        return curr_model['response']
    

def conversation_simulator(
        bot0: ConversationAgent,
        bot1: HumanAgent,
        total_turns: int = 5 ):
        conversation_turns = []
        last_reply = None
        for _ in range(total_turns):
            last_reply = bot0.reply(last_reply)
            conversation_turns.append(dict(name=bot0.name, text=last_reply))
            last_reply = bot1.reply(last_reply)
            conversation_turns.append(dict(name=bot1.name, text=last_reply))
        return conversation_turns

bot_instructions = """You are taking part in discussions with clients as a loan recovery agent.
Only generate text as yourself and do not prefix your reply with your name.
Keep your answers to a couple of short sentences."""
bot2_instructions = """You are a clinet taking to recovery agent. Speak in short single sentences """



bradman_bot = ConversationAgent(model, "Vinod", bot_instructions, context_turns=5)
jardine_bot = ConversationAgent(model, "Sumit", bot2_instructions, context_turns=5)

conversation_turns = conversation_simulator(bradman_bot, jardine_bot, total_turns=1)

for turn in conversation_turns:
    print(f"{turn['name']}: {turn['text']}\n")
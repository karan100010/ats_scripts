import guidance
#from guidance import system, user, assistant,gen
from flask import Flask, request, jsonify
import time
import re
from guidance import gen, select, system, user, assistant,models

model=models.Transformers("microsoft/Phi-3.5-mini-instruct")

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
    def __init__(self, name: str):
        self._name = name

    @property
    def name(self) -> str:
        return self._name
    
    def reply(self, interlocutor_reply = None) -> str:
        if interlocutor_reply is not None:
            print(f"{interlocutor_reply}\n")
        user_reply = input(f"{self.name}: ")
        return user_reply

def conversation_simulator(
        bot: ConversationAgent,
        human: HumanAgent,
        total_turns: int = 5 ):
    conversation_turns = []
    last_reply = None
    for _ in range(total_turns):
        last_reply = bot.reply(last_reply)
        conversation_turns.append(dict(name=bot.name, text=last_reply))
        last_reply = human.reply(last_reply)
        conversation_turns.append(dict(name=human.name, text=last_reply))
    return conversation_turns

bot_instructions = """You are taking part in discussions with clients as a loan recovery agent.
Only generate text as yourself and do not prefix your reply with your name.
Keep your answers to a couple of short sentences."""

bradman_bot = ConversationAgent(model, "Vinod", bot_instructions, context_turns=5)
human_user = HumanAgent("You")

conversation_turns = conversation_simulator(bradman_bot, human_user, total_turns=5)

for turn in conversation_turns:
    print(f"{turn['name']}: {turn['text']}\n")

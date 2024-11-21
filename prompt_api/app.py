import guidance
#from guidance import system, user, assistant,gen
from flask import Flask, request, jsonify
import time
import re
from guidance import gen, select, system, user, assistant,models

model=models.Transformers("microsoft/Phi-3.5-mini-instruct")

app = Flask(__name__)

@app.route('/get_reply', methods=['POST'])
@guidance
class LoanRecoveryAgent:
    def __init__(self, chat_model, agent_name: str, instructions: str, context_turns: int = 2):
        """
        Initializes the Loan Recovery Agent.

        Args:
            chat_model: The chat model used to generate responses.
            agent_name: The name of the loan recovery agent.
            instructions: Instructions for the agent's behavior and tone.
            context_turns: Number of previous turns to retain for context.
        """
        self._chat_model = chat_model
        self._agent_name = agent_name
        self._instructions = instructions
        self._agent_turns = []
        self._user_turns = []
        self._started_conversation = False
        self._context_turns = context_turns

    @property
    def agent_name(self) -> str:
        """Returns the name of the loan recovery agent."""
        return self._agent_name

    def reply(self, user_reply=None) -> str:
        """
        Generates a reply based on the user's input and conversation history.

        Args:
            user_reply: The user's latest message. If None, starts a new conversation.

        Returns:
            The agent's response.
        """
        if user_reply is None:
            # Start a new conversation
            self._agent_turns = []
            self._user_turns = []
            self._started_conversation = True
        else:
            # Record the user's reply
            self._user_turns.append(user_reply)

        # Trim the history to maintain context
        agent_history = self._agent_turns[-self._context_turns:]
        user_history = self._user_turns[-self._context_turns:]

        # Set up the conversation model
        curr_model = self._chat_model
        curr_model += f"Your name is {self.agent_name}. You are a professional loan recovery agent. {self._instructions} "

        # Add system instructions for starting or continuing the conversation
        if len(user_history) == 0:
            curr_model += "Start the conversation by introducing yourself and explaining the purpose of your call."
        elif len(user_history) == 1:
            curr_model += "Introduce yourself briefly before continuing the conversation."

        # Replay the conversation history
        for i in range(len(agent_history)):
            curr_model += f"\nUser: {user_history[i]}\nAgent: {agent_history[i]}"

        if len(user_history) > 0:
            curr_model += f"\nUser: {user_history[-1]}"

        # Generate the agent's reply
        curr_model += "\nAgent:"
        agent_response = self._generate_response(curr_model)
        self._agent_turns.append(agent_response)
        return agent_response

    def _generate_response(self, prompt: str) -> str:
        """
        Simulates generating a response from the chat model.

        Args:
            prompt: The conversation prompt including instructions and history.

        Returns:
            The generated response.
        """
        # Replace with actual chat model call in production
        simulated_response = f"Simulated response based on prompt: {prompt}"
        return simulated_response

        
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5015)
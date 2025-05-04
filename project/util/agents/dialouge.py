import re
from .agent import Agent
from ..llm_agent_utils import output_message
from ..IO import cmd_output, chatroom_output, get_user_input

class dialogue_agent(Agent):
    
    def __init__(self, agent_info, game_state, agents):
        self.data = agent_info
        self.game_state = game_state
        self.agents = agents  

    def handle(self, tag):
        # Initial message sent to the DM (or other agents in the system)
        output_message(
            agents=self.agents,
            agentsTags=["DM", tag[0]],
            message=["dialogue", tag[1]],
            IO=[chatroom_output]
        )
        self.add_message(tag)

        while True:
            # Generate the next response using LLM (Dialogue Agent’s assistant)
            response = self.generate()
            message_text = response["message"]["message"]["content"]

            # Output the generated message to the chat
            output_message(
                agents=self.agents,
                agentsTags=["DM", tag[0]],
                message=["dialogue", message_text],
                IO=[chatroom_output]
            )

            # Check if conversation should end (this can be customized)
            if re.search(r"END(.*)CONVERSATION", message_text, re.DOTALL):
                output_message(
                    agents=self.agents,
                    agentsTags=["DM", tag[0]],
                    message=["dialogue", "Conversation complete."],
                    IO=[chatroom_output]
                )
                return response

            # Add the assistant's message to the agent's message log
            self.data["agent_template"]["messages"].append({
                "role": "assistant",
                "content": message_text
            })

            # Get user input to continue the dialogue
            user_msg = get_user_input()

            # Output the user’s response to the chat
            output_message(
                agents=self.agents,
                agentsTags=["DM", tag[0]],
                message=["user", user_msg],
                IO=[]
            )

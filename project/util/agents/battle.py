# not working for some reason idk


import re
from .agent import Agent
from ..llm_agent_utils import output_message
from ..IO import cmd_output, chatroom_output, get_user_input
from ..llm_agent_utils import process_tags

class battle_agent(Agent):

    def __init__(self, agent_info, game_state, agents):
        self.data = agent_info
        self.game_state = game_state
        self.agents = agents  

    def handle(self, tag):
        # Send initial battle message to the DM
        output_message(
            agents=self.agents,
            agentsTags=["DM", tag[0]],
            message=["battle", tag[1]],
            IO=[chatroom_output]
        )
        self.add_message(tag)

        while True:
            # Generate battle action
            response = self.generate()
            message_text = response["message"]["message"]["content"]

            # Output battle action to the chat
            output_message(
                agents=self.agents,
                agentsTags=["DM", tag[0]],
                message=["battle", message_text],
                IO=[chatroom_output]
            )

            process_tags(response, self.agents)

            # Check if the battle is over
            if re.search(r"Battle(.*)END", message_text, re.DOTALL):
                output_message(
                    agents=self.agents,
                    agentsTags=["DM", tag[0]],
                    message=["battle", "Battle sequence complete."],
                    IO=[chatroom_output]
                )
                return response

            # Add assistant's battle message to agent template
            self.data["agent_template"]["messages"].append({
                "role": "assistant",
                "content": message_text
            })

            # Get user input for next battle move
            user_msg = get_user_input()

            output_message(
                agents=self.agents,
                agentsTags=["DM", tag[0]],
                message=["user", user_msg],
                IO=[chatroom_output]
            )

            

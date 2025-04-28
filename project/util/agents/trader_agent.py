import re
from .agent import Agent
from ..llm_agent_utils import output_message
from ..IO import cmd_output, chatroom_output

class trader_agent(Agent):
    
    def __init__(self, agent_info, game_state, agents):
        self.data = agent_info
        self.game_state = game_state
        self.agents = agents  

    def handle(self, tag):
        output_message(
            agents=self.agents,
            agentsTags=["DM", tag[0]],
            message=["trader", tag[1]],
            IO=[chatroom_output]
        )
        self.add_message(tag)

        while True:
            response = self.generate()
            message_text = response["message"]["message"]["content"]

            # Use output_message instead of print
            output_message(
                agents=self.agents,
                agentsTags=["DM", tag[0]],
                message=["trader", message_text],
                IO=[chatroom_output]
            )

            # Check if trade is done
            if re.search(r"TRADE(.*)DONE", message_text, re.DOTALL):
                output_message(
                    agents=self.agents,
                    agentsTags=["DM", tag[0]],
                    message=["trader", "Trade sequence complete."],
                    IO=[chatroom_output]
                )
                return response

            # Add assistant's message
            self.data["agent_template"]["messages"].append({
                "role": "assistant",
                "content": message_text
            })

            # Prompt user for input
            output_message(
                agents=self.agents,
                agentsTags=["DM", tag[0]],
                message=["user", "Your input: "],
                IO=[chatroom_output]
            )

            user_msg = input()

            output_message(
                agents=self.agents,
                agentsTags=["DM", tag[0]],
                message=["user", user_msg],
                IO=[chatroom_output]
            )

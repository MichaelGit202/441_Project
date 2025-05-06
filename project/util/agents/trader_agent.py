import re
from .agent import Agent
from ..llm_agent_utils import output_message
from ..IO import cmd_output, chatroom_output, get_user_input
from ..image_creation import generateImage  # Import the image generator


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
            print("MESSAGE TEXT \n\n"+message_text+"MESSAGE TEXT DONE\n\n")
            trade_match = re.search(r"TRADE\((.*)\)DONE", message_text, re.DOTALL)
            if trade_match:
                trade_description = trade_match.group(1).strip()
                print("Trade Description: "+trade_description)
                generateImage(trade_description)  # Call image generator
                
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


            user_msg = get_user_input()

            output_message(
                agents=self.agents,
                agentsTags=["DM", tag[0]],
                message=["user", user_msg],
                IO=[]
            )

import random
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

    def handle(self, args):
        #this is here because of old jank:
        tag = [args[0], args[1]["prompt"]]

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
            print("TOP++++++=s")
            print(response["message"]["message"])
            message_text = response["message"]["message"]["content"]

            # Output battle action to the chat
            output_message(
                agents=self.agents,
                agentsTags=["DM", tag[0]],
                message=["battle", message_text],
                IO=[chatroom_output]
            )


            # Check if the battle is over
            if re.search(r"Battle(.*)END", message_text, re.DOTALL | re.IGNORECASE):
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
            self.add_message(["user", user_msg])
            
            output_message(
                agents=self.agents,
                agentsTags=["DM", tag[0]],
                message=["user", user_msg],
                IO=[]
            )
            
            rng_value = self.rng(100)
            rng_msg = f"(Rolling a d{100}... You rolled a {rng_value})"

            rng_result_msg = ["RNGCall", rng_msg]
            self.add_message(rng_result_msg)
            
            output_message(
                agents=self.agents,
                agentsTags=["DM", tag[0]],
                message=rng_result_msg,
                IO=[chatroom_output]
            )

    def rng(self, upper_bound):
        return random.randint(1, upper_bound)

            
#"tools": [
#        {
#          "type": "function",
#          "function": {
#            "name": "retrieve_context_tool",
#            "description": "Used to retrieve context from files containing data that may be relevant to users' questions.",
#            "parameters": {
#              "type": "object",
#              "properties": { 
#                "user_prompt": {"type" : "string"}
#              }
#            }
#          }
#        }
#      ]
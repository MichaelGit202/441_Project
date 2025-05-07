import re
from .agent import Agent
from ..llm_agent_utils import output_message, proccess_tool_calls
from ..IO import cmd_output, chatroom_output, get_user_input

class dialogue_agent(Agent):
    
    def __init__(self, agent_info, game_state, agents):
        self.data = agent_info
        self.game_state = game_state
        self.agents = agents  

    def handle(self, args):
        # Old format handling
        tag = [args[0], args[1]["prompt"]]

        # Initial message sent to the DM (or other agents in the system)
        output_message(
            agents=self.agents,
            agentsTags=["DM", tag[0]],
            message=["dialogue", tag[1]],
            IO=[chatroom_output]
        )
        self.add_message(tag)

        while True:
            # Generate the next response from the LLM
            response = self.generate()
            message = response["message"]["message"]
            
            # Process any tool calls returned
            if "tool_calls" in message:
                proccess_tool_calls(message["tool_calls"], self.agents)

            # Output the generated content
            message_text = message.get("content", "")
            if message_text:
                output_message(
                    agents=self.agents,
                    agentsTags=["DM", tag[0]],
                    message=["dialogue", message_text],
                    IO=[chatroom_output]
                )

                # Add the assistant message to history
                self.data["agent_template"]["messages"].append({
                    "role": "assistant",
                    "content": message_text
                })

            # End the conversation if cue is found
            if re.search(r"END(.*)CONVERSATION", message_text, re.DOTALL | re.IGNORECASE):
                output_message(
                    agents=self.agents,
                    agentsTags=["DM", tag[0]],
                    message=["dialogue", "Conversation complete."],
                    IO=[chatroom_output]
                )
                return response

            # Get next user input
            user_msg = get_user_input()

            # Output and store the user's input
            output_message(
                agents=self.agents,
                agentsTags=["DM", tag[0]],
                message=["user", user_msg],
                IO=[]
            )

            self.data["agent_template"]["messages"].append({
                "role": "user",
                "content": user_msg
            })

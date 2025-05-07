from .agent import Agent
import random
import re
from ..llm_agent_utils import output_message
from ..IO import cmd_output, get_user_input, chatroom_output

class rng_agent(Agent):
    def __init__(self, agent_info, game_state, agents):
        self.data = agent_info
        self.game_state = game_state
        self.agents = agents

        if "tools" in agent_info:
            self.load_tools(agent_info["tools"])

        self.tool_calls = {
            "RNGCALL": self.rng,
        }

    def handle(self, args):
        """
        Handles an RNG tool call by prompting the player, simulating a roll, and 
        outputting the result with optional narrative generation.
        """
        tag = [args[0], args[1]["prompt"]]  # ["tag name", "prompt content"]

        formatted_tag = ["DM", tag[1]]

        # Step 1: Output the DM prompt to the player
        output_message(
            agents=self.agents,
            agentsTags=["DM", tag[0]],
            message=formatted_tag,
            IO=[chatroom_output]
        )

        self.add_message(tag)
        prompt = self.generate()

        # Step 1.5: Output the generated message
        output_message(
            agents=self.agents,
            agentsTags=["DM", tag[0]],
            message=["RNGCall", prompt["message"]["message"]["content"]],
            IO=[chatroom_output]
        )

        # Step 2: Get player input and store it
        user_input = get_user_input()
        self.add_message(user_input)

        output_message(
            agents=self.agents,
            agentsTags=["RNGCall", tag[0]],
            message=["user", user_input],
            IO=[]
        )

        # Step 3: Perform RNG roll
        try:
            upper = tag[1].upper_bound
        except:
            upper = 100

        rng_value = self.rng(upper)
        rng_msg = f"(Rolling a d{upper}... You rolled a {rng_value})"

        rng_result_msg = ["RNGCall", rng_msg]
        self.add_message(rng_result_msg)

        output_message(
            agents=self.agents,
            agentsTags=["DM", tag[0]],
            message=rng_result_msg,
            IO=[chatroom_output]
        )

        # Step 4: Generate a final response based on all prior context
        final_response = self.generate()
        print(final_response)

        output_message(
            agents=self.agents,
            agentsTags=["DM", tag[0]],
            message=["RNGCall", final_response["message"]["message"]["content"]],
            IO=[chatroom_output]
        )

        self.clear_message_history()
        return final_response

    def parse_upper_bound(self, tag_content):
        """
        Parses an upper bound from tag content using regex (e.g. 'max=20').
        Defaults to 100 if not specified.
        """
        match = re.search(r'max\s*=\s*(\d+)', tag_content)
        if match:
            return int(match.group(1))
        return 100

    def rng(self, upper_bound):
        """
        Rolls a random number between 1 and the given upper bound.
        """
        return random.randint(1, upper_bound)

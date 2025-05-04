from .agent import Agent
import random
import re  # regex >:(
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

#TODO, change the name of 'tag' because it makes no sense
# tag is a "[tag, message]" tuple
# this handle function is a complete mess btw
    def handle(self, tag):

        #TODO implement a method for figuring out who called the thing
        # this could be important for tying rng agent to something like battle agent
        caller = self.parse_caller(tag)

        #IDK why its coming ad ["rngcall", tag content]
        formatted_tag = ["DM", tag[1]]
        # Step 1: Ask the player what they want to do
   
        output_message(
            agents=self.agents,
            agentsTags=["DM", tag[0]], #caller goes here if exists
            message=formatted_tag,
            IO=[chatroom_output]
        )

        self.add_message(tag)
        prompt = self.generate()

        # Step 1.5: Output DM's prompt to the player
        output_message(
            agents=self.agents,
            agentsTags=["DM", tag[0]],
            message=["RNGCall", prompt["message"]["message"]["content"]],
            IO=[chatroom_output]
        )

        # Step 2: Get player input
        user_input = get_user_input()
        
        self.add_message(user_input)

        output_message(
            agents=self.agents,
            agentsTags=["RNGCall", tag[0]],
            message=["user", user_input],
            IO=[]
        )


        # Step 3: Perform RNG and interpret result
        upper = self.parse_upper_bound(tag[1])
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

        # Step 4: Final interpretation
        final_response = self.generate()

        print(final_response)

        output_message(
            agents=self.agents,
            agentsTags=["DM", tag[0]],
            message=["RNGCall",final_response["message"]["message"]["content"]],
            IO=[chatroom_output]
        )
        return final_response

    def parse_upper_bound(self, tag_content):
        match = re.search(r'max\s*=\s*(\d+)', tag_content)
        if match:
            return int(match.group(1))
        return 100  # default upper bound

    def rng(self, upper_bound):
        return random.randint(1, upper_bound)

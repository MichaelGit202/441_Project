from .agent import Agent
import random
import re #regex >:(

class rng_agent(Agent):

    def __init__(self, agent_info,  game_state, agents):  
        self.data = agent_info
        self.game_state = game_state
        self.agents = agents  


        keys = agent_info.keys()
        if ("tools" in keys):
            self.load_tools(agent_info["tools"])
        
        self.tool_calls = {  
            "RNGCALL" : self.rng,
        }

        print(self.tool_calls["RNGCALL"](10))

    def handle(self, tag):
        # Step 1: Ask the player what they want to do
        print(tag)
        self.add_message(tag)  # DM prompt: "What do you do?"
        prompt = self.generate()
        self.add_message(["RNGCall", prompt["message"]["message"]["content"]])
        print(prompt["message"]["message"]["content"])
        # Step 2: Get player input
        user_input = input()
        self.add_message(["user", user_input])
        
        # Step 3: Perform RNG and interpret result
        upper = self.parse_upper_bound(tag[1])
        rng_value = self.rng(upper)
        rng_msg = f"(Rolling a d{upper}... You rolled a {rng_value})"
        self.add_message(["RNGCall", rng_msg])
        print(rng_msg)
        # Step 4: Final DM interpretation
        return self.generate()
    
    def parse_upper_bound(self, tag_content):
        match = re.search(r'max\s*=\s*(\d+)', tag_content)
        if match:
            return int(match.group(1))
        return 100  # default upper bound
    
    def rng(self, upper_bound):
        return random.randint(0, upper_bound)



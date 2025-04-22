from .agent import Agent
import random

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
        self.add_message(tag)
        return self.generate()
    
    def rng(self, upper_bound):
        return random.randint(0, upper_bound)




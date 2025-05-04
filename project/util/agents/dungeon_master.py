from .agent import Agent
from ..game_state import GameState

class dungeon_master(Agent):
    

    def __init__(self, agent_info, game_state, agents):
        self.game_state = game_state
        self.agents = agents  
        self.data = agent_info
        keys = agent_info.keys()
        if ("tools" in keys):
            self.load_tools(agent_info["tools"])

            tool_calls = {  
        #example rng_tag : rng_function
        }
    
    def handle(self, tag):
        self.add_message(tag)
        return self.generate()
    

        
    

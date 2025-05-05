from .agent import Agent
from ..game_state import GameState
from ..IO import chatroom_output

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
            
    #this is the weird part where i just want the dm to narrate but 
    # still need a handle function lol
    def handle(self, tag):
        return tag
    

        
    

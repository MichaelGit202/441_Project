from .agent import Agent
from ..game_state import GameState
from ..IO import chatroom_output, get_user_input
from ..llm_agent_utils import proccess_tool_calls, output_message

class dungeon_master(Agent):
    

    def __init__(self, agent_info, game_state, agents):
        self.game_state = game_state
        self.agents = agents  
        self.data = agent_info
        #keys = agent_info.keys()
        #if ("tools" in keys):
        #    self.load_tools(agent_info["tools"])

            
    #this is the weird part where i just want the dm to narrate but 
    # still need a handle function lol
    def handle(self):
        dm_response = self.generate()
        print(dm_response)

        if dm_response["message"]["message"]["content"] != "":
            self.add_message(["user" , "If you want to say something to the user use a function"])
        

        if  "tool_calls" in dm_response["message"]["message"]:
            proccess_tool_calls(dm_response["message"]["message"]["tool_calls"], self.agents)


        #i hate llms so much
        #fall back if guy said nothing
        
        if dm_response["message"]["message"]["content"] == "" and "tool_calls" not in dm_response["message"]["message"]:
            print("fall back triggered")
            user_msg = get_user_input()
            output_message(
                agents=self.agents,
                agentsTags=["DM"],
                message=["user", user_msg],
                IO=[]
            )
        

        return dm_response

    

        
    

#why does this exist, because I need a tool call that just has the dungeon master speak because he likes to only use tool calls 

from .agent import Agent
from ..llm_agent_utils import output_message 
from ..IO import chatroom_output

class dungeon_master_speak(Agent):
    
    def handle(self, args): 
        #print(self.agents["DM"].data["agent_template"]["messages"])
        output_message(
            agents=self.agents,
            agentsTags=["DM"],
            message=["DM", args[1]["prompt"]],
            IO=[chatroom_output]
        )
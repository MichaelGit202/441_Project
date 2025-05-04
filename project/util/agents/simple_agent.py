from .agent import Agent
from ..llm_agent_utils import output_message 
from ..IO import chatroom_output
#this is basically just a Question answer agent, one prompt one response
class simple_response_agent(Agent):
    
    def handle(self, tag): 
        self.add_message(tag)
        msg = self.generate()
        output_message(
            agents=self.agents,
            agentsTags=["DM", tag[0]],
            message=[tag[0], msg["message"]["message"]["content"]],
            IO=[chatroom_output]
        )
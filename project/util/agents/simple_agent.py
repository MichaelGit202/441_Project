from .agent import Agent
from ..llm_agent_utils import output_message 
from ..IO import chatroom_output
#this is basically just a Question answer agent, one prompt one response
class simple_response_agent(Agent):
    
    def handle(self, args): 
        #this is here because of old jank:
        print(args[0] + " triggered from SRA")
        tag = [args[0], args[1]["prompt"]]

        output_message(
            agents=self.agents,
            agentsTags=["DM", tag[0]],
            message=tag,
            IO=[chatroom_output]
        )

        print("cha")
        
        msg = self.generate()
        output_message(
            agents=self.agents,
            agentsTags=["DM", tag[0]],
            message=[tag[0], msg["message"]["message"]["content"]],
            IO=[chatroom_output]
        )
        self.clear_message_history()
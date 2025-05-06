from .agent import Agent
from ..IO import chatroom_output, chatroom_output, get_user_input
from ..llm_agent_utils import output_message

#this is basically just a Question answer agent, one prompt one response
class player_input(Agent):
    def handle(self, args): 
        tag = [args[0], args[1]["prompt"]]

        output_message(
            agents=self.agents,
            agentsTags=["DM", tag[0]],
            message=["DM", tag[1]],
            IO=[chatroom_output]
        )

        user_msg = get_user_input()

        output_message(
            agents=self.agents,
            agentsTags=["DM", tag[0]],
            message=["user", user_msg],
            IO=[]
        )

        return user_msg
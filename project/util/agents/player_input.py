from .agent import Agent
from ..IO import chatroom_output, chatroom_output, get_user_input
from ..llm_agent_utils import output_message

#this is basically just a Question answer agent, one prompt one response
class player_input(Agent):
    def handle(self, tag): 
        user_msg = get_user_input()

        output_message(
            agents=self.agents,
            agentsTags=["DM", tag[0]],
            message=["user", user_msg],
            IO=[chatroom_output]
        )

        return user_msg
from .agent import Agent

#this is basically just a Question answer agent, one prompt one response
class simple_response_agent(Agent):
    
    def handle(self, tag): 
        self.add_message(tag)
        return self.generate()
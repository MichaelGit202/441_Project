import ollama
from ..IO import cmd_output
from ..llm_agent_utils import output_message

class Agent:
    default_output = cmd_output

    data = {
        #everything from the json file
    }
    # I added this tool call thing for tool definitions in the json
    tool_calls = {  
        #example rng_tag : rng_function
    }
    agents = [] # list of all agents, this is by reference according to g4g
    

    def __init__(self, agent_info, game_state, agents):
        self.game_state = game_state
        self.agents = agents  
        self.data = agent_info
        keys = agent_info.keys()
        if ("tools" in keys):
            self.load_tools(agent_info["tools"])


    def load_tools(self,tools): 
        for tool in tools:
            if(tool["type"] == "function"):
                tag = tool["function"]["tool_tag"]
                name = tool["function"]["name"]
                description = tool["function"]["description"]
                self.data["agent_template"]["messages"][0]["content"] += ("You have a function named {name} which is called whenever you say *{tag}*, you will only call it by {name}. This function will {description}.")

    #handler function when agent is invoked
    def handle(self, content):
         #print("handling")
        raise NotImplementedError("Subclasses should implement this method.")


    #function dedicated to prompting ollama
    # I want to make this async at some point to improve response time.    
    def generate(self):
    
        #print(self.data["agent_template"])
        response = {}

        response["message"] = ollama.chat(**self.data["agent_template"]) 
        response["origin"] = {}
        response["origin"] = self.data["metadata"]["agent_name"] 
    
        return response


    def add_message(self, msg):
        #OK so here is what we are going to do
        # to get these guys to talk to each other, we are going to add
        # prompts from other agents will be appended as a USER prompt
    
        if(msg[0] == self.data["metadata"]["tag"]):
            self.data["agent_template"]["messages"].append({"role" : "assistant", "content" : msg[1]})
        else:
            self.data["agent_template"]["messages"].append({"role" :"user", "content" : msg[1]})


    #calls object in the form of
    #   a tuple of the name of function, then an object, ie a variable/array/json file, that is passed to the function
    #   [[function_name, {args} ]  , ...  ] 
    #
    def process_tool_calls(self, calls):
        for call in calls:
            self.tool_calls[call[0]](call[1])

    def parse_caller(self, message):
        pass

    #NO >:(
    #def str_to_msg(self, str):
    #    msg = {}
    #    msg['message'] = {}
    #    msg['message']['message'] = {}
    #    msg['message']['message']['content'] = str
    #    return msg
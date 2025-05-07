from .agent import Agent
import re
import json


#tool calls for the game_state_parser agent

class gamestate_parser(Agent):

    def __init__(self, agent_info, game_state, agents):
        self.game_state = game_state
        self.agents = agents  
        self.data = agent_info
         #there is probably a better way to do this :P
        self.tool_calls = {
            "update_health": self.game_state.update_health,
            "set_max_health": self.game_state.set_max_health,
            "add_item": self.game_state.add_item,
            "remove_item": self.game_state.remove_item,
            "spend_coins": self.game_state.spend_coins,
            "gain_coins": self.game_state.gain_coins,
            "set_location": self.game_state.set_location,
            "add_flag": self.game_state.add_flag,
            "remove_flag": self.game_state.remove_flag,
            "add_party_member": self.game_state.add_party_member,
            "remove_party_member": self.game_state.remove_party_member,
            "add_quest": self.game_state.add_quest,
            "complete_quest": self.game_state.complete_quest,
            "add_log": self.game_state.add_log,
            "advance_turn": self.game_state.advance_turn,
            "set_fact": self.game_state.set_fact,
            "remove_fact": self.game_state.remove_fact,
        }   
        keys = agent_info["agent_template"].keys()
        if ("tools" in keys):
            self.load_tools(self.data["agent_template"]["tools"])


    
    def handle(self, message):
        print("->Parsing<-")
        self.add_message(message)
        self.parse_tool_calls(self.generate())
        self.clear_message_history()


    def parse_tool_calls(self, message):
        #parses tool calls of the form  tool(function_name, parameters)
        #and executes the corresponding function if it exists.   
        print(message)

        pattern = r'tool\((\w+),\s*(\{.*?\})\)'
        matches = re.findall(pattern, message["message"]["message"]["content"], re.DOTALL)

        for function_name, raw_params in matches:
            print(function_name)
            print(raw_params)
            params = json.loads(raw_params)
            if function_name in self.tool_calls.keys():
                try:
                    func = self.tool_calls[function_name]
                    func(**params)
                except:
                    print(function_name + "failed with values : " + raw_params)
            else:
                print(function_name + ": definition not found")

        self.clear_message_history() 
           

            
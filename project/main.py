import os
import json
from pathlib import Path
import sys
from os import listdir

from util.llm_Agent_utils import agent, simple_response_agent, rng_agent
import util.llm_Agent_utils as agent_tools


# a dict of template files {"dungeon-master": {template file}}
    # Need to maintain concurrency across all template files, keeping each one up to date with what it needs to
    # Know
# game state object


agent_class_mapping = {
    "scene" : simple_response_agent,
    "DM"    : simple_response_agent,
    "inventory" : simple_response_agent,
    "RNGCall" : rng_agent,
    "dialogue" : simple_response_agent,
    "battle" : simple_response_agent,
    "trader" : simple_response_agent,
    "player_input" : simple_response_agent,
    "item" : simple_response_agent 
}



def run_console_chat(seed, agents, **kwargs):
    #while True:
    # DM generates stuff & adds tags
    # parse tags and their procceses
   
    while(True):
        dm_response = agents["DM"].generate()      # dungeon master generates a thing
        print("===========dungeon master response============")
        print(dm_response['message']['message']['content'])

        # parsing tags
        parsed_tags = agent_tools.split_response(dm_response['message']['message']['content'], agents.keys()) 
        print("===========parsed tags============")
        print(parsed_tags)

        #parsing tags
        for tag, content in parsed_tags:
            # from out agent list, we parsed out an existing tag, now we are invoking the that tag's agent's handler function
            
            print("===========Tag============")
            print(tag)
            response = agents[tag].handle([tag,content])

            dm_response['message']['message']['content'] = agent_tools.replace_tags(tag, dm_response['message']['message']['content'], response['message']['message']['content'])
            
            
        print("=========== filled response============")
        print(dm_response['message']['message']['content'])
        
        agents["DM"].add_message(["Filled_Response", dm_response['message']['message']['content']])
        
        with open("output.txt", "a") as file:
            file.write("======================START===================")
            file.write(dm_response['message']['message']['content'])
            file.write("\n\n\n")
            file.write("======================END===================")
        
     

if __name__ == "__main__":
    seed = '441_AI_Project'
    agents = {}

    print(os.listdir("441_project/project/agents"))
    agent_list = os.listdir("441_project/project/agents")

    tags_from_json = []
    #populate agents list
    for agent_name in agent_list:
        with open("441_project/project/agents/" + agent_name, 'r') as file:     
            #print(agent_name)
            data = json.load(file)
            tag = data["metadata"]["tag"]
            agents[tag] = agent_class_mapping[tag](data)    
        

    run_console_chat(seed=seed, agents=agents)

    
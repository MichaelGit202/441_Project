import os
import json
from pathlib import Path
import sys
from os import listdir

from util.llm_Agent_utils import agent, simple_response_agent
import util.llm_Agent_utils as agent_tools


# a dict of template files {"dungeon-master": {template file}}
    # Need to maintain concurrency across all template files, keeping each one up to date with what it needs to
    # Know
# game state object


agent_class_mapping = {
    "scene" : simple_response_agent,
    "DM"    : simple_response_agent,
}



def run_console_chat(seed, agents, **kwargs):

   
    #while True:
    # DM generates stuff & adds tags
    # parse tags and their procceses
    response = agents["DM"].generate()
    print("===========dungeon master response============")
    print(response['message']['message']['content'])
    parsed_tags = agent_tools.split_response(response['message']['message']['content'], agents.keys())
    print("===========parsed tags============")
    print(parsed_tags)
    for tag, content in parsed_tags:
        # from out agent list, we parsed out an existing tag, now we are invoking the that tag's agent's handler function
        print("===========Tag============")
        print(tag)
        response = agents[tag].handle([tag,content])
        print("==========={tag} response============")
        print(response['message']['message']['content'])
        
    

if __name__ == "__main__":
    seed = '441_AI_Project'
    agents = {}

    print(os.listdir("441_project/project/agents"))
    agent_list = os.listdir("441_project/project/agents")

    tags_from_json = []
    #populate agents list
    for agent_name in agent_list:
        with open("441_project/project/agents/" + agent_name, 'r') as file:            
            data = json.load(file)
            tag = data["metadata"]["tag"]
            agents[tag] = agent_class_mapping[tag](data)    


    run_console_chat(seed=seed, agents=agents)
    
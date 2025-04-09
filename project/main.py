import os
import json
from pathlib import Path
import sys
from os import listdir

from util.llm_Agent_utils import agent, scene_agent
import util.llm_Agent_utils as agent_tools


# a dict of template files {"dungeon-master": {template file}}
    # Need to maintain concurrency across all template files, keeping each one up to date with what it needs to
    # Know
# game state object


agent_class_mapping = {
    "scene" : scene_agent,
    "DM"    : agent,
}



def run_console_chat(seed, agents, **kwargs):

   
    with open("sampleDmText.txt", 'r', encoding="utf-8") as file:
        bf = file.read()
    
   
   
    #build tag queue for generating tasks for agents
    parsed_tags = agent_tools.split_response(bf, agents.keys())
    
    
    for tag, content in parsed_tags:
        # from out agent list, we parsed out an existing tag, now we are invoking the that tag's agent's handler function
        print(tag)
        response = agents[tag].handle([tag,content])

    #print(response)
    print(response['message']['message']['content'])


    while True:
        break
        # DM generates stuff & adds tags
        # parse tags and their procceses
        #

        response = agents["dungeon_master"].generate()
        agents["dungeon_master"].add_message(response)

  

        
  

        #3 agents talkning to eachother
        #response = agents["assistant1"].generate()
        #agents["assistant1"].add_message(response)
        #agents["assistant2"].add_message(response)
        #agents["assistant3"].add_message(response)
        #print("assistant 1")
        #print(response["message"]["message"]["content"])
        #
#
        #
        #response = agents["assistant2"].generate()
        #print("assistant 2")
        #print(response["message"]["message"]["content"])
        #agents["assistant1"].add_message(response)
        #agents["assistant2"].add_message(response)
        #agents["assistant3"].add_message(response)
#
        #response = agents["assistant3"].generate()
        #print("assistant 3")
        #print(response["message"]["message"]["content"])
        #agents["assistant1"].add_message(response)
        #agents["assistant2"].add_message(response)
        #agents["assistant3"].add_message(response)

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
    
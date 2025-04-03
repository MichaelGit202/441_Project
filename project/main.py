import os
from pathlib import Path
import sys
from os import listdir
import json
from util.dict_tags import TAG_HANDLERS

sys.path.append(str(Path(__file__).parents[1]))


from util.llm_utils import TemplateChat
from util.llm_Agent_utils import agent 
import util.llm_Agent_utils as agTools

# a dict of template files {"dungeon-master": {template file}}
    # Need to maintain concurrency across all template files, keeping each one up to date with what it needs to
    # Know
# game state object




def run_console_chat(seed, agents, **kwargs):

   
    with open("sampleDmText.txt", 'r', encoding="utf-8") as file:
        bf = file.read()
    #
   
   
    #build tag queue for generating tasks for agents
    tags = agTools.split_response(bf)
    
    
    for tag, content in tags:
        handler = TAG_HANDLERS[tag]
        handler(content)
        

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

 
    #populate agents list
    for agent_name in agent_list:
        with open("441_project/project/agents/" + agent_name, 'r') as file:
            data = json.load(file)
            agents[data["metadata"]["agent_name"]] = agent(data)
                                                                                               #that there is a way to load in th
    run_console_chat(seed=seed, agents=agents)
    
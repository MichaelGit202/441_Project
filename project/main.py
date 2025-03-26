import os
from pathlib import Path
import sys
from os import listdir
import json

sys.path.append(str(Path(__file__).parents[1]))


from util.llm_utils import TemplateChat
from util.llm_Agent_utils import agent 

# a dict of template files {"dungeon-master": {template file}}
    # Need to maintain concurrency across all template files, keeping each one up to date with what it needs to
    # Know




# game state object




def run_console_chat(seed, agents, **kwargs):

    while True:
        
        response = agents["assistant1"].generate()
        agents["assistant1"].add_message(response, agents["assistant1"])
        agents["assistant1"].add_message(response, agents["assistant2"])
        print("assistant 1")
        print(response["message"]["message"]["content"])

        
        response = agents["assistant2"].generate()
        print("assistant 2")
        print(response["message"]["message"]["content"])
        agents["assistant2"].add_message(response, agents["assistant1"])
        agents["assistant2"].add_message(response, agents["assistant2"])



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
    
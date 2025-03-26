import os
from pathlib import Path
import sys
from os import listdir
import json

sys.path.append(str(Path(__file__).parents[1]))


from util.llm_utils import TemplateChat
import util.llm_Agent_utils as llm_Utils

# a dict of template files {"dungeon-master": {template file}}
    # Need to maintain concurrency across all template files, keeping each one up to date with what it needs to
    # Know




# game state object




def run_console_chat(seed, agents, **kwargs):

    while True:
        
        response = llm_Utils.generate(agents["assistant1"])
        llm_Utils.add_message(response, agents["assistant1"])
        llm_Utils.add_message(response, agents["assistant2"])
        print("assistant 1")
        print(response)

        
        response1 = llm_Utils.generate(agents["assistant2"])
        print("assistant 2")
        print(response1)
        llm_Utils.add_message(response1, agents["assistant1"])
        llm_Utils.add_message(response1, agents["assistant2"])
  

        #print("\n")
        #print(agents["Dungeon_Master"])
        #print("\n")
        #print(agents["assistant2"])
        #print("\n")


       
       
       
       # chat = TemplateChat.from_file(sign=seed, **kwargs)
        

        #chat_generator = chat.start_chat()
        #print(next(chat_generator))

        #while True: # you have to parameterize the exit condition for the agents here       
        #    try:
                # send user input
                #message = chat_generator.send(input(''))
         #       message -= chat_generator.send()
         #   except StopIteration as e:
          #      print(e)
        



if __name__ == "__main__":
    seed = '441_AI_Project'
    agents = {}
    agent_list = os.listdir("project/agents")

    #populate agents list
    for agent in agent_list:
        with open("project/agents/" + agent, 'r') as file:
            data = json.load(file)
            agents[data["metadata"]["agent_name"]] = data
            #agents[data["metadata"]["agent_name"]]["agent"] = data["metadata"]["agent_name"] #TODO this is scuffed
            #agents[data["metadata"]["agent_name"]]["agent_template"] = data["agent_template"] # im more than certain 
                                                                                                #that there is a way to load in th
    run_console_chat(seed=seed, agents=agents)
    
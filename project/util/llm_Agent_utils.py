#library for agent functions

import re
import json
import ollama
import hashlib
import logging

from pathlib import Path
from types import MethodType
from collections import defaultdict

ollama_seed = lambda x: int(str(int(hashlib.sha512(x.encode()).hexdigest(), 16))[:8])


#function dedicated to prompting ollama
def generate(agent):
   
    #ollama call with the template file
    response = {}
    #print(agent)
    #print("WHAT THE FUCK +++++++++++++")
    #print(agent["agent_template"])
    #print("WHAT THE FUCK 222222222222222222222222222")
    template = agent["agent_template"]
    
    response["message"] = ollama.chat(**template) 
    response["origin"] = {}
    response["origin"] = agent["metadata"]["agent_name"] 
    #print(response)
    return response


def add_message(msg, template):
    #OK so here is what we are going to do
    # to get these FUCKERS to talk to each other, we are going to add
    # prompts from other agents will be appended as a USER prompt

   
    #print(template)
    #print(msg)
     #TODO message manipulation is fucked right now ie msg["message"]["message"] <- what is causing this 
    if(msg["origin"] == template["metadata"]["agent_name"]):
        template["agent_template"]["messages"].append({"role" : msg["message"]["message"]["role"], "content" : msg["message"]["message"]["content"]})
    else:
        template["agent_template"]["messages"].append({"role" :"user", "content" : msg["message"]["message"]["content"]})

def parse_generator_calls():
    pass


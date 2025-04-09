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



#function used to parse tags into a list of tuples
# ie. <scene> prompt from model</scene>s

# returns a tag list in the term 

# if the model spits out a tag that does not exits in TagType
# that string will be completely ignored

def split_response(text, tags):
    pattern = r"<([^>]+)>(.*?)</\1>"
    matches = re.findall(pattern, text, re.DOTALL)

    parsed = []
    for tag, content in matches:
        # if tag exists
        if tag in tags:
            parsed.append((tag, content.strip()))
        else:
            pass  #things that are not in tags go here 
    return parsed   

class agent:
    data = {}

    def __init__(self, agent_info):  
        self.data = agent_info


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
        # to get these FUCKERS to talk to each other, we are going to add
        # prompts from other agents will be appended as a USER prompt
     
         #TODO, fix eye vomit
        if(msg[0] == self.data["metadata"]["tag"]):
            self.data["agent_template"]["messages"].append({"role" : "assistant", "content" : msg[1]})
        else:
            self.data["agent_template"]["messages"].append({"role" :"user", "content" : msg[1]})



    
#this is basically just a Question answer agent, one prompt one response
class simple_response_agent(agent):
    
    def handle(self, tag): 
        self.add_message(tag)
        return self.generate()


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


class agent:
    data = {}

    def __init__(self, agent_info):  
        self.data = agent_info
    #function dedicated to prompting ollama
    def generate(self):
    
        response = {}
        response["message"] = ollama.chat(**self.data["agent_template"]) 
        response["origin"] = {}
        response["origin"] = self.data["metadata"]["agent_name"] 
    
        return response


    def add_message(self, msg):
        #OK so here is what we are going to do
        # to get these FUCKERS to talk to each other, we are going to add
        # prompts from other agents will be appended as a USER prompt
        #print(template)
        #print(msg)

         #TODO message manipulation is fucked right now ie msg["message"]["message"] <- what is causing this
         # also this is eye vomit code 
        if(msg["origin"] == self.data["metadata"]["agent_name"]):
            self.data["agent_template"]["messages"].append({"role" : msg["message"]["message"]["role"], "content" : msg["message"]["message"]["content"]})
        else:
            self.data["agent_template"]["messages"].append({"role" :"user", "content" : msg["message"]["message"]["content"]})

    #def parse_generator_calls():
     #   pass


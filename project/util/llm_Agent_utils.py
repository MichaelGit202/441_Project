#library for agent functions

import re
import json
import ollama
import hashlib
import logging
from enum import Enum


from pathlib import Path
from types import MethodType
from collections import defaultdict

ollama_seed = lambda x: int(str(int(hashlib.sha512(x.encode()).hexdigest(), 16))[:8])



def parse_tags(text):

    return "name_of_model"


#function used to parse DM's tags
# returns a list of strings
#   ex [1] Random dm text ydayada
#      [2] <tag></tag>
#      [3]  the rest of the dm text
#      [4] <anotherTag><\anotherTag>



def handle_player_input(content):
        print("hello from player input")

def handle_scene (content):
        print("hello from scene")

def handle_think(content):
        print("hello from think")

#proomted these up
class TagType(Enum):
    THINK = "think"
    SCENE = "scene"
    PLAYER_INPUT = "player-input"


def split_response(text):
    pattern = r"<([^>]+)>(.*?)</\1>"
    matches = re.findall(pattern, text, re.DOTALL)

    parsed = []
    for tag, content in matches:
        # Map tag to Enum if it exists, otherwise keep it as a string
        tag_enum = TagType[tag.upper().replace("-", "_")] if tag in TagType._value2member_map_ else tag
        parsed.append((tag_enum, content.strip()))

    return parsed   

class agent:
    data = {}

    def __init__(self, agent_info):  
        self.data = agent_info
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
        # to get these agents to talk to each other, we are going to add
        # prompts from other agents will be appended as a USER prompt
     
         #TODO, fix eye vomit
        if(msg["origin"] == self.data["metadata"]["agent_name"]):
            self.data["agent_template"]["messages"].append({"role" : msg["message"]["message"]["role"], "content" : msg["message"]["message"]["content"]})
        else:
            self.data["agent_template"]["messages"].append({"role" :"user", "content" : msg["message"]["message"]["content"]})

    #def parse_generator_calls():
     #   pass


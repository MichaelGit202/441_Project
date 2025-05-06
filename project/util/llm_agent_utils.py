#library for agent functions
import re
import json
import ollama
import hashlib
import logging
import random

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
    print("spliting")
    print(tags)
    print(text)
    parsed = []
    for tag, content in matches:
        # if tag exists
        if tag in tags:
            parsed.append((tag, content.strip()))
        else:
            pass  #things that are not in tags go here 
    return parsed   



def replace_tags(tag, dm_response, response):
    pattern = rf"<{tag}>(.*?)</{tag}>"
    replacement = f"<{tag}>{response}</{tag}>"
    return re.sub(pattern, replacement, dm_response, flags=re.DOTALL)


def process_tags( dm_response, agents):
    tags = split_response(dm_response['message']['message']['content'], agents.keys()) 
    print("=============Parsed Tags============")
    print(tags)
    for tag, content in tags:
        # from out agent list, we parsed out an existing tag, now we are invoking the that tag's agent's handler function
        print("===========Tag============")
        print(tag)
        agents[tag].handle(["DM",content])

        #print(response)
        #dm_response['message']['message']['content'] = replace_tags(tag, dm_response['message']['message']['content'], response['message']['message']['content'])
    
                
    #print("=========== filled response============")
    #print(dm_response['message']['message']['content'])
    #return dm_response


#function designed to parse and add messages when they are generated
#agentTags is which agents you want to add the message to
#IO is for like UI, like you create some sort of stream and output it through the IO specification inside of IO.py
# IO is a list

#note message is that tuple message thing where its [source agents tag, the message object it returned]
#I dont like it either but we already this far
def output_message(agents, agentsTags, message, IO):
    for tag in agentsTags:
        agents[tag].add_message(message)
    
    for output in IO:
        output(message)

def input_message(IO):
    return IO()
    











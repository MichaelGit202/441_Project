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
    for tag, content in tags:
        # from out agent list, we parsed out an existing tag, now we are invoking the that tag's agent's handler function
        print("===========Tag============")
        print(tag)
        response = agents[tag].handle([tag,content])
        #print(response)
        dm_response['message']['message']['content'] = replace_tags(tag, dm_response['message']['message']['content'], response['message']['message']['content'])
    
                
    print("=========== filled response============")
    print(dm_response['message']['message']['content'])
    return dm_response



class agent:
    data = {
        #everything from the json file
    }
    # I added this tool call thing for tool definitions in the json
    tool_calls = {  
        #example rng_tag : rng_function
    }

    def __init__(self, agent_info):  
        self.data = agent_info
        keys = agent_info.keys()
        if ("tools" in keys):
            self.load_tools(agent_info["tools"])


    def load_tools(self,tools): 
        for tool in tools:
            if(tool["type"] == "function"):
                tag = tool["function"]["tool_tag"]
                name = tool["function"]["name"]
                description = tool["function"]["description"]
                self.data["agent_template"]["messages"][0]["content"] += ("You have a function named {name} which is called whenever you say *{tag}*, you will only call it by {name}. This function will {description}.")

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
        # to get these guys to talk to each other, we are going to add
        # prompts from other agents will be appended as a USER prompt
     
         #TODO, fix eye vomit
        if(msg[0] == self.data["metadata"]["tag"]):
            self.data["agent_template"]["messages"].append({"role" : "assistant", "content" : msg[1]})
        else:
            self.data["agent_template"]["messages"].append({"role" :"user", "content" : msg[1]})


    #calls object in the form of
    #   a tuple of the name of function, then an object, ie a variable/array/json file, that is passed to the function
    #   [[function_name, {args} ]  , ...  ] 
    #
    def process_tool_calls(self, calls):
        for call in calls:
            self.tool_calls[call[0]](call[1])



    
#this is basically just a Question answer agent, one prompt one response
class simple_response_agent(agent):
    
    def handle(self, tag): 
        self.add_message(tag)
        return self.generate()



class rng_agent(agent):

    def __init__(self, agent_info):  
        self.data = agent_info
        keys = agent_info.keys()
        if ("tools" in keys):
            self.load_tools(agent_info["tools"])
        
        self.tool_calls = {  
            "RNGCALL" : self.rng,
        }

        print(self.tool_calls["RNGCALL"](10))

    def handle(self, tag):
        self.add_message(tag)
        return self.generate()
    
    def rng(self, upper_bound):
        return random.randint(0, upper_bound)



class trader_agent(agent):
    
    def __init__(self, agent_info):
        self.data = agent_info


    def handle(self, tag):
        # Add the initial message to the conversation
        print("TRADER SEQUENCE")
        self.add_message(tag)

        while True:
            # Generate a response from the agent
            response = self.generate()
            #process_tags(response, agents)
            # Extract the message text
            message_text = response["message"]["message"]["content"]

            # Print or log the message (optional)
            print(f"TRADER: {message_text}")

            # Check if it signals the end of the trade
            if re.search(r"TRADE(.*)DONE", message_text, re.DOTALL):
                print("Trade sequence complete.")
                return response  # Or return the full conversation if you store history
            
            # Otherwise, continue conversation by appending as assistant's message
            self.data["agent_template"]["messages"].append({
                "role": "assistant",
                "content": message_text
            })
            print("Your input: ")
            user_msg = input()
            
            self.data["agent_template"]["messages"].append({
                "role": "user",
                "content": user_msg,
            })
    

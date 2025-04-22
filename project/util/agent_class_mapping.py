from .agents.simple_agent import simple_response_agent
from .agents.rng_agent import rng_agent
from .agents.trader_agent import trader_agent

#these are the things that go in <here><\here>
agent_class_mapping = {
    "scene" : simple_response_agent,
    "DM"    : simple_response_agent,
    "inventory" : simple_response_agent,
    "RNGCall" : rng_agent,
    "dialogue" : simple_response_agent,
    "battle" : simple_response_agent,
    "trader" : trader_agent,
    "player_input" : simple_response_agent,
    "item" : simple_response_agent 
}
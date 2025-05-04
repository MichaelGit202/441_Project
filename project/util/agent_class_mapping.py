from .agents.simple_agent import simple_response_agent
from .agents.rng_agent import rng_agent
from .agents.trader_agent import trader_agent
from .agents.battle import battle_agent
from .agents.player_input import player_input
from .agents.dialouge import dialogue_agent


#these are the things that go in <here><\here>
agent_class_mapping = {
    "scene" : simple_response_agent,
    "DM"    : simple_response_agent,
    "inventory" : simple_response_agent,
    "RNGCall" : rng_agent,
    "dialogue" : dialogue_agent,
    "battle" : battle_agent,
    "trader" : trader_agent,
    "player_input" : player_input,
    "item" : simple_response_agent 
}
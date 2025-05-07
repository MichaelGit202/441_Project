from .agents.simple_agent import simple_response_agent
from .agents.rng_agent import rng_agent
from .agents.trader_agent import trader_agent
from .agents.battle import battle_agent
from .agents.player_input import player_input
from .agents.dialouge import dialogue_agent
from .agents.game_state_parser import gamestate_parser
from .agents.dungeon_master import dungeon_master
from .agents.dungeon_master_speak import dungeon_master_speak

#this is how we map tool calls to the correct agent
agent_class_mapping = {
    "scene" : simple_response_agent,
    "DM"    : dungeon_master,
    "inventory" : simple_response_agent,
    "RNGCall" : rng_agent,
    "dialogue" : dialogue_agent,
    "battle" : battle_agent,
    "trader" : trader_agent,
    "player_input" : player_input,
    "item" : simple_response_agent ,
    "GS" : gamestate_parser,
    "DM_Speak"  : dungeon_master_speak
}
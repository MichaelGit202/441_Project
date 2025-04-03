#this is a dictionary that is dedicated to mapping the agent tags to the 
#agent handler functionsS

from util.llm_Agent_utils import handle_player_input, handle_scene, handle_think,TagType


TAG_HANDLERS = {
    TagType.THINK: handle_think,
    TagType.SCENE: handle_scene,
    TagType.PLAYER_INPUT: handle_player_input
}

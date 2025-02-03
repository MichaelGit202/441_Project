from pathlib import Path
import sys
import re
sys.path.append(str(Path(__file__).parents[1]))

from ollama import chat
from util.llm_utils import pretty_stringify_chat, ollama_seed as seed

# Add you code below
sign_your_name = 'Michael Penfield'
model = 'deepseek-r1:1.5b'
messages = [
  {'role': 'system', 
   'content': 'You are a Dungeons and Dragons style bot that will generate an interesting story and plot \
   for the player. You will do the following: \
   1. Only once, describe the the world the players inhabit\
   2. You will begine the story in the players home and generate a story from there.\
   3. You will organize your responses \
   4. lastly you will caryr out the campaign: \
   start story segments with **STORY**,   \
   dialouge segments with **DIALOUGE**\
   when the player is thinking start with **THINKING** , \
   the player picks up an item you will start with **ITEM** , *Items will be described in 2 sentances, a qualitative segment and a quantitative segment.*\
   when you are describing the scence **SCENE** . *scene segments will be described in passive voice.*\
   You will not number the headers, you will only use the headers\
   You will not use any other headers other than the ones listed\
   make sure you add enough space betwene these so that they can be easily read. \
   Remember your job is to tell an interesting story and keep the player engaged. \
   Prompt the player with choices, ragning from 1-4, which affect the story based on the players response \
   '
   },

]
options = {'temperature': .5, 'max_tokens': 50}

setting = "" #setting
dialouge = "" #dialouge
Item = "" #Item
scene = "" #Scene

pattern = r"\*\*(.*?)\*\*\s*(.*?)(?=\n\*\*|\Z)"

options |= {'seed': seed(sign_your_name)}
# Chat loop
while True:
  # Add your code below
  message = {'role': 'user', 'content': input('You: ')}
  messages.append(message)
  if messages[-1]['content'] == '/exit':
    break
  
  response = chat(model=model, messages=messages, stream=False, options=options)
  print(f'Agent: {response.message.content}')

  #settingIndex = response.find("**")
  

  matches = re.findall(pattern, response.message.content, re.DOTALL)

  parsed_data = {}

  #parsing each action and its coresponding text
  for action, text in matches:
      action = action.strip().upper() #everthing to upper because AI is dumb
      text = text.strip()
      #if the action hasnt been defined yet
      if action not in parsed_data:
          parsed_data[action] = []
      #list of responses for action
      parsed_data[action].append(text)

 
  #parsed_data{"DIALOUGE"}[0]




  messages.append({'role': 'assistant', 'content': response.message.content})



# Save chat
with open(Path('lab03/attempts.txt'), 'a') as f:
  file_string  = ''
  file_string +=       '-------------------------NEW ATTEMPT-------------------------\n\n\n'
  file_string += f'Model: {model}\n'
  file_string += f'Options: {options}\n'
  file_string += pretty_stringify_chat(messages)
  file_string += '\n\n\n------------------------END OF ATTEMPT------------------------\n\n\n'
  f.write(file_string)


from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parents[1]))

from util.llm_utils import TemplateChat

agents = [{}]


def run_console_chat(sign, **kwargs):
    chat = TemplateChat.from_file(sign=sign, **kwargs)
    chat_generator = chat.start_chat()
    print(next(chat_generator))
    while True:
        try:
            message = chat_generator.send(input('You: '))
            print('Agent:', message)
        except StopIteration as e:
            if isinstance(e.value, tuple):
                print('Agent:', e.value[0])
                ending_match = e.value[1]
                print('Ending match:', ending_match)
            break

recruit_template_file = 'lab04/chat.json'

lab04_params = {
   'template_file': recruit_template_file , 
   'sign' : "Michael Penfield",
   'end_regex': r'TRADE(.*)DONE',
}

if __name__ ==  '__main__':
    # run lab04.py to test your template interactively
    run_console_chat(template_file=recruit_template_file,
                     recruit_difficulty='not easy',
                     reward='a sword',
                     sign='Michael penfield',
                     end_regex=r'TRADE(.*)DONE')
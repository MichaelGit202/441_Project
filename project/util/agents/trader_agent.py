from .agent import Agent


class trader_agent(Agent):
    
    def __init__(self, agent_info, game_state, agents):
        self.data = agent_info
        self.game_state = game_state
        self.agents = agents  


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
    

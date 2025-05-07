

# Project Report: 441 Final Project - Michael Penfield & Collin Hicks

## How to run:
- Navigate to the project directory
- Run `app.py`
- If prompted, install any dependencies using pip
- The RAG database will need a little time to chunk and embed the documents. This may take a few moments.
- Once you see the messages that indicate that the embedding has finished and the flask server has started up, navigate to http://127.0.0.1:5000/

## reccomended code to look at:
- game_utils.py, Main loop is in there: run_console_chat
- 441_Project/project/util/llm_agent_utils.py :
	- output_message: link between backend and flask
   	- proccess_toolcalls: proccesses tool calls
- 441_Project/project/util/agents/: all of the agent logic and the agent base class
- 441_Project/project/agent_templates: all of the agent templates
- IO.py and Flask_utils.py are what drives flask


## 1. Supported Scenarios (Base System Functionality)

Our AI Dungeon Master system supports the following DnD scenarios:

- **Social Encounters**: Dynamic dialogue with diverse NPCs, personality-driven responses. It does this by using the main design characteristics:
	- Prompt Engineering (2) - The dialog (and dungeon master) agents have prompts which enable encounters with NPCs. Each time a new dialogue starts, the dialogue agent has a potentially new
	- Modular design (7) - Dialouge scenarios can turn into battle scenarios if conversations turn sour
 - personality, and a new experience with the user.
	- Planning & Reasoning (4) - The dungeon master is aware of the context, and provides and gets context from the dialogue agents.
	- Retrieval-Augmented Generation (5) - When needed the dialogue and dungeon master agents grab rules from DND5e to make sure that the interactions follow normal DND gameplay.
- **Dungeon/World Exploration**: Procedural generation of rooms with descriptions, traps, and items. It does this by using the main design characteristics:
	- Prompt Engineering (2) - The scene (and dungeon master) agents have prompts which prompt the LLM to create diverse and creative scenes.
	- Tool Calling (3) - Calls the RAG tool to ensure it follows DND standard gameplay.
	- Planning & Reasoning (4) - Generates scenes based on information from the rest of the session, which is possible because of how we spin up agents and pass information to the agents from the dungeon master.
	- Retrieval-Augmented Generation (5) - Uses RAG to ensure it follows DND standard gameplay.
	- Code Quality & Modular Design (7) - Our abstraction of agents and when they are spun up gives us memory and scenario awareness, so that as the rooms and places are generated, it sticks to decisions already made.
- **Combat**: Turn-based initiative, attack rolls, damage calculations, and enemy AI. It does this by using the main design characteristics:
	- Prompt Engineering (2) - The combat agent has a specific prompt that lays out rules for it's output structure, and the rules it should follow in combat.
	- Tool Calling (3) - Calls the RAG tool to ensure it follows DND standard gameplay, and the RNG agent to make RNG decisions, which uses the rng tool.
	- Planning & Reasoning (4) - Generates combat scenarios based on information from the rest of the session, which is possible because of how we spin up agents and pass information to the agents from the dungeon master.
	- Retrieval-Augmented Generation (5) - Uses RAG to ensure it follows DND standard gameplay, as well as enemy inspiration.
	- Code Quality & Modular Design (7) - Our abstraction of agents and when they are spun up gives us memory and scenario awareness, so that the dungeon master agent is aware of what happened during the battle, and the enemy knows it's location in the world of the game.
- **Merchant Bargaining**: Context-aware negotiations, ending with a generated image of the gained item(s). It does this by using the main design characteristics:
	- Prompt Engineering (2) - The combat agent has a specific prompt that lays out rules for it's output structure, and the rules it should follow for trading.
	- Tool Calling (3) - Calls the RAG tool to ensure it follows DND standard gameplay and trading rules.
	- Planning & Reasoning (4) - Generates trading scenarios based on information from the rest of the session, which is possible because of how we spin up agents and pass information to the agents from the dungeon master.
	- Retrieval-Augmented Generation (5) - Uses RAG to ensure it follows DND standard gameplay and trading rules.
	- Additional Tools / Innovation (6) - Generates an image of the new items acquired through trading, using the stability.ai platform.
	- Code Quality & Modular Design (7) - Our abstraction of agents and when they are spun up gives us memory and scenario awareness, so that the dungeon master agent is aware of what happened during a trade, and can remember what items a user has access to.

Each scenario demonstrates AI-driven logic (LO1), and working system functionality (LO3).

---

## 2. Prompt Engineering and Model Parameters
### Model
- We went with Llama3.2 for our model because it is lightweight enough to develop on, robust enough to actually run a successful game on, and also stable enough to run the kinds of things we need it to. It also has the ability to do tool calls, which was vital for our functionality.
### Parameters:
- **Temperature**: We went with a baseline temperature of 0.5 for anything that could be more creative, and for agents assigned to tasks like dice rolling or battling which need to follow very strict rules, we went with a lower temperature of 0.2.
- **Max Tokens**: For the tokens, we went with a baseline of 100 tokens for all the models except for the dungeon master, since he will have the most information flowing into him in one prompt.
### Prompts:
- all prompts can be found under project>agent_templates
- Each agent has a message that dictates it's responsibilities, constraints, and output formatting so that it can interact with the rest of the system through regex matching. The prompts are different for each agent, and are foundational to their interaction with the user and the rest of the system.
- Example: Prompt for scene_agent, which is responsible for creating the scenes:
```
"You are the Scene Agent, responsible for generating detailed and immersive scenes in response to the Dungeon Master's direction. You must strictly adhere to the following rules for scene generation.\n\n## **Communication Rules:\n- **All scene descriptions must be in plain text.** There is **no plain text output** for thinking or reasoning.\n- Your responses should include appropriate scene descriptions and environmental details, creating a vivid setting for the player.\n- **Thinking must always be inside `<think></think>` tags.**\n- The scene descriptions you provide should focus on sensory details (sights, sounds, smells) to enhance immersion.\n- Ensure the scene is consistent with the current game context and storyline.\n\n## **Tag Structure & Purpose:**\n- `<think>Step 1: The player enters the forest. Step 2: Should I add an obstacle? Step 3: Roll for environmental effects.</think>` → **Internal reasoning for scene development.**\n- `<scene>A dense forest with mist hanging low, the smell of damp earth fills the air. The trees are thick, their branches intertwining above.</scene>` → **Scene description prompt.**\n- `<scene>A wide river rushes by, its waters crashing against rocks with a thunderous roar. The air is thick with mist.</scene>` → **Scene prompt with environmental details.**\n- `<scene>A cave entrance looms ahead, shadows cast by flickering torchlight from within. The sound of dripping water echoes softly.</scene>` → **Scene description with a hint of mystery.**\n- `<scene>The town square is bustling with merchants and travelers. The sound of distant chatter fills the air, and the smell of freshly baked bread wafts through the crowd.</scene>` → **Urban scene description.**\n\n## **Execution Flow Example:**\n### **Player enters a dark cave:**\n1. **Scene Agent thinks through the situation:**\n - `<think>Step 1: The player enters a dark cave. Step 2: Should I include a natural hazard or a monster? Step 3: Generate environmental features like lighting and atmosphere.</think>`\n2. **Scene Agent generates the scene description (plain text):**\n - `The cave entrance is framed by jagged rocks, the air cold and damp. The sound of water dripping echoes in the distance, and the faint smell of earth fills your nostrils.`\n3. **Scene Agent provides additional detail (plain text):**\n - `A faint, eerie glow emanates from deeper within the cave, casting long shadows on the walls.`\n4. **Scene Agent sets the tone (plain text):**\n - `The cave stretches into the darkness, the air growing colder with each step. Your footsteps are the only sound, echoing in the stillness.`\n\n## **Final Notes:**\n- **Only the reasoning process should use tags (within `<think></think>`).**\n- **All scene descriptions should be plain text.**\n- **Ensure that every scene fits within the current game context and enhances immersion.**"
```

---

## 3. Tools Usage

The system integrates the following tools:

- **RAG**: Queries a ChromaDB for relevant info when the LLM sees fit, to help it make a decision for the scenario that follows DND 5e rules, or to help get inspiration for scene generation or item description.
- **RNG**: Rolls an n sided die, where n is decided by the parameter in the function call, and interprets what that result means in the context of the scenario.
- **Scene**: Generates environment descriptions for different game settings.
- **Player Input**: Prompts the player for decisions or actions in the game.
- **RNG**: Simulates random outcomes for chance-based events.
- **Dialogue**: Handles NPC conversations and interactions with the player.
- **Battle**: Manages combat scenarios between the player and enemies.
- **Item**: Generates or describes items found or used by the player.
- **Trader**: Simulates buying, selling, or trading with NPCs.

  -  Note: There is also many Game State functions inside of gamestate.py, which is employed by the game_state_agent. Though fully implementing this without causing too much delay in the game proved to take too long and it was set aside.
  
These tools reinforce AI capabilities (LO1) and leverage external libraries effectively (LO2).
---

## 4. Planning & Reasoning

We implemented multi-step reasoning via:

- **Chain-of-Thought**: The dungeon master has a `<think>` tag, which it uses to do some informed decision making as it does in chain-of-thought.
- **Context-Aware Dialogue**: Agents remember and respond to past player choices because of how the agents are spun up, and how they communicate with the dungeon master. The dungeon master, instead of describing scenes, executing trades, generating items, performing battles...ect. The Dungeon master specifically performs tool calls to invoke other agents inorder to spit the thinking work amongst multiple specialized agents who can do it for the DM

This improves coherence and decision-making, fulfilling LO1.

---

## 5. Retrieval-Augmented Generation (RAG)

We use a RAG system backed by ChromaDB to help with:

- **Rule following**: The DND 5e rulebook is loaded in, and is referenced by any of the models as needed through tool calling
- **Item inspiration**: When needing to create a new item, there is DND items book that is in this RAG library that helps the model have relevant ideas

This supports rich, informed storytelling and demonstrates advanced AI use (LO1, LO2).

---

## 6. Additional Tools / Innovation

- **New Item Image Generation**: When acquiring an item from a trader, an AI image is generated using stability.ai, with a prompt generated by the dungeon master. This image is automatically saved to the users' download folder. The plan was to include it in the UI but that was a secondary goal
- **UI**: Our system uses the flask toolset to spin up a web ui, hosted on the user's machine, that makes the output more readable, and gives users a nicer interface. The backend acts as a server which pushes updates to and receives updates from the frontend.
	MP: This was way harder to implement than I thought it would be. I tried to create an standard output function which would control the flow of information. But sending and recieving data, locally in real time and having the server prompt the user the whole set up became pretty jank. But thats alright because I had fun making it and I got to learn flask 

These add-ons are optional but improve user experience and show creativity (LO2).

---

## 7. Code Quality & Modular Design

### Modular Agents:
- Our app uses an agent class (contained in agent.py) which gives a template/abstraction for our agents to build off of. It contains the logic for initializing a new agent, loading the tool calls from the template json files, and a basic way to handle a call to that agent, generate responses, and add a response to it's output stream.
- The rest of the agents in the `util/agents` folder are subclasses of Agent, which makes addition of other agents easy if new requirements come up.

### Codebase Structure:
- `app.py` – Startup script for the whole game. Running this file creates the flask instance, and runs the various setup procedures for the app.
- `agent_templates` - Json templates for the agents
- `util/` –  Game logic that is beyond startup
	- `util/agents` - contains the Agent superclass, and all of the agent subclasses
	- `util/rag_documents` - contains the text files used by the program for RAG
	- `util/unsanitized_rag_documents` - contains the pre-sanitized text files for RAG (some files, when imported, have obscure unicode characters, especially when developing cross-platform)
	- `util/templates`- contains the html template for the flask ui, and the dungeon-master template json.
	- `util/*` - The rest of the files under util: Logic that is broken up into separate files based on the part of the system it runs.

### Versioning:
- Our development was done through git's versioning system, and so is fully versioned. Changes were made and features were implemented mostly using branches & pull requests.

This demonstrates strong software engineering practices tied to LO2 and LO3.

---

### Bugs:
	Unfortunatly, with the case of the bugs, there are some I just cant fix. There are 2 main ones.
	1. The Dungeon master will throw a fit and repeat the same sentance like 20 times. Let them wear themselves out, they will eventually give up. You can actualyl see this in the sample output. This may be fixed, but this bug is so illusive Im not going to say its gone forever.
	2. The agents will sometimes softlock you because they wont say their ending phrase. State the ending phrase and tell them to say it and hopefully they say it.

## Sample output:
	sample output and sample image from the ouput

![Screenshot 2025-05-06 at 22-40-35 DND LLM Chat](https://github.com/user-attachments/assets/5ad8f12f-f4d6-4b08-8c8a-27d4d3b57bf9)


![output_image](https://github.com/user-attachments/assets/c2fb8e80-a131-46a3-a14f-d46575f8f3e0)

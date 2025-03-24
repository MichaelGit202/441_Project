##Goals

1. multiple Agents working together
2. pre-story generation
3. save game
4. working inventory




pattern for generation:
    - game state: battle, exploring, town
    - Agents: Dungeon master, narration generator, character generator, NPC dialogue generator, Scene generator, item generator, Battle generator, Trader Generator
    - Dungeon master
        - keeps track of the game state and invokes generators based on context and rng
            - if nothing is happening, have  1/10 chance to generate a random encounter, NCP or Battle
            - if something is happening, in a town, in a battle, DM invokes relevant generator agents
            - does not display thinking text
            - NPC generator has its own loop so that the user can respond back and forth with the llm
                - each npc has their own agent
        - The dungeon master will communicate with itself with <thinking> tags
        - tags:
            <scene>, it invokes a function in game state that returns the current setting
            <inventory> invokes a function in game state that returns the party's current inventory
            <storyContext> invokes a function to get the current story context from the overall pre-generated story, this will be stored in the game-state
            <turns> gets the number of turns that have progressed
            <RNGCall> invoke a rng function
            <thinking> thinking output from the dungeon master, not displayed
            <dialouge></dialouge> section that contains a dialouge segment
            <battle></battle> section that contains a battle segment
            <trader></trader> section that contains trader segment
            <player-input> section for when the user is where the user is prompted and they need to say stuff

        ex: <scene> a fluffy overgrown meadow with a bright sun and a cool breeze
            <storyContext> the player is traveling to the town of riften with their party to warn the residents about a possible dragon attack. The player is with Andrew and Cameron
            <RNGCall> Random event 1/10 : result: NO
            <thinking> So I am thinking about the player walking through this meadow, we should probably describe the scenery and mabey create some dialouge from some of the other party members
            <Scene-Generator> (fills in generation about the current scene)
            <NPC-dialouge-Gen> Andrew, Player, Cameron (fills in a dialouge segment) 


    -Start of game 
        - user is prompted for some parameters for the game:
            - length of game (100 turns) (500 turns) (1000 turns) (inf)
            - character creator
        - Narrative-generator agent pre-generates the game plot and this is stored in steps
            - output is stored in game state
        - narrator agent starts out the story
            - this guy is invoked every time we move forward a step in the story
        - dungeon master starts invoking generators
            - game is played

     Generation pattern:
       - dungeon master is given the functions to invoke the generators
            - dungeon master will think of what to do next, thinking is never read other than when debugging
            - dungeon master invokes functions by providing empty tag blocks ex: <scene></scene>
       - User input states
         
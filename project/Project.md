

# Project Report (THIS IS A TEMPLATE)

## 1. Supported Scenarios (Base System Functionality)

Our AI Dungeon Master system supports the following DnD scenarios:

- **Tavern Social Encounters**: Dynamic dialogue with diverse NPCs, personality-driven responses.
- **Dungeon Exploration**: Procedural generation of rooms with descriptions, traps, and items.
- **Combat Resolution**: Turn-based initiative, attack rolls, damage calculations, and enemy AI.
- **Merchant Bargaining**: Context-aware negotiations with NPCs using past interaction memory.
- **Lore Recall and Continuity**: System remembers player history and updates NPC behavior.
- **Multi-stage Puzzles**: Interactive puzzles requiring multi-step reasoning to solve.
- **Voiced Narration**: Optional text-to-speech for immersive storytelling.

Each scenario demonstrates AI-driven logic (LO1), working system functionality (LO3), and a modular, testable implementation.

---

## 2. Prompt Engineering and Model Parameters

We used structured prompting to ensure scenario-specific responses:

- **System Prompts**: Set tone, role, and rules for the AI as a Dungeon Master.
- **User Prompts**: Player actions (e.g., "I pick the lock" or "I interrogate the goblin").
- **Contextual Prompts**: Inject quest history, NPC memory, or dungeon state.

### Parameters:
- **Temperature**: 0.7 for creative storytelling, 0.2 for factual tasks (e.g., rules recall).
- **Max Tokens**: Default 512, extended to 1024 for long-form narration.
- **Top_p**: Set at 0.9 to balance diversity and relevance.

### Example Prompt:
```
You are a Dungeon Master. The party enters a smoky tavern filled with shady figures. Describe the setting and present them with interaction options.
```

---

## 3. Tools Usage

The system integrates the following tools:

- **Dice Roller**: Resolves 1d20 and other common DnD rolls programmatically.
- **ChromaDB (RAG)**: Maintains lore, past actions, and context memory.
- **SQLite Quest Tracker**: Logs active quests and NPC flags.
- **Monster Stat Lookup**: Queries local monster stat blocks.
- **Web Search Tool (optional)**: For rule clarifications if needed.

These tools reinforce AI capabilities (LO1) and leverage external libraries effectively (LO2).

---

## 4. Planning & Reasoning

We implemented multi-step reasoning via:

- **Chain-of-Thought**: Used in puzzles, traps, and tactical enemy decisions.
- **NPC Strategy**: Enemies decide whether to flee, negotiate, or flank.
- **Context-Aware Dialogue**: NPCs remember and respond to past player choices.

### Example:
```
The rogue examines the pressure plate trap. First, check for wires. If found, decide whether to cut red or blue. Let's proceed step-by-step.
```

This improves coherence and decision-making, fulfilling LO1.

---

## 5. Retrieval-Augmented Generation (RAG)

We use a RAG system backed by ChromaDB to maintain and recall:

- **NPC Memory**: Past conversations influence current behavior.
- **Lore Recall**: Integrates world history, character backstories, and locations.
- **Item/Spell Info**: Quick retrieval of descriptions for in-game use.

### Data Sources:
- Custom JSON files for items and monsters.
- Embedded lore docs and previous game sessions.
- Player facts dynamically added during play.

This supports rich, informed storytelling and demonstrates advanced AI use (LO1, LO2).

---

## 6. Additional Tools / Innovation

- **NPC Portrait Generation**: Uses a local Stable Diffusion model to create unique character images.
- **Text-to-Speech (TTS)**: Narrates descriptions and dialogues using ElevenLabs or local TTS.
- **Dynamic Map Generator**: Builds new dungeons with seeded randomness and room grammars.

These add-ons are optional but improve user experience and show creativity (LO2).

---

## 7. Code Quality & Modular Design

### Codebase Structure:
- `core/` – Prompt handling, model wrappers.
- `tools/` – Dice, RAG, image generation, TTS.
- `data/` – Lore documents, monster stats, NPCs.
- `main.py` – Entry point and scenario loop.
- `utils/` – Common helper functions.

### Practices:
- Follows PEP8 and includes docstrings throughout.
- Git used for version control with clear commit history.
- Managed with `poetry` and `.env` files for environment control.
- Components are modular and independently testable.

This demonstrates strong software engineering practices tied to LO2 and LO3.

---

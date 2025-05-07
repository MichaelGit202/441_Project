# This class keep track of all the stats about the game
class GameState:
    def __init__(self):
        self.inventory = []
        self.health = 100
        self.max_health = 100
        self.coins = 0
        self.location = "Starting Village"
        self.flags = []  # For plot flags, booleans like "met_wizard": True
        self.party = []  # List of companions
        self.quests = []  # Active quests, like a sting list
        self.log = []  # Record of past events, idk
        self.turns = 0
        self.extra_facts = {}

        self.existing_states = [
            ["inventory", "list"],
            ["health", "int"],
            ["max_health", "int"],
            ["coins", "int"],
            ["location", "str"],
            ["flags", "list"],
            ["party", "list"],
            ["quests", "list"],
            ["log", "list"],
            ["turns", "int"],
            ["extra_facts", "dict"]
        ]   

    def update_health(self, amount):
        self.health += amount

    def set_max_health(self, amount):
        self.max_health = max(1, amount)
        self.health = min(self.health, self.max_health)

    def add_item(self, item):
        self.inventory.append(item)

    def remove_item(self, item):
        if item in self.inventory:
            self.inventory.remove(item)

    def spend_coins(self, amount):
        if self.coins >= amount:
            self.coins -= amount
            return True
        return False

    def gain_coins(self, amount):
        self.coins += amount

    def set_location(self, location):
        self.location = location

    def add_flag(self, flag):
        if flag not in self.flags:
            self.flags.append(flag)

    def remove_flag(self, flag):
        if flag in self.flags:
            self.flags.remove(flag)

    def add_party_member(self, member):
        if member not in self.party:
            self.party.append(member)

    def remove_party_member(self, member):
        if member in self.party:
            self.party.remove(member)

    def add_quest(self, quest):
        if quest not in self.quests:
            self.quests.append(quest)

    def complete_quest(self, quest):
        if quest in self.quests:
            self.quests.remove(quest)

    def add_log(self, event):
        self.log.append(event)

    def advance_turn(self):
        self.turns += 1

    def set_fact(self, key, value):
        self.extra_facts[key] = value

    def remove_fact(self, key):
        if key in self.extra_facts:
            del self.extra_facts[key]

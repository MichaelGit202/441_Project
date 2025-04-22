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

    def update_health(self, amount):
        self.health = max(0, min(self.max_health, self.health + amount))

    def add_item(self, item):
        self.inventory.append(item)

    def spend_coins(self, amount):
        if self.coins >= amount:
            self.coins -= amount
            return True
        return False

    def add_log(self, event):
        self.log.append(event)

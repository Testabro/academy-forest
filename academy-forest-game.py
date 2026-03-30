import sys
import random
import copy

# ANSI color constants
GREEN = "\033[92m"
RED = "\033[31m"
YELLOW = "\033[33m"
CYAN = "\033[36m"
BOLD = "\033[1m"
RESET = "\033[0m"


class Finish:
  """Manage a change in state of the program (end the game, change level, etc.)

  Attributes:
      use: A string that represents what this object will be used for
      conditions: A list of strings that stores conditions for the finish trigger
      description: A string that describes the finish object in the world
  """

  def __repr__(self) -> str:
    return "Transition object for new levels, win conditions, etc."

  def __init__(self) -> None:
    self.use = ""
    self.conditions = list()
    self.description = ""

  def executeFinish(self) -> None:
    print("You have elevated beyond academy forest to a more wild and unpredictable land...")
    print("Fair winds and following seas to you adventurer")
    sys.exit()


class Space:
  """Represents a place in the world.

  Attributes:
      description: A string to describe the space as it is in the world
      space_id: An integer that uniquely identifies the space
      x_coord: An integer for the x position on a 2D grid
      y_coord: An integer for the y position on a 2D grid
      north/south/east/west: References to neighboring Space objects (None if impassable)
      items: A list of Item objects in this space
      containers: A list of Inventory objects (chests, etc.)
      monsters: A list of Monster objects
      finish: A Finish object for win/transition conditions
  """

  def __repr__(self) -> str:
    return f"Space({self.space_id}, '{self.description[:30]}...')"

  def __init__(self, space_id: int, description: str):
    self.description = description
    self.space_id = space_id

    self.x_coord = -1
    self.y_coord = -1
    self.north = None
    self.south = None
    self.east = None
    self.west = None

    self.items = list()
    self.containers = list()
    self.monsters = list()
    self.finish = Finish()

  def setFinish(self, finish: Finish) -> None:
    self.finish = finish

  def describeSpace(self) -> None:
    print(f"\n* {self.description} *\n")

  def printCoordinates(self) -> None:
    print(f"X: {self.x_coord} Y: {self.y_coord}")

  def checkNorth(self) -> None:
    if isinstance(self.north, Space):
      self.north.describeSpace()
      return
    print("\nThe way is too thick and overgrown to travel.\n")

  def checkSouth(self) -> None:
    if isinstance(self.south, Space):
      self.south.describeSpace()
      return
    print("\nThe way is too thick and overgrown to travel.\n")

  def checkEast(self) -> None:
    if isinstance(self.east, Space):
      self.east.describeSpace()
      return
    print("\nThe way is too thick and overgrown to travel.\n")

  def checkWest(self) -> None:
    if isinstance(self.west, Space):
      self.west.describeSpace()
      return
    print("\nThe way is too thick and overgrown to travel.\n")

  def showItems(self) -> None:
    for item in self.items:
      print(f"\n{GREEN} {item.item_name} {RESET}\n")

  def showMonsters(self) -> None:
    for monster in self.monsters:
      if monster.state == "ALIVE":
        print(f"\n{RED} {monster.monster_type} {RESET}\n")

  def showContainers(self) -> None:
    for container in self.containers:
      print(f"\n{YELLOW} {container.container_type} {RESET}\n")


class Area:
  """Keep track of spaces and their relationship to one another on a 2D grid.

  Attributes:
      area_graph: A 2D array that contains references to Space objects
      space_list: A list of all Space objects in the area
  """

  def __repr__(self) -> str:
    return "A collection of spaces"

  def __init__(self, rows: int, cols: int) -> None:
    self.area_graph = [[0] * cols for _ in range(rows)]
    self.space_list = list()

  def assignSpace(self, space: Space, row: int, col: int) -> None:
    self.area_graph[row][col] = space
    space.y_coord = row
    space.x_coord = col
    self.space_list.append(space)


class Item:
  """A thing in the world that can be interacted with.

  Attributes:
      item_name: A string identifying the item
      description: A string describing the item in the world
      use: A string identifying interaction type (UNLOCK, ATTACK, EAT, END, etc.)
  """

  def __init__(self):
    self.item_name = "indescript object"
    self.description = "Just a plain object"
    self.use = "boink!"

  def printItem(self):
    print(f"\n{self.item_name}:\n   {self.description}\n")


class Inventory:
  """Hold and manage Items.

  Attributes:
      slots: A list of Items
      max_size: Maximum number of Items allowed
      locked: Whether the inventory contents are accessible
      container_type: Display name for this container in the world
  """

  def __init__(self):
    self.slots = list()
    self.max_size = 10
    self.locked = False
    self.container_type = "Bag"

  def addItem(self, item: Item) -> bool:
    if len(self.slots) < self.max_size:
      self.slots.append(item)
      return True
    return False

  def removeItem(self, item: Item) -> None:
    if item in self.slots:
      self.slots.remove(item)

  def showAllItems(self) -> None:
    for item in self.slots:
      item.printItem()


class Monster:
  """An adversary in the world.

  Attributes:
      hitpoints: Health of this monster
      power: Base damage this monster can deal
      monster_type: What kind of monster this is
      state: Physical state (ALIVE or DEAD)
  """

  def __repr__(self) -> str:
    return f"Monster({self.monster_type}, hp={self.hitpoints}, {self.state})"

  def __init__(self) -> None:
    self.hitpoints = 10
    self.power = 2
    self.monster_type = "Goblin"
    self.state = "ALIVE"

  def takeDamage(self, damage: int) -> None:
    self.hitpoints -= damage
    if self.hitpoints <= 0:
      self.hitpoints = 0
      self.state = "DEAD"

  def attack(self, player) -> None:
    if self.state == "ALIVE":
      player.takeDamage(self.power)


class Player:
  """Manages the state of the player throughout the world.

  Attributes:
      hitpoints: Health of the player
      power: Base damage the player can deal
      inventory: Inventory for the player's items
      location: The Space the player is currently in
  """

  def __repr__(self) -> str:
    return f"Player(hp={self.hitpoints}, sector={self.location.space_id})"

  def __init__(self) -> None:
    self.hitpoints = 10
    self.power = 1
    self.inventory = Inventory()
    self.location = Space(-1, "An odd white void.")

  def die(self):
    print("The end is nigh")

  def takeDamage(self, damage: int) -> None:
    self.hitpoints -= damage
    if self.hitpoints <= 0:
      self.hitpoints = 0
      self.die()

  def attack(self, target: Monster):
    target.takeDamage(self.power)

  def look(self, target: str) -> None:
    if target == "NORTH":
      self.location.checkNorth()
      return
    if target == "SOUTH":
      self.location.checkSouth()
      return
    if target == "EAST":
      self.location.checkEast()
      return
    if target == "WEST":
      self.location.checkWest()
      return
    if target == "INVENTORY":
      self.inventory.showAllItems()
      return

    self.location.describeSpace()
    self.location.showItems()
    self.location.showMonsters()
    self.location.showContainers()
    if self.location.finish.use:
      print(self.location.finish.description)

  def move(self, target: str) -> None:
    print("\n ** one foot in front of the other ** \n")

    direction_map = {
      "NORTH": self.location.north,
      "SOUTH": self.location.south,
      "EAST": self.location.east,
      "WEST": self.location.west,
    }

    destination = direction_map.get(target)
    if isinstance(destination, Space):
      self.location = destination
      self.location.describeSpace()
      return

    print("Gave it a go but the way is impassible.")

  def take(self, target: str) -> None:
    for item in self.location.items:
      if target == item.item_name.upper():
        print("TAKEN")
        print(item.item_name, ":", item.description)
        deep_copy_item = copy.deepcopy(item)
        self.location.items.remove(item)
        self.inventory.addItem(deep_copy_item)
        return
    print("Looked hard but cannot find a", target.lower(), "that can be taken")

  def use(self, target: str) -> None:
    if target == "KEY":
      hasKey = False
      key_index = -1

      for item in self.inventory.slots:
        if item.use.upper() == "UNLOCK":
          hasKey = True
          key_index = self.inventory.slots.index(item)

      if not self.location.containers:
        print("There is nothing here to unlock.")
        return

      if self.location.containers[0].locked and hasKey:
        self.location.containers[0].locked = False
        self.inventory.slots.pop(key_index)
        print("\nYou use the key and lay the contents on the ground\n")
        for item in list(self.location.containers[0].slots):
          deep_copy_item = copy.deepcopy(item)
          self.location.items.append(deep_copy_item)
        self.location.containers[0].slots.clear()
      return

    if target == "SWORD":
      alive_monsters = [m for m in self.location.monsters if m.state == "ALIVE"]
      if not alive_monsters:
        print("You swoosh and swish it a bit in the air. A neat move but that is about it.")
        return
      battle = Battle(self, alive_monsters[0])
      battle.engageBattle()
      # Remove dead monsters after battle
      self.location.monsters = [m for m in self.location.monsters if m.state != "DEAD"]
      return

    # Check if any inventory item triggers the finish condition
    for item in self.inventory.slots:
      if self.location.finish.use and item.use == self.location.finish.use:
        self.location.finish.executeFinish()


class Battle:
  """Manages the state of a battle engagement.

  Attributes:
      player: Reference to the Player
      monster: Reference to the Monster being fought
      engaged: Whether the battle loop should continue
      rewards: Items awarded on victory
  """

  def __repr__(self) -> str:
    return "A battle instance"

  def __init__(self, player: Player, monster: Monster) -> None:
    self.player = player
    self.monster = monster
    self.engaged = True
    self.rewards = list()

  def surveyBattle(self) -> None:
    print(f"*\n\n{RED}---> You are engaged in battle! <---{RESET}\n")
    print(f"  You : {self.player.hitpoints} hp")
    print(f"  {self.monster.monster_type} : {self.monster.hitpoints} hp\n")
    if self.monster.hitpoints <= 0:
      self.processResult("WIN")
    elif self.player.hitpoints <= 0:
      self.processResult("LOSS")

  def processResult(self, result: str) -> None:
    if result == "WIN":
      print("*******************")
      print(f"**** {GREEN}VICTORY{RESET} ****")
      print("*******************\n")
      if self.rewards:
        print(f"\n{GREEN} Rewards have dropped to the ground!!! {RESET}\n")
        for item in self.rewards:
          self.player.location.items.append(item)

    if result == "LOSS":
      print("``````````````````")
      print(f"`````{RED} DEFEAT {RESET}`````")
      print("``````````````````")

    self.engaged = False

  def playerTurn(self) -> None:
    self.surveyBattle()
    if not self.engaged:
      return
    print("Actions:\n (A)ttack \n (R)treat \n")
    action = input("-//>> ")
    if action.upper() == "A":
      damage = self.player.power * random.randint(1, 3)
      print(f"Hit! You deal {damage} damage!")
      self.monster.hitpoints -= damage
      if self.monster.hitpoints <= 0:
        self.monster.hitpoints = 0
        self.monster.state = "DEAD"
    elif action.upper() == "R":
      print("\n\n<<<<<<< Retreat!\n\n")
      self.engaged = False

  def monsterTurn(self) -> None:
    if self.monster.hitpoints <= 0:
      return
    damage = self.monster.power * random.randint(0, 3)
    print(f"\n <<---\\\\ ATTACKED! -{damage} hp\n")
    self.player.hitpoints -= damage

  def generateRewards(self) -> None:
    item_1 = Item()
    item_1.description = "A scroll. It is mostly in another language, elvish? The part that can be made out reads 'PASS'"
    item_1.use = "END"
    item_1.item_name = "Scroll"

    item_2 = Item()
    item_2.description = "Brilliant red. Shiny. Smells of autumn."
    item_2.use = "EAT"
    item_2.item_name = "Apple"

    self.rewards.append(item_1)
    self.rewards.append(item_2)

  def engageBattle(self) -> None:
    self.generateRewards()
    while self.engaged:
      self.playerTurn()
      if not self.engaged:
        break
      self.monsterTurn()
      self.surveyBattle()

    print("nnnnnnnnnnnnnnnnnnnnnnnnnn")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("~~~ The Battle is Over ~~~")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("uuuuuuuuuuuuuuuuuuuuuuuuuu\n\n")


def parseAction(player: Player, action_string: str) -> None:
    formatted_act_str = action_string.upper().split(' ')
    default_response = f'"{action_string}" is a noble pursuit but cannot be done right now.'

    if len(formatted_act_str) <= 1:
      match formatted_act_str[0]:
          case "QUIT":
            exitProgram()
          case "EXIT":
            exitProgram()
          case "HELP":
            helpInfo()
          case _:
            print(default_response)
            return

    if len(formatted_act_str) == 2:
      match formatted_act_str[0]:
        case "LOOK":
          player.look(formatted_act_str[1])
        case "MOVE":
          player.move(formatted_act_str[1])
        case "TAKE":
          player.take(formatted_act_str[1])
        case "USE":
          player.use(formatted_act_str[1])
        case _:
          print(default_response)
          return

    if len(formatted_act_str) > 2:
      print("\nYou are a clever being. Me however, I can really only handle two words at a time.\n")


def exitProgram() -> None:
    print("There is an ancient saying that: reality rots your brain. Play more video games.\n\n")
    sys.exit()


def helpInfo() -> None:
    print("""
        Actions:
           move
              ex. move north

           look
              ex. look east

           take
              ex. take key

           use
              ex. use sword
        """)


def main():
  """Main entry point of the app."""

  print(f"\n\n\n\n\n|========================================================|")
  print(f"|||||||||||||||| {GREEN}Welcome to Academy Forest{RESET} ||||||||||||||")
  print(f"|========================================================|")

  player = Player()

  # Generate map
  forest1 = Space(1, "Somewhere in the Nomad's March.")
  forest2 = Space(2, "Somewhere amidst a decaying mire. The shadows seem to be alive, and move in the darkness.")
  forest3 = Space(3, "A stand of scorched trees amidst an emerald moor.")
  forest4 = Space(4, "A sunlit clearing amidst a verdant forest. A herd of wild boars moves noisily through the trees.")
  forest5 = Space(5, "A labyrinth of thorns amidst a forest of flowering trees.")
  forest6 = Space(6, "The trees are full of dancing lights and mysterious laughter.")
  forest7 = Space(7, "A forest of flowering trees. The air is strangely still and quiet.")
  forest8 = Space(8, "A shadowed part of the forest. A stream of clear water winds its way through the trees.")
  forest9 = Space(9, "Among the trees and moss is a long abandoned stone hut. A wooden chest lies outside.")

  # Map layout:
  #   0 0 0 0 0
  #   7 1 2 0 0
  #   0 0 3 5 0
  #   0 0 4 6 0
  #   0 9 8 0 0
  row_len = 5
  col_len = 5
  forest_area = Area(row_len, col_len)

  forest_area.assignSpace(forest1, 1, 1)
  forest_area.assignSpace(forest2, 1, 2)
  forest_area.assignSpace(forest3, 2, 2)
  forest_area.assignSpace(forest4, 3, 2)
  forest_area.assignSpace(forest5, 2, 3)
  forest_area.assignSpace(forest6, 3, 3)
  forest_area.assignSpace(forest7, 1, 0)
  forest_area.assignSpace(forest8, 4, 2)
  forest_area.assignSpace(forest9, 4, 1)

  # Link neighboring spaces
  for row_index in range(row_len):
    for col_index in range(col_len):
      space = forest_area.area_graph[row_index][col_index]

      if not isinstance(space, Space):
        continue

      if col_index != col_len - 1:
        neighbor = forest_area.area_graph[row_index][col_index + 1]
        if isinstance(neighbor, Space):
          space.east = neighbor

      if col_index != 0:
        neighbor = forest_area.area_graph[row_index][col_index - 1]
        if isinstance(neighbor, Space):
          space.west = neighbor

      if row_index != row_len - 1:
        neighbor = forest_area.area_graph[row_index + 1][col_index]
        if isinstance(neighbor, Space):
          space.south = neighbor

      if row_index != 0:
        neighbor = forest_area.area_graph[row_index - 1][col_index]
        if isinstance(neighbor, Space):
          space.north = neighbor

  # Place player
  player.location = forest3
  forest3.describeSpace()

  # Create treasures
  key = Item()
  key.item_name = "Key"
  key.description = "A rusty key made of bronze. It is large enough for a door or small chest."
  key.use = "UNLOCK"

  sword = Item()
  sword.item_name = "Sword"
  sword.description = "A silver short sword. It has a bit of a glow to it."
  sword.use = "ATTACK"

  chest_1 = Inventory()
  chest_1.locked = True
  chest_1.max_size = 2
  chest_1.container_type = "Chest"

  # Create monsters
  goblin_1 = Monster()

  # Populate world with treasures and beasts
  forest3.items.append(key)
  forest3.containers.append(chest_1)
  chest_1.addItem(sword)
  forest3.monsters.append(goblin_1)

  # Create and place finish condition
  finish_point = Finish()
  finish_point.use = "END"
  finish_point.description = "A pedestal sits here. It has an outline of dust on top that forms the shape of a piece of paper.\n"
  finish_space_index = random.randint(0, len(forest_area.space_list) - 1)
  forest_area.space_list[finish_space_index].setFinish(finish_point)

  # Game loop
  while True:
    try:
      action_string = input("::> ")
      parseAction(player, action_string)
      if player.hitpoints <= 0:
        exitProgram()
    except (KeyboardInterrupt, EOFError):
      print()
      exitProgram()


if __name__ == "__main__":
  main()

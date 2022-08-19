import sys
import random
import copy


class Finish:
  """Manage a change in state of the program. i.e end the game loop, change the map object

  Attributes:
      use: A string that represents what this object will be used for
      conditions: A list of strings that stores the conditions that must be met for finish object to change the state
      description: A string that optionally describes what the finish object will represent in the program
  """

  def __repr__(self) -> str:
    return "Transisiton object for new levels, win conditions, etc."
  
  def __init__(self) -> None:
    self.use = ""
    self.conditions = list()
    self.description = ""
  
  def executeFinish(self) -> None:
    #TODO: make this more modular
      print("You have elevated beyond acedemy forest to a more wild and unpredictable land...")
      print("Fair winds and following seas to you adventurer")
      sys.exit()

class Space:
  """Represents a place in the world
  
  Attributes:
      description: A string to optionally describe the space as it is in the world
      space_id: An integer that uniquely identifies TODO: needs a hash function or similar to prevent collision
    
      #Location information
      x_coord: An integer representing where this space would be located on a grid or 2d array in the x positiion
      y_coord: An integer representing where this space would be located on a grid or 2d array in the y positiion
      north: A reference to a Space object that is -1,0 (row,column) in the grid or 2d array 
      south: A reference to a Space object that is +1,0 (row,column) in the grid or 2d array
      east: A reference to a Space object that is 0,+1 (row,column) in the grid or 2d array
      west: A reference to a Space object that is 0,-1 (row,column) in the grid or 2d array

    # Objects, such as items and monsters, in this space
      items: A list that contains Item objects
      containers: A list that contains Inventory objects
      monsters = A list that contains Monster objects
      finish = A reference to a Finish object

  """
  def __repr__(self):
    return "A space"
  
  def __init__(self,space_id:int, description: str):
    self.description = description
    self.space_id = space_id
    
    #Location information
    self.x_coord = -1
    self.y_coord = -1
    self.north = ""
    self.south = ""
    self.east = ""
    self.west = ""

    # Objects, such as items and monsters, in this space
    self.items = list()
    self.containers = list()
    self.monsters = list()
    self.finish = Finish()

  def setFinish(self, finish:Finish) -> None:
    self.finish = finish

  def describeSpace(self) -> None:
    print("\n* {description} *\n".format(description=self.description))
    
  def interact(self, use: str) -> None:
    print(use + " nothing much else.")
  
  def printCoordinates(self) -> None:
    print("X: " + self.x_coord + "Y: " + self.y_coord)

  def checkNorth(self) -> None:
    if type(self.north) == Space: 
      self.north.describeSpace()
      return
    print("\nThe way is too thick and overgrown to travel.\n")
  
  def checkSouth(self) -> None:
    if type(self.south) == Space: 
      self.south.describeSpace()
      return
    print("\nThe way is too thick and overgrown to travel.\n")

  def checkEast(self) -> None:
    if type(self.east) == Space: 
      self.east.describeSpace()
      return
    print("\nThe way is too thick and overgrown to travel.\n")

  def checkWest(self) -> None:
    if type(self.west) == Space: 
      self.west.describeSpace()
      return
    print("\nThe way is too thick and overgrown to travel.\n")

  def showItems(self) -> None:
    for item in self.items:
      print("\n\033[92m", item.item_name, "\033[37m \n")
  
  def showMonsters(self) -> None:
    for monster in self.monsters:
      print("\n\033[31m", monster.monster_type, "\033[37m \n")
  
  def showContainers(self) -> None:
    for container in self.containers:
      print("\n\033[33m", container.container_type, "\033[37m\n")

class Area:
  """Keep track of spaces and their relationship to one another on a 2d grid

  Attributes:
      area_graph: A 2d array that contains references to Space objects
      space_list: A list of all Space objects referenced in the area_graph
  """
  def __repr__():
      return "A collection of spaces"
  
  def __init__(self, rows:int, cols:int) -> list:
    self.area_graph = [[0] * cols for i in range(rows)]
    self.space_list = list()

  def assignSpace(self,space:Space, row:int, col:int) -> None:
    self.area_graph[row][col] = space
    space.y_coord = row
    space.x_coord = col
    self.space_list.append(space)

class Item:
  """A thing in the world that can be interacted with and can be described

  Attributes:
      item_name: A string that identifys the type of item
      description: A string that gives a description to be used in the world
      use: A string used for identifing interaction possbilities
  """
  def __init__(self):
    self.item_name = "indescript object"
    self.description = "Just a plain object"
    self.use = "boink!"
  
  def printItem(self):
    print("\n{name}:\n   {item_description}\n".format(name=self.item_name, item_description=self.description))
  
  def useItem(self):
    print(self.use + ". Nothing much happens.") 

class Inventory:
  """Hold and manage other objects such as Items

  Attributes:
      slots: A list of Items
      max_size: An integer representing the maximum number of Items that can be keep track of
      locked: A bool that indicates whether the list of items are authorized to be accessed or not
      container_type: A string to plainly represent in words what the Inventory is in the world
  """
  def __init__(self):
    self.slots = list()
    self.max_size = 10
    self.locked = False
    self.container_type = "Bag"

  def addItem(self, item: Item) -> None:
    if len(self.slots) < self.max_size:
      self.slots.append(item)
  
  def removeItem(self, item: Item) -> None:
    if item in self.slots:
      self.slots.pop(item)

  def lookAtItem(self, item: Item) -> str:
    if item in self.slot: return item
  
  def showAllItems(self) -> list:
    for item in self.slots:
      item.printItem()

class Monster:
  """An adversary in the world

  Attributes:
      hitpoints: An integer representing the health of this monster
      power: An integer representing the amount of base damage this monster can do
      monster_type: A string that has the description of what kind of monster this is
      state: A string representing the physical state of the monster in the world
  """
  def __repr__(self) -> str:
      pass

  def __init__(self) -> None:
      self.hitpoints = 10
      self.power = 0.5
      self.monster_type = "Goblin"
      self.state = "ALIVE"
  
  def takeDamage(self, damage:int) -> None:
      self.hitpoints - damage
      if self.hitpoints <= 0:
          self.state = "DEAD"

  def attack(self, player) -> None:
      if self.state == "ALIVE":
          player.takeDamge(self.power)

class Player:
  """Manages the state of the player throughout the world

  Attributes:
      hitpoints: An integer representing the health of the player
      power: An integer representing the amount of base damage the player can do
      inventory: An Inventory object that is used to keep track of Items related to the player
      location: A reference to a Space that the player can currently interact with
  """
  def __repr__(self) -> str:
      pass

  def __init__(self) -> None:
      self.hitpoint = 10
      self.power = 1
      self.inventory = Inventory()
      #Space the player is currently in
      self.location = Space(-1,"An odd white void.")

  def die(self):
      print("The end is nigh")

  def takeDamage(self, damage:int) -> None:
      self.hitpoints - damage
      if self.hitpoints <= 0:
          self.die()

  def attack(self, target:Monster):
      target.takeDamage(self.power)    
  
  def look(self,target:str) -> None:
    
    if target == "NORTH": self.location.checkNorth(); return 
    if target == "SOUTH": self.location.checkSouth(); return
    if target == "EAST":  self.location.checkEast(); return
    if target == "WEST":  self.location.checkWest(); return
    if target == "INVENTORY": self.inventory.showAllItems(); return

    self.location.describeSpace()
    self.location.showItems()
    self.location.showMonsters()
    self.location.showContainers()
    if type(self.location.finish) == Finish:
      print(self.location.finish.description)

  def move(self,target:str) -> None:
    print("\n ** one foot in front of the other ** \n")

    #Move North
    if target == "NORTH" and type(self.location.north) == Space:
      self.location = self.location.north
      self.location.describeSpace()
      return

    #Move South
    if target == "SOUTH" and type(self.location.south) == Space:
      self.location = self.location.south
      self.location.describeSpace()
      return
    
    #Move East
    if target == "EAST" and type(self.location.east) == Space:
      self.location = self.location.east
      self.location.describeSpace()
      return
    
    #Move West
    if target == "WEST" and type(self.location.west) == Space:
      self.location = self.location.west
      self.location.describeSpace()
      return
    
    print("Gave it a go but the way is impassible.")

  def take(self,target:str) -> None:
    for item in self.location.items:
      if target in item.item_name.upper():
        print("TAKEN")
        print(item.item_name,":",item.description)
        deep_copy_item = copy.deepcopy(item)
        self.location.items.remove(item)
        self.inventory.addItem(deep_copy_item)
        return
    print("Looked hard but cannot find a", target.lower(), "that can be taken")

  def use(self,target:str) -> None:
      if target == "KEY":
        #Open item check
        hasKey = False
        key_index = -1
        
        for item in self.inventory.slots:
          print(item.use)
          if item.use.upper() == "UNLOCK":
            hasKey = True
            key_index = self.inventory.slots.index(item)
            print("Found key in inventory")

        #Will try the first container in the space for now. TODO: Look through / select containers
        if self.location.containers[0].locked == True and hasKey == True:
          self.location.containers[0].locked == False
          self.inventory.slots.pop(key_index)
          print("\nYou use the key and lay the contains on the ground\n")
          for item in self.location.containers[0].slots:
            deep_copy_item = copy.deepcopy(item)
            self.location.items.append(deep_copy_item)
            self.location.containers[0].slots.remove(item)

      if target == "SWORD":
        if self.location.monsters.count == 0: print("You swoosh and swish it a bit in the air. A neat move but that is about it."); return
        battle = Battle(self, self.location.monsters[0])
        battle.engaugeBattle()

      for item in self.inventory.slots:
        if item.use == self.location.finish.use:
          self.location.finish.executeFinish()

class Battle:
  """Manages the state of a battle engaugement

  Attributes:
      player: A reference to the Player
      monster: A reference to a Monster
      engauged: A bool that tracks whether the battle loop should continue or end
      rewards: A list of Items that will be presented given a successful outcome
  """
  def __repr__(self) -> str:
    return "A battle instance"
  
  def __init__(self,player:Player, monster:Monster) -> None:
    self.player = player
    self.monster = monster
    self.engauged = True
    self.rewards = list()

  def surveyBattle(self) -> None:
    print("*\n\n\033[31m---> You are engauged in battle! <---\033[37m \n\n Staring down at the challenge ahead:\n")
    print("You : ", self.player.hitpoint, " hp")
    print(self.monster.monster_type, " : ", self.monster.hitpoints, " hp\n\n")
    if self.monster.hitpoints <= 0:
      self.processResult("WIN")
    if self.player.hitpoint <= 0:
      self.processResult("LOSS")

  def processResult(self, result:str) -> None:
    if result == "WIN":
      print("*******************")
      print("**** \033[32m VICTORY \033[37m ****")
      print("*******************\n")
      if len(self.rewards) >= 0:
        print("\n \033[32m Rewards have dropped to the ground!!! \033[37m \n")
        for item in self.rewards:
          self.player.location.items.append(item)

    if result == "LOSS":
      print("``````````````````")
      print("`````\033[31m DEFEAT \033[37m`````")
      print("``````````````````")
    
    self.engauged = False

  def playerTurn(self) -> None:
    self.surveyBattle()
    print("Actions:\n (A)ttack \n (R)treat \n")
    action = input("-//>> ")
    if action == "A" or action == "a":
      print("Hit!")
      self.monster.hitpoints -= self.player.power * random.randint(0, 3)
    if action == "R" or action == "r":
      print("\n\n<<<<<<< Retreat!\n\n")
      self.engauged = False

  def monsterTurn(self) -> None:
    print("\n\n <<---\\\\ ATTACKED!\n\n")
    print("-",self.monster.power)
    self.player.hitpoint -= self.monster.power  * random.randint(0, 3)

  def generateRewards(self) -> None:
    #Test data here for now. TODO: make rewards random
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

  def engaugeBattle(self) -> None:
    self.generateRewards()
    while self.engauged == True:
      self.playerTurn()
      self.monsterTurn()
      self.surveyBattle()

    print("nnnnnnnnnnnnnnnnnnnnnnnnnn")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("~~~ The Battle is Over ~~~")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("uuuuuuuuuuuuuuuuuuuuuuuuuu\n\n")

def parseAction(player:Player, action_string:str) -> None:
    formatted_act_str = action_string.upper().split(' ')
    default_response = '"' + action_string + '"' + " is a noble persuit but can not be done right now. "
    
    #Commands with only 1 arguments
    if len(formatted_act_str) <= 1:
      match formatted_act_str[0]:
          case "QUIT" : exitProgram() 
          case "EXIT" : exitProgram()
          case "HELP" : helpInfo()              
          case _: print(default_response); return

    if len(formatted_act_str) == 2:
      match formatted_act_str[0]:
        case "LOOK" : player.look(formatted_act_str[1]) 
        case "MOVE" : player.move(formatted_act_str[1])
        case "TAKE" : player.take(formatted_act_str[1])
        case "USE" : player.use(formatted_act_str[1])
        case _: print(default_response); return
            
    if len(formatted_act_str) > 2:
      print("\nYou are a clever being. Me however, I can really only handle two words at a time :)\n")

def exitProgram() -> None:
    print("There is an ancient saying that: reality rots your brain. Play more video games ;)\n\n")
    sys.exit()

def helpInfo() -> None:
    print(
        """ 
        Actions:
           move
              ex. move north

           look
              ex. look box

           take
              ex. take apple

           use
              ex. use sword              
        """)
    
def main():
  """ Main entry point of the app """

  print("\n\n\n\n\n|========================================================|")
  print("|||||||||||||||| \033[92m Welcome to Academy Forest \033[37m||||||||||||||")
  print("|========================================================|")

  player = Player()

  # Generate map
  forest1 = Space(1,"Somewhere in the Nomad's March.")
  forest2 = Space(2,"Somewhere amidst a decaying mire. The shadows seem to be alive, and move in the darkness.")
  forest3 = Space(3,"A stand of scorched trees amidst an emerald moor.")
  forest4 = Space(4,"A sunlit clearing amidst a verdant forest. A herd of wild boars moves noisily through the trees.")
  forest5 = Space(5,"A labyrinth of thorns amidst a forest of flowering trees.")
  forest6 = Space(6,"The trees are full of dancing lights and mysterious laughter.")
  forest7 = Space(7,"A forest of flowering trees. The air is strangely still and quiet.")
  forest8 = Space(8,"A shadowed part of the forest. A stream of clear water winds its way through the trees.")
  forest9 = Space(9,"Among the trees and moss is a long abandon stone hut. A wooden chest lies outstide.")

  """
  Example hardcoded map for testing. This can be ingested in future revision to populate an area.

      0 0 0 0 0
      7 1 2 0 0
      0 0 3 5 0
      0 0 4 6 0
      0 9 8 0 0

  """
  #Populate Area to keep track of overview of spaces in relation to one another
  #Number of indexes that will make up the area. It will be a square rowsxcols.
  row_len = 5
  col_len = 5
  forest_area = Area(row_len,col_len)
  
  forest_area.assignSpace(forest1,1,1)
  forest_area.assignSpace(forest2,1,2)
  forest_area.assignSpace(forest3,2,2)
  forest_area.assignSpace(forest4,3,2)
  forest_area.assignSpace(forest5,2,3)
  forest_area.assignSpace(forest6,3,3)
  forest_area.assignSpace(forest7,1,0)
  forest_area.assignSpace(forest8,4,2)
  forest_area.assignSpace(forest9,4,1)

#Identify and locally store in each space it's neighbors to the north south east and west
  for row_index in range(row_len):
    for col_index in range(col_len):
      space = forest_area.area_graph[row_index][col_index]
      
      #Zero represents an untravelable space; All others are expected to be of type Space
      if type(space) != Space: continue
      
      #Neighbors to the East
      if col_index != col_len - 1:
        if type(forest_area.area_graph[row_index][col_index + 1]) == Space:
          forest_area.area_graph[row_index][col_index].east = forest_area.area_graph[row_index][col_index + 1]
          
      #Neighbors to the West
      if col_index != 0:
        if type(forest_area.area_graph[row_index][col_index - 1]) == Space:
          forest_area.area_graph[row_index][col_index].west = forest_area.area_graph[row_index][col_index - 1]
          
      #Neighbors to the South
      if row_index != row_len - 1:
        if type(forest_area.area_graph[row_index + 1][col_index]) == Space:
          forest_area.area_graph[row_index][col_index].south = forest_area.area_graph[row_index + 1][col_index]
          
      #Neighbors to the North
      if row_index != 0:
        if type(forest_area.area_graph[row_index - 1][col_index]) == Space:
          forest_area.area_graph[row_index][col_index].north = forest_area.area_graph[row_index - 1][col_index]
              
  #Place player
  player.location = forest3
  forest3.describeSpace()

  #Create treasures
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
  
  #Create monsters
  goblin_1 = Monster()

  #Populate world with treasures and beasts
  starting_pt_index = forest_area.space_list.index(forest3)
  forest_area.space_list[starting_pt_index].items.append(key)
  forest_area.space_list[starting_pt_index].containers.append(chest_1)
  chest_1.addItem(sword)
  forest_area.space_list[starting_pt_index].monsters.append(goblin_1)

  #Create and place finish condition
  finish_point = Finish()
  finish_point.use = "END"
  finish_point.description = "A petestal sits here. It has an outline of dust on top that forms the shape of a piece of paper.\n"
  finish_space_index = random.randint(0,len(forest_area.space_list) - 1)
  forest_area.space_list[finish_space_index].setFinish(finish_point)


  #Game loop
  play_game = True
  action_string = ""
  while(play_game == True):
      action_string = input("::> ")
      parseAction(player, action_string)
      if player.hitpoint <= 0: exitProgram()

if __name__ == "__main__":
  main()
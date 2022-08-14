import sys
import copy

class Space:
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
      print("\n \033[92m", item.item_name, "\033[37m \n")
  
  def showMonsters(self) -> None:
    for monster in self.monsters:
      print("\n", monster.monster_type, "\n")
  
  def showContainers(self) -> None:
    for container in self.containers:
      print("\n", container.container_type, "\n")

class Area:
    def __repr__():
        return "A collection of spaces"
    
    def __init__(self, rows:int, cols:int) -> list:
      self.area_graph = [[0] * cols for i in range(rows)]
      self.space_list = list()

    def assignSpace(self,space:Space, row:int, col:int) -> None:
      self.area_graph[row][col] = space
      space.y_coord = row
      space.x_coord = col

class Item:
  def __init__(self):
    self.item_name = "indescript object"
    self.description = "Just a plain object"
    self.use = "boink!"
  
  def printItem(self):
    print("\n{name}:\n   {item_description}\n".format(name=self.item_name, item_description=self.description))
  
  def useItem(self):
    print(self.use + ". Nothing much happens.") 

class Inventory:
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

class Battle:
  def __repr__(self) -> str:
    return "A battle instance"
  
  def __init__(self,player:Player, monster:Monster) -> None:
    self.player = player
    self.monster = monster
    self.engauged = True

  def surveyBattle(self) -> None:
    print("*\\---> You've are engaugedd in battle! <---//* \n Staring down at the challenge ahead:")
    print("You : \n", self.player.hitpoint, " hp\n\n")
    print("\nOpponent : ", self.monster.monster_type, " : ", self.monster.hitpoints, " hp\n\n")
  
  def playerTurn(self) -> None:
    print("Actions:\n (A)ttack \n (R)treat")
    action = input("-//>> ")
    if action == "A" or action == "a":
      print("Hit!")
      self.monster.hitpoints -= self.player.power
    if action == "R" or action == "r":
      print("\n\n<<<<<<< Retreat!\n\n")
      self.engauged = False

  def monsterTurn(self) -> None:
    print("\n\n <<---\\\\ ATTACKED!\n\n")
    print("-",self.monster.power)
    self.player.hitpoint -= self.monster.power

  def engaugeBattle(self) -> None:
    while self.engauged == True:
      self.playerTurn()
      self.monsterTurn()
      self.surveyBattle()
    print(""" ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
              ~~~ The Battle is Over ~~~
              ~~~~~~~~~~~~~~~~~~~~~~~~~~
          """)
def parseAction(player:Player, action_string:str) -> None:
    formatted_act_str = action_string.upper().split(' ')
    default_response = '"' + action_string + '"' + " is a noble persuit but can not be done right now. "
    
    #Commands with only 1 arguments
    if len(formatted_act_str) <= 1:
      match formatted_act_str[0]:
          case "QUIT" : exitProgram() 
          case "EXIT" : exitProgram()
          case "HELP" : helpInfo()              
          case _: print(default_response)

    if len(formatted_act_str) == 2:
      match formatted_act_str[0]:
        case "LOOK" : look(player, formatted_act_str[1]) 
        case "MOVE" : move(player, formatted_act_str[1])
        case "TAKE" : take(player, formatted_act_str[1])
        case "USE" : use(player, formatted_act_str[1])
            
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

def look(player:Player, target:str) -> None:
  
  if target == "NORTH": player.location.checkNorth(); return 
  if target == "SOUTH": player.location.checkSouth(); return
  if target == "EAST":  player.location.checkEast(); return
  if target == "WEST":  player.location.checkWest(); return
  if target == "INVENTORY": player.inventory.showAllItems(); return

  player.location.describeSpace()
  player.location.showItems()
  player.location.showMonsters()
  player.location.showContainers()

def move(player:Player, target:str) -> None:
  print("\n ** one foot in front of the other ** \n")

  #Move North
  if target == "NORTH" and type(player.location.north) == Space:
    player.location = player.location.north
    player.location.describeSpace()
    return

  #Move South
  if target == "SOUTH" and type(player.location.south) == Space:
    player.location = player.location.south
    player.location.describeSpace()
    return
  
  #Move East
  if target == "EAST" and type(player.location.east) == Space:
    player.location = player.location.east
    player.location.describeSpace()
    return
  
  #Move West
  if target == "WEST" and type(player.location.west) == Space:
    player.location = player.location.west
    player.location.describeSpace()
    return
  
  print("Gave it a go but the way is impassible.")

def take(player:Player, target:str) -> None:
  for item in player.location.items:
    if target in item.item_name.upper():
      deep_copy_item = copy.deepcopy(item)
      player.location.items.remove(item)
      player.inventory.addItem(deep_copy_item)
      return
  print("Looked hard but cannot find a ", target.lower())

def use(player:Player, target:str) -> None:
  if target == "KEY":
    #Open item check
    hasKey = False
    key_index = -1
    
    for item in player.inventory.slots:
      print(item.use)
      if item.use.upper() == "UNLOCK":
        hasKey = True
        key_index = player.inventory.slots.index(item)
        print("Found key in inventory")

    #Will try the first container in the space for now. TODO: Look through / select containers
    if player.location.containers[0].locked == True and hasKey == True:
      player.location.containers[0].locked == False
      player.inventory.slots.pop(key_index)
      print("\nYou use the key and lay the contains on the ground\n")
      for item in player.location.containers[0].slots:
        deep_copy_item = copy.deepcopy(item)
        player.location.items.append(deep_copy_item)
        player.location.containers[0].slots.remove(item)

  if target == "SWORD":
    if player.location.monsters.count == 0: print("You swoosh and swish it a bit in the air. A neat move but that is about it."); return
    battle = Battle(player, player.location.monsters[0])
    battle.engaugeBattle()
    
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
  forest_area.space_list.append(forest1)

  forest_area.assignSpace(forest2,1,2)
  forest_area.space_list.append(forest2)

  forest_area.assignSpace(forest3,2,2)
  forest_area.space_list.append(forest3)

  forest_area.assignSpace(forest4,3,2)
  forest_area.space_list.append(forest4)

  forest_area.assignSpace(forest5,2,3)
  forest_area.space_list.append(forest4)

  forest_area.assignSpace(forest6,3,3)
  forest_area.space_list.append(forest5)

  forest_area.assignSpace(forest7,1,0)
  forest_area.space_list.append(forest6)

  forest_area.assignSpace(forest8,4,2)
  forest_area.space_list.append(forest7)

  forest_area.assignSpace(forest9,4,1)
  forest_area.space_list.append(forest7)

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
          # print("Space ",forest_area.area_graph[row_index][col_index].space_id," has a neighbor to the east : ", forest_area.area_graph[row_index][col_index + 1].space_id)
      
      #Neighbors to the West
      if col_index != 0:
        if type(forest_area.area_graph[row_index][col_index - 1]) == Space:
          forest_area.area_graph[row_index][col_index].west = forest_area.area_graph[row_index][col_index - 1]
          # print("Space ",forest_area.area_graph[row_index][col_index].space_id," has a neighbor to the west : ", forest_area.area_graph[row_index][col_index - 1].space_id)
      
      #Neighbors to the South
      if row_index != row_len - 1:
        if type(forest_area.area_graph[row_index + 1][col_index]) == Space:
          forest_area.area_graph[row_index][col_index].south = forest_area.area_graph[row_index + 1][col_index]
          # print("Space ",forest_area.area_graph[row_index][col_index].space_id," has a neighbor to the south : ", forest_area.area_graph[row_index + 1][col_index].space_id)
      
      #Neighbors to the North
      if row_index != 0:
        if type(forest_area.area_graph[row_index - 1][col_index]) == Space:
          forest_area.area_graph[row_index][col_index].north = forest_area.area_graph[row_index - 1][col_index]
          # print("Space ",forest_area.area_graph[row_index][col_index].space_id," has a neighbor to the north : ", forest_area.area_graph[row_index - 1][col_index].space_id)
    
    
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

  #Game loop
  play_game = True
  action_string = ""
  while(play_game == True):
      action_string = input("::> ")
      parseAction(player, action_string)

if __name__ == "__main__":
  main()
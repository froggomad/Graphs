from room import Room
from player import Player
from world import World
from copy import copy

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
#map_file = "maps/test_line.txt" #pass 2 moves
#map_file = "maps/test_cross.txt" #pass 14 moves


map_file = "maps/test_loop.txt" #pass 14 moves
#map_file = "maps/test_loop_fork.txt"
#map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
#TODO: track visited rooms, add to traversal path as appropriate

#init
traversal_path = []
forks = {}
visited = set()
current_room = player.current_room
visited.add(current_room)

#surrounding rooms
east_room = current_room.get_room_in_direction("e")
west_room = current_room.get_room_in_direction("w")
north_room = current_room.get_room_in_direction("n")
south_room = current_room.get_room_in_direction("s")

#set direction to travel after moving
def first_visit():
    east_room = current_room.get_room_in_direction("e")
    west_room = current_room.get_room_in_direction("w")
    north_room = current_room.get_room_in_direction("n")
    south_room = current_room.get_room_in_direction("s")

    if east_room != None and east_room not in visited:
        return "e"
    elif west_room != None and west_room not in visited:
        return "w"
    elif north_room != None and north_room not in visited:
        return "n"
    elif south_room != None and south_room not in visited:
        return "s"

    return False

def reverse_dir(dir):
    if dir == "n":
        return "s"
    elif dir == "s":
        return "n"
    elif dir == "e":
        return "w"
    else:
        return "e"

def return_to_fork():
    """travel back to the last fork by reverse-traversing `traversal_path` until current_room == fork"""
    #get the last fork in the dict (python 3.6+ has ordered dicts by default)
    last_fork = list(forks.items())[-1][0]
    #copy the traversal list so we can modify it to efficiently get back to the last fork
    temp_traverse = copy(traversal_path)
    while current_room.id != last_fork.id:
        print(f"returning to fork at {last_fork.id}. currently at {current_room.id}")
        dir = reverse_dir(temp_traverse.pop())
        travel(dir)
    if first_visit():
        travel(first_visit())
    else:
        travel(forks[last_fork][0])

def first_available():
    return current_room.get_exits()[0]

def travel(dir):
    global current_room
    #room before travelling
    if current_room in forks:
        if dir in forks[current_room]:
            forks[current_room].remove(dir)
        if forks[current_room] == []:
            forks[current_room] = None

    player.travel(dir)
    traversal_path.append(dir)
    current_room = player.current_room    
    if current_room not in visited:
        visited.add(current_room)
        #add current room to forks if it has more than one exit
        exits = current_room.get_exits()
        if len(exits) > 1:
            forks[current_room] = exits

def backtrack():
    while first_visit() == False:
        return_to_fork()
    return first_visit()

# MARK: Run Loop
while len(visited) < len(room_graph):    
    visit = first_visit()
    print(f"step: {len(traversal_path)}")
    print(f"I'm going {visit}")
    if visit:
        travel(visit)
    else:
        #TODO: Backtrack to last node where there was a choice
        while not visit:
            backtrack()
            visit = first_visit()
    
        print(f"I'm stuck at {current_room.id}")


# MARK: TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")
    print(visited_rooms)



#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        pass
        #player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")

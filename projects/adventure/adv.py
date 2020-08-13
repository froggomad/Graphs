from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt" #pass 3 moves
map_file = "maps/test_cross.txt" #pass 15 moves


#map_file = "maps/test_loop.txt" #fail, infinite loop
# map_file = "maps/test_loop_fork.txt"
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
traversal_path = [0]
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

def first_available():
    east_room = current_room.get_room_in_direction("e")
    west_room = current_room.get_room_in_direction("w")
    north_room = current_room.get_room_in_direction("n")
    south_room = current_room.get_room_in_direction("s")

    if east_room != None:
        return "e"
    elif west_room != None:
        return "w"
    elif north_room != None:
        return "n"
    elif south_room != None:
        return "s"
    Exception("dead end")
    return False

def travel(dir):
    global current_room
    player.travel(dir)
    traversal_path.append(dir)
    current_room = player.current_room
    if current_room not in visited:
        visited.add(current_room)

def travel_back(dir):
    room = current_room.get_room_in_direction(dir)
    if room:
        travel(dir)
    else:
        #TODO: Travel back to last fork
        travel(first_available())


def backtrack(from_dir):
    while first_visit() == False:
        if from_dir == "n":
            travel_back("s")
        if from_dir == "s":
            travel_back("n")
        if from_dir == "e":
            travel_back("w")
        if from_dir == "w":
            travel_back("e")
    return first_visit()

# MARK: Run Loop
while len(visited) < len(room_graph):
    visit = first_visit()
    if visit:
        travel(visit)
    else:
        #TODO: Backtrack to last node where there was a choice
        while not visit:
            backtrack(traversal_path[-1])
            visit = first_visit()
        #print("I'm stuck")


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

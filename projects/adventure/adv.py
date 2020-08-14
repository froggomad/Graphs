from room import Room
from player import Player
from world import World
from copy import copy

import random
from ast import literal_eval

class Queue():
    def __init__(self):
        self.queue = []
    def enqueue(self, value):
        self.queue.append(value)
    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None
    def size(self):
        return len(self.queue)

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
#map_file = "maps/test_line.txt" #pass 2 moves
#map_file = "maps/test_cross.txt" #pass 14 moves -> return_to_fork method 17 moves


#map_file = "maps/test_loop.txt" #pass 14 moves -> return_to_fork method 22 moves, BFT 20 moves
#map_file = "maps/test_loop_fork.txt" #pass -> return_to_fork method 35 moves, BFT 32 moves
map_file = "maps/main_maze.txt" #pass BFT 1026 moves

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

#init
traversal_path = []
visited = set()

# init hash map containing graphs of paths
room_maps = {
    0: {'n': '?', 's': '?', 'e': '?', 'w': '?'}
}

def reverse_dir(dir):
    if dir == "n":
        return "s"
    elif dir == "w":
        return "e"
    elif dir == "s":
        return "n"
    else:
        return "w"

def travel_map(dir):
    """create map of adjacent rooms, travel, and update room_maps"""
    directions = {}
    # room id before travel
    from_id = player.current_room.id
    from_dir = reverse_dir(dir)

    # get room id of room traveling to and update map
    room_id = player.current_room.get_room_in_direction(dir).id
    room_maps[from_id][dir] = room_id
    
    # travel and add directions to traversal_path
    player.travel(dir)
    traversal_path.append(dir)   

    if room_id not in room_maps:
        for exit in player.current_room.get_exits():
            reverse = reverse_dir(exit)

            exit_id = player.current_room.get_room_in_direction(exit).id
            # add new room
            if exit_id not in room_maps:
                directions[exit] = "?"                            
            # update room we traveled from in new room's directions:
            elif exit is from_dir:
                directions[exit] = from_id
            # handle loops by marking connected room with current room's id to avoid backtracking
            elif room_maps[exit_id][reverse] == "?":
                print(f"""
***
current room: {player.current_room.id}
came from room: {from_id} to the {reverse}
marking: room {exit_id} to the {exit}
with id: {player.current_room.id}
***
                    """)
                    
                room_maps[exit_id][reverse] = room_id

        room_maps[room_id] = directions

def find_nearest_exit(to_id):
    """perform BFS to find nearest exit ('?')"""
    queue = Queue()
    path = []
    queue.enqueue([(to_id, None)])
    visited_rooms = set()

    while queue.size() > 0:
        path = queue.dequeue()
        room = path[-1]

        for dir, room in room_maps[room[0]].items():
            # add room to path
            if room not in visited_rooms:
                room_path = list(path)
                room_path.append((room, dir))
                visited_rooms.add(room)
                
                queue.enqueue(room_path)
                # closest exit
                if room == "?":
                    room_path.pop(0)
                    path_to_room = [room[1] for room in room_path]
                    return path_to_room
    # path not found
    return None

# MARK: Run Loop

#init Stack with starting direction to avoid munging traversal_path
stack = list()
stack.append("n")

while len(room_graph) > len(room_maps):
    dir = stack.pop()
    next = player.current_room.get_room_in_direction(dir)

    exits = player.current_room.get_exits()
    # MARK: Traverse
    if next:
        stack.append(dir)
        travel_map(dir)

        print(f"I'm in room {player.current_room.id}. I came from the {reverse_dir(dir)}")
    # BFS to find next direction to add to stack 
    elif len(stack) == 0:
        for exit in exits:
            to_next_dir = find_nearest_exit(player.current_room.id)
            for i, to_room in enumerate(to_next_dir):
                travel_map(to_room)
                if i == len(to_next_dir) - 1:
                    stack.append(to_room)

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
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")

import random

class Stack():
    def __init__(self):
        self.stack = []
    def push(self, value):
        self.stack.append(value)
    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None
    def size(self):
        return len(self.stack)

class User:
    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        return f'User({repr(self.name)})'

class SocialGraph:
    def __init__(self):
        self.last_id = 0
        self.users = {}
        self.friendships = {}

    def add_friendship(self, user_id, friend_id):
        """
        Creates a bi-directional friendship
        """
        if user_id == friend_id:
            print("WARNING: You cannot be friends with yourself")
        elif friend_id in self.friendships[user_id] or user_id in self.friendships[friend_id]:
            print("WARNING: Friendship already exists")
        else:
            self.friendships[user_id].add(friend_id)
            self.friendships[friend_id].add(user_id)

    def add_user(self, name):
        """
        Create a new user with a sequential integer ID
        """
        self.last_id += 1  # automatically increment the ID to assign the new user
        self.users[self.last_id] = User(name)
        self.friendships[self.last_id] = set()

    def reset(self):
        self.last_id = 0
        self.users = {}
        self.friendships = {}

    def populate_graph(self, num_users, avg_friendships):
        """
        Takes a number of users and an average number of friendships
        as arguments

        Creates that number of users and a randomly distributed friendships
        between those users.

        The number of users must be greater than the average number of friendships.
        """
        # Reset graph
        self.reset()

        # Add users
        for i in range(num_users):
            self.add_user(f"User {i}")

        # Create friendships
        possible_friendships = []

        for user_id in self.users:
            for friend_id in range(user_id + 1, self.last_id + 1):
                possible_friendships.append((user_id, friend_id))
        random.shuffle(possible_friendships)

        for i in range(num_users * avg_friendships //2):
            friendships = possible_friendships[i]
            self.add_friendship(friendships[0], friendships[1])

    def get_all_social_paths(self, user_id):
        """
        Takes a user's user_id as an argument

        Returns a dictionary containing every user in that user's
        extended network with the shortest friendship path between them.

        The key is the friend's ID and the value is the path.

        ex:
        {1: {2, 4}, 2: {1, 3}, 3: {2, 4} 4: {1, 3} }

        how does 1 get to 3?
        """        
        visited = {}  # Note that this is a dictionary, not a set
        #init stack with connection to self ([self])
        stack = Stack()
        stack.push([user_id])
        visited[user_id] = [user_id]
        while stack.size() > 0:
            #get last friend in friendships
            friendships = stack.pop()
            friend = friendships[-1]
            #get connection to each friend
            for outside_friend in self.friendships[friend]:
                if outside_friend not in visited:
                    connection = list(friendships)
                    connection.append(outside_friend)
                    visited[outside_friend] = connection
                    stack.push(connection)

        return visited


if __name__ == '__main__':
    sg = SocialGraph()
    sg.populate_graph(10, 2)
    #print(sg.users)
    print(sg.friendships)    
    connections = sg.get_all_social_paths(1)
    print(f"connections: {connections}")

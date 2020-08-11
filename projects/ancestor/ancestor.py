
class Queue():
    def __init__(self):
        self.queue = []

    def enqueue(self, value):
        self.queue.append(value)
    
    def dequeue(self, value):
        if self.size() >0:
            return self.queue.pop(0)
        else:
            return None

    def size(self):
        return len(self.queue)
    
    def empty(self):
        return self.size() <= 0

def earliest_ancestor(ancestors, starting_node):
    #init graph
    graph = {}    

    #make graph O(n) over ancestors
    for relationship in ancestors:
        parent = relationship[0]
        child = relationship[1]
        if child not in graph:
            graph[child] = list()
            graph[child].append(parent)
        else:
            graph[child].append(parent)
    
    #init ancestor
    ancestor = -1

    #reverse DFS search (need stack?)
    if starting_node in graph:        
        curr = graph[starting_node]
        while curr:
            if curr[0] in graph:
                #curr's first parent is a child of another node, check its parents
                curr = graph[curr[0]]
            else:
                #curr's first parent is ancestor
                if curr[0] != None:
                    ancestor = curr[0]
                    curr = None
    return ancestor

test_ancestors = [(1, 3), (2, 3), (3, 6), (5, 6), (5, 7), (4, 5), (4, 8), (8, 9), (11, 8), (10, 1)]
print(earliest_ancestor(test_ancestors, 1)) # == 4
#completed tests:
# self.assertEqual(earliest_ancestor(test_ancestors, 1), 10)
# self.assertEqual(earliest_ancestor(test_ancestors, 2), -1)
# self.assertEqual(earliest_ancestor(test_ancestors, 3), 10)
# self.assertEqual(earliest_ancestor(test_ancestors, 4), -1)
# self.assertEqual(earliest_ancestor(test_ancestors, 5), 4)
# self.assertEqual(earliest_ancestor(test_ancestors, 6), 10)
# self.assertEqual(earliest_ancestor(test_ancestors, 7), 4)
# self.assertEqual(earliest_ancestor(test_ancestors, 8), 4)
# self.assertEqual(earliest_ancestor(test_ancestors, 9), 4)
# self.assertEqual(earliest_ancestor(test_ancestors, 10), -1)
# self.assertEqual(earliest_ancestor(test_ancestors, 11), -1)
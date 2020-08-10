"""
Simple graph implementation
"""
from util import Stack, Queue  # These may come in handy

class Graph:
    def __init__(self):
        self.vertices = {}        
    
    def add_vertex(self, vertex_id):
        self.vertices[vertex_id] = set()

    def add_edge(self, v1, v2):
        if v1 in self.vertices and v2 in self.vertices:            
            self.vertices[v1].add(v2)
        else:
            raise IndexError("That vertex hasn't been added")

    def get_neighbors(self, vertex_id):
        return self.vertices[vertex_id]

    def remove_edge(self, v1, v2):
        if v1 in self.vertices and v2 in self.vertices and v2 in self.vertices[v1]: 
            self.vertices[v1].remove(v2)
        else:
            raise IndexError("Those vertices aren't neighbors")

    def bft(self, start):
        #init Q(v1)
        q = Queue()
        q.enqueue(start)
        #set for visited
        visited = set()

        # while Q not empty
        while q.size() > 0:
            # DQ, add to visited, add neighbors that aren't visited, loop
            v = q.dequeue()

            if v not in visited:
                visited.add(v)
                print(v)
                for neighbor in self.get_neighbors(v):
                    q.enqueue(neighbor)

    def dft(self, start):
        #init Stack(v1)
        s = Stack()
        s.push(start)
        visited = set()
        # is Stack empty?
        while s.size() > 0:            
        # no - pop, add to visited, add neighbors that aren't visited, loop
            v = s.pop()
            if v not in visited:
                visited.add(v)
                print(v)
                for neighbor in self.get_neighbors(v):
                    s.push(neighbor)        

    def dft_recursive(self, vertex, visited = []):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.

        This should be done using recursion.
        """
        # append vertex to visited list
        visited.append(vertex)
        # print neighbors and add to visited list
        for neighbor in self.get_neighbors(vertex):
            if neighbor not in visited:
                print(neighbor)
                # recurse
                visited = self.dft_recursive(neighbor, visited)

        return visited


    def bfs(self, start):
        """ track path to target node """
        # init Q [start]
        # set of visited
        # while Q not empty:
        # enqueue list of path to neighbors ([start, v1], [start, v2])
        # add path to list of visited        
        # DQ
        pass

    def dfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing a path from
        starting_vertex to destination_vertex in
        depth-first order.
        """
        pass  # TODO

    def dfs_recursive(self, starting_vertex, destination_vertex):
        """
        Return a list containing a path from
        starting_vertex to destination_vertex in
        depth-first order.

        This should be done using recursion.
        """
        pass  # TODO

if __name__ == '__main__':
#####TODO:######
    graph = Graph()  # Instantiate your graph
    # https://github.com/LambdaSchool/Graphs/blob/master/objectives/breadth-first-search/img/bfs-visit-order.png
    graph.add_vertex(1)
    graph.add_vertex(2)
    graph.add_vertex(3)
    graph.add_vertex(4)
    graph.add_vertex(5)
    graph.add_vertex(6)
    graph.add_vertex(7)
    graph.add_edge(5, 3)
    graph.add_edge(6, 3)
    graph.add_edge(7, 1)
    graph.add_edge(4, 7)
    graph.add_edge(1, 2)
    graph.add_edge(7, 6)
    graph.add_edge(2, 4)
    graph.add_edge(3, 5)
    graph.add_edge(2, 3)
    graph.add_edge(4, 6)

    # '''
    # Should print:
    #     {1: {2}, 2: {3, 4}, 3: {5}, 4: {6, 7}, 5: {3}, 6: {3}, 7: {1, 6}}
    # '''
    # print(graph.vertices)

    # '''
    # Valid BFT paths:
    #     1, 2, 3, 4, 5, 6, 7
    #     1, 2, 3, 4, 5, 7, 6
    #     1, 2, 3, 4, 6, 7, 5
    #     1, 2, 3, 4, 6, 5, 7
    #     1, 2, 3, 4, 7, 6, 5
    #     1, 2, 3, 4, 7, 5, 6
    #     1, 2, 4, 3, 5, 6, 7
    #     1, 2, 4, 3, 5, 7, 6
    #     1, 2, 4, 3, 6, 7, 5
    #     1, 2, 4, 3, 6, 5, 7
    #     1, 2, 4, 3, 7, 6, 5
    #     1, 2, 4, 3, 7, 5, 6
    # '''
    # graph.bft(1)

    # '''
    # Valid DFT paths:
    #     1, 2, 3, 5, 4, 6, 7
    #     1, 2, 3, 5, 4, 7, 6
    #     1, 2, 4, 7, 6, 3, 5
    #     1, 2, 4, 6, 3, 5, 7
    # '''
    # graph.dft(1)
    graph.dft_recursive(1)

    # '''
    # Valid BFS path:
    #     [1, 2, 4, 6]
    # '''
    # print(graph.bfs(1, 6))

    # '''
    # Valid DFS paths:
    #     [1, 2, 4, 6]
    #     [1, 2, 4, 7, 6]
    # '''
    # print(graph.dfs(1, 6))
    # print(graph.dfs_recursive(1, 6))

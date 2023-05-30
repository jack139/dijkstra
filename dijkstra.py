from collections import deque

INFINITY = float("inf")


class Graph:
    def __init__(self, filename):
        """Reads graph definition and stores it. Each line of the graph
        definition file defines an edge by specifying the start node,
        end node, and distance, delimited by spaces.

        Stores the graph definition in two properties which are used by
        Dijkstra's algorithm in the shortest_path method:
        self.nodes = set of all unique nodes in the graph
        self.adjacency_list = dict that maps each node to an unordered set of
        (neighbor, distance) tuples.
        """

        # Read the graph definition file and store in graph_edges as a list of
        # lists of [from_node, to_node, distance]. This data structure is not
        # used by Dijkstra's algorithm, it's just an intermediate step in the
        # create of self.nodes and self.adjacency_list.
        graph_edges = []
        with open(filename) as fhandle:
            for line in fhandle:
                edge_from, edge_to, cost, c1 = line.strip().split()
                graph_edges.append((edge_from, edge_to, float(cost), c1))

        self.nodes = set()
        self.comments = {}
        for edge in graph_edges:
            self.nodes.update([edge[0], edge[1]])
            self.comments[(edge[0], edge[1])] = edge[3]

        self.adjacency_list = {node: set() for node in self.nodes}
        for edge in graph_edges:
            self.adjacency_list[edge[0]].add((edge[1], edge[2]))

        #print(self.adjacency_list)

    def shortest_path(self, start_node, end_node):
        """Uses Dijkstra's algorithm to determine the shortest path from
        start_node to end_node. Returns (path, distance).
        """

        unvisited_nodes = self.nodes.copy()  # All nodes are initially unvisited.

        # Create a dictionary of each node's distance from start_node. We will
        # update each node's distance whenever we find a shorter path.
        distance_from_start = {
            node: (0 if node == start_node else INFINITY) for node in self.nodes
        }

        # Initialize previous_node, the dictionary that maps each node to the
        # node it was visited from when the the shortest path to it was found.
        previous_node = {node: None for node in self.nodes}

        while unvisited_nodes:
            # Set current_node to the unvisited node with shortest distance
            # calculated so far.
            current_node = min(
                unvisited_nodes, key=lambda node: distance_from_start[node]
            )
            unvisited_nodes.remove(current_node)

            # If current_node's distance is INFINITY, the remaining unvisited
            # nodes are not connected to start_node, so we're done.
            if distance_from_start[current_node] == INFINITY:
                break

            # For each neighbor of current_node, check whether the total distance
            # to the neighbor via current_node is shorter than the distance we
            # currently have for that node. If it is, update the neighbor's values
            # for distance_from_start and previous_node.
            for neighbor, distance in self.adjacency_list[current_node]:
                new_path = distance_from_start[current_node] + distance
                if new_path < distance_from_start[neighbor]:
                    distance_from_start[neighbor] = new_path
                    previous_node[neighbor] = current_node

            if current_node == end_node:
                break # we've visited the destination node, so we're done

        # To build the path to be returned, we iterate through the nodes from
        # end_node back to start_node. Note the use of a deque, which can
        # appendleft with O(1) performance.
        path = deque()
        current_node = end_node
        while previous_node[current_node] is not None:
            path.appendleft(current_node)
            current_node = previous_node[current_node]
        path.appendleft(start_node)

        path_comment = []
        last_node = None
        for n, node in enumerate(list(path)):
            if n>0:
                path_comment.append(self.comments.get((last_node, node)))
            last_node = node

        return path, distance_from_start[end_node], path_comment



def verify_algorithm(filename, start, end, path, distance):
    graph = Graph(filename)
    returned_path, returned_distance, path_comment = graph.shortest_path(start, end)

    #assert list(returned_path) == path
    #assert returned_distance == distance

    print(f'graph definition file: {filename}')
    print(f'      start/end nodes: {start} -> {end}')
    print(f'        shortest path: {list(returned_path)}')
    print(f'       total distance: {returned_distance}')
    print(f'       total comments: {path_comment}')


if __name__ == "__main__":
    verify_algorithm(
        filename="test.txt",
        start="住院大厅",
        end="候诊大厅",
        path=[],
        distance=11,
    )

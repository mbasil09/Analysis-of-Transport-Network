import matplotlib.pyplot as plt
import numpy as np
import collections


class Graph:
    """
    Set number of edges manually
    Contains nodes and edges
    Nodes are taken as numbers
    """

    # dictionary to store graph
    def __init__(self):
        self.no_of_nodes = 0
        self.no_of_edges = 0
        self.adj_mat = [[0 for _ in range(self.no_of_nodes)] for __ in range(self.no_of_nodes)]
        self.edge_list = dict()
        self.node_set = set()
        self.diameter = 0
        self.avg_path_length = 0
        self.avg_clust_coeff = 0

    # function to add an edge to graph
    def add_edge(self, u, v, undirected=False, weight=1):
        """
        Assuming nodes are added incrementally, so if 0, 1, 2, 3, 4 are present, 5 can be added
        """
        self.edge_list[u].append(v)
        self.adj_mat[v][u] = weight
        if undirected:
            self.edge_list[v].append(u)
            self.adj_mat[u][v] = weight

        if u not in self.node_set:
            self.node_set.add(u)
            self.no_of_nodes += 1
            self.fix_adj_mat()
        if v not in self.node_set:
            self.node_set.add(v)
            self.no_of_nodes += 1
            self.fix_adj_mat()

    # adds rows and columns to accomodate new node
    def fix_adj_mat(self):
        l = len(self.adj_mat)
        for index_row in range(l):
            self.adj_mat[index_row] += [0]
        self.adj_mat.append([0 for i in range(l+1)])

    def make_using_edge_list(self, edge_list):
        # assuming it is unweighted
        self.edge_list = edge_list
        self.no_of_nodes = len(edge_list)
        for i in range(self.no_of_nodes):
            self.node_set.add(i)
        self.adj_mat = [[0 for _ in range(self.no_of_nodes)] for __ in range(self.no_of_nodes)]
        for key in edge_list.keys():
            for el in edge_list[key]:
                self.adj_mat[key][el] = 1

    def make_using_adj_mat(self, adj_mat):
        self.adj_mat = adj_mat
        self.no_of_nodes = len(adj_mat)
        for i in range(self.no_of_nodes):
            self.node_set.add(i)
        self.adj_mat = [[0 for _ in range(self.no_of_nodes)] for __ in range(self.no_of_nodes)]

    # to calculate minimum flights to get from source to destination
    # returns -1 if unreachable
    def bfs(self, src, dest):
        """Make sure the graph is unweighted"""
        queue = [[src]]
        visited = set()

        while queue:
            path = queue.pop(0)
            node = path[-1]

            if node == dest:
                return len(path) - 1
            elif node not in visited:
                for current_neighbour in self.edge_list[node]:
                    new_path = list(path)
                    new_path.append(current_neighbour)
                    queue.append(new_path)

                visited.add(node)
        return -1

    def avg_degree(self):
        return (2*self.no_of_edges)/self.no_of_nodes

    def calculate_prop(self):
        """Calculates avg path length, diameter, avg clustering coefficient"""

        # making graph undirected for bfs
        for e in self.edge_list.keys():
            for val in self.edge_list[e]:
                if val in self.edge_list.keys():
                    if e not in self.edge_list[val]:
                        self.edge_list[val].append(e)
                    else:
                        self.edge_list[val] = [e]

        # print("nodes=", self.no_of_nodes)
        for i in range(self.no_of_nodes):
            for j in range(self.no_of_nodes):
                if i != j:
                    len_ij = self.bfs(i, j)
                    if len_ij:
                        self.avg_path_length += len_ij
                        diameter = max(self.diameter, len_ij)
        self.avg_path_length /= (self.no_of_nodes*(self.no_of_nodes-1))
        # print("Average path length=", self.avg_path_length)
        # print("Diameter=", self.diameter)

        # compute avg clustering coeff
        for id_ in range(self.no_of_nodes):
            no_of_neighbours = 0
            links_btw_neighbours = 0
            neighbours = set()
            for i in range(self.no_of_nodes):
                if self.adj_mat[id_][i] != 0 or self.adj_mat[i][id_] != 0:
                    no_of_neighbours += 1
                    neighbours.add(i)
            neighbours = list(neighbours)
            for m in range(no_of_neighbours):
                for n in range(m+1, no_of_neighbours):
                    n1 = neighbours[m]
                    n2 = neighbours[n]
                    if self.adj_mat[n1][n2] != 0 or self.adj_mat[n1][n2] != 0:
                        links_btw_neighbours += 1
            if no_of_neighbours > 1:
                clust_coeff = (2 * links_btw_neighbours) / (no_of_neighbours * (no_of_neighbours - 1))
                # print("clust", id_, clust_coeff)
                self.avg_clust_coeff += clust_coeff
        self.avg_clust_coeff /= self.no_of_nodes

    # function to plot scaled degree distribution
    def plot_degree_distribution(self, in_out_separate=False):
        if in_out_separate:
            in_degree_distribution = {}
            out_degree_distribution = {}
            for node in range(self.no_of_nodes):
                edges_coming_in = 0
                edges_going_out = 0
                for f in range(self.no_of_nodes):
                    if self.adj_mat[f][node] != 0:
                        edges_going_out += 1
                    if self.adj_mat[node][f] != 0:
                        edges_coming_in += 1
                if edges_coming_in not in in_degree_distribution.keys():
                    in_degree_distribution[edges_coming_in] = 1
                else:
                    in_degree_distribution[edges_coming_in] += 1

                if edges_going_out not in out_degree_distribution:
                    out_degree_distribution[edges_going_out] = 1
                else:
                    out_degree_distribution[edges_going_out] += 1

            for key in in_degree_distribution.keys():
                in_degree_distribution[key] /= self.no_of_nodes
            for key in out_degree_distribution.keys():
                out_degree_distribution[key] /= self.no_of_nodes

            od_in = collections.OrderedDict(sorted(in_degree_distribution.items()))
            od_out = collections.OrderedDict(sorted(out_degree_distribution.items()))

            # print("In degree distribution (k-pk values)", od_in, sep="\n")
            # print("Out degree distribution (k-pk values)", od_out, sep="\n")

            y_pos = np.arange(len(od_in.keys()))
            plt.figure(figsize=(15, 5))
            plt.bar(y_pos, od_in.values())
            plt.xticks(y_pos, od_in.keys())
            plt.xlabel("k")
            plt.ylabel("pk")
            plt.title("Scaled Degree Distribution for In Degree")
            plt.show()

            y_pos = np.arange(len(od_out.keys()))
            plt.figure(figsize=(15, 5))
            plt.bar(y_pos, od_out.values())
            plt.xticks(y_pos, od_out.keys())
            plt.xlabel("k")
            plt.ylabel("pk")
            plt.title("Scaled Degree Distribution for Out Degree")
            plt.show()

        else:
            degree_map_no_of_nodes_with_degree_k = {}
            for node in range(self.no_of_nodes):
                edges_coming_in = 0
                edges_going_out = 0
                for e in self.adj_mat[node]:
                    if e != 0:
                        edges_coming_in += 1
                for row in range(self.no_of_nodes):
                    if self.adj_mat[row][node] != 0:
                        edges_going_out += 1
                degree_of_node = edges_coming_in + edges_going_out
                if degree_of_node not in degree_map_no_of_nodes_with_degree_k:
                    degree_map_no_of_nodes_with_degree_k[degree_of_node] = 1
                else:
                    degree_map_no_of_nodes_with_degree_k[degree_of_node] += 1

            for key in degree_map_no_of_nodes_with_degree_k.keys():
                degree_map_no_of_nodes_with_degree_k[key] /= self.no_of_nodes
            """now we have {k:pk} mapping"""

            od = collections.OrderedDict(sorted(degree_map_no_of_nodes_with_degree_k.items()))

            y_pos = np.arange(len(od.keys()))
            plt.figure(figsize=(15, 5))
            plt.bar(y_pos, od.values())
            plt.xticks(y_pos, od.keys())
            plt.xlabel("k")
            plt.ylabel("pk")
            plt.title("Scaled Degree Distribution")
            plt.show()


g = Graph()
g.make_using_edge_list({0:[1], 1:[0, 2, 4], 2:[1, 3], 3:[2, 4, 5], 4:[1, 3], 5:[3]})
g.add_edge(2, 4)
print(g.bfs(0, 5))
g.add_edge(1, 3)
print(g.bfs(0, 5))
g.no_of_edges = 8
print(g.avg_degree())
g.calculate_prop()
print(g.avg_degree())
print(g.avg_path_length)
print(g.avg_clust_coeff)
g.plot_degree_distribution(True)

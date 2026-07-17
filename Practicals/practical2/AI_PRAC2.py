import heapq
import matplotlib.pyplot as plt
import networkx as nx


# 1. GRAPH DATA
# Road distances (km)
graph = {

    "MVLU College": {
        "Sahar Rd": 1.4,
        "GK Gokhale Bridge": 1.5
    },

    "Sahar Rd": {
        "Shahaji Raje Marg": 1.2
    },

    "Shahaji Raje Marg": {
        "Vaikunthlal Mehta Rd": 3.4
    },

    "GK Gokhale Bridge": {
        "Barfiwala Flyover": 0.5
    },

    "Barfiwala Flyover": {
        "Vaikunthlal Mehta Rd": 2.6
    },

    "Vaikunthlal Mehta Rd": {
        "Juhu Tara Rd": 1.4
    },

    "Juhu Tara Rd": {
        "Juhu Beach": 1.4
    },

    "Juhu Beach": {}
}

# Straight-line heuristic distances to Juhu Beach
heuristics = {

    "MVLU College": 7.8,
    "Sahar Rd": 6.4,
    "Shahaji Raje Marg": 5.0,
    "GK Gokhale Bridge": 5.6,
    "Barfiwala Flyover": 3.8,
    "Vaikunthlal Mehta Rd": 1.5,
    "Juhu Tara Rd": 0.5,
    "Juhu Beach": 0

}

# Coordinates for visualization
node_positions = {

    "MVLU College": (2,10),

    "Sahar Rd": (0,7),

    "GK Gokhale Bridge": (5,7),

    "Shahaji Raje Marg": (0,5),

    "Barfiwala Flyover": (5,5),

    "Vaikunthlal Mehta Rd": (2,3),

    "Juhu Tara Rd": (2,1),

    "Juhu Beach": (2,-1)

}

# 2. A* SEARCH
def a_star_search(graph, heuristics, start, goal):

    priority_queue = [(heuristics[start], start, [start], 0)]

    visited = set()

    while priority_queue:

        f_score, current, path, g_score = heapq.heappop(priority_queue)

        if current in visited:
            continue

        visited.add(current)

        if current == goal:
            return path, g_score

        for neighbor, cost in graph[current].items():

            if neighbor not in visited:

                new_g = g_score + cost
                new_f = new_g + heuristics[neighbor]

                heapq.heappush(
                    priority_queue,
                    (new_f, neighbor, path + [neighbor], new_g)
                )

    return None, float("inf")


# 3. RUN PROGRAM
start = "MVLU College"
goal = "Juhu Beach"

optimal_path, total_distance = a_star_search(
    graph,
    heuristics,
    start,
    goal
)

print("Optimal Path:")
print(" -> ".join(optimal_path))

print("\nTotal Distance:", total_distance, "km")


# 4. VISUALIZATION 
G = nx.DiGraph()

for node, neighbors in graph.items():
    for neighbor, weight in neighbors.items():
        G.add_edge(node, neighbor, weight=weight)


plt.figure(figsize=(12,10))


# Highlight path edges
path_edges = list(zip(optimal_path, optimal_path[1:]))

normal_edges = [
    edge for edge in G.edges()
    if edge not in path_edges
]


# Draw EDGES FIRST (so lines are visible)
nx.draw_networkx_edges(
    G,
    node_positions,
    edgelist=normal_edges,
    edge_color="gray",
    width=2,
    arrows=True,
    arrowsize=20
)


nx.draw_networkx_edges(
    G,
    node_positions,
    edgelist=path_edges,
    edge_color="orange",
    width=4,
    arrows=True,
    arrowsize=25
)


# Draw NODES AFTER EDGES
nx.draw_networkx_nodes(
    G,
    node_positions,
    node_size=1600,
    node_color="skyblue"
)

# Node labels with heuristic values
labels = {
    node: f"{node}\nh(n)={heuristics[node]}"
    for node in G.nodes()
}


nx.draw_networkx_labels(
    G,
    node_positions,
    labels,
    font_size=8,
    font_weight="bold"
)


# Edge distance labels
edge_labels = nx.get_edge_attributes(G, "weight")

edge_labels = {
    k: f"{v} km"
    for k, v in edge_labels.items()
}


nx.draw_networkx_edge_labels(
    G,
    node_positions,
    edge_labels=edge_labels,
    font_color="red",
    font_size=8
)


plt.title(
    "A* Search: MVLU College to Juhu Beach\nOrange Line = Optimal Path",
    fontsize=15
)

plt.axis("off")

plt.tight_layout()

plt.show()

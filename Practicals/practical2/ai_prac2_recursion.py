import matplotlib.pyplot as plt
import networkx as nx


# ------------------------------------------------------------
# 1. GRAPH DATA
# ------------------------------------------------------------

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


# ------------------------------------------------------------
# 2. HEURISTIC VALUES h(n)
# ------------------------------------------------------------

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


# ------------------------------------------------------------
# 3. RBFS ALGORITHM
# ------------------------------------------------------------

# ------------------------------------------------------------
# 3. RBFS ALGORITHM (FIXED)
# ------------------------------------------------------------

def rbfs(node, goal, g, f_limit, path):

    if node == goal:
        return True, path, g, g


    successors = []


    for neighbour, distance in graph[node].items():

        if neighbour not in path:

            new_g = g + distance

            # f(n)=g(n)+h(n)
            new_f = new_g + heuristics[neighbour]

            successors.append(
                [new_f, neighbour, new_g]
            )


    if not successors:
        return False, [], 0, float("inf")


    while True:

        # Lowest f(n) first
        successors.sort(key=lambda x:x[0])


        best = successors[0]


        # If current option is worse than limit
        if best[0] > f_limit:
            return False, [], 0, best[0]


        alternative = (
            successors[1][0]
            if len(successors) > 1
            else float("inf")
        )


        success, result_path, cost, new_f = rbfs(
            best[1],
            goal,
            best[2],
            min(f_limit, alternative),
            path + [best[1]]
        )


        best[0] = new_f


        if success:
            return True, result_path, cost, new_f



def rbfs_search(start, goal):

    success, path, cost, _ = rbfs(
        start,
        goal,
        0,
        float("inf"),
        [start]
    )

    return path, cost


# ------------------------------------------------------------
# 4. RUN RBFS
# ------------------------------------------------------------

start = "MVLU College"
goal = "Juhu Beach"


optimal_path, total_distance = rbfs_search(
    start,
    goal
)

print(optimal_path)


print("Optimal RBFS Path:")
print(" -> ".join(optimal_path))

print("\nTotal Distance:", total_distance, "km")



# ------------------------------------------------------------
# 5. VISUALIZATION
# ------------------------------------------------------------

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



G = nx.DiGraph()


for node, neighbors in graph.items():

    for neighbor, weight in neighbors.items():

        G.add_edge(
            node,
            neighbor,
            weight=weight
        )


plt.figure(figsize=(12,10))


path_edges = list(zip(
    optimal_path,
    optimal_path[1:]
))


normal_edges = [
    edge for edge in G.edges()
    if edge not in path_edges
]


# Draw normal roads

nx.draw_networkx_edges(
    G,
    node_positions,
    edgelist=normal_edges,
    edge_color="gray",
    width=2,
    arrows=True
)


# Draw RBFS selected path

nx.draw_networkx_edges(
    G,
    node_positions,
    edgelist=path_edges,
    edge_color="green",
    width=4,
    arrows=True
)


# Draw nodes

nx.draw_networkx_nodes(
    G,
    node_positions,
    node_size=1600,
    node_color="skyblue"
)


labels = {
    node:f"{node}\nh(n)={heuristics[node]}"
    for node in G.nodes()
}


nx.draw_networkx_labels(
    G,
    node_positions,
    labels,
    font_size=8,
    font_weight="bold"
)


edge_labels = nx.get_edge_attributes(
    G,
    "weight"
)


edge_labels = {
    k:f"{v} km"
    for k,v in edge_labels.items()
}


nx.draw_networkx_edge_labels(
    G,
    node_positions,
    edge_labels=edge_labels,
    font_color="red"
)


plt.title(
    "RBFS Search: MVLU College to Juhu Beach\nGreen Line = Optimal Path",
    fontsize=15
)


plt.axis("off")

plt.tight_layout()

plt.show()

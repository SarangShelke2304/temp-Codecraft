from app.engine.parser import parse_dsl_file
from collections import deque


# def compute_in_degrees(workflow: Workflow):
#     """
#     Computes the in-degree (number of dependencies) for each node in the workflow.
#
#     param workflow: Parsed workflow object containing nodes and connections.
#     :return: A dictionary where keys are node IDs and values are their in-degree count.
#     """
#     in_degree = {node_id: 0 for node_id in workflow.nodes}  # Initialize in-degrees to 0
#
#     # Iterate through connections and update in-degree count
#     for connection in workflow.connections:
#         in_degree[connection.to_node] += 1
#     return in_degree
#
# def create_adjacency_list(workflow: Workflow):
#     """
#     Creates an adjacency list from the workflow connections.
#
#     param workflow: Parsed workflow object containing nodes and connections.
#     :return: A dictionary representing the adjacency list.
#     """
#     adj_list = defaultdict(list)
#     # print(adj_list)
#     for connection in workflow.connections:
#         adj_list[connection.from_node].append(connection.to_node)
#     # print(adj_list)
#     return adj_list




async def execute_dag(_nodes, _connections):

    # Creates an adjacency list from the workflow connections.
    adj_list = {node: [] for node in _nodes}

    # Computes the in-degree (number of dependencies) for each node in the workflow.
    in_degree = {node: 0 for node in _nodes}

    for conn in _connections:
        adj_list[conn.from_node].append(conn.to_node)
        in_degree[conn.to_node] += 1

    queue = deque([node for node in _nodes if in_degree[node] == 0])

    execution_order = []

    while queue:
        node = queue.popleft()
        execution_order.append(node)

        # Simulate execution (replace with actual node execution)

        print(f"Executing {node}")


        # Reduce in-degree of dependent nodes
        for neighbor in adj_list[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    return execution_order

async def parse_and_get_order(__json__):
    # adjacency_list = create_adjacency_list(Workflow)

    # Print adjacency list
    # for Node, dependencies in adjacency_list.items():
    #     print(f"{Node} -> {dependencies}")


    workflow = parse_dsl_file(__json__)
    connections = workflow.connections
    # for connection in connections:
    #     print(connection)
    nodes = workflow.nodes
    # for node in nodes:
    #     print(node)
    order = await execute_dag(nodes, connections)
    return order

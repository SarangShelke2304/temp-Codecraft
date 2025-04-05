from collections import deque

async def dag(_nodes, _connections):

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

        # Reduce in-degree of dependent nodes
        for neighbor in adj_list[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    # temp = []
    # for node_name, node in _nodes.items():
    #     temp.append({node_name: node})
    return execution_order
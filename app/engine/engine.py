from typing import DefaultDict, Any
from app.engine.parser import parse_dsl_file
from collections import deque
from app.engine.tools_executor import execute_file_input, execute_llm, execute_chat_input
from app.engine.parser import Node, Connection

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

output_storage:DefaultDict[Any, Any]={}


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
    temp = []
    # temp1 = []
    for node_name, node in _nodes.items():
        temp.append({node_name: node})
        # temp1.append({node_name: node})
    # print(temp)
    # print('\n', temp1)
    #     # print(f"Node name: {node_name}, type: {node.type}")
    #



    # for _node in execution_order:
    #     for node_name, node in temp:
    #         if node_name == node:
    #             if node.type=='File':
    #                 file_text=execute_file_input(node.config.path)
    #             if node.type=='TextInput':
    #                 text_input=execute_chat_input(text=node.config.input)
    #             if node.type=='ModelNode':
    #                 llm_response=execute_llm(node.config.modelName, node.config.input, api_key=node.config.API_key)



    return execution_order

async def parse_and_get_order(__json__):
    # adjacency_list = create_adjacency_list(Workflow)

    # Print adjacency list
    # for Node, dependencies in adjacency_list.items():
    #     print(f"{Node} -> {dependencies}")


    workflow = parse_dsl_file(__json__)
    connections = workflow.connections
    for connection in connections:
        print(connection)
    nodes = workflow.nodes
    # for node_name, node in nodes.items():
    #     print(f"Node name: {node_name}, type: {node.type}")
    order = await execute_dag(nodes, connections)
    result = await execute_order(order, nodes, connections)
    return result

#execute order and also check node connections such that outputs of the previous nodes are given as input to the next node
async def execute_order(order, nodes, connections):
    for node in order:
        if nodes[node].type == 'File':
            for connection in connections:
                if connection.from_node is None:
                    if connection.from_node == node:
                        nodes[connection.to_node].config.input = output_storage[connection.from_node]
            file_text = execute_file_input(nodes[node].config.fileText)
            output_storage[nodes[node].type] = file_text
            # print(output_storage)
            continue
            # print(output_storage)
        if nodes[node].type == 'Text Input':
            for connection in connections:
                if connection.from_node is None:
                    if connection.from_node == node:
                        nodes[connection.to_node].config.input = output_storage[connection.from_node]
            text_input = execute_chat_input(text=nodes[node].config.Text)
            output_storage[nodes[node].type] = text_input
            print(output_storage)
        if nodes[node].type == 'Gemini':
            for connection in connections:
                if connection.from_node is None:
                    if connection.from_node == node:
                        nodes[connection.to_node].config.input = output_storage[connection.from_node]
            llm_response = execute_llm(nodes[node].config.modelName, file_input=output_storage['File'], chat_input=output_storage['Text Input'],api_key=nodes[node].config.API_key)
            return llm_response
            # output_storage[nodes[node].type] = llm_response
            # print(output_storage)











# from typing import DefaultDict, Any
# from app.engine.parser import parse_dsl_file
# from collections import deque
# from app.engine.tools_executor import execute_file_input, execute_llm, execute_chat_input
# from app.engine.parser import Node, Connection
#
# # def compute_in_degrees(workflow: Workflow):
# #     """
# #     Computes the in-degree (number of dependencies) for each node in the workflow.
# #
# #     param workflow: Parsed workflow object containing nodes and connections.
# #     :return: A dictionary where keys are node IDs and values are their in-degree count.
# #     """
# #     in_degree = {node_id: 0 for node_id in workflow.nodes}  # Initialize in-degrees to 0
# #
# #     # Iterate through connections and update in-degree count
# #     for connection in workflow.connections:
# #         in_degree[connection.to_node] += 1
# #     return in_degree
# #
# # def create_adjacency_list(workflow: Workflow):
# #     """
# #     Creates an adjacency list from the workflow connections.
# #
# #     param workflow: Parsed workflow object containing nodes and connections.
# #     :return: A dictionary representing the adjacency list.
# #     """
# #     adj_list = defaultdict(list)
# #     # print(adj_list)
# #     for connection in workflow.connections:
# #         adj_list[connection.from_node].append(connection.to_node)
# #     # print(adj_list)
# #     return adj_list
#
# output_storage:DefaultDict[Any, Any]={}
#
#
# async def execute_dag(_nodes, _connections):
#
#     # Creates an adjacency list from the workflow connections.
#     adj_list = {node: [] for node in _nodes}
#
#     # Computes the in-degree (number of dependencies) for each node in the workflow.
#     in_degree = {node: 0 for node in _nodes}
#
#     for conn in _connections:
#         adj_list[conn.from_node].append(conn.to_node)
#         in_degree[conn.to_node] += 1
#
#     queue = deque([node for node in _nodes if in_degree[node] == 0])
#
#     execution_order = []
#
#     while queue:
#         node = queue.popleft()
#         execution_order.append(node)
#
#         # Simulate execution (replace with actual node execution)
#
#         print(f"Executing {node}")
#
#
#         # Reduce in-degree of dependent nodes
#         for neighbor in adj_list[node]:
#             in_degree[neighbor] -= 1
#             if in_degree[neighbor] == 0:
#                 queue.append(neighbor)
#     temp = []
#     # temp1 = []
#     for node_name, node in _nodes.items():
#         temp.append({node_name: node})
#         # temp1.append({node_name: node})
#     print(temp)
#     # print('\n', temp1)
#     #     # print(f"Node name: {node_name}, type: {node.type}")
#     #
#
#
#
#     # for _node in execution_order:
#     #     for node_name, node in temp:
#     #         if node_name == node:
#     #             if node.type=='File':
#     #                 file_text=execute_file_input(node.config.path)
#     #             if node.type=='TextInput':
#     #                 text_input=execute_chat_input(text=node.config.input)
#     #             if node.type=='ModelNode':
#     #                 llm_response=execute_llm(node.config.modelName, node.config.input, api_key=node.config.API_key)
#
#
#
#     return execution_order
#
# async def parse_and_get_order(__json__):
#     # adjacency_list = create_adjacency_list(Workflow)
#
#     # Print adjacency list
#     # for Node, dependencies in adjacency_list.items():
#     #     print(f"{Node} -> {dependencies}")
#
#
#     workflow = parse_dsl_file(__json__)
#     connections = workflow.connections
#     for connection in connections:
#         print(connection)
#     nodes = workflow.nodes
#     # for node_name, node in nodes.items():
#     #     print(f"Node name: {node_name}, type: {node.type}")
#     order = await execute_dag(nodes, connections)
#     await execute_order(order, nodes, connections)
#     return output_storage
#
# #execute order and also check node connections such that outputs of the previous nodes are given as input to the next node
# async def execute_order(order, nodes, connections):
#     for node in order:
#         if nodes[node].type == 'File':
#             for connection in connections:
#                 if connection.from_node is None:
#                     if connection.from_node == node:
#                         nodes[connection.to_node].config.input = output_storage[connection.from_node]
#             file_text = execute_file_input(nodes[node].config.fileText)
#             output_storage[node] = file_text
#             continue
#             # print(output_storage)
#         if nodes[node].type == 'TextInput':
#             for connection in connections:
#                 if connection.from_node is None:
#                     if connection.from_node == node:
#                         nodes[connection.to_node].config.input = output_storage[connection.from_node]
#             text_input = execute_chat_input(text=nodes[node].config.Text)
#             output_storage[node] = text_input
#             print(output_storage)
#         if nodes[node].type == 'ModelNode':
#             for connection in connections:
#                 if connection.from_node is None:
#                     if connection.from_node == node:
#                         nodes[connection.to_node].config.input = output_storage[connection.from_node]
#             llm_response = execute_llm(nodes[node].config.modelName, nodes[node].config.input, api_key=nodes[node].config.API_key)
#             output_storage[node] = llm_response








# import asyncio
#
# async def main():
#     order = await parse_and_get_order(r"D:\temp-Codecraft\DSL3.json")  # Await the coroutine
#     # print(order)
#
# asyncio.run(main())

#
# from typing import DefaultDict, Any, List, Tuple
# from collections import deque
# from app.engine.parser import parse_dsl_file
# from app.engine.tools_executor import execute_file_input, execute_llm, execute_chat_input
#
#
# # Doubly Linked List Node representation for each workflow node
# class DLLNode:
#     def __init__(self, node_id: str, node_type: str, config: Any):
#         self.id = node_id  # Node ID
#         self.type = node_type  # Node type: 'File', 'TextInput', 'ModelNode'
#         self.config = config  # Configuration (for storing inputs/outputs and execution settings)
#         self.prev = []  # Previous nodes (dependencies)
#         self.next = []  # Next nodes (dependents)
#         self.result = None  # Store the node's output/result
#
#
# # Build Doubly Linked List from Nodes and Connections
# def build_doubly_linked_list(nodes, connections) -> Tuple[List[DLLNode], dict]:
#     # Create a DLLNode object for each node
#     node_map = {node_id: DLLNode(node_id, node.type, node.config) for node_id, node in nodes.items()}
#
#     # Link nodes via connections
#     for connection in connections:
#         from_node = node_map[connection.from_node]
#         to_node = node_map[connection.to_node]
#         from_node.next.append(to_node)
#         to_node.prev.append(from_node)
#
#     # Identify the head nodes (nodes with no incoming dependencies)
#     head_nodes = [node for node in node_map.values() if not node.prev]
#
#     return head_nodes, node_map
#
#
# # Execute the Doubly Linked List (Workflow DAG Execution)
# async def execute_doubly_linked_list(head_nodes: List[DLLNode]):
#     execution_order = []  # Keep track of the execution order for debugging/logging
#
#     queue = deque(head_nodes)  # Start traversal with head nodes (nodes with no dependencies)
#
#     while queue:
#         current_node = queue.popleft()
#         execution_order.append(current_node.id)
#
#         # Simulate execution (print to track)
#         print(f"Executing {current_node.id}")
#
#         # Execute node based on its type
#         if current_node.type == 'File':
#             current_node.result = execute_file_input(current_node.config.path)
#         elif current_node.type == 'TextInput':
#             current_node.result = execute_chat_input(text=current_node.config.Text)
#         elif current_node.type == 'ModelNode':
#             current_node.result = execute_llm(
#                 current_node.config.modelName,
#                 current_node.config.input,
#                 api_key=current_node.config.API_key
#             )
#
#         # Pass this node's result to all next nodes
#         for next_node in current_node.next:
#             next_node.config.input = current_node.result  # Pass result as input to dependent nodes
#
#             # Remove the dependency link (simulate clearing "in-degree")
#             next_node.prev.remove(current_node)
#             if not next_node.prev:  # If no remaining dependencies, add to queue
#                 queue.append(next_node)
#
#     return execution_order
#
#
# # Parse a Workflow File and Build Linked List
# async def parse_and_get_order(__json__):
#     # Parse the DSL file into workflow data
#     workflow = parse_dsl_file(__json__)
#     nodes = workflow.nodes
#     connections = workflow.connections
#
#     # Build the doubly linked list structure
#     head_nodes, node_map = build_doubly_linked_list(nodes, connections)
#
#     # Execute the DAG using the doubly linked list structure
#     execution_order = await execute_doubly_linked_list(head_nodes)
#
#     return execution_order
#
#
# # Main Execution Function
# import asyncio
#
#
# async def main():
#     # Parse the DSL file and execute the workflow
#     order = await parse_and_get_order(r"D:\temp-Codecraft\DSL2.json")
#     print("Execution Order:", order)
#
#
# # Run the Main Function
# asyncio.run(main())

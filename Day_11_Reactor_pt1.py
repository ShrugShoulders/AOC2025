import collections
import sys

sys.setrecursionlimit(2000)

def parse_device_data(data_lines):
    graph = {}
    
    for line in data_lines:
        line = line.strip()
        if not line:
            continue
            
        try:
            device, outputs_str = line.split(':')
            device = device.strip()
            outputs = [o.strip() for o in outputs_str.split(' ') if o.strip()]
            
            graph[device] = outputs
        except ValueError:
            print(f"Warning: Skipping malformed line: '{line}'")
            
    return graph

def find_all_paths(graph, start_node, end_node):    
    memo = {}
    
    def dfs(current_node):
        """Recursive function to count paths from current_node to end_node."""
        
        # Check memoization cache
        if current_node in memo:
            return memo[current_node]
            
        # Base case: Reached the goal
        if current_node == end_node:
            return 1
            
        # Base case: Node has no outputs (no path forward)
        if current_node not in graph or not graph[current_node]:
            return 0
        
        total_paths = 0
        for neighbor in graph[current_node]:
            total_paths += dfs(neighbor)
            
        # Store result in memoization cache
        memo[current_node] = total_paths
        
        return total_paths

    return dfs(start_node)

def main():
    """
    Main
    """
    example_data = [
        "aaa: you hhh",
        "you: bbb ccc",
        "bbb: ddd eee",
        "ccc: ddd eee fff",
        "ddd: ggg",
        "eee: out",
        "fff: out",
        "ggg: out",
        "hhh: ccc fff iii",
        "iii: out"
    ]
    
    print("====Example Data Verification====")
    example_graph = parse_device_data(example_data)
    example_paths = find_all_paths(example_graph, 'you', 'out')
    print(f"Graph parsed: {example_graph}")
    print(f"Total paths from 'you' to 'out' in example: {example_paths} (Expected: 5)")
    print("-" * 35)

    try:
        with open('input.txt', 'r') as f:
            puzzle_data_lines = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print("\nERROR: 'input.txt' Not Found Bitch")
        return

    start_device = 'you'
    end_device = 'out'

    puzzle_graph = parse_device_data(puzzle_data_lines)
    
    if start_device not in puzzle_graph and start_device != end_device:
         if start_device not in puzzle_graph and start_device != end_device:
             print(f"Warning: Start device '{start_device}' not found as a source device in the input data.")
             
    if end_device not in puzzle_graph and end_device not in example_graph.values():
         is_out_a_target = any(end_device in outputs for outputs in puzzle_graph.values())
         if not is_out_a_target:
             print(f"Warning: End device '{end_device}' not found as a target device in the input data.")


    # Find the path count
    final_paths_count = find_all_paths(puzzle_graph, start_device, end_device)

    print(f"Total number of devices processed: {len(puzzle_graph)}")
    print(f"Final Path Count from '{start_device}' to '{end_device}': {final_paths_count}")

if __name__ == "__main__":
    main()

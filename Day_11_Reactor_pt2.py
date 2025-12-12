import collections
import sys

sys.setrecursionlimit(2000)

def parse_device_data(data_lines):
    """
    Parses the device output data into an adjacency list representation of a graph.
    
    The graph is a dictionary where keys are device names (nodes) and values are 
    lists of connected output device names (neighbors/edges).
    """
    graph = {}
    
    for line in data_lines:
        line = line.strip()
        if not line:
            continue
            
        try:
            device, outputs_str = line.split(':', 1)
            device = device.strip()
            outputs = [o.strip() for o in outputs_str.split(' ') if o.strip()]
            
            graph[device] = outputs
        except ValueError:
            print(f"Warning: Skipping malformed line: '{line}'")
            
    return graph

def find_all_paths(graph, start_node, end_node, exclude_nodes=None):
    """
    Finds the total number of paths from the start_node to the end_node
    using Depth-First Search (DFS) with memoization and node exclusion.
    """
    if exclude_nodes is None:
        exclude_nodes = set()

    memo = {}
    
    def dfs(current_node):
        """Recursive function to count paths from current_node to end_node."""
        
        # Check exclusion constraint
        if current_node in exclude_nodes:
            return 0
            
        # Check memoization cache
        if current_node in memo:
            return memo[current_node]
            
        # Base case: Reached the goal
        if current_node == end_node:
            return 1
            
        # Base case: Node has no outputs (no path forward)
        if current_node not in graph or not graph[current_node]:
            return 0
        
        # Recursive step: Sum paths from all neighbors
        total_paths = 0
        for neighbor in graph[current_node]:
            total_paths += dfs(neighbor)
            
        # Store result in memoization cache
        memo[current_node] = total_paths
        
        return total_paths

    return dfs(start_node)


def solve_constrained_paths(graph, start, end, mid1, mid2):
    """
    Calculates the total number of paths from 'start' to 'end' that visit both 
    'mid1' and 'mid2' in any order.
    
    This is calculated as (Case 1: mid1 then mid2) + (Case 2: mid2 then mid1).
    """
    
    # Segment 1: start -> mid1 (must not visit mid2)
    p1_1 = find_all_paths(graph, start, mid1, exclude_nodes={mid2})
    
    # Segment 2: mid1 -> mid2 (no exclusion needed between the two mandatory points)
    p1_2 = find_all_paths(graph, mid1, mid2)
    
    # Segment 3: mid2 -> end (must not visit mid1)
    p1_3 = find_all_paths(graph, mid2, end, exclude_nodes={mid1})
    
    total_case_1 = p1_1 * p1_2 * p1_3
    
    # Segment 1: start -> mid2 (must not visit mid1)
    p2_1 = find_all_paths(graph, start, mid2, exclude_nodes={mid1})
    
    # Segment 2: mid2 -> mid1 (no exclusion needed)
    p2_2 = find_all_paths(graph, mid2, mid1)
    
    # Segment 3: mid1 -> end (must not visit mid2)
    p2_3 = find_all_paths(graph, mid1, end, exclude_nodes={mid2})
    
    total_case_2 = p2_1 * p2_2 * p2_3
    
    return total_case_1 + total_case_2


def main():
    """
    Main
    """
    pt2_example_data = [
        "svr: aaa bbb",
        "aaa: fft",
        "fft: ccc",
        "bbb: tty",
        "tty: ccc",
        "ccc: ddd eee",
        "ddd: hub",
        "hub: fff",
        "eee: dac",
        "dac: fff",
        "fff: ggg hhh",
        "ggg: out",
        "hhh: out"
    ]
    
    START_DEVICE = 'svr'
    END_DEVICE = 'out'
    MID_1 = 'dac'
    MID_2 = 'fft'
    
    print("====Example Data Verification====")
    example_graph = parse_device_data(pt2_example_data)
    example_paths = solve_constrained_paths(example_graph, START_DEVICE, END_DEVICE, MID_1, MID_2)
    
    print(f"Graph parsed: {example_graph}")
    print(f"Total constrained paths in example: {example_paths} (Expected: 2)")
    print("-" * 35)
    
    try:
        with open('input.txt', 'r') as f:
            puzzle_data_lines = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print("\nERROR: 'input.txt' Not Found Bitch.")
        return

    puzzle_graph = parse_device_data(puzzle_data_lines)
    final_paths_count = solve_constrained_paths(puzzle_graph, START_DEVICE, END_DEVICE, MID_1, MID_2)

    print("\n====Puzzle Solution====")
    print(f"Start: '{START_DEVICE}', End: '{END_DEVICE}'")
    print(f"Required Intermediates: '{MID_1}' and '{MID_2}'")
    print(f"Total Constrained Paths Found: {final_paths_count}")
    print("-" * 40)

if __name__ == "__main__":
    main()

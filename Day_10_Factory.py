import numpy as np
import re
from pulp import LpProblem, LpVariable, LpMinimize, lpSum, PULP_CBC_CMD, LpStatus, value 

def parse_machine_data(line: str):
    # Use regex BAYBAY
    match = re.search(r'^(.*)\{(.*)\}$', line.strip())
    if not match:
        raise ValueError("Input line does not match the expected format: '[...]' (...) {...}")
    
    schematics_str = match.group(1).strip()
    requirements_str = match.group(2).strip()
    
    # Extract joltage requirements
    try:
        b = np.array([int(val) for val in requirements_str.split(',') if val.strip()])
    except ValueError:
        raise ValueError("Could not parse joltage requirements (b vector). Ensure they are comma-separated integers.")
        
    num_counters = len(b)
    
    # Extract and process buttons
    button_schematic_matches = re.findall(r'\((.*?)\)', schematics_str)
    num_buttons = len(button_schematic_matches)
    
    if num_buttons == 0 and num_counters > 0:
        return np.array([[]]), b 

    A = np.zeros((num_counters, num_buttons), dtype=int)
    
    for j, counter_indices_str in enumerate(button_schematic_matches):
        if counter_indices_str.strip():
            try:
                indices = [int(i) for i in counter_indices_str.split(',')]
                for i in indices:
                    if 0 <= i < num_counters:
                        A[i, j] = 1
                    else:
                        print(f"Warning: Counter index {i} out of range (max index is {num_counters - 1}) for machine starting with '{line}...'. Ignoring.")
            except ValueError:
                raise ValueError(f"Could not parse button schematic for button {j} ({counter_indices_str}). Ensure indices are comma-separated integers.")
                
    return A, b

def solve_machine(A, b):
    num_counters = A.shape[0]
    num_buttons = A.shape[1]

    # Check for trivial case (no buttons)
    if num_buttons == 0:
        if np.all(b == 0):
            return 0, np.array([], dtype=int)
        else:
            return float('inf'), np.array([], dtype=int) 
        
    # ILP
    prob = LpProblem("JoltageMinPresses", LpMinimize)
    x = [LpVariable(f"x_{j}", lowBound=0, cat='Integer') for j in range(num_buttons)]
    prob += lpSum(x), "Total_Button_Presses"
    for i in range(num_counters):
        constraint_terms = [A[i, j] * x[j] for j in range(num_buttons)]
        
        prob += lpSum(constraint_terms) == b[i], f"Joltage_Counter_{i}"

    prob.solve(PULP_CBC_CMD(msg=0))
    
    if LpStatus[prob.status] == "Optimal":
        min_total_presses = int(value(prob.objective))
        # Extract the press counts vector
        x_presses = np.array([int(value(x_j)) for x_j in x], dtype=int)
        return min_total_presses, x_presses
    else:
        # Problem is infeasible
        if LpStatus[prob.status] == "Infeasible":
             print(f"\n--- ERROR: Problem is Infeasible for this machine. No solution exists. ---")
        else:
             print(f"\n--- WARNING: ILP Solver failed to find an Optimal solution ({LpStatus[prob.status]}) ---")
             
        return float('inf'), np.array([], dtype=int)

def main():
    """
    Main
    """    
    try:
        with open('input.txt', 'r') as f:
            machine_data_lines = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print("Error: 'input.txt' not found. Please ensure the file is correctly provided.")
        machine_data_lines = [
            "[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}",
            "[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}",
            "[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}"
        ]
        
    total_min_presses = 0
    results = []
    
    for i, line in enumerate(machine_data_lines):
        if not line:
            continue
            
        try:
            A, b = parse_machine_data(line)
            min_presses, x_presses = solve_machine(A, b)
            
            if min_presses != float('inf'):
                total_min_presses += min_presses
                
            results.append({
                'Machine': i + 1,
                'Min Presses': min_presses,
                'Presses Vector': x_presses,
                'Line Preview': line[:40] + '...'
            })
            
            if i < 5 or i == len(machine_data_lines) - 1 or min_presses == float('inf'):
                #print(f"\n[Machine {i + 1}] (Line: {results[-1]['Line Preview']})")
                #print(f"  Counters (b): {b}")
                #print(f"  Matrix A shape: {A.shape}")
                if min_presses == float('inf'):
                    print("Status: IMPOSSIBLE (Target non-zero, no buttons)")
                else:
                    pass
                    #print(f"Minimum Total Presses: {min_presses}")
            
        except ValueError as e:
            print(f"\n[Error processing Machine {i + 1} (Line: {line[:40]}...)]: {e}")
        except Exception as e:
            print(f"\n[Unexpected Error processing Machine {i + 1} (Line: {line[:40]}...)]: {e}")

    successful_machines = [r for r in results if r['Min Presses'] != float('inf')]
    print(f"Total Machines Processed: {len(machine_data_lines)}")
    print(f"Successful Configurations: {len(successful_machines)}")
    print(f"\nTotal Fewest Button Presses Required: {total_min_presses}")

if __name__ == "__main__":
    main()

import numpy as np
import re
from itertools import product
from fractions import Fraction

def parse_input_joltage(line):
    joltage_match = re.search(r'\{(.*?)\}', line)
    if not joltage_match:
        raise ValueError("Missing joltage requirements in {...}")
    
    J_list = [int(j.strip()) for j in joltage_match.group(1).split(',')]
    J = np.array(J_list, dtype=np.int64)
    num_counters = len(J)

    button_schematics = re.findall(r'\((.*?)\)', line)
    num_buttons = len(button_schematics)

    # np.int64 to prevent overflow/type errors=
    A = np.zeros((num_counters, num_buttons), dtype=np.int64) 
    
    for j, schematic in enumerate(button_schematics):
        if schematic:
            try:
                # Indices
                counter_indices = [int(i.strip()) for i in schematic.split(',')]
            except ValueError:
                counter_indices = []
                
            for i in counter_indices:
                if 0 <= i < num_counters:
                    A[i, j] = 1
                
    return A, J, num_counters, num_buttons


def solve_min_presses_joltage(A, J, num_counters, num_buttons):
    if num_buttons == 0:
        return 0 if np.all(J == 0) else -1

    M = [[Fraction(A[i, j]) for j in range(num_buttons)] + [Fraction(J[i])]
         for i in range(num_counters)]
    
    # Gaussian Elimination
    pivot_row = 0
    pivot_cols = []
    
    for col in range(num_buttons):
        if pivot_row == num_counters: break
            
        r = pivot_row
        max_abs = 0
        for i in range(pivot_row, num_counters):
            if abs(M[i][col]) > max_abs: 
                max_abs = abs(M[i][col])
                r = i
        
        if max_abs == 0: continue 
            
        M[pivot_row], M[r] = M[r], M[pivot_row] 

        pivot_val = M[pivot_row][col]
        if pivot_val == 0: continue
            
        M[pivot_row] = [m / pivot_val for m in M[pivot_row]]
            
        for i in range(num_counters):
            if i != pivot_row:
                factor = M[i][col]
                M[i] = [M[i][j] - factor * M[pivot_row][j] for j in range(num_buttons + 1)]
        
        pivot_cols.append(col)
        pivot_row += 1

    for i in range(pivot_row, num_counters):
        if M[i][-1] != 0:
            return -1

    free_cols = [j for j in range(num_buttons) if j not in pivot_cols]
    num_free = len(free_cols)
    
    x_p = np.zeros(num_buttons, dtype=object)
    for i, p_col in enumerate(pivot_cols):
        x_p[p_col] = M[i][-1]
    
    V = np.zeros((num_buttons, num_free), dtype=object)
    
    for k, free_col in enumerate(free_cols):
        v_k = np.zeros(num_buttons, dtype=object)
        v_k[free_col] = Fraction(1) 
        
        for i, p_col in enumerate(pivot_cols):
            v_k[p_col] = -M[i][free_col]
            
        V[:, k] = v_k
        
    max_c_bound = 30 
    
    if num_free > 4:
        max_c_bound = 15
    if num_free > 5:
         return -1

    min_presses = np.inf
    found_solution = False
    
    c_ranges = [range(-max_c_bound, max_c_bound + 1) for _ in range(num_free)]

    for c_tuple in product(*c_ranges):
        c = np.array(c_tuple, dtype=object) 
        
        x = x_p + V @ c
        
        # Non-negativity check
        if np.any(x < 0):
            continue
            
        # Integrality check
        is_integer = np.array([val.denominator == 1 for val in x])
        
        if not np.all(is_integer):
            continue
            
        x_int = np.array([int(val) for val in x], dtype=np.int64)
        
        # Exact equation check
        A_times_x = A @ x_int
        
        if np.array_equal(A_times_x, J):
            presses = np.sum(x_int)
            min_presses = min(min_presses, presses)
            found_solution = True
            
    return int(min_presses) if found_solution else -1

def parse_input_lights_out(line):
    diagram_match = re.search(r'\[(.*?)\]', line)
    if not diagram_match:
        raise ValueError("Invalid input format: missing indicator diagram")
        
    diagram = diagram_match.group(1)
    num_lights = len(diagram)
    T = np.array([1 if c == '#' else 0 for c in diagram], dtype=np.int8)

    button_schematics = re.findall(r'\((.*?)\)', line)
    num_buttons = len(button_schematics)

    # Lights
    A = np.zeros((num_lights, num_buttons), dtype=np.int8)
    
    for j, schematic in enumerate(button_schematics):
        if schematic:
            try:
                # Indices
                light_indices = [int(i.strip()) for i in schematic.split(',')]
            except ValueError:
                light_indices = []
                
            for i in light_indices:
                if 0 <= i < num_lights:
                    A[i, j] = 1

    return A, T, num_lights, num_buttons


def solve_min_presses_lights_out(A, T, num_lights, num_buttons):
    if num_buttons == 0:
        return 0 if np.all(T == 0) else np.inf

    M = np.hstack((A, T.reshape(-1, 1)))
    pivot_row = 0
    pivot_cols = []

    for col in range(num_buttons):
        if pivot_row == num_lights: break
        r = pivot_row
        while r < num_lights and M[r, col] == 0: r += 1

        if r < num_lights:
            M[[pivot_row, r]] = M[[r, pivot_row]] # Trade out
            for i in range(num_lights):
                if i != pivot_row and M[i, col] == 1:
                    M[i, :] = (M[i, :] + M[pivot_row, :]) % 2 # EXTERMINATE
            pivot_cols.append(col)
            pivot_row += 1

    # Check for inconsistency
    for i in range(pivot_row, num_lights):
        if M[i, -1] == 1:
            return np.inf

    free_cols = [j for j in range(num_buttons) if j not in pivot_cols]
    num_free = len(free_cols)
    V = np.zeros((num_buttons, num_free), dtype=np.int8)
    x_p = np.zeros(num_buttons, dtype=np.int8)

    for k, free_col in enumerate(free_cols):
        V[free_col, k] = 1
        for i, p_col in enumerate(pivot_cols):
            V[p_col, k] = M[i, free_col]

    for i, p_col in enumerate(pivot_cols):
        x_p[p_col] = M[i, -1]

    min_presses = np.sum(x_p)

    for i in range(1, 1 << num_free):
        c = np.array([int(b) for b in format(i, f'0{num_free}b')], dtype=np.int8)
        x = (x_p + V @ c) % 2
        
        presses = np.sum(x)
        min_presses = min(min_presses, presses)

    return int(min_presses)

def process_factory_input(data_string):
    """
    Processes each machine line. Attempts Lights Out mode first. 
    If inconsistent, logs it and falls back to Joltage mode.
    """
    input_data_lines = data_string

    total_min_presses = 0
    
    # We only process the actual machine data lines
    machine_lines = [line for line in input_data_lines if line.startswith('[') and ('{' in line)]
    
    print("--- Processing Machines ---")
    for i, line in enumerate(machine_lines):
        machine_num = i + 1
        min_presses = -1

        # Attempt Lights Out Mode
        try:
            A_L, T, num_lights, num_buttons = parse_input_lights_out(line)
            presses_L = solve_min_presses_lights_out(A_L, T, num_lights, num_buttons)
            
            if presses_L != np.inf:
                min_presses = presses_L
            else:
                A_J, J, num_counters, num_buttons = parse_input_joltage(line)
                presses_J = solve_min_presses_joltage(A_J, J, num_counters, num_buttons)

                if presses_J != -1:
                    min_presses = presses_J
                    print(f"🔄 Machine {machine_num} (Fallback Joltage): {min_presses}")
                else:
                    # Both failed wop wop
                    print(f"❌ Machine {machine_num}: No solution in EITHER mode.")
        
        except Exception as e:
            print(f"❌ Error processing machine {machine_num}: {e}")
        
        if min_presses != -1:
            total_min_presses += min_presses

    return total_min_presses

try:
    with open('input.txt', 'r') as f:
        full_factory_input = [line.strip() for line in f if line.strip()]
except FileNotFoundError:
    print("Error: 'input.txt' not found.")
    full_factory_input = [
        "[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}",
        "[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}",
        "[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}"
    ]

final_result = process_factory_input(full_factory_input)
print(f"The total fewest button presses required for all machines is: **{final_result}**")

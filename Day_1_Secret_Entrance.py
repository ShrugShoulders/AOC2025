def count_zero_hits(start_pos, distance, direction, DIAL_SIZE=100):
    """
    Calculates the number of times the dial points exactly at 0 during a 
    rotation of a given distance, starting from start_pos.
    
    This handles multi-cycle rotations (e.g., R1000).
    Stupid fucking elves
    """
    if distance <= 0:
        return 0
        
    if direction == 'R':
        # For Right rotation (increasing numbers):
        # A hit on 0 occurs when (start_pos + distance_traveled) is a multiple of 100.
        # The number of hits is floor((start_pos + distance) / 100).
        return (start_pos + distance) // DIAL_SIZE
    
    elif direction == 'L':
        # For Left rotation (decreasing numbers):
        # A hit on 0 occurs when distance_traveled equals: P_old, P_old + 100, P_old + 200, etc.
        
        # Case 1: Starting exactly at 0. The first hit is only after a full 100 clicks.
        if start_pos == 0:
            return distance // DIAL_SIZE
        
        # Case 2: Starting > 0.
        if distance < start_pos:
            # Not enough distance to reach 0
            return 0
        else:
            # The first hit occurs when the distance traveled equals start_pos (1 hit)
            hits = 1
            
            # Check for additional hits from full 100-click cycles
            # The remaining distance to check after the first hit
            remaining_distance = distance - start_pos
            hits += remaining_distance // DIAL_SIZE
            
            return hits
            
    return 0


def decode_secret_password(rotations_input):
    """
    Calculates the new North Pole secret password (method 0x434C49434B lol), 
    which is the total number of times the dial points at 0 during *any* click.
    """
    DIAL_SIZE = 100
    
    # Starting position of the dial
    current_position = 50
    
    # Track the total number of times the dial hits 0 during ALL clicks.
    total_zero_hits = 0
    
    # Prepare the input for processing
    rotations = rotations_input.strip().split('\n')
    
    print(f"--- Decoy Safe Method 0x434C49434B Analysis ---")
    print(f"Starting Position: {current_position}")
    print("-" * 60)

    for i, rotation in enumerate(rotations):
        # Determine direction and distance
        direction = rotation[0]
        try:
            distance = int(rotation[1:])
        except ValueError:
            print(f"Skipping malformed rotation: {rotation}")
            continue
        
        old_position = current_position
        
        # Calculate how many times 0 is hit during this rotation
        new_hits = count_zero_hits(old_position, distance, direction, DIAL_SIZE)
        total_zero_hits += new_hits
        
        # Calculate the final position (required to start the next rotation)
        if direction == 'R':
            current_position = (current_position + distance) % DIAL_SIZE
        elif direction == 'L':
            # Python's modulo operator handles negative numbers correctly for wrap-around
            current_position = (current_position - distance) % DIAL_SIZE
        
        print(f"Step {i+1}: {rotation} (From {old_position}) -> New Position: {current_position} | Hits in this step: {new_hits} | Total Hits: {total_zero_hits}")

    print("-" * 60)
    print(f"Total times the dial landed on 0 (Password): {total_zero_hits}")
    return total_zero_hits

dial_input = """
L68
L30
R48
L5
R60
L55
L1
L99
R14
L82
"""

password = decode_secret_password(dial_input)
# Lets hope I didn't fuck this all up
print(f"\nThe actual password (the total number of times the dial landed on 0) is: {password}") 

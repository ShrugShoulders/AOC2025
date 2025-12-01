def decode_secret_password(rotations_input):
    """
    Calculates the North Pole secret password, which is the number of times 
    the safe dial lands on 0 after any rotation.
    
    The dial has numbers 0-99 (DIAL_SIZE = 100) and starts at 50.
    Rotations are circular (modulo 100).
    """
    DIAL_SIZE = 100
    
    # Starting position of the dial
    current_position = 50
    
    zero_count = 0
    
    # Prepare the input for processing
    rotations = rotations_input.strip().split('\n')
    
    print(f"--- Decoy Safe Zero Count Analysis ---")
    print(f"Starting Position: {current_position}")
    print("-" * 40)

    for i, rotation in enumerate(rotations):
        # Determine direction and distance
        direction = rotation[0]
        try:
            distance = int(rotation[1:])
        except ValueError:
            print(f"Skipping malformed rotation: {rotation}")
            continue
        
        old_position = current_position
        
        if direction == 'R':
            # Right rotation: Add distance, then use modulo 100
            current_position = (current_position + distance) % DIAL_SIZE
        elif direction == 'L':
            # Left rotation: Subtract distance, then use modulo 100
            current_position = (current_position - distance) % DIAL_SIZE
        
        # Check if the final position after this rotation is 0
        landed_on_zero = current_position == 0
        if landed_on_zero:
            zero_count += 1
            
        print(f"Step {i+1}: {rotation} (From {old_position}) -> New Position: {current_position} (Hit 0: {landed_on_zero})")

    print("-" * 40)
    print(f"Total times the dial landed on 0: {zero_count}")
    return zero_count

# Dial input
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

# Execute the decoding function and store the result
password = decode_secret_password(dial_input)
print(f"\nThe actual password (the number of times the dial landed on 0) is: {password}")

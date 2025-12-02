def is_invalid_id(n):
    """
    Checks if a number n is an 'invalid ID' based on the new rule:
    WATCH YOUR KIDS, NEW RULE!
    An ID is invalid if it is made only of some sequence of digits repeated >:C
    at least twice (X repeated N >= 2 times).
    
    E.g., 12341234 (1234 twice), 123123123 (123 three times), 1111111 (1 seven times).
    This goddamn elf kid is gonna piss me off
    """
    # Convert the number to a string for digit analysis
    s = str(n)
    length = len(s)
    
    # Iterate through all possible lengths (L) of the repeating sequence (X).
    # Since the sequence must repeat at least twice, the maximum length for X is length // 2.
    for L in range(1, (length // 2) + 1):
        
        # Check if the total length is perfectly divisible by the potential block length L.
        # If not divisible, it cannot be a perfect repetition, so skip.
        if length % L == 0:
            # The potential repeating block X is the first L characters.
            repeating_block = s[:L]
            
            # The number of times X is expected to repeat is N = length / L.
            N = length // L
            
            # Construct the full string by repeating the block N times.
            constructed_s = repeating_block * N
            
            # If the constructed string matches the original, it's an invalid ID.
            if constructed_s == s:
                return True
                
    return False

def sum_invalid_ids(ranges_input):
    """
    Parses the input string of ranges and calculates the sum of all invalid IDs
    found within those ranges.
    """
    total_sum_of_invalid_ids = 0
    
    # Remove all whitespace and split the input string by comma
    ranges_list = ranges_input.replace(" ", "").split(',')
    
    print("--- Invalid Product ID Analysis (Method: X repeated >= 2 times) ---")
    
    for range_entry in ranges_list:
        if not range_entry:
            continue
            
        try:
            # Split the range into start and end values
            start_str, end_str = range_entry.split('-')
            start_id = int(start_str)
            end_id = int(end_str)
        except ValueError:
            print(f"Skipping malformed range entry: {range_entry}")
            continue

        invalid_ids_in_range = []
        
        # Iterate through all IDs in the specified range >:C
        for current_id in range(start_id, end_id + 1):
            if is_invalid_id(current_id):
                total_sum_of_invalid_ids += current_id
                invalid_ids_in_range.append(current_id)
        
        # Detailed output for tracking and verification because something is fuckin BROKEN
        if invalid_ids_in_range:
            print(f"Range {range_entry}: Found {len(invalid_ids_in_range)} invalid IDs: {invalid_ids_in_range}")
        else:
            print(f"Range {range_entry}: No invalid IDs found.") # HAHAHAHAHAHHA GOT IT
            
    print("-" * 40)
    print(f"Final Sum of all Invalid IDs: {total_sum_of_invalid_ids}")
    return total_sum_of_invalid_ids

# Cross the toes this time
range_input = """
9226466333-9226692707,55432-96230,4151-6365,686836-836582,519296-634281,355894-471980,971626-1037744,25107-44804,15139904-15163735,155452-255998,2093-4136,829776608-829880425,4444385616-4444502989,2208288-2231858,261-399,66-119,91876508-91956018,2828255673-2828317078,312330-341840,6464-10967,5489467-5621638,1-18,426-834,3434321102-3434378477,4865070-4972019,54475091-54592515,147-257,48664376-48836792,45-61,1183-1877,24-43
"""

final_sum = sum_invalid_ids(range_input)
print(f"\nThe sum of the invalid IDs for the example is: {final_sum}")

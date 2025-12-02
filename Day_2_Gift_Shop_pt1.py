def is_invalid_id(n):
    """
    Checks if a number n is an 'invalid ID'.
    An invalid ID is made only of some sequence of digits repeated twice (XX).
    E.g., 55 (5 twice), 6464 (64 twice), 123123 (123 twice).
    This'll teach those parents not to watch their fuckin' kids
    """
    # Convert the number to a string for digit analysis
    s = str(n)
    length = len(s)
    
    # Length must be even to be composed of two equal halves (XX)
    if length % 2 != 0:
        return False
    
    # Get the length of the repeating sub-sequence (X)
    half_length = length // 2
    
    # Check if the first half (X) equals the second half (X)
    first_half = s[:half_length]
    second_half = s[half_length:]
    
    return first_half == second_half

def sum_invalid_ids(ranges_input):
    """
    Parses the input string of ranges and calculates the sum of all invalid IDs
    found within those ranges.
    Damn elf children.
    """
    total_sum_of_invalid_ids = 0
    
    # Remove all whitespace and split the input string by comma
    ranges_list = ranges_input.replace(" ", "").split(',')
    
    print("--- Invalid Product ID Analysis ---")
    
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
        
        # Iterate through all IDs in the specified range (inclusive) FINALLY WORKS AHAHAH
        for current_id in range(start_id, end_id + 1):
            if is_invalid_id(current_id):
                total_sum_of_invalid_ids += current_id
                invalid_ids_in_range.append(current_id)
        
        # Detailed output for tracking and verification
        if invalid_ids_in_range:
            print(f"Range {range_entry}: Found {len(invalid_ids_in_range)} invalid IDs: {invalid_ids_in_range}")
        else:
            print(f"Range {range_entry}: No invalid IDs found.")
            
    print("-" * 40)
    print(f"Final Sum of all Invalid IDs: {total_sum_of_invalid_ids}")
    return total_sum_of_invalid_ids

range_input = """
9226466333-9226692707,55432-96230,4151-6365,686836-836582,519296-634281,355894-471980,971626-1037744,25107-44804,15139904-15163735,155452-255998,2093-4136,829776608-829880425,4444385616-4444502989,2208288-2231858,261-399,66-119,91876508-91956018,2828255673-2828317078,312330-341840,6464-10967,5489467-5621638,1-18,426-834,3434321102-3434378477,4865070-4972019,54475091-54592515,147-257,48664376-48836792,45-61,1183-1877,24-43
"""

# Lets cross our fingers.
final_sum = sum_invalid_ids(range_input)
print(f"\nThe sum of the invalid IDs is: {final_sum}")

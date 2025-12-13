import sys
import re
import os
from dataclasses import dataclass

class Solver:
    def __init__(self, input_filepath="input.txt"):
        self.shapes: list[BlockShape] = []
        self.target_fits: list[RequiredFit] = []
        self.input_filepath = input_filepath
        self.valid_fits_count = 0

    def _parse_input_blocks(self, content: str) -> bool:
        """Helper to parse the file content into shapes and targets."""
        
        # Clean and split content into blocks
        input_blocks = [block.strip() for block in content.split("\n\n") if block.strip()]

        if not input_blocks:
            print("Error: Input file is empty or contains no valid blocks.")
            return False
            
        # Process BlockShape Definitions (all but the last block)
        for block_str in input_blocks[:-1]:
            current_area = 0
            current_coords = []
            
            # Use list comprehension to filter out empty lines and index lines (ending with ':')
            clean_rows = [r.strip() for r in block_str.split('\n') if r.strip() and not r.strip().endswith(':')]
            
            # Calculate coordinates and area
            for row_idx, row_text in enumerate(clean_rows):
                for col_idx, char in enumerate(row_text):
                    if char == '#':
                        current_coords.append(Coordinate(col_idx, row_idx))
                        current_area += 1
            
            self.shapes.append(BlockShape(area=current_area, occupied_coords=current_coords))

        # Process RequiredFit Targets (the last block)
        target_block_str = input_blocks[-1]
        
        for line in target_block_str.split('\n'):
            line_stripped = line.strip()
            if not line_stripped: continue
            
            # Use regex for parsing
            match = re.match(r"(\d+)x(\d+):\s*(.*)", line_stripped)
            
            if match:
                width, height = int(match.group(1)), int(match.group(2))
                counts_str = match.group(3).strip()
                
                # split and map to int in one line
                counts_list = [int(count) for count in counts_str.split()] if counts_str else []
                
                self.target_fits.append(RequiredFit(width, height, counts_list))

        return True

    def read_input(self) -> bool:
        """Reads the file and delegates parsing."""
        if not os.path.exists(self.input_filepath):
            print(f"Error: Input file '{self.input_filepath}' not found.")
            return False

        try:
            with open(self.input_filepath, 'r') as f:
                content = f.read()
        except Exception as e:
            print(f"Error reading file: {e}")
            return False

        return self._parse_input_blocks(content)

    def solve(self):
        """Calculates which target boxes have enough area for the required shapes."""
        if not self.read_input():
            return
            
        print("===Loaded Data===")
        print(f"Total Shapes: {len(self.shapes)}")
        print([f"Shape {i}: Area {s.area}" for i, s in enumerate(self.shapes)])
        print(f"Total Targets: {len(self.target_fits)}")
        
        self.valid_fits_count = 0
        
        for target in self.target_fits:
            target_area = target.width * target.height
            area_needed = 0
            
            for shape_index, count in enumerate(target.required_counts):
                
                if shape_index < len(self.shapes):
                    # Area Sufficiency Check
                    area_needed += count * self.shapes[shape_index].area
                else:
                    print(f"Warning: Count for shape index {shape_index} (count={count}) is out of range.")
                    
            if target_area >= area_needed:
                self.valid_fits_count += 1
                
        print("FINISH:", self.valid_fits_count)

@dataclass(frozen=True)
class Coordinate:
    """Represents a single point (x, y) occupied by a block in a shape."""
    x_coord: int
    y_coord: int

@dataclass
class BlockShape:
    """Represents a single present shape, including its area."""
    area: int
    occupied_coords: list[Coordinate]

@dataclass
class RequiredFit:
    """Represents a target box and the quantity of shapes required to fit inside."""
    width: int
    height: int
    required_counts: list[int]

if __name__ == "__main__":
    file_path = sys.argv[1] if len(sys.argv) > 1 else "input.txt"
    puzzle_solver = Solver(input_filepath=file_path)
    puzzle_solver.solve()

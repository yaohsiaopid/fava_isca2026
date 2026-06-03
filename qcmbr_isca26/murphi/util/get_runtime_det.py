import os
import re
import sys

def extract_times(search_dir):
    m = 0.0
    # Regex 1: Trigger to start looking
    # Case insensitive just in case; remove re.IGNORECASE if strict case needed
    pattern_invariant = re.compile(r"Invariant.*failed", re.IGNORECASE)
    
    # Regex 2: Extract the seconds
    # Looks for "fired in " followed by digits, a dot, digits, and "s"
    pattern_time = re.compile(r"fired in\s+(\d+\.\d+)s")

    # Walk through the directory recursively
    for root, _, files in os.walk(search_dir):
        for filename in files:
            file_path = os.path.join(root, filename)
            
            try:
                # errors='replace' prevents crashing on binary/weird files
                with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                    
                    found_invariant = False
                    
                    for line in f:
                        # State 1: Look for the failure message
                        if not found_invariant:
                            if pattern_invariant.search(line):
                                found_invariant = True
                                continue # Don't check for time on the exact same line (optional)

                        # State 2: Look for the timing
                        elif found_invariant:
                            match = pattern_time.search(line)
                            if match:
                                seconds = match.group(1)
                                print(f"{file_path}: {seconds}")
                                if float(seconds) > m:
                                    m = float(seconds)
                                
                                break

            except Exception as e:
                # Silently skip unreadable files or permissions errors
                continue
    print("-->", m)
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 extract_times.py <directory>")
        sys.exit(1)
    
    target_dir = sys.argv[1]
    extract_times(target_dir)

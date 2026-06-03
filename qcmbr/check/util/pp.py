import sys
import re

def compress_gv_regex(input_file, output_file):
    print(f"Processing {input_file}...")

    try:
        with open(input_file, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: File {input_file} not found.")
        return

    # Regex to find node definitions with positions
    # Matches: node_name [ ... pos="x,y!" ... ]
    # Group 1: Node Name
    # Group 2: X coordinate
    # Group 3: Y coordinate
    node_pattern = re.compile(r'pos="([0-9\.-]+),([0-9\.-]+)!"')
    node_pattern = re.compile(r'^\s*(\w+)\s*\[.*pos="([0-9\.-]+),([0-9\.-]+)!?"?.*\];')
    
    
    used = set()
    skip = set()
    all = set()
    m_ = {}
    for line in lines:
      match = node_pattern.search(line)
      if match:
        name = match.group(1)
        y = float(match.group(3))
        all.add(y)
        # print(y)
        m_[y] = name
        if "shape=circle" in line:
          used.add(y)
        if "Inst" in line:
          skip.add(y)
        # x = match.group(1)
        # y = float(match.group(2))
        # print(x, y)
    avail_keys = sorted(all, reverse=True) 
    next_avail_idx = 0
    remap = {}
    for k in sorted(list(used) + list(skip), reverse=True):
      remap[k] = avail_keys[next_avail_idx] * 0.5
      next_avail_idx += 1

    with open(output_file, 'w') as f_out:
      for line in lines:
        # Check if this line has a position attribute
        match = node_pattern.search(line)
        if match:
          start_g3 = match.start(3) - match.start(0)
          end_g3 = match.end(3) - match.start(0)
          y = float(match.group(3))
          # print(y)
          if y in remap:
            ny=remap[y]
            new_line = line[:start_g3] + str(ny) + line[end_g3:]
            f_out.write(new_line)
          else:
            continue
        else:
          f_out.write(line)


if __name__ == "__main__":
    # compress_gv_regex("coWR_2.gv", "coWR_2.c.gv")
    if len(sys.argv) < 2:
        print("Usage: python compress_gv_regex.py input.gv [output.gv]")
    else:
        input_gv = sys.argv[1]
        output_gv = sys.argv[2] if len(sys.argv) > 2 else input_gv.replace(".gv", ".c.gv")
        compress_gv_regex(input_gv, output_gv)

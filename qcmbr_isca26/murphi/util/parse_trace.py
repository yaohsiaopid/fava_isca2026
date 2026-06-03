import re
import sys
import argparse
import os
sys.path.append("./src")
from gconst import *
def parse_murphi_trace(file_path, m_proc_state_field, m_proc_selc, prefix):
    """
    Parses a Murphi trace file that shows state differences.

    This function performs the following tasks:
    1. Finds the value of 'selc' in the initial startstate.
    2. Tracks the value of 'i_cache[OBJSET_cache_1].CL[{selc}]' across all transitions.
    3. Whenever 'msg_rec_set' changes in a transition, it prints the most
       recently seen value of 'i_cache[OBJSET_cache_1].CL[{selc}]'.

    Args:
        file_path (str): The path to the Murphi trace file.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: File not found at '{file_path}'")
        return
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    # Split the trace into transitions using the delimiter
    transitions = content.split('----------')
    if not transitions:
        print("Trace file appears to be empty or invalid.")
        return

    # --- 1. Get initial values from the start state ---
    start_state_block = transitions[0]
    selc_value = None
    prev_val = None
    last_known_cache_value = None

    # Find "selc: <value>"
    var_ = {}
    for tar in ["selc", "myaddr"]:
      selc_match = re.search(fr'^\s*{tar}:\s*(\w+)', start_state_block, re.MULTILINE)
      if not selc_match:
        #   print(f"Error: Could not find '{tar}' value in the startstate block.")
          continue
          #return
      selc_value = selc_match.group(1)
      var_[tar] = selc_value
      # print(f"Found '{tar}' value in startstate: {selc_value}")
    tar_var = m_proc_selc
    for k, v in var_.items():
        tar_var = tar_var.replace(k, v)
    tar_var += "." + m_proc_state_field
    # print("==> tar_var", tar_var)
    #"selc", var_['selc']).replace("myaddr", var_['myaddr']) + "." + m_proc_state_field

    # Define the target cache line variable and create a regex for it
    # tar_var = f"i_cache[OBJSET_cache_1].CL[{selc_value}]"
    cache_val_pattern = re.compile(
        r'^\s*' + re.escape(tar_var) + r':\s*(\w+)',
        re.MULTILINE
    )

    # Find the initial value of the cache line
    initial_cache_match = cache_val_pattern.search(start_state_block)
    if initial_cache_match:
        last_known_cache_value = initial_cache_match.group(1).strip()
        # print(f"Initial value of '{tar_var}':\n  {last_known_cache_value.replace(os.linesep, os.linesep + '  ')}\n")
    else:
        print(f"Warning: Could not find initial value for '{tar_var}' in startstate.\n")

    # --- 2. Process subsequent transitions ---
    # print("Searching for changes in 'msg_rec_set' and reporting most recent 'i_cache' value...")
    ret = {}
    for i, block in enumerate(transitions[1:]):
        transition_num = i + 1
        # First, always check if the cache line value was updated in this transition
        # to keep our "last known value" current.
        cache_update_match = cache_val_pattern.search(block)
        if cache_update_match:
            prev_val = last_known_cache_value
            last_known_cache_value = cache_update_match.group(1).strip()

        # Second, check if our trigger condition ('msg_rec_set' changed) occurred.
        if f'msg_{prefix}_set' in block:
            # print(f"\n--- Transition {transition_num}: 'msg_rec_set' changed ---")

            pattern = fr"msg_{prefix}_set\[(\w+)\]:(\w+)"
            matches = re.findall(pattern, block)
            # print(f"\n--- Transition {transition_num}: 'msg_rec_set' changed ---")
            if "last" in block:
                if not (len(ret) == len([k for k, v in matches if v == "true"])):
                  print("-->", prefix, file_path, ret, matches)
                assert(len(ret) == len([k for k, v in matches if v == "true"]))
                continue 

            for mtype, value in matches:
              # print(f"Type: {mtype}, Value: {value}")
              # if prefix is "rec", then its associated with either the previous
              # state if there's change otherwise the current state 
              if prefix == "rec":
                if cache_update_match:
                  # print("->", prev_val) 
                  assert(not mtype in ret)
                  ret[mtype] = prev_val
                else:
                  #print("->", last_known_cache_value)
                  assert(not mtype in ret)
                  ret[mtype] = last_known_cache_value
              else:
                if cache_update_match:
                  # print("-> sent ", mtype, last_known_cache_value) 
                  ret[mtype] = last_known_cache_value
                else:
                  # print("--> ???? ", prefix, file_path, ret, matches, last_known_cache_value)
                  ret[mtype] = last_known_cache_value
                  # assert (0)


            # if last_known_cache_value is not None:
            #     # Report the most recent value we have seen so far
            #     print(f"  Most recent value of '{tar_var}':\n    {last_known_cache_value.replace(os.linesep, os.linesep + '    ')}")
            # else:
            #     # This would happen if the value was not in the startstate and hasn't appeared yet
            #     print(f"  Value of '{tar_var}' has not been seen in the trace yet.")
    #if len(ret) == 0:
    #  print("->", file_path, prefix)
    #assert(len(ret) > 0)
    return ret
if __name__ == "__main__":
    # main()
    parse_murphi_trace("build/s4_1_msg_per_rset:assert/_build/cache_I_ci_store_8_trace_rec_0.txt", m_proc_state_field, m_proc_selc, "rec")
    # parse_murphi_trace("build/s4_1_msg_per_rset:assert/_build/cache_S_ci_store_9_trace_sent_0.txt", m_proc_state_field, m_proc_selc, "sent")
    # parse_murphi_trace("build/s4_msg_per_rset/_build/cache_S_ci_store_9_trace.txt", m_proc_state_field, m_proc_selc, "sent")
import subprocess
import os
import re
import importlib.util
import itertools
import sys
sys.path.append("src")
from gconst import *
import pickle

def get_set_info(resff, prefix, msg_type_arr):
  msg_set = {}
  if msg_type_arr is None:
    pattern = re.compile(rf"msg_imm_{prefix}_set\[(\w+)\]:(\w+)")
  else:
    pattern = re.compile(rf"msg_imm_{prefix}_set_(\w+)\[(\w+)\]:(\w+)")
  assert(os.path.exists(resff))
  with open(resff, "r") as f:
    found_last_state = False
    for line in f:
      if "The last state" in line:
        found_last_state = True
        continue
      if not found_last_state:
        continue
      match = pattern.search(line)
      if not match:
        continue
      if msg_type_arr is None:
        msg_type = match.group(1)
        is_active = match.group(2).lower()
        msg_set[msg_type] = is_active
      else:
        msg_type_group = match.group(1)
        msg_type = match.group(2)
        is_active = match.group(3).lower()
        if msg_type_group not in msg_set:
          msg_set[msg_type_group] = {}
        msg_set[msg_type_group][msg_type] = is_active
  return msg_set
def flat_msg_types():
  """Returns a flat list of all message type names regardless of protocol."""
  if all_msg_types is not None:
    return all_msg_types
  result = []
  for types in all_msg_types_by_type.values():
    result.extend(types)
  return result

def iter_msg_types_with_record():
  """Yields (murphi_record_type, mtype) pairs.
  murphi_record_type is None for single-record protocols (e.g. MSI)."""
  if all_msg_types is not None:
    for mtype in all_msg_types:
      yield (None, mtype)
  else:
    for murphi_type, msg_types in all_msg_types_by_type.items():
      for mtype in msg_types:
        yield (murphi_type, mtype)

def prepare_header(outff_h, design_file):
  with open(f"{design_file}", "r") as tmpf:
    for ln in tmpf:
      outff_h.write(ln)

def power_set(iterable, nonempty=True):
    """Returns the power set of a given iterable."""
    s = list(iterable)
    if nonempty:
      return list(itertools.chain.from_iterable(itertools.combinations(s, r) for r in range(1, len(s) + 1)))
    else:
      return list(itertools.chain.from_iterable(itertools.combinations(s, r) for r in range(0, len(s) + 1)))

def add_to_all_rules(s, to_add):
    """
    Splits the string by the 'rule' keyword, processes each block,
    and rejoins them.
    """
    # 1. Split the string by the 'rule' keyword. The parentheses `(rule)`
    #    ensure that the delimiter ("rule") is kept in the list.
    parts = re.split(r'(rule)', s)
    
    # The resulting list looks like: ['', 'rule', ' block A ', 'rule', ' block B ']
    
    # 2. Iterate through the parts and process each rule block
    for i in range(len(parts)):
        # The content of a rule block is the item *after* a "rule" item
        if parts[i] == 'rule' and i + 1 < len(parts):
            rule_content = parts[i+1]
            idx = rule_content.lower().find("begin") 
            if idx == -1:
              # 3. In this specific block, replace only the *first* "==>"
              #    with "==>JJJ".
              modified_content = rule_content.replace('==>', 
                  "==>\n" + to_add, 1)
            else:
              modified_content = rule_content[:idx+5] + "\n" + to_add + \
                  rule_content[idx+5:]
            



            # Update the list with the modified content
            parts[i+1] = modified_content
            
    # 4. Join all the parts back together into a single string
    return "".join(parts)

def get_order(inff):
  result = subprocess.run(['awk', '/last state of the trace/ {flag=1} flag && /reached_set_order/', inff], 
        stdout=subprocess.PIPE, stderr=subprocess.PIPE) 
  pattern = r"reached_set_order\[(.*)\]:(\d+)"
  all_matches = re.findall(pattern, result.stdout.decode('utf-8'))
  return all_matches

def get_state_per_msg(inff, varname):
  result = subprocess.run(['awk', ('/last state of the trace/ {flag=1} flag && /%s/' % varname), inff], 
        stdout=subprocess.PIPE, stderr=subprocess.PIPE) 
  pattern = fr"{varname}\[(.*)\]:(.*)\n"
  all_matches = re.findall(pattern, result.stdout.decode('utf-8'))
  return all_matches

def err_chk_file(ffname):
  assert(os.path.exists(ffname))
  result = subprocess.run(["grep",  "-q", f"Assertion failed", ffname], stdout=subprocess.PIPE, stderr=subprocess.PIPE) 
  exit_status = result.returncode
  if exit_status == 0:
    assert (0)

def get_inline_prop_file(resff, propname, assertion=False):
  assert(os.path.exists(resff))
  result = subprocess.run(
      ["grep", "-q", f"Assertion failed: {propname}", resff],
      stdout=subprocess.PIPE, stderr=subprocess.PIPE
  )
  # grep returns 0 if the pattern is found (assertion failed)

def get_res_file_stats(resff, propname, assertion=False, inline_prop=False):
  assert(os.path.exists(resff))
  tar_s = f"Invariant \"{propname}\" failed"
  if inline_prop:
    tar_s = f"Assertion failed: {propname}"
  result = subprocess.run(["grep",  "-q", tar_s, resff],
      stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode
  no_err = subprocess.run(["grep",  "-q", f"No error found.", resff],
      stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode
  
  last = subprocess.run(["tail",  "-n1", resff], 
      stdout=subprocess.PIPE, stderr=subprocess.PIPE) 
  ll=last.stdout.decode('utf-8')
  t=None
  if ll.startswith("Time"):
    pattern = r'\d+\.?\d*'
    match = re.search(pattern, ll)
    if match:
        # match.group(0) returns the entire matched string
        t=float(match.group(0))
  if result == 0:
    return (not assertion, t)
  if no_err == 0:
    return (assertion, t)
  if os.getenv("DEBUG") == "1":
    print("--> undetermined", resff)
  return (None, t)
    
res_file_stats = {
    "completed": [],
    "completed_ff": [],
    "undetermined": [],
    "undetermined_ff": [],
    "unknow_ff": []
}
invoked = False
def dump_stats():
  global res_file_stats
  if invoked:
    with open ("build/stats.pkl", "wb") as f:
      pickle.dump(res_file_stats, f)
# if its assertion type, return true if proven; otherwise cover type, return
# true if reachable

def get_res_file(resff, propname, assertion=False, inline_prop=False):
  global res_file_stats
  global invoked
  if not invoked:
    if os.path.exists("build/stats.pkl"):
      with open ("build/stats.pkl", "rb") as f:
        res_file_stats = pickle.load(f)
    invoked = True
  # print("processing res file", resff)
  if not os.path.exists(resff):
    print("==> NOT FOUND", resff)
  assert(os.path.exists(resff))
  if propname is not None:
    tar_s = f"Invariant \"{propname}\" failed"
    if inline_prop:
      tar_s = f"Assertion failed: {propname}"
    result = subprocess.run(["grep",  "-q", tar_s, resff],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    exit_status = result.returncode
  else:
    exit_status = 0

  last = subprocess.run(["tail",  "-n1", resff], 
      stdout=subprocess.PIPE, stderr=subprocess.PIPE) 
  ll=last.stdout.decode('utf-8')
  t=None
  if ll.startswith("Time"):
    pattern = r'\d+\.?\d*'
    match = re.search(pattern, ll)
    if match:
        # match.group(0) returns the entire matched string
        t=float(match.group(0))
        if not resff in res_file_stats['completed_ff']:
          res_file_stats['completed_ff'].append(resff)
          res_file_stats['completed'].append(t)
          # print("==>HERE", t)
  if t is None:
    if "explored in " in ll:
      pattern = r'explored in (\d+\.?\d+)s'
      match = re.search(pattern, ll)
      if match:
        t=float(match.group(1))
        if not resff in res_file_stats['undetermined_ff']:
          res_file_stats['undetermined_ff'].append(resff)
          res_file_stats['undetermined'].append(t)
    else:
      last = subprocess.run(["grep",  "rules fired in ", resff], 
        stdout=subprocess.PIPE, stderr=subprocess.PIPE) 
      ll=last.stdout.decode('utf-8')
      pattern = r'rules fired in (\d+\.?\d+)s'
      match = re.search(pattern, ll)
      if match:
        t=float(match.group(1))
        if not resff in res_file_stats['completed_ff']:
          res_file_stats['completed_ff'].append(resff)
          res_file_stats['completed'].append(t)
      else:
        if not resff in res_file_stats['unknow_ff']:
          res_file_stats['unknow_ff'].append(resff)


  if exit_status == 0:
    return (not assertion)
  else:
    return assertion
def get_file_stats():
  return res_file_stats
  

def get_rset_h(rset_h):
  rset_s = ""
  for s_ in all_llc_states:
    if s_ in aset:
      rset_s += dis_ele_h.format(state=s_, inset="1")
    else:
      rset_s += dis_ele_h.format(state=s_, inset="0")
  return rset_s
def get_last_state(resff, var_name, arr=False):
  assert(os.path.exists(resff))
  sent_match = None
  if arr:
    sent_match = {}
  with open(resff, "r") as f:
      found_last_state = False
      for line in f:
          if "The last state" in line:
              found_last_state = True
              continue
          
          if found_last_state:
            if not arr:
              match = re.search(rf"{var_name}:(\w+)", line)
              if match:
                sent_match = match.group(1)
            else:
              match = re.search(rf"{var_name}\[(\w+)\]:(\w+)", line)
              if match:
                  msg_type = match.group(1)
                  val = match.group(2).lower() 
                  sent_match[msg_type] = val
  return sent_match

def get_resff_multiset(resff, multiset_name):
  ret = set()
  with open(resff , 'r', encoding='utf-8') as f:
    content = f.read()

  transitions = content.split('----------')
  if not transitions:
    print("Trace file appears to be empty or invalid.")
    return

  # --- 1. Get initial values from the start state ---
  start_state_block = transitions[0]
  # Find "selc: <value>"
  var_ = {}
  for tar in ["selh", "myaddr"]:
    selc_match = re.search(fr'^\s*{tar}:\s*(\w+)', start_state_block, re.MULTILINE)
    if not selc_match:
        print(f"Error: Could not find '{tar}' value in the startstate block.")
        return
    selc_value = selc_match.group(1)
    var_[tar] = selc_value
    # print(f"Found '{tar}' value in startstate: {selc_value}")
  #tar_var = m_proc_selc.replace("selc", var_['selc']).replace("myaddr", var_['myaddr']) + "." + m_proc_state_field
  # tar_var = f"{m_home_cur}.{m_home_sharer_field}"
  tar_var = multiset_name # f"{m_home_cur}.{m_home_sharer_field}"
  for k, v in var_.items():
    tar_var = tar_var.replace(k, v)
  # print("-->", tar_var)


  with open(resff, "r") as f:
    found_last_state = False
    for line in f:
      if "The last state" in line:
        found_last_state = True
        continue
    
      if found_last_state:
        rs = re.compile(re.escape(tar_var) + r"\{[0-9]+\}:(\w+)")
        match = re.search(rs, line)
        if match:
          # print("->", match.group(1))
          ret.add(match.group(1))
  # print("=>", ret)
  # print(var_)
  return ret

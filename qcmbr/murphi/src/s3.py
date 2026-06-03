# In s1 and s2 we get all pair of (s, req) that falls in one of the category
# a) accepts exclusively request (and init txn)
# b) accepts and processes request atomically (no txn)
# c) processes existing earlier request of some type
# This step handles case c) to collect all events hapepning during a txn
# - Assumption: in enumerating all reachable set (assuming each state may be
# "enter" at most once during a single transaction)
import fire
import pickle
from gconst import *
from util import *
import subprocess
import os 
import sys
import re
from common_templates import *
if sys.version_info < (3, 6):
  sys.exit(1)
sys.path.append("src")
from code_gen.parse_rules import *

if design_cfg.get('dist_dir', False):
  # we explore only the symmetry set of cores 
  design_cfg['opt_cond_selc'] = "if (n != Home) then\n selc := n; end;\n"

build_dir="build" # past_builds/MSI_fixed_build"
# Assume running from topdir
dirname = f"{build_dir}/s3_rset_txn/out"
logfile = f"{build_dir}/s3_rset_txn/meta.txt"
os.makedirs(dirname, exist_ok = True)  
# cover (defined && prevState == {state} && defined && preReq == {req} && defined && req == {req}) ===
# assert (defined && prevState == {state} -> not (defined && req == {req})) ===
# assert (defined && prevState == {state} -> (!defined || req != {req}))

# !(Procs[selc].{m_proc_state_field} = P_I | Procs[selc].{m_proc_state_field} = P_V)) then
# !(stable_state_disjunction)

# cover (tracked & (start == false i.e., ends) &  reached_some_set)
# assert (tracked & (start == false i.e., ends) --> !reached_some_set)

# {reachable_set} = disjuction overe (MultisetCount(i:reached_set,
# reached_set[i] = {state}) = 1)
rset_template = '''
invariant "{state}_{req}_rset_{idx}"
(tracked & !start) ->
cur_idx != {tar_len};
'''

max_len = 0
assert(os.path.exists(f"{build_dir}/s1_2_transition/_build/todo.txt"))
todo_list = []
with open(f"{build_dir}/s1_2_transition/_build/todo.txt", "r") as f:
  for ln in f:
    aset = ln[:-1].split(",")
    todo_list.append(aset)
    if len(aset) > max_len:
      max_len = len(aset)
assert(max_len <= 6) # TODO: multiset sizing

def gen():

  # todo_list = power_set(all_cc_states)
  # unreachable as the set of (state, req) to explore the transaction
  s2resdirname = f"{build_dir}/s2_req_proc_state/_build"
  todo = []
  lg_f = open(f"{logfile}", "w")
  with open(f"{s2resdirname}/res.txt", "r") as f:
    st = False
    for ln in f:
      if ln.startswith("Unreachable"):
        st = True
      elif ln.startswith("Reachable"):
        st = False
      else:
        if st:
          todo.append(tuple(ln[:-1].split(",")))
  for t_ in todo:
    assert(len(t_) == 2)
    state, req = t_
    # enumerate all reachable set (assuming each state may be "enter" at most
    # once during a single transaction)
    idx = 0
    for aset in todo_list:
      # if state in aset:
      #   print("skipping " + ("+".join(aset)) + " for " + state + " with " + req)
      #   continue
      if not state == aset[0]:
        continue
      asets = "+".join(aset[1:])
      lg_f.write(f"{state},{req},{idx},{asets}\n")
      outff = f"{dirname}/{state}_{req}_{idx}.m"
      outff_h = open(outff, "w")

      # parse_murphi_model(coh_model_file, nodes_iter_types, outff_h, {"track_req": True, "prevState": True, "rset": {"num": max_len, "state_type_name": m_proc_state_type, "m_proc_selc": m_proc_selc, "m_proc_state_field": m_proc_state_field, "stable_state_df": "|".join([f"cur_state = {s}" for s in all_cc_stable_states]), "block_within_start": ""} })

      # # prepare_header(outff_h, "/Users/yaohsiao/work/coh_syn_dev/murphi/protocols/fv/msi_fv_envs/msi.fvt.s3_rset.m") # design_file)
      # rset_s = ""
      # for s_ in all_cc_states:
      #   if s_ in aset[1:]:
      #     rset_s += dis_ele.format(state=s_, inset="1")
      # rset_s += f"(MultisetCount(i:reached_set, true) = {len(aset[1:])}) & \n"
        
      ################################################################################ 
      tar_states = list(aset[1:])
      parse_murphi_model(coh_model_file, nodes_iter_types, outff_h, {
        "track_req": True,
        "prevState": True,
        "rset": {
          "mode": "tar_idx", # original: use None
          "state_type_name": m_proc_state_type,
          "stable_state_df": "|".join([f"cur_state = {s}" for s in all_cc_stable_states]),
          "block_within_start": "",
          "tar_states": tar_states,
          "tar_target_len": len(tar_states),
        },
      })
      ################################################################################
      outff_h.write(track_template.format(state=state, req=req, m_proc_state_field=m_proc_state_field, m_req_type_field=m_req_type_field))
      outff_h.write(rset_template.format(state=state, req=req, idx=idx, tar_len=len(tar_states)))
      outff_h.close()
      idx += 1 
  lg_f.close()

# - [ ] val_chg = '''prevProcs.{m_proc_cl_field} != {m_proc_arr}[selc].{m_proc_cl_field}'''
# - [ ] multiset add a list to track orders 
# - [ ] assert valu equality to request's data 

# cover ({reachable_set} & val != prev_val when at s)
block_record = '''
if ({proc_state_expr} = {tar_state} & prevStateVal != {m_proc_selc}.{m_proc_cl_field}) then
  val_chk := true; 
  assert ({proc_state_expr} != prevProcs) "NO PERMISSION STATE CHANGE?";
endif;
'''
val_template = '''
invariant "{state}_{req}_rset_{idx}"
(tracked & !start & {match_guard}
 true) ->
!(val_chk = true); 
-- violation: {ele} is in the reachable_set and change value is possible
'''
req_val_record = '''
if ({proc_state_expr} = {tar_state}) then 
  assert (trackReq.vld) "not vld trackReq";
  val_chk := (trackReq.tp = {req_type} & {m_proc_selc}.{m_proc_cl_field} = trackReq.cl);
endif;
'''
req_val_template = '''
invariant "{state}_{req}_rset_{idx}"
(tracked & !start & {match_guard}
 true) ->
(val_chk = true);
-- proven: {ele} is in the reachable_set and value always match current request data argument
'''

order_picl_template = '''

invariant "ASSERT_{state}_{req}_rset_{idx}"
(tracked & !start & 
{match_guard}
true ) ->
({conj});
'''

def gen_s2():
  # TODO 
  # design_cfg['end_state_perform']
  # 
  global logfile 
  if not os.path.exists(logfile):
    print(logfile, "not exist")
    sys.exit(0)
  reachable = []
  reachable_order = []
  unreachable = []
  resdirname = f"{build_dir}/s3_rset_txn/_build"
  if not os.path.exists(resdirname):
    sys.exit(0)

  lg_f = open(f"{logfile}", "r")
  for ln in lg_f:
    #  lg_f.write(f"{state},{req},{idx},{asets}\n")
    ln_ = ln[:-1].split(",")
    assert(len(ln_) == 4)
    state, req, idx, asets = ln_
    asets = asets.split("+")
    resff = f"{resdirname}/{state}_{req}_{idx}.txt"
    prop = f"{state}_{req}_rset_{idx}"
    ret = get_res_file(resff, prop, assertion=False, inline_prop=False)
    (ret2, t) = get_res_file_stats(resff, prop, assertion=False, inline_prop=False)
    if ret: 
      # find failure 
      reachable.append((state, req, idx, "+".join(asets)))  
      order = get_order(resff)
      reachable_order.append(order)
    else:
      unreachable.append((state, req, idx, "+".join(asets)))
  with open(f"{resdirname}/res.txt", "w") as f:
    f.write("Reachable (reachable set during a transaction of <s> <req>)\n")
    for itm in reachable:
      f.write(",".join(itm) + "\n")
    f.write("Unreachable \n")
    for itm in unreachable:
      f.write(",".join(itm) + "\n")

  all_possible_ordered_set = []
  with open(f"{build_dir}/s1_2_transition/_build/todo.txt", "r") as f:
    for ln in f:
      aset = ln[:-1].split(",")
      all_possible_ordered_set.append(aset)
  for itm in reachable:
    state, req, idx, aset_ss = itm 
    aset = aset_ss.split("+")
    cnt = 0
    for l in all_possible_ordered_set:
      if set(l[1:]) == set(aset):
        cnt += 1
    if cnt > 1:
      print("-> more than one possibility: ", itm)
  dirname = f"{build_dir}/s3_2_reachable_set_val/out"
  os.makedirs(dirname, exist_ok = True)  
  for itm in reachable:
    state, req, idx, aset_s = itm
    aset = aset_s.split("+")
    tar_states = list(aset)
    match_guard = f"cur_idx = {len(tar_states)} & \n"
    for ele in aset:
      outff = f"{dirname}/{state}_{req}_{idx}_val_for_{ele}.m"
      outff_h = open(outff, "w")

      blk_s = block_record.format(m_proc_selc=m_proc_selc, m_proc_state_field=m_proc_state_field, tar_state=ele, m_proc_cl_field=m_proc_cl_field,proc_state_expr=get_proc_state_expr())
      parse_murphi_model(coh_model_file, nodes_iter_types, outff_h, {
        "track_req": True,
        "prevState": True,
        "prevStateVal": True,
        "rset": {
          "mode": "tar_idx",
          "state_type_name": m_proc_state_type,
          "stable_state_df": "|".join([f"cur_state = {s}" for s in all_cc_stable_states]),
          "block_within_start": blk_s,
          "tar_states": tar_states,
          "tar_target_len": len(tar_states),
        },
      }, additional_var={"val_chk": ("boolean", "val_chk := false;\n", ""), })
      #with open("/Users/yaohsiao/work/coh_syn_dev/murphi/protocols/fv/msi_fv_envs/msi.fvt.s3_2_rset_val.m", "r") as f:
      #  for ln in f:
      #    if "BLOCK_WITHIN_START" in ln:
      #      outff_h.write()
      #      continue
      #    outff_h.write(ln)

      outff_h.write(track_template_ff(state, req, m_req_type_field, m_proc_state_field = m_proc_state_field, isEntry = False, withTrackReq = False))
      outff_h.write(val_template.format(state=state, req=req, m_proc_state_field=m_proc_state_field, m_req_type_field=m_req_type_field, ele=ele, idx=idx, match_guard=match_guard))
      outff_h.close()

      if not req in type_with_args:
        continue

      outff = f"{dirname}/{state}_{req}_{idx}_val_eq_req_for_{ele}.m"
      outff_h = open(outff, "w")
      blk_s = req_val_record.format(m_proc_selc=m_proc_selc, m_proc_state_field=m_proc_state_field, tar_state=ele, req_type = req, m_proc_cl_field=m_proc_cl_field,proc_state_expr=get_proc_state_expr())
      parse_murphi_model(coh_model_file, nodes_iter_types, outff_h, {
        "track_req": True,
        "prevState": True,
        "prevStateVal": True,
        "rset": {
          "mode": "tar_idx",
          "state_type_name": m_proc_state_type,
          "stable_state_df": "|".join([f"cur_state = {s}" for s in all_cc_stable_states]),
          "block_within_start": blk_s,
          "tar_states": tar_states,
          "tar_target_len": len(tar_states),
        },
      }, additional_var={"val_chk": ("boolean", "val_chk := false;\n", ""), "trackReq": ("CoreReq", "undefine trackReq;\n", "")})
      #with open("/Users/yaohsiao/work/coh_syn_dev/murphi/protocols/fv/msi_fv_envs/msi.fvt.s3_2_rset_val.m", "r") as f:
      #  for ln in f:
      #    if "BLOCK_WITHIN_START" in ln:
      #      outff_h.write()
      #      continue
      #    outff_h.write(ln)

      outff_h.write(track_template_ff(state, req, m_req_type_field, m_proc_state_field = m_proc_state_field, isEntry = False, withTrackReq = True))
      outff_h.write(req_val_template.format(state=state, req=req, m_proc_state_field=m_proc_state_field, m_req_type_field=m_req_type_field, ele=ele, idx=idx, match_guard=match_guard))
      outff_h.close()


  if os.path.exists(f"{build_dir}/s1_2_transition/_build/todo.txt"):
    todo_list = []
    with open(f"{build_dir}/s1_2_transition/_build/todo.txt", "r") as f:
      for ln in f:
        aset = ln[:-1].split(",")
        todo_list.append(aset)
  todo_in_reachable = []
  for itm in reachable:
    state, req, idx, aset_s = itm
    cur_set = aset_s.split("+")
    cnt = 0
    for aset in todo_list:
      if set(aset) == set(cur_set):
        cnt += 1
    if cnt > 1:
      print("-- todo -->", itm)
      todo_in_reachable.append(itm)
  with open(f"{resdirname}/rset_ordering_todo.txt", "w") as f:
    for itm in todo_in_reachable:
      state, req, idx, aset_s = itm
      f.write(",".join(itm) + "\n")



def pp():
  # TODO:
  # check Assertion failed
  # unreachable as the set of (state, req) to explore the transaction
  resdirname = f"{build_dir}/s3_rset_txn/_build"
  todo = []
  with open(f"{resdirname}/res.txt", "r") as f:
    st = False
    for ln in f:
      if ln.startswith("Reachable"):
        st = True
      elif ln.startswith("Unreachable"):
        st = False
      elif st:
        todo.append(tuple(ln[:-1].split(",")))
  dirname = f"{build_dir}/s3_2_reachable_set_val/_build"

  reachable = {} # value can change
  unreachable = {} # value don't change

  proven_req_w_data_arg = {}
  disproven_req_w_data_arg = {}
  for t_ in todo:
    assert(len(t_) == 4)
    state, req, idx, rset_ss = t_
    rset = rset_ss.split("+")
    k = (state, req, idx, "+".join(rset))
    reachable[k] = []
    unreachable[k] = []
    if req in type_with_args:
      proven_req_w_data_arg[k] = []
      disproven_req_w_data_arg[k] = []
    for ele in rset: 
      resff = f"{dirname}/{state}_{req}_{idx}_val_for_{ele}.txt"
      prop = f"{state}_{req}_rset_{idx}"
      ret = get_res_file(resff, prop)
      (ret2, t) = get_res_file_stats(resff, prop, assertion=False, inline_prop=False)
      if ret:
        # find failure 
        reachable[k].append(ele)
      else:
        unreachable[k].append(ele)

      if not req in type_with_args:
        continue
      resff = f"{dirname}/{state}_{req}_{idx}_val_eq_req_for_{ele}.txt"
      prop = f"{state}_{req}_rset_{idx}"
      ret = get_res_file(resff, prop, assertion=True)
      (ret2, t) = get_res_file_stats(resff, prop, assertion=False, inline_prop=False)
      if ret:
        proven_req_w_data_arg[k].append(ele)
      else:
        disproven_req_w_data_arg[k].append(ele)

  data_results = {}
  data_results['val_change'] = reachable
  data_results['val_no_change'] = unreachable
  data_results['val_eq_st_data'] = proven_req_w_data_arg 
  data_results['val_neq_st_data'] = disproven_req_w_data_arg 

  with open(f"{dirname}/res.pkl", "wb") as f:
    pickle.dump(data_results, f)

  with open(f"{dirname}/res.txt", "w") as f:
    f.write("For a given picl sets starts with (state, req), which PiCL/state can have the value component differed from previous picl?\n")
    f.write("Reachable:\n")
    for k, v in reachable.items():
      if len(v) == 0:
        continue
      f.write(",".join(k) + ": ")
      f.write(";".join(v) + "\n")
    f.write("Unreachable:\n")
    for k, v in unreachable.items():
      if len(v) == 0:
        continue
      f.write(",".join(k) + ": ")
      f.write(";".join(v) + "\n")
    f.write("For a given picl sets starts with (state, req), which PiCL/state can have the value component always the same as data argument?\n")
    f.write("Proven:\n")
    for k, v in proven_req_w_data_arg.items():
      if len(v) == 0:
        continue
      f.write(",".join(k) + ": ")
      f.write(";".join(v) + "\n")
    f.write("Disproven:\n")
    for k, v in disproven_req_w_data_arg.items():
      if len(v) == 0:
        continue
      f.write(",".join(k) + ": ")
      f.write(";".join(v) + "\n")
  with open(f"{dirname}/todo_msg.txt", "w") as f:
    # possible to change value 
    # for each rset, the picl in it we need the value 
    for k, v in reachable.items():
      if len(v) == 0:
        continue
      # These are where we need to specify the value component 
      # Possibility 1: Proven to be always argument of the request => skip 
      # Possibility 2: Incoming message 
      todo_ = []
      for state_ in v:
        if k in proven_req_w_data_arg and state_ in proven_req_w_data_arg[k]:
          # possibility 1 is ruled out 
          print("skip", k, state_)
          continue
        else:
          # possibility 2 to do
          todo_.append(state_)
      if len(todo_) > 0:
        # TODO what message could come in this state
        f.write(",".join(k) + ": ")
        f.write(";".join(todo_) + "\n")


if __name__ == "__main__":
  fire.Fire()
  dump_stats()
    
     

        

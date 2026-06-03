# In s1 we get all pair of (s, req) indicating <s> can accept a request <req>
# This step distinguish the case (s, req) where <s> accept and atomically
# process at the same time "without initiating txn"
# <s> can perform request <r> without transaction iff it is possible that a
# cache starting from <s> can accept two requests of same type <r> back-to-back
# (i.e., in two consecutive transition step), although it may transition into
# S' after the first time step (e.g., E can accept and perform load/store and
# transitions to M for store).
# Proof: 
# 1) Consider <s> can perform request <r> without transaction. It means the
# permission level is sufficient. If so, then in next step the CC should be able
# to serve another request of same type <r>.  Otherwise its a contradication of
# the permission level. 
# 2) Consider it is possible that a cache starting from <s> can accept two <r>
# back-to-back. Either its a stable-state protocol without any transient state,
# or that the <s> can perform request <r> without transaction, since
# transaction presumably takes more than single time step.
import pickle
from gconst import *
from util import *
import subprocess
import os 
import sys
import re
if sys.version_info < (3, 6):
  sys.exit(1)
sys.path.append("src")
from code_gen.parse_rules import *

# if design_cfg.get('dist_dir', False):
#   # we explore only the symmetry set of cores 
#   design_cfg['opt_cond_selc'] = "if (n != Home) then\n selc := n; end;\n"

# Assume running from topdir
dirname = "build/s2_req_proc_state/out"
logfile = "build/s2_req_proc_state/meta.txt"
os.makedirs(dirname, exist_ok = True)  
# cover (defined && prevState == {state} && defined && preReq == {req} && defined && req == {req}) ===
# assert (defined && prevState == {state} -> not (defined && req == {req})) ===
# assert (defined && prevState == {state} -> (!defined || req != {req}))
template = '''
invariant "{state}_accept_and_perform_{req}"
  (!IsUndefined(prevProcs_2) & (prevProcs_2 = {state}) & 
  !IsUndefined(prevProcReq_2.{m_req_type_field}) & (prevProcReq_2.{m_req_type_field} = {req}) {cond}) -> 
  (IsUndefined(prevProcReq.{m_req_type_field}) | (prevProcReq.{m_req_type_field} != {req}));
'''

# cover (defined && prevState == {state} && defined && preReq == {req} && 
#    defined && req == {req} && state == {state_prime}) EQUIV TO
# assert (
#  (defined && prevState == {state} && defined && preReq == {req}) |-> 
#    not(defined && req == {req} && state == {state_prime})
# ) 
c_template = '''
invariant "{state}_accept_and_perform_{req}_change_to_{state_prime}"
  (!IsUndefined(prevProcs_2) & (prevProcs_2 = {state}) & 
  !IsUndefined(prevProcReq_2.{m_req_type_field}) & (prevProcReq_2.{m_req_type_field} = {req})) -> 
  (IsUndefined(prevProcs) | (prevProcs != {state_prime}) |
  IsUndefined(prevProcReq.{m_req_type_field}) | (prevProcReq.{m_req_type_field} != {req} ));
'''

# cover (defined && prevState == {state} && defined && preReq == {req} && 
#    defined && req == {req} && val != prevVal) EQUIV TO
# assert (
#  (defined && prevState == {state} && defined && preReq == {req}) |-> 
#    not(defined && req == {req} && val != prevVal)
# ) 
# EQVUI 
# !defined | req != {req} | val == prevVal
# V   - store_rule --> V -- store --> V
# prevProcs_2      prevProcs       state
d_template = '''
invariant "{state}_accept_and_perform_{req}_value_change"
  (!IsUndefined(prevProcs_2) & (prevProcs_2 = {state}) & 
  !IsUndefined(prevProcReq_2.{m_req_type_field}) & (prevProcReq_2.{m_req_type_field} = {req})) -> 
  (IsUndefined(prevStateVal) | 
    (prevStateVal = prevStateVal_2) |
  IsUndefined(prevProcReq.{m_req_type_field}) | (prevProcReq.{m_req_type_field} != {req} ));
'''

# assert (defined && prevState == {state} && defined && preReq == {req} && 
#     |-> current_val == preReq.val)
e_template = '''
invariant "{state}_accept_and_perform_as_specified_{req}"
  (!IsUndefined(prevProcs) & (prevProcs = {state}) & 
  !IsUndefined(prevProcReq.{m_req_type_field}) & (prevProcReq.{m_req_type_field} = {req})) ->   
    {m_proc_selc}.{m_proc_cl_field} = prevProcReq.cl;
'''

cores = [("", "")]
is_local_cc = ""
is_not_local_cc = ""
if design_cfg.get('dist_dir', False):
  assert (design_cfg.get('is_not_local_cc', "") != "" and  \
  design_cfg.get('is_local_cc', "") != "")
  is_local_cc = design_cfg.get('is_local_cc')
  is_not_local_cc = design_cfg.get('is_not_local_cc')
  cores = [("h", f"{is_local_cc}"), ("r", f"{is_not_local_cc}")]

def gen():
  s1resdirname = "build/s1_req_acc_state/_build"
  for scope, selc_cond in cores:
    postfix = f"_{scope}" if scope != "" else ""
    todo = []
    with open(f"{logfile}{postfix}", "w") as lg_f:
      with open(f"{s1resdirname}/res{postfix}.txt", "r") as f:
        st = False
        for ln in f:
          if ln.startswith("Reachable"):
            st = True
          elif ln.startswith("Unreachable"):
            st = False
          else:
            if st:
              todo.append(tuple(ln[:-1].split(",")))
              lg_f.write(ln)
    for t_ in todo:
      assert(len(t_) == 2)
      state, req = t_
      outff = f"{dirname}/{state}_{req}{postfix}.m"
      outff_h = open(outff, "w")

      parse_murphi_model(coh_model_file, nodes_iter_types, outff_h, {"track_req": True, "prevState": True, "past_1_prevState": True, "past_1_prevProcReq": True})

      ##os.system(f"cat {design_file} > {outff}")
      #os.system(f"cat /Users/yaohsiao/work/coh_syn_dev/murphi/protocols/fv/msi_fv_envs/msi.fvt.s2_acc_perf.m > {outff}")
      #with open(f"{outff}", "a") as f:
      outff_h.write(template.format(state=state, req=req, m_proc_state_field=m_proc_state_field, m_req_type_field=m_req_type_field, cond="" if scope == "" else f" & ({selc_cond})"))
      outff_h.close()

def gen_s1():
  resdirname = "build/s2_req_proc_state/_build"
  dirname = "build/s2_2_req_proc_state_to_state_prime_val/out"
  os.makedirs(dirname, exist_ok = True)  
  for scope, selc_cond in cores:
    postfix = f"_{scope}" if scope != "" else ""
    logfile_path = f"{logfile}{postfix}"
    if not os.path.exists(logfile_path):
      print(logfile_path, "not exist")
      continue
    resdirname_scope = f"{resdirname}"
    reachable = []
    unreachable = []
    with open(logfile_path, "r") as lg_f:
      for ln in lg_f:
        ln_ = ln[:-1].split(",")
        assert(len(ln_) == 2)
        state, req = ln_[0], ln_[1]
        resff = f"{resdirname_scope}/{state}_{req}{postfix}.txt"
        prop = f"{state}_accept_and_perform_{req}"
        ret = get_res_file(resff, prop, assertion=False, inline_prop=False)
        (ret2, t) = get_res_file_stats(resff, prop, assertion=False, inline_prop=False)
        if ret:
          reachable.append((state, req))
        else:
          unreachable.append((state, req))
    with open(f"{resdirname_scope}/res{postfix}.txt", "w") as f:
      f.write("Reachable (accept and perform)\n")
      for itm in reachable:
        f.write("%s,%s\n" % (itm[0], itm[1]))
      f.write("Unreachable (accept but init txn)\n")
      for itm in unreachable:
        f.write("%s,%s\n" % (itm[0], itm[1]))
    
    if scope == "h":
      # local-to-dir core
      dirname = "build/s2_local_core/out"
      os.makedirs(dirname, exist_ok = True)  
      for itm in reachable:
        state, req = itm 
        # we distinguish if its actual no transaction (w/ directory)
        




    with open(f"build/s1_2_transition/_build/transition{postfix}.pkl", 'rb') as f:
      transition_possible = pickle.load(f)
    for itm in reachable:
      state, req = itm
      for state_prime in all_cc_states:
        if state_prime == state:
          continue
        if not state_prime in transition_possible[state]:
          continue
        outff = f"{dirname}/{state}_{req}_{state_prime}{postfix}.m"
        outff_h = open(outff, "w")

        parse_murphi_model(coh_model_file, nodes_iter_types, outff_h, {"track_req": True, "prevState": True, "past_1_prevState": True, "past_1_prevProcReq": True})

        # # os.system(f"cat {design_file} > {outff}")
        # os.system(f"cat /Users/yaohsiao/work/coh_syn_dev/murphi/protocols/fv/msi_fv_envs/msi.fvt.s2_acc_perf.m > {outff}")
        # with open(f"{outff}", "a") as f:

        outff_h.write(c_template.format(state=state, req=req, m_proc_state_field=m_proc_state_field, m_req_type_field=m_req_type_field, state_prime=state_prime))
        outff_h.close()


      outff = f"{dirname}/{state}_{req}_val.m"
      outff_h = open(outff, "w")

      # os.system(f"cat /Users/yaohsiao/work/coh_syn_dev/murphi/protocols/fv/msi_fv_envs/msi.fvt.s2_acc_perf_vv.m > {outff}")
      parse_murphi_model(coh_model_file, nodes_iter_types, outff_h, {"track_req": True, "prevState": True, "past_1_prevState": True, "past_1_prevProcReq": True, "prevStateVal": True, "past_1_prevStateVal": True})
      outff_h.write(d_template.format(state=state, req=req, m_proc_state_field=m_proc_state_field, m_req_type_field=m_req_type_field, m_proc_cl_field=m_proc_cl_field))
      outff_h.close()

def gen_s2():
  with open("build/s1_2_transition/_build/transition.pkl", 'rb') as f:
    transition_possible = pickle.load(f)
  resdirname = "build/s2_req_proc_state/_build"
  if not os.path.exists(resdirname):
    sys.exit(0)
  todo = []
  with open(f"{resdirname}/res.txt", "r") as f:
    st = False
    for ln in f:
      if ln.startswith("Reachable"):
        st = True
      elif ln.startswith("Unreachable"):
        st = False
      else:
        if st:
          todo.append(tuple(ln[:-1].split(",")))
  curdirname = "build/s2_2_req_proc_state_to_state_prime_val/_build"
  reachable_s_req_s_prime = []
  unreachable_s_req_s_prime = []
  reachable_s_req_val_chg = []
  unreachable_s_req_val_chg = []
  for t_ in todo:
    assert(len(t_) == 2)
    state, req = t_
    resff = f"{curdirname}/{state}_{req}_val.txt"
    prop = f"{state}_accept_and_perform_{req}_value_change"
    ret = get_res_file(resff, prop, assertion=False, inline_prop=False)
    (ret2, t) = get_res_file_stats(resff, prop, assertion=False, inline_prop=False)
    if ret:
      # find failure 
      reachable_s_req_val_chg.append((state, req))
    else:
      unreachable_s_req_val_chg.append((state, req))
    for state_prime in all_cc_states:
      if state == state_prime:
        continue
      if not state_prime in transition_possible[state]:
        continue
      resff = f"{curdirname}/{state}_{req}_{state_prime}.txt"
      prop = f"{state}_accept_and_perform_{req}_change_to_{state_prime}"
      ret = get_res_file(resff, prop, assertion=False, inline_prop=False)
      (ret2, t) = get_res_file_stats(resff, prop, assertion=False, inline_prop=False)
      if ret:
        # find failure 
        reachable_s_req_s_prime.append((state, req, state_prime))
      else:
        unreachable_s_req_s_prime.append((state, req, state_prime))
      # print("->", state, req, state_prime, ret)
  with open(f"{curdirname}/res.txt", "w") as f:
    f.write("Reachable (accept and perform (i.e., without txn) and transition to new state)\n")
    for itm in reachable_s_req_s_prime:
      f.write(",".join(itm) + "\n")
    f.write("Unreachable (accept and perform (i.e., without txn) but no transition to new state)\n")
    for itm in unreachable_s_req_s_prime:
      f.write(",".join(itm) + "\n")
    f.write("Reachable (accept and perform (i.e., without txn) with value change possible\n")
    for itm in reachable_s_req_val_chg:
      f.write(",".join(itm) + "\n")
    f.write("Unreachable (accept and perform (i.e., without txn) with value change not possible\n")
    for itm in unreachable_s_req_val_chg:
      f.write(",".join(itm) + "\n")

  

  dirname = "build/s2_3_req_proc_val/out"
  os.makedirs(dirname, exist_ok = True)  
  for itm in reachable_s_req_val_chg:
    state, req = itm
    if not req in type_with_args:
      continue
    # 
    outff = f"{dirname}/{state}_{req}_val_req.m"
    outff_h = open(outff, "w")

    parse_murphi_model(coh_model_file, nodes_iter_types, outff_h, {"track_req": True, "prevState": True})
    #os.system(f"cat /Users/yaohsiao/work/coh_syn_dev/murphi/protocols/fv/msi_fv_envs/msi.fvt.s2_acc_perf.m > {outff}")
    #with open(f"{outff}", "a") as f:
    outff_h.write(e_template.format(state=state, req=req, m_proc_state_field=m_proc_state_field, m_req_type_field=m_req_type_field, m_proc_cl_field=m_proc_cl_field, m_proc_selc=m_proc_selc))

def pp():
  curdirname = "build/s2_2_req_proc_state_to_state_prime_val/_build"
  todo = []
  with open(f"{curdirname}/res.txt", "r") as f:
    st = False
    for ln in f:
      if ln.startswith("Reachable") and "value" in ln:
        st = True
      elif ln.startswith("Unreachable") and "value" in ln:
        st = False
      else:
        if st:
          todo.append(tuple(ln[:-1].split(",")))
  dirname = "build/s2_3_req_proc_val/_build"
  proven = []
  disproven = []
  for t_ in todo:
    assert(len(t_) == 2)
    state, req = t_
    resff = f"{dirname}/{state}_{req}_val_req.txt"
    prop = "{state}_accept_and_perform_as_specified_{req}"
    ret = get_res_file(resff, prop, assertion=True, inline_prop=False)
    (ret2, t) = get_res_file_stats(resff, prop, assertion=True, inline_prop=False)
    if ret:
      proven.append((state, req))
    else:
      # assertion pass failure 
      disproven.append((state, req))
  print(proven)
  with open(f"{dirname}/res.txt", "w") as f:
    f.write("Proven (accept and perform (i.e., without txn) with value updated as request specified always) (could be bounded..)\n")
    for itm in proven:
      f.write(",".join(itm) + "\n")
    f.write("Disproven\n")
    for itm in disproven:
      f.write(",".join(itm) + "\n")
  

import fire
if __name__ == "__main__":
  fire.Fire()
  dump_stats()
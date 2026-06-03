# what input request 
# At what {hstate} does HOME take in what {msgType}, and initiate or not initiate transaction 

# (hstate, mtype):
#   hstate_prime: 
#     - 'precondition': str (precondition for such change to hstate_prime)
#     - 'val_change': bool
#     - 'val_eq_mtype_cl': bool
#     - 'owner_change': bool
#     - 'send_msg_sets': [{msg_type: (cnt, dst equal to mtype.src, dst not equal to mtype.src)}]
#     - 'sharer_change': bool
#     - 'sharer_change_detail': [empty/all/add_one/decr_one/, .. ]
# 
import fire
import sys
sys.path.append("src")
from gconst import * 
import pickle
import subprocess
import os 
import re
import argparse
from pprint import pprint
from collections import OrderedDict
from util import *
from home_templates import *
from s1 import find_all_simple_paths
import copy
import itertools
from code_gen.parse_rules import *

tardir=build_dir
with open("build/s1_3_global_msg/_build/aggdict.pkl", "rb") as f:
  g_msg_dir = pickle.load(f)
dst_always_defined = g_msg_dir['dst_always_defined']
assert(dst_always_defined)

transition = '''
invariant "{state}_to_{state_prime}"
  (!IsUndefined(prevHomeNode) & (prevHomeNode = {state})) ->
  !({m_home_cur}.{m_home_state_field} = {state_prime});
'''
def gen(): 
  stepname="home_s1_req_acc_state"
  dirname = f"build/{stepname}/out"
  os.makedirs(dirname, exist_ok = True)  
  # TODO: no message in coming and still transition
  for hstate in all_llc_states:
    for mtype in all_msg_types:
      if not (g_msg_dir[mtype][f'from_{m_proc_iter_type}_to_{m_home_iter_type}']):
        # home doesn't receives this message type 
        continue
      outff = f"{dirname}/{hstate}_{mtype}.m"
      outff_h = open(outff, "w")
      obs_s = f"if (!isundefined(cur_node) & cur_node = selh) then\n prevRecProcMsg := {{msg_var}}.{m_msg_type_field};\n endif;\n"
      parse_murphi_model(coh_model_file, nodes_iter_types, outff_h, {"cur_node": True, "RECEIVING": obs_s, "g_msg": False, "home": True}, additional_var={"prevRecProcMsg": (msg_type_name, "undefine prevRecProcMsg;\n", "undefine prevRecProcMsg;\n")})
      outff_h.write(dir_h_accept_template.format(mtype=mtype, m_proc_state_field=m_proc_state_field, m_msg_type_field=m_msg_type_field, hstate = hstate))
      outff_h.close()

  stepname="home_s0_transition"
  dirname = f"build/{stepname}/out"
  os.makedirs(dirname, exist_ok = True)  
  for hstate in all_llc_states:
    for hstate_prime in all_llc_states:
      if hstate == hstate_prime:
        continue
      outff = f"{dirname}/{hstate}_{hstate_prime}.m"
      outff_h = open(outff, "w")
      parse_murphi_model(coh_model_file, nodes_iter_types, outff_h, {"cur_node": True, "home": True})
      outff_h.write(transition.format(state=hstate,m_home_cur=m_home_cur, m_home_state_field=m_home_state_field, state_prime=hstate_prime))
      outff_h.close()

def prepare_header(outff_h, rec_cond="", sending_book_keep_s="", var_ = {}, extra_cfg=None):
  rec_s = f"if (!isundefined(cur_node) & cur_node = selh) then\n prevRecProcMsg := {{msg_var}}.{m_msg_type_field};\n {rec_cond};\n endif;\n" 

  additional_var = {"prevRecProcMsg": (msg_type_name, "undefine prevRecProcMsg;\n", "undefine prevRecProcMsg;\n")} 
  for k, v in var_.items():
    assert(not k in additional_var)
    additional_var[k] = v

  cfg = {"cur_node": True, "RECEIVING": rec_s, "g_msg": False, "home": True}

  if extra_cfg is not None:
    for k, v in extra_cfg.items():
      cfg[k] = v

  if sending_book_keep_s != "":
    cfg['SENDING'] = sending_book_keep_s

  parse_murphi_model(coh_model_file, nodes_iter_types, outff_h, cfg, additional_var=additional_var)


def gen_s1():
  # home_s0
  home_transition = {}
  edges = []
  stepname="home_s0_transition"
  dirname = f"build/{stepname}/_build"
  for hstate in all_llc_states:
    for hstate_prime in all_llc_states:
      if hstate == hstate_prime:
        continue
      resff = f"{dirname}/{hstate}_{hstate_prime}.txt"  
      print(resff)
      transition = get_res_file(resff, f"{hstate}_to_{hstate_prime}")
      if transition:
        edges.append((hstate, hstate_prime))
        if not hstate in home_transition:
          home_transition[hstate] = []
        home_transition[hstate].append(hstate_prime)
  with open(f"{dirname}/home_transition.pkl", "wb") as f:
    pickle.dump(home_transition, f)

  # home_s1
  aggregate = OrderedDict()
  stepname="home_s1_req_acc_state"
  dirname = f"build/{stepname}/_build"
  for hstate in all_llc_states:
    for mtype in all_msg_types:
      if not (g_msg_dir[mtype][f'from_{m_proc_iter_type}_to_{m_home_iter_type}']):
        # home doesn't receives this message type 
        continue
      resff = f"{dirname}/{hstate}_{mtype}.txt"
      hstate_possible = get_res_file(resff, f"{hstate}_consistent_w_{mtype}")
      if hstate_possible:
        print(" possible -->", hstate, mtype)
        aggregate[(hstate, mtype)] = OrderedDict()

        assert(dst_always_defined)
        aggregate[(hstate, mtype)]['proc'] = True
      else:
        print("X impossible", hstate, mtype)
    
  with open(f"{dirname}/aggdict.pkl", "wb") as f: # 'wb' for write binary
    pickle.dump(aggregate, f)

  # (hstate, mtype)
  #   new picl needed or not
  #    (coherence_state, owner, sharer_list, value)
  #     change or  not: home_s2_req_acc_proc_state
  #     not change, owner change or not, sharere list change or not, value chagne or not: home_s3_req_acc_aux
  stepname="home_s2_req_acc_proc_state"
  dirname = f"build/{stepname}/out"
  os.makedirs(dirname, exist_ok = True)  
  
 
  # potentialliy txn
  # 1) we collect all possible transitions including change state or not
  for k, v in aggregate.items():
    hstate, mtype = k
    # {hstate} takes in {mtype} 
    # we see msg.src condition 
    # a) hstate owner be defined
    if m_home_owner_field is not None: 
      outff = f"{dirname}/{hstate}_{mtype}_owner_def.m"
      outff_h = open(outff, "w")
      prepare_header(outff_h, rec_cond="", var_={"prevHomeNodeOnwer": (nodes_iter_types[0], "undefine prevHomeNodeOnwer;\n", f"prevHomeNodeOnwer := {m_home_cur}.{m_home_owner_field};\n")})
      # prepare_header(outff_h, dec_s=f"prevHomeNodeOnwer: {nodes_iter_types[0]};\n", init_state_s="undefine prevHomeNodeOnwer;\n", book_keep_s=f"prevHomeNodeOnwer := {m_home_cur}.{m_home_owner_field};\n") 
      # **can owner be undefeined?**
      outff_h.write(dir_h_accept_owner_def_template.format(mtype=mtype,hstate=hstate))
      outff_h.close()

    # b) sharer list non empty 
    # can sharer list be empty? 
    if m_home_sharer_field is not None:
      outff = f"{dirname}/{hstate}_{mtype}_sharer_list_empty.m"
      outff_h = open(outff, "w")
      prepare_header(outff_h, rec_cond="", var_={"non_empty_sharer": ("boolean", "", f"non_empty_sharer := (multisetcount(i:{m_home_cur}.{m_home_sharer_field}, true) = 0);\n")})
      outff_h.write(dir_h_accept_nonempty_sharer_emplate.format(mtype=mtype,hstate=hstate))
      outff_h.close()

      # b.2) sharer list non empty 
      # can sharer list be non_empty? 
      outff = f"{dirname}/{hstate}_{mtype}_sharer_list_non_empty.m"
      outff_h = open(outff, "w")
      prepare_header(outff_h, rec_cond="", var_={"non_empty_sharer": ("boolean", "", f"non_empty_sharer := (multisetcount(i:{m_home_cur}.{m_home_sharer_field}, true) > 0);\n")})
      outff_h.write(dir_h_accept_nonempty_sharer_emplate.format(mtype=mtype,hstate=hstate))
      outff_h.close()

    # c) transitions to new coherence state? 
    for hstate_prime in [hstate] + home_transition[hstate]:
      outff = f"{dirname}/{hstate}_{mtype}_{hstate_prime}.m"
      outff_h = open(outff, "w")
      prepare_header(outff_h, rec_cond="", var_={})
      outff_h.write(dir_h_accept_trans_template.format(mtype=mtype, hstate=hstate, m_home_cur=m_home_cur,m_home_state_field=m_home_state_field,hstate_prime=hstate_prime))
      outff_h.close()

  
def gen_s1_2():
  with open(f"build/home_s0_transition/_build/home_transition.pkl", "rb") as f:
    home_transition = pickle.load(f)

  with open("build/home_s1_req_acc_state/_build/aggdict.pkl", "rb") as f:
    aggregate = pickle.load(f)

  for k, v in aggregate.items():
    hstate, mtype = k
    v['imm_picl'] = []
    # we check whether {hstate} take in {mtype} 
    # a) transition to ? 
    for hstate_prime in [hstate] + home_transition[hstate]:
      resff = f"build/home_s2_req_acc_proc_state/_build/{hstate}_{mtype}_{hstate_prime}.txt"
      r = get_res_file(resff, f"{hstate}_accept_req_{mtype}")
      # print("->", hstate, mtype, hstate_prime, r)
      if r:
        # tmpval = OrderedDict()
        # tmpval['imm_picl'] = hstate_prime
        v['imm_picl'].append(hstate_prime) #tmpval)
    
    if m_home_owner_field is not None:
      resff = f"build/home_s2_req_acc_proc_state/_build/{hstate}_{mtype}_owner_def.txt"
      r = get_res_file(resff, f"{hstate}_accept_req_{mtype}")
      print("===> res ff ", resff, hstate, mtype, r)
      # true if owner can be undefined
      v['owner_aws_defined'] = not (r)
    if m_home_sharer_field is not None:
      resff = f"build/home_s2_req_acc_proc_state/_build/{hstate}_{mtype}_sharer_list_empty.txt"
      r = get_res_file(resff, f"{hstate}_accept_req_{mtype}")
      v['sharer_can_be_empty'] = r
      resff = f"build/home_s2_req_acc_proc_state/_build/{hstate}_{mtype}_sharer_list_non_empty.txt"
      r = get_res_file(resff, f"{hstate}_accept_req_{mtype}")
      v['sharer_can_be_non_empty'] = r

    aggregate[k] = v

    print("-->", k, v)


  with open("build/home_s2_req_acc_proc_state/_build/agg_raw.pkl", "wb") as f:
    pickle.dump(aggregate, f)

  stepname="home_s3_req_acc_msg_src_cond"
  dirname = f"build/{stepname}/out"
  os.makedirs(dirname, exist_ok = True)  
  
  for k, v in aggregate.items():
    hstate, mtype = k
    assert(len(v['imm_picl']) > 0)
    if not len(v['imm_picl']) > 1:
      continue
    print("=> processing: ", hstate, mtype, v['imm_picl'], 'owner_always_defined (i.e., true implies possibility as a function of owner or not): ', v['owner_aws_defined'], 'empty sharer?', v['sharer_can_be_empty'], 'non-empty sharere?', v['sharer_can_be_non_empty'])

    if v['owner_aws_defined']: 
      # redo transitions checks with the preconditoin
      for hstate_prime in v['imm_picl']:
        # for more than two possibilities we  
        # b) can hstate mtype transition to hstate_prime with  can the inmsg src same as owner 
        outff = f"{dirname}/{hstate}_{mtype}_{hstate_prime}_src_owner.m"
        outff_h = open(outff, "w")
        prepare_header(outff_h, rec_cond=f"prevRecProcMsgSrc := {{msg_var}}.{m_msg_src_field}", var_={ "prevHomeNodeOnwer": (nodes_iter_types[0], "undefine prevHomeNodeOnwer;\n", f"prevHomeNodeOnwer := {m_home_cur}.{m_home_owner_field};\n"), "prevRecProcMsgSrc": (nodes_iter_types[0], "undefine prevRecProcMsgSrc;\n", "")})
        # prepare_header(outff_h, dec_s=f"prevHomeNodeOnwer: {m_machine_iter_type};\n prevRecProcMsgSrc: {m_machine_iter_type};\n", init_state_s="undefine prevHomeNodeOnwer;\n undefine prevRecProcMsgSrc;\n", book_keep_s=f"prevHomeNodeOnwer := {m_home_cur}.{m_home_owner_field};\n", rec_cond=f"prevRecProcMsgSrc := {{msg_var}}.{m_msg_src_field}") 
        outff_h.write(dir_h_accept_owner_src_template.format(mtype=mtype,hstate=hstate, is_owner="=",hstate_prime=hstate_prime,m_home_cur=m_home_cur,m_home_state_field=m_home_state_field))
        outff_h.close()

        # c) can the inmsg src not same as owner
        outff = f"{dirname}/{hstate}_{mtype}_{hstate_prime}_src_not_owner.m"
        outff_h = open(outff, "w")
        prepare_header(outff_h, rec_cond=f"prevRecProcMsgSrc := {{msg_var}}.{m_msg_src_field}", var_={ "prevHomeNodeOnwer": (nodes_iter_types[0], "undefine prevHomeNodeOnwer;\n", f"prevHomeNodeOnwer := {m_home_cur}.{m_home_owner_field};\n"), "prevRecProcMsgSrc": (nodes_iter_types[0], "undefine prevRecProcMsgSrc;\n", "")})
        # prepare_header(outff_h, dec_s=f"prevHomeNodeOnwer: {m_machine_iter_type};\n prevRecProcMsgSrc: {m_machine_iter_type};\n", init_state_s="undefine prevHomeNodeOnwer;\n undefine prevRecProcMsgSrc;\n", book_keep_s=f"prevHomeNodeOnwer := {m_home_cur}.{m_home_owner_field};\n", rec_cond=f"prevRecProcMsgSrc := {{msg_var}}.{m_msg_src_field}") 
        outff_h.write(dir_h_accept_owner_src_template.format(mtype=mtype,hstate=hstate, is_owner="!=",hstate_prime=hstate_prime,m_home_cur=m_home_cur,m_home_state_field=m_home_state_field))
        outff_h.close()

    if v['sharer_can_be_non_empty'] and v['sharer_can_be_empty']:
      for hstate_prime in v['imm_picl']:
        # d) can the inmsg src be not the last sharer: i.e., sharer list is greater than 1 OR the sharer be empty 
        outff = f"{dirname}/{hstate}_{mtype}_{hstate_prime}_src_not_last_sharer_nonempty.m"
        outff_h = open(outff, "w")
        prepare_header(outff_h, rec_cond=f"src_last_sharer := !isundefined(prevSharer) & prevSharer = {{msg_var}}.{m_msg_src_field};\n", var_={ "src_last_sharer": ("boolean", "", f""), 
        "prevSharer": (m_proc_iter_type, "", f"undefine prevSharer;\nif (multisetcount(i:{m_home_cur}.{m_home_sharer_field}, true) = 1) then for t: {m_proc_iter_type} do if (multisetcount(i:{m_home_cur}.{m_home_sharer_field}, {m_home_cur}.{m_home_sharer_field}[i] = t) = 1) then  prevSharer := t;\n endif; endfor;\n endif;\n"), 
        "nonempty": ("boolean", "", f"nonempty := (multisetcount(i:{m_home_cur}.{m_home_sharer_field}, true) > 0);\n")})
        # prepare_header(outff_h, dec_s=f"src_last_sharer: boolean; prevSharer: {m_proc_iter_type};\n nonempty: boolean;\n", init_state_s="", book_keep_s=f"nonempty := (multisetcount(i:{m_home_cur}.{m_home_sharer_field}, true) > 0);\n undefine prevSharer;\n if (multisetcount(i:{m_home_cur}.{m_home_sharer_field}, true) = 1) then for t: {m_proc_iter_type} do if (multisetcount(i:{m_home_cur}.{m_home_sharer_field}, {m_home_cur}.{m_home_sharer_field}[i] = t) = 1) then  prevSharer := t;\n endif; endfor;\n endif;\n", rec_cond=f"src_last_sharer := !isundefined(prevSharer) & prevSharer = {{msg_var}}.{m_msg_src_field};\n")
        outff_h.write(dir_h_accept_sharer_src_template.format(mtype=mtype,hstate=hstate, is_last="!", hstate_prime=hstate_prime,m_home_cur=m_home_cur,m_home_state_field=m_home_state_field, aux_cond="nonempty & "))
        outff_h.close()

        outff = f"{dirname}/{hstate}_{mtype}_{hstate_prime}_src_not_last_sharer_empty.m"
        outff_h = open(outff, "w")
        prepare_header(outff_h, rec_cond=f"src_last_sharer := !isundefined(prevSharer) & prevSharer = {{msg_var}}.{m_msg_src_field};\n", var_={ "src_last_sharer": ("boolean", "", f""), 
        "prevSharer": (m_proc_iter_type, "", f"undefine prevSharer;\nif (multisetcount(i:{m_home_cur}.{m_home_sharer_field}, true) = 1) then for t: {m_proc_iter_type} do if (multisetcount(i:{m_home_cur}.{m_home_sharer_field}, {m_home_cur}.{m_home_sharer_field}[i] = t) = 1) then  prevSharer := t;\n endif; endfor;\n endif;\n"), 
        "nonempty": ("boolean", "", f"nonempty := (multisetcount(i:{m_home_cur}.{m_home_sharer_field}, true) > 0);\n")})

        # prepare_header(outff_h, dec_s=f"src_last_sharer: boolean; prevSharer: {m_proc_iter_type};\n nonempty: boolean;\n", init_state_s="", book_keep_s=f"nonempty := (multisetcount(i:{m_home_cur}.{m_home_sharer_field}, true) > 0);\n undefine prevSharer;\n if (multisetcount(i:{m_home_cur}.{m_home_sharer_field}, true) = 1) then for t: {m_proc_iter_type} do if (multisetcount(i:{m_home_cur}.{m_home_sharer_field}, {m_home_cur}.{m_home_sharer_field}[i] = t) = 1) then  prevSharer := t;\n endif; endfor;\n endif;\n", rec_cond=f"src_last_sharer := !isundefined(prevSharer) & prevSharer = {{msg_var}}.{m_msg_src_field};\n")
        outff_h.write(dir_h_accept_sharer_src_template.format(mtype=mtype,hstate=hstate, is_last="!", hstate_prime=hstate_prime,m_home_cur=m_home_cur,m_home_state_field=m_home_state_field, aux_cond="!nonempty & "))
        outff_h.close()

        # e) cam the inmsg src be the last sharer 
        outff = f"{dirname}/{hstate}_{mtype}_{hstate_prime}_src_last_sharer.m"
        outff_h = open(outff, "w")
        prepare_header(outff_h, rec_cond=f"src_last_sharer := !isundefined(prevSharer) & prevSharer = {{msg_var}}.{m_msg_src_field};\n", var_={ "src_last_sharer": ("boolean", "", f""), 
        "prevSharer": (m_proc_iter_type, "", f"undefine prevSharer;\nif (multisetcount(i:{m_home_cur}.{m_home_sharer_field}, true) = 1) then for t: {m_proc_iter_type} do if (multisetcount(i:{m_home_cur}.{m_home_sharer_field}, {m_home_cur}.{m_home_sharer_field}[i] = t) = 1) then  prevSharer := t;\n endif; endfor;\n endif;\n"), 
        "nonempty": ("boolean", "", f"nonempty := (multisetcount(i:{m_home_cur}.{m_home_sharer_field}, true) > 0);\n")})

        # prepare_header(outff_h, dec_s=f"src_last_sharer: boolean; prevSharer: {m_proc_iter_type};\n \n", init_state_s="", book_keep_s=f"undefine prevSharer;\n if (multisetcount(i:{m_home_cur}.{m_home_sharer_field}, true) = 1) then for t: {m_proc_iter_type} do if (multisetcount(i:{m_home_cur}.{m_home_sharer_field}, {m_home_cur}.{m_home_sharer_field}[i] = t) = 1) then  prevSharer := t;\n endif; endfor;\n endif;\n", rec_cond=f"src_last_sharer := !isundefined(prevSharer) & prevSharer = {{msg_var}}.{m_msg_src_field};\n")
        outff_h.write(dir_h_accept_sharer_src_template.format(mtype=mtype,hstate=hstate, is_last="", hstate_prime=hstate_prime,m_home_cur=m_home_cur,m_home_state_field=m_home_state_field, aux_cond=""))
        outff_h.close()

  stepname="home_s3_msg_out_val_sharere_owner"
  dirname = f"build/{stepname}/out"
  os.makedirs(dirname, exist_ok = True)  
   
   
  for k, v in aggregate.items():
    hstate, mtype = k
    for hstate_prime in v['imm_picl']: 
      # a) value change?
      outff = f"{dirname}/{hstate}_{mtype}_{hstate_prime}_val.m"
      outff_h = open(outff, "w")

      var_ = {"prevHomeNodeVal": (m_val_type_name, "", f"prevHomeNodeVal := {m_home_cur}.{m_home_cl_field};\n")}
      prepare_header(outff_h, rec_cond="", var_=var_)
      # prepare_header(outff_h, dec_s=f"prevHomeNodeVal: {m_val_type_name};\n", book_keep_s=f"prevHomeNodeVal := {m_home_cur}.{m_home_cl_field};\n")
      outff_h.write(dir_h_accept_trans_val_template.format(mtype=mtype, hstate=hstate, m_home_cur=m_home_cur,m_home_state_field=m_home_state_field,hstate_prime=hstate_prime, m_home_cl_field=m_home_cl_field))
      outff_h.close()
      # b) sharer list change
      outff = f"{dirname}/{hstate}_{mtype}_{hstate_prime}_sharere.m"
      outff_h = open(outff, "w")
      var_ = {"prev_sharer": (f"array [{m_proc_iter_type}] of boolean", f"for m: {m_proc_iter_type} do prev_sharer[m] := false; endfor;\n", f"for m: {m_proc_iter_type} do prev_sharer[m] := (multisetcount(i:{m_home_cur}.{m_home_sharer_field}, {m_home_cur}.{m_home_sharer_field}[i] = m) > 0); endfor;\n")}
      prepare_header(outff_h, rec_cond="", var_=var_)
      # prepare_header(outff_h, dec_s=f"prev_sharer: array [{m_proc_iter_type}] of boolean;\n", init_state_s=f"for m: {m_proc_iter_type} do prev_sharer[m] := false; endfor;\n", book_keep_s=f"for m: {m_proc_iter_type} do prev_sharer[m] := (multisetcount(i:{m_home_cur}.{m_home_sharer_field}, {m_home_cur}.{m_home_sharer_field}[i] = m) > 0); endfor;\n", rec_cond="") 
      outff_h.write(dir_h_accept_trans_sharers_template.format(mtype=mtype, hstate=hstate, m_home_cur=m_home_cur,m_home_state_field=m_home_state_field,hstate_prime=hstate_prime, m_home_cl_field=m_home_cl_field, m_home_sharer_field=m_home_sharer_field, m_proc_iter_type=m_proc_iter_type))
      outff_h.close()

      # c) owner change
      outff = f"{dirname}/{hstate}_{mtype}_{hstate_prime}_onwer.m"
      outff_h = open(outff, "w")

      var_ = {"prevHomeNodeOnwer": (nodes_iter_types[0], "undefine prevHomeNodeOnwer;\n", f"prevHomeNodeOnwer := {m_home_cur}.{m_home_owner_field};\n")}
      prepare_header(outff_h, rec_cond="", var_=var_)

      # prepare_header(outff_h, dec_s=f"prevHomeNodeOnwer: {m_machine_iter_type};\n", init_state_s="undefine prevHomeNodeOnwer;\n", book_keep_s=f"prevHomeNodeOnwer := {m_home_cur}.{m_home_owner_field};\n") 
      outff_h.write(dir_h_accept_trans_owner_template.format(mtype=mtype, hstate=hstate, m_home_cur=m_home_cur,m_home_state_field=m_home_state_field,hstate_prime=hstate_prime, m_home_cl_field=m_home_cl_field, m_home_owner_field=m_home_owner_field))
      outff_h.close()
      # d) sent messages to request source, owner, sharer list - requester, sharer list, or all cores 
      # get trace only at this step msg sending per hstate, mtype, hstate_prime
      outff = f"{dirname}/{hstate}_{mtype}_{hstate_prime}.m"
      outff_h = open(outff, "w")

      var_ = {"prevSentMsgSet": (f"array [{msg_type_name}] of boolean", f"for m: {msg_type_name} do\n prevSentMsgSet[m]:= false;\n endfor;\n", f"for m: {msg_type_name} do\n prevSentMsgSet[m]:= false;\n endfor;\n")}
      prepare_header(outff_h, rec_cond="", sending_book_keep_s=f"if (!isundefined(cur_node) & cur_node = selh) then\n prevSentMsgSet[{{msg_var}}.{m_msg_type_field}]:= true; endif;\n", var_=var_)
      # prepare_header(outff_h, dec_s=f"prevSentMsg: array [{msg_type_name}] of boolean;\n", init_state_s=f"for m: {msg_type_name} do\n prevSentMsg[m]:= false;\n endfor;\n", book_keep_s=f"for m: {msg_type_name} do\n prevSentMsg[m]:= false;\n endfor;\n", rec_cond="", sending_book_keep_s=f"if (!isundefined(cur_node) & cur_node = selh) then\n prevSentMsg[{{msg_var}}.{m_msg_type_field}]:= true; endif;\n")
      outff_h.write(dir_h_accept_trans_template.format(mtype=mtype, hstate=hstate, m_home_cur=m_home_cur,m_home_state_field=m_home_state_field,hstate_prime=hstate_prime))
      outff_h.close()

def gen_s2():
  with open(f"build/home_s0_transition/_build/home_transition.pkl", "rb") as f:
    home_transition = pickle.load(f)
  with open("build/home_s2_req_acc_proc_state/_build/agg_raw.pkl", "rb") as f:
    aggregate = pickle.load(f)

  aggregate_prime = OrderedDict()
  stepname = "home_s3_msg_out_set"
  dirname=f"build/{stepname}/out/"
  os.makedirs(dirname, exist_ok = True)  
  for k, v in aggregate.items():
    hstate, mtype = k
    
    v['transition_info'] = OrderedDict()
    for hstate_prime in v['imm_picl']: 
      cur = OrderedDict()
      print("--->", hstate, mtype, hstate_prime)
      resff = f"build/home_s3_msg_out_val_sharere_owner/_build/{hstate}_{mtype}_{hstate_prime}_val.txt"
      r = get_res_file(resff, f"{hstate}_accept_req_{mtype}")
      # print("\t valuage change ever? ", r)
      cur['val_change'] = r
      resff = f"build/home_s3_msg_out_val_sharere_owner/_build/{hstate}_{mtype}_{hstate_prime}_sharere.txt"
      r = get_res_file(resff, f"{hstate}_accept_req_{mtype}")
      #print("\t sharere change ever? ", r)
      cur['sharer_chage'] = r
      resff = f"build/home_s3_msg_out_val_sharere_owner/_build/{hstate}_{mtype}_{hstate_prime}_onwer.txt"
      r = get_res_file(resff, f"{hstate}_accept_req_{mtype}")
      cur['owner_change'] = r
      # print("\t owner change ever? ", r)
      v['transition_info'][hstate_prime] = cur 

      # iteratively find the sentMsg associated with the 
      # the same set of picl with same set of received message may have the different sent msg depending on the source of core
      resff = f"build/home_s3_msg_out_val_sharere_owner/_build/{hstate}_{mtype}_{hstate_prime}.txt"
      # ret = get_last_state(resff, "prevSentMsgSet", arr=True)
      # print("\t sent msg potential:", [k for k, v in ret.items() if v == 'true'])

      outff = f"{dirname}/{hstate}_{mtype}_{hstate_prime}_iter.py"
      outff_h = open(outff, "w")
      outff_h.write(f"stepname = \"{stepname}\"\n")
      outff_h.write(f"hstate = \"{hstate}\"\n")
      outff_h.write(f"mtype = \"{mtype}\"\n")
      outff_h.write(f"m_home_cur = \"{m_home_cur}\"\n")
      outff_h.write(f"m_home_state_field = \"{m_home_state_field}\"\n")
      outff_h.write(f"hstate_prime = \"{hstate_prime}\"\n")
      outff_h.write(f"tardir = \"{tardir}\"\n")
      with open("src/home_upath_dir_sent_iter.py", "r") as f:
        for ln in f:
          outff_h.write(ln)
      outff_h.close()

      outff = f"{dirname}/{hstate}_{mtype}_{hstate_prime}_baseff.m"
      outff_h = open(outff, "w")
      var_ = {"prevSentMsgSet": (f"array [{msg_type_name}] of boolean", f"for m: {msg_type_name} do\n prevSentMsgSet[m]:= false;\n endfor;\n", f"for m: {msg_type_name} do\n prevSentMsgSet[m]:= false;\n endfor;\n")}
      prepare_header(outff_h, rec_cond="", sending_book_keep_s=f"if (!isundefined(cur_node) & cur_node = selh) then\n prevSentMsgSet[{{msg_var}}.{m_msg_type_field}]:= true; endif;\n", var_=var_)
      #prepare_header(outff_h, dec_s=f"prevSentMsgSet: array [{msg_type_name}] of boolean;\n", init_state_s=f"for m: {msg_type_name} do\n prevSentMsgSet[m]:= false;\n endfor;\n", book_keep_s=f"for m: {msg_type_name} do\n prevSentMsgSet[m]:= false;\n endfor;\n", rec_cond="", sending_book_keep_s=f"if (!isundefined(cur_node) & cur_node = selh) then\n prevSentMsgSet[{{msg_var}}.{m_msg_type_field}]:= true; endif;\n")

      # sent_msg_ss = []
      # for mtype_, val_ in ret.items():
      #   sent_msg_ss.append(f"prevSentMsgSet[{mtype_}] = {val_}")
      outff_h.close()
    aggregate_prime[k] = v

  with open("build/home_s3_msg_out_val_sharere_owner/_build/agg_raw.pkl", "wb") as f:
    pickle.dump(aggregate_prime, f)

  # for those picl set,  a) change value, b) change owner, c) change sharer we go on to see how the change?
  stepname="home_s3_src_owner_sharere_extract"
  dirname = f"build/{stepname}/out"
  os.makedirs(dirname, exist_ok = True)  

  for k, v in aggregate_prime.items():
    hstate, mtype = k 
    for hstate_prime, cur in v['transition_info'].items():
      if cur['val_change']:
        # assert incoming message to be the message value field 
        outff = f"{dirname}/{hstate}_{mtype}_{hstate_prime}_val.m"
        outff_h = open(outff, "w")

        var_ = {"prevHomeNodeVal": (m_val_type_name, "", f"prevHomeNodeVal := {m_home_cur}.{m_home_cl_field};\n"), "prevRecProcMsgVal": (m_val_type_name, "","")}
        prepare_header(outff_h, rec_cond=f"prevRecProcMsgVal := {{msg_var}}.{m_msg_cl_field};\n", sending_book_keep_s="", var_=var_)

        # prepare_header(outff_h, dec_s=f"prevHomeNodeVal: {m_val_type_name};\n prevRecProcMsgVal: {m_val_type_name};\n", book_keep_s=f"prevHomeNodeVal := {m_home_cur}.{m_home_cl_field};\n", )
        outff_h.write(dir_h_val_change_src_template.format(mtype=mtype, hstate=hstate, m_home_cur=m_home_cur,m_home_state_field=m_home_state_field,hstate_prime=hstate_prime, m_home_cl_field=m_home_cl_field))
        outff_h.close()


      if cur['owner_change']:
        # we assert its always the requester otherwise we don't know..
        outff = f"{dirname}/{hstate}_{mtype}_{hstate_prime}_assert_src_as_owner.m"
        outff_h = open(outff, "w")
        prepare_header(outff_h, rec_cond=f"prevRecProcMsgSrc := {{msg_var}}.{m_msg_src_field}", var_={ "prevHomeNodeOnwer": (nodes_iter_types[0], "undefine prevHomeNodeOnwer;\n", f"prevHomeNodeOnwer := {m_home_cur}.{m_home_owner_field};\n"), "prevRecProcMsgSrc": (nodes_iter_types[0], "undefine prevRecProcMsgSrc;\n", "")})
        outff_h.write(dir_h_assert_owner_src_template.format(mtype=mtype,hstate=hstate, is_owner="=",hstate_prime=hstate_prime,m_home_cur=m_home_cur,m_home_state_field=m_home_state_field, m_home_owner_field=m_home_owner_field))
        outff_h.close()
      
      if cur['sharer_chage']:
        # owner is added to the sharere list 
        # 
        # resff = f"build/home_s3_msg_out_val_sharere_owner/_build/{hstate}_{mtype}_{hstate_prime}_sharere.txt"
        
        # # # is it empty in the trace: 
        # multiset_sharer = get_resff_multiset(resff, f"{m_home_cur}.{m_home_sharer_field}")
        
        # Assertion 1: src is included in the sharer list after transition
        outff = f"{dirname}/{hstate}_{mtype}_{hstate_prime}_src_added_to_sharer.m"
        outff_h = open(outff, "w")
        var_ = {
          "prev_sharer": (f"array [{m_proc_iter_type}] of boolean", f"for m: {m_proc_iter_type} do prev_sharer[m] := false; endfor;\n", f"for m: {m_proc_iter_type} do prev_sharer[m] := (multisetcount(i:{m_home_cur}.{m_home_sharer_field}, {m_home_cur}.{m_home_sharer_field}[i] = m) > 0); endfor;\n"),
          "prevRecProcMsgSrc": (nodes_iter_types[0], "undefine prevRecProcMsgSrc;\n", "")
        }
        prepare_header(outff_h, rec_cond=f"prevRecProcMsgSrc := {{msg_var}}.{m_msg_src_field};", var_=var_)
        prop = f'''invariant \"{hstate}_{mtype}_{hstate_prime}_src_added_to_sharer\"
              (!isundefined(prevHomeNode) & prevHomeNode = {hstate} & 
              !isundefined(prevRecProcMsg) & prevRecProcMsg = {mtype} & 
              {m_home_cur}.{m_home_state_field} = {hstate_prime}) ->
              (
              !prev_sharer[prevRecProcMsgSrc] & (multisetcount(i:{m_home_cur}.{m_home_sharer_field}, {m_home_cur}.{m_home_sharer_field}[i] = prevRecProcMsgSrc) > 0));'''
                # f"  (!IsUndefined(prevHomeNode) & (prevHomeNode = {hstate}) & !IsUndefined(prevRecProcMsgSrc)) ->\n"
                # f"  !(forall i:{m_proc_iter_type} do (i = prevRecProcMsgSrc & {m_home_cur}.{m_home_state_field} = {hstate_prime}) -> (multisetcount(j:{m_home_cur}.{m_home_sharer_field}, {m_home_cur}.{m_home_sharer_field}[j] = i) > 0) endforall);\n")
        outff_h.write(prop) 
        outff_h.close()

        # Assertion 2: sharer list is empty after transition
        outff = f"{dirname}/{hstate}_{mtype}_{hstate_prime}_sharer_list_empty.m"
        outff_h = open(outff, "w")
        prepare_header(outff_h, rec_cond="", var_=var_)
        prop = f'''invariant \"{hstate}_{mtype}_{hstate_prime}_sharer_list_empty\"
              (!isundefined(prevHomeNode) & prevHomeNode = {hstate} & 
              !isundefined(prevRecProcMsg) & prevRecProcMsg = {mtype} & 
              {m_home_cur}.{m_home_state_field} = {hstate_prime}) ->
              (multisetcount(i:{m_home_cur}.{m_home_sharer_field}, true) = 0);'''
        outff_h.write(prop)
        outff_h.close()

        # Assertion 3: src was in prev_sharer but removed after transition
        outff = f"{dirname}/{hstate}_{mtype}_{hstate_prime}_src_removed_from_sharer.m"
        outff_h = open(outff, "w")
        var_ = {
          "prev_sharer": (f"array [{m_proc_iter_type}] of boolean", f"for m: {m_proc_iter_type} do prev_sharer[m] := false; endfor;\n", f"for m: {m_proc_iter_type} do prev_sharer[m] := (multisetcount(i:{m_home_cur}.{m_home_sharer_field}, {m_home_cur}.{m_home_sharer_field}[i] = m) > 0); endfor;\n"),
          "prevRecProcMsgSrc": (nodes_iter_types[0], "undefine prevRecProcMsgSrc;\n", "")
        }
        prepare_header(outff_h, rec_cond=f"prevRecProcMsgSrc := {{msg_var}}.{m_msg_src_field};", var_=var_)
        prop = f'''invariant \"{hstate}_{mtype}_{hstate_prime}_src_added_to_sharer\"
              (!isundefined(prevHomeNode) & prevHomeNode = {hstate} & 
              !isundefined(prevRecProcMsg) & prevRecProcMsg = {mtype} & 
              {m_home_cur}.{m_home_state_field} = {hstate_prime}) ->
              (
              --prev_sharer[prevRecProcMsgSrc] & 
              (multisetcount(i:{m_home_cur}.{m_home_sharer_field}, {m_home_cur}.{m_home_sharer_field}[i] = prevRecProcMsgSrc) = 0));'''
                # f"  (!IsUndefined(prevHomeNode) & (prevHomeNode = {hstate}) & !IsUndefined(prevRecProcMsgSrc)) ->\n"
                # f"  !(forall i:{m_proc_iter_type} do (i = prevRecProcMsgSrc & {m_home_cur}.{m_home_state_field} = {hstate_prime}) -> (multisetcount(j:{m_home_cur}.{m_home_sharer_field}, {m_home_cur}.{m_home_sharer_field}[j] = i) > 0) endforall);\n")
        outff_h.write(prop) 
        outff_h.close()

        # # constrain the hb edges relative to previous instructions 

        # # we see the trace and go on to assert 
        # resff = f"build/home_s3_msg_out_val_sharere_owner/_build/{hstate}_{mtype}_{hstate_prime}_sharere.txt"
        # # is it empty in the trace: 
        # multiset_sharer = get_resff_multiset(resff, f"{m_home_cur}.{m_home_sharer_field}")
        # if len(multiset_sharer) == 0:
        #   # we assert the case of empty
        #   pass
        # if len(multiset_sharer) == 1:
        #   # the src (i.e., owner)
        #   pass 
        # if len(multiset_sharer) == prev_sharere - 1:
        #   # the src
        #   pass 
        # if len(multiset_sharer) == prev_sharere - 2:
        #   # the src and the owner 
        #   pass 
        
        # if len(multiset_sharer) == prev_sharere + 1:
        #   # the src 
        #   pass 

        # if len(multiset_sharer) == prev_sharere + 2:
        #   # the src and the owner 
        #   pass 



  # refine per coherence set to finer grained than the (hstate, mtype) if necessary 
  # > build/home_s3_req_acc_msg_src_cond/_build/agg.pkl
  aggregate_update = OrderedDict()
  for k, v in aggregate_prime.items():
    hstate, mtype = k
    assert(len(v['imm_picl']) > 0)
    if not len(v['imm_picl']) > 1:
      #aggregate_update[(hstate, mtype, None)] = OrderedDict()
      #aggregate_update[(hstate, mtype, None)]['imm_picl'] = v['imm_picl']
      aggregate_update[k] = v
      continue

    if v['owner_aws_defined']: 
      for hstate_prime in v['imm_picl']:
        resff = f"build/home_s3_req_acc_msg_src_cond/_build/{hstate}_{mtype}_{hstate_prime}_src_owner.txt"
        r = get_res_file(resff, f"{hstate}_accept_req_{mtype}")
        print(hstate, mtype, "src is owner and transition to ", hstate_prime, "possible: ", r)
        if r:
          # if not (hstate, mtype, "src_owner") in aggregate_update:
          #   aggregate_update[(hstate, mtype, "src_owner")] = OrderedDict()
          #   aggregate_update[(hstate, mtype, "src_owner")]['imm_picl'] = [] 
          # aggregate_update[(hstate, mtype, "src_owner")]['imm_picl'].append(hstate_prime)
          if not 'precondition' in v['transition_info'][hstate_prime]:
            v['transition_info'][hstate_prime]['precondition'] = []
          v['transition_info'][hstate_prime]['precondition'].append("src_owner")
        resff = f"build/home_s3_req_acc_msg_src_cond/_build/{hstate}_{mtype}_{hstate_prime}_src_not_owner.txt"
        r = get_res_file(resff, f"{hstate}_accept_req_{mtype}")
        print(hstate, mtype, "src is not owner and transition to ", hstate_prime, "possible: ", r)
        if r:
          #if not (hstate, mtype, "src_not_owner") in aggregate_update:
          #  aggregate_update[(hstate, mtype, "src_not_owner")] = OrderedDict()
          #  aggregate_update[(hstate, mtype, "src_not_owner")]['imm_picl'] = [] 
          #aggregate_update[(hstate, mtype, "src_not_owner")]['imm_picl'].append(hstate_prime)
          if not 'precondition' in v['transition_info'][hstate_prime]:
            v['transition_info'][hstate_prime]['precondition'] = []
          v['transition_info'][hstate_prime]['precondition'].append("src_not_owner")
          
        
    if v['sharer_can_be_non_empty'] and v['sharer_can_be_empty']:
      for hstate_prime in v['imm_picl']:
        resff = f"build/home_s3_req_acc_msg_src_cond/_build/{hstate}_{mtype}_{hstate_prime}_src_not_last_sharer_nonempty.txt"
        r = get_res_file(resff, f"{hstate}_accept_req_{mtype}")
        print(hstate, mtype, "src is not last sharere (nonempty) and transition to ", hstate_prime, "possible: ", r)
        if r:
          # if not (hstate, mtype, "not_last_sharer") in aggregate_update:
          #   aggregate_update[(hstate, mtype, "not_last_sharer_nonempty")] = OrderedDict()
          #   aggregate_update[(hstate, mtype, "not_last_sharer_nonempty")]['imm_picl'] = [] 
          # aggregate_update[(hstate, mtype, "not_last_sharer_nonempty")]['imm_picl'].append(hstate_prime)
          if not 'precondition' in v['transition_info'][hstate_prime]:
            v['transition_info'][hstate_prime]['precondition'] = []
          v['transition_info'][hstate_prime]['precondition'].append("not_last_sharer_nonempty")

        resff = f"build/home_s3_req_acc_msg_src_cond/_build/{hstate}_{mtype}_{hstate_prime}_src_not_last_sharer_empty.txt"
        r = get_res_file(resff, f"{hstate}_accept_req_{mtype}")
        print(hstate, mtype, "src is not last sharere (empty) and transition to ", hstate_prime, "possible: ", r)
        if r:
          # if not (hstate, mtype, "not_last_sharer") in aggregate_update:
          #   aggregate_update[(hstate, mtype, "not_last_sharer_empty")] = OrderedDict()
          #   aggregate_update[(hstate, mtype, "not_last_sharer_empty")]['imm_picl'] = [] 
          # aggregate_update[(hstate, mtype, "not_last_sharer_empty")]['imm_picl'].append(hstate_prime)
          if not 'precondition' in v['transition_info'][hstate_prime]:
            v['transition_info'][hstate_prime]['precondition'] = []
          v['transition_info'][hstate_prime]['precondition'].append("not_last_sharer_empty")

          
        resff = f"build/home_s3_req_acc_msg_src_cond/_build/{hstate}_{mtype}_{hstate_prime}_src_last_sharer.txt"
        r = get_res_file(resff, f"{hstate}_accept_req_{mtype}")
        print(hstate, mtype, "src is last sharer and transition to ", hstate_prime, "possible: ", r)
        if r:
          # if not (hstate, mtype, "last_sharer") in aggregate_update:
          #   aggregate_update[(hstate, mtype, "last_sharer")] = OrderedDict()
          #   aggregate_update[(hstate, mtype, "last_sharer")]['imm_picl'] = [] 
          # aggregate_update[(hstate, mtype, "last_sharer")]['imm_picl'].append(hstate_prime)
          if not 'precondition' in v['transition_info'][hstate_prime]:
            v['transition_info'][hstate_prime]['precondition'] = []
          v['transition_info'][hstate_prime]['precondition'].append("last_sharer")
    aggregate_update[k] = v
  pprint(aggregate_update) 
  for k, v in aggregate_prime.items():
    hstate, mtype = k
    if not len(v['imm_picl']) > 1:
      continue
    for hstate_prime in v['imm_picl']:
      assert('precondition' in v['transition_info'][hstate_prime])
  with open("build/home_s3_req_acc_msg_src_cond/_build/agg.pkl", "wb") as f:
    pickle.dump(aggregate_update, f)
  
  

  
def gen_s3():
  # collect results for sent message type set 

  # with open(f"build/home_s3_msg_out_val_sharere_owner/_build/agg_raw.pkl", "rb") as f:
  with open("build/home_s3_req_acc_msg_src_cond/_build/agg.pkl", "rb") as f:
    aggregate = pickle.load(f)
  for k, v in aggregate.items():
    hstate, mtype = k 
    for hstate_prime, cur in v['transition_info'].items():
      if cur['val_change']:
        resff = f"build/home_s3_src_owner_sharere_extract/_build/{hstate}_{mtype}_{hstate_prime}_val.txt"
        r = get_res_file(resff, f"{hstate}_accept_req_{mtype}", assertion=True)
        print("-->", hstate, mtype, hstate_prime, "val src always equal to inmsg value", r)
        cur['val_change_src'] = "inmsg.cl" if r else ""
      if cur['sharer_chage']:
        resff = f"build/home_s3_src_owner_sharere_extract/_build/{hstate}_{mtype}_{hstate_prime}_src_added_to_sharer.txt"
        r_src_added = get_res_file(resff, f"{hstate}_{mtype}_{hstate_prime}_src_added_to_sharer", assertion=True)
        
        resff = f"build/home_s3_src_owner_sharere_extract/_build/{hstate}_{mtype}_{hstate_prime}_sharer_list_empty.txt"
        r_empty = get_res_file(resff, f"{hstate}_{mtype}_{hstate_prime}_sharer_list_empty", assertion=True)
        
        resff = f"build/home_s3_src_owner_sharere_extract/_build/{hstate}_{mtype}_{hstate_prime}_src_removed_from_sharer.txt"
        r_src_removed = get_res_file(resff, f"{hstate}_{mtype}_{hstate_prime}_src_added_to_sharer", assertion=True)
        print("-->", hstate, mtype, hstate_prime, "sharer src added", r_src_added, "sharer empty", r_empty, "sharer src removed", r_src_removed)

        cur['sharer_change_src_added'] = r_src_added
        cur['sharer_change_empty'] = r_empty
        cur['sharer_change_src_removed'] = r_src_removed
      if cur['owner_change']:
        resff = f"build/home_s3_src_owner_sharere_extract/_build/{hstate}_{mtype}_{hstate_prime}_assert_src_as_owner.txt"
        r = get_res_file(resff, f"{hstate}_accept_req_{mtype}", assertion=True)
        print("-->", hstate, mtype, hstate_prime, "owner change always equal to inmsg.src")
        cur['owner_change_src'] = "inmsg.src" if r else ""
        if not r:
          print("=====> owner change to someone other than the requester???")
      v['transition_info'][hstate_prime] = cur
    aggregate[k] = v
  with open("build/home_s3_src_owner_sharere_extract/_build/agg.pkl", "wb") as f:
    pickle.dump(aggregate, f)
  #pprint(aggregate)

  stepname="home_s3_msg_val_src_dst"
  dirname = f"build/{stepname}/out"
  os.makedirs(dirname, exist_ok = True)   
  for k, v in aggregate.items():
    hstate, mtype = k
    for hstate_prime in v['imm_picl']:
      # we first get the trace and the sent mesage if defined
      resff = f"build/home_s3_msg_out_set/_build/{hstate}_{mtype}_{hstate_prime}_iter.pkl"
      with open(resff, "rb") as f:
        sent_msg_list = pickle.load(f)
      msg_type_sets = [[k for k, v in ele.items() if v == "true"] for ele in sent_msg_list]
      print("->", hstate, mtype, hstate_prime, msg_type_sets)
      v['transition_info'][hstate_prime]['out_msg_sets'] = msg_type_sets


      uniq_msg_types = set([item for sublist in msg_type_sets for item in sublist])
      for out_msg_mtype in uniq_msg_types: 
        # destinations for each type of out message
        # 0) number 
        outff = f"{dirname}/{hstate}_{mtype}_{hstate_prime}_{out_msg_mtype}_cnt.m"
        outff_h = open(outff, "w")

        var_ = {"sent": ("boolean", "sent := false;\n", "sent := false;\n"),
        "out_msg_dst": (m_proc_iter_type, "", "undefine out_msg_dst;\n"),
        "in_msg_src": (m_proc_iter_type, "", ""),
        "cnt": ("0..2", "cnt := 0;\n", "cnt := 0;")
        }
        prepare_header(outff_h, rec_cond=f"in_msg_src := {{msg_var}}.{m_msg_src_field};\n", sending_book_keep_s=f"if (!isundefined(cur_node) & cur_node = selh & {{msg_var}}.{m_msg_type_field} = {out_msg_mtype}) then\n sent := true;\n endif;\n if (!isundefined(cur_node) & cur_node = selh & {{msg_var}}.{m_msg_type_field} = {out_msg_mtype}) then\n out_msg_dst := {{msg_var}}.{m_msg_dst_field};\n cnt := cnt + 1;\n endif;\n", var_=var_)

        outff_h.write(dir_h_accept_trans_outmsg_cnt_template.format(hstate=hstate, mtype=mtype, hstate_prime=hstate_prime, m_home_cur=m_home_cur, m_home_cl_field=m_home_cl_field, m_home_state_field=m_home_state_field))
        outff_h.close()

        # a) original requester 
        #   [x] a.1) always not the requester 
        #   [x] a.2) always the requester 
        outff = f"{dirname}/{hstate}_{mtype}_{hstate_prime}_{out_msg_mtype}_dst_aws_src.m"
        outff_h = open(outff, "w")

        var_ = {"sent": ("boolean", "sent := false;\n", "sent := false;\n"),
        "out_msg_dst": (m_proc_iter_type, "", "undefine out_msg_dst;\n"),
        "in_msg_src": (m_proc_iter_type, "", ""),
        }
        prepare_header(outff_h, rec_cond=f"in_msg_src := {{msg_var}}.{m_msg_src_field};\n", sending_book_keep_s=f"if (!isundefined(cur_node) & cur_node = selh & {{msg_var}}.{m_msg_type_field} = {out_msg_mtype}) then\n sent := true;\n endif;\n if (!isundefined(cur_node) & cur_node = selh & {{msg_var}}.{m_msg_type_field} = {out_msg_mtype}) then\n out_msg_dst := {{msg_var}}.{m_msg_dst_field};\n endif;\n", var_=var_)

        outff_h.write(dir_h_accept_trans_outmsg_dst_src_template.format(hstate=hstate, mtype=mtype, hstate_prime=hstate_prime, m_home_cur=m_home_cur, m_home_cl_field=m_home_cl_field, m_home_state_field=m_home_state_field, is_src=""))
        outff_h.close()

        outff = f"{dirname}/{hstate}_{mtype}_{hstate_prime}_{out_msg_mtype}_dst_aws_not_src.m"
        outff_h = open(outff, "w")

        var_ = {"sent": ("boolean", "sent := false;\n", "sent := false;\n"),
        "out_msg_dst": (m_proc_iter_type, "", "undefine out_msg_dst;\n"),
        "in_msg_src": (m_proc_iter_type, "", ""),
        }
        prepare_header(outff_h, rec_cond=f"in_msg_src := {{msg_var}}.{m_msg_src_field};\n", sending_book_keep_s=f"if (!isundefined(cur_node) & cur_node = selh & {{msg_var}}.{m_msg_type_field} = {out_msg_mtype}) then\n sent := true;\n endif;\n if (!isundefined(cur_node) & cur_node = selh & {{msg_var}}.{m_msg_type_field} = {out_msg_mtype}) then\n out_msg_dst := {{msg_var}}.{m_msg_dst_field};\n endif;\n", var_=var_)

        outff_h.write(dir_h_accept_trans_outmsg_dst_src_template.format(hstate=hstate, mtype=mtype, hstate_prime=hstate_prime, m_home_cur=m_home_cur, m_home_cl_field=m_home_cl_field, m_home_state_field=m_home_state_field, is_src="!"))
        outff_h.close()

        # b) shareres except the requsters 
        # (do in gen_s4 since this depends on the cnt)

        # c) dst always owner? 
        # if its false then its indep of the owner 
        if v['owner_aws_defined']:
          # does it always sent to owner
          outff = f"{dirname}/{hstate}_{mtype}_{hstate_prime}_{out_msg_mtype}_dst_aws_owner.m"
          outff_h = open(outff, "w")

          var_ = {"sent": ("boolean", "sent := false;\n", "sent := false;\n"),
          "out_msg_dst": (m_proc_iter_type, "", "undefine out_msg_dst;\n"),
          "in_msg_src": (m_proc_iter_type, "", ""),
          "prevHomeNodeOnwer": (nodes_iter_types[0], "undefine prevHomeNodeOnwer;\n", f"prevHomeNodeOnwer := {m_home_cur}.{m_home_owner_field};\n")
          }
          prepare_header(outff_h, rec_cond=f"in_msg_src := {{msg_var}}.{m_msg_src_field};\n", sending_book_keep_s=f"if (!isundefined(cur_node) & cur_node = selh & {{msg_var}}.{m_msg_type_field} = {out_msg_mtype}) then\n sent := true;\n endif;\n if (!isundefined(cur_node) & cur_node = selh & {{msg_var}}.{m_msg_type_field} = {out_msg_mtype}) then\n out_msg_dst := {{msg_var}}.{m_msg_dst_field};\n endif;\n", var_=var_)

          outff_h.write(dir_h_accept_trans_outmsg_dst_aws_owner_template.format(hstate=hstate, mtype=mtype, hstate_prime=hstate_prime, m_home_cur=m_home_cur, m_home_cl_field=m_home_cl_field, m_home_state_field=m_home_state_field))
          outff_h.close()

          # assert(0)

        # value for each out message type 

        if (out_msg_mtype in req_msg_types_with_data or out_msg_mtype in resp_msg_types_w_data):
          print("--> PROCESSING ", out_msg_mtype)
          # assert msg val source to be the home 
          outff = f"{dirname}/{hstate}_{mtype}_{hstate_prime}_{out_msg_mtype}.m"
          outff_h = open(outff, "w")

          var_ = {"sent": ("boolean", "sent := false;\n", "sent := false;\n"),
          "val_match": ("boolean", "val_match := false;\n", ""),
          "home_val": (m_val_type_name, "", f"home_val := {m_home_cur}.{m_home_cl_field};"),
          }
          prepare_header(outff_h, rec_cond="", sending_book_keep_s=f"if (!isundefined(cur_node) & cur_node = selh & {{msg_var}}.{m_msg_type_field} = {out_msg_mtype}) then\n sent := true;\n endif;\n if (!isundefined(cur_node) & cur_node = selh & {{msg_var}}.{m_msg_type_field} = {out_msg_mtype}) then\n val_match := ({{msg_var}}.{m_msg_cl_field} = home_val);\n endif;\n", var_=var_)
          
          outff_h.write(dir_h_accept_trans_outmsg_src_template.format(hstate=hstate, mtype=mtype, hstate_prime=hstate_prime, m_home_cur=m_home_cur, m_home_cl_field=m_home_cl_field, m_home_state_field=m_home_state_field))
          outff_h.close()


      # we try to see if its dependent on the rsc in sharer or not OR its dependent on the src == owner or not
      if not len(msg_type_sets) > 1:
        continue
      print("\t\t HERE WE WANT TO SEE IF WE CAN KNOW THE REASON FOR DIVERGENCE under same (hstate, inmsg, hstate_prime)\n", k, hstate_prime, [[k for k, v in itm.items() if v == 'true'] for itm in sent_msg_list]) # v['transition_info'])
      
      # if its false then its indep of the owner 
      if v['owner_aws_defined']:
        print("TBD owner aw defined")
        # because src is owner or not to distinguish the out-msg-set?
        # continue
        # assert(0)
      if v['sharer_can_be_empty'] and v['sharer_can_be_non_empty']:
        # we conjecture maybe its because there is sharere other than src or not
        # following tries to prove this 
        for mset_idx, mset in enumerate(msg_type_sets):
          # this mset_idx is 

          for s_idx, scenario_nm in enumerate(["non_null_shr", "null_shr"]):
            # null_shr: almost empty except src 
            outff = f"{dirname}/{hstate}_{mtype}_{hstate_prime}_{mset_idx}_{s_idx}.m"
            outff_h = open(outff, "w")
            var_ = {
                "prevSentMsgSet": (f"array [{msg_type_name}] of boolean", f"for m: {msg_type_name} do\n prevSentMsgSet[m]:= false;\n endfor;\n", f"for m: {msg_type_name} do\n prevSentMsgSet[m]:= false;\n endfor;\n"),
                "prevRecProcMsgSrc": (nodes_iter_types[0], "undefine prevRecProcMsgSrc;\n", ""), 
                "precond": ("boolean", "precond := false;\n", "precond := false;\n"), 
                "prev_sharer_cnt": ("0..3", "prev_sharer_cnt := 0;\n", f"prev_sharer_cnt := multisetcount(i:{m_home_cur}.{m_home_sharer_field}, true);\n"), 
                "src_in_sh": (f"array [{m_proc_iter_type}] of boolean", f"for tmpm: {m_proc_iter_type} do\n src_in_sh[tmpm] := false; endfor;\n", f"for tmpm: {m_proc_iter_type} do\n src_in_sh[tmpm] := multisetcount(i:{m_home_cur}.{m_home_sharer_field}, {m_home_cur}.{m_home_sharer_field}[i] = tmpm) > 0; endfor;\n")
                }
            sent_msg_ss = []
            for a_m in all_msg_types:
              sent_msg_ss.append(f"prevSentMsgSet[{a_m}] = {(a_m in mset)}")
            sent_msg_ss_acc = " (" + " & ".join(sent_msg_ss) + ") \n"
            
            rec_cond = f"prevRecProcMsgSrc := {{msg_var}}.{m_msg_src_field}"
            if scenario_nm == "null_shr":
              # rec_cond = f"prevRecProcMsgSrc := {{msg_var}}.{m_msg_src_field}; \n if ({{msg_var}}.{m_msg_type_field} = {mtype}) then precond := (multisetcount(i:{m_home_cur}.{m_home_sharer_field}, true) = 0) | (multisetcount(i:{m_home_cur}.{m_home_sharer_field}, {m_home_cur}.{m_home_sharer_field}[i] = {{msg_var}}.{m_msg_src_field}) = 1 & multisetcount(i:{m_home_cur}.{m_home_sharer_field}, true) = 1); \nendif"
              rec_cond = f"prevRecProcMsgSrc := {{msg_var}}.{m_msg_src_field}; \n if ({{msg_var}}.{m_msg_type_field} = {mtype}) then precond := (prev_sharer_cnt = 0) | (prev_sharer_cnt = 1 & src_in_sh[{{msg_var}}.{m_msg_src_field}] = true);\nendif"
            else:
              # non null shar
              # rec_cond = f"prevRecProcMsgSrc := {{msg_var}}.{m_msg_src_field}; \n  if ({{msg_var}}.{m_msg_type_field} = {mtype}) then precond := (multisetcount(i:{m_home_cur}.{m_home_sharer_field}, true) > 0) & (multisetcount(i:{m_home_cur}.{m_home_sharer_field}, {m_home_cur}.{m_home_sharer_field}[i] = {{msg_var}}.{m_msg_src_field}) = 0 | multisetcount(i:{m_home_cur}.{m_home_sharer_field}, true) > 1); \n endif"
              rec_cond = f"prevRecProcMsgSrc := {{msg_var}}.{m_msg_src_field}; \n if ({{msg_var}}.{m_msg_type_field} = {mtype}) then precond := (prev_sharer_cnt > 0) & (prev_sharer_cnt > 1 | src_in_sh[{{msg_var}}.{m_msg_src_field}] = false);\nendif"

            prepare_header(outff_h, rec_cond=rec_cond, sending_book_keep_s=f"if (!isundefined(cur_node) & cur_node = selh) then\n prevSentMsgSet[{{msg_var}}.{m_msg_type_field}]:= true; endif;\n", var_=var_)
            assert_template = '''
            invariant "ASSERT_{hstate}_accept_req_{mtype}"
              (!isundefined(prevHomeNode) & prevHomeNode = {hstate} & 
              !isundefined(prevRecProcMsg) & prevRecProcMsg = {mtype} & 
              {m_home_cur}.{m_home_state_field} = {hstate_prime} & 
              precond) ->
              ({sent_msg_ss_acc});
            '''
            # Combine sent and received message constraints
            outff_h.write(assert_template.format(mtype=mtype, hstate=hstate, m_home_cur=m_home_cur, sent_msg_ss_acc=sent_msg_ss_acc,hstate_prime=hstate_prime, m_home_state_field=m_home_state_field))
            outff_h.close()
        # others? 
        print("OTHER POSSIBILITIES !")
    aggregate[k] = v

  with open(f"build/home_s3_src_owner_sharere_extract/_build/agg_raw.pkl", "wb") as f:
    pickle.dump(aggregate, f)
  # pprint(aggregate)

def gen_chk_dst_shr(dirname, hstate, mtype, hstate_prime, out_msg_mtype):

  # all destinations of this out message must be in current sharer list
  outff = f"{dirname}/{hstate}_{mtype}_{hstate_prime}_{out_msg_mtype}_sent_dst.m"
  outff_h = open(outff, "w")

  var_ = {
    "sent": ("boolean", "sent := false;\n", "sent := false;\n"),
    "fail": ("boolean", "fail := false;\n", "fail := false;\n"),
    "src_in_sh": (
      f"array [{m_proc_iter_type}] of boolean",
      f"for tmpm: {m_proc_iter_type} do\n src_in_sh[tmpm] := false; endfor;\n",
      f"for tmpm: {m_proc_iter_type} do\n src_in_sh[tmpm] := multisetcount(i:{m_home_cur}.{m_home_sharer_field}, {m_home_cur}.{m_home_sharer_field}[i] = tmpm) > 0; endfor;\n",
    ),
    "cur_dst": (
      f"array [{m_proc_iter_type}] of boolean",
      f"for tmpm: {m_proc_iter_type} do\n cur_dst[tmpm] := false; endfor;\n",
      f"for tmpm: {m_proc_iter_type} do\n cur_dst[tmpm] := false; endfor;\n",
    ),
    "prevRecProcMsgSrc": (nodes_iter_types[0], "undefine prevRecProcMsgSrc;\n", "")
  }

  rec_cond = f"prevRecProcMsgSrc := {{msg_var}}.{m_msg_src_field}"
  sending_book_keep_s = f"if (!isundefined(cur_node) & cur_node = selh & {{msg_var}}.{m_msg_type_field} = {out_msg_mtype}) then\n sent := true;\n cur_dst[{{msg_var}}.{m_msg_dst_field}] := true;\n  endif;\n"
  prepare_header(outff_h, rec_cond=rec_cond, sending_book_keep_s=sending_book_keep_s, var_=var_)
  outff_h.write(
      f'''invariant "ASSERT_{{hstate}}_accept_req_{{mtype}}"
  (!isundefined(prevHomeNode) & prevHomeNode = {{hstate}} & 
  !isundefined(prevRecProcMsg) & prevRecProcMsg = {{mtype}} & 
  {{m_home_cur}}.{{m_home_state_field}} = {{hstate_prime}} & sent) ->
  !isundefined(prevRecProcMsg) & (forall tmpm: {m_proc_iter_type} do 
    (tmpm = prevRecProcMsgSrc & cur_dst[tmpm] = false) | 
    (tmpm != prevRecProcMsgSrc & cur_dst[tmpm] = src_in_sh[tmpm])
  endforall);
  '''.format( hstate=hstate, mtype=mtype, hstate_prime=hstate_prime, m_home_cur=m_home_cur, m_home_state_field=m_home_state_field,)
  )
  outff_h.close()
def gen_s4():
  # collect
  # home_s3_msg_val_src_dst: out msg info: dst, sharere, and owner 
  with open(f"build/home_s3_src_owner_sharere_extract/_build/agg_raw.pkl", "rb") as f:
    aggregate = pickle.load(f)
  stepname = "home_s3_sharer"
  dirname = f"build/{stepname}/out"
  os.makedirs(dirname, exist_ok = True)
  for k, v in aggregate.items():
    hstate, mtype = k
    for hstate_prime, cur in v['transition_info'].items():
      v['transition_info'][hstate_prime]['out_msg_dst'] = OrderedDict()
      v['transition_info'][hstate_prime]['out_msg_val'] = OrderedDict()
      v['transition_info'][hstate_prime]['out_msg_cnt_le_1'] = OrderedDict()
      v['transition_info'][hstate_prime]['out_msg_dst_aws_owner'] = OrderedDict()
      v['transition_info'][hstate_prime]['out_msg_set_scenario'] = OrderedDict()
      print("### ", hstate, mtype, hstate_prime)
      msg_type_sets = cur['out_msg_sets']
      uniq_msg_types = set([item for sublist in msg_type_sets for item in sublist])
      for out_msg_mtype in uniq_msg_types:
        resff = f"build/home_s3_msg_val_src_dst/_build/{hstate}_{mtype}_{hstate_prime}_{out_msg_mtype}_cnt.txt"
        r_cnt = get_res_file(resff, f"ASSERT_{hstate}_accept_req_{mtype}", assertion=True)
        v['transition_info'][hstate_prime]['out_msg_cnt_le_1'][out_msg_mtype] = r_cnt
        if not r_cnt:
          print("TODO we see if when multiple msg, are dst includes all sharerees (except the src)", hstate, mtype, hstate_prime, out_msg_mtype)
          gen_chk_dst_shr(dirname, hstate, mtype, hstate_prime, out_msg_mtype)

        resff = f"build/home_s3_msg_val_src_dst/_build/{hstate}_{mtype}_{hstate_prime}_{out_msg_mtype}_dst_aws_src.txt"
        r_aws_src = get_res_file(resff, f"ASSERT_{hstate}_accept_req_{mtype}", assertion=True)


        resff = f"build/home_s3_msg_val_src_dst/_build/{hstate}_{mtype}_{hstate_prime}_{out_msg_mtype}_dst_aws_not_src.txt"
        r = get_res_file(resff, f"ASSERT_{hstate}_accept_req_{mtype}", assertion=True)

        if not (r_aws_src ^ r):
          print("????? TODO ????? \n????? TODO ????? \n????? TODO ????? \n") 
          print("--> out msg ", out_msg_mtype, " dst always equalt to src of ", mtype, "?", r_aws_src)
          print("--> out msg ", out_msg_mtype, " dst always not equalt to src of ", mtype, "?", r)
        if r_aws_src:
          print("--> out msg ", out_msg_mtype, " dst always equalt to src of ", mtype)
          v['transition_info'][hstate_prime]['out_msg_dst'][out_msg_mtype] = f"always_{mtype}.src"
        if r: 
          print("--> out msg ", out_msg_mtype, " dst always not equalt to src of ", mtype)
          v['transition_info'][hstate_prime]['out_msg_dst'][out_msg_mtype] = f"always_not_{mtype}.src"

        if v['owner_aws_defined']:
          resff = f"build/home_s3_msg_val_src_dst/_build/{hstate}_{mtype}_{hstate_prime}_{out_msg_mtype}_dst_aws_owner.txt"
          r_owner = get_res_file(resff, f"ASSERT_{hstate}_accept_req_{mtype}", assertion=True)
          v['transition_info'][hstate_prime]['out_msg_dst_aws_owner'][out_msg_mtype] = r_owner
          if r_owner:
            print("--> out msg ", out_msg_mtype, " dst always equal to owner")
          

        if (out_msg_mtype in req_msg_types_with_data or out_msg_mtype in resp_msg_types_w_data):
          resff = f"build/home_s3_msg_val_src_dst/_build/{hstate}_{mtype}_{hstate_prime}_{out_msg_mtype}.txt"
          r = get_res_file(resff, f"ASSERT_{hstate}_accept_req_{mtype}", assertion=True)
          print("--> out msg ", out_msg_mtype, "value src equal cache line value? ", r)
          if r:
            v['transition_info'][hstate_prime]['out_msg_val'][out_msg_mtype] = "cl_val"

      if len(msg_type_sets) > 1 and v['sharer_can_be_empty'] and v['sharer_can_be_non_empty']:
        scenario_map = OrderedDict()
        onehot_ok = True
        selected_scenarios = []
        for mset_idx, mset in enumerate(msg_type_sets):
          row = {
            'msg_set': mset,
            'non_null_shr': None,
            'null_shr': None,
            'selected': None,
          }
          for s_idx, scenario_nm in enumerate(["non_null_shr", "null_shr"]):
            resff = f"build/home_s3_msg_val_src_dst/_build/{hstate}_{mtype}_{hstate_prime}_{mset_idx}_{s_idx}.txt"
            r_scenario = get_res_file(resff, f"ASSERT_{hstate}_accept_req_{mtype}", assertion=True)
            row[scenario_nm] = r_scenario

          # Exactly one of non_null_shr / null_shr should be true for each mset.
          if row['non_null_shr'] ^ row['null_shr']:
            row['selected'] = "non_null_shr" if row['non_null_shr'] else "null_shr"
            selected_scenarios.append(row['selected'])
          else:
            onehot_ok = False

          scenario_map[mset_idx] = row

        # Across msets, selected scenarios should be different.
        distinct_ok = (len(selected_scenarios) == len(scenario_map)) and (len(set(selected_scenarios)) == len(selected_scenarios))

        if onehot_ok and distinct_ok:
          v['transition_info'][hstate_prime]['out_msg_set_scenario'] = scenario_map
          v['transition_info'][hstate_prime]['out_msg_set_scenario_cause_uncovered'] = True
        else:
          v['transition_info'][hstate_prime]['out_msg_set_scenario'] = OrderedDict()
          v['transition_info'][hstate_prime]['out_msg_set_scenario_cause_uncovered'] = False
          print("WARN out_msg_set_scenario invalid:", hstate, mtype, hstate_prime, "onehot_ok=", onehot_ok, "distinct_ok=", distinct_ok)

        
    aggregate[k] = v 
  
    
  g_all_paths = []
  for k, v in aggregate.items():
    hstate, mtype = k
    if not hstate in all_llc_stable_states:
      continue
    for hstate_prime in v['imm_picl']:
      # print("start (", hstate, mtype, ")", hstate_prime)
      all_paths = []
      def find_paths_to_stable(start_node, mtype, path, visited_in_path):
        path.append((mtype, start_node))
        visited_in_path.add(start_node)

        # If the current node is a stable state, we found a path
        if start_node in all_llc_stable_states:
            all_paths.append(list(path))
        else:
            # Explore neighbors
            for tmpk, tmpv in aggregate.items():
              tmp_hstate, tmp_mtype = tmpk
              if tmp_hstate == start_node:
                for neighbor in tmpv['imm_picl']:
                  if not neighbor in visited_in_path:
                    find_paths_to_stable(neighbor, tmp_mtype, path, visited_in_path)
        # Backtrack
        path.pop()
        visited_in_path.remove(start_node)
      find_paths_to_stable(hstate_prime, mtype, [], set([hstate])) 
      # each path consists of element being (mtype, hstate_prime)
      # print("=>", all_paths)
      for p in all_paths:
        g_all_paths.append((hstate, p))
      # for picl_list in all_paths:
      #   cur_upath = OrderedDict()
      #   # start with hstate, take in in_msg[idx], and transition to picl_list[idx]
      #   cur_upath['picl_list'] = [e[1] for e in picl_list]
      #   cur_upath['in_msg'] = [e[0] for e in picl_list]
      #   # picl_val in next step 
      #   update_val['upaths'].append(cur_upath)
    # aggregate_update[k] = update_val

  with open("build/home_s3_msg_val_src_dst/_build/agg.pkl", "wb") as f:
    pickle.dump((aggregate, g_all_paths), f)  
  pprint(g_all_paths)

  # home_path_group_info_
  stepname = "home_s4_upath_cur_idx"
  dirname = f"build/{stepname}/out"
  os.makedirs(dirname, exist_ok = True)

  track_template = '''
  -- Randomly select the request to track
  rule "track_{hstate}_{entry_msg}"
      (!tracked & !IsUndefined(prevHomeNode) & prevHomeNode = {hstate} &
      !IsUndefined(prevRecProcMsg) & prevRecProcMsg = {entry_msg}) ==>
        start := true;
        tracked := true;
  endrule;
  '''
  path_msg_pairwise = OrderedDict()
  for path_idx, (hstate, p) in enumerate(g_all_paths):
    if len(p) <= 1:
      continue
    in_msgs = [e[0] for e in p]
    tar_states = [e[1] for e in p]
    entry_msg = in_msgs[0]
    
    # For each path, enumerate all possible message pairs across per-step in/out messages.
    # Each step contributes exactly one incoming message and one possible outgoing message set.
    step_msg_options = []
    cur_state = hstate
    for step_idx, (step_in_msg, step_next_state) in enumerate(p):
      out_msg_sets = []
      if (cur_state, step_in_msg) in aggregate and step_next_state in aggregate[(cur_state, step_in_msg)]['transition_info']:
        out_msg_sets = aggregate[(cur_state, step_in_msg)]['transition_info'][step_next_state].get('out_msg_sets', [])
      if len(out_msg_sets) == 0:
        out_msg_sets = [[]]

      cur_step_options = []
      for out_msg_set in out_msg_sets:
        cur_step_msgs = [("in", step_idx, step_in_msg)]
        for out_msg in out_msg_set:
          cur_step_msgs.append(("out", step_idx, out_msg))
        cur_step_options.append(cur_step_msgs)
      step_msg_options.append(cur_step_options)
      cur_state = step_next_state

    pairwise_msgs = []
    seen_pairwise_msgs = set()
    for per_step_choice in itertools.product(*step_msg_options):
      concrete_msg_list = [m for step_msgs in per_step_choice for m in step_msgs]
      for m0, m1 in itertools.combinations(concrete_msg_list, 2):
        pair = tuple(sorted((m0, m1)))
        if pair in seen_pairwise_msgs:
          continue
        seen_pairwise_msgs.add(pair)
        pairwise_msgs.append(pair)

    path_msg_pairwise[path_idx] = {
     'hstate': hstate,
     'path': p,
     'pairwise_msgs': pairwise_msgs,
    }
    print("-->", "path_idx", path_idx, "pairwise msg combos", pairwise_msgs)
    for pair_idx, pair_msg in enumerate(sorted(pairwise_msgs)):
      ################################################## 
      m0, m1 = pair_msg
      
      # Classify messages: tuples are (direction, step_idx, mtype)
      m0_dir, m0_idx, m0_msg = m0
      m1_dir, m1_idx, m1_msg = m1
      
      m0_is_in = (m0_dir == "in")
      m0_is_out = (m0_dir == "out")
      m1_is_in = (m1_dir == "in")
      m1_is_out = (m1_dir == "out")
      
      rec_cond = f"prevRecProcMsgSrc := {{msg_var}}.{m_msg_src_field}"
      sending_book_keep_s = f"if (!isundefined(cur_node) & cur_node = selh) then\n prevSentMsgDst := {{msg_var}}.{m_msg_dst_field}; prevSentMsg := {{msg_var}}.{m_msg_type_field}; endif;\n"
      blk_start = ""
      
      # Case 1: Both incoming messages (both in)
      if m0_is_in and m1_is_in:
        assert(m0_idx != m1_idx)
        # Track sender for both incoming messages
        blk_start = (f"if (cur_idx = {m0_idx} & !isundefined(prevRecProcMsg) & prevRecProcMsg = {m0_msg}) then m0 := prevRecProcMsgSrc; endif;\n "
                    f"if (cur_idx = {m1_idx} & !isundefined(prevRecProcMsg) &  prevRecProcMsg = {m1_msg}) then m1 := prevRecProcMsgSrc; endif;\n ")
      
      # Case 2: Both outgoing messages (both out)
      elif m0_is_out and m1_is_out:
        # Track receiver for both outgoing messages
        assert(m0_idx != m1_idx)
        blk_start = (f"if (cur_idx = {m0_idx} & !isundefined(prevSentMsg) & prevSentMsg = {m0_msg}) then m0 := prevSentMsgDst; endif;\n"
                      f"if (cur_idx = {m1_idx} & !isundefined(prevSentMsg) & prevSentMsg = {m1_msg}) then m1 := prevSentMsgDst; endif;\n")

      # Case 3: Mixed (one in, one out)
      elif (m0_is_in and m1_is_out) or (m0_is_out and m1_is_in):
        # For incoming message: track sender
        # For outgoing message: track receiver
        in_, out_ = m0_idx, m1_idx
        in_m, out_m = m0_msg, m1_msg
        if m1_is_in:
          in_, out_ = m1_idx, m0_idx
          in_m, out_m = m1_msg, m0_msg
        blk_start = (f"if (cur_idx = {in_} & !isundefined(prevRecProcMsg) & prevRecProcMsg = {in_m}) then m0 := prevRecProcMsgSrc; endif;\n "
                    f"if (cur_idx = {out_} & !isundefined(prevSentMsg) & prevSentMsg = {out_m}) then m1 := prevSentMsgDst; endif;\n ")

      ################################################## 
      # Declare variables for message pair tracking
      var_ = {
        "m0": (m_proc_iter_type, "undefine m0;\n", ""),
        "m1": (m_proc_iter_type, "undefine m1;\n", ""),
        "prevRecProcMsgSrc": (m_proc_iter_type, "undefine prevRecProcMsgSrc;\n", ""),
        "prevSentMsgDst": (m_proc_iter_type, "undefine prevSentMsgDst;\n", ""),
      }
      
      extra_cfg = {
      "rset": {
          "mode": "tar_idx", # original: use None
          "state_type_name": m_home_state_type, 
          "stable_state_df": "|".join([f"{m_home_cur}.{m_home_state_field} = {s}" for s in all_llc_stable_states]),
          "block_within_start": blk_start,
          "tar_states": tar_states,
          "tar_target_len": len(tar_states),
          # "proc_state_expr": f"{m_home_cur}.{m_home_state_field}",
          # "prev_state_var": "prevHomeNode",
          'home': True,
          'm_home_cur': m_home_cur,
          'm_home_state_field': m_home_state_field,
        },
      "msg_prevsent": True
      }
      outff = f"{dirname}/{hstate}_{entry_msg}_{path_idx}_{pair_idx}.m"
      outff_h = open(outff, "w")
      prepare_header(outff_h, rec_cond=rec_cond, sending_book_keep_s=sending_book_keep_s, var_=var_, extra_cfg=extra_cfg,)
      outff_h.write(track_template.format(hstate=hstate, entry_msg=entry_msg))
      outff_h.write(
        f'''invariant "ASSERT_{path_idx}_{pair_idx}"
            (tracked & !start & cur_idx = {len(tar_states)}) ->
           !isundefined(m0) & !isundefined(m1) & m0 = m1; 
           -- {m0_dir}, {m0_idx}, {m0_msg}
           -- {m1_dir}, {m1_idx}, {m1_msg}
          '''
      )
      outff_h.close()
      print(f"  pair {pair_idx}: ({m0_dir}[{m0_idx}]::{m0_msg}) <-> ({m1_dir}[{m1_idx}]::{m1_msg}) | case: {'both_in' if (m0_is_in and m1_is_in) else 'both_out' if (m0_is_out and m1_is_out) else 'mixed'}")


  build_dirname = f"build/{stepname}/_build"
  os.makedirs(build_dirname, exist_ok = True)
  with open(f"{build_dirname}/path_msg_pairwise.pkl", "wb") as f:
    pickle.dump(path_msg_pairwise, f)
   
  return
def pp():
  stepname = "home_s4_upath_cur_idx"
  build_dirname = f"build/{stepname}/_build"

  with open(f"{build_dirname}/path_msg_pairwise.pkl", "rb") as f:
    path_msg_pairwise = pickle.load(f)

  aggregate = OrderedDict()

  for path_idx, path_info in path_msg_pairwise.items():
    hstate = path_info['hstate']
    path = path_info['path']
    pairwise_msgs = sorted(path_info['pairwise_msgs'])
    entry_msg = path[0][0]

    path_res = OrderedDict()
    path_res['hstate'] = hstate
    path_res['path'] = path
    path_res['pairwise_msgs'] = pairwise_msgs
    path_res['pair_results'] = OrderedDict()

    for pair_idx, pair_msg in enumerate(pairwise_msgs):
      resff = f"{build_dirname}/{hstate}_{entry_msg}_{path_idx}_{pair_idx}.txt"
      ret = get_res_file(resff, f"ASSERT_{path_idx}_{pair_idx}", assertion=True)
      path_res['pair_results'][pair_idx] = {
        'pair_msg': pair_msg,
        'assertion_proven': ret,
      }

    aggregate[path_idx] = path_res
    print("->", "path_idx", path_idx, "pairs", len(pairwise_msgs), "all proven")
  with open(f"{build_dirname}/agg.pkl", "wb") as f:
    pickle.dump(aggregate, f)
  pprint(aggregate)

def depr():
  assert(0)
  # summarize 
  aggregate_update = OrderedDict()
  for k, v in aggregate.items():
    hstate, mtype = k
    if not hstate in all_llc_stable_states:
      continue
    print('->', hstate, mtype, v['imm_picl'])
    update_val = v
    update_val['upaths'] = []
    for hstate_prime in v['imm_picl']:
      all_paths = []
      def find_paths_to_stable(start_node, mtype, path, visited_in_path):
        path.append((mtype, start_node))
        visited_in_path.add(start_node)

        # If the current node is a stable state, we found a path
        if start_node in all_llc_stable_states:
            all_paths.append(list(path))
        else:
            # Explore neighbors
            for tmpk, tmpv in aggregate.items():
              tmp_hstate, tmp_mtype = tmpk
              if tmp_hstate == start_node:
                for neighbor in tmpv['imm_picl']:
                  if not neighbor in visited_in_path:
                    find_paths_to_stable(neighbor, tmp_mtype, path, visited_in_path)
        # Backtrack
        path.pop()
        visited_in_path.remove(start_node)
      find_paths_to_stable(hstate_prime, mtype, [], set([hstate])) 
      
      for picl_list in all_paths:
        # each ele is (mtype, hstate_prime)
        cur_upath = OrderedDict()
        # start with hstate, take in in_msg[idx], and transition to picl_list[idx]
        cur_upath['picl_list'] = [e[1] for e in picl_list]
        cur_upath['in_msg'] = [e[0] for e in picl_list]
        # picl_val in next step 
        update_val['upaths'].append(cur_upath)
    aggregate_update[k] = update_val
  with open("build/home_s3_src_owner_sharere_extract/_build/agg_update.pkl", "wb") as f:
    pickle.dump(aggregate_update, f) 
  

  # then assert 



##################################################  
# 1) serve without the need of transaction (i.e., transitioning to transient states) 
#   a. send out message? 
#       - how many message?
#   b. transition to new state?
# 2) serve w/ transaction
#   a. set of nodes
#   b. send messages? 
#   c. receive messages?





# def gen_s5():
#   pass 
#   stepname="home_s3_msg_out"
#   dirname = f"build/{stepname}/out"
#   with open(f"{dirname}/agg_raw.pkl", "rb") as f:
#     aggregate = pickle.load(f)
   
#   for k, v in aggregate.items():
#     hstate, mtype = k
#     for hstate_prime in v['imm_picl']:
#       # we first get the trace and the sent mesage if defined
#       resff = f"build/{stepname}/_build/{hstate}_{mtype}_{hstate_prime}_iter.pkl"
#       with open(resff, "rb") as f:
#         sent_msg_list = pickle.load(f)
#       print("->", hstate, mtype, hstate_prime, [[k for k, v in ele.items() if v == "true"] for ele in sent_msg_list])

#       # [ ] we assert the value from msg out to be the same value as picl; otherwise 
      
  
#   return 
#   # from previous step, home_s3_msg_out, we get the messsage sent set 
#   # [ ] we assert the value from msg out to be the same value as picl; otherwise 
#   # 4) msg sending's value?
#   for k, v in aggregate.items():
#     hstate, mtype = k
#     for hstate_prime in v['imm_picl']:
#       # we first get the trace and the sent mesage if defined
#       resff = f"build/home_s2_msg_out_and_val/_build/{hstate}_{mtype}_{hstate_prime}.txt"
#       ret = get_last_state(resff, "prevSentMsg")
#       print(hstate, mtype, hstate_prime, "sent msg potential:", ret)
#       if ret is not None and ret.lower() != "undefined":
#         out_mtype = ret
#         resff = f"build/{stepname}/_build/{hstate}_{mtype}_{hstate_prime}_sent_assert_{out_mtype}.txt"
#         r = get_res_file(resff, f"ASSERT_{hstate}_accept_req_{mtype}", assertion=True)
#         print(hstate, mtype, hstate_prime, "sent msg potential:", ret, "pass assertion", r)




# def gen_s4():
#   if not dst_always_defined:
#     tpath = "build/home_s1_1_req_acc_proc_state/_build/aggdict.pkl"
#   else:
#     tpath = "build/home_s1_req_acc_state/_build/aggdict.pkl"
#   with open(tpath, "rb") as f:
#     aggregate = pickle.load(f)
# 
#   stepname="home_s2_req_acc_proc_state"
#   dirname = f"build/{stepname}/_build"
#   stepname_tmp ="home_s3_val_check"
#   dirname_tmp = f"build/{stepname_tmp}/out"
#   os.makedirs(dirname_tmp, exist_ok = True)  
#   if set(all_llc_states) == set(all_llc_stable_states):
#     # no need to explore transaction
# 
#     for k, v in aggregate.items():
#       hstate, mtype = k
#       print ("###########")
#       print (hstate, mtype)
#       if not v['proc']:
#         # empty upath
#         continue
#       v['init_txn'] = False
#       # then 
#     
#       v['state_prime'] = None
#       for h_prime in all_llc_stable_states:
#         resff = f"{dirname}/{hstate}_{mtype}_no_txn_{h_prime}.txt"
#         r = get_res_file(resff, f"{hstate}_accept_req_{mtype}")
#         if r:
#           assert(v['state_prime'] is None)
#           print("-> transition", hstate, mtype, h_prime)
#           v['state_prime'] = h_prime
# 
#        out_mtype = ret
##       # b. send out message?
#        out_mtype = ret
##       # c. send out message to the sender of the mtype that triggers or not? 
#        out_mtype = ret
#       # e. TODO: if out_mtype is dataresp, it is always the HomeNode.val? 
#       for out_mtype in all_msg_types: 
#         resff = f"{dirname}/{hstate}_{mtype}_outmsg_{out_mtype}.txt"
#         r = get_res_file(resff, f"{hstate}_accept_req_{mtype}")
#         if not 'send_msg' in v:
#        out_mtype = ret
#           v['send_msg'] = OrderedDict()
#         if r:
#           print("-> out msg", hstate, mtype, out_mtype)
#           v['send_msg'][out_mtype] = OrderedDict()
#           v['send_msg'][out_mtype]['cnt'] = 1 # TODO
# 
#         resff = f"{dirname}/{hstate}_{mtype}_outmsg_{out_mtype}_to_src_chk.txt"
#         r_src = get_res_file(resff, f"{hstate}_accept_req_{mtype}")
#         if r and r_src:
#           print("-> out msg can dst to src of ", mtype)
#           v['send_msg'][out_mtype]['dst_to_inmsg_src'] = True
#         resff = f"{dirname}/{hstate}_{mtype}_outmsg_{out_mtype}_val_from_picl.txt"
#         r_val = get_res_file(resff, f"{hstate}_accept_req_{mtype}")
#         if r and r_val:
#           v['send_msg'][out_mtype]['val_eq_picl_val'] = True
# 
#       resff = f"{dirname}/{hstate}_{mtype}_val_change.txt"
#       r = get_res_file(resff, f"{hstate}_accept_req_{mtype}")
#       v['val_change'] = r
#       if r:
#         print("-> val change possible", hstate, mtype)
# 
#         outff = f"{dirname_tmp}/{hstate}_{mtype}_val_chk_inmsg.m"
#         print(outff)
#         outff_h = open(outff, "w")
#         prepare_header(outff_h, design_file)
#         outff_h.write(home_inmsg_notxn_val_eq_in_template.format(hstate=hstate, mtype=mtype, m_home_iter=m_home_iter,m_msg_type_field=m_msg_type_field))
#         outff_h.close()
# 
#         if main_mem is not None:
#           outff = f"{dirname_tmp}/{hstate}_{mtype}_val_chk_mainmem.m"
#           print(outff)
#           outff_h = open(outff, "w")
#           prepare_header(outff_h, design_file)
#           outff_h.write(home_inmsg_notxn_val_eq_mainmem_template.format(hstate=hstate, mtype=mtype, m_home_iter=m_home_iter,m_msg_type_field=m_msg_type_field, main_mem=main_mem))
#           outff_h.close()
# 
# 
#       aggregate[k] = v
#   else:
#     # hprim_state to be non-stable-state
#     # we get the 
#     print("TODO")
#     assert(0)
# 
#   with open(f"{dirname}/aggdict.pkl", "wb") as f: # 'wb' for write binary
#     pickle.dump(aggregate, f)
#   pprint(aggregate)
# def gen_s5():
#   tpath = "build/home_s2_req_acc_proc_state/_build/aggdict.pkl"
#   with open(tpath, "rb") as f:
#     aggregate = pickle.load(f)
#   if set(all_llc_states) == set(all_llc_stable_states):
#     for k, v in aggregate.items():
#       hstate, mtype = k
#       if not v['proc']:
#         # empty upath
#         continue
#       # v['init_txn'] is false AND the following 
#       # 1. v['state_prime'] if not None gives the resulting h_prime
#       # 2. v['send_msg'] if not empty key gives the sent message
#       # 3. v['val_change'] gives whether value can be changed 
#       # if not in val_change then it means no val_change
#       if v['val_change']:
#         # collect results 
#         stepname_tmp ="home_s3_val_check"
#         dirname_tmp = f"build/{stepname_tmp}/_build"
#         resff = f"{dirname_tmp}/{hstate}_{mtype}_val_chk_inmsg.txt"
#         proven_ = get_res_file(resff, f"ASSERT_{hstate}_accept_req_{mtype}", assertion=True)
#         proven_m = None
#         if main_mem is not None: 
#           resff = f"{dirname_tmp}/{hstate}_{mtype}_val_chk_mainmem.txt"
#           proven_m = get_res_file(resff, f"ASSERT_{hstate}_accept_req_{mtype}", assertion=True)

#         print("--> ", hstate, mtype, "val change always to inmsg.val?", proven_)
#         print("--> ", hstate, mtype, "val change always to mainmem?", proven_m)
#         v['val_aws_to_inmsg'] = proven_
#         v['val_aws_to_main_mem'] = proven_m
#       aggregate[k] = v

#   with open(f"{dirname_tmp}/aggdict.pkl", "wb") as f: # 'wb' for write binary
#     pickle.dump(aggregate, f)
#   pprint(aggregate)

if __name__ == "__main__":
    fire.Fire()
    dump_stats()


# # b) no transition at all 
#       idx = 0
#       for aset in ([[hstate, hstate]] + paths):
#         if not aset[0] == hstate:
#           continue
#         outff = f"{dirname}/{hstate}_{mtype}_{idx}.m"
#         outff_h = open(outff, "w")
#         dec = False
#         if dst_always_defined:      
#           with open("/Users/yaohsiao/work/coh_syn_dev/murphi/protocols/fv/msi_fv_envs/msi.fvt.home_s3_rset.m", "r") as f:
#             for ln in f:
#               if f"#RECEIVING" in ln:
#                 msg_var = ln[:-1].split(",")[-1]
#                 outff_h.write(f"if (!isundefined(cur_node) & cur_node = selh) then\n prevRecProcMsg := {msg_var}.{m_msg_type_field};\n endif;\n")
#               # elif "endstartstate" in ln:
#               #   outff_h.write(ln)
#               else:
#                 outff_h.write(ln)
#               # if "var" == ln[:3] and not dec:
#               #   dec = True
#           rset_s = ""
#           for s_ in all_llc_states:
#             if s_ in aset[1:]:
#               rset_s += dis_ele.format(state=s_, inset="1")
#             else:
#               rset_s += dis_ele.format(state=s_, inset="0")
        
#           outff_h.write(h_track_template.format(hstate=hstate, mtype=mtype))
#           outff_h.write(rset_template.format(hstate=hstate, mtype=mtype, idx=idx,
#               reachable_set=rset_s))
#           outff_h.close()
#           idx += 1 


# # 2) picl value per hstate, mtype, hstate_prime
#   for k, v in aggregate.items():
#     hstate, mtype = k
#     for hstate_prime in v['imm_picl']:
#       outff = f"{dirname}/{hstate}_{mtype}_{hstate_prime}_val.m"
#       outff_h = open(outff, "w")
#       dec = False
#       with open("/Users/yaohsiao/work/coh_syn_dev/murphi/protocols/fv/msi_fv_envs/msi.fvt.s1_msg.m", "r") as f:
#         for ln in f:
#           if f"#RECEIVING" in ln:
#             msg_var = ln[:-1].split(",")[-1]
#             outff_h.write(f"if (!isundefined(cur_node) & cur_node = selh) then\n prevRecProcMsg := {msg_var}.{m_msg_type_field};\n endif;\n")
#           elif "BLOCK_WITHIN_BOOK_KEEP" in ln:
#             outff_h.write(f"prevHomeNode := {m_home_cur};\n")
#             outff_h.write("undefine prevRecProcMsg;\n")
#           elif "endstartstate" in ln:
#             outff_h.write("undefine prevHomeNode;\n")
#             outff_h.write("undefine prevRecProcMsg;\n")
#             outff_h.write(f"for i:{m_home_iter_type} do\n selh := i;\n endfor;\n")
#             outff_h.write(f"for i:{addr_type_name} do\n myaddr := i;\n endfor;\n")
#             outff_h.write(ln)
#           else:
#             outff_h.write(ln)
#           if "var" == ln[:3] and not dec:
#             dec = True
#             outff_h.write(f"prevHomeNode: {m_home_type_name};\n")
#             outff_h.write(f"prevRecProcMsg: {msg_type_name};\n")
#             # m_home_cur requires: 
#             outff_h.write(f"selh: {m_home_iter_type};\n")
#             outff_h.write(f"myaddr: {addr_type_name};\n")
#       # can it ever change value during this picl set 
#       outff_h.write(dir_h_accept_trans_val_template.format(mtype=mtype, hstate=hstate, m_home_cur=m_home_cur,m_home_state_field=m_home_state_field,hstate_prime=hstate_prime, m_home_cl_field=m_home_cl_field))
#       outff_h.close()




  # stepname="home_s2_msg_out_and_val"
  # dirname = f"build/{stepname}/out"
  # os.makedirs(dirname, exist_ok = True)  

  

  # # 3.1) get trace only at this step msg sending per hstate, mtype, hstate_prime
  # for k, v in aggregate.items():
  #   hstate, mtype = k
  #   for hstate_prime in v['imm_picl']:
  #     # we first get the trace and the sent mesage if defined
  #     outff = f"{dirname}/{hstate}_{mtype}_{hstate_prime}.m"
  #     outff_h = open(outff, "w")
  #     dec = False
  #     with open("/Users/yaohsiao/work/coh_syn_dev/murphi/protocols/fv/msi_fv_envs/msi.fvt.s1_msg.m", "r") as f:
  #       for ln in f:
  #         if f"#RECEIVING" in ln:
  #           msg_var = ln[:-1].split(",")[-1]
  #           outff_h.write(f"if (!isundefined(cur_node) & cur_node = selh) then\n prevRecProcMsg := {msg_var}.{m_msg_type_field};\n endif;\n")
  #         elif f"#SENDING" in ln:
  #           msg_var = ln[:-1].split(",")[-1]
  #           #outff_h.write(f"if (!isundefined(cur_node) & cur_node = selh) then\n prevSentMsg := {msg_var}.{m_msg_type_field};\n endif;\n")
  #           outff_h.write(f"if (!isundefined(cur_node) & cur_node = selh) then\n prevSentMsg[{msg_var}.{m_msg_type_field}]:= true; endif;\n")
  #         elif "BLOCK_WITHIN_BOOK_KEEP" in ln:
  #           outff_h.write(f"prevHomeNode := {m_home_cur}.{m_home_state_field};\n")
  #           outff_h.write("undefine prevRecProcMsg;\n")
  #           outff_h.write(f"for m: {msg_type_name} do\n prevSentMsg[m]:= false;\n endfor;\n")
  #         elif "endstartstate" in ln:
  #           outff_h.write("undefine prevHomeNode;\n")
  #           outff_h.write("undefine prevRecProcMsg;\n")
  #           outff_h.write(f"for m: {msg_type_name} do\n prevSentMsg[m]:= false;\n endfor;\n")
  #           outff_h.write(f"for i:{m_home_iter_type} do\n selh := i;\n endfor;\n")
  #           outff_h.write(f"for i:{addr_type_name} do\n myaddr := i;\n endfor;\n")
  #           outff_h.write(ln)
  #         else:
  #           outff_h.write(ln)
  #         if "var" == ln[:3] and not dec:
  #           dec = True
  #           outff_h.write(f"prevHomeNode: {m_home_state_type};\n")
  #           outff_h.write(f"prevRecProcMsg: {msg_type_name};\n")
  #           outff_h.write(f"prevSentMsg: array [{msg_type_name}] of boolean;\n")
  #           # m_home_cur requires: 
  #           outff_h.write(f"selh: {m_home_iter_type};\n")
  #           outff_h.write(f"myaddr: {addr_type_name};\n")
  #     outff_h.write(dir_h_accept_trans_template.format(mtype=mtype, hstate=hstate, m_home_cur=m_home_cur,m_home_state_field=m_home_state_field,hstate_prime=hstate_prime))
  #     outff_h.close()
      

# 
# def gen_s4():
# 
#   stepname="home_s3_msg_out"
#   dirname = f"build/{stepname}/out"
#   os.makedirs(dirname, exist_ok = True)  
#   with open("build/home_s2_req_acc_proc_state/_build/agg_raw.pkl", "rb") as f:
#     aggregate = pickle.load(f)
# 
#   # 2) picl value per hstate, mtype, hstate_prime
#   for k, v in aggregate.items():
#     hstate, mtype = k
#     for hstate_prime in v['imm_picl']:
#       resff = f"build/home_s2_msg_out_and_val/_build/{hstate}_{mtype}_{hstate_prime}_val.txt"
#       r = get_res_file(resff, f"{hstate}_accept_req_{mtype}")
#       print(hstate, mtype, hstate_prime, "val change?", r)
#       v['val_change'] = r
#     aggregate[k] = v
#   with open(f"{dirname}/agg_raw.pkl", "wb") as f:
#     pickle.dump(aggregate, f)
#    
#   for k, v in aggregate.items():
#     hstate, mtype = k
#     for hstate_prime in v['imm_picl']:
#       # we first get the trace and the sent mesage if defined
#       resff = f"build/home_s2_msg_out_and_val/_build/{hstate}_{mtype}_{hstate_prime}.txt"
#       ret = get_last_state(resff, "prevSentMsg", arr=True)
#       print(hstate, mtype, hstate_prime, "sent msg potential:", [k for k, v in ret.items() if v == 'true'])
#       if ret is not None: # ret.lower() != "undefined":
#         # 3.2) we assert the case ITERATIVELY
#         outff = f"{dirname}/{hstate}_{mtype}_{hstate_prime}_iter.py"
#         outff_h = open(outff, "w")
#         outff_h.write(f"stepname = \"{stepname}\"\n")
#         outff_h.write(f"hstate = \"{hstate}\"\n")
#         outff_h.write(f"mtype = \"{mtype}\"\n")
#         outff_h.write(f"m_home_cur = \"{m_home_cur}\"\n")
#         outff_h.write(f"m_home_state_field = \"{m_home_state_field}\"\n")
#         outff_h.write(f"hstate_prime = \"{hstate_prime}\"\n")
#         with open("src/home_upath_dir_sent_iter.py", "r") as f:
#           for ln in f:
#             outff_h.write(ln)
#         outff_h.close()
# 
#         outff = f"{dirname}/{hstate}_{mtype}_{hstate_prime}_baseff.m"
#         outff_h = open(outff, "w")
# 
#         dec = False
#         with open("/Users/yaohsiao/work/coh_syn_dev/murphi/protocols/fv/msi_fv_envs/msi.fvt.s1_msg.m", "r") as f:
#           for ln in f:
#             if f"#RECEIVING" in ln:
#               msg_var = ln[:-1].split(",")[-1]
#               outff_h.write(f"if (!isundefined(cur_node) & cur_node = selh) then\n prevRecProcMsg := {msg_var}.{m_msg_type_field};\n endif;\n")
#             elif f"#SENDING" in ln:
#               msg_var = ln[:-1].split(",")[-1]
#               #outff_h.write(f"if (!isundefined(cur_node) & cur_node = selh) then\n prevSentMsg := {msg_var}.{m_msg_type_field};\n endif;\n")
#               outff_h.write(f"if (!isundefined(cur_node) & cur_node = selh) then\n prevSentMsg[{msg_var}.{m_msg_type_field}]:= true; endif;\n")
#             elif "BLOCK_WITHIN_BOOK_KEEP" in ln:
#               outff_h.write(f"prevHomeNode := {m_home_cur}.{m_home_state_field};\n")
#               outff_h.write("undefine prevRecProcMsg;\n")
#               outff_h.write(f"for m: {msg_type_name} do\n prevSentMsg[m]:= false;\n endfor;\n")
#             elif "endstartstate" in ln:
#               outff_h.write("undefine prevHomeNode;\n")
#               outff_h.write("undefine prevRecProcMsg;\n")
#               outff_h.write(f"for m: {msg_type_name} do\n prevSentMsg[m]:= false;\n endfor;\n")
#               outff_h.write(f"for i:{m_home_iter_type} do\n selh := i;\n endfor;\n")
#               outff_h.write(f"for i:{addr_type_name} do\n myaddr := i;\n endfor;\n")
#               outff_h.write(ln)
#             else:
#               outff_h.write(ln)
#             if "var" == ln[:3] and not dec:
#               dec = True
#               outff_h.write(f"prevHomeNode: {m_home_state_type};\n")
#               outff_h.write(f"prevRecProcMsg: {msg_type_name};\n")
#               outff_h.write(f"prevSentMsg: array [{msg_type_name}] of boolean;\n")
#               # m_home_cur requires: 
#               outff_h.write(f"selh: {m_home_iter_type};\n")
#               outff_h.write(f"myaddr: {addr_type_name};\n")
#         sent_msg_ss = []
#         for k, v in ret.items():
#           sent_msg_ss.append(f"prevSentMsg[{k}] = {v}")
# 
#         #outff_h.write(dir_h_accept_trans_template.format(mtype=mtype, hstate=hstate, m_home_cur=m_home_cur,m_home_state_field=m_home_state_field,hstate_prime=hstate_prime))
#         # outff_h.write(dir_h_accept_trans_outmsg_template.format(mtype=mtype, hstate=hstate, m_home_cur=m_home_cur, sent_msg_ss=" & ".join(sent_msg_ss),hstate_prime=hstate_prime, m_home_state_field=m_home_state_field))
#         outff_h.close()
# 
#       # outff_h.close()

# from s4.py
# - gen_assoc_s5: 
#   a. givne the build/s3_2_reachable_set_val/_build/todo_msg.txt, find the message that the picl bind the values to (that picl hasn't been determined); we also re-evaluate picl_eq_prev with stronger precondition (that constrain the in_msg_type_set); the original gen_s4() in s4.py
# - gen_assoc_s6: 
#   a. assemble per upath so far for those initiati transaction
#   b. outgoing message set, we want to see what value (which picl) does it get its value from
#       - since there's only one set of out msg per picl set, we omit constraining in the precondition
#   c. returned value check 
# - gen_assoc_s7:
#   - collect result for b. 
#       - [  ] whats remain for core-upath: 2) returned value (i.e., c.)) 3) core id for the dst/src  (d.))
# 

################################################################################
#   c. [ ] return value sources, and if picl set does return value 
#         -> could this be a livelock check? 
#   d. [ ] for each possibility in the cross product of sent and receive message type set (along with the src/dst), we find for those to/from core, we see if the core are the same or different
import fire
from collections import OrderedDict
import pickle
from pprint import pprint
from gconst import *
from util import *
import itertools
import subprocess
import os 
import sys
import re
from common_templates import *
from s4_util import * 
sys.path.append("util")
from parse_trace import *
from code_gen.parse_rules import *

if sys.version_info < (3, 6):
  sys.exit(1)

# build_dir="past_builds/MSI_fixed_build"
build_dir="build"
with open(f"{build_dir}/s3_2_reachable_set_val/_build/res.pkl", "rb") as f:
  picl_set_data_res = pickle.load(f)

max_len = 0
assert(os.path.exists(f"{build_dir}/s1_2_transition/_build/todo.txt"))
todo_list = []
with open(f"{build_dir}/s1_2_transition/_build/todo.txt", "r") as f:
  for ln in f:
    aset = ln[:-1].split(",")
    todo_list.append(aset)
    if len(aset) > max_len:
      max_len = len(aset)
assert_assoc_msgsrc_state = '''
invariant "ASSERT_{state}_{req}_rset_{idx}"
(tracked & !start & {reachable_set}
{msg_set}
) ->
(
chk);
'''
# TODO check the msg type to be {msgtype} to update prevMsgVal
obs_mtype_template = '''
if (start & !isundefined(cur_node) & cur_node = selc) then
  msg_{prefix}_set[{{msg_var}}.{m_msg_type_field}] := true;
  if ({{msg_var}}.{m_msg_type_field} = {tar_type}) then
    prevMsgVal := {{msg_var}}.{m_msg_cl_field};
  endif;
endif;
'''

obs_mtype_no_val_template = '''
if (start & !isundefined(cur_node) & cur_node = selc) then
  msg_{prefix}_set[{{msg_var}}.{m_msg_type_field}] := true;
endif;
'''

block_record = '''
if ({m_proc_selc}.{m_proc_state_field} = {tar_state} & prevProcVal != {m_proc_selc}.{m_proc_cl_field}) then
  val_chk := true; 
  assert ({m_proc_selc}.{m_proc_state_field} != prevProcs) "NO PERMISSION STATE CHANGE?";
endif;
'''
val_under_msg_set_template = '''
invariant "{state}_{req}_rset_{idx}"
(tracked & !start & {reachable_set}
{msg_set}) ->
!(val_chk = true); 
-- violation: {ele} is in the reachable_set and change value is possible
'''

arg_under_msg_set_template = '''
invariant "{state}_{req}_rset_{idx}"
(tracked & !start & {reachable_set}
{msg_set}) ->
(val_chk = true); 
-- violation: {ele} is in the reachable_set and change value is possible
'''

req_val_record = '''
if ({m_proc_selc}.{m_proc_state_field} = {tar_state}) then 
  assert (trackReq.vld) "not vld trackReq";
  val_chk := (trackReq.tp = {req_type} & {m_proc_selc}.{m_proc_cl_field} = trackReq.cl);
endif;
'''

with open(f"{build_dir}/s1_3_global_msg/_build/aggdict.pkl", "rb") as f:
  g_msg_dir = pickle.load(f)
dst_always_defined = g_msg_dir['dst_always_defined']
def get_todo_msg_type():
  with open(f"{build_dir}/s1_3_global_msg/_build/aggdict.pkl", "rb") as f:
    g_msg_dir = pickle.load(f)
  # sent
  src_dst_mtype = {'sent': {}, 'rec': {}}
  # dst_always_defined = g_msg_dir['dst_always_defined']
  for mtype, v in g_msg_dir.items():
    if mtype == "dst_always_defined":
      continue
    src_dst_mtype['sent'][mtype] = []
    src_dst_mtype['rec'][mtype] = []
    for direction, val in v.items():
      if f"from_{m_proc_iter_type}" in direction and val:
        if f"to_{m_proc_iter_type}" in direction:
          src_dst_mtype['sent'][mtype].append('core')
        else:
          src_dst_mtype['sent'][mtype].append('home')
      if f"to_{m_proc_iter_type}" in direction and val:
        if f"from_{m_proc_iter_type}" in direction:
          src_dst_mtype['rec'][mtype].append('core')
        else:
          src_dst_mtype['rec'][mtype].append('home')
  return src_dst_mtype
def gen_assoc_s5():
  # design_file_limited_fv_tmp = "/Users/yaohsiao/work/coh_syn_dev/murphi/protocols/fv/msi_fv_envs/msi.fvt.s4.m"
  # a. givne the build/s3_2_reachable_set_val/_build/todo_msg.txt, find the message that the picl bind the values to (that picl hasn't been determined)
  with open(f"{build_dir}/s4_3_v2_src_dst/out/aggdict.pkl", "rb") as f:
    aggregate = pickle.load(f)

  src_dst_mtype = get_todo_msg_type()
  # for each rec-sent msg type set
  # we check the src/dst
  for k, cur_val in aggregate.items():
    (state, req, idx) = k
    aset_arr = cur_val['rset']
    # we still have another degree of freedom to find  
    if len(cur_val['sent']) > 1 and len(cur_val['rec']) > 1:
      assert(0)
    if not 'src_dst_comb_under_test' in cur_val:
      assert ('in_out_msg_type_set_list_w_dst_src' in cur_val)
      continue 
    
    for itm in cur_val['src_dst_comb_under_test']:
      sent_idx_msg, rec_idx_msg, combidx, combo, assignment = itm
      resff = f"{build_dir}/s4_3_v2_src_dst/_build/{state}_{req}_{idx}_trace_{sent_idx_msg}_{rec_idx_msg}_{combidx}.txt"
      sent_msg_type_set = cur_val['sent'][sent_idx_msg]
      rec_msg_type_set =cur_val['rec'][rec_idx_msg]
      ret = get_res_file(resff, f"{state}_{req}_rset_{idx}", assertion=False, inline_prop=False)
      if ret:
        print("--> possible", state, req, aset_arr, sent_msg_type_set, rec_msg_type_set, assignment)
        if not 'in_out_msg_type_set_list_w_dst_src' in cur_val:
          cur_val['in_out_msg_type_set_list_w_dst_src'] = OrderedDict()
        if not (sent_idx_msg, rec_idx_msg) in cur_val['in_out_msg_type_set_list_w_dst_src']:
          cur_val['in_out_msg_type_set_list_w_dst_src'][(sent_idx_msg, rec_idx_msg)] = OrderedDict()
          cur_val['in_out_msg_type_set_list_w_dst_src'][(sent_idx_msg, rec_idx_msg)]['src_dst_comb'] = []
        m_sent = {}
        for k, v in sent_msg_type_set.items():
          if v == 'true':
            if (len(src_dst_mtype['sent'][k]) == 1):
              assert(not f"out_{k}" in assignment)
              m_sent[k] = src_dst_mtype['sent'][k][0]
            else:
              assert(f"out_{k}" in assignment)
              m_sent[k] = assignment[f"out_{k}"]
        m_rec = {}
        for k, v in rec_msg_type_set.items():
          if v == 'true':
            if (len(src_dst_mtype['rec'][k]) == 1):
              assert(not f"in_{k}" in assignment)
              m_rec[k] = src_dst_mtype['rec'][k][0]
            else:
              assert(f"in_{k}" in assignment)
              m_rec[k] = assignment[f"in_{k}"]
        print("->", m_sent, m_rec)
        cur_val['in_out_msg_type_set_list_w_dst_src'][(sent_idx_msg, rec_idx_msg)]['src_dst_comb'].append((m_sent, m_rec))
    del cur_val['src_dst_comb_under_test']
    aggregate[(state, req, idx)] = cur_val 

  with open(f"{build_dir}/s4_3_v2_src_dst/_build/aggdict_update.pkl", "wb") as f:
    pickle.dump(aggregate, f)

  stepname="s4_4_picl_val_from_msg"
  dirname = f"{build_dir}/{stepname}/out"
  os.makedirs(dirname, exist_ok = True)  

  per_transition_val_src_ff = f"{build_dir}/s1_msg_per_transition_val_src/_build/res.pkl"
  assert(os.path.exists(per_transition_val_src_ff))
  with open(per_transition_val_src_ff, "rb") as f:
    per_transtion_val_src = pickle.load(f)

  per_transition_val_chg_ff = f"{build_dir}/s1_msg_per_transition_val_change/_build/res.pkl"
  assert(os.path.exists(per_transition_val_chg_ff))
  with open(per_transition_val_chg_ff, "rb") as f:
    per_transition_val_chg = pickle.load(f)
  

  # in s3_... step, we check the general case (constrain rset) and found these states are those that has different value from previous state and don't always equal to the data argument of store 
  # This step: potentially they can have same value when the msg_set is constrained and therefore we check again for equal to previous value with the additional constraint 
  todo_state_per_rset = {}
  # these are state we find can possibly change and not always euqal to the argument yet   
  with open(f"{build_dir}/s3_2_reachable_set_val/_build/todo_msg.txt", "r") as f:
    for ln in f:
      k, v = ln[:-1].split(": ")
      state, req, idx, rset_ss = k.split(',')
      todo_states = v.split(";")
      todo_state_per_rset[(state, req, idx, rset_ss)] = todo_states

  for k, v in todo_state_per_rset.items():
    state, req, idx, rset_ss = k
    for todo_state in v:
      print("->", k, todo_state)
      assert ((state, req, idx) in aggregate)
      assert (rset_ss == "+".join(aggregate[(state, req, idx)]['rset']))
      cur_val = aggregate[(state, req, idx)]
      aset_arr = cur_val['rset']
      # each now is a complete upath possibility
      cur_val['in_out_msg_type_set_list_with_info'] = []

      # for each complete upath now
      for msgset_idx, msgset_idx_set in enumerate(cur_val['in_out_msg_type_set_list']):
        cur_upath = OrderedDict()
        sent_msg_type_set, rec_msg_type_set = cur_val['sent'][msgset_idx_set[0]], cur_val['rec'][msgset_idx_set[1]]
        cur_upath['sent_msg_type_set_idx'] = msgset_idx_set[0]
        cur_upath['rec_msg_type_set_idx'] = msgset_idx_set[1]
        cur_upath['sent_msg_type_set'] = sent_msg_type_set
        cur_upath['rec_msg_type_set'] = rec_msg_type_set
        cur_upath['sent_msg_type_assoc_state'] = cur_val['assoc_map']['sent']
        cur_upath['rec_msg_type_assoc_state'] = cur_val['assoc_map']['rec']
        # the property doesn't add checks in precondition on the sent set
        assert(len(cur_val['sent']) == 1)

        red_rec_msg_type = tuple(sorted([k for k, v in rec_msg_type_set.items() if v == 'true']))
        assert(red_rec_msg_type in cur_val['assoc_map']['rec'])
        prev_state = cur_val['rset'][cur_val['rset'].index(todo_state) - 1]
        print("\t\t -> a upath", cur_val['assoc_map']['rec'][red_rec_msg_type], ":::", prev_state, todo_state)
        print("\t\t", per_transtion_val_src[prev_state][todo_state])
        msg_val_write = False
        no_val_change = False
        # 1. assert that {todo_state} get the value from the {msgtype}, which is assoc. with prev_state of {todo_state}
        for msgtype, assoc_states in cur_val['assoc_map']['rec'][red_rec_msg_type].items():
          if msgtype in sent_msg_type_set and sent_msg_type_set[msgtype] == "true":
            # for snooping 
            send_rec_msg_type = tuple(sorted([k for k, v in sent_msg_type_set.items() if v == 'true']))
            if aset_arr[0] in cur_val['assoc_map']['sent'][send_rec_msg_type][msgtype]:
              print("TODO skipping ... !! msgtype ", state, req, idx, msgtype,aset_arr, "in sent set", cur_val['assoc_map']['sent'])
              assert(not dst_always_defined)
              continue

          if prev_state in assoc_states:
            if msgtype in req_msg_types_with_data or msgtype in resp_msg_types_w_data: 
              if per_transtion_val_src[prev_state][todo_state][msgtype]:
                msg_val_write = True
              elif prev_state in per_transition_val_chg and todo_state in per_transition_val_chg[prev_state] and per_transition_val_chg[prev_state][todo_state][msgtype]:
                no_val_change = True
              else:
                outff = f"{dirname}/{state}_{req}_{idx}_{msgset_idx}_{msgtype}.m"
                outff_h = open(outff, "w")
                # set up the rset and msg in/rec set
                blk_start = f"if (cur_state = {todo_state}) then chk := (!isundefined(prevMsgVal) & {m_proc_selc}.{m_proc_cl_field} = prevMsgVal); endif;\n"

                cfg = {"track_req": True, "prevState": True, "prevStateVal": False, "rset": {"num": max_len, "state_type_name": m_proc_state_type, "m_proc_selc": m_proc_selc, "m_proc_state_field": m_proc_state_field, "stable_state_df": "|".join([f"cur_state = {s}" for s in all_cc_stable_states]), "block_within_start": blk_start}, f"msg_rec": True, "cur_node": True}
                additional_var = {
                  "prevMsgVal": (m_val_type_name, "undefine prevMsgVal;\n", "undefine prevMsgVal;\n"), 
                  "chk": ("boolean", "chk := false;\n", ""), 
                  }
                cfg["RECEIVING"] = obs_mtype_template.format(m_msg_type_field=m_msg_type_field, prefix="rec", m_msg_cl_field=m_msg_cl_field, tar_type=msgtype) 
                parse_murphi_model(coh_model_file, nodes_iter_types, outff_h, cfg, additional_var=additional_var)

                outff_h.write(track_template_ff(state, req, m_req_type_field, m_proc_state_field = m_proc_state_field, isEntry = False, withTrackReq = False, msg = False, m_msg_type_field = m_msg_type_field))
                msg_set_ss = []
                for m_, v in rec_msg_type_set.items():
                  msg_set_ss.append(f"msg_rec_set[{m_}] = {v}")
                # cover (rset plus msgset "with the src/dst for the todo_mtype_<>  be core/home as defined by this assignment ")
                outff_h.write(assert_assoc_msgsrc_state.format(state=state, req=req, idx=idx, reachable_set=get_s_from_rset(aset_arr), msg_set="(" + " & ".join(msg_set_ss) + ")"))
                outff_h.close()

        #################################################################################
        # 2. we check again for value changes with msg_rec_set constraint added
        if not msg_val_write and not no_val_change: 
          outff = f"{dirname}/{state}_{req}_{idx}_{msgset_idx}_{todo_state}_val_change.m"
          outff_h = open(outff, "w")
          # set up the rset and msg in/rec set

          # check at todo_state  
          blk_start = block_record.format(m_proc_selc=m_proc_selc, m_proc_state_field=m_proc_state_field, tar_state=todo_state, m_proc_cl_field=m_proc_cl_field)

          cfg = {"track_req": True, "prevState": True, "prevStateVal": False, "rset": {"num": max_len, "state_type_name": m_proc_state_type, "m_proc_selc": m_proc_selc, "m_proc_state_field": m_proc_state_field, "stable_state_df": "|".join([f"cur_state = {s}" for s in all_cc_stable_states]), "block_within_start": blk_start}, f"msg_rec": True, "cur_node": True}
          additional_var = {
            "prevProcVal": (m_val_type_name, "undefine prevProcVal;\n", f"prevProcVal := {m_proc_selc}.{m_proc_cl_field};\n"), 
            "val_chk": ("boolean", "val_chk := false;\n", ""), 
            }

          cfg["RECEIVING"] = obs_mtype_no_val_template.format(m_msg_type_field=m_msg_type_field, prefix="rec", m_msg_cl_field=m_msg_cl_field)

          parse_murphi_model(coh_model_file, nodes_iter_types, outff_h, cfg, additional_var=additional_var)

          outff_h.write(track_template_ff(state, req, m_req_type_field, m_proc_state_field = m_proc_state_field, isEntry = False, withTrackReq = False, msg = False, m_msg_type_field = m_msg_type_field))
          msg_set_ss = []
          for m_, v in rec_msg_type_set.items():
            msg_set_ss.append(f"msg_rec_set[{m_}] = {v}")
          # outff_h.write(assert_assoc_msgsrc_state.format(state=state, req=req, idx=idx, reachable_set=get_s_from_rset(aset_arr), msg_set="(" + " & ".join(msg_set_ss) + ")"))
          # cover (rset plus msgset "with the src/dst for the todo_mtype_<>  be core/home as defined by this assignment ")
          outff_h.write(val_under_msg_set_template.format(state=state, req=req, m_proc_state_field=m_proc_state_field, ele=todo_state, idx=idx, reachable_set=get_s_from_rset(aset_arr), msg_set="(" + " & ".join(msg_set_ss) + ")"))
          outff_h.close()

        # TODO 
        # val eq to data 
        #################################################################################
        # 3. we check again for value match
        if not req in type_with_args:
          continue

        if msg_val_write:
          continue
        if no_val_change:
          continue
        outff = f"{dirname}/{state}_{req}_{idx}_{msgset_idx}_{todo_state}_arg.m"
        print("HEREEE ", outff)
        outff_h = open(outff, "w")
        # set up the rset and msg in/rec set

        blk_start = req_val_record.format(m_proc_selc=m_proc_selc, m_proc_state_field=m_proc_state_field, tar_state=todo_state, req_type = req, m_proc_cl_field=m_proc_cl_field)
        # blk_start = block_record.format(m_proc_selc=m_proc_selc, m_proc_state_field=m_proc_state_field, tar_state=todo_state, m_proc_cl_field=m_proc_cl_field)

        cfg = {"track_req": True, "prevState": True, "prevStateVal": False, "rset": {"num": max_len, "state_type_name": m_proc_state_type, "m_proc_selc": m_proc_selc, "m_proc_state_field": m_proc_state_field, "stable_state_df": "|".join([f"cur_state = {s}" for s in all_cc_stable_states]), "block_within_start": blk_start}, f"msg_rec": True, "cur_node": True}
        additional_var = {
          # "prevProcVal": (m_val_type_name, "undefine prevProcVal;\n", f"prevProcVal := {m_proc_selc}.{m_proc_cl_field};\n"), 
          "val_chk": ("boolean", "val_chk := false;\n", ""), 
          "trackReq": ("CoreReq", "undefine trackReq;\n", "")
          }

        cfg["RECEIVING"] = obs_mtype_no_val_template.format(m_msg_type_field=m_msg_type_field, prefix="rec", m_msg_cl_field=m_msg_cl_field)

        parse_murphi_model(coh_model_file, nodes_iter_types, outff_h, cfg, additional_var=additional_var)

        outff_h.write(track_template_ff(state, req, m_req_type_field, m_proc_state_field = m_proc_state_field, isEntry = False, withTrackReq = True, msg = False, m_msg_type_field = m_msg_type_field))
        msg_set_ss = []
        for m_, v in rec_msg_type_set.items():
          msg_set_ss.append(f"msg_rec_set[{m_}] = {v}")
        # outff_h.write(assert_assoc_msgsrc_state.format(state=state, req=req, idx=idx, reachable_set=get_s_from_rset(aset_arr), msg_set="(" + " & ".join(msg_set_ss) + ")"))
        # cover (rset plus msgset "with the src/dst for the todo_mtype_<>  be core/home as defined by this assignment ")
        outff_h.write(arg_under_msg_set_template.format(state=state, req=req, m_proc_state_field=m_proc_state_field, ele=todo_state, idx=idx, reachable_set=get_s_from_rset(aset_arr), msg_set="(" + " & ".join(msg_set_ss) + ")"))
        outff_h.close()


def collect_previous_steps(state, req, idx, cur_upath):
  # value 
  rset = cur_upath['rset']
  k = (state, req, idx, "+".join(rset))
  assert(k in picl_set_data_res['val_no_change'])
  cur_upath['picl_val_eq_prev'] = []
  cur_upath['picl_val_eq_inmsg'] = []
  cur_upath['picl_val_eq_inmsg_types'] = []
  no_change_ele = picl_set_data_res['val_no_change'][k]
  for ele in rset:
    cur_upath['picl_val_eq_prev'].append(ele in no_change_ele)
    cur_upath['picl_val_eq_inmsg'].append(False)
    cur_upath['picl_val_eq_inmsg_types'].append(None)

  if req in type_with_args:
    assert(k in picl_set_data_res['val_eq_st_data'])
    cur_upath['picl_val_eq_data'] = []
    proven_req_data = picl_set_data_res['val_eq_st_data'][k]
    for ele in rset:
      cur_upath['picl_val_eq_data'].append(ele in proven_req_data)
    # key sent and rec are just the space of all possible sent/rec message set
  return cur_upath

assert_outmsg_val_src = '''
invariant "ASSERT_{state}_{req}_rset_{idx}"
(tracked & !start & {reachable_set}
true
) ->
(
chk);
'''
# it could've returned twice? 
# we check next step 
cover_rset_for_ret_state = '''
invariant "{state}_{req}_rset_{idx}"
(tracked & !start) -> 
!({reachable_set} 
true);
'''
def gen_assoc_s6():

  per_transition_val_src_ff = f"{build_dir}/s1_msg_per_transition_val_src/_build/res.pkl"
  assert(os.path.exists(per_transition_val_src_ff))
  with open(per_transition_val_src_ff, "rb") as f:
    per_transtion_val_src = pickle.load(f)

  per_transition_val_chg_ff = f"{build_dir}/s1_msg_per_transition_val_change/_build/res.pkl"
  assert(os.path.exists(per_transition_val_chg_ff))
  with open(per_transition_val_chg_ff, "rb") as f:
    per_transition_val_chg = pickle.load(f)

  # design_file_limited_fv_tmp = "/Users/yaohsiao/work/coh_syn_dev/murphi/protocols/fv/msi_fv_envs/msi.fvt.s4.m"
  # a. givne the build/s3_2_reachable_set_val/_build/todo_msg.txt, find the message that the picl bind the values to (that picl hasn't been determined)
  with open(f"{build_dir}/s4_3_v2_src_dst/_build/aggdict_update.pkl", "rb") as f:
    aggregate = pickle.load(f)
  stepname="s4_4_picl_val_from_msg"
  dirname = f"{build_dir}/{stepname}/out"

  todo_state_per_rset = {}
  with open(f"{build_dir}/s3_2_reachable_set_val/_build/todo_msg.txt", "r") as f:
    for ln in f:
      k, v = ln[:-1].split(": ")
      state, req, idx, rset_ss = k.split(',')
      todo_states = v.split(";")
      todo_state_per_rset[(state, req, idx, rset_ss)] = todo_states

  for k, cur_val in aggregate.items():
    (state, req, idx) = k
    aset_arr = cur_val['rset']
    cur_val['upaths'] = []
    for msgset_idx, msgset_idx_set in enumerate(cur_val['in_out_msg_type_set_list']):
      cur_upath = OrderedDict()
      sent_msg_type_set, rec_msg_type_set = cur_val['sent'][msgset_idx_set[0]], cur_val['rec'][msgset_idx_set[1]]
      cur_upath['sent_msg_type_set_idx'] = msgset_idx_set[0]
      cur_upath['rec_msg_type_set_idx'] = msgset_idx_set[1]
      cur_upath['rset'] = aset_arr

      red_rec_msg_type = tuple(sorted([k for k, v in rec_msg_type_set.items() if v == 'true']))
      cur_upath['rec_assoc_map'] = cur_val['assoc_map']['rec'][red_rec_msg_type]
      red_sent_msg_type = tuple(sorted([k for k, v in sent_msg_type_set.items() if v == 'true']))
      cur_upath['sent_assoc_map'] = cur_val['assoc_map']['sent'][red_sent_msg_type]
      cur_upath['sent_msg_type_set'] = sent_msg_type_set
      cur_upath['rec_msg_type_set'] = rec_msg_type_set
      if not 'in_out_msg_type_set_list_w_dst_src' in cur_val:
        print("===>", aset_arr, state, req, idx, msgset_idx_set, sent_msg_type_set, rec_msg_type_set)
        assert(0)
      cur_upath['in_out_msg_src_dst_comb'] = cur_val['in_out_msg_type_set_list_w_dst_src'][msgset_idx_set]['src_dst_comb']
      # cur_upath['sent_msg_type_assoc_state'] = cur_val['assoc_map']['sent']
      # cur_upath['rec_msg_type_assoc_state'] = cur_val['assoc_map']['rec']

      # the picl_val_<> are from constraining only the rset  
      cur_upath = collect_previous_steps(state, req, idx, cur_upath)

      # the property doesn't add checks in precondition on the sent set
      assert(len(cur_val['sent']) == 1)
      cur_val['upaths'].append(cur_upath) 
    aggregate[(state,req, idx)] = cur_val

  for k, v in todo_state_per_rset.items():
    state, req, idx, rset_ss = k
    cur_val = aggregate[(state,req, idx)]
    aset_arr = cur_val['rset']
    for todo_state in v:
      print("->", k, todo_state)
      assert ((state, req, idx) in aggregate)
      assert (rset_ss == "+".join(aggregate[(state, req, idx)]['rset']))
      # each now is an almost complete upath possibility
      # missing component is msg_dst_and_src
      # TODO: we here assume in regardles of msg_dst_and_src combination, the value should only be dependent on the message type set
      is_src_inmsg = False
      for msgset_idx, msgset_idx_set in enumerate(cur_val['in_out_msg_type_set_list']):
        cur_upath = cur_val['upaths'][msgset_idx]
        # the todo_state must be that we find it generally can change (and not necessarily equal to the argument)
        sent_msg_type_set, rec_msg_type_set = cur_val['sent'][msgset_idx_set[0]], cur_val['rec'][msgset_idx_set[1]]

        red_rec_msg_type = tuple(sorted([k for k, v in rec_msg_type_set.items() if v == 'true']))
        assert(red_rec_msg_type in cur_val['assoc_map']['rec'])
        prev_state = cur_val['rset'][cur_val['rset'].index(todo_state) - 1]
        print("\t\t -> a upath", cur_val['assoc_map']['rec'][red_rec_msg_type], ":::", prev_state)

        todo_state_idx = aset_arr.index(todo_state)
        msg_val_write = False
        no_val_change = False
        ret2 = False
        resff = "N/A"
        for msgtype, assoc_states in cur_val['assoc_map']['rec'][red_rec_msg_type].items():
          if msgtype in sent_msg_type_set and sent_msg_type_set[msgtype] == "true":
            # for snooping
            send_rec_msg_type = tuple(sorted([k for k, v in sent_msg_type_set.items() if v == 'true']))
            if aset_arr[0] in cur_val['assoc_map']['sent'][send_rec_msg_type][msgtype]:
              print("TODO skipping ... !! msgtype ", msgtype, "in sent set", cur_val['assoc_map']['sent'])
              continue

          if prev_state in assoc_states:
            if msgtype in req_msg_types_with_data or msgtype in resp_msg_types_w_data: 
              if per_transtion_val_src[prev_state][todo_state][msgtype]:
                msg_val_write = True
                cur_upath['picl_val_eq_inmsg'][todo_state_idx] = True #is_src_inmsg
                cur_upath['picl_val_eq_inmsg_types'][todo_state_idx] = msgtype
                cur_upath['picl_val_eq_prev'][todo_state_idx] = False
                if req in type_with_args:
                  cur_upath['picl_val_eq_data'][todo_state_idx] = False
              elif prev_state in per_transition_val_chg and \
                   todo_state in per_transition_val_chg[prev_state] and \
                   msgtype in per_transition_val_chg[prev_state][todo_state] and \
                   per_transition_val_chg[prev_state][todo_state][msgtype]:
                no_val_change = True
                cur_upath['picl_val_eq_inmsg'][todo_state_idx] = False
                cur_upath['picl_val_eq_prev'][todo_state_idx] = True 
                if req in type_with_args:
                  assert(todo_state_idx >= 1)
                  cur_upath['picl_val_eq_data'][todo_state_idx] = cur_upath['picl_val_eq_data'][todo_state_idx-1]
              else:
                # assert that {todo_state} get the value from the {msgtype}
                resff = f"{build_dir}/{stepname}/_build/{state}_{req}_{idx}_{msgset_idx}_{msgtype}.txt"
                prop = f"ASSERT_{state}_{req}_rset_{idx}"
                is_src_inmsg = get_res_file(resff, prop, assertion=True, inline_prop=False)
                cur_upath['picl_val_eq_inmsg'][todo_state_idx] = is_src_inmsg
                if is_src_inmsg: 
                  assert(cur_upath['picl_val_eq_inmsg_types'][todo_state_idx] is None)
                  # should not be written already
                  cur_upath['picl_val_eq_inmsg_types'][todo_state_idx] = msgtype

        # if msg_val_write:
        #   cur_upath['picl_val_eq_prev'][todo_state_idx] = False
        # elif no_val_change:
        #   cur_upath['picl_val_eq_prev'][todo_state_idx] = True
        #   if todo_state_idx == 0:
        #     cur_upath['picl_val_eq_inmsg'][todo_state_idx] = False
        #     if req in type_with_args:
        #       cur_upath['picl_val_eq_data'][todo_state_idx] = False
        #   else:
        #     cur_upath['picl_val_eq_inmsg'][todo_state_idx] = cur_upath['picl_val_eq_inmsg'][todo_state_idx - 1]
        #     if req in type_with_args:
        #       cur_upath['picl_val_eq_data'][todo_state_idx] = cur_upath['picl_val_eq_data'][todo_state_idx - 1]
        if not msg_val_write and not no_val_change:
          resff = f"{build_dir}/{stepname}/_build/{state}_{req}_{idx}_{msgset_idx}_{todo_state}_val_change.txt"
          prop = f"{state}_{req}_rset_{idx}" # can change
          ret2 = get_res_file(resff, prop, assertion=False, inline_prop=False)
          cur_upath['picl_val_eq_prev'][todo_state_idx] = not ret2

        if req in type_with_args:
          if not msg_val_write and not no_val_change:
            resff = f"{build_dir}/{stepname}/_build/{state}_{req}_{idx}_{msgset_idx}_{todo_state}_arg.txt"
            prop = f"{state}_{req}_rset_{idx}" 
            ret3 = get_res_file(resff, prop, assertion=True, inline_prop=False)
            cur_upath['picl_val_eq_data'][todo_state_idx] = ret3

  
        # print(f"\t\t\t -> inmsg ({msgtype}? ", is_src_inmsg, "val_change?", ret2, 'eq_prev?', cur_upath['picl_val_eq_prev'][todo_state_idx], resff)
        # if ((not ret) and ret2) or (ret and (not ret2)):
        #   print("missing some data resp msg types ??????")
        #   # raise Exception("???")
        #   # assert(0)
        # add check 
        cur_val['upaths'][msgset_idx] = cur_upath
      aggregate[(state,req, idx)] = cur_val
  for k, v in todo_state_per_rset.items():
    state, req, idx, rset_ss = k
    cur_val = aggregate[(state,req, idx)]
    aset_arr = cur_val['rset']
    for msgset_idx, msgset_idx_set in enumerate(cur_val['in_out_msg_type_set_list']):
      cur_upath = cur_val['upaths'][msgset_idx]
      print(state, req, idx, rset_ss, msgset_idx)
      pprint(cur_upath)
      print("===> eq prev ", cur_upath['picl_val_eq_prev'])
      print("===> eq inms ", cur_upath['picl_val_eq_inmsg'])
      if 'picl_val_eq_data' in cur_upath:
        print("===> eq data ", cur_upath['picl_val_eq_data'])
      for idx in range(len(aset_arr)): 
        if cur_upath['picl_val_eq_prev'][idx]:
          if idx == 0: 
            assert(cur_upath['picl_val_eq_inmsg'][idx] == False)
            if 'picl_val_eq_data' in cur_upath:
              assert(cur_upath['picl_val_eq_data'][idx] == False)
          else:
            assert(cur_upath['picl_val_eq_inmsg'][idx] == cur_upath['picl_val_eq_inmsg'][idx-1])
            if 'picl_val_eq_data' in cur_upath:
              assert(cur_upath['picl_val_eq_data'][idx] == cur_upath['picl_val_eq_data'][idx-1])
        else:
          if 'picl_val_eq_data' in cur_upath:
            assert(cur_upath['picl_val_eq_inmsg'][idx] ^ cur_upath['picl_val_eq_data'][idx])
          else:
            assert(cur_upath['picl_val_eq_inmsg'][idx])
            # otherwise we miss data resp msg type??? 
          # aggregate[(state,req, idx)] = cur_val
      # 
    with open(f"{build_dir}/{stepname}/_build/res.pkl", "wb") as f:
      pickle.dump(aggregate, f) 
    # for tar_state in v:
    #   # prev
    #   pass

  stepname="s4_5_msg_val_from_picl"
  dirname = f"{build_dir}/{stepname}/out"
  os.makedirs(dirname, exist_ok = True)  

  transition_msg_map = None
  transition_map_file = f"{build_dir}/s1_msg_per_transition_cl/_build/res.pkl"
  if os.path.exists(transition_map_file):
    with open(transition_map_file, "rb") as f:
      transition_msg_map = pickle.load(f) 

  # we check which picl sources value for out going message's value
  # for getting out going message value to be cache line 
  for k, cur_val in aggregate.items():
    state, req, idx = k
    aset_arr = cur_val['rset']
    assert(len(cur_val['sent']) == 1)
    sent_msg_type_set = cur_val['sent'][0]
    red_sent_msg_type = tuple(sorted([k for k, v in sent_msg_type_set.items() if v == 'true']))
    assoc_state_map = cur_val['assoc_map']['sent'][red_sent_msg_type]
    for mtype in red_sent_msg_type:
      if not mtype in req_msg_types_with_data and not mtype in resp_msg_types_w_data:
        continue
      print("==>", mtype)
      assoc_state = assoc_state_map[mtype][0] # mtype is sent out concurrently with assoc_state
      sent_state_idx = aset_arr.index(assoc_state) + 1
      find_transition_resolve = False 
      if transition_msg_map is not None:
        tmpstate = ([state] + aset_arr)[sent_state_idx-1]
        if tmpstate in transition_msg_map and assoc_state in transition_msg_map[tmpstate]:
          sent_res_ = transition_msg_map[tmpstate][assoc_state]
          if mtype in sent_res_:
            find_transition_resolve = True
      if find_transition_resolve:
        continue
      print("==>", mtype, state, req, idx) 
      # the value for mtype can only be from state whose index < sent_state_idx
      for cur_idx in range(sent_state_idx):
        # TODO if no change then skip  picl_set_data_res['val_no_change'][(state, req, idx, "+".join(aset_arr))]
        tar_state = ([state] + aset_arr)[cur_idx]
        outff = f"{dirname}/{state}_{req}_{idx}_{mtype}_{cur_idx}.m"
        outff_h = open(outff, "w")

        blk_s = ""
        if tar_state != aset_arr[-1]:
          blk_s = f"if (cur_state = {tar_state}) then \n tarMsgVal := {m_proc_selc}.{m_proc_cl_field}; endif;"
        cfg = {"track_req": True, "prevState": True, "prevStateVal": True, "rset": {"num": max_len, "state_type_name": m_proc_state_type, "m_proc_selc": m_proc_selc, "m_proc_state_field": m_proc_state_field, "stable_state_df": "|".join([f"cur_state = {s}" for s in all_cc_stable_states]), "block_within_start": blk_s}, "cur_node": True}

        initial_state = ""
        if cur_idx == 0:
          initial_state = f'''
          if (!isundefined(cur_node) & cur_node = selc & {{msg_var}}.{m_msg_type_field} = {mtype}) then \n prevMsgVal := {{msg_var}}.{m_msg_cl_field};\n endif;
          '''
        cfg['SENDING'] = f'''
          {initial_state}
          if (start & !isundefined(cur_node) & cur_node = selc & {{msg_var}}.{m_msg_type_field} = {mtype}) then
            chk := (!isundefined(tarMsgVal) & {{msg_var}}.{m_msg_cl_field} = tarMsgVal);
          endif;
        '''
        additional_var = {"chk": ("boolean", "chk := false;\n", ""), 
        "tarMsgVal": (m_val_type_name, "undefine tarMsgVal;\n", "")
        }
        if cur_idx == 0:
          additional_var['prevMsgVal'] = (m_val_type_name, "undefine prevMsgVal;\n", "undefine prevMsgVal;\n")
        else:
          additional_var['prevMsgVal'] = (m_val_type_name, "undefine prevMsgVal;\n", "")
        parse_murphi_model(coh_model_file, nodes_iter_types, outff_h, cfg, additional_var=additional_var)
        
        msg_s_cond = ""
        if cur_idx == 0:
          msg_s_cond = f"if (prevProcs = {tar_state}) then \n chk := (!isundefined(prevMsgVal) & prevMsgVal = prevStateVal);\n endif;\n"

        outff_h.write(track_template_ff(state, req, m_req_type_field, m_proc_state_field = m_proc_state_field, isEntry = False, withTrackReq = False, msg = False, m_msg_type_field = m_msg_type_field, msg_s_cond = msg_s_cond))
        outff_h.write(assert_outmsg_val_src.format(state=state, req=req,idx=idx, reachable_set=get_s_from_rset(aset_arr)))
        outff_h.close()

no_txn_template = '''
invariant "{state}_accept_and_perform_{req}"
  (!IsUndefined(prevProcs) & (prevProcs = {state})) ->
(IsUndefined(prevProcReq.{m_req_type_field}) | (prevProcReq.{m_req_type_field} != {req}));
'''
def gen_assoc_s7():
  # collect 
  with open(f"{build_dir}/s4_4_picl_val_from_msg/_build/res.pkl", "rb") as f:
    aggregate = pickle.load(f)
  transition_msg_map = None
  transition_map_file = f"{build_dir}/s1_msg_per_transition_cl/_build/res.pkl"
  if os.path.exists(transition_map_file):
    with open(transition_map_file, "rb") as f:
      transition_msg_map = pickle.load(f)

  stepname="s4_5_msg_val_from_picl"
  
  # for getting out going message value
  for k, cur_val in aggregate.items():
    state, req, idx = k
    aset_arr = cur_val['rset']
    assert(len(cur_val['sent']) == 1)
    sent_msg_type_set = cur_val['sent'][0]
    red_sent_msg_type = tuple(sorted([k for k, v in sent_msg_type_set.items() if v == 'true']))
    assoc_state_map = cur_val['assoc_map']['sent'][red_sent_msg_type]
    cur_val['out_msg_data_src'] = OrderedDict()
    print("-->", state, req, idx, [state]+aset_arr)
    for mtype in red_sent_msg_type:
      if (not mtype in req_msg_types_with_data) and (not mtype in resp_msg_types_w_data):
        continue
      assoc_state = assoc_state_map[mtype][0] # mtype is sent out concurrently with assoc_state
      sent_state_idx = aset_arr.index(assoc_state) + 1

      find_transition_resolve = False 
      if transition_msg_map is not None:
        tmpstate = ([state] + aset_arr)[sent_state_idx-1]
        if tmpstate in transition_msg_map and assoc_state in transition_msg_map[tmpstate]:
          sent_res_ = transition_msg_map[tmpstate][assoc_state]
          if mtype in sent_res_:
            find_transition_resolve = True
            cur_val['out_msg_data_src'][mtype] = tmpstate 
            print("===>", mtype, "at", assoc_state, ", equ", tmpstate)
      if find_transition_resolve:
        continue
      # the value for mtype can only be from state whose index < sent_state_idx
      at_least_one = False
      match_state = None
      print("\t", mtype, ":")
      find_transition_resolve = False
      proven_ = True 
      for cur_idx in range(sent_state_idx):
        tar_state = ([state] + aset_arr)[cur_idx]
        resff = f"{build_dir}/{stepname}/_build/{state}_{req}_{idx}_{mtype}_{cur_idx}.txt"
        prop = f"ASSERT_{state}_{req}_rset_{idx}"
        ret = get_res_file(resff, prop, assertion=True, inline_prop=False)
        ret2 = get_res_file_stats(resff, prop, assertion=True, inline_prop=False)
        print("\t\t-->", state, req, idx, mtype, "value from ", tar_state, "?", ret)
        proven_ = proven_ and (ret2[0] is not None and ret)
        if ret2[0] is None: 
          print("\t\t==> undetermined", resff)
          if transition_msg_map is not None:
            nxt_state = ([state] + aset_arr)[cur_idx + 1]
            if tar_state in transition_msg_map and nxt_state in transition_msg_map[tar_state]:
              sent_res_ = transition_msg_map[tar_state][nxt_state]
              if mtype in sent_res_:
                print("fixed!")
                find_transition_resolve = True
        if at_least_one and ret:
          # already equal to some other state 
          stats_w_same_val_as_prev = picl_set_data_res['val_no_change'][(state, req, idx, "+".join(aset_arr))]
          assert (tar_state in stats_w_same_val_as_prev)
        if ret:
          at_least_one = True
          match_state = tar_state
          cur_val['out_msg_data_src'][mtype] = match_state
      if not at_least_one:
        print("---> fail", state, req, idx, mtype)
      if mtype in cur_val['out_msg_data_src']:
        if not proven_ and not find_transition_resolve:
          print("==> TBD!!!", mtype)

    aggregate[k] = cur_val

  os.makedirs(f"{build_dir}/{stepname}/_build", exist_ok = True)  
  with open(f"{build_dir}/{stepname}/_build/res.pkl", "wb") as f:
    pickle.dump(aggregate, f)

  # we check the returned value is at which state, should be the last state of the transaction 
  # we assert the picl's value at the moment otherwise should be innmsg 
  stepname="s4_6_ret_val"
  dirname = f"{build_dir}/{stepname}/out"
  os.makedirs(dirname, exist_ok = True)  
  
  # based on the tagging 
  # `#RETLD,CL`: this state we return the load with "CL" value, i.e., the cacheline's value 
  # `#RETLD,<>`: something else 
  # for getting out going message value

  # this step we use the trace to see if exists a state in each upath that returns value (based on the annotation. 
  # although we can turn this into a static check we currently just use model checking 
  for k, cur_val in aggregate.items():
    state, req, idx = k
    if not req in req_is_read:
      continue 
    aset_arr = cur_val['rset']
    assert(len(cur_val['sent']) == 1)
    # this particular rset 
    # we first see what state does it returned 
    outff = f"{dirname}/{state}_{req}_{idx}_trace.m"
    outff_h = open(outff, "w")

    blk_start = ""

    cfg = {"track_req": True, "prevState": True, "prevStateVal": False, "rset": {"num": max_len, "state_type_name": m_proc_state_type, "m_proc_selc": m_proc_selc, "m_proc_state_field": m_proc_state_field, "stable_state_df": "|".join([f"cur_state = {s}" for s in all_cc_stable_states]), "block_within_start": blk_start}, "cur_node": True}
    additional_var = {
      "just_ret": ("boolean", "just_ret := false;\n", "just_ret := false;\n"),
      "state_ret_val": (m_proc_state_type, "undefine state_ret_val;\n", f"if (just_ret) then state_ret_val := {m_proc_selc}.{m_proc_state_field};\n endif;\n"), 
      }
    # RETLD could be before or after the transition to the new state for which we associated with  
    # cfg["RETLD"] = f"if (start & !isundefined(cur_node) & cur_node = selc) then \n if (!isundefined(state_ret_val)) then undefine state_ret_val; \n else state_ret_val := {m_proc_selc}.{m_proc_state_field}; \n endif; \n endif; \n" 
    cfg["RETLD"] = f"if (start & !isundefined(cur_node) & cur_node = selc) then \n if (!isundefined(state_ret_val)) then undefine state_ret_val; \n else just_ret := true;\n endif;\n endif;\n"
    # state_ret_val := {m_proc_selc}.{m_proc_state_field}; \n endif; \n endif; \n" 
    #obs_mtype_template.format(m_msg_type_field=m_msg_type_field, prefix="rec", m_msg_cl_field=m_msg_cl_field) 
    parse_murphi_model(coh_model_file, nodes_iter_types, outff_h, cfg, additional_var=additional_var)


    outff_h.write(track_template_ff(state, req, m_req_type_field, m_proc_state_field = m_proc_state_field, isEntry = False, withTrackReq = False, msg = False, m_msg_type_field = m_msg_type_field, msg_s_cond = ""))
    # this iteration we get the trace 
    outff_h.write(cover_rset_for_ret_state.format(state=state, req=req,idx=idx, reachable_set=get_s_from_rset(aset_arr)))

  # we handle those not initiating transaction
  with open(f"{build_dir}/s4_3_v2_src_dst/out/aggdict_s1_to_s3.pkl", "rb") as f:
    aggregate_s1_to_s3 = pickle.load(f)
  for k, v in aggregate_s1_to_s3.items():
    state, req = k
    if (not req in req_is_read) or (v['txn_init']):
      continue 
    
    # accept and perform 
    # return value must be the state 
    outff = f"{dirname}/{state}_{req}_no_txn_ini_trace.m"
    outff_h = open(outff, "w")


    blk_start = ""

    cfg = {"track_req": True, "prevState": True, "prevStateVal": False, "cur_node": True}
    additional_var = {
      "state_ret_val": (m_proc_state_type, "undefine state_ret_val;\n", "")
      }
    cfg["RETLD"] = f"undefine state_ret_val; if (!isundefined(cur_node) & cur_node = selc) then state_ret_val := {m_proc_selc}.{m_proc_state_field}; \n endif; \n"
    #obs_mtype_template.format(m_msg_type_field=m_msg_type_field, prefix="rec", m_msg_cl_field=m_msg_cl_field) 
    parse_murphi_model(coh_model_file, nodes_iter_types, outff_h, cfg, additional_var=additional_var)


    # outff_h.write(track_template_ff(state, req, m_req_type_field, m_proc_state_field = m_proc_state_field, isEntry = False, withTrackReq = False, msg = False, m_msg_type_field = m_msg_type_field, msg_s_cond = ""))
    # this iteration we get the trace 
    # outff_h.write(cover_rset_for_ret_state.format(state=state, req=req,idx=idx, reachable_set=get_s_from_rset(aset_arr))) 

    outff_h.write(no_txn_template.format(state=state, req=req, m_proc_state_field=m_proc_state_field, m_req_type_field=m_req_type_field))
    outff_h.close()
  


  # 
def get_ret_state(resff):
  return_state = None
  with open(resff, "r") as f:
    found_last_state = False
    for line in f:
      if "The last state" in line:
        found_last_state = True
        continue
    
      if found_last_state:
        state_ret_val_match = re.search(r"state_ret_val:(\w+)", line)
        if state_ret_val_match:
          return_state = state_ret_val_match.group(1)
          break
  return return_state

def gen_assoc_s8():
  # with open(f"{build_dir}/s4_4_picl_val_from_msg/_build/res.pkl", "rb") as f:
  with open(f"{build_dir}/s4_5_msg_val_from_picl/_build/res.pkl", "rb") as f:
    aggregate = pickle.load(f)
  # previous step only get the possible state that a upath return value 
  # this step we get to see if there is multiple state that returns value 

  # stepname="s4_7_ret_val_two"
  # dirname = f"{build_dir}/{stepname}/out"
  # os.makedirs(dirname, exist_ok = True)  

  # this step we only see if a) what state does eahc upath return the value and b) if each txn has a returned state  
  # although we can turn this into a static check we currently just 
  for k, cur_val in aggregate.items():
    state, req, idx = k
    if not req in req_is_read:
      continue 
    aset_arr = cur_val['rset']
    assert(len(cur_val['sent']) == 1)
    # this particular rset 
    # we first see what state does it returned 
    resff = f"{build_dir}/s4_6_ret_val/_build/{state}_{req}_{idx}_trace.txt"
    _ = get_res_file(resff, None)
    return_state = get_ret_state(resff)
    if return_state is None:
      print("===> !! No returned value found??", state, req, idx, return_state, aset_arr)
    if (return_state is not None and return_state.lower() == "undefined"):
      print("===> !! No returned value", state, req, idx, return_state, aset_arr)
    print("->", state, req, idx, return_state)
    cur_val['state_ret_val'] = return_state 
    aggregate[k] = cur_val
  with open(f"{build_dir}/s4_6_ret_val/_build/agg_txn_init.pkl", "wb") as f:
    pickle.dump(aggregate, f)
  # TODO: assert it is always the case? maybe the same rset we could have differing returned state potentially still 

 

  # we handle those not initiating transaction
  with open(f"{build_dir}/s4_3_v2_src_dst/out/aggdict_s1_to_s3.pkl", "rb") as f:
    aggregate_s1_to_s3 = pickle.load(f)
  for k, v in aggregate_s1_to_s3.items():
    state, req = k
    if (not req in req_is_read) or (v['txn_init']):
      continue 
    # accept and perform 
    resff = f"{build_dir}/s4_6_ret_val/_build/{state}_{req}_no_txn_ini_trace.txt"
    _ = get_res_file(resff, None)
    return_state = get_ret_state(resff) 
    if return_state is None:
      raise ValueError("===> !! No returned value", state, req, idx, return_state)
    if (return_state is not None and return_state.lower() == "undefined"):
      raise ValueError("===> !! No returned value", state, req, idx, return_state)
    print("->", state, req, idx, return_state)
    v['state_ret_val'] = return_state
    aggregate_s1_to_s3[k] = v
   
  with open(f"{build_dir}/s4_6_ret_val/_build/agg_no_txn_init.pkl", "wb") as f:
    pickle.dump(aggregate_s1_to_s3, f)

if __name__ == "__main__":
  fire.Fire()
  dump_stats()

import itertools
import os
import pickle
import sys
from collections import OrderedDict

import fire

from common_templates import *
from gconst import *
from util import *

sys.path.append("src")
from code_gen.parse_rules import *
from s4_util import *


if sys.version_info < (3, 6):
  sys.exit(1)

# build_dir="past_builds/MSI_fixed_build"
build_dir="build"
rset_msg_template = '''
invariant "{state}_{req}_rset_{idx}"
(tracked & !start & cur_idx = {tar_len}) ->
(match != {tar_len})
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


def load_todo_from_prevstep(prevstep="s3_rset_txn"):
  prevresdirname = f"{build_dir}/{prevstep}/_build"
  todo = []
  with open(f"{prevresdirname}/res.txt", "r") as f:
    st = False
    for ln in f:
      if ln.startswith("Reachable"):
        st = True
      elif ln.startswith("Unreachable"):
        st = False
      elif st:
        todo.append(tuple(ln[:-1].split(",")))
  return todo


def get_msg_sets_for_pair(transition_msg_map, s1, s2):
  if s1 in transition_msg_map and s2 in transition_msg_map[s1]:
    sent_res, rec_res = transition_msg_map[s1][s2]
    sent_res = [] if sent_res is None else sent_res
    rec_res = [] if rec_res is None else rec_res
    return sent_res, rec_res
  return [],[]


def build_match_switch_block(combo):
  block = "if (prevProcs != cur_state) then\n"
  block += "  switch match\n"
  fail_val = len(combo) + 1
  for i, sent_set in enumerate(combo):
    terms = []
    for m_, v in sent_set.items():
      terms.append(f"msg_imm_sent_set[{m_}] = {v}")
    cond = "true" if len(terms) == 0 else " & ".join(terms)
    block += f"    case {i}:\n"
    block += f"      if ({cond}) then match := match + 1; else match := {fail_val}; endif;\n"
  block += "  endswitch;\n"
  block += f" for tmpm: {msg_type_name} do msg_imm_sent_set[tmpm] := false; endfor;\n"
  block += "endif;\n"
  return block, fail_val


def gen():
  stepname = "s4_constrained"
  outdir = f"{build_dir}/{stepname}/out"
  os.makedirs(outdir, exist_ok=True)

  transition_msg_map = {}
  transition_map_file = f"{build_dir}/s1_msg_per_transition_iter/_build/res.pkl"
  if os.path.exists(transition_map_file):
    with open(transition_map_file, "rb") as f:
      transition_msg_map = pickle.load(f)

  todo = load_todo_from_prevstep(prevstep="s3_rset_txn")
  for t_ in todo:
    assert(len(t_) == 4)
    state, req, idx, asets = t_
    aset_arr = asets.split("+") if len(asets) > 0 else []
    path_states = [state] + aset_arr

    pair_sent_sets = []
    pair_rec_sets = []
    pair_labels = []
    for i in range(len(path_states) - 1):
      s1 = path_states[i]
      s2 = path_states[i + 1]
      sent_sets, rec_sets = get_msg_sets_for_pair(transition_msg_map, s1, s2)

      if len(sent_sets) == 0:
        # If no transition data is available for a pair, no constrained combo exists.
        pair_sent_sets = []
        assert(0)
        break
      pair_labels.append((s1, s2))
      pair_sent_sets.append(sent_sets)
      pair_rec_sets.append(rec_sets)

    assert(len(pair_sent_sets) > 0)
    #if len(pair_sent_sets) == 0:
    #  continue

    combo_count_send = 1
    for sent_sets in pair_sent_sets:
      combo_count_send *= len(sent_sets)
    print("==>", state, req, aset_arr, 'pair_sent', pair_sent_sets, '\n', list(itertools.product(*pair_sent_sets)), "\n", list(itertools.product(*pair_rec_sets)))
    combo_count = 1
    for rec_sets in pair_rec_sets:
      combo_count *= len(rec_sets)

    assert(combo_count != 1 ^ combo_count_send != 1)

    if (combo_count_send) > 1:
      for combo_idx, combo in enumerate(itertools.product(*pair_sent_sets)):
        
        enabled_msg_types = [[k for k, v in arr.items() if v == "true"] for arr in combo]
        # print("==>", enabled_msg_types)
        msg_type_count = OrderedDict()
        for msg_types in enabled_msg_types:
          for msg_type in msg_types:
            if not msg_type in msg_type_count:
              msg_type_count[msg_type] = 0
            msg_type_count[msg_type] += 1
        print("==>", [[k for k, v in arr.items() if v == "true"] for arr in combo])
        if any(cnt >= 3 for cnt in msg_type_count.values()):
          print("WARN", msg_type_count)
          continue
        outff = f"{outdir}/{state}_{req}_{idx}_{combo_idx}_sent.m"
        outff_h = open(outff, "w")

        match_switch_block, fail_val = build_match_switch_block(combo)
        additional_var = {
          "match": (f"0..{fail_val}", "match := 0;\n", ""),
        }

        cfg = {
          "track_req": True,
          "prevState": True,
          "prevStateVal": False,
          "prevMsgSet_sent": True,
          "rset": {
            "mode": "tar_idx",
            "state_type_name": m_proc_state_type,
            "stable_state_df": "|".join([f"cur_state = {s}" for s in all_cc_stable_states]),
            "block_within_start": match_switch_block,
            "tar_states": aset_arr,
            "tar_target_len": len(aset_arr),
          },
          "cur_node": True,
        }

        # Keep immediate message-set tracking at receiving points.
        cfg["SENDING"] = (
          "if (!isundefined(cur_node) & cur_node = selc) then\n"
          f"prevMsg := {{msg_var}}.{m_msg_type_field};\n"
          "endif;"
          "if (start & !isundefined(cur_node) & cur_node = selc) then\n"
          f"  msg_imm_sent_set[{{msg_var}}.{m_msg_type_field}] := true;\n"
          "endif;\n"
        )

        parse_murphi_model(coh_model_file, nodes_iter_types, outff_h, cfg, additional_var=additional_var)
        # outff_h.write(track_template.format(state=state, req=req, m_proc_state_field=m_proc_state_field, m_req_type_field=m_req_type_field))
        outff_h.write(track_template_ff(state, req, m_req_type_field, m_proc_state_field = m_proc_state_field, isEntry = False, withTrackReq = False, msg = True, m_msg_type_field = m_msg_type_field, msg_sent_set="msg_imm_sent_set"))
        outff_h.write(rset_msg_template.format(state=state, req=req, idx=idx, tar_len=len(aset_arr)))
        outff_h.close() 
      continue

    if (combo_count == 1):
      print(state, req, idx, asets, combo_count)
      print("1 ==>", [[k for k, v in arr[0].items() if v == "true"] for arr in pair_rec_sets])
      continue

    for combo_idx, combo in enumerate(itertools.product(*pair_rec_sets)):
      
      enabled_msg_types = [[k for k, v in arr.items() if v == "true"] for arr in combo]
      # print("==>", enabled_msg_types)
      msg_type_count = OrderedDict()
      for msg_types in enabled_msg_types:
        for msg_type in msg_types:
          if not msg_type in msg_type_count:
            msg_type_count[msg_type] = 0
          msg_type_count[msg_type] += 1
      print("==>", [[k for k, v in arr.items() if v == "true"] for arr in combo])
      if any(cnt >= 3 for cnt in msg_type_count.values()):
        print("WARN", msg_type_count)
        continue
      outff = f"{outdir}/{state}_{req}_{idx}_{combo_idx}.m"
      outff_h = open(outff, "w")

      match_switch_block, fail_val = build_match_switch_block(combo)
      additional_var = {
        "match": (f"0..{fail_val}", "match := 0;\n", ""),
      }

      cfg = {
        "track_req": True,
        "prevState": True,
        "prevStateVal": False,
        "prevMsgSet_sent": True,
        "rset": {
          "mode": "tar_idx",
          "state_type_name": m_proc_state_type,
          "stable_state_df": "|".join([f"cur_state = {s}" for s in all_cc_stable_states]),
          "block_within_start": match_switch_block,
          "tar_states": aset_arr,
          "tar_target_len": len(aset_arr),
        },
        "cur_node": True,
      }

      # Keep immediate message-set tracking at receiving points.
      cfg["RECEIVING"] = (
        "if (start & !isundefined(cur_node) & cur_node = selc) then\n"
        f"  msg_imm_sent_set[{{msg_var}}.{m_msg_type_field}] := true;\n"
        "endif;\n"
      )

      parse_murphi_model(coh_model_file, nodes_iter_types, outff_h, cfg, additional_var=additional_var)
      outff_h.write(track_template.format(state=state, req=req, m_proc_state_field=m_proc_state_field, m_req_type_field=m_req_type_field))
      outff_h.write(rset_msg_template.format(state=state, req=req, idx=idx, tar_len=len(aset_arr)))
      outff_h.close()


def _append_assoc(cur_map, msg_set, assoc_state):
  for msg_type, v in msg_set.items():
    if str(v).lower() != "true":
      continue
    if not msg_type in cur_map:
      cur_map[msg_type] = []
    if not assoc_state in cur_map[msg_type]:
      cur_map[msg_type].append(assoc_state)


def _combine_msg_sets(msg_sets):
  combined = {} #OrderedDict()
  for m in all_msg_types:
    combined[m] = "false"
  for msg_set in msg_sets:
    for msg_type, v in msg_set.items():
      if v == "true":
        combined[msg_type] = "true"
  return combined


def _enabled_tuple(msg_set):
  return tuple(sorted([msg_type for msg_type, v in msg_set.items() if str(v).lower() == "true"]))


def gen_s2():
  stepname = "s4_constrained"
  transition_msg_map = {}
  transition_map_file = f"{build_dir}/s1_msg_per_transition_iter/_build/res.pkl"
  if os.path.exists(transition_map_file):
    with open(transition_map_file, "rb") as f:
      transition_msg_map = pickle.load(f)

  aggregate = OrderedDict()
  todo = load_todo_from_prevstep(prevstep="s3_rset_txn")
  for t_ in todo:
    assert(len(t_) == 4)
    state, req, idx, asets = t_
    aset_arr = asets.split("+") if len(asets) > 0 else []
    path_states = [state] + aset_arr

    pair_sent_sets = []
    pair_rec_sets = []
    pair_labels = []
    for i in range(len(path_states) - 1):
      s1 = path_states[i]
      s2 = path_states[i + 1]
      sent_sets, rec_sets = get_msg_sets_for_pair(transition_msg_map, s1, s2)
      if len(sent_sets) == 0:
        pair_sent_sets = []
        break
      pair_labels.append((s1, s2))
      pair_sent_sets.append(sent_sets)
      pair_rec_sets.append(rec_sets)

    if len(pair_sent_sets) == 0:
      continue

    sent_combo_count = 1
    for sent_sets in pair_sent_sets:
      sent_combo_count *= len(sent_sets)
    print("-->, sent combo", sent_combo_count, state, req, idx, asets, pair_sent_sets)
    if sent_combo_count != 1:
      # assert(0)
      print("TODO")

      cur_val = OrderedDict()
      cur_val["rset"] = aset_arr
      cur_val["sent"] = []
      cur_val["rec"] = []
      cur_val["assoc_map"] = {"sent": {}, "rec": {}} #OrderedDict()}

      # rec is assumed to be unique; collect this one fixed sent-space.
      combo_rec = [rec_sets[0] for rec_sets in pair_rec_sets]
      rec_agg = _combine_msg_sets(combo_rec)
      rec_key = _enabled_tuple(rec_agg)
      cur_val["rec"].append(rec_agg)
      cur_val["assoc_map"]["rec"][rec_key] = {} #OrderedDict()
      for step_idx, sent_set in enumerate(combo_rec):
        s1, s2 = pair_labels[step_idx]
        _append_assoc(cur_val["assoc_map"]["rec"][rec_key], sent_set, s2)

      combo_count = 1
      for rec_sets in pair_sent_sets:
        combo_count *= len(rec_sets)
      if (combo_count == 1):
        # assert(0)
        combo_rec = [rec_sets[0] for rec_sets in pair_sent_sets]
        rec_agg = _combine_msg_sets(combo_rec)
        rec_key = _enabled_tuple(rec_agg)
        cur_val["sent"].append(rec_agg)
        cur_val["assoc_map"]["sent"][rec_key] = {} #OrderedDict()
        for step_idx, rec_set in enumerate(combo_rec):
          _, s2 = pair_labels[step_idx]
          _append_assoc(cur_val["assoc_map"]["sent"][rec_key], rec_set, s2)
        aggregate[(state, req, idx)] = cur_val
        continue

      seen_rec_keys = set()
      for combo_idx, combo in enumerate(itertools.product(*pair_sent_sets)):
        enabled_msg_types = [[k for k, v in arr.items() if v == "true"] for arr in combo]
        # print("==>", enabled_msg_types)
        msg_type_count = OrderedDict()
        for msg_types in enabled_msg_types:
          for msg_type in msg_types:
            if not msg_type in msg_type_count:
              msg_type_count[msg_type] = 0
            msg_type_count[msg_type] += 1
        print("==>", [[k for k, v in arr.items() if v == "true"] for arr in combo])
        if any(cnt >= 3 for cnt in msg_type_count.values()):
          print("WARN", msg_type_count)
          continue

        resff = f"{build_dir}/{stepname}/_build/{state}_{req}_{idx}_{combo_idx}_sent.txt"
        print(resff)
        assert(os.path.exists(resff))
        ret = get_res_file(resff, f"{state}_{req}_rset_{idx}", assertion=False, inline_prop=False)
        if not ret:
          continue

        combo_rec = list(combo)
        rec_agg = _combine_msg_sets(combo_rec)
        rec_key = _enabled_tuple(rec_agg)

        if not rec_key in seen_rec_keys:
          seen_rec_keys.add(rec_key)
          cur_val["sent"].append(rec_agg)
          cur_val["assoc_map"]["sent"][rec_key] = {} #OrderedDict()

        for step_idx, rec_set in enumerate(combo_rec):
          s1, s2 = pair_labels[step_idx]
          _append_assoc(cur_val["assoc_map"]["sent"][rec_key], rec_set, s2)

      aggregate[(state, req, idx)] = cur_val
      continue

    cur_val = OrderedDict()
    cur_val["rset"] = aset_arr
    cur_val["sent"] = []
    cur_val["rec"] = []
    cur_val["assoc_map"] = {"sent": {}, "rec": {}} #OrderedDict()}

    # Sent is assumed to be unique; collect this one fixed sent-space.
    sent_combo = [sent_sets[0] for sent_sets in pair_sent_sets]
    sent_agg = _combine_msg_sets(sent_combo)
    sent_key = _enabled_tuple(sent_agg)
    cur_val["sent"].append(sent_agg)
    cur_val["assoc_map"]["sent"][sent_key] = {} #OrderedDict()
    for step_idx, sent_set in enumerate(sent_combo):
      _, s2 = pair_labels[step_idx]
      _append_assoc(cur_val["assoc_map"]["sent"][sent_key], sent_set, s2)

    combo_count = 1
    for rec_sets in pair_rec_sets:
      combo_count *= len(rec_sets)
    if (combo_count == 1):
      combo_rec = [rec_sets[0] for rec_sets in pair_rec_sets]
      rec_agg = _combine_msg_sets(combo_rec)
      rec_key = _enabled_tuple(rec_agg)
      cur_val["rec"].append(rec_agg)
      cur_val["assoc_map"]["rec"][rec_key] = {} #OrderedDict()
      for step_idx, rec_set in enumerate(combo_rec):
        s1, _ = pair_labels[step_idx]
        _append_assoc(cur_val["assoc_map"]["rec"][rec_key], rec_set, s1)
      aggregate[(state, req, idx)] = cur_val
      continue

    seen_rec_keys = set()
    for combo_idx, combo in enumerate(itertools.product(*pair_rec_sets)):
      enabled_msg_types = [[k for k, v in arr.items() if v == "true"] for arr in combo]
      # print("==>", enabled_msg_types)
      msg_type_count = OrderedDict()
      for msg_types in enabled_msg_types:
        for msg_type in msg_types:
          if not msg_type in msg_type_count:
            msg_type_count[msg_type] = 0
          msg_type_count[msg_type] += 1
      print("==>", [[k for k, v in arr.items() if v == "true"] for arr in combo])
      if any(cnt >= 3 for cnt in msg_type_count.values()):
        print("WARN", msg_type_count)
        continue

      resff = f"{build_dir}/{stepname}/_build/{state}_{req}_{idx}_{combo_idx}.txt"
      print(resff)
      assert(os.path.exists(resff))
      ret = get_res_file(resff, f"{state}_{req}_rset_{idx}", assertion=False, inline_prop=False)
      if not ret:
        continue

      combo_rec = list(combo)
      rec_agg = _combine_msg_sets(combo_rec)
      rec_key = _enabled_tuple(rec_agg)

      if not rec_key in seen_rec_keys:
        seen_rec_keys.add(rec_key)
        cur_val["rec"].append(rec_agg)
        cur_val["assoc_map"]["rec"][rec_key] = {} #OrderedDict()

      for step_idx, rec_set in enumerate(combo_rec):
        s1, _ = pair_labels[step_idx]
        _append_assoc(cur_val["assoc_map"]["rec"][rec_key], rec_set, s1)

    aggregate[(state, req, idx)] = cur_val

  outdir = f"{build_dir}/{stepname}/_build"
  os.makedirs(outdir, exist_ok=True)
  with open(f"{outdir}/aggdict.pkl", "wb") as f:
    pickle.dump(aggregate, f)
  # return aggregate

assert_assoc_msgsrc_state = '''
invariant "{state}_{req}_rset_{idx}"
(tracked & !start & {reachable_set}
{msg_set}
) ->
(
!chk);
'''
def gen_s3():
  obs_mtype_template = '''
  if (!isundefined(cur_node) & cur_node = selc) then
    prevMsg := {{msg_var}}.{m_msg_type_field};
  endif;
  if (start & !isundefined(cur_node) & cur_node = selc) then
    msg_{prefix}_set[{{msg_var}}.{m_msg_type_field}] := true;
  endif;
  '''
  # we now check 
  # 2. the number of message sent/received: s1_3_global_msg, we overapproximate the number when number > 1
  #   -> most message type are 1 except likely some say Inv_Ack -> s1_3_global_msg
  # 3. find the destination/source of the message 
  #     - source: since the message.src can possibly different from the real sender we check whether the source can be core or can be home 
  # design_file_limited_fv_tmp = "/Users/yaohsiao/work/coh_syn_dev/murphi/protocols/fv/msi_fv_envs/msi.fvt.s4.m"
  stepname = "s4_3_v2_src_dst"
  dirname = f"{build_dir}/{stepname}/out"
  os.makedirs(dirname, exist_ok = True)  
  aggregate = None
  with open(f"{build_dir}/s4_constrained/_build/aggdict.pkl", "rb") as f:
    aggregate = pickle.load(f)
  
  with open(f"{build_dir}/s1_3_global_msg/_build/aggdict.pkl", "rb") as f:
    g_msg_dir = pickle.load(f)
  # sent
  todo_msg_type = {'sent': [], 'rec': []}
  src_dst_mtype = {'sent': {}, 'rec': {}}
  dst_always_defined = g_msg_dir['dst_always_defined']
  for mtype, v in g_msg_dir.items():
    if mtype == "dst_always_defined":
      continue
    src_dst_mtype['sent'][mtype] = []
    src_dst_mtype['rec'][mtype] = []
    cnt_sent, cnt_rec = 0, 0
    for direction, val in v.items():
      if f"from_{m_proc_iter_type}" in direction and val:
        cnt_sent += 1
        if f"to_{m_proc_iter_type}" in direction:
          src_dst_mtype['sent'][mtype].append('core')
        else:
          src_dst_mtype['sent'][mtype].append('home')
      if f"to_{m_proc_iter_type}" in direction and val:
        cnt_rec += 1
        if f"from_{m_proc_iter_type}" in direction:
          src_dst_mtype['rec'][mtype].append('core')
        else:
          src_dst_mtype['rec'][mtype].append('home')
    if cnt_sent >= 2:
      print(mtype, "dst can be more than one")
      todo_msg_type['sent'].append(mtype)
    if cnt_rec >= 2:
      print(mtype, "src can be more than one")
      todo_msg_type['rec'].append(mtype)
  print("todo msg type")
  pprint(todo_msg_type)

  # for each rec-sent msg type set
  # we check the src/dst to be home/core
  for k, cur_val in aggregate.items():
    (state, req, idx) = k
    # v 
    aset_arr = cur_val['rset']
    # cross product of the in msg_type_set and out msg_type_set as "almost" unique upath now 
    # we still have another degree of freedom to find  
    if len(cur_val['sent']) > 1 and len(cur_val['rec']) > 1:
      assert(0)

    # currently we only handle the case at least one of the message type set is len of 1
    for sent_idx_msg, sent_msg_type_set in enumerate(cur_val['sent']):
      todo_mtype_sent = todo_msg_type['sent']
      for rec_idx_msg, rec_msg_type_set in enumerate(cur_val['rec']):
        todo_mtype_rec = todo_msg_type['rec']
        # aset_arr + todo_mtype_sent + todo_mtype_rec -> an almost unique upath 
        # following checks the src/dst types
        if not 'in_out_msg_type_set_list' in cur_val:
          cur_val['in_out_msg_type_set_list'] = []
        # this upath features this set of message types
        cur_val['in_out_msg_type_set_list'].append((sent_idx_msg, rec_idx_msg))
        mtype_sent_prime = [k for k, v in sent_msg_type_set.items() if (k in todo_mtype_sent and v == 'true')]
        mtype_rec_prime = [k for k, v in rec_msg_type_set.items() if (k in todo_mtype_rec and v == 'true')]
        print("mtype_sent_prime", mtype_sent_prime, sent_msg_type_set, todo_mtype_sent)
        todo = len(mtype_sent_prime) > 0 or len(mtype_rec_prime) > 0
        if not todo:
          if not 'in_out_msg_type_set_list_w_dst_src' in cur_val:
            cur_val['in_out_msg_type_set_list_w_dst_src'] = OrderedDict()
          # this upath features this set of message types
          cur_val['in_out_msg_type_set_list_w_dst_src'][(sent_idx_msg, rec_idx_msg)] = OrderedDict()
          m_sent = {}
          for k, v in sent_msg_type_set.items():
            if v == 'true':
              assert(len(src_dst_mtype['sent'][k]) == 1)
              m_sent[k] = src_dst_mtype['sent'][k][0]
          m_rec = {}
          for k, v in rec_msg_type_set.items():
            if v == 'true':
              assert(len(src_dst_mtype['rec'][k]) == 1)
              m_rec[k] = src_dst_mtype['rec'][k][0]
          cur_val['in_out_msg_type_set_list_w_dst_src'][(sent_idx_msg, rec_idx_msg)]['src_dst_comb'] = [(m_sent, m_rec)]
          continue
        print("HERE -> ", state, req, idx, sent_msg_type_set, rec_msg_type_set)
        combinations = list(itertools.product(["core", "home"], repeat=len(mtype_sent_prime) + len(mtype_rec_prime)))
        for combidx, combo in enumerate(combinations):
          assignment = dict(zip([('out_' + v) for v in  mtype_sent_prime] + [('in_' + v) for v in mtype_rec_prime], combo))
          if not 'src_dst_comb_under_test' in cur_val:
            cur_val['src_dst_comb_under_test'] = []
          cur_val['src_dst_comb_under_test'].append((sent_idx_msg, rec_idx_msg, combidx, combo, assignment))
          # set up the rset and msg in/rec set, we check if the msg set's dst/src can be as defined by the combo
          outff = f"{dirname}/{state}_{req}_{idx}_trace_{sent_idx_msg}_{rec_idx_msg}_{combidx}.m"
          outff_h = open(outff, "w")

          print("--> exploring if this is possible: ", outff, assignment)

          cfg = {"track_req": True, "prevState": True, "prevStateVal": False, "rset": {"num": max_len, "state_type_name": m_proc_state_type, "m_proc_selc": m_proc_selc, "m_proc_state_field": m_proc_state_field, "stable_state_df": "|".join([f"cur_state = {s}" for s in all_cc_stable_states]), "block_within_start": ""}, f"msg_chk": True, "cur_node": True}
          for TYPE, prefix, tar_set in [("SENDING", "sent", sent_msg_type_set), ("RECEIVING", "rec", rec_msg_type_set)]:
            cfg[TYPE] = obs_mtype_template.format(m_msg_type_field=m_msg_type_field, prefix=prefix)
          
          # TODO: at prevMsg in the track_template_ff we may miss

          additional_var = {"chk": ("boolean", "chk := true;\n", "")}
          # sender is home or core for msg received
          for tar_mtype in mtype_rec_prime: # todo_mtype_rec:
            tar_receiver = m_home_iter_type if assignment['in_' + tar_mtype] == "home" else m_proc_iter_type 
            if dst_always_defined:
              cfg['SENDING'] += (f"if (start & {{msg_var}}.{m_msg_type_field} = {tar_mtype} & {{msg_var}}.{m_msg_dst_field} = selc) then chk := chk & (ismember(cur_node, {tar_receiver})); \n endif;\n")
            else:
              cfg['RECEIVING'] += (f"if (start & {{msg_var}}.{m_msg_type_field} = {tar_mtype} & !isundefined(cur_node) & cur_node = selc) then chk := chk & ismember({{msg_var}}.{m_msg_src_field}, {tar_receiver}); endif;\n")

          # receiver is home or core for msg sent out 
          for tar_mtype in mtype_sent_prime: # todo_mtype_sent:
            tar_receiver = m_home_iter_type if assignment['out_' + tar_mtype] == "home" else m_proc_iter_type 
            if dst_always_defined:
              cfg['SENDING'] += (f"if (start & {{msg_var}}.{m_msg_type_field} = {tar_mtype} & cur_node = selc) then chk := chk & ismember({{msg_var}}.{m_msg_dst_field}, {tar_receiver}); endif;\n")
            else:
              if assignment['out_' + tar_mtype] == "home":
                cfg['home'] = True
                cfg['RECEIVING'] += (f"if (start & {{msg_var}}.{m_msg_type_field} = {tar_mtype} & {{msg_var}}.{m_msg_src_field} = selc &  ismember(cur_node, {tar_receiver})) then prevMsgReceiver := cur_node; endif;\n")
                #  chk & ismember(cur_node, {tar_receiver}); endif;\n")
                cfg['SENDING'] += f"if (cur_node = selh) then prevSent := true; endif;\n"
                # additional_var['prevProcs2'] = (m_home_state_type, "", f"prevProcs2 := {m_home_cur}.{m_home_state_field};\n")
                additional_var['prevSent'] = ("boolean", "prevSent := false;\n", "prevSent := false;\n")
                additional_var['prevMsgReceiver'] = (nodes_iter_types[0], "", "undefine prevMsgReceiver;\n")
                cfg['rset']['block_within_start'] = f'''
                  if (!isundefined(prevMsgReceiver)) then 
                    chk := chk & (!isundefined(prevHomeNode) & prevHomeNode != {m_home_cur}.{m_home_state_field} | prevSent);
                  endif;
                '''
              else:
                # cfg['prevState2'] = True

                cfg['SENDING'] += f"if (cur_node = selc2) then prevSent := true; endif;\n"
                additional_var['selc2'] = (m_proc_iter_type, f"for n : {m_proc_iter_type} do\n if (n != selc) then selc2 := n; \n endif; endfor;\n", None)
                m_proc_selc2 = m_proc_selc.replace("selc", "selc2")
                additional_var['prevProcs2'] = (m_proc_state_type, "", f"prevProcs2 := {m_proc_selc2}.{m_proc_state_field};\n")
                additional_var['prevSent'] = ("boolean", "prevSent := false;\n", "prevSent := false;\n")
                additional_var['prevMsgReceiver'] = (nodes_iter_types[0], "", "undefine prevMsgReceiver;\n")
                cfg['RECEIVING'] += (f"if (start & {{msg_var}}.{m_msg_type_field} = {tar_mtype} & {{msg_var}}.{m_msg_src_field} = selc &  cur_node = selc2) then prevMsgReceiver := cur_node; endif;\n")
                #  chk & ismember(cur_node, {tar_receiver}); endif;\n")
                cfg['rset']['block_within_start'] = f'''
                  if (!isundefined(prevMsgReceiver)) then 
                    chk := chk & (prevProcs2 != {m_proc_selc2}.{m_proc_state_field} | prevSent);
                  endif;
                '''
          parse_murphi_model(coh_model_file, nodes_iter_types, outff_h, cfg, additional_var=additional_var) 
          outff_h.write(track_template_ff(state, req, m_req_type_field, m_proc_state_field = m_proc_state_field, isEntry = False, withTrackReq = False, msg = True, m_msg_type_field = m_msg_type_field))
          msg_set_ss = []
          for m_, v in rec_msg_type_set.items():
            msg_set_ss.append(f"msg_rec_set[{m_}] = {v}")
          for m_, v in sent_msg_type_set.items():
            msg_set_ss.append(f"msg_sent_set[{m_}] = {v}")
          # cover (rset plus msgset "with the src/dst for the todo_mtype_<>  be core/home as defined by this assignment ")
          outff_h.write(assert_assoc_msgsrc_state.format(state=state, req=req, idx=idx, reachable_set=get_s_from_rset(aset_arr), msg_set="(" + " & ".join(msg_set_ss) + ")"))
          outff_h.close()
    aggregate[(state, req, idx)] = cur_val
    
  dirname = f"{build_dir}/s4_3_v2_src_dst/_build"
  os.makedirs(dirname, exist_ok = True)  
  # for those with transactions
  with open(f"{build_dir}/s4_3_v2_src_dst/out/aggdict.pkl", "wb") as f:
    pickle.dump(aggregate, f)

  # collect 
  aggregate_from_s1_to_s3 = assemble() 
  with open(f"{build_dir}/s4_3_v2_src_dst/out/aggdict_s1_to_s3.pkl", "wb") as f:
    pickle.dump(aggregate_from_s1_to_s3, f)


  # 


if __name__ == "__main__":
  fire.Fire()
  dump_stats()

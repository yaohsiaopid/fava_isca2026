import os
import pickle
import sys
from collections import OrderedDict

import fire

from gconst import *
from util import *

if sys.version_info < (3, 6):
  sys.exit(1)

build_dir="build" #past_builds/MSI_fixed_build"
sys.path.append("src")
from code_gen.parse_rules import *

# For each transition s -> s', uncover the message set observed around
# the transition event.
stepname = "s1_msg_per_transition"
prevstep = "s1_2_transition"

assert_invariant_template = '''
invariant "ASSERT_{state}_to_{state_prime}_{prefix}"
((!isundefined(prevProcs) & prevProcs = {state}) &
({m_proc_selc}.{m_proc_state_field} = {state_prime})) ->
({msg_set});
'''

proc_state_expr = get_proc_state_expr()
transition = '''
invariant "{state}_to_{state_prime}"
  (!IsUndefined(prevProcs) & (prevProcs = {state})) ->
  !({proc_state_expr} = {state_prime});
'''


def iter_transitions(transition_possible):
  for state in all_cc_states:
    if not state in transition_possible:
      continue
    for state_prime in all_cc_states:
      if state == state_prime or not state_prime in transition_possible[state]:
        continue
      yield state, state_prime


def build_cfg(TYPE, prefix):
  obs_mtype_template = '''
  if (!isundefined(cur_node) & cur_node = selc) then
    msg_imm_{prefix}_set[{{msg_var}}.{m_msg_type_field}] := true;
  endif;
  '''
  cfg = {
    "track_req": False,
    "prevState": True,
    "prevStateVal": False,
    "msg_chk": False,
    f"prevMsgSet_{prefix}": True,
    "cur_node": True,
  }
  cfg[TYPE] = obs_mtype_template.format(
    m_msg_type_field=m_msg_type_field,
    prefix=prefix,
  )
  cfg["book_keep"] = (
    f"if (!isundefined(prevProcs) & prevProcs != {proc_state_expr}) then\n"
    f"for m:{msg_type_name} do msg_imm_{prefix}_set[m] := false;\nendfor;\n"
    "endif;\n"
  )
  return cfg


def gen():
  with open(f"{build_dir}/s1_2_transition/_build/transition.pkl", 'rb') as f:
    transition_possible = pickle.load(f)

  dirname = f"{build_dir}/{stepname}/out"
  print("-->", dirname)
  os.makedirs(dirname, exist_ok = True)  

  for state in all_cc_states:
    for state_prime in all_cc_states:
      if state == state_prime \
        or (not state in transition_possible) \
        or (not state_prime in transition_possible[state]):
        continue

      for TYPE, prefix in [("SENDING", "sent"), ("RECEIVING", "rec")]:
        obs_mtype_template = '''
        if (!isundefined(cur_node) & cur_node = selc) then
          msg_imm_{prefix}_set[{{msg_var}}.{m_msg_type_field}] := true;
        endif;
        '''
        #for TYPE, prefix in [("SENDING", "sent"), ("RECEIVING", "rec")]:
        cfg = {"track_req": False, "prevState": True, "prevStateVal": False, "msg_chk": False, f'prevMsgSet_{prefix}': True, "cur_node": True}
        cfg["book_keep"] = (
          f"if (!isundefined(prevProcs) & prevProcs != {proc_state_expr}) then\n"
          f"for m:{msg_type_name} do msg_imm_{prefix}_set[m] := false;\nendfor;\n"
          "endif;\n"
        )
        cfg[TYPE] = obs_mtype_template.format(m_msg_type_field=m_msg_type_field, prefix=prefix) 
        outff = f"{dirname}/{state}_{state_prime}_{prefix}_trace.m"
        outff_h = open(outff, "w")
        parse_murphi_model(coh_model_file, nodes_iter_types, outff_h, cfg, additional_var={})
        outff_h.write(transition.format(state=state, proc_state_expr=proc_state_expr, state_prime=state_prime))
        outff_h.close()


def gen_s2():
  with open(f"{build_dir}/{prevstep}/_build/transition.pkl", "rb") as f:
    transition_possible = pickle.load(f)
  # for stats purpose
  dirname = f"{build_dir}/s1_msg_per_transition/_build"
  for state in all_cc_states:
    for state_prime in all_cc_states:
      if state == state_prime \
        or (not state in transition_possible) \
        or (not state_prime in transition_possible[state]):
        continue
      for prefix in ["sent", "rec"]:
        resff = f"{dirname}/{state}_{state_prime}_{prefix}_trace.txt"
        ret = get_res_file(resff, None, assertion=True, inline_prop=True)
      

  stepname = "s1_msg_per_transition_iter"
  dirname = f"{build_dir}/{stepname}/out"
  os.makedirs(dirname, exist_ok = True)
  tardir = build_dir

  for state, state_prime in iter_transitions(transition_possible):
    for TYPE, prefix in [("SENDING", "sent"), ("RECEIVING", "rec")]:
      cfg = build_cfg(TYPE, prefix)

      outff = f"{dirname}/{state}_{state_prime}_{prefix}_baseff.m"
      outff_h = open(outff, "w")
      parse_murphi_model(coh_model_file, nodes_iter_types, outff_h, cfg, additional_var={})
      outff_h.close()

      outff = f"{dirname}/{state}_{state_prime}_{prefix}_iter.py"
      outff_h = open(outff, "w")
      outff_h.write(f'tardir = "{tardir}"\n')
      outff_h.write(f'stepname = "{stepname}"\n')
      outff_h.write(f'prefix = "{prefix}"\n')
      outff_h.write(f'state = "{state}"\n')
      outff_h.write(f'state_prime = "{state_prime}"\n')
      outff_h.write(f'proc_state_expr = "{proc_state_expr}"\n')
      with open("src/s1_iter_template.py", "r") as f:
        for ln in f:
          outff_h.write(ln)
      outff_h.close()


def gen_s3():
  iter_stepname = "s1_msg_per_transition_iter"
  with open(f"{build_dir}/{prevstep}/_build/transition.pkl", "rb") as f:
    transition_possible = pickle.load(f)

  res = OrderedDict()
  for state, state_prime in iter_transitions(transition_possible):
    sentff = f"{build_dir}/{iter_stepname}/_build/{state}_{state_prime}_sent_iter.pkl"
    recff = f"{build_dir}/{iter_stepname}/_build/{state}_{state_prime}_rec_iter.pkl"

    sent_res = None
    rec_res = None
    if os.path.exists(sentff):
      with open(sentff, "rb") as f:
        sent_res = pickle.load(f)
    if os.path.exists(recff):
      with open(recff, "rb") as f:
        rec_res = pickle.load(f)

    # Collect stats for all iter trace result files that these pkl summaries depend on.
    for prefix, iter_res in [("sent", sent_res), ("rec", rec_res)]:
      if iter_res is None:
        continue
      for iter_idx in range(len(iter_res)):
        resff = f"{build_dir}/{iter_stepname}/_build/{state}_{state_prime}_{prefix}_{iter_idx}.txt"
        if os.path.exists(resff):
          get_res_file(resff, None, assertion=True, inline_prop=False)

    if not state in res:
      res[state] = OrderedDict()
    res[state][state_prime] = (sent_res, rec_res)

  outdir = f"{build_dir}/{iter_stepname}/_build"
  os.makedirs(outdir, exist_ok=True)
  outff = f"{outdir}/res.pkl"
  with open(outff, "wb") as f:
    pickle.dump(res, f)


sending_template = '''
if (!isundefined(cur_node) & cur_node = selc & 
    !isundefined(prevProcs) & prevProcs = {state} & 
    {proc_state_expr} = {state_prime} & {{msg_var}}.{m_msg_type_field} = {msg_type}) then
  assert ({{msg_var}}.{m_msg_cl_field} = prevStateVal) "DIFF";
endif;
'''

def gen_s4():
  inff = f"{build_dir}/s1_msg_per_transition_iter/_build/res.pkl"
  assert(os.path.exists(inff))
  with open(inff, "rb") as f:
    transition_msg_res = pickle.load(f)

  stepname_s4 = "s1_msg_per_transition_cl"
  outdir = f"{build_dir}/{stepname_s4}/out"
  os.makedirs(outdir, exist_ok=True)


  for state, next_map in transition_msg_res.items():
    for state_prime, msg_res in next_map.items():
      sent_res, _ = msg_res
      print("==>", state, state_prime)
      assert(sent_res is not None)

      msg_types = set()
      for s_map in sent_res:
        for msg_type, enabled in s_map.items():
          if str(enabled).lower() == "true":
            msg_types.add(msg_type)

      for msg_type in sorted(msg_types):
        if (not msg_type in req_msg_types_with_data) and (not msg_type in resp_msg_types_w_data):
          continue

        outff = f"{outdir}/{state}_{state_prime}_{msg_type}.m"
        outff_h = open(outff, "w")
        cfg = {
          "track_req": False,
          "prevState": True,
          "prevStateVal": True,
          "cur_node": True
        }
        cfg["SENDING"] = sending_template.format(
          state=state,
          state_prime=state_prime,
          proc_state_expr=proc_state_expr,
          msg_type=msg_type,
          m_msg_type_field=m_msg_type_field,
          m_msg_cl_field=m_msg_cl_field,
        )
        parse_murphi_model(coh_model_file, nodes_iter_types, outff_h, cfg, additional_var={})
        outff_h.close()

def gen_s5():
  inff = f"{build_dir}/s1_msg_per_transition_iter/_build/res.pkl"
  assert(os.path.exists(inff))
  with open(inff, "rb") as f:
    transition_msg_res = pickle.load(f)

  stepname_s4 = "s1_msg_per_transition_cl"
  build_outdir = f"{build_dir}/{stepname_s4}/_build"
  assert(os.path.isdir(build_outdir))

  res = OrderedDict()
  for state, next_map in transition_msg_res.items():
    if not state in res:
      res[state] = OrderedDict()

    for state_prime, msg_res in next_map.items():
      sent_res, _ = msg_res
      if sent_res is None:
        res[state][state_prime] = []
        continue

      msg_types = set()
      for s_map in sent_res:
        for msg_type, enabled in s_map.items():
          if str(enabled).lower() == "true":
            msg_types.add(msg_type)

      passed = []
      for msg_type in sorted(msg_types):
        if (not msg_type in req_msg_types_with_data) and (not msg_type in resp_msg_types_w_data):
          continue

        resff = f"{build_outdir}/{state}_{state_prime}_{msg_type}.txt"
        assert(os.path.exists(resff))

        ret = get_res_file(resff, "DIFF", assertion=True, inline_prop=True)
        if ret:
          passed.append(msg_type)
        else:
          print("fail", resff)

      res[state][state_prime] = passed

  outff = f"{build_outdir}/res.pkl"
  with open(outff, "wb") as f:
    pickle.dump(res, f)

      
def gen_s6():
  inff = f"{build_dir}/s1_msg_per_transition_iter/_build/res.pkl"
  assert(os.path.exists(inff))
  with open(inff, "rb") as f:
    transition_msg_res = pickle.load(f)

  # cache line updated with value of message just received
  stepname_s5 = "s1_msg_per_transition_val_src"
  outdir = f"{build_dir}/{stepname_s5}/out"
  os.makedirs(outdir, exist_ok=True)

    # --{proc_state_expr} = {state}) then
  rec_capture_template = '''
if (!isundefined(cur_node) & cur_node = selc &
    {{msg_var}}.{m_msg_type_field} = {msg_type}) then
  rec := true;
  tmpcl := {{msg_var}}.{m_msg_cl_field};
endif;
'''

  book_keep_check_template = '''
if (!isundefined(prevProcs) & prevProcs = {state} &
    {proc_state_expr} = {state_prime} & rec) then
  assert (tmpcl = {m_proc_selc}.{m_proc_cl_field}) "DIFF_EQ_MSG";
endif;
if (!isundefined(prevProcs) & prevProcs != {proc_state_expr}) then
  rec := false;
endif;
'''

  for state, next_map in transition_msg_res.items():
    for state_prime, msg_res in next_map.items():
      _, rec_res = msg_res
      if rec_res is None:
        continue

      msg_types = set()
      for r_map in rec_res:
        for msg_type, enabled in r_map.items():
          if str(enabled).lower() == "true":
            msg_types.add(msg_type)

      for msg_type in sorted(msg_types):
        if (not msg_type in req_msg_types_with_data) and (not msg_type in resp_msg_types_w_data):
          continue

        outff = f"{outdir}/{state}_{state_prime}_{msg_type}.m"
        outff_h = open(outff, "w")
        cfg = {
          "track_req": False,
          "prevState": True,
          "prevStateVal": False,
          "cur_node": True,
        }
        cfg["RECEIVING"] = rec_capture_template.format(
          state=state,
          proc_state_expr=proc_state_expr,
          msg_type=msg_type,
          m_msg_type_field=m_msg_type_field,
          m_msg_cl_field=m_msg_cl_field,
        )
        cfg["book_keep"] = book_keep_check_template.format(
          state=state,
          state_prime=state_prime,
          proc_state_expr=proc_state_expr,
          m_proc_selc=m_proc_selc,
          m_proc_cl_field=m_proc_cl_field,
        )
        additional_var = {
          "rec": ("boolean", "rec := false;\n", ""),
          "tmpcl": (m_val_type_name, "undefine tmpcl;\n", ""),
        }
        parse_murphi_model(coh_model_file, nodes_iter_types, outff_h, cfg, additional_var=additional_var)
        outff_h.close()


def gen_s7():
  inff = f"{build_dir}/s1_msg_per_transition_iter/_build/res.pkl"
  assert(os.path.exists(inff))
  with open(inff, "rb") as f:
    transition_msg_res = pickle.load(f)

  stepname = "s1_msg_per_transition_val_src"
  build_outdir = f"{build_dir}/{stepname}/_build"
  assert(os.path.isdir(build_outdir))

  stepname = "s1_msg_per_transition_val_change"
  outdir = f"{build_dir}/{stepname}/out"
  os.makedirs(outdir, exist_ok = True)

  rec_capture_template = '''
if (!isundefined(cur_node) & cur_node = selc &
    {{msg_var}}.{m_msg_type_field} = {msg_type}) then
  rec := true;
endif;
'''

  book_keep_check_template = '''
if (!isundefined(prevProcs) & prevProcs = {state} &
    {proc_state_expr} = {state_prime} & rec) then
  assert (prevStateVal = {m_proc_selc}.{m_proc_cl_field}) "DIFF_VAL";
endif;
if (!isundefined(prevProcs) & prevProcs != {proc_state_expr}) then
  rec := false;
endif;
'''

  res = OrderedDict()
  for state, next_map in transition_msg_res.items():
    if not state in res:
      res[state] = OrderedDict()

    for state_prime, msg_res in next_map.items():
      _, rec_res = msg_res
      res[state][state_prime] = OrderedDict()
      if rec_res is None:
        continue

      msg_types = set()
      for r_map in rec_res:
        for msg_type, enabled in r_map.items():
          if str(enabled).lower() == "true":
            msg_types.add(msg_type)

      for msg_type in sorted(msg_types):
        if (not msg_type in req_msg_types_with_data) and (not msg_type in resp_msg_types_w_data):
          continue

        resff = f"{build_outdir}/{state}_{state_prime}_{msg_type}.txt"
        assert(os.path.exists(resff))
        ret = get_res_file(resff, "DIFF_EQ_MSG", assertion=True, inline_prop=True)
        res[state][state_prime][msg_type] = bool(ret)
        if not ret:
          outff = f"{outdir}/{state}_{state_prime}_{msg_type}.m"
          outff_h = open(outff, "w")
          cfg = {
            "track_req": False,
            "prevState": True,
            "prevStateVal": True,
            "cur_node": True,
          }
          cfg["RECEIVING"] = rec_capture_template.format(
            msg_type=msg_type,
            m_msg_type_field=m_msg_type_field,
          )
          cfg["book_keep"] = book_keep_check_template.format(
            state=state,
            state_prime=state_prime,
            proc_state_expr=proc_state_expr,
            m_proc_selc=m_proc_selc,
            m_proc_cl_field=m_proc_cl_field,
          )
          additional_var = {
            "rec": ("boolean", "rec := false;\n", ""),
          }
          parse_murphi_model(coh_model_file, nodes_iter_types, outff_h, cfg, additional_var=additional_var)
          outff_h.close()

  outff = f"{build_outdir}/res.pkl"
  with open(outff, "wb") as f:
    pickle.dump(res, f)
  # return res

def pp():
  inff = f"{build_dir}/s1_msg_per_transition_iter/_build/res.pkl"
  assert(os.path.exists(inff))
  with open(inff, "rb") as f:
    transition_msg_res = pickle.load(f)

  stepname = "s1_msg_per_transition_val_change"
  build_outdir = f"{build_dir}/{stepname}/_build"
  assert(os.path.isdir(build_outdir))

  res = OrderedDict()
  for state, next_map in transition_msg_res.items():
    if not state in res:
      res[state] = OrderedDict()

    for state_prime, msg_res in next_map.items():
      _, rec_res = msg_res
      res[state][state_prime] = OrderedDict()
      if rec_res is None:
        continue

      msg_types = set()
      for r_map in rec_res:
        for msg_type, enabled in r_map.items():
          if str(enabled).lower() == "true":
            msg_types.add(msg_type)

      for msg_type in sorted(msg_types):
        if (not msg_type in req_msg_types_with_data) and (not msg_type in resp_msg_types_w_data):
          continue

        resff = f"{build_outdir}/{state}_{state_prime}_{msg_type}.txt"
        if os.path.exists(resff):
          ret = get_res_file(resff, "DIFF_VAL", assertion=True, inline_prop=True)
          res[state][state_prime][msg_type] = bool(ret)

  outff = f"{build_outdir}/res.pkl"
  with open(outff, "wb") as f:
    pickle.dump(res, f)


if __name__ == "__main__":
  fire.Fire()
  dump_stats()



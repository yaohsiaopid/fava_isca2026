# Each state of cache controller either
# a) accepts exclusively request (and init txn)
# b) accepts and processes request atomically (no txn)
# c) processes existing earlier request of some type
# Goal: Distinguish a, b from c
import pickle
import fire 
from gconst import *
import subprocess
import os 
import sys
import re
import argparse
from pprint import pprint
from util import *
# from mini_parse import *
if sys.version_info < (3, 6):
  sys.exit(1)
sys.path.append("src")
from code_gen.parse_rules import *

build_dir = "build"
s0_reachable_states = []
s0_state_path = os.path.join(build_dir, "s0_state_reachability", "_build", "res.pkl")
if os.path.exists(s0_state_path):
  with open(s0_state_path, "rb") as f:
    s0_reachable_states = pickle.load(f)
# os.getenv("BUILD")
# assert(build_dir is not None)
# print("==> build dir", build_dir)

# murphi is s -- > some rule --> s':
# Each s we treat as the instant of rising clock edge, and thus what happens at
# the current cycle associted when state is s are the rule that is triggered to
# transition to s'. We thus only know what currently happens at the next cycle
# when state is already s'.

# cover (defined && state == {state} && defined && req == {req}) ===
# assert (defined && state == {state} -> not (defined && req == {req})) ===
# assert (defined && state == {state} -> (!defined || req != {req}))
template = '''
invariant "{state}_accept_req_{req}"
  (!IsUndefined(prevProcs) & (prevProcs = {state})) ->
(IsUndefined(prevProcReq.{m_req_type_field}) | (prevProcReq.{m_req_type_field} != {req}));
'''
if design_cfg.get('dist_dir', False):
  # we explore only the symmetry set of cores 
  design_cfg['opt_cond_selc'] = "if (n != Home) then\n selc := n; end;\n"

def gen():
  
  print(s0_reachable_states)
  dirname = f"{build_dir}/s1_req_acc_state/out"
  os.makedirs(dirname, exist_ok = True)  
  for itm in all_cc_states:
    if len(s0_reachable_states) and not f"{itm}_r" in s0_reachable_states:
      continue 
    for req in all_req_types:
      outff = f"{dirname}/{itm}_{req}.m"
      outff_h = open(outff, "w")
      
      parse_murphi_model(coh_model_file, nodes_iter_types, outff_h, {"track_req": True, "prevState": True})
      outff_h.write(template.format(state=itm, req=req, m_proc_state_field=m_proc_state_field, m_req_type_field=m_req_type_field))
      outff_h.close()

  outff = f"{dirname}/dst_defined_chk.m"
  outff_h = open(outff, "w")
  # parse_murphi_model(coh_model_file, nodes_iter_types, outff_h, {"track_req": False, "prevState": False, "cur_node": True, "SENDING": f"assert !isundefined({{msg_var}}.{m_msg_dst_field}) \"DST NOT DEFINED\";\n"})
  parse_murphi_model(coh_model_file, nodes_iter_types, outff_h, {"track_req": False, "prevState": False, "cur_node": True, "SENDING": "assert !isundefined({dst}) \"DST NOT DEFINED\";\n"})

  # design_file_limited_fv_tmp = "/Users/yaohsiao/work/coh_syn_dev/murphi/protocols/fv/msi_fv_envs/msi.fvt.s1_msg.m"
  # with open(design_file_limited_fv_tmp, "r") as f:
  #   for ln in f:
  #     if "#SENDING" in ln:
  #       msg_var = ln[:-1].split(",")[-1]
  #       outff_h.write(f"assert !isundefined({msg_var}.{m_msg_dst_field}) \"DST NOT DEFINED\"; \n")
  #       continue
  #     outff_h.write(ln)
  outff_h.close()

def gen_s2():
  proc_state_expr = get_proc_state_expr()
  transition = '''
  invariant "{state}_to_{state_prime}"
    (!IsUndefined(prevProcs) & (prevProcs = {state})) ->
    !({proc_state_expr} = {state_prime});
  '''
  dirname = f"{build_dir}/s1_2_transition/out"
  os.makedirs(dirname, exist_ok = True)  
  for itm in all_cc_states:
    if len(s0_reachable_states) and not f"{itm}_r" in s0_reachable_states:
      continue 
    for itm_prime in all_cc_states:
      if len(s0_reachable_states) and not f"{itm_prime}_r" in s0_reachable_states:
        continue 
      if itm == itm_prime:
        continue
      outff = f"{dirname}/{itm}_{itm_prime}.m"
      outff_h = open(outff, "w")
      parse_murphi_model(coh_model_file, nodes_iter_types, outff_h, {"track_req": True, "prevState": True})
      outff_h.write(transition.format(state=itm, proc_state_expr=proc_state_expr, state_prime=itm_prime))
      outff_h.close()

# since the msg src may be hidden ... -- (ismember({msg_var}.{m_msg_src_field}, {m_proc_src_type})) & 
# Original or general interconnection
# dst: {msg_var}.{m_msg_dst_field}
# src: cur_node
from_to_template = '''
assert !(ismember({msg_var}.{m_msg_dst_field}, {m_proc_dst_type}) & 
ismember(cur_node, {m_proc_src_type}) & 
({msg_var}.{m_msg_type_field} = {tar_type})) "{tar_type} from {m_proc_src_type} to {m_proc_dst_type}";
'''

from_to_template_no_diff_iter_type = '''
assert !({{dst}} {m_proc_dst_type_pred} & 
({{src}} {m_proc_src_type_pred}) & 
({{msg_var}}.{m_msg_type_field} = {tar_type})) "{tar_type} from {src_type} to {dst_type}";
'''
cnt_template = '''
-- being sent out 
if ({msg_var}.{m_msg_type_field} = {tar_type}) then
  msg_cnt := msg_cnt + 1;
endif;
assert (msg_cnt <= {cnt}) "{tar_type} can be sent over {cnt} time";
'''

def snooping_g_msg(dirname):
  # 1. since everyone essentially receives/snoops all messages type
  # a node receive == "receive and process OR dst defined"
  # where "process" is "change coherence state/aux state/value OR send message OR any action"
  # 2. #RECEIVING is place where the bus model is delivering only and thus may be right before or right after the processing action of a node on the message that receives
  # at RECEIVING
  obs_template = '''
    if (!isundefined(cur_node) & cur_node = selc) then
      prevMsg := {{msg_var}}.{m_msg_type_field};
      prevMsgSrc := {{msg_var}}.{m_msg_src_field};
      prevMsgDst := {{msg_var}}.{m_msg_dst_field};
    endif;
  '''
  obs_send_template = '''
    if (!isundefined(cur_node) & cur_node = selc) then
      prevSentMsg := {{msg_var}}.{m_msg_type_field};
    endif;
  '''
  from_to_template = '''
  -- can a core ever receives and proc {mtype} message with src from someone
  invariant "core_rec_from_{m_src_type}_{mtype}"
  ( !isundefined(prevMsg) & prevMsg = {mtype} & 
    -- proecess or dst defined
    ((!isundefined(prevProcs) & prevProcs != {m_proc_selc}.{m_proc_state_field}) |
    (!isundefined(prevMsgDst) & prevMsgDst = selc) |
    !isundefined(prevSentMsg))) ->
    !(!isundefined(prevMsgSrc) & ismember(prevMsgSrc, {m_src_type}));
  '''
  h_obs_template = '''
    if (!isundefined(cur_node) & cur_node = selh) then
      prevMsg := {{msg_var}}.{m_msg_type_field};
      prevMsgSrc := {{msg_var}}.{m_msg_src_field};
      prevMsgDst := {{msg_var}}.{m_msg_dst_field};
    endif;
  '''
  h_obs_send_template = '''
    if (!isundefined(cur_node) & cur_node = selh) then
      prevSentMsg := {{msg_var}}.{m_msg_type_field};
    endif;
  '''


  h_from_to_template = '''
  -- can a core ever receives and proc {mtype} message with src from someone
  invariant "home_rec_from_core_{mtype}"
  !(!isundefined(prevMsg) & prevMsg = {mtype} & 
    -- proecess or dst defined
    ((!isundefined(prevHomeNode) & prevHomeNode != {m_home_cur}.{m_home_state_field}) |
    (!isundefined(prevMsgDst) & prevMsgDst = selh) |
    (!isundefined(prevSentMsg))))
  '''

  for mtype in all_msg_types:
    outff = f"{dirname}/{mtype}_from_core_to_core.m"
    outff_h = open(outff, "w")
    obs_send_s = obs_send_template.format(m_msg_type_field=m_msg_type_field)
    obs_s = obs_template.format(m_msg_type_field=m_msg_type_field, m_msg_src_field=m_msg_src_field, m_msg_dst_field=m_msg_dst_field)
    parse_murphi_model(coh_model_file, nodes_iter_types, outff_h, {"track_req": False, "prevState": True, "cur_node": True, "RECEIVING": obs_s, "SENDING": obs_send_s, "g_msg": True})
    outff_h.write(from_to_template.format(mtype=mtype, m_src_type=m_proc_iter_type, m_proc_selc=m_proc_selc, m_proc_state_field=m_proc_state_field))
    outff_h.close()

    # 
    outff = f"{dirname}/{mtype}_from_home_to_core.m"
    outff_h = open(outff, "w")
    obs_send_s = obs_send_template.format(m_msg_type_field=m_msg_type_field)
    obs_s = obs_template.format(m_msg_type_field=m_msg_type_field, m_msg_src_field=m_msg_src_field, m_msg_dst_field=m_msg_dst_field)
    parse_murphi_model(coh_model_file, nodes_iter_types, outff_h, {"track_req": False, "prevState": True, "cur_node": True, "RECEIVING": obs_s, "SENDING": obs_send_s, "g_msg": True})
    outff_h.write(from_to_template.format(mtype=mtype, m_src_type=m_home_iter_type, m_proc_selc=m_proc_selc, m_proc_state_field=m_proc_state_field))
    outff_h.close()

    outff = f"{dirname}/{mtype}_from_core_to_home.m"
    outff_h = open(outff, "w")
    obs_send_s = h_obs_send_template.format(m_msg_type_field=m_msg_type_field)
    obs_s = h_obs_template.format(m_msg_type_field=m_msg_type_field, m_msg_src_field=m_msg_src_field, m_msg_dst_field=m_msg_dst_field)
    parse_murphi_model(coh_model_file, nodes_iter_types, outff_h, {"track_req": False, "prevState": True, "cur_node": True, "RECEIVING": obs_s, "SENDING": obs_send_s, "g_msg": True, "home": True})
    outff_h.write(h_from_to_template.format(mtype=mtype, m_proc_selc=m_proc_selc, m_home_cur=m_home_cur, m_home_state_field=m_home_state_field))
    outff_h.close()

  
def gen_s3():
  dirname = f"{build_dir}/s1_req_acc_state/_build"
  resff = f"{dirname}/dst_defined_chk.txt"
  prop = "DST NOT DEFINED"
  ret = get_res_file(resff, prop, assertion=True, inline_prop=True)
  # (ret2, t) = get_res_file_stats(resff, prop, assertion=True, inline_prop=True)
  dst_always_defined = ret


  dirname = f"{build_dir}/s1_3_global_msg/out"
  os.makedirs(dirname, exist_ok = True)  

  if not dst_always_defined:
    print("--> dst_always_defined", ret)
    snooping_g_msg(dirname)
    return

  # all destination is defined 

  if len(nodes_iter_types) == 1:
    # home/directory is the same machine iter type as the cores (possibly because distributed direcotry..)
    if all_msg_types is None:
      assert(all_msg_types_by_type)
      for m_murphi_type, msg_types in all_msg_types_by_type.items():
        for mtype in msg_types:

          outff = f"{dirname}/{mtype}_from_core_to_core.m"
          outff_h = open(outff, "w")
          
          tmpss = from_to_template_no_diff_iter_type.format(m_proc_src_type=m_proc_iter_type, m_msg_type_field=m_msg_type_field, tar_type=mtype, m_proc_dst_type=m_proc_iter_type, src_type="core", dst_type="core", m_proc_dst_type_pred=m_is_node_type_pred, m_proc_src_type_pred=m_is_node_type_pred)
          parse_murphi_model(coh_model_file, nodes_iter_types, outff_h, {"track_req": False, "prevState": False, "cur_node": True, "SENDING": (m_murphi_type, tmpss)})
          outff_h.close()

          outff = f"{dirname}/{mtype}_from_core_to_home.m"
          outff_h = open(outff, "w")

          tmpss = from_to_template_no_diff_iter_type.format(m_proc_src_type=m_proc_iter_type, m_msg_type_field=m_msg_type_field, tar_type=mtype, m_proc_dst_type=m_proc_iter_type, src_type="core", dst_type="home", m_proc_dst_type_pred=m_is_home_type_pred, m_proc_src_type_pred=m_is_node_type_pred)
          parse_murphi_model(coh_model_file, nodes_iter_types, outff_h, {"track_req": False, "prevState": False, "cur_node": True, "SENDING": (m_murphi_type, tmpss)})
          outff_h.close()

          outff = f"{dirname}/{mtype}_from_home_to_core.m"
          outff_h = open(outff, "w")

          tmpss = from_to_template_no_diff_iter_type.format(m_proc_src_type=m_proc_iter_type, m_msg_type_field=m_msg_type_field, tar_type=mtype, m_proc_dst_type=m_proc_iter_type, src_type="home", dst_type="core", m_proc_dst_type_pred=m_is_node_type_pred, m_proc_src_type_pred=m_is_home_type_pred)
          parse_murphi_model(coh_model_file, nodes_iter_types, outff_h, {"track_req": False, "prevState": False, "cur_node": True, "SENDING": (m_murphi_type, tmpss)})
          outff_h.close()
      return 
    assert (0)


  # len(nodes_iter_types) > 1
  for mtype in all_msg_types:
    outff = f"{dirname}/{mtype}_from_core_to_core.m"
    outff_h = open(outff, "w")

    from_to_template_ss = from_to_template.replace("{msg_var}", "{{msg_var}}")
    tmpss = from_to_template_ss.format(m_msg_src_field=m_msg_src_field, m_msg_dst_field=m_msg_dst_field, m_proc_src_type=m_proc_iter_type, m_msg_type_field=m_msg_type_field, tar_type=mtype, m_proc_dst_type=m_proc_iter_type)
    parse_murphi_model(coh_model_file, nodes_iter_types, outff_h, {"track_req": False, "prevState": False, "cur_node": True, "SENDING": tmpss})
    outff_h.close()

    outff = f"{dirname}/{mtype}_from_core_to_home.m"
    outff_h = open(outff, "w")
    tmpss = from_to_template_ss.format(m_msg_src_field=m_msg_src_field, m_msg_dst_field=m_msg_dst_field, m_proc_src_type=m_proc_iter_type, m_msg_type_field=m_msg_type_field, tar_type=mtype, m_proc_dst_type=m_home_iter_type)
    parse_murphi_model(coh_model_file, nodes_iter_types, outff_h, {"track_req": False, "prevState": False, "cur_node": True, "SENDING": tmpss})
    outff_h.close()

    outff = f"{dirname}/{mtype}_from_home_to_core.m"
    outff_h = open(outff, "w")
    tmpss = from_to_template_ss.format(m_msg_src_field=m_msg_src_field, m_msg_dst_field=m_msg_dst_field, m_proc_src_type=m_home_iter_type, m_msg_type_field=m_msg_type_field, tar_type=mtype, m_proc_dst_type=m_proc_iter_type)
    parse_murphi_model(coh_model_file, nodes_iter_types, outff_h, {"track_req": False, "prevState": False, "cur_node": True, "SENDING": tmpss})
    outff_h.close()

  return 

  # TODO
  
  for mtype in all_msg_types:
    for cnt_max in range(1, MSG_CNT_BOUND):
      outff = f"{dirname}/msg_send_{cnt_max}_{mtype}.m"
      outff_h = open(outff, "w")
      design_file_limited_fv_tmp = "/Users/yaohsiao/work/coh_syn_dev/murphi/protocols/fv/msi_fv_envs/msi.fvt.s1_msg_cnt.m"
      with open(design_file_limited_fv_tmp, "r") as f:
        for ln in f:
          if "#SENDING" in ln:
            msg_var = ln[:-1].split(",")[-1]
            outff_h.write(cnt_template.format(msg_var=msg_var, m_msg_type_field=m_msg_type_field, tar_type=mtype, cnt=cnt_max))
            continue
          outff_h.write(ln)
      outff_h.close()

  arb_track_template = '''
  -- Randomly select the request to track
  rule "track_some_req"
    true ==> 
    start := true;
    tracked := true;
  endrule;
  '''
  obs_mtype_template = '''
  if (!isundefined(cur_node) & cur_node = selc & {msg_var}.{m_msg_type_field} = {tar_type}) then
    msg_cnt := msg_cnt + 1;
    assert (msg_cnt <= {cnt}) "{tar_type} can be sent over {cnt} time";
    if (!start) then
      start := true;
    endif;
  endif;
  '''
  for mtype in all_msg_types:
    for cnt in range(1, 3):
      for TYPE, prefix in [("SENDING", "sent"), ("RECEIVING", "rec")]:
        outff = f"{dirname}/msg_cnt_txn_{prefix}_{mtype}_{cnt}.m"
        outff_h = open(outff, "w")
        design_file_limited_fv_tmp = "/Users/yaohsiao/work/coh_syn_dev/murphi/protocols/fv/msi_fv_envs/msi.fvt.s1_msg_cnt_txn.m"
        with open(design_file_limited_fv_tmp, "r") as f:
          for ln in f:
            if f"#{TYPE}" in ln:
              msg_var = ln[:-1].split(",")[-1]
              outff_h.write(obs_mtype_template.format(msg_var=msg_var, m_msg_type_field=m_msg_type_field, tar_type=mtype, cnt=cnt))
            outff_h.write(ln)
        
        outff_h.write(arb_track_template)
        outff_h.close()

  # check what type of message could be the source of the cache line value
  # for mtype in all_msg_types:
  #   outff = f"{dirname}/{mtyp}_data.m"
  #   outff_h = open(outff, "w")
  #   design_file_limited_fv_tmp = "/Users/yaohsiao/work/coh_syn_dev/murphi/protocols/fv/msi_fv_envs/msi.fvt.s1_msg.m"
  #   with open(design_file_limited_fv_tmp, "r") as f:
  #     bg = 0
  #     for ln in f:
  #       if "#RECEIVING" in ln:
  #         msg_var = ln[:-1].split(",")[-1]
  #         # TODO
  #         outff_h.write(f"prevMsg := {msg_var}; \n")
  #         outff_h.write(f"prevNode := cur_node; \n")
  #         continue
  #       elif "procedure book_keep" in ln:
  #         st = True
  #       elif "var" in ln and not dec:
  #         dec = True
  #         outff_h.write(f"prevMsg: {msg_type};\n")
  #       if st:
  #         if "begin" in ln:
  #           bg += 1
  #         elif "end" in ln:
  #           bg -= 1
  #       if st and bg == 1:
  #         outff_h.write("undefine prevMsg");
  #       outff_h.write(ln)
  #   outff_h.write(f"invariant \"{mtype}\"
  #     prevNode.cl = prevMsg.cl
  #   ")
  #   outff_h.close()

def find_all_simple_paths(edges, sources, destinations):
    """
    Finds all simple paths (and simple cycles) from sources to destinations.
    """
    
    # 1. Build the adjacency list
    graph = {}
    for u, v in edges:
        if u not in graph:
            graph[u] = []
        graph[u].append(v)

    all_paths = []
    dest_set = set(destinations) # Use a set for fast lookups

    # 4. Recursive DFS helper function
    def dfs(u, current_path):
        """
        'u' is the current node.
        'current_path' is the list of nodes from source to 'u'.
        """
       
        # 5. Explore neighbors
        if u not in graph:
            return # This node has no outgoing edges

        for v in graph[u]:
            # This is the "simple path" check
            
            # Case A: Neighbor 'v' is the original source.
            # This is the cycle case (e.g., n10 -> n1 -> n10)
            if v == current_path[0]:
                if v in dest_set:
                    # Complete the cycle and add it.
                    all_paths.append(current_path + [v])
            
            # Case B: Neighbor 'v' has NOT been visited on this path.
            if v in current_path:
              continue

            if v in dest_set:
                # Found a path. Add it.
                all_paths.append(current_path + [v])
                continue # Check next neighbor
            current_path.append(v)
            dfs(v, current_path)
            current_path.pop() # Backtrack
          
    # 2. Start a DFS from each source node
    for src in sources:
        if src not in graph and src not in dest_set:
            continue # Skip sources that are not in the graph
        
        # We start the recursion with a path containing just the source
        dfs(src, [src])

    return all_paths


def gen_core_send_msg_cnt(g_msg_dir):
  dirname = f"{build_dir}/s1_gmsg_cnt/out"
  os.makedirs(dirname, exist_ok = True)

  proc_state_expr = get_proc_state_expr()
  book_keep_s = f"if (!isundefined(prevProcs) & prevProcs != {proc_state_expr}) then\n cnt := 0;\nendif;\n"
  home_state_expr = f"{m_home_cur}.{m_home_state_field}"
  book_keep_h = f"if (!isundefined(prevHomeNode) & prevHomeNode != {home_state_expr}) then\n cnt := 0;\nendif;\n"

  for mtype in sorted([k for k in g_msg_dir.keys() if k != 'dst_always_defined']):
    mdir = g_msg_dir[mtype]
    from_core_possible = (
      mdir.get("from_core_to_core", False)
      or mdir.get("from_core_to_home", False)
      or mdir.get(f"from_{m_proc_iter_type}_to_{m_proc_iter_type}", False)
      or mdir.get(f"from_{m_proc_iter_type}_to_{m_home_iter_type}", False)
    )
    if from_core_possible:
      outff = f"{dirname}/{mtype}_cnt.m"
      with open(outff, "w") as outff_h:
        tmpss = (
          f"if (!isundefined(cur_node) & cur_node = selc & "
          f"{{msg_var}}.{m_msg_type_field} = {mtype}) then\n"
          "  cnt := cnt + 1;\n"
          "endif;\n"
        )
        parse_murphi_model(
          coh_model_file,
          nodes_iter_types,
          outff_h,
          {
            "track_req": False,
            "prevState": True,
            "cur_node": True,
            "SENDING": tmpss,
            "book_keep": book_keep_s,
          },
          {"cnt": ("0..2", "cnt := 0;\n", "")},
        )
        outff_h.write(
          f"""\ninvariant \"core_sent_{mtype}_cnt\"\n  cnt <= 1;\n"""
        )

    from_home_possible = (
      mdir.get("from_home_to_core", False)
      or mdir.get(f"from_{m_home_iter_type}_to_{m_proc_iter_type}", False)
    )
    if from_home_possible:
      outff = f"{dirname}/home_{mtype}_cnt.m"
      with open(outff, "w") as outff_h:
        tmpss = (
          f"if (!isundefined(cur_node) & cur_node = selh & "
          f"{{msg_var}}.{m_msg_type_field} = {mtype}) then\n"
          "  cnt := cnt + 1;\n"
          "endif;\n"
        )
        parse_murphi_model(
          coh_model_file,
          nodes_iter_types,
          outff_h,
          {
            "track_req": False,
            # "prevState": True,
            "cur_node": True,
            "SENDING": tmpss,
            "book_keep": book_keep_h,
            "home": True,
          },
          {"cnt": ("0..2", "cnt := 0;\n", "")},
        )
        outff_h.write(
          f"""\ninvariant \"home_sent_{mtype}_cnt\"\n  cnt <= 1;\n"""
        )

    to_core_possible = False
    for k, v in mdir.items():
      if (not v):
        continue
      if k.endswith("_to_core"):
        to_core_possible = True
        break
      if k.endswith(f"_to_{m_proc_iter_type}"):
        to_core_possible = True
        break

    if to_core_possible:
      outff = f"{dirname}/in_{mtype}_cnt.m"
      with open(outff, "w") as outff_h:
        tmpss = (
          f"if (!isundefined(cur_node) & cur_node = selc & "
          f"{{msg_var}}.{m_msg_type_field} = {mtype}) then\n"
          "  cnt := cnt + 1;\n"
          "endif;\n"
        )
        parse_murphi_model(
          coh_model_file,
          nodes_iter_types,
          outff_h,
          {
            "track_req": False,
            "prevState": True,
            "cur_node": True,
            "RECEIVING": tmpss,
            "book_keep": book_keep_s,
          },
          {"cnt": ("0..2", "cnt := 0;\n", "")},
        )
        outff_h.write(
          f"""\ninvariant \"core_recv_{mtype}_cnt\"\n  cnt <= 1;\n"""
        )

  print(f"==> {dirname}")


def gen_core_send_msg_cnt_snoop(g_msg_dir):
  dirname = f"{build_dir}/s1_gmsg_cnt/out"
  os.makedirs(dirname, exist_ok = True)

  proc_state_expr = get_proc_state_expr()
  book_keep_s = f"if (!isundefined(prevProcs) & prevProcs != {proc_state_expr}) then\n cnt := 0;\nendif;\n"
  home_state_expr = f"{m_home_cur}.{m_home_state_field}"
  book_keep_h = f"if (!isundefined(prevHomeNode) & prevHomeNode != {home_state_expr}) then\n cnt := 0;\nendif;\n"

  for mtype in sorted([k for k in g_msg_dir.keys() if k != 'dst_always_defined']):
    mdir = g_msg_dir[mtype]
    from_core_possible = (
      mdir.get("from_core_to_core", False)
      or mdir.get("from_core_to_home", False)
      or mdir.get(f"from_{m_proc_iter_type}_to_{m_proc_iter_type}", False)
      or mdir.get(f"from_{m_proc_iter_type}_to_{m_home_iter_type}", False)
    )
    if from_core_possible:
      outff = f"{dirname}/{mtype}_cnt.m"
      with open(outff, "w") as outff_h:
        tmpss = (
          f"if (!isundefined(cur_node) & cur_node = selc & "
          f"{{msg_var}}.{m_msg_type_field} = {mtype}) then\n"
          "  cnt := cnt + 1;\n"
          "endif;\n"
        )
        parse_murphi_model(
          coh_model_file,
          nodes_iter_types,
          outff_h,
          {
            "track_req": False,
            "prevState": True,
            "cur_node": True,
            "SENDING": tmpss,
            "book_keep": book_keep_s,
          },
          {"cnt": ("0..2", "cnt := 0;\n", "")},
        )
        outff_h.write(
          f"""\ninvariant \"core_sent_{mtype}_cnt\"\n  cnt <= 1;\n"""
        )

    from_home_possible = (
      mdir.get("from_home_to_core", False)
      or mdir.get(f"from_{m_home_iter_type}_to_{m_proc_iter_type}", False)
    )
    if from_home_possible:
      outff = f"{dirname}/home_{mtype}_cnt.m"
      with open(outff, "w") as outff_h:
        tmpss = (
          f"if (!isundefined(cur_node) & cur_node = selh & "
          f"{{msg_var}}.{m_msg_type_field} = {mtype}) then\n"
          "  cnt := cnt + 1;\n"
          "endif;\n"
        )
        parse_murphi_model(
          coh_model_file,
          nodes_iter_types,
          outff_h,
          {
            "track_req": False,
            "cur_node": True,
            "SENDING": tmpss,
            "book_keep": book_keep_h,
            "home": True,
          },
          {"cnt": ("0..2", "cnt := 0;\n", "")},
        )
        outff_h.write(
          f"""\ninvariant \"home_sent_{mtype}_cnt\"\n  cnt <= 1;\n"""
        )

    to_core_possible = False
    for k, v in mdir.items():
      if (not v):
        continue
      if k.endswith("_to_core"):
        to_core_possible = True
        break
      if k.endswith(f"_to_{m_proc_iter_type}"):
        to_core_possible = True
        break

    if to_core_possible:
      outff = f"{dirname}/in_{mtype}_cnt.m"
      with open(outff, "w") as outff_h:
        tmpss = (
          f"if (!isundefined(cur_node) & cur_node = selc & "
          f"{{msg_var}}.{m_msg_type_field} = {mtype}) then\n"
          "  cnt := cnt + 1;\n"
          "endif;\n"
        )
        parse_murphi_model(
          coh_model_file,
          nodes_iter_types,
          outff_h,
          {
            "track_req": False,
            "prevState": True,
            "cur_node": True,
            "RECEIVING": tmpss,
            "book_keep": book_keep_s,
          },
          {"cnt": ("0..2", "cnt := 0;\n", "")},
        )
        outff_h.write(
          f"""\ninvariant \"core_recv_{mtype}_cnt\"\n  cnt <= 1;\n"""
        )

  print(f"==> {dirname}")


def gen_s4():
  reachable = []
  unreachable = []
  resdirname = f"{build_dir}/s1_req_acc_state/_build"
  if not os.path.exists(resdirname):
    sys.exit(0)
  for itm in all_cc_states:
    if len(s0_reachable_states) and not f"{itm}_r" in s0_reachable_states:
      continue 
    for req in all_req_types:
      resff = f"{resdirname}/{itm}_{req}.txt"
      prop = f"{itm}_accept_req_{req}"
      ret = get_res_file(resff, prop, assertion=False, inline_prop=False)
      (ret2, t) = get_res_file_stats(resff, prop, assertion=False, inline_prop=False)
      if ret2 is None:
        print("--> undetermined", resff)
      if ret:
        reachable.append((itm, req))
      else:
        unreachable.append((itm, req))
  with open(f"{resdirname}/res.txt", "w") as f:
    f.write("Reachable\n")
    for itm in reachable:
      f.write("%s,%s\n" % (itm[0], itm[1]))
    f.write("Unreachable\n")
    for itm in unreachable:
      f.write("%s,%s\n" % (itm[0], itm[1]))
  print(f"==> {resdirname}/res.txt")

  
  dirname = f"{build_dir}/s1_2_transition/_build"
  state_transitions = {}
  edges = []
  for itm in all_cc_states:
    if len(s0_reachable_states) and not f"{itm}_r" in s0_reachable_states:
      continue 
    for itm_prime in all_cc_states:
      if len(s0_reachable_states) and not f"{itm_prime}_r" in s0_reachable_states:
        continue 
      if itm == itm_prime:
        continue
      resff = f"{dirname}/{itm}_{itm_prime}.txt"
      t = get_res_file(resff, f"{itm}_to_{itm_prime}")
      if t: 
        edges.append((itm, itm_prime))
        if not itm in state_transitions:
         state_transitions[itm] = []
        state_transitions[itm].append(itm_prime)
        # print("->", itm, itm_prime)
  with open(f"{dirname}/transition.pkl", "wb") as f:
    pickle.dump(state_transitions, f)

  print(f"==> {dirname}/transition.pkl")


  sources = all_cc_stable_states
  destinations = all_cc_stable_states
  paths = find_all_simple_paths(edges, sources, destinations)
  # print("Found paths:")
  print("len of paths", len(paths))
  with open(f"{dirname}/todo.txt", "w") as f:
    for p in paths:
      f.write(",".join(p)) 
      f.write("\n")

  print(f"==> {dirname}/todo.txt")

  dirname = f"{build_dir}/s1_req_acc_state/_build"
  resff = f"{dirname}/dst_defined_chk.txt"
  prop = "DST NOT DEFINED"
  ret = get_res_file(resff, prop, assertion=True, inline_prop=True)
  dst_always_defined = ret
  if not dst_always_defined:
    g_msg_dir = {}
    g_msg_dir['dst_always_defined'] = dst_always_defined
    dirname = f"{build_dir}/s1_3_global_msg/_build"

    g_msg=[]
    for mtype in all_msg_types:
      arr = [(f"{dirname}/{mtype}_from_core_to_core.txt", m_proc_iter_type,m_proc_iter_type),
      (f"{dirname}/{mtype}_from_home_to_core.txt", m_home_iter_type,m_proc_iter_type)]
      for itm in arr:
        resff, src, dst = itm
        prop=f"core_rec_from_{src}_{mtype}" 
        # "{tar_type} from {m_proc_src_type} to {m_proc_dst_type}".format(tar_type=mtype, m_proc_src_type=src, m_proc_dst_type=dst)
        ret = get_res_file(resff, prop, assertion=False, inline_prop=False)
        # (ret2, t) = get_res_file_stats(resff, prop, assertion=False, inline_prop=True)
        # if ret2 is None:
        #   print("--> undetermined", resff)
        g_msg.append((mtype, src, dst, "1" if ret else "0"))
      resff = f"{dirname}/{mtype}_from_core_to_home.txt"
      prop=f"home_rec_from_core_{mtype}"
      ret = get_res_file(resff, prop, assertion=False, inline_prop=False)
      g_msg.append((mtype, m_proc_iter_type, m_home_iter_type, "1" if ret else "0"))
    print("-->")
    for mtype, src, dst, is_possible_str in g_msg:
        if mtype not in g_msg_dir:
            g_msg_dir[mtype] = {}
        
        key = f"from_{src}_to_{dst}"
        is_possible = (is_possible_str == "1")
        g_msg_dir[mtype][key] = is_possible
    print("->")
    pprint(g_msg_dir)
    with open(f"{dirname}/aggdict.pkl", "wb") as f: 
      pickle.dump(g_msg_dir, f)
    print(f"==> {dirname}/aggdict.pkl")
    # TODO: send out / receive in more than once or not 
    gen_core_send_msg_cnt_snoop(g_msg_dir)
    return

  dirname = f"{build_dir}/s1_3_global_msg/_build"
  print("global", ret)
  # if ret2 is None:
  #   print("--> undetermined", resff)
  g_msg=[]

  # for mtype in all_msg_types:
  if len(nodes_iter_types) == 1 and all_msg_types is None:
    assert(all_msg_types_by_type)
    msg_types = []
    for _, types in all_msg_types_by_type.items():
      msg_types.extend(types)
  else:
    msg_types = all_msg_types

  for mtype in msg_types:
    if len(nodes_iter_types) == 1 and all_msg_types is None:
      arr = [(f"{dirname}/{mtype}_from_core_to_core.txt", "core", "core"),
      (f"{dirname}/{mtype}_from_core_to_home.txt", "core", "home"),
      (f"{dirname}/{mtype}_from_home_to_core.txt", "home", "core")]
    else:
      arr = [(f"{dirname}/{mtype}_from_core_to_core.txt", m_proc_iter_type,m_proc_iter_type),
      (f"{dirname}/{mtype}_from_core_to_home.txt", m_proc_iter_type,m_home_iter_type),
      (f"{dirname}/{mtype}_from_home_to_core.txt", m_home_iter_type,m_proc_iter_type)]

  # for mtype in all_msg_types:
    for itm in arr:
      resff, src, dst = itm
      prop="{tar_type} from {m_proc_src_type} to {m_proc_dst_type}".format(tar_type=mtype, m_proc_src_type=src, m_proc_dst_type=dst)
      ret = get_res_file(resff, prop, assertion=False, inline_prop=True)
      (ret2, t) = get_res_file_stats(resff, prop, assertion=False, inline_prop=True)
      if ret2 is None:
        print("--> undetermined", resff)
      g_msg.append((mtype, src, dst, "1" if ret else "0"))
  print("-->")
  g_msg_dir = {}
  for mtype, src, dst, is_possible_str in g_msg:
      if mtype not in g_msg_dir:
          g_msg_dir[mtype] = {}
      
      key = f"from_{src}_to_{dst}"
      is_possible = (is_possible_str == "1")
      g_msg_dir[mtype][key] = is_possible

  g_msg_dir['dst_always_defined'] = dst_always_defined
  with open(f"{dirname}/aggdict.pkl", "wb") as f: 
    pickle.dump(g_msg_dir, f)

  print(f"==> {dirname}/aggdict.pkl")
  gen_core_send_msg_cnt(g_msg_dir)
  # with open(f"{dirname}/gmsg.txt", "w") as f:
  #   f.write("dst_always_defined,%d\n" % dst_always_defined)
  #   for itm in g_msg:
  #     f.write(",".join(itm) + "\n")

def pp():
  
  # collect sent/recv count-check results and store as pkl
  dirname = f"{build_dir}/s1_gmsg_cnt/_build"
  os.makedirs(dirname, exist_ok = True)


  with open(f"{build_dir}/s1_3_global_msg/_build/aggdict.pkl", "rb") as f:
    g_msg_dir = pickle.load(f)

  g_msg_cnt = {}
  for mtype in sorted([k for k in g_msg_dir.keys() if k != 'dst_always_defined']):
    mdir = g_msg_dir[mtype]

    g_msg_cnt[mtype] = {}
    from_core_possible = (
      mdir.get("from_core_to_core", False)
      or mdir.get("from_core_to_home", False)
      or mdir.get(f"from_{m_proc_iter_type}_to_{m_proc_iter_type}", False)
      or mdir.get(f"from_{m_proc_iter_type}_to_{m_home_iter_type}", False)
    )
    if from_core_possible:
      sent_prop = f"core_sent_{mtype}_cnt"
      sent_resff = f"{dirname}/{mtype}_cnt.txt"
      sent_ret = get_res_file(sent_resff, sent_prop, assertion=True, inline_prop=False)
      g_msg_cnt[mtype]["core_sent_cnt_le_1"] = sent_ret 



    to_core_possible = False
    for k, v in mdir.items():
      if (not v):
        continue
      if k.endswith("_to_core"):
        to_core_possible = True
        break
      if k.endswith(f"_to_{m_proc_iter_type}"):
        to_core_possible = True
        break

    if to_core_possible:
      recv_prop = f"core_recv_{mtype}_cnt"
      recv_resff = f"{dirname}/in_{mtype}_cnt.txt"
      recv_ret = get_res_file(recv_resff, recv_prop, assertion=True, inline_prop=False)
      g_msg_cnt[mtype]["core_recv_cnt_le_1"] = recv_ret

    from_home_possible = (
      mdir.get("from_home_to_core", False)
      or mdir.get(f"from_{m_home_iter_type}_to_{m_proc_iter_type}", False)
    )
    if from_home_possible:
      home_sent_prop = f"home_sent_{mtype}_cnt"
      home_sent_resff = f"{dirname}/home_{mtype}_cnt.txt"
      home_sent_ret = get_res_file(home_sent_resff, home_sent_prop, assertion=True, inline_prop=False)
      g_msg_cnt[mtype]["home_sent_cnt_le_1"] = home_sent_ret


  outpkl = f"{dirname}/aggdict.pkl"
  with open(outpkl, "wb") as f:
    pickle.dump(g_msg_cnt, f)
  print(f"==> {outpkl}")

if __name__ == "__main__":
  fire.Fire()
  dump_stats()

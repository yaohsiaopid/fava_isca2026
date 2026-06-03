
# - core-level upaths: 
#   - build/s4_6_ret_val/_build/agg_txn_init.pkl
#   - build/s4_6_ret_val/_build/agg_no_txn_init.pkl 
# - post-fix info: build/core_s4_req_send_val/_build/agg.pkl
# - home-level upaths: 
#   directory
#   - per coherence set info: build/home_s3_msg_val_src_dst/_build/agg.pkl (aggregate, g_all_upaths)
#   snooping
#   - per coherence set info: build/home_s3_msg_out_info/_build/agg.pkl (aggregate, g_all_upaths)

import sys
from pprint import pprint
import pickle
import argparse
from collections import OrderedDict
from gconst import *
from uspec_lib import *
import itertools
import inspect
debug_ = True
if "mi_no_fetch_on_write_coh_model" in coh_model_file:
  debug_ = False

class MySyntaxTree:
  def __init__(self, core_upath_no_txn: OrderedDict, core_upath_txn: OrderedDict, home_dict: OrderedDict, home_all_paths: list, post_fix_dict: OrderedDict, g_msg_dir: OrderedDict, init_core_imp_dir, init_core_imp_core, mresp_at_end_txn, g_msg_cnt=None):
    self.core_upath_no_txn= core_upath_no_txn
    self.core_upath_txn= core_upath_txn
    self.home_dict= home_dict
    self.home_all_paths = home_all_paths
    self.post_fix_dict= post_fix_dict
    self.g_msg_dir= g_msg_dir
    self.g_msg_cnt = g_msg_cnt
    self.dst_always_defined = g_msg_dir['dst_always_defined']
    self.init_core_imp_dir = init_core_imp_dir
    self.init_core_imp_core = init_core_imp_core

    self.mresp_at_end_txn = mresp_at_end_txn
    print("======> mresp_at_end_txn", mresp_at_end_txn)
    self.en_owner = (m_home_owner_field is not None)
    # TODO TODO
    self.en_core_checks = False
    self.en_g_init = True
    self.en_src_core_check_home = False

    self.state_accepting_req = set()
    for k, v in self.core_upath_no_txn.items():
      # initial {state} takes in {req}  
      state, req = k 
      self.state_accepting_req.add(state)
    print("===> state accepting req", state)

    self.post_fix_states = set()
    for k, v in post_fix_dict.items():
      self.post_fix_states.add(v['state_prime'])

    self.possible_partial_order = {}

    for k, v in core_upath_txn.items():
      for n0, n1 in zip(v['rset'][:-1], v['rset'][1:]):
        if not n0 in self.possible_partial_order:
          self.possible_partial_order[n0] = []
        self.possible_partial_order[n0].append(n1)

    for k, v in post_fix_dict.items():
      if not k[0] in self.possible_partial_order:
        self.possible_partial_order[k[0]] = []
      self.possible_partial_order[k[0]].append(v['state_prime'])
    # transitive closure 
    self.possible_partial_order = trans_closure(self.possible_partial_order)


    # intermediate structure
    self.nodes_in_home_level_paths = set()           
    self.req_serving_home_upath = OrderedDict()
    self.nodes_in_postfix_paths = [] #set()

    self.home_upath_idx = 0
    self.core_upath_idx = 0 
    self.all_core_paths = {}
    self.nodes_in_req_serving_paths = set()
    self.overlapped_nodes = {}
    # key: request type , values: list of diciontary ((idx, list of predicates, list of predicates for initial state, list of macro names for home level path that's consistent, is true empty path, last coherece state, nodes))

    # uspec lang 
    self.all_core_msg_labels = set()
    self.all_home_msg_labels = set()
    self.case_labels = []
    # stage idx
    self.next_i = 0   
    self.next_v = 0

    self.labels = ""
    self.macros = ""
    self.axioms = ""

    print("[INFO] owner support :", self.en_owner)
    print("[INFO] post fix dst states:", self.post_fix_states)
    print("================================================================")

  def non_intervene_core_postfix(self, q, state, cc_s):
    return non_intervene_core_postfix_(q, state, cc_s, self.possible_partial_order)


  def find_matching_paths(self, actor2_msgs):
    """
    Perform DFS to find all possible lists of paths such that
    the out/in messages of actor 1 match the in/out messages of actor 2.

    Args:
        actor2_msgs (list of tuples): Each tuple contains (out_msg, in_msg) for actor 2.

    Returns:
        list of lists: Each list contains paths that satisfy the matching condition.
    """
    def dfs(path, remaining_msgs, visited):
      if not remaining_msgs:
        # If no more messages to match, add the path to results
        results.append(path[:])
        return

      for req_type, upath_list in self.req_serving_home_upath.items():
        for upath in upath_list:
          if upath['idx'] in visited:
            continue

          # Check if the current path matches the next message pair
          actor1_out, actor1_in = upath['out_msg'], upath['in_msg']
          actor2_out, actor2_in = remaining_msgs[0]

          if actor1_out == actor2_in and actor1_in == actor2_out:
            # Mark as visited and continue DFS
            visited.add(upath['idx'])
            path.append(upath)
            dfs(path, remaining_msgs[1:], visited)
            # Backtrack
            path.pop()
            visited.remove(upath['idx'])

    results = []
    dfs([], actor2_msgs, set())
    return results
  
  def addStage(self, stage_type, nm):
    # normal/vtstage
    if stage_type == "nm": 
      ret = nm_stage.format(i = self.next_i, nm = nm)
    else:
      ret = v_stage.format(i = self.next_i, j = self.next_v, nm = nm)
      self.next_v += 1
    self.next_i += 1
    self.labels += ret 

  def _add_msg_label(self, name, msg_type, tp="core"):
    t = nm_stage.format(i=self.next_i, nm=name)
    if is_data_type(msg_type):
      t = v_stage.format(i=self.next_i, j=self.next_v, nm=name)
      self.next_v += 1
    self.next_i += 1
    self.labels += t
    if tp == "core":
      self.all_core_msg_labels.add(name)
    else:
      self.all_home_msg_labels.add(name)

  def p_labels(self):
    self.addStage("nm", "CReq")
    for n in all_cc_states:
      self.addStage("vt", f"cc_{n}_1")
      self.addStage("nm", f"cc_{n}_lst")

    # core msg 
    for m in all_msg_types:
      msg_dir = self.g_msg_dir[m]
      #if self.dst_always_defined:
      # in regardless of self.dst_always_defined we in upath synthesis already
      # discovered each upath that is handled by core or home eventually
      if msg_dir['from_core_to_core']:
        self._add_msg_label(f"out_c_{m}", m)
      if msg_dir['from_core_to_home']:
        self._add_msg_label(f"out_h_{m}", m)
      #else:
      #  if msg_dir['from_core_to_core'] or \
      #     msg_dir['from_core_to_home']:
      #    self._add_msg_label(f"out_{m}", m)
          
      if msg_dir['from_home_to_core']:
        self._add_msg_label(f"in_h_{m}", m)
      if msg_dir['from_core_to_core']:
        self._add_msg_label(f"in_c_{m}", m)

    # home nodes
    for n in all_llc_states:
      self.addStage("vt", f"h_{n}_1")
      self.addStage("nm", f"h_{n}_lst")

    # home msg
    for m in all_msg_types:
      msg_dir = self.g_msg_dir[m]
      if msg_dir['from_core_to_home']:
        self._add_msg_label(f"h_in_{m}", m, tp="home")
      if msg_dir['from_home_to_core']:
        self._add_msg_label(f"h_out_{m}", m, tp="home")
    self.addStage("nm", "MResp")

  def construct_all(self):

    self.p_labels()

    self.construct_overlapped_nodes()

    # populates self.nodes_in_XXX
    self.construct_home_upath() 

    self.construct_core_upath_no_txn()
    self.construct_core_upath_txn()


    # also construct self.nodes_in_postfix_paths
    self.construct_postfix_paths()

    # export ^ as macro 
    # we need to see 
    self.selective_empty_home_path()

    # update the predicate that needs ~nodes in core_upath
    # relies on both self.nodes_in_postfix_paths and self.nodes_in_req_serving_paths
    # TODO: do pruning based on usage
    self.selective_empty_path()


    # each i that features some upath which requires initial state at local and home
    self.construct_local_init_state()
    self.construct_home_initial_state()


    self.export_core_upaths()

    self.add_postfix_paths_axioms()

    self.add_core_model()

    self.final_state()

    self.construct_global_init_state()

    self.msg_exchange()

    self.construct_total_order()


  def construct_overlapped_nodes(self):
    # we prepare for potentially a single column having multiple instances of
    # same in_{src}_{msg_type} when it is at different coherence state (i.e.,
    # PiCL). I.e., we go over each possible core-path, and cross product with
    # potential post-fix paths that can incur such scenario


    # 1. first we collect per path nodes 
    per_path_nodes_and_end = []
    for k, v in self.core_upath_txn.items():
      state, req, rset_idx = k
      initial_state = state
      aset = v['rset']
      for upath_idx, upath_info in enumerate(v['upaths']):
        for comb_idx, in_out_msg_src_dst_mapping in enumerate(upath_info['in_out_msg_src_dst_comb']):
          nodes_cur = set()
          an_tc = ["CReq"]
          for o_idx, inter_state in enumerate(aset):
            an_tc.append(f"cc_{inter_state}_1")
            assoc_msg_types = [mtype_ for mtype_, states_ in upath_info['sent_assoc_map'].items() if inter_state in states_]
            if len(assoc_msg_types):
              concur_ = set()
              for mtype in assoc_msg_types:
                dst = in_out_msg_src_dst_mapping[0][mtype]
                dst_ss = "h" if dst == "home" else "c"
                concur_.add(f"out_{dst_ss}_{mtype}")
              an_tc.append(concur_)

            assoc_msg_types_in = [mtype_ for mtype_, states_ in upath_info['rec_assoc_map'].items() if inter_state in states_]
            if not self.dst_always_defined:
              assoc_msg_types_in = [mtype_ for mtype_, states_ in upath_info['rec_assoc_map'].items() if (inter_state in states_ and (not mtype_ in assoc_msg_types))]

            if len(assoc_msg_types_in):
              concur_ = set()
              for mtype in assoc_msg_types_in:
                src = in_out_msg_src_dst_mapping[1][mtype]
                src_ss = "h" if src == "home" else "c"
                concur_.add(f"in_{src_ss}_{mtype}")
              an_tc.append(concur_) #f"in_{src_ss}_{mtype}")
            an_tc.append(f"cc_{inter_state}_lst")

          nodes_cur = set()
          for tmpitm in an_tc:
            if not type(tmpitm) is set:
              nodes_cur.add(tmpitm)
            else:
              nodes_cur.update(tmpitm)
          per_path_nodes_and_end.append({'nodes': nodes_cur, 'end_state': aset[-1]})

    # postfix all possible paths 
    all_paths = []
    def find_paths_to_stable(start_node, mtype, path):
      path.append((start_node, mtype))
      all_paths.append(path.copy())
      end_state = self.post_fix_dict[(start_node, mtype)]['state_prime']
      for tmpk, tmpv in self.post_fix_dict.items():
        tmp_state, tmp_mtype = tmpk
        if tmp_state == end_state:
          find_paths_to_stable(tmp_state, tmp_mtype, path)
      path.pop()
    for k, v in self.post_fix_dict.items():
      st, in_msg = k
      find_paths_to_stable(st, in_msg, [])
    print("==> postfix all paths", all_paths)
    self.postfix_all_paths = all_paths

    # globally overlapped nodes 
    overlapped_nodes = {}
    impacted_postfix_path = []
    for a_postfix_path in all_paths:
      # nodes in this postfix path
      acc_nodes = []
      print(a_postfix_path)
      for path_ele in a_postfix_path:
        info = self.post_fix_dict[path_ele]
        in_msg = path_ele[1]
        msg_src = info['msg_src']
        prefix_msg_src = "c" if msg_src == "core" else "h"
        msg_event = f"in_{prefix_msg_src}_{in_msg}"
        acc_nodes.append(msg_event)
        state_prime = info['state_prime']
        acc_nodes.append(f"cc_{state_prime}_1")
        acc_nodes.append(f"cc_{state_prime}_lst")
        concur = set()
        if 'outmsg_set' in info:
          for mtype, inc in info['outmsg_set'].items():
            if inc == "true":
              dst = "c" if info['outmsg_set_dst'][mtype] == "core" else "h"
              concur.add(f"out_{dst}_{mtype}")
        acc_nodes += list(sorted(concur))
        print("\t", acc_nodes)
      print("==> acc nodes", acc_nodes)
      assert(len(set(acc_nodes)) == len(acc_nodes))
      acc_nodes = set(acc_nodes)
      initial_state = a_postfix_path[0][0]
      imp = False
      for core_path in per_path_nodes_and_end:
        if core_path['end_state'] == initial_state:
          inter_n = core_path['nodes'].intersection(acc_nodes) 
          if (len(inter_n) > 0):
              for itm in sorted(inter_n):
                imp = True
                overlapped_nodes[itm] = f"1__{itm}"
                assert(itm[:2] == "in" or itm[:3] == "out")
                in_msg_type = itm.split("_")[-1]
      if imp:
        impacted_postfix_path.append(a_postfix_path)
    print("-> impacted_postfix_path", impacted_postfix_path)
    print("-> overlapped nodes", overlapped_nodes)
    self.overlapped_nodes = overlapped_nodes
    self.impacted_postfix_path = impacted_postfix_path
    # these are message labels 
    for k, v in overlapped_nodes.items():
      msg_type_ = v.split("_")[-1]
      self._add_msg_label(v, msg_type_)

  def construct_total_order(self):
    idx = 0
    for s1 in all_llc_stable_states:
      for s2 in all_llc_stable_states:  
        self.axioms += home_init_preced.format(state1=s1, state2=s2, idx=idx)
        idx += 1
        self.axioms += home_po.format(state1=s1, state2=s2, idx=idx)
        idx += 1
    idx = 0
    for i in range(len(all_llc_states)):
      for j in range(i+1,len(all_llc_states)):
        s1, s2 = all_llc_states[i], all_llc_states[j]
        self.axioms += home_single_state.format(idx=idx, state1=s1, state2=s2)
        idx += 1
    for i in range(len(all_llc_states)):
      tmp_hstate = all_llc_states[i]
      dis = []
      for sprime in all_llc_stable_states:
          dis.append(f"EdgeExists ((r, (0, h_{sprime}_lst)), (i, (0, h_{tmp_hstate}_lst)), \"inter_\", \"black\")")
          dis.append(f"EdgeExists ((i, (0, h_{tmp_hstate}_lst)), (r, (0, h_{sprime}_1)), \"inter_\", \"black\")")
          #  /\ EdgeExists ((r, (0, h_{sprime}_1)), (r, (0, h_{tmp_hstate}_lst)), \"inter_\", \"black\"))")
          dis.append(f"(~NodeExists (r, (0, h_{sprime}_1)) /\\ ~NodeExists (r, (0, h_{sprime}_lst)))")
      self.axioms += home_single_state_non_inter.format(idx=idx, state=tmp_hstate,disjunct=" \\/ \n".join(dis))
      idx += 1
    idx = 0
    for s1 in all_cc_stable_states: 
      for s2 in all_cc_stable_states: 
        self.axioms += cc_total_order_po.format(idx=idx, state1=s1, state2=s2)
        idx += 1

    idx = 0
    for i in range(len(all_cc_stable_states)):
      for j in range(i+1):
        s1, s2 = all_cc_stable_states[i], all_cc_stable_states[j]
        opt_pred = ""
        if i == j:
          opt_pred = " /\\ ~SameMicroop i j"
        self.axioms += cc_single_state.format(idx=idx, state1=s1, state2=s2, opt_pred=opt_pred)
        idx += 1
    

  def final_state(self):
    self.axioms += "%" * 50 + '\n' + '% FINAL STATE \n' + "%" * 50 + '\n'

    for state in all_llc_stable_states:
      before = []
      for state_j in all_llc_stable_states:
        before.append(f'( NodeExists (j, (0, h_{state_j}_1)) /\\ EdgeExists ((i, (0, h_{state}_1)), (j, (0, h_{state_j}_1)), "i_not_final"))')
      s_ = " \\/ \n".join(before)
      self.axioms += final_state_chk_t.format(state=state, before_ss=s_) 
    # if not debug_ and self.en_owner:
    #   assert(0)

  def add_core_model(self):
    self.axioms += "%" * 50 + '\n' + '% CORE MODEL \n' + "%" * 50 + '\n'
    self.axioms += one_req_axiom


  @log_method_name
  def msg_exchange(self):
    # each core-level upath out/in msg sets with dst/src; if they are core we constrain if they are the same other core or not 

    # a. per core-level upath same or differnet core that have the pair
    for req, req_upaths_info in self.all_core_paths.items():
      for idx, a_upath in enumerate(req_upaths_info):
        if a_upath['true_empty_path']:
          # already exclude everything 
          continue 
        case_pred = f"NodeExists (i, case_{idx})"
        type_pred = get_type_pred(req, "i")
        core_groups = a_upath['core_groups']
        # for i in range(1, len(core_groups)):
        #   for j in range(i):
        #     # different cores 
        #     pass 
        done_inmsg = set()
        for gidx, a_group in enumerate(core_groups):
          acc_ = []
          for ele in a_group: 
            dir_, type_ = ele
            opp_ = "out" if dir_ == "in" else "in"
            if dir_ == "out":
              acc_.append(g_edge(f"(i, {dir_}_c_{type_})", f"(j, {opp_}_c_{type_})", "match"))
            else:
              acc_.append(g_edge(f"(j, {opp_}_c_{type_})", f"(i, {dir_}_c_{type_})", "match"))
            # same cores 
            if dir_ == "in" and (dir_, "c", type_) in a_upath['in_msg_val_bind']: 
              #f"{dir_}_c_{type_}" in a_upath['in_msg_val_bind']: 
              acc_.append(f"AssocValEqCmp (j, out_c_{type_}) (i, in_c_{type_})")
              done_inmsg.add(f"{dir_}_c_{type_}")

          self.axioms += msg_axioms.format(nm=f"msg_match_core_{req}_{idx}_{gidx}", type_pred=type_pred, case_pred=case_pred, pred="/\\ \n".join(acc_))

          # assert(done_inmsg == a_upath['in_msg_val_bind'])
          # # other wise we should set up additional msg match 
        # for other out-going in-coming messages: 
        # we address in export_core_paths 

        

    home_msg_dst_flags = {}
    for _, home_info in self.home_dict.items():
      for trans_info in home_info.get('transition_info', {}).values():
        for msg_t, dst in trans_info.get('out_msg_dst', {}).items():
          seen, all_non_src = home_msg_dst_flags.get(msg_t, (False, True))
          home_msg_dst_flags[msg_t] = (True, all_non_src and isinstance(dst, str) and dst.startswith("always_not_") and dst.endswith(".src"))
    always_not_src_msgs = {m for m, (seen, all_non_src) in home_msg_dst_flags.items() if seen and all_non_src}

    # b. by each msg, if its one-to-one (send out and receive exactly once on each side), or multiple-to-one (receive multiple same type from different cores at a state), or one-to-multiple (send out multiple same type to different cores)
    # 
    for m in all_msg_types:
      msg_dir = self.g_msg_dir[m]
      #if self.dst_always_defined:
      # in regardless of self.dst_always_defined we in upath synthesis already
      # discovered each upath that is handled by core or home eventually
      if msg_dir['from_core_to_core']:
        node_pred = f"NodeExists (i, in_c_{m})"
        acc_ = []
        e = [f'EdgeExists ((j, out_c_{m}), (i, in_c_{m}), "com")']
        if f"out_c_{m}" in self.overlapped_nodes:
          e.append(f'EdgeExists ((j, {self.overlapped_nodes[f"out_c_{m}"]}), (i, in_c_{m}), "com")')
        acc_.append("(" + " \\/ ".join(e) + ")")
        # if (m in resp_msg_types_w_data or m in req_msg_types_with_data):
        #   acc_.append(f"AssocValEqCmp (j, out_c_{m}) (i, in_c_{m})")
        
        self.axioms += per_msg_existence.format(node_pred = node_pred, pred = " /\\ \n".join(acc_), dir="in", mtype=m) 

        ex_nm_list = [f"out_c_{m}"]
        if f"out_c_{m}" in self.overlapped_nodes:
          ex_nm = self.overlapped_nodes[f"out_c_{m}"]
          ex_nm_list.append(ex_nm)

        for ex_nm in ex_nm_list:
          node_pred = f"NodeExists (i, {ex_nm})"
          e = [f'EdgeExists ((i, {ex_nm}), (j, in_c_{m}), "com")']
          acc_ = []
          if f"in_c_{m}" in self.overlapped_nodes:
            e.append(f'EdgeExists ((i, {ex_nm}), (j, {self.overlapped_nodes[f"in_c_{m}"]})"com")')
          acc_.append("(" + " \\/ ".join(e) + ")")
          # if (m in resp_msg_types_w_data or m in req_msg_types_with_data):
          #   acc_.append(f"AssocValEqCmp (j, in_c_{m}) (i, out_c_{m})")
          self.axioms += per_msg_existence.format(node_pred = node_pred, pred = " /\\ \n".join(acc_), dir="out", mtype=ex_nm) 


      # for case from home_to_core, its either a) serving the particular upath, b) serving on behalf of other request from other core that happens during the particular upath (at Define Macro for h_cases and each iteration that stitches some home and core paths) or postix 
      if msg_dir['from_home_to_core']:
        always_not_src = m in always_not_src_msgs
        #always_not_src = True
        ## we want to see if "in_h_<msgtype>" is always triggered by other cores 
        ## which basically depends on that from the home's perspective, message is sent to the request 
        #for home_key in sorted(self.home_dict.keys()):
        #  home_state, in_msg_type = home_key
        #  home_info = self.home_dict[home_key]
        #  transition_info = home_info.get('transition_info', {})
        #  for hstate_prime in sorted(transition_info.keys()):
        #    trans_info = transition_info[hstate_prime]
        #    out_msg_dst = trans_info.get('out_msg_dst', {})
        #    if m not in out_msg_dst:
        #      continue
        #    dst = out_msg_dst[m]
        #    if (not isinstance(dst, str)) or (not dst.startswith("always_not_")) or (not dst.endswith(".src")):
        #      always_not_src = False
        if always_not_src:
          print("===> ALWAYS NOT SRC", m)
          tmpe = [f"EdgeExists ((i, (0, h_out_{m})), (j, in_h_{m}), \"com\")"]
          self.axioms += not_src_msg_rev.format(mtype=m, mtype_at_core=f"in_h_{m}")
          if f"in_h_{m}" in self.overlapped_nodes:
            tmpn = self.overlapped_nodes[f"in_h_{m}"]
            tmpe.append(f'EdgeExists ((i, (0, h_out_{m})), (j, {tmpn}), "com")')
            self.axioms += not_src_msg_rev.format(mtype=m, mtype_at_core=self.overlapped_nodes[f"in_h_{m}"])
          self.axioms += not_src_msg.format(mtype=m, disj=" \\/ \n".join(tmpe))

          #self.axioms += not_src_msg.format(mtype=m, mtype_at_core=f"in_h_{m}")
          #if f"in_h_{m}" in self.overlapped_nodes:
          #  self.axioms += not_src_msg.format(mtype=m, mtype_at_core=self.overlapped_nodes[f"in_h_{m}"])



      # should be for InvAck? But not ncessarily DataResp
      # if msg_dir['from_home_to_core']:
      #   print("===> from home to core", m)
      #   node_pred = f"NodeExists (i, in_h_{m})"
      #   acc_ = [f'EdgeExists ((j, (0, h_out_{m})), (i, in_h_{m}), "com")']
      #   if (m in resp_msg_types_w_data or m in req_msg_types_with_data):
      #     acc_.append(f"AssocValEqCmp (j, (0, h_out_{m})) (i, in_h_{m})")
      #   self.axioms += per_msg_existence.format(node_pred = node_pred, pred = acc_, dir="in_h", mtype=m) 
      
    print("=> TODO one to one")
    print(always_not_src_msgs)
    for m in all_msg_types:
      msg_dir = self.g_msg_dir[m]
      if msg_dir['from_core_to_core']:
        # we go on to see if this message type is one to one
        if self.g_msg_cnt[m].get('core_recv_cnt_le_1', False) and self.g_msg_cnt[m].get('core_sent_cnt_le_1', False):
          self.axioms += one_to_one_map_t.format(m="c_" + m, in_nm=f"in_c_{m}", out_nm=f"out_c_{m}")
          print("core to core one to one map", m)
      if m in always_not_src_msgs and msg_dir['from_home_to_core']:
        if self.g_msg_cnt[m].get('core_recv_cnt_le_1', False) and self.g_msg_cnt[m].get('home_sent_cnt_le_1', False):
          self.axioms += one_to_one_map_t.format(m="h_" + m, in_nm=f"in_h_{m}", out_nm=f"(0, h_out_{m})") 
          print("i at home to j at core one to one map", m)
    
      if msg_dir['from_core_to_home']:
        if self.g_msg_cnt[m].get('core_sent_cnt_le_1', False) and not m in req_msg_types:
          self.axioms += one_to_one_map_t.format(m="ch_" + m, in_nm=f"(0, h_in_{m})", out_nm=f"out_h_{m}")
          print("core send to home", m)

#     self.axioms += r'''
# Axiom "one_to_one_map_":
# forall microop "i", forall microop "j",
#   ~AccessType InitAcc i /\ ~AccessType InitAcc j =>
#     ~SameCore i j /\ SamePhysicalAddress i j =>
#     EdgeExists ((i, (0, h_out_Fwd_GetS)), (j, in_h_Fwd_GetS), "com") =>
#     (forall microop "k",
#       (~AccessType InitAcc k /\ ~SameMicroop i k /\ ~SameMicroop j k /\ SamePhysicalAddress k i) =>
#       (EdgeExists ((k, (0, h_out_Fwd_GetS)), (j, in_h_Fwd_GetS), "com") =>
#         (exists microop "n", 
#           ~AccessType InitAcc n /\ (~SameMicroop n i) /\ (~SameMicroop n j) /\ ~SameMicroop n k /\ SamePhysicalAddress k n /\
#           % EdgeExists ((k, (0, h_out_Fwd_GetS)), (n, in_h_Fwd_GetS), "com") 
#           NodeExists (n, in_h_Fwd_GetS)
#         )
#       )
#     )
#  .
# 
# Axiom "one_to_one_map_WB":
# forall microop "i", forall microop "j",
#   ~AccessType InitAcc i /\ ~AccessType InitAcc j =>
#     ~SameCore i j /\ SamePhysicalAddress i j =>
#     EdgeExists ((i, out_h_WB), (j, (0, h_in_WB)), "com") =>
#     (forall microop "k",
#       (~AccessType InitAcc k /\ ~SameMicroop i k /\ ~SameMicroop j k /\ SamePhysicalAddress k i) =>
#       (EdgeExists ((i, out_h_WB), (k, (0, h_in_WB)), "com") =>
#         (exists microop "n", 
#           ~AccessType InitAcc n /\ (~SameMicroop n i) /\ (~SameMicroop n j) /\ ~SameMicroop n k /\ SamePhysicalAddress k n /\
#           % EdgeExists ((n, out_h_WB), (k, (0, h_in_WB)), "com") 
#           NodeExists (n, out_h_WB)
#         )
#       )
#     )
#  .
# 
# Axiom "one_to_one_map_outcack":
# forall microop "i", forall microop "j",
#   ~AccessType InitAcc i /\ ~AccessType InitAcc j =>
#     ~SameCore i j /\ SamePhysicalAddress i j =>
#     EdgeExists ((i, out_c_GetS_Ack), (j, in_c_GetS_Ack), "com") =>
#     (forall microop "k",
#       (~AccessType InitAcc k /\ ~SameMicroop i k /\ ~SameMicroop j k /\ SamePhysicalAddress k i) =>
#       (EdgeExists ((k, out_c_GetS_Ack), (j, in_c_GetS_Ack), "com") =>
#         (exists microop "n", 
#           ~AccessType InitAcc n /\ (~SameMicroop n i) /\ (~SameMicroop n j) /\ ~SameMicroop n k /\ SamePhysicalAddress k n /\
#           % EdgeExists ((n, out_c_GetS_Ack), (k, in_c_GetS_Ack), "com") 
#           NodeExists (n, in_c_GetS_Ack)
#         )
#       )
#     )
#  .
# 
#       '''


  @log_method_name
  def add_postfix_paths_axioms(self):
    self.axioms += "%" * 50 + '\n' + '% POSTFIX PATH \n' + "%" * 50 + '\n'
    for req, req_upaths_info in self.all_core_paths.items():
      for idx, a_upath in enumerate(req_upaths_info):
        if a_upath['true_empty_path']:
          # already exclude everything 
          continue 
        case_pred = f"NodeExists (j, case_{idx})"
        type_pred = get_type_pred(req, "j")
        cur_nodes = set(a_upath['nodes'])
        acc_ = []
        # postfix_case_empty should not be 
        for tup, info in self.post_fix_dict.items():
          acc_nodes = set()
          core_state, in_msg = tup
          msg_src = info['msg_src']
          postfix_nodes = set(info['nodes'])
          possibility = []
          if core_state == a_upath['end_state']:
            acc_.append(f"ExpandMacro postfix_case_{core_state}_{in_msg}_{msg_src}")
            if (len(cur_nodes.intersection(postfix_nodes)) > 0):
              print("->", req, idx, sorted(cur_nodes), "\n", sorted(postfix_nodes))
              print(cur_nodes.intersection(postfix_nodes))
              print(a_upath['order_picl'])
              assert(0)
            if 'other_paths' in info:
              for idx, p in enumerate(info['other_paths']):
                acc_.append(f"ExpandMacro postfix_case_{core_state}_{in_msg}_{msg_src}_c_{idx}")
        nlist = [g_node("j", s , w_pred=True, neg=True) for s in self.nodes_in_postfix_paths if not s in cur_nodes]
        acc_.append("("+ "/\\ \n ".join(nlist) + ")")
        # if len(acc_) > 0:
        postfix_possibilities = "\\/ \n".join(acc_)
        self.axioms += postfix_axiom.format(req = req, idx = idx, type_pred = type_pred, case_pred = case_pred, postfix_possibilities = postfix_possibilities)
    self.axioms += "%" * 50 + '\n' + '% END POSTFIX PATH \n' + "%" * 50 + '\n'


  @log_method_name
  def export_core_upaths(self):
    max_case_idx = 1
    self.axioms += "%" * 50 + '\n' + '% CORE UPATH PATH \n' + "%" * 50 + '\n'
    for req, req_upaths_info in self.all_core_paths.items():
      case_arr = []
      if len(req_upaths_info) > max_case_idx:
        max_case_idx = len(req_upaths_info)
      for idx, a_upath in enumerate(req_upaths_info):
        print("==> ", req, "idx = ", idx)
        macro_ss = f"DefineMacro \"c_case_{req}_{idx}\":\n"
        macro_ss += " /\\ \n".join(a_upath['upath_predicates']) + ".\n"
        self.macros += macro_ss + "\n"

        if a_upath['home_paths_names'] is None or len(a_upath['home_paths_names']) == 0:
          home_cases = f"ExpandMacro h_empty_case"
        else:
          acc_h = [] # disjunctive
          for possible_h in a_upath['home_paths_names']:
            my_own_txn = possible_h['txn'][1]
            this_h = f"( ExpandMacro {my_own_txn} "
            print("==> myown ", my_own_txn)
            print("==> possible_h", possible_h['other_txns'])
            other_txn_possibilities = [] # disjunctive
            for other_c_possible in possible_h['other_txns']:
              other_pred = []
              for other_c in other_c_possible:
                init_state_msg, p_idx, complete_h_path, t_home_path_idx, in_out_msg_tup = other_c 
                in_h_msgs, out_h_msgs = in_out_msg_tup
                print(in_h_msgs, out_h_msgs)
                msg_exch_pred = []
                for itm in in_h_msgs:
                  e = g_edge(f"(j, (0, h_out_{itm}))", f"(i, in_h_{itm})", "contingen_other")
                  # if f"in_h_{itm}" in self.overlapped_nodes:
                  #   o = self.overlapped_nodes[f"in_h_{itm}"]
                  #   e = "(" + e  + " \\/ " + g_edge(f"(j, (0, h_out_{itm}))", f"(i, {o})", "contingen_other") + ")"
                  msg_exch_pred.append(e)

                  for titm in a_upath['in_msg_val_bind']:
                    dir_, src_, in_msg_ = titm
                    if src_ == "h" and dir_ == "in" and in_msg_ == itm: 
                      msg_exch_pred.append(f"AssocValEqCmp (j, (0, h_out_{itm})) (i, in_h_{itm})")
                for itm in out_h_msgs:
                  msg_exch_pred.append(g_edge(f"(i, out_h_{itm})", f"(j, (0, h_in_{itm}))", "contingent_other"))
                  cur_h_state = complete_h_path[0]
                  in_msg = complete_h_path[1][0][0]
                  for t_h_path in self.req_serving_home_upath[(cur_h_state, in_msg)]:
                    if t_h_path['home_path_idx'] == t_home_path_idx:
                      if itm in t_h_path['home_in_msg_val_bind']:
                        msg_exch_pred.append(f"AssocValEqCmp (i, out_h_{itm}) (j, (0, h_in_{itm}))")
                msg_exc_s = " /\\ ".join(msg_exch_pred)
                other_pred.append(f"(exists microop \"j\", ~SameCore i j /\\ SamePhysicalAddress i j /\\ \n EdgeExists ((j, CReq), (j, h_case_{t_home_path_idx}), \"contingent_hPath\", \"\") /\\ \n {msg_exc_s})")
              other_txn_possibilities.append("(" + "/\\ ".join(other_pred) + ")")
              # 
            # for titm in a_upath['in_msg_val_bind']:
            #   dir_, src_, in_msg_ = titm 
            #   if (("in", in_msg_) in [r for e in a_upath['core_groups'] for r in e]) or (src_ == "c") or \
            #    titm in a_upath['in_msg_val_bind_h_skip']:
            #     continue 
            #   e_ =  g_edge(f"(j, (0, h_out_{in_msg_}))", f"(i, in_h_{in_msg_})", "match_w_val_correponding_home_individual")
            #   val_ = f"AssocValEqCmp (j, (0, h_out_{in_msg_})) (i, in_h_{in_msg_})"
            #   this_h += (f" /\\ (exists microop \"j\", SamePhysicalAddress i j /\\ \n {e_} /\\ \n {val_})")

            if len(other_txn_possibilities): 
              this_h += " /\\ (" + " \\/ \n ".join(other_txn_possibilities) 
              this_h += ")"
            this_h += " )"
            acc_h.append(this_h)
          home_cases = "(" +  " \\/ \n ".join(acc_h) + ")"
        case_s = "("
        case_s += f"{home_cases} /\\ \n" # f"ExpandMacro {h_case_select} /\\ \n"
        case_s += f"ExpandMacro c_case_{req}_{idx} /\\ \n"
        case_s += f"ExpandMacro c_case_label_{idx} \n"
        case_s += ")"
        case_arr.append(case_s)
    
      req_axiom = f"Axiom \"{req}_upath\":\n"
      req_axiom += "forall microop \"i\", OnCore c i => "
      req_axiom += get_type_pred(req, "i")
      req_axiom += "=>\n ("
      req_axiom += " \\/ \n ".join(case_arr)
      req_axiom += ")."
      self.axioms += req_axiom + "\n\n"

    # we construct the c_case_label_ macros 
    for c_idx in range(max_case_idx):
      m_ = f"DefineMacro \"c_case_label_{c_idx}\":\n"
      m_ += g_edge("(i, CReq)", f"(i, case_{c_idx})", "case") + " /\\ \n"
      pred = []
      for other_idx in range(max_case_idx):
        if c_idx == other_idx:
          continue
        else:
          pred.append(g_node("i", f"case_{other_idx}", w_pred=True, neg=True))
      m_ += " /\\ ".join(pred)
      m_ += " .\n"

      self.labels += nm_stage.format(i=self.next_i, nm=f"case_{c_idx}")
      self.case_labels.append(f"case_{c_idx}")
      self.next_i += 1

      self.macros += m_  + "\n"

    self.axioms += "%" * 50 + '\n' + '% END CORE PATH \n' + "%" * 50 + '\n'

  def construct_global_init_state(self):
    self.axioms += "%" * 50 + '\n' + '% INIT ACC \n' + "%" * 50 + '\n'
    # initAcc per core coherence states and initAccc per core coherence state implication at home level and other cores 
    dis = []
    for sst in all_cc_stable_states:
      acc_ = [g_edge(f"(i, cc_{sst}_1)", f"(i, cc_{sst}_lst)", "init"), f"AssocValEqDataOfI (i, cc_{sst}_1) i"]
      tnodes = set([f"cc_{sst}_1", f"cc_{sst}_lst", "MResp"])
      nlist = [g_node("i", s_prime, w_pred=True, neg=True) for s_prime in sorted(self.nodes_in_req_serving_paths) if (not s_prime in tnodes)]
      if len(nlist) > 0:
        acc_ += nlist 
      if not self.en_g_init:
        mapping_ = {"P_V": "H_V", "cache_M": "directory_M"}
        share_ = {"cache_S": "directory_S"}
        if sst in mapping_:
          hstate = mapping_[sst]
          if sst in mapping_:
            acc_.append(g_edge(f"(i, (0, h_{hstate}_1))", f"(i, cc_{sst}_1)", "init_home_core"))
            acc_.append(g_edge(f"(i, cc_{sst}_lst)", f"(i, (0, h_{hstate}_lst))", "init_home_core"))
        elif sst in share_:
          hstate = share_[sst]
          if sst in mapping_:
            acc_.append(f'(exists microop "j", SamePhysicalAddress i j /\\ AccessType InitAcc j /\\ EdgeExists ((j, (0, h_{hstate}_1)), (i, cc_{sst}_1), "init_home_core")) /\\ EdgeExists ((i, cc_{sst}_lst), (j, (0, h_{hstate}_lst)),  "init_home_core")')
        assert(0)
        # else:
        #   nlist = [g_node("i", f"(0, h_{s_prime}_1)", w_pred=True, neg=True) for s_prime in all_llc_stable_states]
        #   acc_.append("  /\\ ".join(nlist))
      else:
        # 
        disj = []
        for hstate in all_llc_stable_states:
          fnd = False
          # having sst implies dir has hstate 
          if self.init_core_imp_dir[sst][hstate]:
            assert(not fnd)
            fnd = True
            # having sst implies not other core in sst?
            if self.init_core_imp_core[sst][sst]:
              # if true, its exclusive 
              disj.append("(" + g_edge(f"(i, (0, h_{hstate}_1))", f"(i, cc_{sst}_1)", "init_home_core") + " /\\ \n" \
              + g_edge(f"(i, (0, h_{hstate}_1))", f"(i, (0, h_{hstate}_lst))", "init_home_core") + ")")
              # acc_.append(g_edge(f"(i, cc_{sst}_lst)", f"(i, (0, h_{hstate}_lst))", "init_home_core"))
            else:
              # not exclusive but still exist some hstate 
              disj.append(f'(exists microop "j", SamePhysicalAddress i j /\\ AccessType InitAcc j /\\ \n \
                EdgeExists ((j, (0, h_{hstate}_1)), (i, cc_{sst}_1), "init_home_core") /\\ \n  \
                EdgeExists ((j, (0, h_{hstate}_1)), (j, (0, h_{hstate}_lst)), "init_home_core"))')
              # EdgeExists ((i, cc_{sst}_lst), (j, (0, h_{hstate}_lst)),  "init_home_core"))')
        if len(disj) == 1:
          acc_.append(disj[0])
        elif len(disj) > 1:
          acc_.append("(" +  " \\/ \n".join(disj) + ")")


      dis.append("(" + " /\\ \n".join(acc_) + ")")
    self.axioms +=  init_acc_axiom.format(nm="initacc_path", pred_n= " \\/ \n".join(dis))
    n_ = self.all_core_msg_labels.copy()
    n_.update([f"(0, {l})" for l in sorted(self.all_home_msg_labels)])
    n_.update(self.case_labels)
    pred_n = " /\\ ".join([g_node("i", s , w_pred=True, neg=True) for s in sorted(n_)])
    self.axioms += init_acc_axiom.format(nm="initacc_no_txn", pred_n=pred_n)

    # initAcc mc 
    # if not debug_ and self.en_owner:
    #   assert(0)
    dis = ["ExpandMacro h_empty_case"] #self.g_empty_paths("i", "home")]
    for sst in all_llc_stable_states:
      acc_ = [g_edge(f"(i, (0, h_{sst}_1))", f"(i, (0, h_{sst}_lst))", "init_home_level"), f"AssocValEqDataOfI (i, (0, h_{sst}_1)) i"]
      tnodes = set([f"(0, h_{sst}_1)", f"(0, h_{sst}_lst)"])
      nlist = [g_node("i", s_prime, w_pred=True, neg=True) for s_prime in sorted(self.nodes_in_home_level_paths) if not s_prime in tnodes]
      if len(nlist) > 0:
        acc_ += nlist 
      dis.append("(" + " /\\ \n".join(acc_) + ")")
    self.axioms += init_acc_axiom.format(nm="initacc_path_home", pred_n= " \\/ \n".join(dis))

    dis_n = " \\/ ".join([g_node("i", f"(0, h_{s_prime}_1)", w_pred=True, neg=False) for s_prime in all_llc_stable_states])
    nlist = " /\\ ".join([g_node("j", f"(0, h_{s_prime}_1)", w_pred=True, neg=True) for s_prime in all_llc_stable_states])
    self.axioms += f'''Axiom "init_state_home_exclusive": \nforall microop "i", forall microop "j", AccessType InitAcc i /\\ AccessType InitAcc j /\\ \n~SameMicroop i j /\\ SamePhysicalAddress i j =>\n {dis_n} =>\n {nlist}.\n'''
    
    # initAccc per core coherence state implication at home level and other cores 
    if not self.en_g_init:
      mapping_ = {"P_V": "H_V", "cache_M": "directory_M"}
      for sst in all_cc_stable_states:
        if sst in mapping_:
          hstate = mapping_[sst]
          # nlist = " /\\ ".join([g_node("j", f"cc_{s_prime}_1", w_pred=True, neg=True) for s_prime in all_cc_stable_states])
          nlist = g_node("j", f"cc_{sst}_1", w_pred=True, neg=True)
          self.axioms += f'''Axiom "init_state_home_{sst}": forall microop "i", forall microop "j", AccessType InitAcc i /\\ AccessType InitAcc j /\\\n ~SameMicroop i j /\\ SamePhysicalAddress i j => NodeExists (i, (0, h_{hstate}_1)) =>\n {nlist}.\n'''
      assert(0)
    else:
      for sst in all_cc_stable_states:
        conj_ = []
        for t_k in sorted(self.init_core_imp_core[sst].keys()):
          if not t_k in all_cc_stable_states:
            continue
          t_v = self.init_core_imp_core[sst][t_k]
          if t_v:
            conj_.append(g_node("j", f"cc_{t_k}_1", w_pred=True, neg=True))
        conj = " /\\ ".join(conj_) 
        if conj != "":
          self.axioms += f'''Axiom "init_state_{sst}_imp_others": forall microop "i", forall microop "j", AccessType InitAcc i /\\ AccessType InitAcc j => \n ~SameMicroop i j /\\ SamePhysicalAddress i j => \n NodeExists (i, cc_{sst}_1) => \n {conj}. \n'''

    # core-level -> home-level
    # home-level -> core-level 
    # core-level -> core-level

    ###################################################################
    # continue 
    # if "P_V" in all_cc_stable_states:
    #   print("==> TODO")
    #   self.axioms += f'''
    #   Axiom "init_state_cc":
    #     forall microop "i", forall microop "j", 
    #     (AccessType InitAcc i /\\ AccessType InitAcc j /\\ ~SameMicroop i j /\\ SamePhysicalAddress i j /\\ 
    #     NodeExists (i, cc_P_V_1)) =>
    #       (~NodeExists (j, cc_P_V_1) /\\ ~NodeExists (j, cc_P_V_lst)).
    #   '''
    #   assert(0)

  @log_method_name
  def construct_home_initial_state(self):
    self.axioms += "%" * 50 + '\n' + '% HOME INITIAL STATE \n' + "%" * 50 + '\n'
    pprint(self.req_serving_home_upath) 
    for req, req_upaths_info in self.all_core_paths.items():
      print(f"--> req: {req} len of upaths", len(req_upaths_info))
      for idx, a_upath in enumerate(req_upaths_info):
        # core_upath_idx, _, core_initial_, home_upaths, no_picl_no_txn, _ = a_upath
        if a_upath['home_paths_names'] is None:
          print("-> home upath is None", req, idx, "its no transaction (may introduce picl or not)")
          continue
        # having transaction but potentially with empty home paths
        # 
        # self.req_serving_home_upath[(initial_hstate, rest_of_path[0][0])].append((f"h_case_{hstate}_{inmsg_type}_{home_upath_idx}", acc_, remote_initial, a_list_of_out_msg_set))
        
        for home_level_p in a_upath['home_paths_names']:
          nm = home_level_p['txn'][1]
          fnd = False
          ret = None
          for tup, h_paths in self.req_serving_home_upath.items():
            for ele in h_paths:
              if ele['name'] == nm:
                assert(not fnd)
                fnd = True 
                ret = (tup, ele) 
          if not fnd:
            print('->', nm)
          assert(fnd)
          home_upath_case_idx = ret[1]['home_path_idx'] # ret[1][4]
          remote_initial = ret[1]['home_init']
          remote_initial_k_precond = " /\\ ".join(ret[1]['home_init_k_cond'])
          if remote_initial_k_precond != "":
            remote_initial_k_precond += " /\\ "
          #  tup = a_upath['home_paths_names'][0]
          #  assert (tup in self.req_serving_home_upath)
          #  # home_initial_state_axiom 
          #  remote_initial = self.req_serving_home_upath[tup][2]
          remote_initial_pred = " /\\ \n".join(remote_initial)
          print("-->remote initial", req, idx, remote_initial)
          type_pred = get_type_pred(req, "i")
          cur_axiom = home_initial_state_axiom.format(req=req, idx=idx,type_pred=type_pred,home_initial_pred=remote_initial_pred, h_idx=home_upath_case_idx, k_precond=remote_initial_k_precond)
          self.axioms += cur_axiom + "\n\n" 

        # TODO?? if its home empty path, we should also include the "initial state " such that home is empty (i.e. no response): snooping only? 
  
    self.axioms += "%" * 50 + '\n' + '% END HOME INITIAL STATE \n' + "%" * 50 + '\n'
    

  def construct_local_init_state(self):
    # for local initial state for each local upath
    self.axioms += "%" * 50 + '\n' + '% LOCAL INITIAL STATE \n' + "%" * 50 + '\n'
    for req, req_upaths_info in self.all_core_paths.items():
      for idx, a_upath in enumerate(req_upaths_info):
        #core_upath_idx, _, core_initial_, home_upaths, _, _ = a_upath
        # print("->", idx, a_upath['idx'])
        # assert(idx == a_upath['idx'])
        type_pred = get_type_pred(req, "i")
        core_initial_pred = " /\\ \n".join(a_upath['precond_q'])
        cur_axiom = initial_state_axiom.format(req=req, idx=idx,type_pred=type_pred,core_initial_pred=core_initial_pred)
        self.axioms += cur_axiom + "\n\n"
    self.axioms += "%" * 50 + '\n' + '% END LOCAL INITIAL STATE \n' + "%" * 50 + '\n'

  def selective_empty_path(self):
    print("--> selective empty path", self.nodes_in_req_serving_paths)
    for req, upaths in self.all_core_paths.items():
      new_upaths = []
      for idx, itm in enumerate(upaths): 
        #idx, acc_original, core_initial_, home, no_picl_no_txn, end_state = itm  
        acc_ = []
        for pred in itm['upath_predicates']:
          if type(pred) is tuple and pred[0] == "selective_empty_path":
            elist = pred[1]
            nlist = [g_node("i", s_prime, w_pred=True, neg=True) for s_prime in sorted(self.nodes_in_req_serving_paths) if ((not s_prime in elist) and (not s_prime in self.nodes_in_postfix_paths)) ]
            # exclude those ones in self.nodes_in_postfix_paths to let the postfix axioms handle 
            # these should be for all upaths except those request that initiate no txn and no new picl
            if len(nlist) > 0:
              acc_.append("/\\ ".join(nlist))
            continue
          acc_.append(pred)
        itm['upath_predicates'] = acc_
        new_upaths.append(itm)
        # new_upaths.append((itm['idx'], acc_, core_initial_, home, no_picl_no_txn, end_state))
      self.all_core_paths[req] = new_upaths
  

  def construct_postfix_paths(self):
    
    postfix_possible_labels = set()
    for path in self.postfix_all_paths:
      tar_key = path[0]

      acc_ = []
      acc_nodes = set()
      non_interven_postfix_pred = None
      # path in self.impacted_postfix_path
      # by default we just use new labels when constructing postfix 
      imp = len(self.impacted_postfix_path) > 0
      # not necessarily after MResp but something else
      # an_order = ["MResp"]
      an_order = ["cc_%s_1" % tar_key[0]]
      for post_fix_idx, pre_ele in enumerate(path):
        tup = pre_ele
        info = self.post_fix_dict[tup]
        core_state, in_msg = tup
        
        msg_src = info['msg_src']

        # j is the one with this postfix upath
        
        prefix_msg_src = "c" if msg_src == "core" else "h"
        msg_event = f"in_{prefix_msg_src}_{in_msg}"
        # we by default in postfix use potential inv_ack
        if imp:
          msg_event = self.overlapped_nodes.get(msg_event, msg_event)

        if prefix_msg_src == "c":
          acc_.append("(exists microop \"i\", SamePhysicalAddress i j /\\ ~SameCore i j /\\ {e})".format(e=g_edge(f"(i, out_c_{in_msg})", f"(j, {msg_event})", "postfix_trigger")))
        else:
          acc_.append("(exists microop \"i\", SamePhysicalAddress i j /\\ ~SameCore i j /\\ {e})".format(e=g_edge(f"(i, (0, h_out_{in_msg}))", f"(j, {msg_event})", "postfix_trigger")))

        acc_nodes.add(msg_event)

        if post_fix_idx == 0:
          an_order.append(msg_event)
          an_order.append(f"cc_{core_state}_lst")
      
        #if not info['txn_init']:
        state_prime = info['state_prime']
        acc_nodes.add(f"cc_{state_prime}_1")
        acc_nodes.add(f"cc_{state_prime}_lst")

        if not info['val_chg']:
          acc_.append(f"AssocValEqCmp (j, cc_{core_state}_1) (j, cc_{state_prime}_1)")
        
        an_order.append(f"cc_{state_prime}_1")
        concur = set()
        if 'outmsg_set' in info:
          for mtype, inc in info['outmsg_set'].items():
            if inc == "true":
              dst = "c" if info['outmsg_set_dst'][mtype] == "core" else "h"
              msg_e = f"out_{dst}_{mtype}"
              msg_e = self.overlapped_nodes.get(msg_e, msg_e) if imp else msg_e
              concur.add(msg_e)
              if (mtype in resp_msg_types_w_data or mtype in req_msg_types_with_data):
                if info['outmsg_val_eq_cl'][mtype]:
                  acc_.append(f"AssocValEqCmp (j, cc_{core_state}_1) (j, {msg_e})")
        an_order.append(concur) 
        acc_nodes.update(concur)
        if post_fix_idx < len(path) - 1:
          tmp_tup = path[post_fix_idx + 1]
          in_msg = tmp_tup[1]
          msg_src = self.post_fix_dict[tmp_tup]['msg_src']
          # j is the one with this postfix upath
          prefix_msg_src = "c" if msg_src == "core" else "h"
          msg_event = f"in_{prefix_msg_src}_{in_msg}"
          if imp:
            msg_event = self.overlapped_nodes.get(msg_event, msg_event)
          an_order.append(msg_event)

        an_order.append(f"cc_{state_prime}_lst")
        disjunc = []
        for cc in all_cc_stable_states:
          disjunc.append(f"(EdgeExists ((j, cc_{core_state}_lst), (r, cc_{cc}_1), \"inter\") /\\ EdgeExists ((r, cc_{cc}_1), (j, cc_{state_prime}_1),  \"inter\"))")
        if post_fix_idx == 0:
          non_interven_postfix_pred = postfix_nonintervene.format(pred=" \\/ \n".join(disjunc))

        ll_e = []
        for c_itm, n_itm in zip(an_order[:-1], an_order[1:]):
          if not type(c_itm) is set:
            c_itm = set([c_itm])
          if not type(n_itm) is set:
            n_itm = set([n_itm])
          for a in sorted(c_itm):
            for b in sorted(n_itm):
              ll_e.append(g_edge(f"(j, {a})", f"(j, {b})", "postfix_path", e=False, w_pred=False))
          #ll_e.append(g_edge(f"(i, {c_itm})", f"(i, {n_itm})"))
      postfix_path = "AddEdges[%s]" % ("; \n".join(ll_e))
      print("==> postfixconstruct", ll_e)
      acc_.append(postfix_path)
      # self.all_all_postifx_paths[tup] = ()
      exist_nodes = acc_nodes | (set({"cc_%s_1" % tar_key[0], "cc_%s_lst" % tar_key[0]}))
      postfix_possible_labels.update(acc_nodes)
      if len(path) == 1:
        if not 'nodes' in info:
          info['nodes'] = acc_nodes
          info['acc_pred'] = [acc_, non_interven_postfix_pred, ("selective", exist_nodes)]
          if len(concur):
            info['last_out_msg_sets'] = concur
          else:
            info['last_out_msg_sets'] = f"cc_{state_prime}_1"
          info['initiate_msg_l'] = msg_event
          self.post_fix_dict[tup] = info 
      else:
        if not 'other_paths' in self.post_fix_dict[path[0]]: 
          self.post_fix_dict[path[0]]['other_paths'] = []
        self.post_fix_dict[path[0]]['other_paths'].append([acc_, non_interven_postfix_pred, ("selective", exist_nodes)])

    # ################################################################################
    # for tup, info in self.post_fix_dict.items():
    #   acc_ = []
    #   acc_nodes = set()
    #   core_state, in_msg = tup

    #   msg_src = info['msg_src']
    #   # in_msg 

    #   # j is the one with this postfix upath
    #   an_order = ["MResp"]
    #   prefix_msg_src = "c" if msg_src == "core" else "h"
    #   msg_event = f"in_{prefix_msg_src}_{in_msg}"
    #   # we by default in postfix use potential inv_ack
    #   if [tup] in self.impacted_postfix_path:
    #     print("===> this is an impacted postfix path", tup)
    #     msg_event = self.overlapped_nodes.get(msg_event, msg_event)

    #   if prefix_msg_src == "c":
    #     acc_.append("(exists microop \"i\", SamePhysicalAddress i j /\\ ~SameCore i j /\\ {e})".format(e=g_edge(f"(i, out_c_{in_msg})", f"(j, {msg_event})", "postfix_trigger")))
    #   else:
    #     acc_.append("(exists microop \"i\", SamePhysicalAddress i j /\\ ~SameCore i j /\\ {e})".format(e=g_edge(f"(i, (0, h_out_{in_msg}))", f"(j, {msg_event})", "postfix_trigger")))
    #   acc_nodes.add(msg_event)
    #   # acc_nodes.add(f"cc_{core_state}_lst")
    #   an_order.append(msg_event)
    #   an_order.append(f"cc_{core_state}_lst")
      
    #   #if not info['txn_init']:
    #   state_prime = info['state_prime']
    #   acc_nodes.add(f"cc_{state_prime}_1")
    #   acc_nodes.add(f"cc_{state_prime}_lst")

    #   an_order.append(f"cc_{state_prime}_1")
    #   concur = set()
    #   if 'outmsg_set' in info:
    #     for mtype, inc in info['outmsg_set'].items():
    #       if inc == "true":
    #         dst = "c" if info['outmsg_set_dst'][mtype] == "core" else "h"
    #         msg_e = f"out_{dst}_{mtype}"
    #         msg_e = self.overlapped_nodes.get(msg_e, msg_e)
    #         concur.add(msg_e)
    #         if (mtype in resp_msg_types_w_data or mtype in req_msg_types_with_data):
    #           if info['outmsg_val_eq_cl'][mtype]:
    #             acc_.append(f"AssocValEqCmp (j, cc_{core_state}_1) (j, {msg_e})")
    #   an_order.append(concur) 
    #   acc_nodes.update(concur)
    #   an_order.append(f"cc_{state_prime}_lst")
    #   disjunc = []
    #   for cc in all_cc_stable_states:
    #     disjunc.append(f"(EdgeExists ((j, cc_{core_state}_lst), (r, cc_{cc}_1), \"inter\") /\\ EdgeExists ((r, cc_{cc}_1), (j, cc_{state_prime}_1),  \"inter\"))")
    #   non_interven_postfix_pred = postfix_nonintervene.format(pred=" \\/ \n".join(disjunc))


    #   ll_e = []
    #   for c_itm, n_itm in zip(an_order[:-1], an_order[1:]):
    #     if not type(c_itm) is set:
    #       c_itm = set([c_itm])
    #     if not type(n_itm) is set:
    #       n_itm = set([n_itm])
    #     for a in c_itm:
    #       for b in n_itm:
    #         ll_e.append(g_edge(f"(j, {a})", f"(j, {b})", "postfix_path", e=False, w_pred=False))
    #     #ll_e.append(g_edge(f"(i, {c_itm})", f"(i, {n_itm})"))
    #   postfix_path = "AddEdges[%s]" % ("; \n".join(ll_e))
    #   acc_.append(postfix_path)
    #   # self.all_all_postifx_paths[tup] = ()
    #   postfix_possible_labels.update(acc_nodes)
    #   info['nodes'] = acc_nodes
    #   info['acc_pred'] = [acc_, non_interven_postfix_pred, ("selective", acc_nodes)]
    #   if len(concur):
    #     info['last_out_msg_sets'] = concur
    #   else:
    #     info['last_out_msg_sets'] = f"cc_{state_prime}_1"
    #   info['initiate_msg_l'] = msg_event
    #   print("[DUMP] postfix ", tup)
    #   pprint(info)
    #   self.post_fix_dict[tup] = info 

    # pprint(self.post_fix_dict)
    self.nodes_in_postfix_paths = list(sorted(postfix_possible_labels))

    # for path in self.postfix_all_paths:
    #   if len(path) < 2:
    #     continue
    #   tar_key = path[0]
    #   print("==>t key", tar_key, self.post_fix_dict.keys())
    #   if not 'other_path' in self.post_fix_dict[tar_key]:
    #     self.post_fix_dict[tar_key]['other_paths'] = []
    #   acc_, non_interven_postfix_pred, n = self.post_fix_dict[tar_key]['acc_pred'][0].copy(), self.post_fix_dict[tar_key]['acc_pred'][1], self.post_fix_dict[tar_key]['acc_pred'][2]
    #   print("\t\t tar key ", tar_key, self.post_fix_dict[tar_key]['acc_pred'][2])
    #   acc_nodes = n[1].copy()
    #   for pre_ele, ele in zip(path[:-1], path[1:]):
    #     acc_ += self.post_fix_dict[ele]['acc_pred'][0]
    #     acc_nodes.update(self.post_fix_dict[ele]['acc_pred'][2][1])
    #     in_m_label = self.post_fix_dict[ele]['initiate_msg_l']
    #     if type(self.post_fix_dict[pre_ele]['last_out_msg_sets']) is set:
    #       for t_ele in self.post_fix_dict[pre_ele]['last_out_msg_sets']:
    #         acc_.append(g_edge(f"(j, {t_ele})", f"(j, {in_m_label})"))
    #     elif type(self.post_fix_dict[pre_ele]['last_out_msg_sets']) is str:
    #       prev_picl = self.post_fix_dict[pre_ele]['last_out_msg_sets']
    #       acc_.append(g_edge(f"(j, {prev_picl})", f"(j, {in_m_label})"))

    #   self.post_fix_dict[tar_key]['other_paths'].append((acc_, non_interven_postfix_pred, (n[0], acc_nodes)))
        
    # print("--> all paths", all_paths)
    print("--> postfix update")
    pprint(self.post_fix_dict, width=200)

    for tup, info in self.post_fix_dict.items():
      core_state, in_msg = tup
      msg_src = info['msg_src']
      acc_ = f"DefineMacro \"postfix_case_{core_state}_{in_msg}_{msg_src}\":\n"
      pred_arr = [] # info['acc_pred'][0]
      for itm in info['acc_pred']:
        if type(itm) is tuple and itm[0] == "selective":
          nodes = [g_node("j", l, w_pred=True, neg=True) for l in sorted(postfix_possible_labels) if not l in itm[1]]
          predicate = " /\\ ".join(nodes)
          if predicate != "":
            pred_arr.append(predicate)
          continue
        if type(itm) is list:
          pred_arr += itm
        else:
          pred_arr.append(itm)
      for titm in pred_arr:
        assert(type(titm) is str)
      print("=> pred arrr ", pred_arr)
      acc_ += "/\\ \n".join(pred_arr)
      acc_ += ".\n"
      # info['macros'] = [acc_]
      self.macros += acc_ + "\n"
      if 'other_paths' in info:
        for idx, other_path in enumerate(info['other_paths']):
          print("--> other paths", type(other_path))
          acc_ = f"DefineMacro \"postfix_case_{core_state}_{in_msg}_{msg_src}_c_{idx}\":\n"
          pred_arr = [] # info['acc_pred'][0]
          for itm in other_path: #info['acc_pred']:
            if type(itm) is tuple and itm[0] == "selective":
              nodes = [g_node("j", l, w_pred=True, neg=True) for l in sorted(postfix_possible_labels) if not l in itm[1]]
              predicate = " /\\ ".join(nodes)
              if predicate != "":
                pred_arr.append(predicate)
              continue
            if type(itm) is list:
              pred_arr += itm
            else:
              pred_arr.append(itm)
          print("==> pred arr", pred_arr)
          acc_ += "/\\ \n".join(pred_arr)
          acc_ += ".\n"
          self.macros += acc_ + "\n"
          # info['macros'].append(acc_)


  def construct_core_upath_no_txn(self):
    print("[INFO] Method: ", inspect.stack()[0].function)
    nodes_ = set()
    # unique core-level upaths 

    for k, v in self.core_upath_no_txn.items():
      # initial {state} takes in {req}  
      state, req = k 
      if v['txn_init']:
        continue

      if req == "ci_load" and state == "cache_S":
        if not req in self.all_core_paths:
          t = 0
        else:
          t = len(self.all_core_paths[req])
        print("DEBUGG ci_load shared state case", t)

      if req == "ci_store" and state == "cache_M":
        if not req in self.all_core_paths:
          t = 0
        else:
          t = len(self.all_core_paths[req])
        print("DEBUGG ci_store modified state case", t)

      # predicates for current path (without txn)
      
      nodes_cur = set(["CReq", "MResp"])
      acc_ = [g_edge("(i, CReq)", "(i, MResp)")]
      # current instruction is i and other instruction is q, constrained by core_initial_
      core_initial_ = [] 
      core_initial_.append(g_edge(f"(q, cc_{state}_1)", f"(q, cc_{state}_lst)"))
      # no intervening instruction in between q and i with picl
      core_initial_.append(non_intervene_core("i", "q", all_cc_stable_states)) 
      # q doesn't feature the post fix state 
      non_inter = self.non_intervene_core_postfix("q", state, self.post_fix_states)
      # if non_inter != "":
      #   core_initial_.append(non_inter)

      empty_path = True
      end_state = None

      tar_state = state
      new_picl = False

      if 'new_state' in v: 
        tar_state = v['new_state']
        new_picl = True

      if v['new_val']:  
        new_picl = True
        if not v['val_src'] == "store.data":
          print("val src not same as store.data")
          assert(0)

        # currently support only val_src always to be store.data  
        acc_.append(f"AssocValEqDataOfI (i, cc_{tar_state}_1) i")

      if new_picl:
        if non_inter != "":
          core_initial_.append(non_inter)
      # for no new picl we don't wont to constrain the post condition for the other instruction that source my initial state 
      if new_picl:
        core_initial_.append(g_edge(f"(q, cc_{state}_lst)", f"(i, CReq)"))
        acc_.append(g_edge(f"(i, CReq)", f"(i, cc_{tar_state}_1)"))
        acc_.append(g_edge(f"(i, cc_{tar_state}_1)", f"(i, cc_{tar_state}_lst)"))
        # no transaction so we add constraints that it doesn't feature nodes that appear in the paths that initiate transaction
        nodes_cur.add(f"cc_{tar_state}_1")
        nodes_cur.add(f"cc_{tar_state}_lst")
        acc_.append(("selective_empty_path", nodes_cur)) # [f"cc_{tar_state}_1", f"cc_{tar_state}_lst"]))
        end_state = tar_state

        # TODO: since this path ends with {tar_state}, which based on the post fix data, can only take and transition to limited set of state_prime, which is subset of the post_fix_states we exclude the case here
        # TODO: _postfix_data endstate is in there? if not, empty path for the post-fix path 
        # i.e., for each state S in possible postfix path states, if tar_state != S 
      else:
        # no transaction and no picl 
        # true empty path without any nodes possible
        acc_.append(self.g_empty_paths("i", "core"))
        # TODO: acc_.append(("selective_empty_path", set())) # [f"cc_{tar_state}_1", f"cc_{tar_state}_lst"]))

        core_initial_.append(g_edge(f"(q, cc_{state}_1)", "(i, CReq)"))
        core_initial_.append(g_edge("(i, MResp)", f"(q, cc_{state}_lst)"))
      if req in req_is_read:
        assert(not new_picl)
        if v['state_ret_val'] != tar_state:
          t_ = v['state_ret_val']
          print("[ERROR] ??? '' {t_} '' returns value")
        core_initial_.append(f"AssocValEqDataOfI (q, cc_{state}_1) i")

      # since its no transaction 
      # Skip below since the export already handle (line 420)
      # acc_.append(self.g_empty_paths("i", "home"))
      if not req in self.all_core_paths:
        self.all_core_paths[req] = []
      nodes_.update(nodes_cur)

      # (not new_picl) = empty core-level plus home-level path
      if req == "ci_store" and state == "cache_M":
        print("DEBUG paths no txn store: ", len(self.all_core_paths[req]))
      if req == "ci_load" and state == "cache_S":
        print("DEBUG paths no txn load: ", len(self.all_core_paths[req]))

      self.all_core_paths[req].append(
        {'idx': self.core_upath_idx, 
        'upath_predicates': acc_,
        'precond_q': core_initial_, 
        'home_paths_names': None, 
        'true_empty_path': (not new_picl), 
        'end_state': end_state, 
        'nodes': nodes_cur, 
        'core_groups': [], 
        'in_msg_val_bind': set()
        })
      self.core_upath_idx += 1
    print("[INFO] core paths")
    pprint(self.all_core_paths, width=200)
    self.nodes_in_req_serving_paths.update(nodes_)

  @log_method_name
  def construct_core_upath_txn(self):
    nodes_ = set()
    for k, v in self.core_upath_txn.items():
      state, req, rset_idx = k
      initial_state = state
      aset = v['rset']
      if req == "ci_store" and state == "cache_I" and set(aset) == set(["cache_I_store","cache_I_store__Fwd_GetS_S","cache_S"]):
          print("DEBUGG ci_store store miss case", len(self.all_core_paths[req]))
      if req == "ci_load" and state == "cache_I" and set(aset) == set(["cache_I_load","cache_S"]):
          print("DEBUGG ci_load load miss case", len(self.all_core_paths[req]))

      # v['rset]
      # the unique upaths that all feature this rset with different in/out msg_type_sets, in/out msg_src/dst 
      for upath_idx, upath_info in enumerate(v['upaths']):
        for comb_idx, in_out_msg_src_dst_mapping in enumerate(upath_info['in_out_msg_src_dst_comb']):
          # Construct a unique upath
          if req == "ci_store" and (int(rset_idx) in [8, 3]):
            print("DEBUG paths store: ", len(self.all_core_paths[req]))
          if req == "ci_load" and (int(rset_idx) in [1]):
            print("DEBUG paths load: ", len(self.all_core_paths[req]))

          nodes_cur = set()
          # the set of in_message that determines the picl's value
          in_msg_val_bind = set() 
          print("====" * 3)
          print("-> A unique core-level upath", state, req, rset_idx, upath_idx, aset,  in_out_msg_src_dst_mapping) # upath_info)
          core_initial_ = [] # current instruction is i and other instruction is q
          core_initial_.append(g_edge(f"(q, cc_{state}_1)", f"(q, cc_{state}_lst)"))
          core_initial_.append(g_edge(f"(q, cc_{state}_lst)", f"(i, CReq)"))
          core_initial_.append(non_intervene_core("i", "q", all_cc_stable_states)) # no intervening instruction in between q and i
          non_inter = self.non_intervene_core_postfix("q", state, self.post_fix_states)
          if non_inter != "":
            core_initial_.append(non_inter)

          # a core level upath specified
          acc_ = [g_edge("(i, CReq)", "(i, MResp)")]

          # rset plus the upath_info defines the picl set plus the message set (including the dst and src) 
          an_tc = ["CReq"]
          an_order_picl = aset
          state_order = {state_name: idx for idx, state_name in enumerate(an_order_picl)}

          # If a message is associated with multiple states, keep it only at the
          # latest state along this path order.
          def is_latest_assoc_state(cur_state, assoc_states):
            valid_states = [st for st in assoc_states if st in state_order]
            if cur_state not in valid_states or len(valid_states) == 0:
              return False
            latest_state = max(valid_states, key=lambda st: state_order[st])
            return cur_state == latest_state

          mresp_done = False
          msg_set_ = set() 
          in_mapping = {}
          in_h_msg_set = []
          out_h_msg_set = []
          # iterate over each stat/picl of this path consisting of rset 
          for o_idx, inter_state in enumerate(an_order_picl):
            an_tc.append(f"cc_{inter_state}_1")
            # if inter_state in self.state_accepting_req:
            #   an_tc.append("MResp")
            if self.mresp_at_end_txn and o_idx == len(an_order_picl) - 1:
              # this is the last state
              an_tc.append("MResp")

            # if any out message  
            assoc_msg_types = [mtype_ for mtype_, states_ in upath_info['sent_assoc_map'].items() if inter_state in states_]
            #if inter_state in upath_info['sent_assoc_map']:
            if len(assoc_msg_types):
              print("\t assoc out msg type", assoc_msg_types)
              concur_ = set()
              concur_filtered = set()
              for mtype in assoc_msg_types:
                dst = in_out_msg_src_dst_mapping[0][mtype]
                dst_ss = "h" if dst == "home" else "c"
                msg_set_.add(f"out_{dst_ss}_{mtype}")
                concur_.add(f"out_{dst_ss}_{mtype}")
                if dst == "home":
                  concur_filtered.add(mtype)

              if not self.mresp_at_end_txn and not mresp_done and inter_state in self.state_accepting_req:
                concur_.add("MResp")
                mresp_done = True
              an_tc.append(concur_)
              out_h_msg_set.append(concur_filtered)
            else:
              if not self.mresp_at_end_txn and not mresp_done and inter_state in self.state_accepting_req:
                an_tc.append("MResp")
                mresp_done = True

            # if any in message
            assoc_msg_types_in = [
              mtype_
              for mtype_, states_ in upath_info['rec_assoc_map'].items()
              if is_latest_assoc_state(inter_state, states_)
            ]
            if not self.dst_always_defined:
              # snooping can potentially "receive" its own msg 
              # TODO: unless we update property that uncovers the rec msg set 
              assoc_msg_types_in = [
                mtype_
                for mtype_, states_ in upath_info['rec_assoc_map'].items()
                if (is_latest_assoc_state(inter_state, states_) and (not mtype_ in assoc_msg_types))
              ]

            if len(assoc_msg_types_in):
              concur_ = set()
              concur_filtered = set()

              # ordering on the inmsg 
              # TODO: only one of them causes the transition of coherence state, and thus the others should happens-before it

              for mtype in assoc_msg_types_in:
                src = in_out_msg_src_dst_mapping[1][mtype]
                src_ss = "h" if src == "home" else "c"
                msg_set_.add(f"in_{src_ss}_{mtype}")
                concur_.add(f"in_{src_ss}_{mtype}")
                if not inter_state in in_mapping:
                  in_mapping[inter_state] = {}
                in_mapping[inter_state][mtype] = ("in", src_ss, mtype) #f"in_{src_ss}_{mtype}"

                if src == "home":
                  concur_filtered.add(mtype)
              an_tc.append(concur_) #f"in_{src_ss}_{mtype}")
              in_h_msg_set.append(concur_filtered)
            an_tc.append(f"cc_{inter_state}_lst")
          nodes_cur = set()
          for tmpitm in an_tc:
            if not type(tmpitm) is set:
              nodes_cur.add(tmpitm)
            else:
              nodes_cur.update(tmpitm)
          ll_e = []
          for c_itm, n_itm in zip(an_tc[:-1], an_tc[1:]):
            if not type(c_itm) is set:
              c_itm = set([c_itm])
            if not type(n_itm) is set:
              n_itm = set([n_itm])
            for a in sorted(c_itm):
              for b in sorted(n_itm):
                ll_e.append(g_edge(f"(i, {a})", f"(i, {b})", "to_picl_msg", e=False, w_pred=False))
            #ll_e.append(g_edge(f"(i, {c_itm})", f"(i, {n_itm})"))
          # print("-> ll_e", ll_e)
          a_complete_core_level_upath = "AddEdges[%s]" % ("; \n".join(ll_e))
          acc_.append(a_complete_core_level_upath)
          acc_.append(("selective_empty_path", list(nodes_cur)))
          nodes_.update(nodes_cur)

          # in/out msg core ids
          core_groups = []
          if self.en_core_checks:
            for g in upath_info['in_out_msg_src_dst_comb_core_ids'][comb_idx]:
              # a set of tuples (in/out, msgtype) for this in_out_msg_src_dst_mapping 
              # for this combination, elements in g are same core 
              core_groups.append([f"{ele[0]}_c_{ele[1]}" for ele in g])
          else:
            print("TODO")
            if "GetMsg" in in_out_msg_src_dst_mapping[0] and in_out_msg_src_dst_mapping[0]['GetMsg'] == 'core' and  "DataRespMsg" in in_out_msg_src_dst_mapping[1] and in_out_msg_src_dst_mapping[1]['DataRespMsg'] == 'core':
              core_groups.append([("in", "DataRespMsg"), ("out", "GetMsg")])

          # values on these picls 
          prev = None
          eq_arg = upath_info.get('picl_val_eq_data', [False] * len(an_order_picl))
          for val_eq_arg, val_eq_inmsg, inmsg_type, val_eq_prev, inter_state in \
              zip(eq_arg, upath_info['picl_val_eq_inmsg'], upath_info['picl_val_eq_inmsg_types'], upath_info['picl_val_eq_prev'], an_order_picl):

            add_already = False

            if val_eq_arg:
              acc_.append(f"AssocValEqDataOfI (i, cc_{inter_state}_1) i")
              add_already = True

            if not add_already and prev is not None and val_eq_prev:
              acc_.append(f"AssocValEqCmp (i, cc_{prev}_1) (i, cc_{inter_state}_1)")
              add_already = True

            if not add_already and prev is None and val_eq_prev:
              core_initial_.append(f"AssocValEqCmp (q, cc_{initial_state}_1) (i, cc_{inter_state}_1)")
              print("val eq first state of this path:", core_initial_[-1])
              assert(initial_state == state)
              add_already = True

            if not add_already and val_eq_inmsg:
              # v_['picl_val_eq_inmsg] should be mtype or None 
              # val_eq_inmsg should be mtype that  
              # we find the assoc. in_msg received at the last cycle of `prev`
              # print("-->", prev)
              assert (inmsg_type is not None)
              # inmsg_type should be received at prev:
              assoc_msg_types_in = [mtype_ for mtype_, states_ in upath_info['rec_assoc_map'].items() if (prev in states_)]
              assert (inmsg_type in assoc_msg_types_in)

              print("--> in mapping", in_mapping, prev, mtype, inter_state, inmsg_type)
              in_msg_node = "_".join(in_mapping[prev][inmsg_type])
              print(f"--> {inter_state} val eq inmsg {inmsg_type} rec'd at {prev} ({in_msg_node})")
              print("CHANGE")
              acc_.append(f"AssocValEqCmp (i, cc_{inter_state}_1) (i, {in_msg_node})")
              in_msg_val_bind.add(in_mapping[prev][inmsg_type]) #in_msg_node)
              add_already = True

            prev = inter_state
          # values on outgoing message for this upath
          for mtype, src_state in v['out_msg_data_src'].items():
            assert(mtype in upath_info['sent_assoc_map'].keys())
            dst = in_out_msg_src_dst_mapping[0][mtype]
            dst_ss = "h" if dst == "home" else "c"
            if src_state == initial_state:  # state:
              core_initial_.append(f"AssocValEqCmp (i, out_{dst_ss}_{mtype}) (q, cc_{src_state}_1)")
            else:
              if eq_arg[an_order_picl.index(src_state)]:
                acc_.append(f"AssocValEqDataOfI (i, out_{dst_ss}_{mtype}) i")
              else:
                acc_.append(f"AssocValEqCmp (i, out_{dst_ss}_{mtype}) (i, cc_{src_state}_1)")
            # acc_.append
          if req in req_is_read: 
            if v['state_ret_val'] is not None:
              src_state = v['state_ret_val']
              acc_.append(f"AssocValEqDataOfI (i, cc_{src_state}_1) i")
            else:
              assert(0)
          if not req in self.all_core_paths:
            self.all_core_paths[req] = []

          # we try to construct the home paths 
          print("---> from home level", in_h_msg_set, "to home level", out_h_msg_set)
          # the home paths that needs to happen for this particular upath 
          home_paths_names = []
          for tmp_k, tmp_v in self.req_serving_home_upath.items():
            hstate, home_inmsg = tmp_k

            for upath in tmp_v:
              # from core perspective
              cur_in_h_msg_set = [m for ele in in_h_msg_set for m in ele] # in_h_msg_set.copy()
              cur_out_h_msg_set =  [m for ele in out_h_msg_set for m in ele] # out_h_msg_set.copy()

              # we first see if inmsg is in out_h_msg_set and thus this hstate will be the one handle this core this request
              if not home_inmsg in cur_out_h_msg_set:
                continue
              cur_out_h_msg_set.remove(home_inmsg)
              # this particular home upath with this particular set of out msg sets 
              # at least this upath at home level should match the in/out message set 
              home_out_msg_list = upath['out_msg']
              for itm in home_out_msg_list:
                align = True
                # concrete path 
                for ele in itm:
                  # home level send back msg to the source of requeset but the msg is not in the received set of this core-level path
                  if (('out', ele) in upath['out_msg_dst']['src']):
                    if (not ele in cur_in_h_msg_set):  
                      align = False
                      break 
                    cur_in_h_msg_set.remove(ele)
              # rest of this path 
              for e in upath['path'][1][1:]:
                t_in_msg_type,  hstate_prime = e
                if ('in', t_in_msg_type) in upath['out_msg_dst']['src']:
                  if (not t_in_msg_type in cur_out_h_msg_set):
                    # print("-> not finding that this core path also sends out these message received ")
                    align = False 
                    break
                  else:
                    cur_out_h_msg_set.remove(t_in_msg_type) #ele[1])
              
              if not align:
                continue
              
              # we select this upath starting with hstate, inmsg (from this request) to handl this core this request 
              print("==> possible align", hstate, home_inmsg, upath['path'], upath['out_msg'], cur_out_h_msg_set, cur_in_h_msg_set)

              # this home upath may be possibly serving this core-level transaction
              # rest of this we enumerate all set of home upaths again to find their "not_src" can satisfy the rest of cur_out_h_msg_set and cur_in_h_msg_set: 
              self.all_combs = []
              if len(cur_out_h_msg_set) == 0 and len(cur_in_h_msg_set) == 0:
                print("Skipping: we just need the selected home upath that serves this particular request upath!")
                home_paths_names.append({'txn': (tmp_k, upath['name'], upath), 'other_txns': []})
                continue 

              self.find_paths(cur_out_h_msg_set[:], cur_in_h_msg_set[:], [], (hstate, None, upath['path'], (None, None)))
              if len(self.all_combs) == 0:
                print("failing to align")
              else:
                print("==> all combination", self.all_combs)
                home_paths_names.append({'txn': (tmp_k, upath['name'], upath), 'other_txns': self.all_combs})


              # TODO which we instantiate the (i, (0, h_<>)) event
              # for the remaining message sent to/from home we go on to search the matching set


              # cur_out_h_msg_set.remove()

            # out_msg_dst_ = upath['out_msg_dst']

            # home upath 
            ###########################################################################
            # for upath in tmp_v:
            #   # case_name, _, _, out_msg_list, _ = upath 
            #   case_name = upath['name']
            #   out_msg_list = upath['out_msg']
            #   # print("--> outmsglist, ", req, upath_idx, out_msg_list)
            #   # assert(len(out_msg_list) == 1)
            #   for ll in out_msg_list:
            #     if set([m for ele in in_h_msg_set for m in ele]) == set(ll) and set([m for ele in out_h_msg_set for m in ele]) == set([inmsg]):
            #       home_paths_names.append(case_name)
          # the paths in home_paths_names share the same inmsg/out_msg_list but not necessarily the same initial hstate 

          in_msg_val_bind_h_skip = set() 
          # for the set of in coming message that has value bind to my picl we also constrain the value to be equal (although the )
          for titm in in_msg_val_bind: 
            dir_, src_, in_msg_ = titm
            # if its not in the core_groups which has stronger constraint we here instantiate additional predicates for it 
            if src_ == "c" and ("in", in_msg_) in [r for e in core_groups for r in e]:
              continue 
            e_ = g_edge(f"(j, out_c_{in_msg_})", f"(i, in_c_{in_msg_})", "match_w_val_correponding")
            val_ = f"AssocValEqCmp (j, out_c_{in_msg_}) (i, in_c_{in_msg_})"
            if src_ != "c": # in_out_msg_src_dst_mapping[1][in_msg_] != "core":
              print("==> in h", in_msg_)
              in_ = True 
              for possible_h in home_paths_names:
                if not ('out', in_msg_) in possible_h['txn'][2]['out_msg_dst']['src']:
                  in_ = False
                  break
              # this in_h_{in_msg_} is alreayd satisfied by all possible its home-level txns/upaths
              if in_:
                in_msg_val_bind_h_skip.add(titm)
                # # otherwise it means the message is sometimes satisfied by the contingent home level paths 
                # e_ =  g_edge(f"(j, (0, h_out_{in_msg_}))", f"(i, in_h_{in_msg_})", "match_w_val_correponding_others_home")
                # val_ = f"AssocValEqCmp  (j, (0, h_out_{in_msg_})) (i, in_h_{in_msg_})"
                # print("====>", titm)
                # # the j could be the same as i depending on whether this h_out msg is processing its own trxn or someone else's 
                # # In export_core_upath we handle the case for "h"
                # # if its always address by its own home field we don't need to add 
                # acc_.append(f"(exists microop \"j\", SamePhysicalAddress i j /\\ ~SameCore i j /\\ \n {e_} /\\ \n {val_})")
              else:
                print("====> in_h_msg?? ", src_, in_msg_)
            else:
              acc_.append(f"(exists microop \"j\", ~SameCore i j /\\ SamePhysicalAddress i j /\\ \n {e_} /\\ \n {val_})")

          #TODO: _postfix_data endstate is in there? if not, empty path for the post-fix path 
          # TODO: ordering of the home_paths_name other transacations 
          self.all_core_paths[req].append({'idx': self.core_upath_idx, 'upath_predicates': acc_, 
            'precond_q': core_initial_, 'home_paths_names': home_paths_names, 'true_empty_path': False, 'end_state': an_order_picl[-1], 'nodes': nodes_cur, 
            'core_groups': core_groups, 'order_picl': an_order_picl, 'in_msg_val_bind': in_msg_val_bind, 'in_msg_val_bind_h_skip': in_msg_val_bind_h_skip})
          # for possible_h in home_paths_names:
          #   my_own_txn = possible_h['txn'][1]
          #   self.home_upath_names_used.add(my_own_txn) 
          #   self.home_upath_idx_used.add(int(my_own_txn.split("_")[-1]))
          #   for other_c_possible in possible_h['other_txns']:
          #     for other_c in other_c_possible:
          #       nm_ = f"h_case_{other_c[0][0]}_{other_c[0][1]}_{other_c[3]}"
          #       self.home_upath_idx_used.add(int(other_c[3]))
          #       self.home_upath_names_used.add(nm_) 
          self.core_upath_idx += 1
          print("--> adding req", req, len(self.all_core_paths[req]))
          pprint(self.all_core_paths[req][-1])
        
    # for evict artificial nop path 
    # for initial state that doesn't take in evict request 
    initial_state = [k[0] for k, v in self.core_upath_txn.items() if k[1] == "ci_evict"]
    initial_state += [k[0] for k, v in self.core_upath_no_txn.items() if k[1] == "ci_evict"]
    print("--> evict nop paths", initial_state)
    for other_state in all_cc_stable_states:
      if other_state in initial_state:
        continue
      acc_ = [g_edge("(i, CReq)", "(i, MResp)", "evict_nop")]
      acc_.append(self.g_empty_paths("i", "core"))
      # TODO acc_.append(("selective_empty_path", set())) 
      core_initial_ = [] # current instruction is i and other instruction is q
      core_initial_.append(g_edge(f"(q, cc_{other_state}_1)", f"(q, cc_{other_state}_lst)", "evict_nop"))
      core_initial_.append(g_edge(f"(q, cc_{other_state}_1)", f"(i, CReq)"))
      core_initial_.append(non_intervene_core("i", "q", all_cc_stable_states)) # no intervening instruction in between q and i
      non_inter = self.non_intervene_core_postfix("q", other_state, self.post_fix_states)
      if non_inter != "":
        core_initial_.append(non_inter)
      # no picl and no txn
      if not 'ci_evict' in self.all_core_paths:
        self.all_core_paths['ci_evict'] = []
      self.all_core_paths['ci_evict'].append(
        {'idx': self.core_upath_idx, 
        'upath_predicates': acc_,
        'precond_q': core_initial_, 
        'home_paths_names': None, 
        'true_empty_path': True,  
        'end_state': None, 'nodes': set(), 'core_groups': [], 'in_msg_val_bind': set() })
      self.core_upath_idx += 1

    self.nodes_in_req_serving_paths.update(nodes_)

  def chk_any_new_picl(self, hstate_, rest_of_path):
    hstate = hstate_
    any_new_picl = False
    picls = []
    for ele in rest_of_path:
      inmsg_type, hstate_prime = ele
      trans_info = self.home_dict[(hstate, inmsg_type)]['transition_info'][hstate_prime]
      # we see if this path instantiatses any new picl 
      any_new_picl = any_new_picl or (hstate != hstate_prime) or trans_info['val_change']
      
      if self.en_owner and 'owner_change' in trans_info:
        any_new_picl = any_new_picl or trans_info['owner_change']
      hstate = hstate_prime
    print("->", hstate_, rest_of_path, any_new_picl)
    return any_new_picl

  def construct_home_upath(self):
    nodes_ = set()
    home_upath_idx = 0

    path_change_owner = []
    # collect paths that change owner 
    for upath_idx, upath in enumerate(self.home_all_paths):
      hstate = upath[0]
      initial_hstate_ = upath[0]
      rest_of_path = upath[1]
      owner_change_to_src = None
      owner_change_to_src_hstate = None
      for ele in rest_of_path:
        inmsg_type, hstate_prime = ele
        info = self.home_dict[(hstate, inmsg_type)]['transition_info'][hstate_prime]
        if not 'owner_change' in info: 
          continue 
        if info['owner_change']:
          if info['owner_change_src'] == "inmsg.src":
            owner_change_to_src = True if owner_change_to_src is None else (owner_change_to_src)
            owner_change_to_src_hstate = hstate_prime
          else:
            owner_change_to_src = False
        hstate = hstate_prime

      pools = [] 
      hstate = upath[0]
      for ele in rest_of_path:
        inmsg_type, hstate_prime = ele
        pools.append(self.home_dict[(hstate, inmsg_type)]['transition_info'][hstate_prime]['out_msg_sets'])
        hstate = hstate_prime
      combinations = list(itertools.product(*pools))

      inmsg_type, hstate_prime = rest_of_path[0]
      out_msg_set_dst = {"src": [], "not_src": []}
      out_msg_set_dst['src'].append(("in", inmsg_type))
      for msg_, dst_ in self.home_dict[(initial_hstate_, inmsg_type)]['transition_info'][hstate_prime]['out_msg_dst'].items():
        if dst_ == f'always_{inmsg_type}.src': 
          out_msg_set_dst['src'].append(("out", msg_))
        if dst_ == f'always_not_{inmsg_type}.src': 
          out_msg_set_dst['not_src'].append(("out", msg_))

      if not self.en_src_core_check_home:
        # TODO
        if initial_hstate_ == "directory_M" and rest_of_path[0][0] == "GetS" and len(rest_of_path) == 2:
          out_msg_set_dst['not_src'].append(("in", "WB"))

      for list_out_msg_set_idx, a_list_of_out_msg_set in enumerate(combinations):
        if owner_change_to_src is not None and owner_change_to_src:
          # TODO add the state to the element
          path_change_owner.append({'h_path_idx': home_upath_idx, 'h_state': owner_change_to_src_hstate})
        home_upath_idx += 1

    print("==> path_change_owner", path_change_owner)
    home_upath_idx = 0
    for upath_idx, upath in enumerate(self.home_all_paths):
      hstate = upath[0]
      initial_hstate_ = upath[0]
      rest_of_path = upath[1]
      print("[DEBUG] hstate = ", hstate, rest_of_path)
      if not (hstate, rest_of_path[0][0]) in self.req_serving_home_upath:
        self.req_serving_home_upath[(hstate, rest_of_path[0][0])] = []

      # Cross product of each transition msg_out sets    
      pools = [] 
      for ele in rest_of_path:
        inmsg_type, hstate_prime = ele
        pools.append(self.home_dict[(hstate, inmsg_type)]['transition_info'][hstate_prime]['out_msg_sets'])
        hstate = hstate_prime
      combinations = list(itertools.product(*pools))
      print("--> combinations len: ", len(combinations))

      inmsg_type, hstate_prime = rest_of_path[0]
      out_msg_set_dst = {"src": [], "not_src": []}
      out_msg_set_dst['src'].append(("in", inmsg_type))
      for msg_, dst_ in self.home_dict[(initial_hstate_, inmsg_type)]['transition_info'][hstate_prime]['out_msg_dst'].items():
        if dst_ == f'always_{inmsg_type}.src': 
          out_msg_set_dst['src'].append(("out", msg_))
        if dst_ == f'always_not_{inmsg_type}.src': 
          out_msg_set_dst['not_src'].append(("out", msg_))

      if not self.en_src_core_check_home:
        if initial_hstate_ == "directory_M" and rest_of_path[0][0] == "GetS" and len(rest_of_path) == 2:
          out_msg_set_dst['not_src'].append(("in", "WB"))
          print("[TMP][DEBUG] adding", out_msg_set_dst) #.subsets())
            
          #TODO

      for list_out_msg_set_idx, a_list_of_out_msg_set in enumerate(combinations):
        # ==> this is a unique home level upath: hstate + rest_of_path with outmsg_set (i.e., a_list_of_out_msg_set)
        initial_hstate = upath[0]
        hstate = upath[0]
        rest_of_path = upath[1]

        # conjunction of predicates
        nodes_cur = set() # this path what nodes occur  (location, node_label)
        acc_ = [] 
        share_pred = []
        remote_initial = [] # on microop k that will be "SamePhysicalAddress k i /\ ~SameMicroop k i /\ {predicates in remote_initial}"
        remote_initial_k_cond = []

        remote_initial.append(g_edge(f"(k, (0, h_{hstate}_1))", f"(k, (0, h_{hstate}_lst))"))

        # core-level connecting to this home-level upath
        inmsg_type, hstate_prime = rest_of_path[0]
        acc_.append(g_edge(f"(i, out_h_{inmsg_type})", f"(i, (0, h_in_{inmsg_type}))", "stitch_h_c"))
        if (inmsg_type in resp_msg_types_w_data or inmsg_type in req_msg_types_with_data):
          acc_.append(f"AssocValEqCmp (i, out_h_{inmsg_type}) (i, (0, h_in_{inmsg_type}))")

        new_picl_chk = self.chk_any_new_picl(hstate, rest_of_path)
        cur_node = f"(i, (0, h_in_{inmsg_type}))"
        if new_picl_chk:
          remote_initial.append(g_edge(f"(k, (0, h_{hstate}_lst))", cur_node))
          pred_t = [f"(EdgeExists ((k, (0, h_{hstate}_lst)), (q, (0, h_{interm_s}_1)), \"inter_\", \"black\") /\\ \n EdgeExists ((q, (0, h_{interm_s}_1)), (i, (0, h_{hstate_prime}_1)), \"inter_\", \"black\"))" for interm_s in all_llc_stable_states]
          pred_t_s = "(" + " \\/ \n".join(pred_t) + ")"
          remote_initial.append(f'~(exists microop "q",  ~SameMicroop q k /\\ SamePhysicalAddress q k /\\  ~SameMicroop q i /\\ \n {pred_t_s})')
        else:
          remote_initial.append(g_edge(f"(k, (0, h_{hstate}_1))", cur_node))
          pred_t = [f"(EdgeExists ((k, (0, h_{hstate}_lst)), (q, (0, h_{interm_s}_1)), \"inter_\", \"black\") /\\ \n EdgeExists ((q, (0, h_{interm_s}_1)), (i, (0, h_in_{inmsg_type})), \"inter_\", \"black\"))" for interm_s in all_llc_stable_states]
          pred_t_s = "(" + " \\/ \n".join(pred_t) + ")"
          remote_initial.append(f'~(exists microop "q",  ~SameMicroop q k /\\ SamePhysicalAddress q k /\\  ~SameMicroop q i /\\ \n {pred_t_s})')
        home_path_group_info_ = []

        # non interven
        tmpprev = rest_of_path[0][1]
        for itm in rest_of_path[1:]:
          disj = []
          for inter_hstate in all_llc_states:
            disj.append(f"(EdgeExists ((i, (0, h_{tmpprev}_lst)), (r, (0, h_{inter_hstate}_1)), \"home_inter\", \"black\") /\\ EdgeExists ((r, (0, h_{inter_hstate}_1)), (i, (0, h_{itm[1]}_1)), \"home_inter\", \"black\"))")
          acc_.append("~(exists microop \"r\", SamePhysicalAddress i r /\\ ~SameMicroop i r /\\ \n ({disjunct}))".format(disjunct=" \\/ ".join(disj)))

        if debug_ and len(rest_of_path) == 2:
          # groups of same core 
          home_path_group_info_ = [[("out", "Fwd_GetS"), ("in", "WB")]]
          for g_of_msgs in home_path_group_info_:
            # correspondance 
            pred = []
            for g_msg_itm in g_of_msgs:
              dir_, msgtype_ = g_msg_itm
              if dir_ == "out":
                pred.append(g_edge(f"(i, (0, h_out_{msgtype_}))", f"(j, in_h_{msgtype_})"))
                if is_data_type(msgtype_):
                  pred.append(f"AssocValEqCmp (i, (0, h_out_{msgtype_})) (j, in_h_{msgtype_})")
              else: 
                pred.append(g_edge(f"(j, out_h_{msgtype_})", f"(i, (0, h_in_{msgtype_}))"))
                if is_data_type(msgtype_):
                  pred.append(f"AssocValEqCmp (j, out_h_{msgtype_}) (i, (0, h_in_{msgtype_}))")

            acc_.append("(exists microop \"j\", ~SameCore i j /\\ SamePhysicalAddress i j /\\ \n {edge_exists})".format(edge_exists=" /\\ ".join(pred)))
        
        cur_node = None
        ele_idx = 0
        in_out_msg_list = []
        # constructing the predicates 
        prev_hstate = hstate
        for ele, outmsg_set in zip(rest_of_path, a_list_of_out_msg_set):
          inmsg_type, hstate_prime = ele
          in_out_msg_list.append(("in", inmsg_type))
          if len(self.home_dict[(prev_hstate, inmsg_type)]['transition_info'][hstate_prime]['out_msg_sets']) > 1:
            # we see if there is precondition
            print("more than 2?", prev_hstate, inmsg_type, )
            precond = None 
            if True:
              print("DEBUG", len(outmsg_set))
              precond = "sharer_empty_except_src" 
              if (len(outmsg_set)) > 1: 
                precond = "sharer_nonempty"
              
            else: 
              precond = self.home_dict[(prev_hstate, inmsg_type)]['transition_info'][hstate_prime]['out_msg_sets_precond'][list(sorted(outmsg_set))]

            if precond == "sharer_nonempty":
              print("SHAR NONEMPTY")
              # sends out the message to sharere, meaning 
              # exists at least one sharer
              add_sharer = []

              # TODO
              # its Inv message sent out to all sharers 
              outmsg_to_sharer = ["Inv"]
              sst_imp_sharer = ["cc_cache_S_1"]
              for itm in sst_imp_sharer:
                add_sharer.append(f'EdgeExists ((j, {itm}), (i, (0, h_in_{inmsg_type})), "before")')
                add_sharer.append(f'(AccessType InitAcc j /\\ NodeExists (j, {itm}))')

              # Find in_msg types that can trigger sharer_change with sharer_change_src_added
              sharer_change_msgs = set()
              sharer_no_change_msgs = set()
              for (hstate_k, inmsg_k), home_info_k in self.home_dict.items():
                for hstate_prime_k, trans_info_k in home_info_k.get('transition_info', {}).items():
                  if trans_info_k.get('sharer_chage', False):
                    if trans_info_k.get('sharer_change_src_added', False):
                      sharer_change_msgs.add(inmsg_k) # append((inmsg_k, hstate_k, hstate_prime_k))
                    else:
                      sharer_no_change_msgs.add(inmsg_k)

              if len(sharer_change_msgs) > 0:
                for add_itm in sorted(sharer_change_msgs):
                  add_sharer.append(f'EdgeExists ((j, (0, h_in_{add_itm})), (i, (0, h_in_{inmsg_type})), "add_sharer_before")')

              preds = []
              j_got_inv = []
              not_j_got_inv = []
              n_nd = []
              for msg_sh in outmsg_to_sharer:
                tmp_h_labels = [f"in_h_{msg_sh}"]
                if f"in_h_{msg_sh}" in self.overlapped_nodes:
                  alt_label = self.overlapped_nodes[f"in_h_{msg_sh}"]
                  tmp_h_labels.append(alt_label)
                not_j_got_inv.append(g_edge(f"(i, (0, h_out_{msg_sh}))", f"(k, in_h_{msg_sh})", "home_to_core_sharer"))
                not_j_got_inv.append(g_edge(f"(i, (0, h_in_{inmsg_type}))", f"(k, (0, h_in_{inmsg_type}))", "home_to_core_sharer"))
                for h_ll in tmp_h_labels:
                  j_got_inv.append(g_edge(f"(i, (0, h_out_{msg_sh}))", f"(j, {h_ll})", "home_to_core_sharer"))
                  n_nd.append(f"~NodeExists (j, {h_ll})")

                  # cj.append("(" + " \\/ \n \t\t ".join(add_sharer) + ")")
                  # preds.append("(" + " /\\ \n".join(cj) + ")")
                  # print("===>", preds)
                # the core may be conditional e.g, owner or sharere
              not_j_got_inv_s = " /\\ \n".join(not_j_got_inv)
              not_j_inv_s = "(" + " /\\".join(n_nd) + " \n /\\ " +  \
              f"(exists microop \"k\", ProgramOrder j k /\\ SamePhysicalAddress j k /\\ ~AccessType InitAcc k /\\ \n ({not_j_got_inv_s}))" +  \
               ")"
              share_pred.append("(exists microop \"j\", ~SameCore i j /\\ SamePhysicalAddress i j /\\ \n ({add_shar}) /\\ \n (({j_inv}) \\/ ({not_j_inv})) )".format(add_shar=" \\/ \n".join(add_sharer), j_inv= " \\/ \n ".join(j_got_inv), not_j_inv=not_j_inv_s))
              # and for all sharere we send out the message
            elif precond == "sharer_empty_except_src":
              # meaning that all action that can add a core into the sharer list already been removed by some action
              add_sharer = []

              # Find in_msg types that can trigger sharer_change with sharer_change_src_added
              sharer_change_msgs = set()
              sharer_no_change_msgs = set()
              for (hstate_k, inmsg_k), home_info_k in self.home_dict.items():
                for hstate_prime_k, trans_info_k in home_info_k.get('transition_info', {}).items():
                  if trans_info_k.get('sharer_chage', False):
                    if trans_info_k.get('sharer_change_src_added', False):
                      sharer_change_msgs.add(inmsg_k) # append((inmsg_k, hstate_k, hstate_prime_k))
                    else:
                      sharer_no_change_msgs.add(inmsg_k)

              rm_itself_msg = set()
              not_rm_itself_msg = set()
              remove_sharer = []
              # from same core
              for (hstate_k, inmsg_k), home_info_k in self.home_dict.items():
                for hstate_prime_k, trans_info_k in home_info_k.get('transition_info', {}).items():
                  if trans_info_k.get('sharer_chage', False):
                    if trans_info_k.get('sharer_change_src_removed', False):
                      rm_itself_msg.add(inmsg_k)
                    else:
                      print("->", hstate_prime_k, hstate_k, inmsg_k)
                      not_rm_itself_msg.add(inmsg_k)
              print(f"[DDDEBUG] in_msg triggering sharer_change with src_added: {sharer_change_msgs}")
              print(f"[DDDEBUG] rm_itself: {rm_itself_msg}")
              if len(rm_itself_msg) and len(sharer_change_msgs):
                print(not_rm_itself_msg)
                assert(len(rm_itself_msg & not_rm_itself_msg) == 0)
                assert(len(sharer_no_change_msgs & sharer_change_msgs) == 0)
                for add_itm in sorted(sharer_change_msgs):
                  add_sharer.append(f'EdgeExists ((r, (0, h_in_{add_itm})), (i, (0, h_in_{inmsg_type})), "before")')
                  for itm in sorted(rm_itself_msg):
                    remove_sharer.append(f'(ProgramOrder r k /\\ EdgeExists ((r, (0, h_in_{add_itm})), (k, (0, h_in_{itm})), "before") /\\ EdgeExists ((k, (0, h_in_{itm})), (i, (0, h_in_{inmsg_type})), "before"))')

              # not from same core but can remove element(s) from share list 
              llc_sst_no_sharer = ["directory_M"]
              # TODO
              for sst in llc_sst_no_sharer:
                for add_itm in sharer_change_msgs:
                  remove_sharer.append(f'(EdgeExists ((r, (0, h_in_{add_itm})), (k, (0, h_{sst}_1)), "before") /\\ EdgeExists ((k, (0, h_{sst}_1)), (i, (0, h_in_{inmsg_type})), "before"))')

              if len(add_sharer) != 0:
                pred_core_added_to_sharer = " \\/ ".join(add_sharer)
                disj_to_rm_from_sharer = "(" + "\\/ \n".join(remove_sharer) + ")"
                acc_.append(f'''
(forall microop "r", SamePhysicalAddress i r => 
% core of r is in sharer list 
({pred_core_added_to_sharer}) => 
% they are remove already before this particular home upath for i
(exists microop "k", SamePhysicalAddress k r /\\ 
  {disj_to_rm_from_sharer}
)
)
                ''')

              # for case r not having direct interaction (i.e., not necessarily r has (0, h_in_{some_msg}))
              # TODO
              add_sharer = []
              remove_sharer = []
              sst_imp_sharer = ["cc_cache_S_1"]
              for itm in sst_imp_sharer:
                add_sharer.append(f'EdgeExists ((r, {itm}), (i, (0, h_in_{inmsg_type})), "before")')
              print("TODO ginit")
              add_sharer.append("(AccessType InitAcc r /\\ NodeExists (r, cc_cache_S_1))")
              for add_itm in sst_imp_sharer:
                for itm in sorted(rm_itself_msg):
                  remove_sharer.append(f'(ProgramOrder r k /\\ EdgeExists ((r, {add_itm}), (k, (0, h_in_{itm})), "before") /\\ EdgeExists ((k, (0, h_in_{itm})), (i, (0, h_in_{inmsg_type})), "before"))')
              llc_sst_no_sharer = ["directory_M"]
              # TODO
              for sst in llc_sst_no_sharer:
                for add_itm in sst_imp_sharer:
                  remove_sharer.append(f'(EdgeExists ((r, {add_itm}), (k, (0, h_{sst}_1)), "before") /\\ EdgeExists ((k, (0, h_{sst}_1)), (i, (0, h_in_{inmsg_type})), "before"))')
              if len(add_sharer) != 0:
                pred_core_added_to_sharer = " \\/ ".join(add_sharer)
                disj_to_rm_from_sharer = "(" + "\\/ \n".join(remove_sharer) + ")"
                acc_.append(f'''
(forall microop "r", SamePhysicalAddress i r => 
% core of r is in sharer list 
({pred_core_added_to_sharer}) => 
% they are remove already before this particular home upath for i
(exists microop "k", SamePhysicalAddress k r /\\ 
  {disj_to_rm_from_sharer}
)
)
                ''')
            else:
              assert(0)

          for itm in outmsg_set:
            in_out_msg_list.append(("out", itm))
            ret = [msg_ for msg_, dst_ in self.home_dict[(prev_hstate, inmsg_type)]['transition_info'][hstate_prime]['out_msg_dst'].items() if msg_ == itm]
            assert(len(ret) > 0)

          

          nodes_cur.add(f"(0, h_in_{inmsg_type})")
          if cur_node is not None:
            # prev picl immediatly precededs this inmsg_type
            cur_node_next = f"(i, (0, h_in_{inmsg_type}))" 
            assert("lst" in cur_node)
            acc_.append(g_edge(cur_node_next, cur_node, "home_upath_nxt"))
            acc_.append(g_edge(cur_node, f"(i, (0, h_{hstate_prime}_1))", "home_upath_nxt"))
            # cur_node = f"(i, (0, h_{hstate_prime}_1))"
          else:
            assert(ele_idx == 0)
            # {hstate} takes in {inmsg_type} and transitions to {hstate_prime} 
            cur_node = f"(i, (0, h_in_{inmsg_type}))"

          trans_info = self.home_dict[(prev_hstate, inmsg_type)]['transition_info'][hstate_prime] 
          if 'precondition' in trans_info:
            precond = []
            # TODO
            init_acc_owner = ["(AccessType InitAcc m /\\ " + g_node("m", "(0, h_directory_M_1)", w_pred=True) + ")"]
            if "src_not_owner" in trans_info['precondition']:
              # this instruction o that does incur change owner (h_case_pred) at the home level should not be the same core and 
              # the remote_initial handle the immediate hstate for a path to show
              # i.e., 
              remote_initial_k_cond.append("~SameCore i k")
              # We add additional constrains that there exists some instruction (m) of ""different core""" exhibit path that acquire owner (src_not_owner)
              # AND exists no other instruction (r) from same core that exhibit paths that acquired owner comes in between 
              m_paths = "(" + " \\/ ".join([g_node("m", f"h_case_{v['h_path_idx']}",  w_pred=True) for v in path_change_owner] + init_acc_owner) + ")"

              inter_s = []
              for m_hstates in sorted(set([v['h_state'] for v in path_change_owner])):
                for r_hstates in sorted(set([v['h_state'] for v in path_change_owner])):
                  r_node_1, r_node_lst = f"(r, (0, h_{r_hstates}_1))", f"(r, (0, h_{r_hstates}_lst))"
                  inter_s.append("(" + g_edge(f"(m, (0, h_{m_hstates}_lst))", r_node_1, "owner_inter") + " /\\ " + g_edge(r_node_lst, f"(i, (0, h_in_{inmsg_type}))", "owner_inter") + ")")

              r_paths_acc_s = "(" + " \\/ ".join([g_node("r", f"h_case_{v['h_path_idx']}",  w_pred=True) for v in path_change_owner]) + ")  /\\ \n" 
              r_paths_acc_s += "(" + " \\/ \n ".join(inter_s) + ")"
              precond.append(f"(exists microop \"m\", SamePhysicalAddress i m /\\ ~SameCore i m /\\ \n{m_paths} /\\ \n % src not owner \n ~(exists microop \"r\", SamePhysicalAddress i r /\\ ProgramOrder r i /\\ \n{r_paths_acc_s}))")

            if "src_owner" in trans_info['precondition']:
              remote_initial_k_cond.append("ProgramOrder k i")
              # This constrains there exists some instruction (m) of same core as i that exhibits the paths that acquired the owner (src_owner)
              # AND exists no other instruction (r) from other core that exhibit paths that acquired owner comes in between 

              # m_paths = "(" + " \\/ ".join([g_node("m", f"h_case_{e}",  w_pred=True) for e in path_change_owner] + init_acc_owner) + ")"

              # # r_paths = "(" + " \\/ ".join([(g_edge("(m, (0, {m_hstate}))", "(r, (0, {m_hstate}))", "inter_owner2") + " /\\ " g_node("r", f"h_case_{e}",  w_pred=True) + g_edge("(r, (0, {m_hstate}))", "i, (0, h_in_{inmsg_})")) for e in path_change_owner] + init_acc_owner) + ")"
              # r_paths = ""

              # precond.append(f"(exists microop \"m\", SamePhysicalAddress i m /\\ ProgramOrder m i /\\ {m_paths} /\\ ~(exists microop \"r\", SamePhysicalAddress i r /\\ ~SameCore r i /\\ {r_paths}))")

              m_paths = "(" + " \\/ ".join([g_node("m", f"h_case_{v['h_path_idx']}",  w_pred=True) for v in path_change_owner] + init_acc_owner) + ")"

              inter_s = []
              for m_hstates in sorted(set([v['h_state'] for v in path_change_owner])):
                for r_hstates in sorted(set([v['h_state'] for v in path_change_owner])):
                  r_node_1, r_node_lst = f"(r, (0, h_{r_hstates}_1))", f"(r, (0, h_{r_hstates}_lst))"
                  inter_s.append("(" + g_edge(f"(m, (0, h_{m_hstates}_lst))", r_node_1, "owner_inter") + " /\\ " + g_edge(r_node_lst, f"(i, (0, h_in_{inmsg_type}))", "owner_inter") + ")")

              r_paths_acc_s = "(" + " \\/ ".join([g_node("r", f"h_case_{v['h_path_idx']}",  w_pred=True) for v in path_change_owner]) + ")  /\\ \n" 
              r_paths_acc_s += "(" + " \\/ \n ".join(inter_s) + ")"
              precond.append(f"(exists microop \"m\", SamePhysicalAddress i m /\\ ProgramOrder m i /\\ \n {m_paths} /\\ \n ~(exists microop \"r\", SamePhysicalAddress i r /\\ ~SameCore r i /\\ \n{r_paths_acc_s}))")

            # sharere 
            if "not_last_sharer_nonempty" in trans_info['precondition']:
              pass 
            
            if "not_last_sharer_empty" in trans_info['precondition']:
              pass 
            if "last_sharer" in trans_info['precondition']:
              pass 
            if len(precond):
              acc_.append("(" + " \\/ ".join(precond) + ")")
          cur_node_next = None
          picl_in_processing = None
          if prev_hstate != hstate_prime: #hstate_prime != hstate:
            cur_node_next = f"(i, (0, h_{hstate_prime}_1))" 
            nodes_cur.add(f"(0, h_{hstate_prime}_1)")
            nodes_cur.add(f"(0, h_{hstate_prime}_lst)")
            acc_.append(g_edge(cur_node, cur_node_next, "home_upath"))
            cur_node = cur_node_next
            picl_in_processing = cur_node

          if picl_in_processing is None and (trans_info['val_change'] or 
            (trans_info['owner_change'] and self.en_owner)):
            cur_node_next = f"(i, (0, h_{prev_hstate}_1))" 
            nodes_cur.add(f"(0, h_{prev_hstate}_1)")
            nodes_cur.add(f"(0, h_{prev_hstate}_lst)")
            acc_.append(g_edge(cur_node, cur_node_next, "home_upath"))

            cur_node = cur_node_next
            picl_in_processing = cur_node

          if picl_in_processing is None and trans_info['owner_change'] and self.en_owner:
            assert(0)

          home_in_msg_val_bind = {}
          # the value for this new picl
          if cur_node_next is not None:
            if trans_info['val_change']:
              # check 
              if trans_info['val_change_src'] == 'inmsg.cl':
                if 'mmem_change' in trans_info and not trans_info['mmem_change']:
                  print("TODO ? the main memory is not sync?! ")
                acc_.append(f"AssocValEqCmp (i, (0, h_in_{inmsg_type})) {cur_node_next}")
                home_in_msg_val_bind[inmsg_type] = cur_node_next
              elif trans_info['val_change_src'] == 'main_mem':
                if 'mmem_change' in trans_info and trans_info['mmem_change']:
                  print("TODO ? the main memory is not sync?! ")
                # TODO: currently we model the main memory's value in the home's invalid state, which should be the initial state when v['val_aws_to_main_mem'] is true 
                remote_initial.append(f"AssocValEqCmp {cur_node_next} (k, (0, h_{prev_hstate}_1))")
                print("---> TODO 170", remote_initial[-1], "; ", prev_hstate, "should be invalid state, which we model main memory's value in picl for this invalid state")
              else:
                print("no value source for this picl at home level", prev_hstate, upath_idx)
            else:
              # initial condition we need to match the initial state hstate's value  
              if ele_idx == 0:
                remote_initial.append(f"AssocValEqCmp {cur_node_next} (k, (0, h_{prev_hstate}_1))")
              else:
                assert(0)
                acc_.append(f"AssocValEqCmp {cur_node_next} (i, (0, h_{prev_hstate}_1))")

          # out message to ?
          for h_send_msg_type in outmsg_set: #v['out_msg_sets']: 

            cur_node_next = f"(i, (0, h_out_{h_send_msg_type}))"
            nodes_cur.add(f"(0, h_out_{h_send_msg_type})")
            acc_.append(g_edge(cur_node, cur_node_next))

            if trans_info['out_msg_dst'][h_send_msg_type] == f'always_{inmsg_type}.src':
              acc_.append(g_edge(cur_node_next, f"(i, in_h_{h_send_msg_type})", "stitch_h_c"))
              print("[DEBUG], here", cur_node_next, h_send_msg_type)
              if h_send_msg_type in resp_msg_types_w_data or h_send_msg_type in req_msg_types_with_data:
                acc_.append(f"AssocValEqCmp (i, in_h_{h_send_msg_type}) {cur_node_next}")
            elif not ("out", h_send_msg_type) in [e for gp in home_path_group_info_ for e in gp]:
              assert(trans_info['out_msg_dst'][h_send_msg_type] == f'always_not_{inmsg_type}.src')
              # since this is sent by home, here constrains exists core that receives it 
              print("===> fail", h_send_msg_type)
              assert((not "msi_protogen_min_vv_coh_model" in coh_model_file) or len(rest_of_path) != 2) # for msi particuarlly 
              # if not (debug_ and len(rest_of_path) == 2):
              # exists some other cores that receives this message 
              
              tmp_h_labels = [f"in_h_{h_send_msg_type}"]
              if f"in_h_{h_send_msg_type}" in self.overlapped_nodes:
                print("===> in_h_{h_send_msg_type} is in overlapped nodes")
                alt_label = self.overlapped_nodes[f"in_h_{h_send_msg_type}"]
                tmp_h_labels.append(alt_label)
              preds = []
              for h_ll in tmp_h_labels:
                cj = [g_edge(cur_node_next, f"(j, {h_ll})", "home_to_core_receiver")]
                if is_data_type(h_send_msg_type):
                  cj.append(f"AssocValEqCmp {cur_node_next} (j, {h_ll}) ")
                preds.append("(" + " /\\ ".join(cj) + ")")
                # the core may be conditional e.g, owner or sharere
              acc_.append("(exists microop \"j\", ~SameCore i j /\\ SamePhysicalAddress i j /\\ \n ({edge_exists}))".format(edge_exists=" \\/ ".join(preds)))

            if is_data_type(h_send_msg_type):
              if trans_info['out_msg_val'][h_send_msg_type] == 'cl_val':
                assert(f"h_out_{h_send_msg_type}" in sorted(self.all_home_msg_labels))
                remote_initial.append(f"AssocValEqCmp (k, (0, h_{prev_hstate}_1)) {cur_node_next}")
              else:
                print("Huh unconstrain the value of message", h_send_msg_type)

            # k is the message type 
            # v is dictionary, key: cnt, dst_to_inmsg_src
                
            # add the last 
            if picl_in_processing is not None:
              if ele_idx != len(rest_of_path) - 1:
                # we get the next transition's input message 
                tmp_in_msg = rest_of_path[ele_idx+1][0]
                acc_.append(g_edge(cur_node_next, f"(i, (0, h_in_{tmp_in_msg}))"))
              else:
                end_node = picl_in_processing.replace("_1", "_lst")
                acc_.append(g_edge(cur_node_next, end_node))
            else:
              assert(not new_picl_chk)
              remote_initial.append(g_edge(cur_node_next, f"(k, (0, h_{initial_hstate}_lst))"))

          # prepare for this immeidate iteration 
          if picl_in_processing is not None:
            cur_node_next = picl_in_processing.replace("_1", "_lst")
            if ele_idx == len(rest_of_path) - 1:
              acc_.append(g_edge(cur_node, cur_node_next))
            cur_node = cur_node_next 
          ele_idx += 1
          prev_hstate = hstate_prime 

        # finish constructing this path
        acc_.append(("selective_empty_path_home", list(nodes_cur)))
        nodes_.update(nodes_cur)

        assert(len(in_out_msg_list) == len(set(in_out_msg_list)))
        nodes_cur.add(f"h_case_{home_upath_idx}")
        # predicates for this home upath, and the remote initial condition
        # TODO above should be stack 
        self.req_serving_home_upath[(initial_hstate, rest_of_path[0][0])].append({
          'name': f"h_case_{initial_hstate}_{rest_of_path[0][0]}_{home_upath_idx}", 
          'pred': acc_, 
          'path': upath,  # raw data
          'home_init': remote_initial, 
          'home_init_k_cond': remote_initial_k_cond,
          'out_msg': a_list_of_out_msg_set, 
          'home_path_idx': home_upath_idx, 
          'out_msg_dst': out_msg_set_dst, 
          'home_in_msg_val_bind': home_in_msg_val_bind,
          'sharer_pred': share_pred}) # list(out_msg_set_dst.subsets())})
        if (len(share_pred) > 0):
          print("DEBUG HERE 0418", share_pred, home_upath_idx)
        home_upath_idx += 1

        # when core doesn't feature any out_h_<> -> "h_empty_case"
        # h_empty_case = (f"h_empty", self.g_empty_paths("i", "home"), [], set())
        # out_msg_set for matching with core level upath
    self.home_upath_idx = home_upath_idx
    self.nodes_in_home_level_paths = nodes_
    print("========================================")
    print("==> home upath construction result:")
    print("========================================")
    pprint(self.req_serving_home_upath, width=100)
    
  def selective_empty_home_path(self):
    print("[INFO] Method: ", inspect.stack()[0].function)
    print("--> nodes in home_level_paths", self.nodes_in_home_level_paths)
    # given that self.home_upath_idx is settled 
    for k, a_list_of_upaths in self.req_serving_home_upath.items():
      # this upaths starts with same (hstate, in_msgtype)
      for v in a_list_of_upaths:
        acc_pred = []
        for pred in v['pred']: # v[1]:
          if type(pred) is tuple and pred[0] == "selective_empty_path_home":
            elist = pred[1]
            nlist = [g_node("i", s_prime, w_pred=True, neg=True) for s_prime in sorted(self.nodes_in_home_level_paths) if not s_prime in elist]
            print("--> nlist: ", nlist)
            if len(nlist) > 0:
              acc_pred.append("/\\ ".join(nlist))
            continue
          acc_pred.append(pred)
        hstate, inmsg_type = k
        home_idx = v['home_path_idx']
        #acc_ = f"DefineMacro \"h_case_{hstate}_{inmsg_type}\":\n"
        # TODO if not v['name'] in self.home_upath_names_used:
        #   print("--> skipping home path macro: ", v['name'])
        #   continue
        acc_ = f"DefineMacro \"{v['name']}\":\n"
        acc_ += " /\\ \n".join(acc_pred) 
        acc_ += " /\\ " + g_edge("(i, CReq)", f"(i, h_case_{home_idx})", "case") 
        n_case = []
        for tmp_idx in range(self.home_upath_idx): # + 1):
          assert(home_idx < self.home_upath_idx)
          if tmp_idx == home_idx: # v[-1]:
            continue
          # TODO if tmp_idx in self.home_upath_idx_used:
          n_case.append(g_node("i", f"h_case_{tmp_idx}", w_pred=True, neg=True))
        if len(n_case):
          acc_ += "/\\ " +  ("/\\ ".join(n_case))
        assert(len(n_case) == len(set(n_case))) 
        print("-=-> adding k: ", k)
        print(acc_) 
        self.macros += acc_ + ".\n\n"
        #  "%%" + str("%% ;;".join(v['home_init'])) + "\n\n"
        if len(v['sharer_pred']) > 0:
          self.axioms += f"Axiom \"imp_h_case_{home_idx}\":\n"
          self.axioms += f"forall microop \"i\", OnCore c i => (~AccessType InitAcc i) => \n NodeExists (i, h_case_{home_idx})  => \n "
          self.axioms += v['sharer_pred'][0]
          self.axioms += ".\n\n"
          # sha f"forall microop \"i\", OnCore c i => (~AccessType InitAcc i) => NodeExists (i, h_case_{home_idx}  => \n "

      #self.req_serving_home_upath[k] = (f"h_case_{hstate}_{inmsg_type}", acc_, remote_initial)
    
    preds = self.g_empty_paths("i", "home")
    acc_ = f"DefineMacro \"h_empty_case\":\n"
    n_case = []
    for tmp_idx in range(self.home_upath_idx): # + 1):
      n_case.append(g_node("i", f"h_case_{tmp_idx}", w_pred=True, neg=True))
      self.labels += nm_stage.format(i=self.next_i, nm=f"h_case_{tmp_idx}")
      self.next_i += 1
      self.case_labels.append(f"h_case_{tmp_idx}")
    if len(n_case):
      acc_ += ("/\\ ".join(n_case)) + " /\\ "
    acc_ += preds + ".\n\n"
    print(acc_) 
    self.macros += acc_ + "\n"

  def g_empty_paths(self, iname, tp, exclude_list=[]):
    nlist = []
    if tp == "core":
      todo = all_cc_states
      prefix = "cc"
      for state in todo:
        if state in exclude_list:
          continue
        nlist.append(g_node(iname, f"{prefix}_{state}_1"))
        nlist.append(g_node(iname, f"{prefix}_{state}_lst"))
    else:
      todo = all_llc_states
      prefix = "h"
      for state in todo:
        if state in exclude_list:
          continue
        # if not debug_ and self.en_owner:
        #   assert(0)
        nlist.append(g_node(iname, f"{prefix}_{state}_1", single=True))
        nlist.append(g_node(iname, f"{prefix}_{state}_lst", single=True))
    if tp == "core":
      #pass
      for m in sorted(self.all_core_msg_labels):
        if m in exclude_list:
          continue 
        nlist.append(g_node(iname,m))
    else:
      for m in sorted(self.all_home_msg_labels):
        if m in exclude_list:
          continue 
        # if not debug_ and self.en_owner:
        #   assert(0)
        nlist.append(g_node(iname,f"(0, {m})"))
    
    return " /\\ ".join([f"~NodeExists {n}" for n in nlist])
    
  def find_paths(self, tmp_out_h_msg, tmp_in_h_msg, acc_paths, starting_path): 
    if len(tmp_out_h_msg) == 0 and len(tmp_in_h_msg) == 0:
      perm_ = has_valid_permutation(acc_paths + [starting_path])
      # TODO: add the ordering among these acc_path + starting_path 
      # 
      # if the permutation exists we assert
      # otherwise we do iteratively CEX refining to see the total order among the acc_paths + starting_path
      self.all_combs.append(acc_paths)
      # did the acc_path can be satisfiable based on the transition table?
      # if len(perm_) > 0:
      #   # all_combs.append(perm_)
      #   all_combs += perm_
      #   print("\t==> acc_paths", perm_)
      # if len(perm_) > 1:
      #   print("===> more than one", perm_)
      print("==> acc_paths", acc_paths, len(perm_))
      return 
    for tmp_k, tmp_v in self.req_serving_home_upath.items():
      hstate, inmsg = tmp_k
      for idx, upath in enumerate(tmp_v):
        # could this upath be satisfying the rest 
        out_msg_list_tmp = upath['out_msg']
        all_sat = True                    
        all_zero_length = True
        in_to_remove = []
        out_to_remove = []
        for t_out_msg_set in out_msg_list_tmp:
          if len(t_out_msg_set) != 0:
            all_zero_length = False
          for e in t_out_msg_set: 
            if ("out", e) in upath['out_msg_dst']['not_src']:
              all_sat = all_sat and (e in tmp_in_h_msg)
              in_to_remove.append(e)
        for e in upath['path'][1]:
          in_msg_type, state_prime = e
          if ("in", in_msg_type) in upath['out_msg_dst']['not_src']:
            all_sat = all_sat and (in_msg_type in tmp_out_h_msg)
            out_to_remove.append(in_msg_type)
        # if  not len(in_to_remove) all_sat or all_zero_length: 
        if len(in_to_remove) == 0 and len(out_to_remove) == 0:
          continue 
        if not all_sat:
          continue
        # all_sat is true 

        for itm in in_to_remove:
          tmp_in_h_msg.remove(itm)
        for itm in out_to_remove:
          tmp_out_h_msg.remove(itm)
        self.find_paths(tmp_out_h_msg[:], tmp_in_h_msg[:], acc_paths + [(tmp_k, idx, upath['path'], upath['home_path_idx'], (in_to_remove, out_to_remove))], starting_path)
        # 'path': the complete path  -> upath['path'][0] = initial_hstate and rest_of_path is upath['path'][1]

        for itm in in_to_remove:
          tmp_in_h_msg.append(itm)
        for itm in out_to_remove:
          tmp_out_h_msg.append(itm)


  def export(self, fnm):
    with open(fnm, "w") as f:
      f.write(self.labels)
      f.write("\n")
      f.write(self.macros)
      f.write("\n")
      f.write(self.axioms)
      # f.write("Axiom \"J\":\nforall microop \"i\", ExpandMacro h_case_H_I_GetMsg.")

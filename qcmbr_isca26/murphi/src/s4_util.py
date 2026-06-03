import os 
import pickle
import re
from gconst import *
from common_templates import *
from collections import OrderedDict
from pprint import pprint
build_dir="build"
def get_res_gchk(resff):
  dst_always_defined = None
  with open(resff, "r") as f:
    st = True
    for line in f:
      if st: 
        assert ("proven" in line)
        st = False
      else:
        if "cex" in line:
          # dst_always_define is false 
          dst_always_defined = False
        else:
          dst_always_defined = True
  return dst_always_defined
def get_s_from_rset(aset):
  rset_s = ""
  for s_ in all_cc_states:
    if s_ in aset:
      rset_s += dis_ele.format(state=s_, inset="1")
    else:
      rset_s += dis_ele.format(state=s_, inset="0")
  return rset_s

def get_msg_dst(resff):
  ret = None
  with open(resff , 'r', encoding='utf-8') as f:
    content = f.read()

  transitions = content.split('----------')
  if not transitions:
    print("Trace file appears to be empty or invalid.")
    return

  # --- 1. Get initial values from the start state ---
  start_state_block = transitions[0]
  cur_ = {f"prevMsg.{m_msg_type_field}": None, f"prevMsg.{m_msg_src_field}": None, f"prevMsg.{m_msg_dst_field}": None, "selc": None} 
  ret = {}
  def get_block(block, prev):
    for tar in prev.keys(): #["prevProcs", "prevMsg_chk"]:
      selc_match = re.search(fr'^\s*{tar}:\s*(\w+)', block, re.MULTILINE)
      if selc_match:
        selc_value = selc_match.group(1)
        prev[tar] = selc_value
    return prev
  cur_ = get_block(start_state_block, cur_)
  # --- 2. Process subsequent transitions ---
  # print("Searching for changes in 'msg_rec_set' and reporting most recent 'i_cache' value...")
  for i, block in enumerate(transitions[1:]):
    # update the last know values from the block info
    if "last state" in block:
      break
    cur_ = get_block(block, cur_)
    sent_match = re.search(r"msg_sent_set\[(\w+)\]:(\w+)", block)
    if sent_match:
      msg_type = sent_match.group(1)
      is_active = sent_match.group(2).lower() 
      if not  (cur_[f"prevMsg.{m_msg_type_field}"] == msg_type):
        print((cur_[f"prevMsg.{m_msg_type_field}"], msg_type), f"prevMsg.{m_msg_type_field}")
      assert(cur_[f"prevMsg.{m_msg_type_field}"] == msg_type)
      dst = cur_[f"prevMsg.{m_msg_dst_field}"]
      ret[msg_type] = dst 
  return ret

def prepare_header_and_rset(outff_h, design_file, aset):
  with open(f"{design_file}", "r") as tmpf:
    for ln in tmpf:
      # if "if (false) then  -- #define ENABLE_TRACK" in ln:
      #   outff_h.write(ln.replace("false", "true"))
      # elif "if (true) then -- #define END_TRACK_CONDITION" in ln:
      #   disjunct = " | ".join([end_tracking_condition.format(state=s) for
      #       s in all_cc_stable_states])
      #   outff_h.write(f"if (!({disjunct})) then\n")
      # else:
      outff_h.write(ln)

  rset_s = ""
  for s_ in all_cc_states:
    if s_ in aset:
      rset_s += dis_ele.format(state=s_, inset="1")
    else:
      rset_s += dis_ele.format(state=s_, inset="0")
  return rset_s
def get_s_from_msg_combination(combo):
  msg_set_s_send_set = ""
  for s_ in all_msg_types:
    if "out_" + s_  in combo.keys():
      if combo["out_" + s_ ] == "undefined":
        msg_set_s_send_set += dis_ele_dst_undefined.format(msgtype=s_, pred=" > 0", m_msg_type_field=m_msg_type_field, 
        m_msg_dst_field=m_msg_dst_field, m_home_node=m_home_node)
      elif combo["out_" + s_ ] == "Home":
        msg_set_s_send_set += dis_ele_msgsend_dst.format(msgtype=s_, pred=" > 0", m_msg_type_field=m_msg_type_field, m_msg_dst_field=m_msg_dst_field, m_home_node=m_home_node)
      elif combo["out_" + s_ ] == "Core":
        msg_set_s_send_set += dis_ele_msgsend_dst.format(msgtype=s_, pred=" > 0", m_msg_type_field=m_msg_type_field, m_msg_dst_field=m_msg_dst_field, m_home_node=m_proc_node)
      else:
        assert(0)
    else:
      msg_set_s_send_set += dis_ele_msgsent.format(msgtype=s_, pred=" = 0", m_msg_type_field=m_msg_type_field)          
  msg_set_s_rec_set = ""
  for s_ in all_msg_types:
    if "in_" + s_ in combo.keys():
      if combo["in_" + s_ ] == "Home":
        msg_set_s_rec_set += dis_ele_msgrec_src.format(msgtype=s_, pred=" > 0", m_msg_type_field=m_msg_type_field, m_msg_src_field=m_msg_src_field, m_home_node=m_home_node)
      elif combo["in_" + s_ ] == "Core":
        msg_set_s_rec_set += dis_ele_msgrec_src.format(msgtype=s_, pred=" > 0", m_msg_type_field=m_msg_type_field, m_msg_src_field=m_msg_src_field, m_home_node=m_proc_node)
      else:
        assert(0)
    else:
      msg_set_s_rec_set += dis_ele_msgrec.format(msgtype=s_, pred=" = 0", m_msg_type_field=m_msg_type_field)
  return (msg_set_s_send_set, msg_set_s_rec_set)


def assemble_dist(debug=True):
  cores = [("", "")]
  is_local_cc = ""
  is_not_local_cc = ""
  if design_cfg.get('dist_dir', False):
    assert (design_cfg.get('is_not_local_cc', "") != "" and  \
    design_cfg.get('is_local_cc', "") != "")
    is_local_cc = design_cfg.get('is_local_cc')
    is_not_local_cc = design_cfg.get('is_not_local_cc')
    cores = [("h", f"{is_local_cc}"), ("r", f"{is_not_local_cc}")]
  # key: (state, req), the state that accept req to process

  # s1: which states accept which requests
  agg_list = []
  for scope, selc_cond in cores:
    aggregate = OrderedDict()
    postfix = f"_{scope}" if scope != "" else ""
    with open(f"{build_dir}/s1_req_acc_state/_build/res{postfix}.txt", "r") as f:
      st = False
      for ln in f:
        if ln.startswith("Reachable"):
          st = True
          continue
        elif ln.startswith("Unreachable"):
          break
        if st:
          state, req_type = ln[:-1].split(",")
          if not (state, req_type) in aggregate:
            aggregate[(state, req_type)] = OrderedDict()
          aggregate[(state, req_type)]['has_arg'] = (req_type in type_with_args)
          aggregate[(state, req_type)]['scope'] = scope

    # s2: distinguish atomic processing vs. transaction initiation
    postfix = f"_{scope}" if scope != "" else ""
    s2_res_path = f"{build_dir}/s2_req_proc_state/_build/res{postfix}.txt"

    local_core_data = {}
    if scope == "h":
        s2_local_core_path = f"{build_dir}/s2_local_core/res{postfix}.pkl"
        if os.path.exists(s2_local_core_path):
            with open(s2_local_core_path, "rb") as f:
                local_core_data = pickle.load(f)

    if not os.path.exists(s2_res_path):
       assert(0) 
    with open(s2_res_path, "r") as f:
      st = False
      for ln in f:
        if ln.startswith("Reachable"):
          cur_type = False  # "non_txn_init_perf"
          st = True
          continue
        elif ln.startswith("Unreachable"):
          cur_type = True  # "txn_init"
          st = True
          continue
        elif not st:
            continue
        state, req_type = ln[:-1].split(",")
        # if (state, req_type) in aggregate:
        if scope == 'r':
            aggregate[(state, req_type)]['txn_init'] = cur_type
        else: # scope == 'h'
            dir_involved_possible = local_core_data.get('btb_reachable_dir_involve_possible', False)
            aggregate[(state, req_type)]['txn_init'] = cur_type or (not cur_type and ((state, req_type) in dir_involved_possible))

    # s2_2, s2_3: details for non-transactional operations
    postfix = f"_{scope}" if scope != "" else ""
    s2_2_res_path = f"{build_dir}/s2_2_req_proc_state_to_state_prime_val/_build/res{postfix}.txt"
    if not os.path.exists(s2_2_res_path):
      assert(0)
    with open(s2_2_res_path, "r") as f:
      cur_type = ""
      for ln in f:
        if ln.startswith("Reachable (accept and perform (i.e., without txn) and transition to new state)"):
          cur_type = "new_state"
          continue
        elif ln.startswith("Reachable (accept and perform (i.e., without txn) with value change possible"):
          cur_type = "new_val"
          continue
        elif ln.startswith("Unreachable (accept and perform (i.e., without txn) with value change not possible"):
          cur_type = "fixed_val"
          continue
        elif "Unreachable" in ln:
          cur_type = "skip"
          continue
        # elif "Unreachable" in ln or "Reachable" in ln:
        #   cur_type = "skip"
        #   continue
        # if cur_type == "skip" or not cur_type:
        #     continue

        ln_ = ln[:-1].split(",")
        state, req_type = ln_[0], ln_[1]
        if (state, req_type) in aggregate and not aggregate[(state, req_type)]['txn_init']:
          if cur_type == "new_state":
            state_prime = ln_[2]
            aggregate[(state, req_type)]['new_state'] = state_prime
          elif cur_type == "new_val":
            aggregate[(state, req_type)]['new_val'] = True
          elif cur_type == "fixed_val":
            aggregate[(state, req_type)]['new_val'] = False

    s2_3_res_path = f"{build_dir}/s2_3_req_proc_val/_build/res{postfix}.txt"
    if not os.path.exists(s2_3_res_path):
        assert(0)
    with open(s2_3_res_path, "r") as f:
      cur_type = ""
      for ln in f:
        if "Proven" in ln:
          cur_type = "store.data"
          continue
        elif "Disproven" in ln:
          break
        if not cur_type:
            continue
        ln_ = ln[:-1].split(",")
        state, req_type = ln_[0], ln_[1]
        if (state, req_type) in aggregate and not aggregate[(state, req_type)]['txn_init']:
          aggregate[(state, req_type)]['val_src'] = cur_type

    if debug:
      pprint(aggregate)
    agg_list.append((scope, aggregate))
  #if debug:
  #  pprint(aggregate)
  # pprint(aggregate)
  return agg_list # aggregate

def assemble(debug=True):
  # key: (state, req), the state that accept req to process  
  aggregate = OrderedDict()
  with open(f"{build_dir}/s1_req_acc_state/_build/res.txt", "r") as f:
    st = False
    for ln in f:
      if ln.startswith("Reachable"):
        st = True
        continue
      elif ln.startswith("Unreachable"):
        break
      if st:
        state, req_type = ln[:-1].split(",")
        aggregate[(state, req_type)] = OrderedDict()
        aggregate[(state, req_type)]['has_arg'] = (req_type in type_with_args) 


  with open(f"{build_dir}/s2_req_proc_state/_build/res.txt", "r") as f:
    st = False 
    for ln in f:
      if ln.startswith("Reachable"):
        cur_type = False #"non_txn_init_perf"
        continue
      elif ln.startswith("Unreachable"):
        cur_type = True #"txn_init"
        continue
      state, req_type = ln[:-1].split(",")
      aggregate[(state, req_type)]['txn_init'] = cur_type

  with open(f"{build_dir}/s2_2_req_proc_state_to_state_prime_val/_build/res.txt", "r") as f:      
    for ln in f:
      if ln.startswith("Reachable (accept and perform (i.e., without txn) and transition to new state)"):
        cur_type = "new_state"
        continue
      elif ln.startswith("Reachable (accept and perform (i.e., without txn) with value change possible"):
        cur_type = "new_val"
        continue
      elif ln.startswith("Unreachable (accept and perform (i.e., without txn) with value change not possible"):
        cur_type = "fixed_val"
        continue
      elif "Unreachable" in ln:
        cur_type = "skip"
        continue
      ln_ = ln[:-1].split(",")
      state, req_type = ln_[0], ln_[1]
      assert(aggregate[(state, req_type)]['txn_init'] == False)
      if cur_type == "new_state":
        state_prime = ln_[2]
        aggregate[(state, req_type)]['new_state'] = state_prime 
      elif cur_type == "new_val":
        aggregate[(state, req_type)]['new_val'] = True
      elif cur_type == "fixed_val":
        aggregate[(state, req_type)]['new_val'] = False 
  # for thos txn_init == False and new_val == True, we see if its always the value specified in the request 
  with open(f"{build_dir}/s2_3_req_proc_val/_build/res.txt", "r") as f:      
    for ln in f:
      if "Proven" in ln:
        cur_type = "store.data"
        continue
      elif "Disproven" in ln:
        break
      ln_ = ln[:-1].split(",")
      state, req_type = ln_[0], ln_[1]
      assert(aggregate[(state, req_type)]['txn_init'] == False)
      aggregate[(state, req_type)]['val_src'] = cur_type
  # # reachable set 
  # with open("build/s3_rset_txn/_build/res.txt", "r") as f:
  #   st = False
  #   for ln in f:
  #     if ln.startswith("Reachable"):
  #       st = True
  #       continue
  #     elif ln.startswith("Unreachable"):
  #       st = False
  #       continue
  #     if not st:
  #       continue 
  #     t_ = ln[:-1].split(",")
  #     assert(len(t_) == 4)
  #     state, req, idx, rset_ss = t_

  #     if not 'upaths' in aggregate[(state, req)]:
  #       aggregate[(state, req)]['upaths'] = OrderedDict()
  #     rset = tuple(sorted(rset_ss.split("+")))
  #     tmpidx = len(aggregate[(state, req)]['upaths'].keys())
  #     aggregate[(state, req)]['upaths'][rset] = OrderedDict()
  #     aggregate[(state, req)]['upaths'][rset]['rset_idx'] = tmpidx

  # with open("build/s3_3_reachable_set_order/_build/res.txt", "r") as f:
  #   st = False
  #   for ln in f:
  #     if ln.startswith("Proven"):
  #       st = True
  #       continue
  #     ln_ = ln[:-1].split(",")
  #     state, req, idx, asets, the_set_order = ln_
  #     rset = tuple(sorted(asets.split("+")))
  #     aggregate[(state, req)]['upaths'][rset]['picl_rset_ordered'] = the_set_order.split(";")
  # for k, v in aggregate.items():
  #   if v['txn_init']:
  #     for k_, v_ in v['upaths'].items():
  #       # each k_ is an rset, and v_ contains rset relevant information 
  #       if not 'picl_rset_ordered' in v_:
  #         raise Exception("No Fixed Order?!")
  
  # with open("build/s3_2_reachable_set_val/_build/res.txt", "r") as f:
  #   diff_sec = None  
  #   subsec = False 
  #   for ln in f:
  #     if "the value component differed from previous" in ln:
  #       diff_sec = True
  #       continue
  #     if "value component always the same as data" in ln:
  #       diff_sec = False
  #     if ln.startswith("Reachable") or ln.startswith("Unreachable") or \
  #      ln.startswith("Proven") or ln.startswith("Disproven"):
  #       subsec = ln.split(":")[0]
  #       continue
  #     if diff_sec is not None and diff_sec and subsec == "Reachable":
  #       k, v = ln[:-1].split(": ")
  #       k_ = k.split(",")
  #       v_ = v.split(";")
  #       state, req, idx, rset_ss = k_
  #       rset = tuple(sorted(rset_ss.split("+")))
  #       aggregate[(state, req)]['upaths'][rset]["picl_val_eq_prev"] = []
  #       for e in aggregate[(state, req)]['upaths'][rset]["picl_rset_ordered"]:
  #         result = not (e in v_)
  #         aggregate[(state, req)]['upaths'][rset]["picl_val_eq_prev"].append(result)
  #     if diff_sec is not None and diff_sec and subsec == "Unreachable":
  #       k, v = ln[:-1].split(": ")
  #       k_ = k.split(",")
  #       v_ = v.split(";")
  #       state, req, idx, rset_ss = k_
  #       rset = tuple(sorted(rset_ss.split("+")))
  #       if "picl_val_eq_prev" in aggregate[(state, req)]['upaths'][rset]:
  #         for e in v_:
  #           assert(not (e in aggregate[(state, req)]['upaths'][rset]["picl_val_eq_prev"]))
  #       else:
  #         aggregate[(state, req)]['upaths'][rset]["picl_val_eq_prev"] = []
  #         for e in aggregate[(state, req)]['upaths'][rset]["picl_rset_ordered"]:
  #           result = (e in v_)
  #           aggregate[(state, req)]['upaths'][rset]["picl_val_eq_prev"].append(result)
  #     if diff_sec is not None and (not diff_sec) and subsec == "Proven":
  #       k, v = ln[:-1].split(": ")
  #       k_ = k.split(",")
  #       v_ = v.split(";")
  #       state, req, idx, rset_ss = k_
  #       rset = tuple(sorted(rset_ss.split("+")))
  #       aggregate[(state, req)]['upaths'][rset]["picl_val_eq_data"] = []
  #       for e in aggregate[(state, req)]['upaths'][rset]["picl_rset_ordered"]:
  #         result = e in v_
  #         aggregate[(state, req)]['upaths'][rset]["picl_val_eq_data"].append(result)
        

  # resff = "build/s4_msg_per_rset/_build/gcheck.txt"
  # dst_always_defined = get_res_gchk(resff)
  # aggregate['global'] = OrderedDict()
  # aggregate['global']['dst_always_defined'] = dst_always_defined
  # # TODO
  # aggregate['global']['per_core_msg_is_arr'] = False

  # with open("build/s4_msg_per_rset/_build/res.txt", "r") as f:
  #   first = True
  #   for ln in f:
  #     if first:
  #       first = False
  #       continue 
  #     if ln.startswith("Proven") or ln.startswith("Reachable"):
  #       st = True 
  #       cur_type = ("Proven" in ln)
  #       continue
  #     if ln.startswith("Disproven") or ln.startswith("Unreachable"):
  #       st = False
  #     if not st:
  #       continue
  #     ln_ = ln[:-1].split(",")
  #     state, req, idx, msg_set_idx, asets, amsgset_s, type_of_msg = ln_ 
  #     rset = tuple(sorted(asets.split("+")))
  #     if cur_type:
  #       # check if its already included
  #       type_of_msg = type_of_msg.replace("_assert", "")
  #       #aggregate[(state, req)]['upaths'][rset][f"only_one_msg_set_{type_of_msg}"] = True
  #       assert(0) # deprecated
  #     else:
  #       m_ = amsgset_s.split("+")
  #       if amsgset_s == "":
  #         m_ = []
  #       assert (not ((f"msg_set_{type_of_msg}") in aggregate[(state, req)]['upaths'][rset]))
  #       aggregate[(state, req)]['upaths'][rset][f"msg_set_{type_of_msg}"] = OrderedDict()
  #       for msg_type in m_:
  #         aggregate[(state, req)]['upaths'][rset][f"msg_set_{type_of_msg}"][msg_type] = OrderedDict()
  #         # aggregate[(state, req)]['upaths'][rset][f"msg_set_{type_of_msg}"][msg_type]['can_tfHome'] = False 
  #         # aggregate[(state, req)]['upaths'][rset][f"msg_set_{type_of_msg}"][msg_type]['aws_tfHome'] = False 
  #         aggregate[(state, req)]['upaths'][rset][f"msg_set_{type_of_msg}"][msg_type]['cnt'] = 1 ## TODO
  #         # if not dst_always_defined and type_of_msg == "out":
  #         #   aggregate[(state, req)]['upaths'][rset][f"msg_set_{type_of_msg}"][msg_type]['can_tfHome'] = None  
  #         #   aggregate[(state, req)]['upaths'][rset][f"msg_set_{type_of_msg}"][msg_type]['aws_tfHome'] = None

  #       #aggregate[(state, req)]['upaths'][rset][f"only_one_msg_set_{type_of_msg}"] = False
  # # for k, v in aggregate.items():
  # #   if k != 'global' and v['txn_init']:
  # #     for k_, v_ in v['upaths'].items():
  # #       if not (v_['only_one_msg_set_in'] and v_['only_one_msg_set_out']):
  # #         raise Exception("No Fixed Msg Set?!")


  # with open("build/s4_2_msg_type_and_order/_build/res.txt", "r") as f:
  #   fst, start = False, False
  #   t_ = ""
  #   for ln in f:
  #     if not fst: 
  #       fst = True
  #       continue
  #     if "Proven" in ln or "Reachable" in ln:
  #       start = True
  #       t_ = "assert" if "Proven" in ln else "cover" 
  #       continue
  #     ln_ = ln[:-1].split(",")
  #     state, req, idx, msg_set_idx, asets, amsgset_s, type_of_msg, midx, tar_msg_type = ln_ 
  #     rset = tuple(sorted(asets.split("+")))
  #     type_of_msg_ = "out" if "out" in type_of_msg else "in"
  #     if t_ == "assert":
  #       if type_of_msg == "out_assert_undefined":
  #         aggregate[(state, req)]['upaths'][rset][f"msg_set_{type_of_msg_}"][tar_msg_type]['aws_undefined'] = True 
  #       elif type_of_msg == "out_assert":
  #         aggregate[(state, req)]['upaths'][rset][f"msg_set_{type_of_msg_}"][tar_msg_type]['aws_tfHome'] = True 
  #       elif type_of_msg == "in_assert":
  #         aggregate[(state, req)]['upaths'][rset][f"msg_set_{type_of_msg_}"][tar_msg_type]['aws_tfHome'] = True 
  #       else:
  #         assert(0)
  #     else:
  #       aggregate[(state, req)]['upaths'][rset][f"msg_set_{type_of_msg_}"][tar_msg_type]['can_tfHome'] = True 

  # with open("build/s4_2_msg_type_and_order/_build/res_mapping.txt", "r") as f:
  #   start = False
  #   for ln in f:
  #     if "Proven" in ln:
  #       start = True
  #       continue
  #     elif "Disproven" in ln:
  #       break
  #     if not start:
  #       continue
  #     ln_ = ln[:-1].split(",")
  #     state,req,idx,msg_set_idx,asets,amsgset_s,type_of_msg,midx,state_msg_map_s = ln_
  #     print("==>", state, req, idx, state_msg_map_s, type_of_msg)
  #     rset = tuple(sorted(asets.split("+")))
  #     if not f'picl_rset_assoc_{type_of_msg}_msg' in aggregate[(state, req)]['upaths'][rset]:
  #       aggregate[(state, req)]['upaths'][rset][f'picl_rset_assoc_{type_of_msg}_msg'] = OrderedDict()
  #     tups = state_msg_map_s.split("+")
  #     if state_msg_map_s == "":
  #       tups = []
  #     for a_t in tups:
  #       k, v = a_t.split(":")
  #       if not v in aggregate[(state, req)]['upaths'][rset][f'picl_rset_assoc_{type_of_msg}_msg']:
  #         aggregate[(state, req)]['upaths'][rset][f'picl_rset_assoc_{type_of_msg}_msg'][v] = []
  #       aggregate[(state, req)]['upaths'][rset][f'picl_rset_assoc_{type_of_msg}_msg'][v].append(k)

  if debug:     
    pprint(aggregate)
  return aggregate


# what input request 
# At what {hstate} does HOME take in what {msgType}, and initiate or not initiate transaction 
# TODO: collect all possible upaths here
# TODO: then in s5.py we simply apply which upath is compatible
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
from code_gen.parse_rules import *

with open("build/s1_3_global_msg/_build/aggdict.pkl", "rb") as f:
  g_msg_dir = pickle.load(f)
dst_always_defined = g_msg_dir['dst_always_defined']
assert(not dst_always_defined)

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
def prepare_header(outff_h, rec_cond="", sending_book_keep_s="", var_ = {}):
  rec_s = f"if (!isundefined(cur_node) & cur_node = selh) then\n prevRecProcMsg := {{msg_var}}.{m_msg_type_field};\n {rec_cond};\n endif;\n" 

  additional_var = {"prevRecProcMsg": (msg_type_name, "undefine prevRecProcMsg;\n", "undefine prevRecProcMsg;\n")} 
  for k, v in var_.items():
    assert(not k in additional_var)
    additional_var[k] = v

  cfg = {"cur_node": True, "RECEIVING": rec_s, "g_msg": False, "home": True}

  if sending_book_keep_s != "":
    cfg['SENDING'] = sending_book_keep_s

  parse_murphi_model(coh_model_file, nodes_iter_types, outff_h, cfg, additional_var=additional_var)


transition = '''
invariant "{state}_to_{state_prime}"
  (!IsUndefined(prevHomeNode) & (prevHomeNode = {state})) ->
  !({m_home_cur}.{m_home_state_field} = {state_prime});
'''
def gen(): 
  stepname="home_s1_req_acc_state"
  dirname = f"build/{stepname}/out"
  os.makedirs(dirname, exist_ok = True)  
  for hstate in all_llc_states:
    for mtype in all_msg_types:
      if not (g_msg_dir[mtype][f'from_{m_proc_iter_type}_to_{m_home_iter_type}']):
        # home doesn't receives this message type 
        continue
      outff = f"{dirname}/{hstate}_{mtype}.m"
      outff_h = open(outff, "w")
      obs_s = f'''if (!isundefined(cur_node) & cur_node = selh) then
      prevMsg := {{msg_var}}.{m_msg_type_field};
      prevMsgSrc := {{msg_var}}.{m_msg_src_field};
      prevMsgDst := {{msg_var}}.{m_msg_dst_field};
       endif;'''
      obs_send_s = f"if (!isundefined(cur_node) & cur_node = selh) then\nprevSentMsg := {{msg_var}}.{m_msg_type_field};\nendif;\n"
      
      parse_murphi_model(coh_model_file, nodes_iter_types, outff_h, {"track_req": False, "prevState": False, "cur_node": True, "RECEIVING": obs_s, "SENDING": obs_send_s, "g_msg": True, "home": True})
      outff_h.write(h_accept_template.format(hstate=hstate, mtype=mtype, m_home_cur=m_home_cur, m_home_state_field=m_home_state_field))
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
      else:
        print("X impossible", hstate, mtype)
    
  with open(f"{dirname}/aggdict.pkl", "wb") as f: # 'wb' for write binary
    pickle.dump(aggregate, f)

  stepname="home_s2_req_acc_proc_state"
  dirname = f"build/{stepname}/out"
  os.makedirs(dirname, exist_ok = True)  

  # we see if {hstate} that accepts {mtype} can 
  # 1) serve without the need of transaction (i.e., transitioning to transient states) 
  #   a. send out message? 
  #       - how many message?
  #   b. transition to new state?
  # 2) serve w/ transaction
  #   a. set of nodes
  #   b. send messages? 
  #   c. receive messages?


  for k, v in aggregate.items():
    hstate, mtype = k
    # if not v['proc']:
    #   # empty upath
    #   continue

    # TODO: aux state (if len ['imm_picl'] > 1)

    # a. transition to new state or not
    for hstate_prime in [hstate] + home_transition[hstate]:
      outff = f"{dirname}/{hstate}_{mtype}_{hstate_prime}.m"
      outff_h = open(outff, "w")

      # obs_s = f'''if (!isundefined(cur_node) & cur_node = selh) then
      # prevMsg := {{msg_var}}.{m_msg_type_field};
      # prevMsgSrc := {{msg_var}}.{m_msg_src_field};
      # prevMsgDst := {{msg_var}}.{m_msg_dst_field};
      #  endif;'''
      # obs_send_s = f"if (!isundefined(cur_node) & cur_node = selh) then\nprevSentMsg := {{msg_var}}.{m_msg_type_field};\nendif;\n"
      
      # parse_murphi_model(coh_model_file, nodes_iter_types, outff_h, {"track_req": False, "prevState": False, "cur_node": True, "RECEIVING": obs_s, "SENDING": obs_send_s, "g_msg": True, "home": True})
      var_ = {}
      prepare_header(outff_h, rec_cond="", var_=var_)

      outff_h.write(home_inmsg_notxn_transition_template.format(hstate=hstate, mtype=mtype, m_home_cur=m_home_cur, m_msg_type_field=m_msg_type_field, hstate_prime=hstate_prime, m_home_state_field=m_home_state_field))
      outff_h.close()

    # value change? 
    outff = f"{dirname}/{hstate}_{mtype}_val.m"
    outff_h = open(outff, "w")

    var_ = {"prevHomeNodeVal": (m_val_type_name, "", f"prevHomeNodeVal := {m_home_cur}.{m_home_cl_field};\n")}
    prepare_header(outff_h, rec_cond="", var_=var_)

    outff_h.write(home_inmsg_notxn_val_template.format(hstate=hstate, mtype=mtype, m_msg_type_field=m_msg_type_field, m_home_cur=m_home_cur, m_home_cl_field=m_home_cl_field))
    outff_h.close()

    if main_mem_name is not None:
      # TODO
      outff = f"{dirname}/{hstate}_{mtype}_val_mainmem.m"
      outff_h = open(outff, "w")

      var_ = {"prevHomeNodeVal": (m_val_type_name, "", f"prevHomeNodeVal := {main_mem_name};\n")}
      prepare_header(outff_h, rec_cond="", var_=var_)

      outff_h.write(home_inmsg_notxn_val_template.format(hstate=hstate, mtype=mtype, m_msg_type_field=m_msg_type_field, m_home_cur=m_home_cur, m_home_cl_field=m_home_cl_field))
      outff_h.close()

    # sent messages to request source, owner, sharer list - requester, sharer list, or all cores  (line: 357)
    outff = f"{dirname}/{hstate}_{mtype}_msg_trace.m"
    outff_h = open(outff, "w")

    var_ = {"prevSentMsgSet": (f"array [{msg_type_name}] of boolean", f"for m: {msg_type_name} do\n prevSentMsgSet[m]:= false;\n endfor;\n", f"for m: {msg_type_name} do\n prevSentMsgSet[m]:= false;\n endfor;\n")}
    prepare_header(outff_h, rec_cond="", sending_book_keep_s=f"if (!isundefined(cur_node) & cur_node = selh) then\n prevSentMsgSet[{{msg_var}}.{m_msg_type_field}]:= true; endif;\n", var_=var_)
    outff_h.write(h_accept_template_trace.format(hstate=hstate, mtype=mtype))
    outff_h.close()

def gen_s1_2():

  with open(f"build/home_s0_transition/_build/home_transition.pkl", "rb") as f:
    home_transition = pickle.load(f)
  with open("build/home_s1_req_acc_state/_build/aggdict.pkl", "rb") as f:
    aggregate = pickle.load(f)
  dirname="build/home_s2_req_acc_proc_state/_build"

  stepname="home_s2_msg_out"
  n_dirname = f"build/{stepname}/out"
  os.makedirs(n_dirname, exist_ok = True)  

  for k, v in aggregate.items():
    hstate, mtype = k
    v['imm_picl'] = []
    # a. transition to new state or not
    for hstate_prime in [hstate] + home_transition[hstate]:
      resff = f"{dirname}/{hstate}_{mtype}_{hstate_prime}.txt"
      r = get_res_file(resff, f"{hstate}_accept_req_{mtype}")
      if r:
        v['imm_picl'].append(hstate_prime)
    aggregate[k] = v

  for k, v in aggregate.items():
    hstate, mtype = k
    v['transition_info'] = OrderedDict()
    print(v)
    assert(len(v['imm_picl']) == 1)
    for hstate_prime in v['imm_picl']: 
      cur = OrderedDict()

      resff = f"{dirname}/{hstate}_{mtype}_val.txt"
      r = get_res_file(resff, f"{hstate}_accept_req_{mtype}")
      print("===> here", resff)
      cur['val_change'] = r

      if main_mem_name is not None:
        # TODO
        resff = f"{dirname}/{hstate}_{mtype}_val_mainmem.txt"
        r = get_res_file(resff, f"{hstate}_accept_req_{mtype}")
        cur['mmem_change'] = r


      v['transition_info'][hstate_prime] = cur 

      if cur['val_change']:
        #  val change src to be inmsg.cl ? 
        outff = f"{n_dirname}/{hstate}_{mtype}_{hstate_prime}_val_inmsg.m"
        outff_h = open(outff, "w")
        var_ = {"prevHomeNodeVal": (m_val_type_name, "", f"prevHomeNodeVal := {m_home_cur}.{m_home_cl_field};\n"), "prevRecProcMsgVal": (m_val_type_name, "","")}
        prepare_header(outff_h, rec_cond=f"prevRecProcMsgVal := {{msg_var}}.{m_msg_cl_field};\n", sending_book_keep_s="", var_=var_)
        outff_h.write(dir_h_val_change_src_template.format(mtype=mtype, hstate=hstate, m_home_cur=m_home_cur,m_home_state_field=m_home_state_field,hstate_prime=hstate_prime, m_home_cl_field=m_home_cl_field, home_state_expr=f"{m_home_cur}.{m_home_state_field}", home_cl_expr=f"{m_home_cur}.{m_home_cl_field}" ))
        outff_h.close()

        # val change src to be Main memory?
        if main_mem_name is not None:
          outff = f"{n_dirname}/{hstate}_{mtype}_{hstate_prime}_val_mainmem.m"
          outff_h = open(outff, "w")
          var_ = {"prevHomeNodeVal": (m_val_type_name, "", f"prevHomeNodeVal := {m_home_cur}.{m_home_cl_field};\n"), "prevMainMem": (m_val_type_name, "",f"prevMainMem := {main_mem_name};\n")}
          prepare_header(outff_h, rec_cond="", sending_book_keep_s="", var_=var_)
          outff_h.write(dir_h_val_change_src_mem_template.format(mtype=mtype, hstate=hstate, m_home_cur=m_home_cur,m_home_state_field=m_home_state_field,hstate_prime=hstate_prime, m_home_cl_field=m_home_cl_field))
          outff_h.close()

      # find out msg set 

      resff = f"{dirname}/{hstate}_{mtype}_msg_trace.txt"
      _ = get_res_file(resff, None)
      ret = get_last_state(resff, "prevSentMsgSet", arr=True)
      print("-->", resff,  ret)
      sent_msg_ss = []
      for k, v_ in ret.items():
        sent_msg_ss.append(f"prevSentMsgSet[{k}] = {v_}")
      sent_msg_ss_acc = (" (" + " & ".join(sent_msg_ss) + ") \n")
      msg_type_sets = [k for k, val in ret.items() if val == "true"] 
      v['transition_info'][hstate_prime]['out_msg_sets'] = [msg_type_sets]

      outff = f"{n_dirname}/{hstate}_{mtype}_msg_assert.m"
      outff_h = open(outff, "w")
      var_ = {"prevSentMsgSet": (f"array [{msg_type_name}] of boolean", f"for m: {msg_type_name} do\n prevSentMsgSet[m]:= false;\n endfor;\n", f"for m: {msg_type_name} do\n prevSentMsgSet[m]:= false;\n endfor;\n")}
      prepare_header(outff_h, rec_cond="", sending_book_keep_s=f"if (!isundefined(cur_node) & cur_node = selh) then\n prevSentMsgSet[{{msg_var}}.{m_msg_type_field}]:= true; endif;\n", var_=var_)
      outff_h.write(h_accept_outmsg_assert.format(hstate=hstate, mtype=mtype, sent_msg_ss=sent_msg_ss_acc))
      outff_h.close()

      # get trace only at this step msg sending per hstate, mtype, hstate_prime
    
    aggregate[(hstate, mtype)] = v
  pprint(aggregate)
  with open(f"{n_dirname}/agg.pkl", "wb") as f:
    pickle.dump(aggregate, f)
def gen_s2():
  stepname="home_s3_msg_out_info"
  dirname = f"build/{stepname}/out"
  os.makedirs(dirname, exist_ok = True)  

  with open(f"build/home_s2_msg_out/out/agg.pkl", "rb") as f:
    aggregate = pickle.load(f)
  for k, v in aggregate.items():
    hstate, mtype = k
    for hstate_prime in v['imm_picl']: 
      cur = v['transition_info'][hstate_prime]
      if cur['val_change']:
        resff = f"build/home_s2_msg_out/_build/{hstate}_{mtype}_{hstate_prime}_val_inmsg.txt"
        r = get_res_file(resff, f"{hstate}_accept_req_{mtype}", assertion=True)
        print("-->", hstate, mtype, resff)
        src_ = "inmsg.cl" if r else ""
        if src_ == "" and main_mem_name is not None:
          resff = f"build/home_s2_msg_out/_build/{hstate}_{mtype}_{hstate_prime}_val_mainmem.txt"
          r = get_res_file(resff, f"{hstate}_accept_req_{mtype}", assertion=True)
          #if r and src_ != "":
          #  print("src to be inmsg and main mem????")
          src_ = "main_mem" if r else ""
        cur['val_change_src'] = src_
        if src_ == "":
          print("???? no src?")
      # get val_change src assertion result 
      resff = f"build/home_s2_msg_out/_build/{hstate}_{mtype}_msg_assert.txt"
      r = get_res_file(resff, f"ASSERT_{hstate}_accept_req_{mtype}", assertion=True)
      if not r:
        print("WARNiNG TODO")
        assert(0)

      # get msg set src/dst
      msg_type_sets = v['transition_info'][hstate_prime]['out_msg_sets'][0]
      for out_msg_mtype in msg_type_sets: 
        # dst of each out msg type 
        outff = f"{dirname}/{hstate}_{mtype}_{out_msg_mtype}_dst_aws_src.m"
        outff_h = open(outff, "w")
        var_ = {"sent": ("boolean", "sent := false;\n", "sent := false;\n"),
        "out_msg_dst": (m_proc_iter_type, "", "undefine out_msg_dst;\n"),
        "in_msg_src": (m_proc_iter_type, "", ""),
        }
        prepare_header(outff_h, rec_cond=f"in_msg_src := {{msg_var}}.{m_msg_src_field};\n", sending_book_keep_s=f"if (!isundefined(cur_node) & cur_node = selh & {{msg_var}}.{m_msg_type_field} = {out_msg_mtype}) then\n sent := true;\n endif;\n if (!isundefined(cur_node) & cur_node = selh & {{msg_var}}.{m_msg_type_field} = {out_msg_mtype}) then\n out_msg_dst := {{msg_var}}.{m_msg_dst_field};\n endif;\n", var_=var_)
        outff_h.write(h_accept_trans_outmsg_dst_src_template.format(hstate=hstate, mtype=mtype, m_home_cur=m_home_cur, m_home_cl_field=m_home_cl_field, m_home_state_field=m_home_state_field, is_src=""))
        outff_h.close()

        outff = f"{dirname}/{hstate}_{mtype}_{out_msg_mtype}_dst_aws_not_src.m"
        outff_h = open(outff, "w")
        var_ = {"sent": ("boolean", "sent := false;\n", "sent := false;\n"),
        "out_msg_dst": (m_proc_iter_type, "", "undefine out_msg_dst;\n"),
        "in_msg_src": (m_proc_iter_type, "", ""),
        }
        prepare_header(outff_h, rec_cond=f"in_msg_src := {{msg_var}}.{m_msg_src_field};\n", sending_book_keep_s=f"if (!isundefined(cur_node) & cur_node = selh & {{msg_var}}.{m_msg_type_field} = {out_msg_mtype}) then\n sent := true;\n endif;\n if (!isundefined(cur_node) & cur_node = selh & {{msg_var}}.{m_msg_type_field} = {out_msg_mtype}) then\n out_msg_dst := {{msg_var}}.{m_msg_dst_field};\n endif;\n", var_=var_)
        outff_h.write(h_accept_trans_outmsg_dst_src_template.format(hstate=hstate, mtype=mtype, m_home_cur=m_home_cur, m_home_cl_field=m_home_cl_field, m_home_state_field=m_home_state_field, is_src="!"))
        outff_h.close()

        # out msg's value : 664
        if not (out_msg_mtype in req_msg_types_with_data or out_msg_mtype in resp_msg_types_w_data):
          continue

        # assert msg val source to be the home's cl
        outff = f"{dirname}/{hstate}_{mtype}_{out_msg_mtype}.m"
        outff_h = open(outff, "w")

        var_ = {"sent": ("boolean", "sent := false;\n", "sent := false;\n"),
        "val_match": ("boolean", "val_match := false;\n", ""),
        "home_val": (m_val_type_name, "", f"home_val := {m_home_cur}.{m_home_cl_field};"),
        }
        prepare_header(outff_h, rec_cond="", sending_book_keep_s=f"if (!isundefined(cur_node) & cur_node = selh & {{msg_var}}.{m_msg_type_field} = {out_msg_mtype}) then\n sent := true;\n endif;\n if (!isundefined(cur_node) & cur_node = selh & {{msg_var}}.{m_msg_type_field} = {out_msg_mtype}) then\n val_match := ({{msg_var}}.{m_msg_cl_field} = home_val);\n endif;\n", var_=var_)
        outff_h.write(h_accept_trans_outmsg_src_template.format(hstate=hstate, mtype=mtype))
        outff_h.close()

         # val src'd from Main memory?
        if main_mem_name is not None:
          outff = f"{dirname}/{hstate}_{mtype}_{out_msg_mtype}_mainmem.m"
          outff_h = open(outff, "w")
          var_ = {"sent": ("boolean", "sent := false;\n", "sent := false;\n"),
          "val_match": ("boolean", "val_match := false;\n", ""),
          "home_val": (m_val_type_name, "", f"home_val := {main_mem_name};\n")}
          prepare_header(outff_h, rec_cond="", sending_book_keep_s=f"if (!isundefined(cur_node) & cur_node = selh & {{msg_var}}.{m_msg_type_field} = {out_msg_mtype}) then\n sent := true;\n endif;\n if (!isundefined(cur_node) & cur_node = selh & {{msg_var}}.{m_msg_type_field} = {out_msg_mtype}) then\n val_match := ({{msg_var}}.{m_msg_cl_field} = home_val);\n endif;\n", var_=var_)
          outff_h.write(h_accept_trans_outmsg_src_template.format(hstate=hstate, mtype=mtype))
          outff_h.close()
        

      v['transition_info'][hstate_prime] = cur 

  pprint(aggregate)
  with open(f"{dirname}/agg.pkl", "wb") as f:
    pickle.dump(aggregate, f)


def gen_s3():
  with open("build/home_s3_msg_out_info/out/agg.pkl", "rb") as f:
    aggregate = pickle.load(f)
  for k, v in aggregate.items():
    hstate, mtype = k
    for hstate_prime in v['imm_picl']: 
      v['transition_info'][hstate_prime]['out_msg_dst'] = OrderedDict()
      v['transition_info'][hstate_prime]['out_msg_val'] = OrderedDict()

      msg_type_sets = v['transition_info'][hstate_prime]['out_msg_sets'][0]
      for out_msg_mtype in msg_type_sets: 
        resff = f"build/home_s3_msg_out_info/_build/{hstate}_{mtype}_{out_msg_mtype}_dst_aws_src.txt"
        r_aws_src = get_res_file(resff, f"ASSERT_{hstate}_accept_req_{mtype}", assertion=True)

        resff = f"build/home_s3_msg_out_info/_build/{hstate}_{mtype}_{out_msg_mtype}_dst_aws_not_src.txt"
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

        if not (out_msg_mtype in req_msg_types_with_data or out_msg_mtype in resp_msg_types_w_data):
          continue

        resff = f"build/home_s3_msg_out_info/_build/{hstate}_{mtype}_{out_msg_mtype}.txt"
        r = get_res_file(resff, f"ASSERT_{hstate}_accept_req_{mtype}", assertion=True)
        if r:
          v['transition_info'][hstate_prime]['out_msg_val'][out_msg_mtype] = "cl_val"
          print("--> outmsg data val src cl val", hstate, mtype)
        if main_mem_name is not None:
          resff = f"build/home_s3_msg_out_info/_build/{hstate}_{mtype}_{out_msg_mtype}_mainmem.txt"
          r = get_res_file(resff, f"ASSERT_{hstate}_accept_req_{mtype}", assertion=True)
          if r:
            v['transition_info'][hstate_prime]['out_msg_val'][out_msg_mtype] = "cl_val"
            print("--> outmsg data mainmem val", hstate, mtype)
  aggregate[k] = v

  # with open("build/home_s3_msg_out_info/_build/agg.pkl", "wb") as f:
  #   pickle.dump(aggregate, f)

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
  with open("build/home_s3_msg_out_info/_build/agg.pkl", "wb") as f:
    pickle.dump((aggregate, g_all_paths), f)  
  pprint(g_all_paths)



################################################################################
  # collect 
    # b. send out message?
    # for out_mtype in all_msg_types: 
    #   outff = f"{dirname}/{hstate}_{mtype}_outmsg_{out_mtype}.m"
    #   outff_h = open(outff, "w")
    #   prepare_header(outff_h, design_file)
    #   outff_h.write(home_inmsg_notxn_send_msg_template.format(hstate=hstate, mtype=mtype, m_home_iter=m_home_iter,m_msg_type_field=m_msg_type_field, out_mtype=out_mtype))
    #   outff_h.close()

    #   outff = f"{dirname}/{hstate}_{mtype}_outmsg_{out_mtype}_to_src_chk.m"
    #   outff_h = open(outff, "w")
    #   prepare_header(outff_h, design_file)
    #   outff_h.write(home_inmsg_notxn_snedmsg_dst_template.format(hstate=hstate, mtype=mtype, m_home_iter=m_home_iter,m_msg_type_field=m_msg_type_field, out_mtype=out_mtype))
    #   outff_h.close()

    #   # outmsg value equal to 
    #   outff = f"{dirname}/{hstate}_{mtype}_outmsg_{out_mtype}_val_from_picl.m"
    #   outff_h = open(outff, "w")
    #   prepare_header(outff_h, design_file)
    #   outff_h.write(home_inmsg_notxn_snedmsg_val_template.format(hstate=hstate, mtype=mtype, m_home_iter=m_home_iter,m_msg_type_field=m_msg_type_field, out_mtype=out_mtype, m_msg_cl_field=m_msg_cl_field, m_proc_cl_field=m_proc_cl_field))
    #   outff_h.close()


    # c. send out message to the sender of the mtype that triggers or not? 
    # e. TODO: if out_mtype is dataresp, it is always the HomeNode.val? 


    # 2) picl value 

    # 2) msg sending?  
    # 3) msg sending's value?
    # 4) receiving? 

    ##################################################  
    # 1) serve without the need of transaction (i.e., transitioning to transient states) 
    #   a. send out message? 
    #       - how many message?
    #   b. transition to new state?
    # 2) serve w/ transaction
    #   a. set of nodes
    #   b. send messages? 
    #   c. receive messages?
    

def gen_s4():
  # if not dst_always_defined:
  #   tpath = "build/home_s1_1_req_acc_proc_state/_build/aggdict.pkl"
  # else:
  tpath = "build/home_s1_req_acc_state/_build/aggdict.pkl"
  with open(tpath, "rb") as f:
    aggregate = pickle.load(f)

  stepname="home_s2_req_acc_proc_state"
  dirname = f"build/{stepname}/_build"
  stepname_tmp ="home_s3_val_check"
  dirname_tmp = f"build/{stepname_tmp}/out"
  os.makedirs(dirname_tmp, exist_ok = True)  
  if set(all_llc_states) == set(all_llc_stable_states):
    # no need to explore transaction

    for k, v in aggregate['home'].items():
      hstate, mtype = k
      print ("###########")
      print (hstate, mtype)
      if not v['proc']:
        # empty upath
        continue
      v['init_txn'] = False
      # then 
    
      v['state_prime'] = None
      for h_prime in all_llc_stable_states:
        resff = f"{dirname}/{hstate}_{mtype}_no_txn_{h_prime}.txt"
        r = get_res_file(resff, f"{hstate}_accept_req_{mtype}")
        if r:
          assert(v['state_prime'] is None)
          print("-> transition", hstate, mtype, h_prime)
          v['state_prime'] = h_prime

      # b. send out message?
      # c. send out message to the sender of the mtype that triggers or not? 
      # e. TODO: if out_mtype is dataresp, it is always the HomeNode.val? 
      for out_mtype in all_msg_types: 
        resff = f"{dirname}/{hstate}_{mtype}_outmsg_{out_mtype}.txt"
        r = get_res_file(resff, f"{hstate}_accept_req_{mtype}")
        if not 'send_msg' in v:
          v['send_msg'] = OrderedDict()
        if r:
          print("-> out msg", hstate, mtype, out_mtype)
          v['send_msg'][out_mtype] = OrderedDict()
          v['send_msg'][out_mtype]['cnt'] = 1 # TODO

        resff = f"{dirname}/{hstate}_{mtype}_outmsg_{out_mtype}_to_src_chk.txt"
        r_src = get_res_file(resff, f"{hstate}_accept_req_{mtype}")
        if r and r_src:
          print("-> out msg can dst to src of ", mtype)
          v['send_msg'][out_mtype]['dst_to_inmsg_src'] = True
        resff = f"{dirname}/{hstate}_{mtype}_outmsg_{out_mtype}_val_from_picl.txt"
        r_val = get_res_file(resff, f"{hstate}_accept_req_{mtype}")
        if r and r_val:
          v['send_msg'][out_mtype]['val_eq_picl_val'] = True

      resff = f"{dirname}/{hstate}_{mtype}_val_change.txt"
      # TODO val.txt
      r = get_res_file(resff, f"{hstate}_accept_req_{mtype}")
      v['val_change'] = r
      if r:
        print("-> val change possible", hstate, mtype)

        outff = f"{dirname_tmp}/{hstate}_{mtype}_val_chk_inmsg.m"
        print(outff)
        outff_h = open(outff, "w")
        prepare_header(outff_h, design_file)
        outff_h.write(home_inmsg_notxn_val_eq_in_template.format(hstate=hstate, mtype=mtype, m_home_iter=m_home_iter,m_msg_type_field=m_msg_type_field))
        outff_h.close()

        if main_mem is not None:
          outff = f"{dirname_tmp}/{hstate}_{mtype}_val_chk_mainmem.m"
          print(outff)
          outff_h = open(outff, "w")
          prepare_header(outff_h, design_file)
          outff_h.write(home_inmsg_notxn_val_eq_mainmem_template.format(hstate=hstate, mtype=mtype, m_home_iter=m_home_iter,m_msg_type_field=m_msg_type_field, main_mem=main_mem))
          outff_h.close()


      aggregate['home'][k] = v
  else:
    # hprim_state to be non-stable-state
    # we get the 
    print("TODO")
    assert(0)

  with open(f"{dirname}/aggdict.pkl", "wb") as f: # 'wb' for write binary
    pickle.dump(aggregate, f)
  pprint(aggregate)
def gen_s5():
  tpath = "build/home_s2_req_acc_proc_state/_build/aggdict.pkl"
  with open(tpath, "rb") as f:
    aggregate = pickle.load(f)
  if set(all_llc_states) == set(all_llc_stable_states):
    for k, v in aggregate['home'].items():
      hstate, mtype = k
      if not v['proc']:
        # empty upath
        continue
      # v['init_txn'] is false AND the following 
      # 1. v['state_prime'] if not None gives the resulting h_prime
      # 2. v['send_msg'] if not empty key gives the sent message
      # 3. v['val_change'] gives whether value can be changed 
      # if not in val_change then it means no val_change
      if v['val_change']:
        # collect results 
        stepname_tmp ="home_s3_val_check"
        dirname_tmp = f"build/{stepname_tmp}/_build"
        resff = f"{dirname_tmp}/{hstate}_{mtype}_val_chk_inmsg.txt"
        proven_ = get_res_file(resff, f"ASSERT_{hstate}_accept_req_{mtype}", assertion=True)
        proven_m = None
        if main_mem is not None: 
          resff = f"{dirname_tmp}/{hstate}_{mtype}_val_chk_mainmem.txt"
          proven_m = get_res_file(resff, f"ASSERT_{hstate}_accept_req_{mtype}", assertion=True)

        print("--> ", hstate, mtype, "val change always to inmsg.val?", proven_)
        print("--> ", hstate, mtype, "val change always to mainmem?", proven_m)
        v['val_aws_to_inmsg'] = proven_
        v['val_aws_to_main_mem'] = proven_m
      aggregate['home'][k] = v

  with open(f"{dirname_tmp}/aggdict.pkl", "wb") as f: # 'wb' for write binary
    pickle.dump(aggregate, f)
  pprint(aggregate)

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

# {hstate} consistent with {msg}
# stepname="home_s1_1_req_acc_proc_state"
# dirname = f"build/{stepname}/out"
# os.makedirs(dirname, exist_ok = True)  
# # snooping: we see if {hstate} does take in {mtype}
# for k, v in aggregate.items():
#   # k is consistent 
#   hstate, mtype = k
#   outff = f"{dirname}/{hstate}_{mtype}_proc.m"
#   outff_h = open(outff, "w")
#   prepare_header(outff_h, design_file)
#   outff_h.write(home_inmsg_proc_template.format(hstate=hstate, mtype=mtype, m_home_iter=m_home_iter,m_msg_type_field=m_msg_type_field))
#   outff_h.close()


# with open(f"build/home_s1_req_acc_state/_build/aggdict.pkl", "rb") as f: # 'wb' for write binary
#   aggregate = pickle.load(f)
#if not dst_always_defined:
#  stepname="home_s1_1_req_acc_proc_state"
#  dirname = f"build/{stepname}/_build"
#  # snooping: we see if {hstate} always take in {mtype} (we will not have
#  # sometimes take in {mtype} versus not because its a finite state machine)
#  for k, v in aggregate['home'].items():
#    # k is consistent 
#    hstate, mtype = k
#    resff = f"{dirname}/{hstate}_{mtype}_proc.txt"
#    hstate_proc = get_res_file(resff, f"{hstate}_accept_req_{mtype}")
#    print("-->", hstate, mtype, "process?", hstate_proc)
#    v['proc'] = hstate_proc
#    aggregate['home'][k] = v 
#  with open(f"{dirname}/aggdict.pkl", "wb") as f: # 'wb' for write binary
#    pickle.dump(aggregate, f)

#if not dst_always_defined:
#  tpath = "build/home_s1_1_req_acc_proc_state/_build/aggdict.pkl"
#else:
#  tpath = "build/home_s1_req_acc_state/_build/aggdict.pkl"
#with open(tpath, "rb") as f:
#    aggregate = pickle.load(f)

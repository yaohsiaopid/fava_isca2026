import fire
import pickle
import subprocess
import os 
import sys
import re
import argparse
from pprint import pprint
from collections import OrderedDict
from util import *

sys.path.append("src")
from code_gen.parse_rules import *
from gconst import *

with open(f"{build_dir}/s1_3_global_msg/_build/aggdict.pkl", "rb") as f:
  g_msg_dir = pickle.load(f)
dst_always_defined = g_msg_dir['dst_always_defined']

# directory 
c_accept_template= '''
invariant "{state_}_rec_{mtype}"
  -- can {state_} ever receives {mtype} message 
  (!IsUndefined(prevProcs) & (prevProcs = {state_})) ->
  (isundefined(prevMsg) | prevMsg != {mtype});
'''
c_accept_assert_outmsg_template= '''
invariant "{state_}_rec_{mtype}"
  -- can {state_} ever receives {mtype} message 
  (!IsUndefined(prevProcs) & (prevProcs = {state_}) & 
  !isundefined(prevMsg) & prevMsg = {mtype}) ->
  {sent_msg_ss};
'''
# for snooping
c_accept_proc_template= '''
invariant "{state_}_rec_{mtype}"
  -- can {state_} ever receives and proc {mtype} message 
  (!IsUndefined(prevProcs) & prevProcs = {state_} &
    !isundefined(prevMsg) & prevMsg = {mtype}) ->
    -- process or dst defined
    !((!isundefined(prevProcs) & prevProcs != {m_proc_selc}.{m_proc_state_field}) |
    (!isundefined(prevMsgDst) & prevMsgDst = selc) |
    !isundefined(prevSentMsg));
'''
c_accept_proc_assert_outmsg_template= '''
invariant "{state_}_rec_{mtype}"
  -- can {state_} ever receives and proc {mtype} message 
  (!IsUndefined(prevProcs) & prevProcs = {state_} &
    !isundefined(prevMsg) & prevMsg = {mtype}) ->
    {sent_msg_ss};
'''
# for snooping
c_accept_proc_inmsg_src_template= '''
invariant "{state_}_rec_{mtype}"
  -- can {state_} ever receives and proc {mtype} message 
  (!IsUndefined(prevProcs) & prevProcs = {state_} &
    !isundefined(prevMsg) & prevMsg = {mtype} &
    ((!isundefined(prevProcs) & prevProcs != {m_proc_selc}.{m_proc_state_field}) |
    (!isundefined(prevMsgDst) & prevMsgDst = selc) |
    !isundefined(prevSentMsg))
     ) ->
    -- process or dst defined
    !ismember(prevMsgSrc, {tar_type});
    ;
'''
# directory
dir_pp_prime_template = '''
invariant "{state_}_rec_{mtype}"
  -- can {state_} ever receives and proc {mtype} message 
  (!IsUndefined(prevProcs) & prevProcs = {state_} & !isundefined(prevMsg) & prevMsg = {mtype}) -> 
  !({m_proc_selc}.{m_proc_state_field} = {state_prime});
'''
pp_prime_template = '''
invariant "{state_}_rec_{mtype}"
  -- can {state_} ever receives and proc {mtype} message 
  (!IsUndefined(prevProcs) & prevProcs = {state_} &
    !isundefined(prevMsg) & prevMsg = {mtype} & 
    -- process or dst defined
    ((!isundefined(prevProcs) & prevProcs != {m_proc_selc}.{m_proc_state_field}) |
    (!isundefined(prevMsgDst) & prevMsgDst = selc) |
    !isundefined(prevSentMsg))) ->
    !({m_proc_selc}.{m_proc_state_field} = {state_prime});
'''
dir_postfix_outmsg_template = '''
invariant "{state_}_rec_{mtype}"
  -- can {state_} ever receives and proc {mtype} message and then send out 
  (!IsUndefined(prevProcs) & prevProcs = {state_} & !isundefined(prevMsg) & prevMsg = {mtype}) -> 
  (isundefined(prevSentMsg) | prevSentMsg != {outmsg_type});
'''
dir_postfix_no_outmsg_template = '''
invariant "{state_}_rec_{mtype}"
  -- can {state_} ever receives and proc {mtype} message and then send out 
  (!IsUndefined(prevProcs) & prevProcs = {state_} & !isundefined(prevMsg) & prevMsg = {mtype}) -> 
  !(isundefined(prevSentMsg));
'''
# snooping
postfix_outmsg_template = '''
invariant "{state_}_rec_{mtype}"
  -- can {state_} ever receives and proc {mtype} message and then send out 
  (!IsUndefined(prevProcs) & prevProcs = {state_} &
    !isundefined(prevMsg) & prevMsg = {mtype} & 
    -- process or dst defined
    ((!isundefined(prevProcs) & prevProcs != {m_proc_selc}.{m_proc_state_field}) |
    (!isundefined(prevMsgDst) & prevMsgDst = selc) |
    !isundefined(prevSentMsg))) ->
  (isundefined(prevSentMsg) | prevSentMsg != {outmsg_type});
'''
postfix_no_outmsg_template = '''
invariant "{state_}_rec_{mtype}"
  -- can {state_} ever receives and proc {mtype} message and then send out 
  (!IsUndefined(prevProcs) & prevProcs = {state_} &
    !isundefined(prevMsg) & prevMsg = {mtype} & 
    -- process or dst defined
    ((!isundefined(prevProcs) & prevProcs != {m_proc_selc}.{m_proc_state_field}) |
    (!isundefined(prevMsgDst) & prevMsgDst = selc) |
    !isundefined(prevSentMsg))) ->
  !isundefined(prevSentMsg);
'''
dir_postfix_outmsg_val_template = '''
invariant "ASSERT_{state_}_rec_{mtype}"
  -- can {state_} ever receives and proc {mtype} message and then send out 
  (!IsUndefined(prevProcs) & prevProcs = {state_} & !isundefined(prevMsg) & prevMsg = {mtype}) -> 
  (!isundefined(prevSentMsgVal) & prevSentMsgVal = prevStateVal);
'''
postfix_outmsg_val_template = '''
invariant "ASSERT_{state_}_rec_{mtype}"
  -- can {state_} ever receives and proc {mtype} message and then send out 
  (!IsUndefined(prevProcs) & prevProcs = {state_} &
    !isundefined(prevMsg) & prevMsg = {mtype} & 
    -- process or dst defined
    ((!isundefined(prevProcs) & prevProcs != {m_proc_selc}.{m_proc_state_field}) |
    (!isundefined(prevMsgDst) & prevMsgDst = selc) |
    !isundefined(prevSentMsg))) -> 
  (!isundefined(prevSentMsgVal) & prevSentMsgVal = prevStateVal);
'''

val_transition_template = '''
invariant "ASSERT_{state}_to_{state_prime}"
((!isundefined(prevProcs) & prevProcs = {state}) &
({m_proc_selc}.{m_proc_state_field} = {state_prime})) ->
(prevStateVal = {m_proc_selc}.{m_proc_cl_field});
'''

def gen(): 
  stepname="core_s1_req_acc_state"
  dirname = f"{build_dir}/{stepname}/out"
  os.makedirs(dirname, exist_ok = True)  
  for state_ in all_cc_stable_states:
    for mtype in all_msg_types:
      if mtype in resp_msg_types:
        continue 
      outff = f"{dirname}/{state_}_{mtype}.m"
      outff_h = open(outff, "w")

      # dec = False
      # if dst_always_defined:
      #   with open("/Users/yaohsiao/work/coh_syn_dev/murphi/protocols/fv/msi_fv_envs/msi.fvt.s1_msg_cnt_txn.m", "r") as f:
      #     for ln in f:
      #       if f"#RECEIVING" in ln:
      #         msg_var = ln[:-1].split(",")[-1]
      #         outff_h.write(f"if (!isundefined(cur_node) & cur_node = selc) then\n prevMsg := {msg_var}.{m_msg_type_field};\n endif;\n")
      #       elif "BLOCK_WITHIN_BOOK_KEEP" in ln:
      #         outff_h.write("undefine prevMsg;\n") # for checking 
      #       elif "endstartstate" in ln:
      #         outff_h.write("undefine prevMsg;\n")
      #         outff_h.write(ln)
      #       else:
      #         outff_h.write(ln)
      #       if "var" == ln[:3] and not dec:
      #         dec = True
      #         outff_h.write(f"prevMsg: {msg_type_name};\n")
      #   outff_h.write(c_accept_template.format(state_=state_, mtype=mtype, m_proc_state_field=m_proc_state_field, m_msg_type_field=m_msg_type_field))
      # else:
      #   prepare_header(outff_h, design_file)
      if dst_always_defined:
        rec_ss = f"if (!isundefined(cur_node) & cur_node = selc) then\n prevMsg := {{msg_var}}.{m_msg_type_field};\n endif;\n"
        cfg = {"track_req": False, "prevState": True, "cur_node": True, "RECEIVING": rec_ss, "g_msg": True}
        parse_murphi_model(coh_model_file, nodes_iter_types, outff_h, cfg, additional_var={})

        outff_h.write(c_accept_template.format(state_=state_, mtype=mtype, m_proc_state_field=m_proc_state_field, m_msg_type_field=m_msg_type_field))
      else:
        rec_ss = f"if (!isundefined(cur_node) & cur_node = selc) then\n prevMsg := {{msg_var}}.{m_msg_type_field};\n prevMsgDst := {{msg_var}}.{m_msg_dst_field};\n endif;\n"
        send_ss = f"if (!isundefined(cur_node) & cur_node = selc) then prevSentMsg := {{msg_var}}.{m_msg_type_field}; endif;\n"
        cfg = {"track_req": False, "prevState": True, "cur_node": True, "RECEIVING": rec_ss, "SENDING": send_ss, "g_msg": True}
        parse_murphi_model(coh_model_file, nodes_iter_types, outff_h, cfg, additional_var={})
        outff_h.write(c_accept_proc_template.format(state_=state_, mtype=mtype, m_proc_state_field=m_proc_state_field,  m_proc_selc=m_proc_selc))
      outff_h.close()

def gen_s2():
  with open(f"{build_dir}/s1_2_transition/_build/transition.pkl", "rb") as f:
    state_transitions = pickle.load(f)
  dirname = f"{build_dir}/core_s2_req_acc_state_prime/out"
  os.makedirs(dirname, exist_ok = True)  
  for state_ in all_cc_stable_states:
    for mtype in all_msg_types:
      if mtype in resp_msg_types:
        continue 
      resff = f"{build_dir}/core_s1_req_acc_state/_build/{state_}_{mtype}.txt"
      state_inmsg_possible = get_res_file(resff, f"{state_}_rec_{mtype}")
      print("-->", state_, mtype, state_inmsg_possible)
      if state_inmsg_possible:
        # mtype src
        todo = []
        for src, src_nm in zip([m_proc_iter_type, m_home_iter_type], ["core", "home"]):
          k = f"from_{src}_to_{m_proc_iter_type}"
          if g_msg_dir[mtype][k]:
            todo.append((src, src_nm))
        if len(todo) > 1:
          for src, src_nm in zip([m_proc_iter_type, m_home_iter_type], ["core", "home"]):
            outff = f"{dirname}/{state}_{mtype}_{src_nm}.m"
            outff_h = open(outff, "w")
            # see if the sender is 
            if dst_always_defined:
              # at SENDING check 
              assert(0)
            else:
              rec_ss = f"if (!isundefined(cur_node) & cur_node = selc) then\n prevMsg := {{msg_var}}.{m_msg_type_field};\n prevMsgDst := {{msg_var}}.{m_msg_dst_field};\n prevMsgSrc := prevMsg.{m_msg_src_field}; \nendif;\n"
              send_ss = f"if (!isundefined(cur_node) & cur_node = selc) then prevSentMsg := {{msg_var}}.{m_msg_type_field}; endif;\n"
              cfg = {"track_req": False, "prevState": True, "cur_node": True, "RECEIVING": rec_ss, "SENDING": send_ss, "g_msg": True}
              parse_murphi_model(coh_model_file, nodes_iter_types, outff_h, cfg, additional_var={})
              outff_h.write(c_accept_proc_inmsg_src_template.format(state_=state_, mtype=mtype, m_proc_state_field=m_proc_state_field,  m_proc_selc=m_proc_selc, tar_type=src))
              # at RECEIVING check
              assert(0)
            outff_h.close()
        for state_prime in all_cc_stable_states:
          if (state_prime == state_) or (not state_prime in state_transitions[state_]):
            continue
          outff = f"{dirname}/{state_}_{mtype}_{state_prime}.m"
          outff_h = open(outff, "w")


          # dec = False
          if dst_always_defined:

            rec_ss = f"if (!isundefined(cur_node) & cur_node = selc) then\n prevMsg := {{msg_var}}.{m_msg_type_field};\n endif;\n"
            cfg = {"track_req": False, "prevState": True, "cur_node": True, "RECEIVING": rec_ss, "g_msg": True}
            parse_murphi_model(coh_model_file, nodes_iter_types, outff_h, cfg, additional_var={})

            # with open("/Users/yaohsiao/work/coh_syn_dev/murphi/protocols/fv/msi_fv_envs/msi.fvt.s1_msg_cnt_txn.m", "r") as f:
            #   for ln in f:
            #     if f"#RECEIVING" in ln:
            #       msg_var = ln[:-1].split(",")[-1]
            #       outff_h.write(f"if (!isundefined(cur_node) & cur_node = selc) then\n prevMsg := {msg_var}.{m_msg_type_field};\n endif;\n")
            #     elif "BLOCK_WITHIN_BOOK_KEEP" in ln:
            #       outff_h.write("undefine prevMsg;\n") # for checking 
            #     elif "endstartstate" in ln:
            #       outff_h.write("undefine prevMsg;\n")
            #       outff_h.write(ln)
            #     else:
            #       outff_h.write(ln)
            #     if "var" == ln[:3] and not dec:
            #       dec = True
            #       outff_h.write(f"prevMsg: {msg_type_name};\n")
            # #outff_h.write(c_accept_template.format(state_=state_, mtype=mtype, m_proc_state_field=m_proc_state_field, m_msg_type_field=m_msg_type_field))
            outff_h.write(dir_pp_prime_template.format(state_=state_, mtype=mtype, m_proc_state_field=m_proc_state_field, m_msg_type_field=m_msg_type_field, state_prime=state_prime, m_proc_selc=m_proc_selc))
          else:
            rec_ss = f"if (!isundefined(cur_node) & cur_node = selc) then\n prevMsg := {{msg_var}}.{m_msg_type_field};\n prevMsgDst := {{msg_var}}.{m_msg_dst_field};\n endif;\n"
            send_ss = f"if (!isundefined(cur_node) & cur_node = selc) then prevSentMsg := {{msg_var}}.{m_msg_type_field}; endif;\n"
            cfg = {"track_req": False, "prevState": True, "cur_node": True, "RECEIVING": rec_ss, "SENDING": send_ss, "g_msg": True}
            parse_murphi_model(coh_model_file, nodes_iter_types, outff_h, cfg, additional_var={})

            outff_h.write(pp_prime_template.format(state_=state_, mtype=mtype, m_proc_state_field=m_proc_state_field, m_msg_type_field=m_msg_type_field, state_prime=state_prime, m_proc_selc=m_proc_selc))

          outff_h.close()

        # got the trace toward getting the out msg set 
        # TODO: we guess here that there's only one possible state_prime
        outff = f"{dirname}/{state_}_{mtype}_trace.m"
        outff_h = open(outff, "w")
        
        if dst_always_defined:
          rec_ss = f"if (!isundefined(cur_node) & cur_node = selc) then\n prevMsg := {{msg_var}}.{m_msg_type_field};\n endif;\n"
          cfg = {"track_req": False, "prevState": True, "cur_node": True, "RECEIVING": rec_ss, "g_msg": True}
          var_ = {"prevSentMsgSet": (f"array [{msg_type_name}] of boolean", f"for m: {msg_type_name} do\n prevSentMsgSet[m]:= false;\n endfor;\n", f"for m: {msg_type_name} do\n prevSentMsgSet[m]:= false;\n endfor;\n")}
          cfg['SENDING'] = f"if (!isundefined(cur_node) & cur_node = selc) then\n prevSentMsgSet[{{msg_var}}.{m_msg_type_field}]:= true; endif;\n"
          parse_murphi_model(coh_model_file, nodes_iter_types, outff_h, cfg, additional_var=var_)
          outff_h.write(c_accept_template.format(state_=state_, mtype=mtype, m_proc_state_field=m_proc_state_field, m_msg_type_field=m_msg_type_field))

        else:
          rec_ss = f"if (!isundefined(cur_node) & cur_node = selc) then\n prevMsg := {{msg_var}}.{m_msg_type_field};\n prevMsgDst := {{msg_var}}.{m_msg_dst_field};\n endif;\n"
          send_ss = f"if (!isundefined(cur_node) & cur_node = selc) then prevSentMsgSet[{{msg_var}}.{m_msg_type_field}]:= true; endif;\n"
          cfg = {"track_req": False, "prevState": True, "cur_node": True, "RECEIVING": rec_ss, "SENDING": send_ss, "g_msg": True}
          var_ = {"prevSentMsgSet": (f"array [{msg_type_name}] of boolean", f"for m: {msg_type_name} do\n prevSentMsgSet[m]:= false;\n endfor;\n", f"for m: {msg_type_name} do\n prevSentMsgSet[m]:= false;\n endfor;\n")}
          parse_murphi_model(coh_model_file, nodes_iter_types, outff_h, cfg, additional_var=var_)
          outff_h.write(c_accept_proc_template.format(state_=state_, mtype=mtype, m_proc_state_field=m_proc_state_field,  m_proc_selc=m_proc_selc))
        outff_h.close()

def gen_s3():
  with open(f"{build_dir}/s1_3_global_msg/_build/aggdict.pkl", "rb") as f:
    g_msg_dir = pickle.load(f)
  # collect previous results 
  with open(f"{build_dir}/s1_2_transition/_build/transition.pkl", "rb") as f:
    state_transitions = pickle.load(f)
  
  transition_msg_map = None
  transition_map_file = f"{build_dir}/s1_msg_per_transition_cl/_build/res.pkl"
  if os.path.exists(transition_map_file):
    with open(transition_map_file, "rb") as f:
      transition_msg_map = pickle.load(f)

  dirname = f"{build_dir}/core_s3_req_send/out"
  os.makedirs(dirname, exist_ok = True)  
  aggregate = OrderedDict() 
  for state_ in all_cc_stable_states:
    for mtype in all_msg_types:
      if mtype in resp_msg_types:
        continue 
      resff = f"{build_dir}/core_s1_req_acc_state/_build/{state_}_{mtype}.txt"
      state_inmsg_possible = get_res_file(resff, f"{state_}_rec_{mtype}")
      print("-->", state_, mtype, state_inmsg_possible)
      if state_inmsg_possible:
        aggregate[(state_, mtype)] = OrderedDict()
        todo = []
        for src, src_nm in zip([m_proc_iter_type, m_home_iter_type], ["core", "home"]):
          k = f"from_{src}_to_{m_proc_iter_type}"
          if g_msg_dir[mtype][k]:
            todo.append((src, src_nm))
        if len(todo) > 1:
          for src, src_nm in zip([m_proc_iter_type, m_home_iter_type], ["core", "home"]):
            resff = f"{build_dir}/core_s2_req_acc_state_prime/_build/{state}_{mtype}_{src_nm}.txt"
            _ = get_res_file(resff, None)
        else:
          print("--> todo", todo)
          aggregate[(state_, mtype)]['msg_src'] = todo[0][1]

        for state_prime in all_cc_stable_states:
          if (state_prime == state_) or (not state_prime in state_transitions[state_]):
            continue
          resff = f"{build_dir}/core_s2_req_acc_state_prime/_build/{state_}_{mtype}_{state_prime}.txt"
          res = get_res_file(resff, f"{state_}_rec_{mtype}")
          if res: 
            aggregate[(state_, mtype)]['state_prime'] = state_prime
            print("\t-->", state_, mtype, state_prime)

            outff = f"{dirname}/{state_}_{mtype}_{state_prime}_val.m"
            outff_h = open(outff, "w")
            cfg = {
              "track_req": False,
              "prevState": True,
              "prevStateVal": True,
              "cur_node": True,
            }
            parse_murphi_model(coh_model_file, nodes_iter_types, outff_h, cfg, additional_var={})
            outff_h.write(val_transition_template.format(
              state=state_,
              state_prime=state_prime,
              m_proc_selc=m_proc_selc,
              m_proc_state_field=m_proc_state_field,
              m_proc_cl_field=m_proc_cl_field,
            ))
            outff_h.close()

        resff = f"{build_dir}/core_s2_req_acc_state_prime/_build/{state_}_{mtype}_trace.txt"
        _ = get_res_file(resff, None)
        ret = get_last_state(resff, "prevSentMsgSet", arr=True)

        aggregate[(state_, mtype)]['outmsg_set'] = ret
        print("--> prevmsgsent", ret)
        sent_msg_ss = []
        for k, v_ in ret.items():
          sent_msg_ss.append(f"prevSentMsgSet[{k}] = {v_}")
        sent_msg_ss_acc = (" (" + " & ".join(sent_msg_ss) + ") \n")
        
        outff = f"{dirname}/{state_}_{mtype}_trace_assert.m"
        outff_h = open(outff, "w")
        
        if dst_always_defined:
          rec_ss = f"if (!isundefined(cur_node) & cur_node = selc) then\n prevMsg := {{msg_var}}.{m_msg_type_field};\n endif;\n"
          cfg = {"track_req": False, "prevState": True, "cur_node": True, "RECEIVING": rec_ss, "g_msg": True}
          var_ = {"prevSentMsgSet": (f"array [{msg_type_name}] of boolean", f"for m: {msg_type_name} do\n prevSentMsgSet[m]:= false;\n endfor;\n", f"for m: {msg_type_name} do\n prevSentMsgSet[m]:= false;\n endfor;\n")}
          cfg['SENDING'] = f"if (!isundefined(cur_node) & cur_node = selc) then\n prevSentMsgSet[{{msg_var}}.{m_msg_type_field}]:= true; endif;\n"
          parse_murphi_model(coh_model_file, nodes_iter_types, outff_h, cfg, additional_var=var_)
          outff_h.write(c_accept_assert_outmsg_template.format(state_=state_, mtype=mtype, m_proc_state_field=m_proc_state_field, m_msg_type_field=m_msg_type_field, sent_msg_ss=sent_msg_ss_acc))

        else:
          rec_ss = f"if (!isundefined(cur_node) & cur_node = selc) then\n prevMsg := {{msg_var}}.{m_msg_type_field};\n prevMsgDst := {{msg_var}}.{m_msg_dst_field};\n endif;\n"
          send_ss = f"if (!isundefined(cur_node) & cur_node = selc) then prevSentMsgSet[{{msg_var}}.{m_msg_type_field}]:= true; endif;\n"
          cfg = {"track_req": False, "prevState": True, "cur_node": True, "RECEIVING": rec_ss, "SENDING": send_ss, "g_msg": True}
          var_ = {"prevSentMsgSet": (f"array [{msg_type_name}] of boolean", f"for m: {msg_type_name} do\n prevSentMsgSet[m]:= false;\n endfor;\n", f"for m: {msg_type_name} do\n prevSentMsgSet[m]:= false;\n endfor;\n")}
          parse_murphi_model(coh_model_file, nodes_iter_types, outff_h, cfg, additional_var=var_)
          outff_h.write(c_accept_proc_assert_outmsg_template.format(state_=state_, mtype=mtype, m_proc_state_field=m_proc_state_field,  m_proc_selc=m_proc_selc, sent_msg_ss=sent_msg_ss_acc))
        outff_h.close()

        print(state_, mtype)
        todo = []
        for k, v in ret.items():
          if v == "true":
            if g_msg_dir[k][f'from_{m_proc_iter_type}_to_{m_proc_iter_type}'] and g_msg_dir[k][f'from_{m_proc_iter_type}_to_{m_home_iter_type}']:
              todo.append(k)
        if len(todo):
          # we go on to see todo's dst 
          print("todo: dst of ", todo)
          print("output file that collect the dst ")
          assert(0)
        else:
          map_ = {}
          for k, v in ret.items():
            if v == "true":
              if g_msg_dir[k][f'from_{m_proc_iter_type}_to_{m_proc_iter_type}']:
                map_[k] = "core" 
              else:
                map_[k] = "home" 
          aggregate[(state_, mtype)]['outmsg_set_dst'] = map_



  with open(f"{dirname}/agg.pkl", "wb") as f:
    pickle.dump(aggregate, f)

  
  # # send out msg type  and value 
  # for k, v in aggregate.items():
  #   state_, mtype = k
  #   for outmsg_type in all_msg_types: 
  #     if outmsg_type in req_msg_types:
  #       continue
  #     if not (g_msg_dir[outmsg_type][f'from_{m_proc_iter_type}_to_{m_proc_iter_type}'] or g_msg_dir[outmsg_type][f'from_{m_proc_iter_type}_to_{m_home_iter_type}']):
  #       continue

  #     outff = f"{dirname}/{state_}_{mtype}_{outmsg_type}.m"
  #     outff_h = open(outff, "w")
  #     dec = False
  #     if dst_always_defined:

  #       rec_ss = f"if (!isundefined(cur_node) & cur_node = selc) then\n prevMsg := {{msg_var}}.{m_msg_type_field};\n endif;\n"
  #       send_ss = f"if (!isundefined(cur_node) & cur_node = selc) then\n prevSentMsg := {{msg_var}}.{m_msg_type_field};\n endif;\n"
  #       cfg = {"track_req": False, "prevState": True, "cur_node": True, "RECEIVING": rec_ss, "SENDING": send_ss, "g_msg": True}
  #       parse_murphi_model(coh_model_file, nodes_iter_types, outff_h, cfg, additional_var={})

  #       outff_h.write(dir_postfix_outmsg_template.format(state_=state_, mtype=mtype, m_proc_state_field=m_proc_state_field, m_msg_type_field=m_msg_type_field, state_prime=state_prime, m_proc_selc=m_proc_selc, outmsg_type=outmsg_type))

  #       # with open("/Users/yaohsiao/work/coh_syn_dev/murphi/protocols/fv/msi_fv_envs/msi.fvt.s1_msg_cnt_txn.m", "r") as f:
  #       #   for ln in f:
  #       #     if f"#RECEIVING" in ln:
  #       #       msg_var = ln[:-1].split(",")[-1]
  #       #       outff_h.write(f"if (!isundefined(cur_node) & cur_node = selc) then\n prevMsg := {msg_var}.{m_msg_type_field};\n endif;\n")
  #       #     elif f"#SENDING" in ln:
  #       #       msg_var = ln[:-1].split(",")[-1]
  #       #       outff_h.write(f"if (!isundefined(cur_node) & cur_node = selc) then\n prevSentMsg := {msg_var}.{m_msg_type_field};\n endif;\n")
  #       #     elif "BLOCK_WITHIN_BOOK_KEEP" in ln:
  #       #       outff_h.write("undefine prevMsg;\n") # for checking 
  #       #       outff_h.write("undefine prevSentMsg;\n") # for checking 
  #       #     elif "endstartstate" in ln:
  #       #       outff_h.write("undefine prevMsg;\n")
  #       #       outff_h.write("undefine prevSentMsg;\n") # for checking 
  #       #       outff_h.write(ln)
  #       #     else:
  #       #       outff_h.write(ln)
  #       #     if "var" == ln[:3] and not dec:
  #       #       dec = True
  #       #       outff_h.write(f"prevMsg: {msg_type_name};\n")
  #       #       outff_h.write(f"prevSentMsg: {msg_type_name};\n")
  #       # outff_h.write(dir_postfix_outmsg_template.format(state_=state_, mtype=mtype, m_proc_state_field=m_proc_state_field, m_msg_type_field=m_msg_type_field, state_prime=state_prime, m_proc_selc=m_proc_selc, outmsg_type=outmsg_type))
  #     else:
  #       rec_ss = f"if (!isundefined(cur_node) & cur_node = selc) then\n prevMsg := {{msg_var}}.{m_msg_type_field};\n prevMsgDst := {{msg_var}}.{m_msg_dst_field};\n endif;\n"
  #       send_ss = f"if (!isundefined(cur_node) & cur_node = selc) then prevSentMsg := {{msg_var}}.{m_msg_type_field}; endif;\n"
  #       cfg = {"track_req": False, "prevState": True, "cur_node": True, "RECEIVING": rec_ss, "SENDING": send_ss, "g_msg": True}
  #       parse_murphi_model(coh_model_file, nodes_iter_types, outff_h, cfg, additional_var={})
  #       outff_h.write(postfix_outmsg_template.format(state_=state_, mtype=mtype, m_proc_state_field=m_proc_state_field, m_msg_type_field=m_msg_type_field, state_prime=state_prime, m_proc_selc=m_proc_selc, outmsg_type=outmsg_type))
  #     outff_h.close()
  #       # assert(0)
  #       #pass 
  #       #prepare_header(outff_h, design_file)
  #       #outff_h.write(pp_prime_template.format(state_=state_, mtype=mtype, m_proc_state_field=m_proc_state_field, m_msg_type_field=m_msg_type_field, state_prime=state_prime))
  #       # if state_inmsg_possible:
  #       #   for state_prime in all_cc_stable_states:
  #       #     if state_prime == state_:
  #       #       continue
  #       #     resff = f"{dirname}/{state_}_{mtype}_{state_prime}.txt"
  #       #     transition = get_res_file(resff, f"{state_}_rec_{mtype}")
  #       #     if transition:
  #       #       print("\t --> transition possible", state_prime)

  #   outff = f"{dirname}/{state_}_{mtype}_no_outmsg.m"
  #   outff_h = open(outff, "w")
  #   dec = False
  #   if dst_always_defined:

  #     rec_ss = f"if (!isundefined(cur_node) & cur_node = selc) then\n prevMsg := {{msg_var}}.{m_msg_type_field};\n endif;\n"
  #     send_ss = f"if (!isundefined(cur_node) & cur_node = selc) then\n prevSentMsg := {{msg_var}}.{m_msg_type_field};\n endif;\n"
  #     cfg = {"track_req": False, "prevState": True, "cur_node": True, "RECEIVING": rec_ss, "SENDING": send_ss, "g_msg": True}
  #     parse_murphi_model(coh_model_file, nodes_iter_types, outff_h, cfg, additional_var={})
  #     outff_h.write(dir_postfix_no_outmsg_template.format(state_=state_, mtype=mtype, m_proc_state_field=m_proc_state_field, m_msg_type_field=m_msg_type_field, state_prime=state_prime, m_proc_selc=m_proc_selc, outmsg_type=outmsg_type))
  #   else:
  #     rec_ss = f"if (!isundefined(cur_node) & cur_node = selc) then\n prevMsg := {{msg_var}}.{m_msg_type_field};\n prevMsgDst := {{msg_var}}.{m_msg_dst_field};\n endif;\n"
  #     send_ss = f"if (!isundefined(cur_node) & cur_node = selc) then prevSentMsg := {{msg_var}}.{m_msg_type_field}; endif;\n"
  #     cfg = {"track_req": False, "prevState": True, "cur_node": True, "RECEIVING": rec_ss, "SENDING": send_ss, "g_msg": True}
  #     parse_murphi_model(coh_model_file, nodes_iter_types, outff_h, cfg, additional_var={})
  #     outff_h.write(postfix_no_outmsg_template.format(state_=state_, mtype=mtype, m_proc_state_field=m_proc_state_field, m_msg_type_field=m_msg_type_field, state_prime=state_prime, m_proc_selc=m_proc_selc, outmsg_type=outmsg_type))
      
def gen_s4():
  # get sent msg value 
  with open("build/s1_3_global_msg/_build/aggdict.pkl", "rb") as f:
    g_msg_dir = pickle.load(f)
  with open("build/core_s3_req_send/out/agg.pkl", "rb") as f: 
    aggregate = pickle.load(f)
  dirname = f"build/core_s4_req_send_val/out"
  os.makedirs(dirname, exist_ok = True)  
  for k, v in aggregate.items():
    state_, mtype = k

  
    state_prime = v['state_prime']
    resff = f"build/core_s3_req_send/_build/{state_}_{mtype}_{state_prime}_val.txt"
    ret = get_res_file(resff, f"ASSERT_{state_}_to_{state_prime}", assertion = True)
    assert(ret)
    v['val_chg'] = False

    resff = f"build/core_s3_req_send/_build/{state_}_{mtype}_trace_assert.txt"
    ret = get_res_file(resff, f"{state_}_rec_{mtype}", assertion = True)
    if not ret:
      print("ERROR")
      # need to iterate over to find all message sets 
      assert(0)

    todo = []
    for msg, inc in v['outmsg_set'].items():
      if inc == "true":
        if g_msg_dir[msg][f'from_{m_proc_iter_type}_to_{m_proc_iter_type}'] and g_msg_dir[msg][f'from_{m_proc_iter_type}_to_{m_home_iter_type}']:
          todo.append(msg)
    if len(todo):
      # we go on to see todo's dst 
      print("output the assertion on the dst ")
      assert(0)

    for outmsg_type, inc in v['outmsg_set'].items():
      if inc != "true":
        continue
      if (outmsg_type in req_msg_types) or \
       not outmsg_type in resp_msg_types_w_data:
        continue 

      outff = f"{dirname}/{state_}_{mtype}_{outmsg_type}.m"
      outff_h = open(outff, "w")
      dec = False
      if dst_always_defined:
        rec_ss = f"if (!isundefined(cur_node) & cur_node = selc) then\n prevMsg := {{msg_var}}.{m_msg_type_field};\n endif;\n"
        send_ss = f"if (!isundefined(cur_node) & cur_node = selc & {{msg_var}}.{m_msg_type_field} = {outmsg_type}) then\n prevSentMsg := {{msg_var}}.{m_msg_type_field}; prevSentMsgVal := {{msg_var}}.{m_msg_cl_field};\n endif;\n"
        cfg = {"track_req": False, "prevState": True, "cur_node": True, "RECEIVING": rec_ss, "SENDING": send_ss, "g_msg": True, "prevStateVal": True}
        parse_murphi_model(coh_model_file, nodes_iter_types, outff_h, cfg, additional_var={"prevSentMsgVal": (m_val_type_name, "undefine prevSentMsgVal;\n", "undefine prevSentMsgVal;\n")})
        outff_h.write(dir_postfix_outmsg_val_template.format(state_=state_, mtype=mtype, m_proc_state_field=m_proc_state_field, m_msg_type_field=m_msg_type_field, m_proc_selc=m_proc_selc, outmsg_type=outmsg_type, m_proc_cl_field=m_proc_cl_field))
        
      else:
        rec_ss = f"if (!isundefined(cur_node) & cur_node = selc) then\n prevMsg := {{msg_var}}.{m_msg_type_field};\n prevMsgDst := {{msg_var}}.{m_msg_dst_field};\n endif;\n"
        send_ss = f"if (!isundefined(cur_node) & cur_node = selc) then prevSentMsg := {{msg_var}}.{m_msg_type_field}; prevSentMsgVal := {{msg_var}}.{m_msg_cl_field}; endif;\n"
        cfg = {"track_req": False, "prevState": True, "cur_node": True, "RECEIVING": rec_ss, "SENDING": send_ss, "g_msg": True, "prevStateVal": True}
        parse_murphi_model(coh_model_file, nodes_iter_types, outff_h, cfg, additional_var={"prevSentMsgVal": (m_val_type_name, "undefine prevSentMsgVal;\n", "undefine prevSentMsgVal;\n")})
        outff_h.write(postfix_outmsg_val_template.format(state_=state_, mtype=mtype, m_proc_state_field=m_proc_state_field, m_msg_type_field=m_msg_type_field, m_proc_selc=m_proc_selc, outmsg_type=outmsg_type, m_proc_cl_field=m_proc_cl_field))

        #assert(0)

    continue 

    # resff = f"build/core_s3_req_send/_build/{state_}_{mtype}_no_outmsg.txt"
    # no_outmsg_possible = get_res_file(resff, f"{state_}_rec_{mtype}")
    # possible_outmsg = []
    # if no_outmsg_possible:
    #   possible_outmsg.append("NA")
    #   print("===> no out msg for ", state_, mtype )

    # for outmsg_type in all_msg_types: 
    #   if outmsg_type in req_msg_types:
    #     continue
    #   if not (g_msg_dir[outmsg_type][f'from_{m_proc_iter_type}_to_{m_proc_iter_type}'] or g_msg_dir[outmsg_type][f'from_{m_proc_iter_type}_to_{m_home_iter_type}']):
    #     continue

    #   resff = f"build/core_s3_req_send/_build/{state_}_{mtype}_{outmsg_type}.txt"
    #   outmsg_type_possible = get_res_file(resff, f"{state_}_rec_{mtype}")
    #   if outmsg_type_possible:
    #     possible_outmsg.append(outmsg_type)

    #   if (outmsg_type in req_msg_types) or \
    #    not outmsg_type in resp_msg_types_w_data:
    #     continue 

    #   resff = f"build/core_s3_req_send/_build/{state_}_{mtype}_{outmsg_type}.txt"
    #   print("-->", state_, mtype, outmsg_type, outmsg_type_possible)
    #   if outmsg_type_possible:
    #     outff = f"{dirname}/{state_}_{mtype}_{outmsg_type}.m"
    #     outff_h = open(outff, "w")
    #     dec = False
    #     if dst_always_defined:
    #       rec_ss = f"if (!isundefined(cur_node) & cur_node = selc) then\n prevMsg := {{msg_var}}.{m_msg_type_field};\n endif;\n"
    #       send_ss = f"if (!isundefined(cur_node) & cur_node = selc & {{msg_var}}.{m_msg_type_field} = {outmsg_type}) then\n prevSentMsg := {{msg_var}}.{m_msg_type_field}; prevSentMsgVal := {{msg_var}}.{m_msg_cl_field};\n endif;\n"
    #       cfg = {"track_req": False, "prevState": True, "cur_node": True, "RECEIVING": rec_ss, "SENDING": send_ss, "g_msg": True, "prevStateVal": True}
    #       parse_murphi_model(coh_model_file, nodes_iter_types, outff_h, cfg, additional_var={"prevSentMsgVal": (m_val_type_name, "undefine prevSentMsgVal;\n", "undefine prevSentMsgVal;\n")})

    #       # with open("/Users/yaohsiao/work/coh_syn_dev/murphi/protocols/fv/msi_fv_envs/msi.fvt.s1_msg.m", "r") as f:
    #       #   for ln in f:
    #       #     if f"#RECEIVING" in ln:
    #       #       msg_var = ln[:-1].split(",")[-1]
    #       #       outff_h.write(f"if (!isundefined(cur_node) & cur_node = selc) then\n prevMsg := {msg_var}.{m_msg_type_field};\n endif;\n")
    #       #     elif f"#SENDING" in ln:
    #       #       msg_var = ln[:-1].split(",")[-1]
    #       #       outff_h.write(f"if (!isundefined(cur_node) & cur_node = selc) then\n prevSentMsg := {msg_var}.{m_msg_cl_field};\n endif;\n")
    #       #     elif "BLOCK_WITHIN_BOOK_KEEP" in ln:
    #       #       outff_h.write("undefine prevMsg;\n") # for checking 
    #       #       outff_h.write("undefine prevSentMsg;\n") # for checking 
    #       #       outff_h.write(f"prevProcs := {m_proc_selc};\n")
    #       #     elif "endstartstate" in ln:
    #       #       outff_h.write("undefine prevMsg;\n")
    #       #       outff_h.write("undefine prevSentMsg;\n") # for checking 
    #       #       outff_h.write("undefine prevProcs;\n")
    #       #       outff_h.write(f"for a: {addr_type_name} do myaddr := a; endfor;\n")
    #       #       outff_h.write(f"for n: {m_proc_iter_type} do selc := n; endfor;\n")
    #       #       outff_h.write(ln)
    #       #     else:
    #       #       outff_h.write(ln)
    #       #     if "var" == ln[:3] and not dec:
    #       #       dec = True
    #       #       outff_h.write(f"prevMsg: {msg_type_name};\n")
    #       #       outff_h.write(f"prevSentMsg: {m_val_type_name};\n")
    #       #       outff_h.write(f"prevProcs: {m_cache_type_name};\n")
    #       #       outff_h.write(f"selc: {m_proc_iter_type};\n")
    #       #       outff_h.write(f"myaddr: {addr_type_name};\n")
    #       outff_h.write(dir_postfix_outmsg_val_template.format(state_=state_, mtype=mtype, m_proc_state_field=m_proc_state_field, m_msg_type_field=m_msg_type_field, m_proc_selc=m_proc_selc, outmsg_type=outmsg_type, m_proc_cl_field=m_proc_cl_field))
          
    #     else:
    #       rec_ss = f"if (!isundefined(cur_node) & cur_node = selc) then\n prevMsg := {{msg_var}}.{m_msg_type_field};\n prevMsgDst := {{msg_var}}.{m_msg_dst_field};\n endif;\n"
    #       send_ss = f"if (!isundefined(cur_node) & cur_node = selc) then prevSentMsg := {{msg_var}}.{m_msg_type_field}; prevSentMsgVal := {{msg_var}}.{m_msg_cl_field}; endif;\n"
    #       cfg = {"track_req": False, "prevState": True, "cur_node": True, "RECEIVING": rec_ss, "SENDING": send_ss, "g_msg": True, "prevStateVal": True}
    #       parse_murphi_model(coh_model_file, nodes_iter_types, outff_h, cfg, additional_var={"prevSentMsgVal": (m_val_type_name, "undefine prevSentMsgVal;\n", "undefine prevSentMsgVal;\n")})
    #       outff_h.write(postfix_outmsg_val_template.format(state_=state_, mtype=mtype, m_proc_state_field=m_proc_state_field, m_msg_type_field=m_msg_type_field, m_proc_selc=m_proc_selc, outmsg_type=outmsg_type, m_proc_cl_field=m_proc_cl_field))

    #       #assert(0)
    print("outmsg type", k, possible_outmsg)
    assert(len(possible_outmsg) == 1)
    assert (not 'outmsg' in v)
    if possible_outmsg[0] != "NA":
      v['outmsg'] = possible_outmsg[0]
    # not 'outmsg' in v means no outmsg
    aggregate[k] = v 
  with open(f"{dirname}/agg.pkl", "wb") as f:
    pickle.dump(aggregate, f)

def pp():
  with open("build/core_s4_req_send_val/out/agg.pkl", "rb") as f:
    aggregate = pickle.load(f)
  for k, v in aggregate.items():
    state_, mtype = k

    for outmsg_type, inc in v['outmsg_set'].items():
      if inc != "true":
        continue
      if (outmsg_type in req_msg_types) or \
       not outmsg_type in resp_msg_types_w_data:
        continue 
      resff = f"build/core_s4_req_send_val/_build/{state_}_{mtype}_{outmsg_type}.txt"
      ret = get_res_file(resff, f"ASSERT_{state_}_rec_{mtype}", assertion=True)
      if not 'outmsg_val_eq_cl' in v:
        v['outmsg_val_eq_cl'] = {}
      v['outmsg_val_eq_cl'][outmsg_type] = ret
      if ret:
        print("->", state_, mtype, outmsg_type, ret, outmsg_type in resp_msg_types_w_data)

    # if not 'outmsg' in v:
    #   continue
    # outmsg_type = v['outmsg']
    # if (outmsg_type in req_msg_types) or \
    #   not outmsg_type in resp_msg_types_w_data:
    #   continue 
    # resff = f"build/core_s4_req_send_val/_build/{state_}_{mtype}_{outmsg_type}.txt"
    # ret = get_res_file(resff, f"ASSERT_{state_}_rec_{mtype}", assertion=True)
    # v['outmsg_val_eq_cl'] = ret
    # if ret:
    #   print("->", state_, mtype, outmsg_type, ret, outmsg_type in resp_msg_types_w_data)
    aggregate[k] = v 
  with open("build/core_s4_req_send_val/_build/agg.pkl", "wb") as f:
    pickle.dump(aggregate, f)

if __name__ == "__main__":
    fire.Fire()
    dump_stats()

import os
import pickle
import sys

import fire

from gconst import *
from util import *

if sys.version_info < (3, 6):
  sys.exit(1)

sys.path.append("src")
from code_gen.parse_rules import *


global_inv_template = '''
invariant "{s}_imply_{dir_s}"
forall n: {m_proc_iter_type} do
  ({no_active_txn} & 
    {ss}.{m_proc_state_field} = {s}) ->
  (forall dir: {m_dir_iter_type} do
    {m_dir}.{m_dir_state_field} = {dir_s}
  endforall)
endforall;
'''
global_cov_inv_template = '''
invariant "{s}_imply_{dir_s}"
forall n: {m_proc_iter_type} do
  ({no_active_txn} & 
    {ss}.{m_proc_state_field} = {s}) ->
  !(forall dir: {m_dir_iter_type} do
    {m_dir}.{m_dir_state_field} = {dir_s}
  endforall)
endforall;
'''


# global_inv_iter_stepname = "global_chk_iter"


def gen():
  dirname = f"{build_dir}/global_chk/out"
  os.makedirs(dirname, exist_ok=True)

  # iter_dirname = f"{build_dir}/{global_inv_iter_stepname}/out"
  # os.makedirs(iter_dirname, exist_ok=True)

  ss = m_proc_selc.replace("selc", "n")
  m_dir = m_home_cur.replace("selh", "dir")
  d_dir = m_home_cur.replace("selh", "d")
  tmpn = m_proc_selc.replace("selc", "tmpn")

  core_stable_disj = " | ".join([f"{tmpn}.{m_proc_state_field} = {s_}" for s_ in all_cc_stable_states])
  dir_stable_disj = " | ".join([f"{d_dir}.{m_home_state_field} = {dir_s_}" for dir_s_ in all_llc_stable_states])
  no_active_txn = (
    f"(forall tmpn: {m_proc_iter_type} do\n"
    f"  ({core_stable_disj})\n"
    f"endforall) & (forall d: {m_home_iter_type} do\n"
    f"  ({dir_stable_disj})\n"
    f"endforall)"
  )

  for s in all_cc_stable_states:
    for dir_s in all_llc_stable_states:
      outff = f"{dirname}/{s}_imply_{dir_s}.m"
      with open(outff, "w") as outff_h:
        cfg = {
          "track_req": False,
          "prevState": False,
          "home": True,
        }
        parse_murphi_model(coh_model_file, nodes_iter_types, outff_h, cfg, additional_var={})
        outff_h.write(global_inv_template.format(
          s=s,
          dir_s=dir_s,
          no_active_txn=no_active_txn,
          ss=ss,
          m_proc_state_field=m_proc_state_field,
          m_proc_iter_type=m_proc_iter_type,
          m_dir=m_dir,
          m_dir_iter_type=m_home_iter_type,
          m_dir_state_field=m_home_state_field,
        ))
      outff = f"{dirname}/{s}_imply_cover_{dir_s}.m"
      with open(outff, "w") as outff_h:
        cfg = {
          "track_req": False,
          "prevState": False,
          "home": True,
        }
        parse_murphi_model(coh_model_file, nodes_iter_types, outff_h, cfg, additional_var={})
        outff_h.write(global_cov_inv_template.format(
          s=s,
          dir_s=dir_s,
          no_active_txn=no_active_txn,
          ss=ss,
          m_proc_state_field=m_proc_state_field,
          m_proc_iter_type=m_proc_iter_type,
          m_dir=m_dir,
          m_dir_iter_type=m_home_iter_type,
          m_dir_state_field=m_home_state_field,
        ))

  # # Generate iterative scripts that infer the directory-state disjunction from traces.
  # for s in all_cc_stable_states:
  #   baseff = f"{iter_dirname}/{s}_imply_dir_baseff.m"
  #   with open(baseff, "w") as outff_h:
  #     cfg = {
  #       "track_req": False,
  #       "prevState": False,
  #       "home": True,
  #     }
  #     parse_murphi_model(coh_model_file, nodes_iter_types, outff_h, cfg, additional_var={})

  #   iterff = f"{iter_dirname}/{s}_imply_dir_iter.py"
  #   with open(iterff, "w") as outff_h:
  #     outff_h.write(f'tardir = "{build_dir}"\n')
  #     outff_h.write(f'stepname = "{global_inv_iter_stepname}"\n')
  #     outff_h.write(f's = "{s}"\n')
  #     outff_h.write(f'ss = "{ss}"\n')
  #     outff_h.write(f'm_proc_state_field = "{m_proc_state_field}"\n')
  #     outff_h.write(f'm_proc_iter_type = "{m_proc_iter_type}"\n')
  #     outff_h.write(f'm_dir = "{m_dir}"\n')
  #     outff_h.write(f'm_dir_iter_type = "{m_home_iter_type}"\n')
  #     outff_h.write(f'm_dir_state_field = "{m_home_state_field}"\n')
  #     outff_h.write(f'no_active_txn = {repr(no_active_txn)}\n')
  #     outff_h.write(f'all_llc_stable_states = {repr(all_llc_stable_states)}\n')
  #     with open("src/global_chk_iter_template.py", "r") as f:
  #       for ln in f:
  #         outff_h.write(ln)

def gen_s2():
  dirname = f"{build_dir}/globl_dir_imp/out"
  os.makedirs(dirname, exist_ok=True)

  # m_dir = m_home_cur.replace("selh", "dir")
  d_dir = m_home_cur.replace("selh", "d")
  tmpn = m_proc_selc.replace("selc", "tmpn")
  ss = m_proc_selc.replace("selc", "n2")

  core_stable_disj = " | ".join([f"{tmpn}.{m_proc_state_field} = {s_}" for s_ in all_cc_stable_states])
  dir_stable_disj = " | ".join([f"{d_dir}.{m_home_state_field} = {dir_s_}" for dir_s_ in all_llc_stable_states])
  no_active_txn = (
    f"(forall tmpn: {m_proc_iter_type} do\n"
    f"  ({core_stable_disj})\n"
    f"endforall) & (forall d: {m_home_iter_type} do\n"
    f"  ({dir_stable_disj})\n"
    f"endforall)"
  )

  prop_template = '''
invariant "{dir_s}_owner_imply_not_{s}_others"
forall n1: {m_proc_iter_type} do
  ({no_active_txn} & {m_dir}.{m_dir_state_field} = {dir_s} & {m_dir}.{m_home_owner_field} = n1) ->
  (forall n2: {m_proc_iter_type} do
    n2 != n1 ->
    {ss}.{m_proc_state_field} != {s}
  endforall)
endforall;
'''
  n1_ss = m_proc_selc.replace("selc", "n1")
  prop_template_no_owner = '''
invariant "{s}_imply_not_{sprime}_others"
forall n1: {m_proc_iter_type} do
  ({no_active_txn} & {n1_ss}.{m_proc_state_field} = {s}) ->
  (forall n2: {m_proc_iter_type} do
    n2 != n1 ->
    {ss}.{m_proc_state_field} != {sprime}
  endforall)
endforall;
'''

  if False: #m_home_owner_field is not None: 
    for dir_s in all_llc_stable_states:
      for s in all_cc_stable_states:
        outff = f"{dirname}/{dir_s}_owner_imply_not_{s}.m"
        with open(outff, "w") as outff_h:
          cfg = {
            "track_req": False,
            "prevState": False,
            "home": True,
          }
          parse_murphi_model(coh_model_file, nodes_iter_types, outff_h, cfg, additional_var={})
          outff_h.write(prop_template.format(
            no_active_txn=no_active_txn,
            m_proc_iter_type=m_proc_iter_type,
            m_dir=m_home_cur,
            m_dir_state_field=m_home_state_field,
            dir_s=dir_s,
            m_home_owner_field=m_home_owner_field,
            ss=ss,
            m_proc_state_field=m_proc_state_field,
            s=s,
          ))
  else:
    for s in all_cc_stable_states:
      for s_prime in all_cc_stable_states:
        outff = f"{dirname}/{s}_imply_no_other_{s_prime}.m"
        with open(outff, "w") as outff_h:
          cfg = {
            "track_req": False,
            "prevState": False,
            "home": True,
          }
          parse_murphi_model(coh_model_file, nodes_iter_types, outff_h, cfg, additional_var={})
          outff_h.write(prop_template_no_owner.format(
            no_active_txn=no_active_txn,
            m_proc_iter_type=m_proc_iter_type,
            m_dir=m_home_cur,
            m_dir_state_field=m_home_state_field,
            m_home_owner_field=m_home_owner_field,
            ss=ss,
            m_proc_state_field=m_proc_state_field,
            sprime=s_prime,
            s=s,
            n1_ss=n1_ss
          ))

  if m_home_sharer_field is not None:
    prop_template_imply_sharer = '''
invariant "{s}_imply_in_sharer_list"
forall n1: {m_proc_iter_type} do
  ({no_active_txn} & {n1_ss}.{m_proc_state_field} = {s}) ->
  (multisetcount(i:{m_dir}.{m_home_sharer_field}, {m_dir}.{m_home_sharer_field}[i] = n1) > 0)
endforall;
'''
    for s in all_cc_stable_states:
      outff = f"{dirname}/{s}_imply_in_sharer_list.m"
      with open(outff, "w") as outff_h:
        cfg = {
          "track_req": False,
          "prevState": False,
          "home": True,
        }
        parse_murphi_model(coh_model_file, nodes_iter_types, outff_h, cfg, additional_var={})
        outff_h.write(prop_template_imply_sharer.format(
          s=s,
          no_active_txn=no_active_txn,
          n1_ss=n1_ss,
          m_proc_iter_type=m_proc_iter_type,
          m_proc_state_field=m_proc_state_field,
          m_dir=m_home_cur,
          m_home_sharer_field=m_home_sharer_field,
        ))

  if m_home_owner_field is not None:
    prop_template_imply_owner = '''
invariant "{s}_imply_owner"
forall n1: {m_proc_iter_type} do
  ({no_active_txn} & {n1_ss}.{m_proc_state_field} = {s}) ->
  ({m_dir}.{m_home_owner_field} = n1)
endforall;
'''
    for s in all_cc_stable_states:
      outff = f"{dirname}/{s}_imply_owner.m"
      with open(outff, "w") as outff_h:
        cfg = {
          "track_req": False,
          "prevState": False,
          "home": True,
        }
        parse_murphi_model(coh_model_file, nodes_iter_types, outff_h, cfg, additional_var={})
        outff_h.write(prop_template_imply_owner.format(
          s=s,
          no_active_txn=no_active_txn,
          n1_ss=n1_ss,
          m_proc_iter_type=m_proc_iter_type,
          m_proc_state_field=m_proc_state_field,
          m_dir=m_home_cur,
          m_home_owner_field=m_home_owner_field,
        ))

def pp():
  resdir = f"{build_dir}/global_chk/_build"
  if not os.path.isdir(resdir):
    return

  res = {}
  for s in all_cc_stable_states:
    res[s] = {}
    found = False
    for dir_s in all_llc_stable_states:
      resff = f"{resdir}/{s}_imply_{dir_s}.txt"
      if not os.path.exists(resff):
        res[s][dir_s] = None
        continue
      res[s][dir_s] = get_res_file(resff, f"{s}_imply_{dir_s}", assertion=True, inline_prop=False)
      found = res[s][dir_s] or found 
    if not found: 
      print("===> 0418 TODO", s)
      # we see if there is any combination of those 
      cov_s = []
      for dir_s in all_llc_stable_states:
        resff = f"{resdir}/{s}_imply_cover_{dir_s}.txt"
        ret = get_res_file(resff, f"{s}_imply_{dir_s}", assertion=False, inline_prop=False)
        if ret:
          cov_s.append(dir_s)
      # print(res[s][dir_s])
      if len(cov_s) != len(all_llc_stable_states):
        for itm in cov_s:
          res[s][itm] = True

  with open(f"{resdir}/res.pkl", "wb") as f:
    pickle.dump(res, f)

  with open(f"{resdir}/res.txt", "w") as f:
    for s in all_cc_stable_states:
      for dir_s in all_llc_stable_states:
        f.write(f"{s},{dir_s}:{res[s][dir_s]}\n")

  resdir_s2 = f"{build_dir}/globl_dir_imp/_build"
  if not os.path.isdir(resdir_s2):
    return

  res_s2 = {}
  if False: #m_home_owner_field is not None:
    for dir_s in all_llc_stable_states:
      if not dir_s in res_s2:
        res_s2[dir_s] = {}
      for s in all_cc_stable_states:
        resff = f"{resdir_s2}/{dir_s}_owner_imply_not_{s}.txt"
        prop = f"{dir_s}_owner_imply_not_{s}_others"
        if not os.path.exists(resff):
          res_s2[dir_s][s] = None
          continue
        res_s2[dir_s][s] = get_res_file(resff, prop, assertion=True, inline_prop=False)
  else:
    for s in all_cc_stable_states:
      if s not in res_s2:
        res_s2[s] = {}
      for s_prime in all_cc_stable_states:
        resff = f"{resdir_s2}/{s}_imply_no_other_{s_prime}.txt"
        prop = f"{s}_imply_not_{s_prime}_others"
        if not os.path.exists(resff):
          res_s2[s][s_prime] = None
          continue
        res_s2[s][s_prime] = get_res_file(resff, prop, assertion=True, inline_prop=False)

      if m_home_sharer_field is not None:
        resff = f"{resdir_s2}/{s}_imply_in_sharer_list.txt"
        prop = f"{s}_imply_in_sharer_list"
        if not os.path.exists(resff):
          res_s2[s]["imply_in_sharer_list"] = None
        else:
          res_s2[s]["imply_in_sharer_list"] = get_res_file(resff, prop, assertion=True, inline_prop=False)

      if m_home_owner_field is not None:
        resff = f"{resdir_s2}/{s}_imply_owner.txt"
        prop = f"{s}_imply_owner"
        if not os.path.exists(resff):
          res_s2[s]["imply_owner"] = None
        else:
          res_s2[s]["imply_owner"] = get_res_file(resff, prop, assertion=True, inline_prop=False)

  with open(f"{resdir_s2}/res.pkl", "wb") as f:
    pickle.dump(res_s2, f)

  with open(f"{resdir_s2}/res.txt", "w") as f:
    if False: #m_home_owner_field is not None:
      for dir_s in all_llc_stable_states:
        for s in all_cc_stable_states:
          f.write(f"{dir_s},{s}:{res_s2[dir_s][s]}\n")
    else:
      for s in all_cc_stable_states:
        for s_prime in all_cc_stable_states:
          f.write(f"{s},{s_prime}:{res_s2[s][s_prime]}\n")
        if m_home_sharer_field is not None:
          f.write(f"{s},imply_in_sharer_list:{res_s2[s]['imply_in_sharer_list']}\n")
        if m_home_owner_field is not None:
          f.write(f"{s},imply_owner:{res_s2[s]['imply_owner']}\n")


if __name__ == "__main__":
  fire.Fire()
  dump_stats()

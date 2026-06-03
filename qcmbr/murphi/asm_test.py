import sys
from pprint import pprint
import pickle
import argparse
from collections import OrderedDict
sys.path.append("src")
from gconst import *

from assemble_uspec_reorg import *

if len(sys.argv) < 2:
  print("out file name?")
  sys.exit(0)
outf = sys.argv[1]
core_upath_no_txn = load_pickle_file("build/s4_6_ret_val/_build/agg_no_txn_init.pkl")
core_upath_txn = load_pickle_file("build/s4_6_ret_val/_build/agg_txn_init.pkl")
post_fix_dict = load_pickle_file("build/core_s4_req_send_val/_build/agg.pkl") #load_pickle_file("tmp.pkl")
g_msg_dir_raw = load_pickle_file("build/s1_3_global_msg/_build/aggdict.pkl")
g_msg_cnt = load_pickle_file("build/s1_gmsg_cnt/_build/aggdict.pkl")
init_core_imp_dir = load_pickle_file("build/global_chk/_build/res.pkl")
init_core_imp_core = load_pickle_file("build/globl_dir_imp/_build/res.pkl")
g_msg_dir = OrderedDict()
for m, val in g_msg_dir_raw.items():
  if m in all_msg_types:
    g_msg_dir[m] = OrderedDict()
    for k, v in val.items():
      if k == f"from_{m_proc_iter_type}_to_{m_home_iter_type}":
        g_msg_dir[m]['from_core_to_home'] = v
      elif k == f"from_{m_proc_iter_type}_to_{m_proc_iter_type}":
        g_msg_dir[m]['from_core_to_core'] = v
      elif k == f"from_{m_home_iter_type}_to_{m_proc_iter_type}":
        g_msg_dir[m]['from_home_to_core'] = v
  else:
    g_msg_dir[m] = val
if g_msg_dir['dst_always_defined']:
  home_dict, all_paths = load_pickle_file("build/home_s3_msg_val_src_dst/_build/agg.pkl")
else:
  home_dict, all_paths = load_pickle_file("build/home_s3_msg_out_info/_build/agg.pkl")
if len(sys.argv) < 3 or (sys.argv[2] != "yes" and sys.argv[2] != "no"):
  print("mresp_at_end_txn")
  sys.exit(0)
mresp_at_end_txn = True if sys.argv[2] == "yes" else False
protocol = MySyntaxTree(core_upath_no_txn, core_upath_txn, home_dict, all_paths, post_fix_dict, g_msg_dir, init_core_imp_dir, init_core_imp_core, mresp_at_end_txn, g_msg_cnt)

protocol.construct_all()
protocol.export(outf)

sys.exit(0)

post_fix_dict = OrderedDict()
post_fix_dict[("P_V", "GetMsg", "core")] = OrderedDict()
# TODO: GetMsg src
# no transient state 
# False -> 'state_prime/msg_out' is sinlge value whereas True then 'state_prime/msg_out' should be array
post_fix_dict[("P_V", "GetMsg", "core")]['txn_init'] = False 
post_fix_dict[("P_V", "GetMsg", "core")]['state_prime'] = 'P_I'
# dest to core/hoome
post_fix_dict[("P_V", "GetMsg", "core")]['msg_out'] = ('DataRespMsg', 'core')
# TODO: value constraint 
# TODO: post fix path: 
# could there be some message type that can be received/sent out during
# transaction and in the post-fix path it is also received/sent out -> which
# requires multiple instance of same label

g_msg_dir = {}
for msg in all_msg_types:
  g_msg_dir[msg] = {}
g_msg_dir["GetMsg"]['from_core_to_home'] = True
g_msg_dir["GetMsg"]['from_core_to_core'] = True 
g_msg_dir["GetMsg"]['from_home_to_core'] = False
g_msg_dir["PutMsg"]['from_core_to_home'] = True
g_msg_dir["PutMsg"]['from_core_to_core'] = False
g_msg_dir["PutMsg"]['from_home_to_core'] = False
g_msg_dir["DataRespMsg"]['from_core_to_home'] = False
g_msg_dir["DataRespMsg"]['from_core_to_core'] = True
g_msg_dir["DataRespMsg"]['from_home_to_core'] = True

# - [ ] ci_evict
#   - put_msg value same as the q's cc_P_V_1
# - 
# - [ ] from_home_to_core: is it ithe same core or different core as the rqeuesting core
# - [ ] msg_dst_src_reachable not only the src/dst to core/home but also see if the multiple message type are to the same core or not i.e., out_c_{mtype1}.dst == in_c_{mtype2}.src
# - [ ] out/in data msg value matched which picl

from assemble_uspec import *

# python3 src/assemble_uspec.py past_builds/VI_build/s5_0_home_no_involved/_build/aggdict.pkl past_builds/VI_build/home_s3_val_check/_build/aggdict.pkl tmp.pkl

core_upaths_dict =  load_pickle_file("past_builds/VI_build/s5_0_home_no_involved/_build/aggdict.pkl")
home_dict = load_pickle_file("past_builds/VI_build/home_s3_val_check/_build/aggdict.pkl")
# post_fix_dict = load_pickle_file("tmp.pkl")
protocol = MySyntaxTree(core_upaths_dict, home_dict, post_fix_dict, g_msg_dir)

protocol.construct_all()
protocol.export("vi_test.uarch")

  
build_dir="past_builds/VI_buggy_build"
all_req_types = ["ci_load", "ci_store", "ci_evict"] 
req_is_read = ["ci_load"]
type_with_args = ["ci_store"]

coh_model_file = "protocols/plain/mi_no_fetch_on_write_buggy.m"
# assume nodes_iter_types[0] is largest set of all 
nodes_iter_types = ["Node", "Proc"]
m_val_type_name = "Value"

m_proc_iter_type = "Proc"

m_proc_selc = "Procs[selc]"

addr_type_name = ""
m_proc_state_type = "ProcStateEnum"
m_proc_state_field = "state"

m_proc_cl_field = "val"

# HOME
all_llc_states = ["H_I", "H_V"]
all_llc_stable_states = ["H_I", "H_V"]
m_home_cur = "HomeNode"
m_home_iter_type = "Home"
m_home_state_type = "HomeStateEnum"
m_home_state_field = "state"
m_home_cl_field = "val"
main_mem_name = 'MainMemory'

m_home_owner_field = None
m_home_sharer_field = None

all_cc_states = ["P_I", "P_IVD", "P_V"]
all_cc_stable_states = ["P_I", "P_V"]

m_req_type_field = "tp"

all_msg_types = ["GetMsg", "PutMsg", "DataRespMsg"]
#
req_msg_types = ["GetMsg", "PutMsg"]
req_msg_types_with_data = ["PutMsg"]
#
fwd_req_msg_types = []
# 
resp_msg_types_w_data = ["DataRespMsg"]
resp_msg_types = ["DataRespMsg"]

m_msg_dst_field = "dst"
m_msg_src_field = "src"
m_msg_type_field = "mtype"
m_msg_cl_field = "val"

msg_type_name = "MessageType"
design_cfg = {}
#  ################################################################################
#  # VI protocol
#  ################################################################################
#  # including transient and non-transient
#  # type of request with data value 
#  type_val_return = ["ci_load"]
#  # Already in CI interface
#  # design_file = "./protocols/ci/mi_no_fetch_on_write.m"
#  # TODO instrumented with the FV environemtn variables...
#  design_file = "./protocols/fv/mi_no_fetch_on_write.fvt.m"
#  req_msg_types = ["PutMsg", "GetMsg"]
#  req_msg_types_with_data = ["PutMsg"]
#  fwd_req_msg_types = []
#  
#  dst_always_defined=False
#  
#  typeid_cc_state = 'ProcState'
#  # if the implementation does model the main memory 
#  
#  config = {
#      # annotate the type refer to all nodes
#      "`AllNodeCI": "Node",
#      # annotate the type refer to all caches
#      "`ALLCoreCI": "Proc",
#      # the array name that contains all caches 
#      "`ALLCores": "Procs", 
#      # annotate the type refer to all values; 
#      "`ValueCI": "Value", 
#      # (<rule_name>, <quantifier ID over `AllCoreCI>)
#      "rule_accepting_read": [("load_P_I", "n")], 
#      # (<rule_name>, <quantifier ID over `AllCoreCI>, <quantifier_ID_over_`ValueCI) 
#      "rule_accepting_write": [("store_P_I", "n", "v"), ("store_P_V", "n", "v")],
#      # (<rule_name>, <quantifier ID over `AllCoreCI>, <name_for_value_retured/cacheline value>)
#      "rule_accepting_read_ret_read": [("load_P_V", "n",  "p.val")], 
#      "rule_accepting_eviction": [("evict_P_V", "n")],
#      # TODO!!!? Per core's incoming/outgoing message array/variable 
#  }
#  
#  m_proc_arr = config['`ALLCores']
#  # m_proc_selc = Procs[selc]
#  # field name that correspond to the state in the private cache 
#  m_proc_state_field = "state"
#  # field name that correspond to the value in the private cache  (al so the value used in home)
#  # the field name in the message type that correspond to the types of message 
#  # Home type
#  m_home_node = "Home"
#  # Proc type
#  m_proc_node = "Proc"
#  
#  
#  # field name that correspond to the state in the home
#  # the value that can index to the Home in confg[`AllNodeCI]
#  m_home_iter = "HomeType"    # annotate the value that can is indexing in to home 
#  
#  ################################################################################
#  
#  dis_junc_stable_states = "("
#  for itm in all_cc_stable_states:
#    dis_junc_stable_states += f"a_core_state = {itm} | "
#  dis_junc_stable_states += " false )"
#  
import re
from pprint import pprint
import pickle
from gconst import *
import random
colors_=["aliceblue","antiquewhite","aquamarine","azure","beige","bisque","black","blanchedalmond","blue","blueviolet","brown","burlywood","cadetblue","chartreuse","chocolate","coral","cornflowerblue","cornsilk","crimson","cyan","darkblue","darkcyan","darkgoldenrod","darkgray","darkgreen","darkgrey","darkkhaki","darkolivegreen","darkorange","darkorchid","darkred","darksalmon","darkseagreen","darkslateblue","darkslategray","darkslategrey","darkturquoise","darkviolet","deeppink","deepskyblue","dimgray","dimgrey","dodgerblue","firebrick","floralwhite","forestgreen","gainsboro","ghostwhite","gold","goldenrod","gray","grey","green","greenyellow","honeydew","hotpink","indianred","indigo","ivory","khaki","lavender","lavenderblush","lawngreen","lemonchiffon","lightblue","lightcoral","lightcyan","lightgoldenrodyellow","lightgray","lightgrey","lightpink","lightsalmon","lightseagreen","lightskyblue","lightslategray","lightslategrey","lightsteelblue","lightyellow","limegreen","linen","magenta","maroon","mediumaquamarine","mediumblue","mediumorchid","mediumpurple","mediumseagreen","mediumslateblue","mediumspringgreen","mediumturquoise","yellow","yellowgreen"]
color_idx = 0
en_color = False
def g_color():
  if not en_color:
    return "black"
  global color_idx
  ret = colors_[color_idx]
  color_idx += 1
  color_idx = color_idx % len(colors_)
  return ret 

nm_stage = "StageName {i} \"{nm}\".\n"
v_stage = "VTStageName {i} {j} \"{nm}\".\n"

postfix_axiom = '''
Axiom \"{req}_upath_{idx}_postfix_possibility\":
forall microop "j", OnCore c j => {type_pred} => 
  {case_pred} => (
  {postfix_possibilities}
  ).
'''
initial_state_axiom = '''
Axiom \"{req}_upath_{idx}_initial_state\":
  forall microop "i", OnCore c i => {type_pred} => 
  NodeExists (i, case_{idx}) => 
  (exists microop "q", ProgramOrder q i /\\ SamePhysicalAddress q i /\\
  {core_initial_pred}
  ).
'''
home_initial_state_axiom = '''
Axiom \"{req}_upath_{idx}_home_initial_state\":
  forall microop "i", OnCore c i => {type_pred} => 
  % core case 
  NodeExists (i, case_{idx}) => 
  % home case 
  NodeExists (i, h_case_{h_idx}) => 
  (exists microop "k", ~SameMicroop k i /\\ SamePhysicalAddress k i /\\ 
  {k_precond}
  {home_initial_pred}
  ).
'''
postfix_nonintervene = '''
~(exists microop "r", SameCore r j /\\ ~SameMicroop r j /\\ SamePhysicalAddress r j /\\ ~AccessType InitAcc r /\\ (
{pred}))
'''
def get_type_pred(req, inst):
  if req == "ci_load":
    return f"(~AccessType InitAcc {inst} /\\ ~AccessType Evict {inst} /\\ IsAnyRead {inst})"
  elif req == "ci_store":
    return f"(~AccessType InitAcc {inst} /\\ ~AccessType Evict {inst} /\\ IsAnyWrite {inst})"
  else:
    return f"(~AccessType InitAcc {inst} /\\ AccessType Evict {inst} /\\ IsAnyWrite {inst})"
def g_edge(n1, n2, comment="", c="black", e=False, w_pred=True):
  c=g_color()
  if e:
    return f"EdgeExists ({n1}, {n2}, \"{comment}\", \"{c}\")"
  if w_pred:
    return f"AddEdge ({n1}, {n2}, \"{comment}\", \"{c}\")"
  else:
    return f"({n1}, {n2}, \"{comment}\", \"{c}\")"
def g_node(i, n, w_pred=False, neg=False, single=False):
  if single:
    n = f"(0, {n})"
  pre = ""
  if neg:
    pre="~"
  if w_pred:
    return f"{pre}NodeExists ({i}, {n})"
  return f"({i}, {n})"
# def non_intervene_core_postfix_(q, state, cc_s, trans_closure):
#   preds_ = [] 
#   for c in cc_s:
#     #e_.append("~" + g_edge(f"({q}, cc_{state}_1)", f"({q}, cc_{c}_1)", e=True))
#     if c == state:
#       continue
#     # within single column 
#     if c in trans_closure and state in trans_closure[c]:
#       preds_.append("((%s) \\/ (%s))" % (g_node(q, f"cc_{c}_1", w_pred=True, neg=True), g_edge(f"({q}, cc_{c}_lst)", f"({q}, cc_{state}_1)", e=True)))
#     else:
#       preds_.append(g_node(q, f"cc_{c}_1", w_pred=True, neg=True))
#   return " /\\ ".join(preds_)

def non_intervene_core(i, q, cc_s):
  assert(q != "r" and i != "r")
  preds_ = []
  for c in cc_s:
    preds_.append(f"NodeExists (r, cc_{c}_1)")
  preds = " \\/ ".join(preds_)
  return f"~(exists microop \"r\", ProgramOrder {q} r /\\ ProgramOrder r {i} /\\ SamePhysicalAddress {q} r /\\ \n ({preds}))"

def load_pickle_file(filename):
    try:
        with open(filename, 'rb') as f:
            data = pickle.load(f)
            print(f"Successfully loaded data from {filename}")
            return data
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
        return None
    except pickle.UnpicklingError:
        print(f"Error: Could not unpickle the file '{filename}'. It may be corrupted or not a pickle file.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

import functools

def log_method_name(func):
    @functools.wraps(func)  # Preserves the original method name and docstring
    def wrapper(*args, **kwargs):
        print(f"[INFO] Method: {func.__name__}")
        return func(*args, **kwargs)
    return wrapper
    
one_req_axiom = '''
Axiom "one_req_simple_core_across_all_addresses_at_a_time":
  forall microop "i", forall microop "j",
  SameCore i j /\\
  ~(AccessType InitAcc i /\\ AccessType InitAcc j) /\\
  ProgramOrder i j =>
    AddEdge ((i, MResp), (j, CReq), "single_req", "black").
'''
final_state_chk_t = '''
Axiom "final_state_check_{state}":
forall microop "i", 
  NodeExists (i, (0, h_{state}_1))  =>
  % or i is final then its value match
  IsFinalDefined i => 
  AssocValEqFinalDataAtPA (i, (0, h_{state}_1)) i \\/  
    % not i is final -> exists some j such that 
    (exists microop "j", SamePhysicalAddress i j /\\ ~SameMicroop i j /\\
     ({before_ss}) 
    ).
'''
init_acc_axiom = '''
Axiom "{nm}": 
  forall microop "i", AccessType InitAcc i =>
  {pred_n}. 
'''

msg_axioms = '''
Axiom "{nm}":
forall microop "i", 
  OnCore c i => {type_pred} =>
  {case_pred} =>
  ( % exists the one that responds
    exists microop "j",
    ~SameCore i j /\\  SamePhysicalAddress i j /\\
    {pred}
  ).
'''
# one to one
per_msg_existence = '''
Axiom "msg_{dir}_{mtype}":
forall microop "i", 
  {node_pred} => 
    exists microop "j", (
    ~SameCore i j /\\ SamePhysicalAddress i j /\\ 
    {pred}
).

'''

# diff core trigger for 
not_src_msg = '''
Axiom "msg_h_out_{mtype}":
forall microop "i", 
 NodeExists (i, (0, h_out_{mtype})) =>
  exists microop "j", (
  ~SameCore i j /\ SamePhysicalAddress i j /\   
  ({disj})
). 
'''
not_src_msg_rev = '''
Axiom "msg_{mtype_at_core}":
forall microop "i", 
 NodeExists (i, {mtype_at_core}) =>
  exists microop "j", (
  ~SameCore i j /\ SamePhysicalAddress i j /\   
  EdgeExists ((j, (0, h_out_{mtype})), (i, {mtype_at_core}), "com") 
). 

'''
#    EdgeExists ((i, outmsg_get), (j, inmsg_get), "com") /\
#    (forall microop "k", 
#      ((~SameMicroop i k) /\ (~SameMicroop j k) /\ SamePhysicalAddress k i 
#        %/\ ~NodeExists (k, (0, mc_inmsg_get))
#        ) =>
#        (NodeExists (k, outmsg_get) => (
#          (EdgeExists ((i, outmsg_get), (k, outmsg_get), "ATOM") /\ EdgeExists ((j, inmsg_get), (k, outmsg_get), "ATOM")) \/
#          (EdgeExists ((k, outmsg_get), (i, outmsg_get), "ATOM") /\ EdgeExists ((k, outmsg_get), (j, inmsg_get), "ATOM"))
#        )) /\
#        (NodeExists (k, inmsg_get) => (
#          (EdgeExists ((i, outmsg_get), (k, inmsg_get), "ATOM") /\ EdgeExists ((j, inmsg_get), (k, inmsg_get), "ATOM")) \/
#          (EdgeExists ((k, inmsg_get), (i, outmsg_get), "ATOM") /\ EdgeExists ((k, inmsg_get), (j, inmsg_get), "ATOM"))
#        ))
#    )
cc_total_order_po = r'''
Axiom "total_order_cc_state_follows_program_order_{idx}":
forall microop "i", forall microop "j",  
  ProgramOrder i j /\ SamePhysicalAddress i j =>
  NodeExists (i, cc_{state1}_1) /\ NodeExists (j, cc_{state2}_1) =>
  EdgeExists ((i, cc_{state1}_lst), (j, cc_{state2}_1), "total_order_PO").
'''
home_init_preced = r'''
Axiom "mc_for_initacc_{idx}":
  forall microop "i", forall microop "j", 
    AccessType InitAcc i /\ ~SameMicroop i j /\ SamePhysicalAddress i j => 
      NodeExists (i, (0, h_{state1}_1)) /\ NodeExists (j, (0, h_{state2}_1)) =>
      EdgeExists ((i, (0, h_{state1}_lst)), (j, (0, h_{state2}_1)), "i_mc_precdeall").
'''
home_po = r'''
Axiom "mc_for_po_{idx}":
forall microop "i", forall microop "j",
ProgramOrder i j /\ SamePhysicalAddress i j  => 
NodeExists (i, (0, h_{state1}_1)) /\ NodeExists (j, (0, h_{state2}_1)) =>
EdgeExists ((i, (0, h_{state1}_lst)), (j, (0, h_{state2}_1)), "mc_po").
'''

home_single_state_non_inter = r'''
Axiom "single_state_main_mem_{idx}":
forall microop "i", forall microop "r", 
SamePhysicalAddress i r /\ ~SameMicroop i r  =>
EdgeExists ((i, (0, h_{state}_1)), (i, (0, h_{state}_lst)), "h", "black") =>  
({disjunct}).
'''

home_single_state = r'''
Axiom "single_state_main_mem_{idx}":
forall microop "i", forall microop "j", 
 ~SameMicroop i j /\ SamePhysicalAddress i j  =>
NodeExists (i, (0, h_{state1}_1)) /\ NodeExists (j, (0, h_{state2}_1)) => 
EdgeExists ((i, (0, h_{state1}_lst)), (j, (0, h_{state2}_1)), "one_way") \/
EdgeExists ((j, (0, h_{state2}_lst)), (i, (0, h_{state1}_1)), "the_other").
'''
cc_single_state = r'''
Axiom "total_order_cc_state_{idx}":
forall microop "i", forall microop "j", 
SameCore i j /\ SamePhysicalAddress i j {opt_pred} =>
(NodeExists (i, cc_{state1}_1) /\ NodeExists (j, cc_{state2}_1)) => 
EdgeExists ((i, cc_{state1}_lst), (j, cc_{state2}_1), "one_way") \/
EdgeExists ((j, cc_{state2}_lst), (i, cc_{state1}_1), "the_other").
'''

from itertools import permutations

def has_valid_permutation(tuples_list):
    """
    Determines if there exists a permutation of tuples such that
    for any element p[i], the second element of p[i] equals the first
    element of p[i+1].

    Args:
        tuples_list (list of tuples): List of tuples to check.

    Returns:
        bool: True if such a permutation exists, False otherwise.
    """
    ret = []
    for perm in permutations(tuples_list):
        valid = True
        for i in range(len(perm) - 1):
            if perm[i][2][1][-1][1] != perm[i + 1][0][0]:
                valid = False
                break
        if valid:
          ret.append(perm)
    return ret
def is_data_type(msg_type):
  return (msg_type in resp_msg_types_w_data) or (msg_type in req_msg_types_with_data)

def non_intervene_core_postfix_(q, state, cc_s, trans_closure):
  preds_ = [] 
  for c in sorted(cc_s):
    #e_.append("~" + g_edge(f"({q}, cc_{state}_1)", f"({q}, cc_{c}_1)", e=True))
    if c == state:
      continue
    # within single column 
    if c in trans_closure and state in trans_closure[c]:
      preds_.append("((%s) \\/ (%s))" % (g_node(q, f"cc_{c}_1", w_pred=True, neg=True), g_edge(f"({q}, cc_{c}_lst)", f"({q}, cc_{state}_1)", e=True)))
    else:
      preds_.append(g_node(q, f"cc_{c}_1", w_pred=True, neg=True))
  print("DEBUG0224 preds", preds_)
  return " /\\ ".join(preds_)

def trans_closure(adj_matrix):
    """
    Compute the transitive closure of a directed graph represented as an adjacency list.

    Args:
        adj_list (dict): A dictionary where keys are nodes and values are lists of adjacent nodes.

    Returns:
        dict: A dictionary representing the transitive closure of the graph.
    """
    V = set(adj_matrix.keys())
    for k, v in adj_matrix.items():
      V.update(v)

    # Assuming adj_matrix is initialized with 1 for edges and 0 otherwise
    for k in V: 
        for i in V:
            for j in V:
                if i in adj_matrix and k in adj_matrix[i] and k in adj_matrix and j in adj_matrix[k]:
                  if not i in adj_matrix:
                    adj_matrix[i] = []
                  adj_matrix[i].append(j)
    return adj_matrix
    # return {node: list(adj_nodes) for node, adj_nodes in closure.items()}

one_to_one_map_t = r'''
Axiom "one_to_one_map_{m}":
forall microop "i", forall microop "j",
~AccessType InitAcc i /\ ~AccessType InitAcc j =>
~SameCore i j /\ SamePhysicalAddress i j =>
EdgeExists ((i, {out_nm}), (j, {in_nm}), "com") =>
    (forall microop "k",
      (~AccessType InitAcc k /\ ~SameMicroop i k /\ ~SameMicroop j k /\ SamePhysicalAddress k i) =>
      (EdgeExists ((i, {out_nm}), (k, {in_nm}), "com") =>
      (exists microop "n", ~AccessType InitAcc n /\ SamePhysicalAddress k n /\ 
        ~SameMicroop n i /\ ~SameMicroop n j /\ ~SameMicroop n k /\  
        NodeExists (n, {out_nm})
      )
    )
  )
.
% EdgeExists ((n, {out_nm}), (k, {in_nm}), "com") 

'''
import fire
from gconst import *
import pickle
import subprocess
import os 
import sys
import re
import argparse
from collections import OrderedDict
from util import *
# cover (home.state = {hstate} & recMesage/snoopMsg = {msgType})
# For directory-based: whether {hstate} can receive {msgType}  
# For snooping-based: <> whether {hstate} can snoop {msgType} ; It doesn't yet
# mean the {hstate} can accepts and process {msgType} or not 
h_accept_template= '''
invariant "{hstate}_consistent_w_{mtype}"
  -- can {hstate} ever receives/processes {mtype} message 
  (!isundefined(prevHomeNode) & prevHomeNode = {hstate} & 
    !isundefined(prevMsg) & prevMsg = {mtype}) ->
  !( prevHomeNode != {m_home_cur}.{m_home_state_field} | 
    (!isundefined(prevMsgDst) & prevMsgDst = selh) | 
    !isundefined(prevSentMsg));
'''
h_accept_template_trace = '''
invariant "{hstate}_consistent_w_{mtype}"
  -- can {hstate} receives {mtype} message 
  (!isundefined(prevHomeNode) & (prevHomeNode = {hstate})) -> 
  (isundefined(prevRecProcMsg) | prevRecProcMsg != {mtype});
'''
h_accept_outmsg_assert = '''
invariant "ASSERT_{hstate}_accept_req_{mtype}"
  (!isundefined(prevHomeNode) & prevHomeNode = {hstate} & 
   !isundefined(prevRecProcMsg) & prevRecProcMsg = {mtype}) ->
   ({sent_msg_ss});
'''
dir_h_accept_template = '''
invariant "{hstate}_consistent_w_{mtype}"
  -- can {hstate} receives {mtype} message 
  (!isundefined(prevHomeNode) & (prevHomeNode = {hstate})) -> 
  (isundefined(prevRecProcMsg) | prevRecProcMsg != {mtype});
'''

dir_h_accept_trans_local_core_template = '''
-- check {hstate} receives/processes {mtype} and transition to {hstate_prime}?
invariant "{hstate}_accept_req_{mtype}"
  (!isundefined(prevHomeNode) & prevHomeNode = {hstate} & 
   !isundefined(prevRecProcMsg) & prevRecProcMsg = {mtype} & 
   ({home_state_expr} = {hstate_prime})) ->
  (prevProcs = {proc_state_expr})
   ;
'''
dir_h_accept_trans_template_no_inmsg = '''
invariant "{hstate}_no_inmsg"
 !( !isundefined(prevHomeNode) & (prevHomeNode = {hstate}) & ({home_state_expr} = {hstate_prime}) & (p_inmsg = false) );
'''
dir_h_accept_trans_template = '''
-- check {hstate} receives/processes {mtype} and transition to {hstate_prime}?
invariant "{hstate}_accept_req_{mtype}"
  (!isundefined(prevHomeNode) & prevHomeNode = {hstate} & 
   !isundefined(prevRecProcMsg) & prevRecProcMsg = {mtype}) ->
   !({home_state_expr} = {hstate_prime});
'''
home_inmsg_notxn_transition_template = '''
-- check {hstate} receives/processes {mtype} and transition to {hstate_prime}?
invariant "{hstate}_accept_req_{mtype}"
  (!isundefined(prevHomeNode) & (prevHomeNode = {hstate}) & 
   !isundefined(prevRecProcMsg) & prevRecProcMsg = {mtype}) ->
   !({m_home_cur}.{m_home_state_field} = {hstate_prime});
'''

dir_h_accept_owner_vld_field_template = '''
-- check {hstate} with owner undefined receives/processes {mtype} ?
invariant "{hstate}_accept_req_{mtype}"
  (!isundefined(prevHomeNode) & prevHomeNode = {hstate} & 
   !isundefined(prevRecProcMsg) & prevRecProcMsg = {mtype}) ->
   !prevHomeNodeOnwerVld;
'''
dir_h_accept_owner_def_template = '''
-- check {hstate} with owner undefined receives/processes {mtype} ?
invariant "{hstate}_accept_req_{mtype}"
  (!isundefined(prevHomeNode) & prevHomeNode = {hstate} & 
   !isundefined(prevRecProcMsg) & prevRecProcMsg = {mtype}) ->
   !isundefined(prevHomeNodeOnwer);
'''
dir_h_assert_owner_src_template = '''
-- check {hstate} with owner undefined receives/processes {mtype} transition to {hstate_prime} with src be owner?
invariant "{hstate}_accept_req_{mtype}"
  (!isundefined(prevHomeNode) & prevHomeNode = {hstate} & 
   !isundefined(prevRecProcMsg) & prevRecProcMsg = {mtype} & 
    {home_state_expr} = {hstate_prime}) -> 
    ({m_home_owner_expr} = prevRecProcMsgSrc);
'''
dir_h_accept_owner_src_template = '''
-- check {hstate} with owner undefined receives/processes {mtype} transition to {hstate_prime} with src be owner?
invariant "{hstate}_accept_req_{mtype}"
  (!isundefined(prevHomeNode) & prevHomeNode = {hstate} & 
   !isundefined(prevRecProcMsg) & prevRecProcMsg = {mtype} & 
   !isundefined(prevHomeNodeOnwer) & prevHomeNodeOnwer {is_owner} prevRecProcMsgSrc) ->
   !({m_home_cur}.{m_home_state_field} = {hstate_prime});
'''
dir_h_accept_nonempty_sharer_emplate = '''
-- check {hstate} with owner undefined receives/processes {mtype} ?
invariant "{hstate}_accept_req_{mtype}"
  (!isundefined(prevHomeNode) & prevHomeNode = {hstate} & 
   !isundefined(prevRecProcMsg) & prevRecProcMsg = {mtype}) ->
   !(non_empty_sharer);
'''
dir_h_accept_sharer_src_template = '''
-- check {hstate} with owner undefined receives/processes {mtype} ?
invariant "{hstate}_accept_req_{mtype}"
  (!isundefined(prevHomeNode) & prevHomeNode = {hstate} & 
   !isundefined(prevRecProcMsg) & prevRecProcMsg = {mtype} & 
   {aux_cond} 
   {is_last}src_last_sharer) ->
   !{m_home_cur}.{m_home_state_field} = {hstate_prime}
   ;
'''

dir_h_accept_trans_outmsg_dst_aws_owner_template = '''
invariant "ASSERT_{hstate}_accept_req_{mtype}"
  (!isundefined(prevHomeNode) & prevHomeNode = {hstate} & 
   !isundefined(prevRecProcMsg) & prevRecProcMsg = {mtype} & 
   {home_state_expr} = {hstate_prime} & sent) ->
   (out_msg_dst = prevHomeNodeOnwer);
'''

dir_h_accept_trans_outmsg_dst_aws_owner_template_no_inmsg = '''
invariant "ASSERT_{hstate}_no_inmsg"
  (!isundefined(prevHomeNode) & prevHomeNode = {hstate} & 
   p_inmsg = false & 
   {home_state_expr} = {hstate_prime} & sent) ->
   (out_msg_dst = prevHomeNodeOnwer);
'''

dir_h_accept_trans_outmsg_cnt_template = '''
invariant "ASSERT_{hstate}_accept_req_{mtype}"
  (!isundefined(prevHomeNode) & prevHomeNode = {hstate} & 
   !isundefined(prevRecProcMsg) & prevRecProcMsg = {mtype} & 
   {home_state_expr} = {hstate_prime} & sent) ->
   cnt <= 1;
'''
dir_h_accept_trans_outmsg_cnt_template_no_inmsg = '''
invariant "ASSERT_{hstate}_no_inmsg"
  (!isundefined(prevHomeNode) & prevHomeNode = {hstate} & 
   p_inmsg = false & 
   {home_state_expr} = {hstate_prime} & sent) ->
  cnt <= 1;
'''
dir_h_accept_trans_outmsg_dst_src_template = '''
invariant "ASSERT_{hstate}_accept_req_{mtype}"
  (!isundefined(prevHomeNode) & prevHomeNode = {hstate} & 
   !isundefined(prevRecProcMsg) & prevRecProcMsg = {mtype} & 
   {home_state_expr} = {hstate_prime} & sent) ->
   {is_src}(out_msg_dst = in_msg_src);
'''
dir_h_accept_trans_outmsg_dst_src_template_no_inmsg = '''
invariant "ASSERT_{hstate}_no_inmsg"
  (!isundefined(prevHomeNode) & prevHomeNode = {hstate} & 
   p_inmsg = false & 
   {home_state_expr} = {hstate_prime} & sent) ->
   {is_src}(out_msg_dst = in_msg_src);
'''
h_accept_trans_outmsg_dst_src_template = '''
invariant "ASSERT_{hstate}_accept_req_{mtype}"
  (!isundefined(prevHomeNode) & prevHomeNode = {hstate} & 
   !isundefined(prevRecProcMsg) & prevRecProcMsg = {mtype} & sent) ->
   {is_src}(out_msg_dst = in_msg_src);
'''
dir_h_accept_trans_outmsg_src_template = '''
invariant "ASSERT_{hstate}_accept_req_{mtype}"
  (!isundefined(prevHomeNode) & prevHomeNode = {hstate} & 
   !isundefined(prevRecProcMsg) & prevRecProcMsg = {mtype} & 
   {home_state_expr} = {hstate_prime} & sent) ->
   val_match;
'''
dir_h_accept_trans_outmsg_src_template_no_inmsg = '''
invariant "ASSERT_{hstate}_no_inmsg"
  (!isundefined(prevHomeNode) & prevHomeNode = {hstate} & 
   p_inmsg = false & 
   {home_state_expr} = {hstate_prime} & sent) ->
  val_match;
'''
h_accept_trans_outmsg_src_template = '''
invariant "ASSERT_{hstate}_accept_req_{mtype}"
  (!isundefined(prevHomeNode) & prevHomeNode = {hstate} & 
   !isundefined(prevRecProcMsg) & prevRecProcMsg = {mtype} & sent) ->
   val_match;
'''

# dir_h_accept_msg_cond = [
#   '!(!isundefined(prevHomeNode.{m_home_owner_field}) & prevRecProcMsg.{m_msg_src_field} = prevHomeNode.{m_home_owner_field});', 
#   '!(MultiSetCount(i:prevHomeNode.{m_home_sharer_field}, sv[i] = n) = 0)',
#   '!(MultiSetCount(i:prevHomeNode.{m_home_sharer_field}, sv[i] = n) != 0)',
# ]
dir_h_val_change_src_template = '''
invariant "{hstate}_accept_req_{mtype}"
  (!isundefined(prevHomeNode) & prevHomeNode = {hstate} & 
   !isundefined(prevRecProcMsg) & prevRecProcMsg = {mtype} & 
   {home_state_expr} = {hstate_prime}) ->
   ({home_cl_expr} = prevRecProcMsgVal);
'''
dir_h_val_change_src_mem_template = '''
invariant "{hstate}_accept_req_{mtype}"
  (!isundefined(prevHomeNode) & prevHomeNode = {hstate} & 
   !isundefined(prevRecProcMsg) & prevRecProcMsg = {mtype} & 
   {m_home_cur}.{m_home_state_field} = {hstate_prime}) ->
   ({m_home_cur}.{m_home_cl_field} = prevMainMem);
'''
dir_h_accept_trans_sharers_template_no_inmsg = '''
invariant "{hstate}_no_inmsg"
  (!isundefined(prevHomeNode) & prevHomeNode = {hstate} & 
  p_inmsg = false & 
   {home_state_expr} = {hstate_prime}) ->
   (forall m: {m_proc_iter_type} do 
    prev_sharer[m] = {m_home_sharer_func}
   endforall
   );
'''
dir_h_accept_trans_val_template_no_inmsg = '''
invariant "{hstate}_no_inmsg"
  (!isundefined(prevHomeNode) & prevHomeNode = {hstate} & 
    p_inmsg = false & 
   {home_state_expr} = {hstate_prime}) ->
   ({home_cl_expr} = prevHomeNodeVal);
'''
dir_h_accept_trans_val_template = '''
-- {hstate} receives/processes {mtype} and transition to {hstate_prime} and change value?
invariant "{hstate}_accept_req_{mtype}"
  (!isundefined(prevHomeNode) & prevHomeNode = {hstate} & 
   !isundefined(prevRecProcMsg) & prevRecProcMsg = {mtype} & 
   {home_state_expr} = {hstate_prime}) ->
   ({home_cl_expr} = prevHomeNodeVal);
'''

home_inmsg_notxn_val_template = '''
-- check {hstate} receives/processes {mtype} and has value change
invariant "{hstate}_accept_req_{mtype}"
  (!isundefined(prevHomeNode) & (prevHomeNode = {hstate}) & 
   !isundefined(prevRecProcMsg) & prevRecProcMsg = {mtype}) ->
   (prevHomeNodeVal = {m_home_cur}.{m_home_cl_field});
'''
dir_h_accept_trans_owner_template_no_inmsg = '''
invariant "{hstate}_no_inmsg"
  (!isundefined(prevHomeNode) & prevHomeNode = {hstate} & 
  p_inmsg = false & 
   {home_state_expr} = {hstate_prime}) ->
  !(
   (prevHomeNodeOnwerVld & {m_home_owner_vld_field} & {m_home_owner_expr} != prevHomeNodeOnwer) | 
    (prevHomeNodeOnwerVld != {m_home_owner_vld_field})); 
'''
dir_h_accept_trans_owner_template = '''
-- {hstate} receives/processes {mtype} and transition to {hstate_prime} and change?
invariant "{hstate}_accept_req_{mtype}"
  (!isundefined(prevHomeNode) & prevHomeNode = {hstate} & 
   !isundefined(prevRecProcMsg) & prevRecProcMsg = {mtype} & 
   {home_state_expr} = {hstate_prime}) ->
   !(
   (prevHomeNodeOnwerVld & {m_home_owner_vld_field} & {m_home_owner_expr} != prevHomeNodeOnwer) | 
    (prevHomeNodeOnwerVld != {m_home_owner_vld_field})); 
'''
dir_h_accept_trans_sharers_template = '''
-- {hstate} receives/processes {mtype} and transition to {hstate_prime} and change?
invariant "{hstate}_accept_req_{mtype}"
  (!isundefined(prevHomeNode) & prevHomeNode = {hstate} & 
   !isundefined(prevRecProcMsg) & prevRecProcMsg = {mtype} & 
   {home_state_expr} = {hstate_prime}) ->
   (forall m: {m_proc_iter_type} do 
    prev_sharer[m] = {m_home_sharer_func}
   endforall
   );
'''
dir_h_accept_trans_outmsg_template = '''
-- {hstate} receives/processes {mtype} and transition to {hstate_prime} and send out msg 
invariant "ASSERT_{hstate}_accept_req_{mtype}"
  (!isundefined(prevHomeNode) & prevHomeNode = {hstate} & 
   !isundefined(prevRecProcMsg) & prevRecProcMsg = {mtype} & 
   {m_home_cur}.{m_home_state_field} = {hstate_prime}) ->
   ({sent_msg_ss});
'''
dis_ele = "(MultisetCount(i:reached_set, reached_set[i] = {state}) = {inset}) & \n"
h_track_template = '''
-- Randomly select the request msg to track
rule "track_{hstate}_{mtype}"
  (!tracked & !IsUndefined(prevHomeNode) & prevHomeNode = {hstate} & 
  !IsUndefined(prevRecProcMsg) & prevRecProcMsg = {mtype}) ==>
  -- no need for book_keep() as this time stamp shouldn't perturb the state of
  -- the machine 
  start := true;
  tracked := true;
endrule;
'''
# home_inmsg_proc_template = '''
# invariant "{hstate}_accept_req_{mtype}"
#   -- can {hstate} ever snoops AND receive/process {mtype} message 
#   (!isundefined(prevHomeNode.state) & (prevHomeNode.state = {hstate}) & 
#    !isundefined(prevRecProcMsg[{m_home_iter}].{m_msg_type_field}) & prevRecProcMsg[{m_home_iter}].{m_msg_type_field} = {mtype}) ->
#   -- ! (receive and process)
#   !(prevHomeNode.state != HomeNode.state | !isundefined(prevSendMsg[{m_home_iter}].{m_msg_type_field})); 
# '''

dir_inmsg_txn_new_picl_template = '''
invariant "{hstate}_{mtype}_newpicl"
  -- can {hstate} receives {mtype} message and transition to new state
  (!isundefined(prevHomeNode) & prevHomeNode = {hstate} &
  isundefined(prevRecProcMsg) & prevRecProcMsg = {mtype}) ->
  prevHomeNode == {m_home_cur};
'''

home_inmsg_notxn_send_msg_template = '''
-- check {hstate} receives/processes {mtype} and sends out {out_mtype}?
invariant "{hstate}_accept_req_{mtype}"
  (!isundefined(prevHomeNode.state) & (prevHomeNode.state = {hstate}) & 
   !isundefined(prevRecProcMsg[{m_home_iter}].{m_msg_type_field}) & prevRecProcMsg[{m_home_iter}].{m_msg_type_field} = {mtype}) ->
   (isundefined(prevSendMsg[{m_home_iter}].mtype) | prevSendMsg[{m_home_iter}].mtype != {out_mtype});
'''
home_inmsg_notxn_snedmsg_val_template = '''
-- check {hstate} receives/processes {mtype} and sends out {out_mtype} with value same as {hstate} value?
invariant "{hstate}_accept_req_{mtype}"
  (!isundefined(prevHomeNode.state) & (prevHomeNode.state = {hstate}) & 
   !isundefined(prevRecProcMsg[{m_home_iter}].{m_msg_type_field}) & prevRecProcMsg[{m_home_iter}].{m_msg_type_field} = {mtype} & 
   !isundefined(prevSendMsg[{m_home_iter}].mtype) & prevSendMsg[{m_home_iter}].mtype = {out_mtype}) ->
   !(prevSendMsg[{m_home_iter}].{m_msg_cl_field} = prevHomeNode.{m_proc_cl_field});
'''

home_inmsg_notxn_snedmsg_dst_template = '''
-- check {hstate} receives/processes {mtype} and sends out {out_mtype} with dst same as inmsg.src?
invariant "{hstate}_accept_req_{mtype}"
  (!isundefined(prevHomeNode.state) & (prevHomeNode.state = {hstate}) & 
   !isundefined(prevRecProcMsg[{m_home_iter}].{m_msg_type_field}) & prevRecProcMsg[{m_home_iter}].{m_msg_type_field} = {mtype} & 
   !isundefined(prevSendMsg[{m_home_iter}].mtype) & prevSendMsg[{m_home_iter}].mtype = {out_mtype}) ->
   !(prevSendMsg[{m_home_iter}].dst = prevRecProcMsg[{m_home_iter}].src); 
'''
home_inmsg_notxn_val_eq_in_template = '''
-- check {hstate} receives/processes {mtype} and has value change
invariant "ASSERT_{hstate}_accept_req_{mtype}"
  (!isundefined(prevHomeNode.state) & (prevHomeNode.state = {hstate}) & 
   !isundefined(prevRecProcMsg[{m_home_iter}].{m_msg_type_field}) & prevRecProcMsg[{m_home_iter}].{m_msg_type_field} = {mtype}) ->
   (HomeNode.val = prevRecProcMsg[{m_home_iter}].val);
'''
home_inmsg_notxn_val_eq_mainmem_template = '''
-- check {hstate} receives/processes {mtype} and has value change
invariant "ASSERT_{hstate}_accept_req_{mtype}"
  (!isundefined(prevHomeNode.state) & (prevHomeNode.state = {hstate}) & 
   !isundefined(prevRecProcMsg[{m_home_iter}].{m_msg_type_field}) & prevRecProcMsg[{m_home_iter}].{m_msg_type_field} = {mtype}) ->
   (HomeNode.val = {main_mem});
'''
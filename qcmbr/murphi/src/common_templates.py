from gconst import *
from util import iter_msg_types_with_record
# msg set 
dis_ele_msgsent = \
"(MultisetCount(i:msg_sent_set, msg_sent_set[i].{m_msg_type_field} = {msgtype}) {pred}) & \n"
dis_ele_msgrec = \
"(MultisetCount(i:msg_rec_set, msg_rec_set[i].{m_msg_type_field} = {msgtype}) {pred}) & \n"
# msg set that is to/from directory ?
dis_ele_msgrec_src = \
"(MultisetCount(i:msg_rec_set, (msg_rec_set[i].{m_msg_type_field} = {msgtype}) & IsMember(msg_rec_set[i].{m_msg_src_field}, {m_home_node})) {pred}) & \n"

dis_ele_msgsend_dst = \
"(MultisetCount(i:msg_sent_set, (msg_sent_set[i].{m_msg_type_field} = {msgtype}) & IsMember(msg_sent_set[i].{m_msg_dst_field}, {m_home_node})) {pred}) & \n"
dis_ele_dst_undefined = \
"(MultisetCount(i:msg_sent_set, (msg_sent_set[i].{m_msg_type_field} = {msgtype}) & isundefined(msg_sent_set[i].{m_msg_dst_field})) {pred}) & \n"


msgset_rset_template = '''
invariant "{state}_{req}_rset_{idx}_{msgsetidx}"
(tracked & !start & {reachable_set} 
true) ->
!(
  {msg_set}
  true);
'''

msgset_rset_assertion_template = '''
invariant "ASSERT_{state}_{req}_rset_{idx}_{msgsetidx}"
(tracked & !start & {reachable_set} 
true) ->
(
  {msg_set}
  true);
'''

msgset_rset_type_template = '''
invariant "{state}_{req}_rset_{idx}_{msgsetidx}"
(tracked & !start & {reachable_set} 
{msg_set}
true) ->
!(
  {msg_src_dst}
  true);
'''

msgset_rset_type_template_assert = '''
invariant "ASSERT_{state}_{req}_rset_{idx}_{msgsetidx}"
(tracked & !start & {reachable_set} 
{msg_set}
true) ->
(
  {msg_src_dst}
  true);
'''

msgset_rset_assoc_check_assert = '''
invariant "ASSERT_{state}_{req}_rset_{idx}_{msgsetidx}"
(tracked & !start & {reachable_set} 
{msg_set}
true) ->
(
  {msg_state_map}
  true);
'''

# reachable set 
dis_ele = "(MultisetCount(i:reached_set, reached_set[i] = {state}) = {inset}) & \n"

# For tracking txn-initiating request 
track_h_template = '''
rule "track_hstate_{hstate}"
  (tracked & start & !isundefined(prevHomeNode) & prevHomeNode = {hstate}) ==> 
  start_h := true;
endrule;
'''
track_template = '''
-- Randomly select the request to track
rule "track_{state}_{req}"
  !tracked & !IsUndefined(prevProcs) & (prevProcs = {state}) & 
  !IsUndefined(prevProcReq.{m_req_type_field}) & (prevProcReq.{m_req_type_field} = {req}) ==>
  -- no need for book_keep() as this time stamp shouldn't perturb the state of
  -- the machine 
  start := true;
  tracked := true;
endrule;
'''
def track_template_ff(state, req, m_req_type_field, m_proc_state_field = None, isEntry = False, withTrackReq = False, msg = False, m_msg_type_field="", msg_s_cond="", msg_sent_set="msg_sent_set"):
  procstate = "prevProcs"
  if isEntry:
    assert(m_proc_state_field is not None)
    procstate = f"prevProcs.{m_proc_state_field}"
  track = ''
  if withTrackReq:
    track = '''trackReq := prevProcReq;
    trackReq.vld := true;  -- since the core may already return but still processing the txn...
    '''
  msg_s = ""
  
  if msg:
    msg_s = f"if (!isundefined(prevMsg)) then\n {msg_sent_set} [prevMsg] := true;\nendif\n"
  return f'''
  -- Randomly select the request to track
  rule "track_{state}_{req}"
    !tracked & !IsUndefined({procstate}) & ({procstate} = {state}) & 
    !IsUndefined(prevProcReq.{m_req_type_field}) & (prevProcReq.{m_req_type_field} = {req}) ==>
    -- no need for book_keep() as this time stamp shouldn't perturb the state of
    -- the machine 
    start := true;
    tracked := true;
    {track}
    {msg_s}
    {msg_s_cond}
  endrule;
  '''

def track_template_ff_multimsg(state, req, m_req_type_field, m_proc_state_field = None, isEntry = False, withTrackReq = False, msg = False, m_msg_type_field="", msg_s_cond="", msg_sent_set="msg_sent_set"):
  procstate = "prevProcs"
  if isEntry:
    assert(m_proc_state_field is not None)
    procstate = f"prevProcs.{m_proc_state_field}"
  track = ''
  if withTrackReq:
    track = '''trackReq := prevProcReq;
    trackReq.vld := true;  -- since the core may already return but still processing the txn...
    '''
  msg_s = ""

  if msg:
    msg_lines = []
    for _, msg_type in iter_msg_types_with_record():
      msg_lines.append(
        f"if (!isundefined(prevMsg_{msg_type})) then\n"
        f" {msg_sent_set}_{msg_type}[prevMsg_{msg_type}] := true;\n"
        "endif\n"
      )
    msg_s = "".join(msg_lines)
  return f'''
  -- Randomly select the request to track
  rule "track_{state}_{req}"
    !tracked & !IsUndefined({procstate}) & ({procstate} = {state}) & 
    !IsUndefined(prevProcReq.{m_req_type_field}) & (prevProcReq.{m_req_type_field} = {req}) ==>
    -- no need for book_keep() as this time stamp shouldn't perturb the state of
    -- the machine 
    start := true;
    tracked := true;
    {track}
    {msg_s}
    {msg_s_cond}
  endrule;
  '''
end_tracking_condition = "{m_proc_arr}[selc].{m_proc_state_field} = {state}"


req_val_eq_msg_template = '''
invariant "ASSERT_{state}_{req}_rset_{idx}_inmsg_for_{ss}"
(tracked & !start & {reachable_set}
 true) ->
(!isundefined (picl_val_src_msg[{ss}].{m_msg_type_field}) & 
  picl_val_src_msg[{ss}].{m_msg_type_field} = {tar_mtype});
'''

################################################################################
# s5
# Can the core send out {mtype} and snooped when the home is in {hstate}? 
# Not checking if its "receive and process" yet only check if initial state is
# even possible
# cover (when the core c1 send out the msg {mtype} (in prevSendMsg[selc]), meaning it should already be on the bus snoopable by others, can HOME be in {hstate})
home_hstate_template = '''
invariant "{hstate}_consistent_w_{mtype}"
  (tracked & !start & {reachable_set} 
  {msg_set}
    true) ->
isundefined(home_state_possible[{mtype}][{hstate}]);
'''

# Does home at {hstate} not take in {inMsg}? 
# cover (tracked & (start == false i.e., ends) & reached_some_set & 
#        during the entire txn time "from the point of core", can the home
#        at {hstate} receive and process message from all cores but the selected
#        symbolic core)
# cover (when HOME snoops the message {mtype}, does HOME ignores it without any action)
home_inmsg_no_accept_template = '''
invariant "{hstate}_accept_msg_{mtype}"
  (tracked & !start & {reachable_set} 
    {msg_set}
    true) ->
!(!isundefined(home_ignore_t[{hstate}][{mtype}]) & 
home_ignore_t[{hstate}][{mtype}]);
'''

home_inmsg_accept_template = '''
invariant "{hstate}_accept_msg_{mtype}"
  (tracked & !start & {reachable_set} 
    {msg_set}
    true) ->
!(!isundefined(home_accept_t[{hstate}][{mtype}]) & 
home_accept_t[{hstate}][{mtype}]);
'''

#track_template_home = '''
#-- Randomly select the request to track
#rule "track_{state}_{req}"
#  (tracked & !new_req -- we're targeting a particular request
#   !
#    )
#  !tracked_h & 
#  !tracked & !IsUndefined(prevProcs.{m_proc_state_field}) & (prevProcs.{m_proc_state_field} = {state}) & 
#  !IsUndefined(prevProcReq.{m_req_type_field}) & (prevProcReq.{m_req_type_field} = {req}) ==>
#  -- no need for book_keep() as this time stamp shouldn't perturb the state of
#  -- the machine 
#  start := true;
#  tracked := true;
#  trackReq := prevProcReq;
#  cur_idx := cur_idx + 1;
#endrule;
#'''
## TODO:
## end_tracking_condition_home = "{m_proc_arr}[selc].{m_proc_state_field} = {state}"



#  h reachable set
h_dis_outmsg_ele = "(MultisetCount(i:send_msg_h_set, send_msg_h_set[i].{m_msg_type_field} = {mtype}) = {qual}) & \n"
h_dis_ele = "(MultisetCount(i:reached_set_h, reached_set_h[i] = {state}) = {inset}) & \n"
h_rset_template = '''
invariant "{hstate}_accept_msg_{mtype}_{hrset_idx}"
  (tracked & !start & tracked_h & !start_h & 
    {reachable_set} 
    {msg_set}
    (!isundefined(home_accept_t[{hstate}][{mtype}]) & 
    home_accept_t[{hstate}][{mtype}]) &
  true) ->
  !(
    {hrset}
  true);
'''

h_track_template = '''
-- Randomly select the request to track
rule "track_{hstate}_{mtype}"
  ( tracked & !new_req & 
    !tracked_h & 
    (!isundefined(prevHomeNode.state) & (prevHomeNode.state = {hstate}) & 
      !isundefined(prevRecProcMsg[{m_home_iter}].{m_msg_type_field}) & prevRecProcMsg[{m_home_iter}].{m_msg_type_field} = {mtype} & prevRecProcMsg[{m_home_iter}].{m_msg_src_field} = selc)) ==>
  start_h := true;
  tracked_h := true;
  proc_h := (prevHomeNode.state != HomeNode.state) | !isundefined(prevSendMsg[HomeType].mtype);
endrule;
'''
# h_end_tracking_condition = "{m_proc_arr}[selc].{m_proc_state_field} = {state}"





################################################################################
# DEPR
################################################################################
# cover (reachable_set && defined && prevHState == {state} && defined && preProcMsg.src = selc &&
# preProcMsg.type = {mtype})
# assert (defined && prevHState == {state} && defined && preProcMsg.src = selc
# -> not (preProcMsg.type = {mtype})
-- With value specified for store to prepare for CI
-- FVT: Instrumented with tracking variables already

-- Two-state snoop-based VI protocol
--   core <-> cc <-> data cache (write back)
--          ↕
--        shared bus: a shared set of wires on which a core issue a message
--        and have it observed by all cores and the LLC/memory
--          ↕
--    memory controller <-> LLC
--          ↕
--      main memory
-- * Primer p. 132: "Figure 7.8 illustrates the operation of an atomic bus.
-- Because a coherence transaction occupies the bus until the response
-- completes, an atomic bus trivially implements atomic transactions."
-- * ````Primer p. 113: "Atomic Request": coherence requests is ordered in the
-- same cycle that it is issued.''''
-- * Primer p. 113: "Atomic Transactions": A subsequent request for the same
-- block may not appear on the bus until after the first coherence transaction
-- completes."
-- * The "bus" implementation is such that  (instead of -- `eecs570_twostate_bus_naive.m` lockstep):
-- a) A message stays in gbuf until all nodes sees the message (and transitions)
-- b) Each node has a buf that holds the message to be sent
-- c) For each node, if there is a message in gbuf prioritize to process it
---  (otherwise other request from core, say evict, may send more messages..)
-- d) A message is delivered when its dequeue from a local node's buf to gbuf
-- * eecs570_sampel/twostate.m use additional transient state to handle this
----------------------------------------------------------------------
-- Constants
----------------------------------------------------------------------
const
  ProcCount: 3;          -- number processors
  ValueCount:   2;       -- number of data values.
  -- NetMax: ProcCount+1;   -- Proc and LLC/MemoryController
  HopCount: 2;

----------------------------------------------------------------------
-- Types
----------------------------------------------------------------------
type
  -- <typedecl> :: <ID> : <typeExpr>
  Proc: scalarset(ProcCount);   -- unordered range of processors
  Value: scalarset(ValueCount); -- arbitrary values for tracking coherence
  Home: enum { HomeType };      -- MemoryController, need enumeration for IsMember calls
  Node: union { Home , Proc };

  CurReq: record 
    val: Value;
    tp: enum {store, load, evict}; 
    vld: boolean; 
  end;

  MessageType: enum {  
    GetMsg,
    PutMsg,
    DataRespMsg
    };

  Message:
    Record
      mtype: MessageType;
      src: Node;
      dst: Node;
      -- Bus-based everyone snoop the message
      val: Value;
    End;

  -- Memory Controller <-> LLC 
  HomeStateEnum: enum { H_I, H_V };
  HomeState:
    Record
      state: HomeStateEnum;
      val: Value; 
    End;

  ProcStateEnum: enum { P_I, P_IVD, P_V};

  ProcState:
    Record
      state: ProcStateEnum;
      val: Value;
    End;
  

----------------------------------------------------------------------
-- Variables
----------------------------------------------------------------------
-- CI { 
CoreReq: record
  cl: Value;
  vld: boolean;
  tp: enum {ci_store, ci_load, ci_evict}; 
end;
-- * vld = true,  tp determines the type
-- * The coherence protocol should mark vld as false when finishing a store 
-- * The read is poppsed (marked invalid) only if the coherence protocol return
-- values (i.e., `.cl` is no longer undefined)
-- } CI
myarrtype : array [MessageType] of boolean;
myarrtype2 : array [HomeStateEnum] of boolean;

var
  -- <vardecl> ::= <ID>: <typeExpr>
  HomeNode:  HomeState;                     -- a previously defined type
  Procs: array [Proc] of ProcState;

  LastWrite: Value; -- FVT, Used to confirm that writes are not lost; this variable would not exist in real hardware
  -- Main Memory
  MainMemory: Value; -- Value in main memory

  -- message delivery
  -- until everyone sees it and someone process the message
  gBuf: Message;                   -- bus current 
  ackBus: array [Node] of boolean;
  msgBuf: array [Node] of Message; -- response 
  msgBufNonEmpty: Boolean;
  -- [ ] defined(gBuf) |-> at most one message in the msgBuf
  -- [ ] undefined(gBuf) |-> may fetch from the msgBuf
  -- [ ] Requests are issued directly to the gBuf (only when gBuf is undefined
  -- and msgBuf is empty)
  -- -> wait for the gBuf and msgBuf to be empty
  -- [ ] defined(gBuf) and defined(nMsg) may also be (req there and resp made
  -- but to it waits until all people sees it/obsereve it)
  -- * Assume real bus persist the message until all cores sets input wires of ack
  -- to high before getting next message onto the bus from some arbiter that
  -- choose someone's message
  -- * A core should read the message on the bus (if there exists) before it can
  -- issue anything at all to the bus
  
  curRequsts: array [Proc] of CurReq;

  -- FVT {
  -- The request that the randomly selected processor is currently processing
  trackReq: CoreReq;
  prevProcReq: CoreReq; 
  prevProcReq_2: CoreReq; 
  prevProcs: ProcState;
  prevProcs_2: ProcState;
  prevHomeNode: HomeState;

  -- Assume at any given time, a core/directory send/receive at most one msg 
  prevSendMsg: array [Node] of Message;
  prevRecProcMsg: array [Node] of Message;

  
  selc: Proc;

  start: boolean;
  tracked: boolean;
  new_req: boolean; 
  -- total number of states for cache controller
  reached_set: multiset [3] of ProcStateEnum;
  reached_set_val_change: array [ProcStateEnum] of boolean;
  reached_set_val_match: array [ProcStateEnum] of boolean;
  picl_val_src_msg: array [ProcStateEnum] of Message; 
  reached_set_order: array [ProcStateEnum] of 0..3;
  cur_idx: 0..5; -- for ordeirng 
  

  -- all messages sent from the Proc[selc] during a transaction
  msg_sent_set: multiset [3] of Message;
  msg_sent_concurrent_state: array [MessageType] of ProcStateEnum;

  -- all messages received and processed by the Proc[selc] during a
  -- transaction
  msg_rec_set: multiset [3] of Message;
  msg_rec_concurrent_state: array [MessageType] of ProcStateEnum;

  -- home 

  reached_set_h: multiset [3] of HomeStateEnum;
  send_msg_h_set: multiset [3] of Message;
  start_h: boolean;
  proc_h: boolean;
  tracked_h: boolean;

  -- } FVT
----------------------------------------------------------------------
-- Procedures
----------------------------------------------------------------------
-- CI { 
-- The 1-entry buffer has the following behavior: At any given time point, if
-- tagged invalid, an entry/request can be non-deterministically get allocated. 
-- A load is popped from the buffer only if the value is returned.
  req_pending: array[Proc] of CoreReq;
-- } CI
Procedure send_req(mtype:MessageType;
  src:Node;
  dst:Node;
  val:Value;
);
Begin
  assert (IsUndefined(gBuf.src)) "??";
  assert (!msgBufNonEmpty) "??? still response";

  gBuf.mtype := mtype;
  gBuf.src   := src;
  gBuf.dst   := dst;
  gBuf.val   := val;
  for n:Node do
    ackBus[n] := false;
  endfor;
  -- FVT {
  prevSendMsg[src] := gBuf;
  -- }
  -- FVT_G_CHK
  -- assert (!isundefined(gBuf.src)) "source is undefined?";  -- proven true
  -- assert (!isundefined(gBuf.dst)) "dst is undefined?"; -- disproven
End;

Procedure send_resp(
  mtype:MessageType;
  src:Node;
  dst:Node;
  val:Value;
);
var msg:Message;
Begin
  assert (!msgBufNonEmpty) "??? still response";
  assert (!IsUndefined(gBuf.src)) "? no txn?";
  msg.mtype := mtype;
  msg.src   := src;
  msg.dst   := dst;
  msg.val   := val;
  msgBuf[src] := msg;
  msgBufNonEmpty := true;

  -- FVT { 
  prevSendMsg[src] := msg;
  -- }
End;

Procedure HomeReceive(msg:Message);
Begin
  switch HomeNode.state
  case H_I:
    switch msg.mtype
    case GetMsg:
      -- Send data block in DataResp message to requstor and transition to V
      HomeNode.state := H_V;
      HomeNode.val := MainMemory; -- we got from the MainMemory
      send_resp(DataRespMsg, HomeType, msg.src, HomeNode.val);
    else
      error "Unhandled message type!"; 
      -- shouldn't have dataresp or putmsg on the bus 
    endswitch;

  case H_V:
    switch msg.mtype
    case PutMsg:
      HomeNode.state := H_I;
      HomeNode.val := msg.val;
      MainMemory := msg.val;
      -- Send(DataRespMsg, msg.src, HomeType, VC1, UNDEFINED);
    -- case GetMsg:
    --   HomeNode.state := H_V;
    --   -- no action
    -- case DataRespMsg:
    --   -- ignore although could see on the bus 
    --   HomeNode.state := H_V;
    endswitch;
  endswitch; -- switch HomeNode.state
End; -- Procedure HomeReceive


Procedure ProcReceive(msg:Message; p:Proc);
Begin
  alias ps:Procs[p].state do
  alias pv:Procs[p].val do

  switch ps
  case P_I:
    if msg.mtype = GetMsg then
      assert (msg.src != p) "Huh?";
    endif
  --   switch msg.mtype
  --   -- case GetMsg: Ignored
  --   -- case PutMsg: 
  --   endswitch;

  case P_IVD:
    switch msg.mtype
    case DataRespMsg:
      assert (msg.dst = p) "Huh not for me?";
      if (!isundefined(curRequsts[p].vld) & 
        curRequsts[p].vld & curRequsts[p].tp = store ) then
        curRequsts[p].vld := false;
        LastWrite := pv; 
      else 
        pv := msg.val;
      endif;
      ps := P_V;
    case GetMsg:
      assert (msg.src = p) "not from me?";
    else 
      error "Huh?? I'm in active transaction?";
    endswitch;

  case P_V:
    switch msg.mtype
    case GetMsg:
      send_resp(DataRespMsg, p, msg.src, pv);
      ps := P_I;
    else
      error "Huh? I hold it";
		endswitch;
  endswitch;
  endalias;
  endalias;
End; -- Procedure ProcReceive


----------------------------------------------------------------------
----------------------------------------------------------------------
-- FVT
----------------------------------------------------------------------
-- Book keeping variables that is right when a rule is fired 
-- update and reset (i.e., the precondition is true and before executing the
-- postcondition)

function mycmp (var m1: Message; var m2: Message): boolean;
begin
  return m1.mtype = m2.mtype & m1.src = m2.src & m1.dst = m2.dst & m1.val = m2.val;
end;
procedure book_keep();
begin
  -- ****Before a rule is applied and update the variables****
  -- starting from the request arrives at the core until the next imeediate
  -- request that initiate transaction for core c again
  -- new_req := false;

  if (tracked & !start) then
    if (!isundefined(prevSendMsg[selc].mtype) & 
        (prevSendMsg[selc].mtype = GetMsg | prevSendMsg[selc].mtype = PutMsg ) -- request 
    ) then
      new_req := true;
    endif
  endif;

  if (start_h) then
    if (!(HomeNode.state = H_I | HomeNode.state = H_V)) then
      if (prevHomeNode.state != HomeNode.state) then
        multisetadd(HomeNode.state, reached_set_h);
        -- reached_set_order[Procs[selc].state] := cur_idx;
        -- cur_idx := cur_idx + 1;
        assert (multisetcount(i:reached_set_h, reached_set_h[i] = HomeNode.state) < 2) "non-consecutive re-visits???";
      endif;
    else
      -- end the tracking as it has reached the stable state (i.e., those that
      -- can take in requests message types
      if (multisetcount(i:reached_set_h, reached_set_h[i] = HomeNode.state) = 0) then
      --   -- register this last state for ending this transaction
        multisetadd(HomeNode.state, reached_set_h);
      else
        assert false "home end state exists?";
      endif;
      start_h := false;
    endif;
    
    if (!isundefined(prevSendMsg[HomeType].mtype)) then
      multisetadd(prevSendMsg[HomeType], send_msg_h_set);
    endif;

  endif;
  -- Procs[selc] is sync with prevSendMsg 
  -- predRecProcMsg is sync with prevProcs.state
  -- prevRecProcMsg is sync with prevHomeNode.state
  -- If start is true, we collect the Procs[selc]'s current state if this
  -- current state that the rule is applying to is not a stalbe state
  if (start) then
    -- Since start is True, it is for sure if from selc then its the request we're currently tracking.  

    -- defined only means that the node observes the message (but not
    -- necessarily recieve, i.e., process, the message)

    if (!isundefined(prevSendMsg[selc].mtype)) then
      assert(prevSendMsg[selc].src = selc) "huh wrong src mssg???";
      multisetadd(prevSendMsg[selc], msg_sent_set);
      if (!isundefined(msg_sent_concurrent_state[prevSendMsg[selc].mtype])) then
        assert (msg_sent_concurrent_state[prevSendMsg[selc].mtype] = Procs[selc].state) "diff state associated??"; 
      endif;
      msg_sent_concurrent_state[prevSendMsg[selc].mtype] := Procs[selc].state; 
    endif;

    if (!isundefined(prevRecProcMsg[selc].mtype)) then
      -- TODO: since, in snooping based, all core may receive and see all
      -- messages, but not necessarily "process it", we here constrain  
      -- TODO: Maybe not necessarily change state but at least some action????? 
      if ((prevProcs.state != Procs[selc].state) | 
        (!isundefined(prevRecProcMsg[selc].dst) & (prevRecProcMsg[selc].dst = selc)) 
        ) then
        multisetadd(prevRecProcMsg[selc], msg_rec_set);
        if (!isundefined(msg_rec_concurrent_state[prevRecProcMsg[selc].mtype])) then
          assert (msg_rec_concurrent_state[prevRecProcMsg[selc].mtype] = prevProcs.state) "diff state associated??"; 
        endif;
        msg_rec_concurrent_state[prevRecProcMsg[selc].mtype] := prevProcs.state; 
        if (isundefined(picl_val_src_msg[Procs[selc].state].mtype)) then 
          if (Procs[selc].val = prevRecProcMsg[selc].val) then
            picl_val_src_msg[Procs[selc].state] := prevRecProcMsg[selc]; -- true;
          else 
            undefine picl_val_src_msg[Procs[selc].state];
          endif;
        else 
          --if ((Procs[selc].val = prevRecProcMsg[selc].val) !=  picl_val_src_msg[Procs[selc].state]) then 
          if (mycmp(prevRecProcMsg[selc], picl_val_src_msg[Procs[selc].state])) then 
            undefine picl_val_src_msg[Procs[selc].state];
          endif;
        endif;
      endif;
    endif;
    
    if (!(Procs[selc].state = P_I | Procs[selc].state = P_V)) then
      if (prevProcs.state != Procs[selc].state) then
        if (prevProcs.val != Procs[selc].val) then
          reached_set_val_change[Procs[selc].state] := true;
        endif;
        if (Procs[selc].val = trackReq.cl) then
          reached_set_val_match[Procs[selc].state] := true;
        endif;
        MultisetAdd(Procs[selc].state, reached_set);
        reached_set_order[Procs[selc].state] := cur_idx;
        cur_idx := cur_idx + 1;
        assert (multisetcount(i:reached_set, reached_set[i] = Procs[selc].state) < 2) "non-consecutive re-visits???";
      endif;
    else
      -- end the tracking as it has reached the stable state (i.e., those that
      -- can take in requests
      if (multisetcount(i:reached_set, reached_set[i] = Procs[selc].state) = 0) then
      ----   -- register this last state for ending this transaction
        if (prevProcs.val != Procs[selc].val) then
          reached_set_val_change[Procs[selc].state] := true;
        endif;
        if (Procs[selc].val = trackReq.cl) then
          reached_set_val_match[Procs[selc].state] := true;
        endif;
        MultisetAdd(Procs[selc].state, reached_set);
        reached_set_order[Procs[selc].state] := cur_idx;
        cur_idx := cur_idx + 1;
      else
        assert false "end state exists?";
      endif;
      start := false;
    endif;
  endif;

  if (start_h) then 
    if (!(HomeNode.state = H_I | HomeNode.state = H_V )) then
      -- home node in transient state
      if (prevHomeNode.state != prevHomeNode.state) then 
        multisetadd(HomeNode.state, reached_set_h);
      endif;
    else 
      -- home node in stable state those that can initiate requests
      if (multisetcount(i:reached_set_h, reached_set_h[i] = HomeNode.state) = 0) then
        multisetadd(HomeNode.state, reached_set_h);
      else 
        assert false "the end state already exists????????";
      endif;
      start_h := false;
    endif;
  endif;

  prevProcs_2 := prevProcs;
  prevProcs := Procs[selc];    -- other data are assoc. w/ this prevState
  -- prevProcs is assoc. w/ the prevProcReq that may be updated after a rule
  -- fires
  prevHomeNode := HomeNode;
  prevProcReq_2 := prevProcReq;
  undefine prevProcReq;
  prevProcReq.vld := true; -- FVT

  -- this is executed right before the rule is applied (which may change the
  -- state) and therefore the message get sent or received is associated with
  -- the current state that is about to apply rule and change
  undefine prevSendMsg;
  undefine prevRecProcMsg;

end;
-- Rules
----------------------------------------------------------------------


-- Processor actions (affecting coherency)

function has_read(var v: CoreReq): boolean;
begin
    return v.vld & (v.tp = ci_load) & isundefined(v.cl);
end;
function has_write(var v: CoreReq): boolean;
begin
    return v.vld &  (v.tp = ci_store);
end;

procedure resp_read(var v: CoreReq; var ret_val: Value);
begin
  assert (isundefined(v.cl)) "?";
  v.cl := ret_val; 
end;
procedure resp_store(var v: CoreReq);
begin
  v.vld := false;
end;
ruleset n:Proc Do
  alias p:Procs[n] Do

  
alias creq: req_pending[n] do
rule "load_P_I"
    -- only if previous transaction is done 
    (p.state = P_I) & !msgBufNonEmpty & IsUndefined(gBuf.src) 
    
& has_read(creq) -- CI"
==>
      book_keep(); -- FVT
      if (n = selc) then
        prevProcReq.tp:= ci_load; -- FVT
        prevProcReq.cl:= UNDEFINED; -- FVT
        prevProcReq.vld := true; -- FVT
      endif;
 

      send_req (GetMsg, n, UNDEFINED, UNDEFINED);
      p.state := P_IVD;


  
endrule; 
endalias;


	ruleset v:Value Do
    
alias creq: req_pending[n] do
rule "store_P_I"
      -- only if previous transaction is done 
      (p.state = P_I) & !msgBufNonEmpty & IsUndefined(gBuf.src) 
      
& has_write(creq) & creq.cl = v -- CI"
==>

          book_keep(); -- FVT
        if (n = selc) then
          prevProcReq.tp := ci_store; -- FVT
          prevProcReq.cl := v; -- FVT
          prevProcReq.vld := true; -- FVT
        endif;
 
        curRequsts[n].vld := true;
        curRequsts[n].tp := store;
        send_req (GetMsg, n, UNDEFINED, UNDEFINED);
        p.state := P_IVD;
        p.val := v; 
    
endrule; 
endalias;

  endruleset;

  -- P_IVD: stall all other requests 

  
alias creq: req_pending[n] do
rule "load_P_V"
    (p.state = P_V)
    
& has_read(creq) -- CI"
==>
      book_keep(); -- FVT
      if (n = selc) then
        prevProcReq.tp := ci_load; -- FVT
        prevProcReq.cl := UNDEFINED; -- FVT
        prevProcReq.vld := true; -- FVT
      endif;
resp_read(creq, p.val); -- CI


      p.state := P_V;

  
endrule; 
endalias;


	ruleset v:Value Do
    
alias creq: req_pending[n] do
rule "store_P_V"
   	  (p.state = P_V)
    	
& has_write(creq) & creq.cl = v -- CI"
==>
        book_keep(); -- FVT
        if (n = selc) then
          prevProcReq.tp := ci_store; -- FVT
          prevProcReq.cl := v; -- FVT
          prevProcReq.vld := true; -- FVT
        endif;


 		    p.val := v;      
 		    LastWrite := v;  --We use LastWrite to sanity check that reads receive the value of the last write

  	
endrule; 
endalias;

	endruleset;

  rule "evict_P_V"
    -- only if previous transaction is done 
    (p.state = P_V) & !msgBufNonEmpty & IsUndefined(gBuf.src) 
    ==> 
      book_keep(); -- FVT
      if (n = selc) then
        prevProcReq.tp := ci_evict; -- FVT
        prevProcReq.cl := UNDEFINED; -- FVT
        prevProcReq.vld := true; -- FVT
      endif;

      send_req (PutMsg, n, HomeType, p.val);
      p.state := P_I;

  endrule;

  endalias;
endruleset;

-- Message delivery rules
ruleset n:Node Do
  rule "receiveFromBus"
    !IsUndefined(gBuf.src) & !ackBus[n] ==>
    begin
      book_keep(); -- FVT
      -- FVT
      prevRecProcMsg[n] := gBuf;
      ackBus[n] := true;
      if IsMember(n, Home) then
        HomeReceive(gBuf);
      else
        ProcReceive(gBuf, n);
      endif;
  endrule;
endruleset;

rule "bus_atomic_req"
  !IsUndefined(gBuf.src) ==>
  var allAck: boolean;
  var nMsg: Message;
  begin
    book_keep(); -- FVT
    undefine nMsg;
    allAck := true;
    for n: Node do
      allAck := allAck & ackBus[n];
    endfor;
    if allAck then
      for n: Node do
        ackBus[n] := false;
      endfor;
      undefine gBuf;
      if msgBufNonEmpty then
        for n: Node do
          if !IsUndefined(msgBuf[n].src) then
            assert (IsUndefined(nMsg.src)) "there should exist some active txn?";
            nMsg := msgBuf[n];
            undefine msgBuf[n];
            msgBufNonEmpty := false;
          endif
        endfor;
        -- 
        gBuf := nMsg;
        assert (!IsUndefined(gBuf.src)) "should be completing...";
      endif;
    endif;
endrule;

----------------------------------------------------------------------
-- Startstate
----------------------------------------------------------------------

-- CI {
-- 1-entry buffer getting requests and popping request 
ruleset m:Proc do
  ruleset v: Value do
  rule "core_issue_write_nondeterm"
    !req_pending[m].vld ==> 
    req_pending[m].cl := v;
    req_pending[m].vld := true; 
    req_pending[m].tp := ci_store;
  endrule;
  endruleset;

  rule "core_issue_read_nondeterm"
    !req_pending[m].vld ==> 
    undefine req_pending[m].cl;
    req_pending[m].vld := true; 
    req_pending[m].tp := ci_load;
  endrule;

  rule "core_pop_read"
    req_pending[m].vld & 
    req_pending[m].tp = ci_load & 
    !isundefined (req_pending[m].cl)
    ==> 
    req_pending[m].vld := false;
  endrule;
endruleset;
-- } CI 
startstate

  undefine curRequsts;
  -- home node initialization
  HomeNode.state := H_I;
	for v:Value do
    MainMemory := v;
  endfor;
  
	LastWrite := MainMemory;
  -- processor initialization
  for i:Proc do
    Procs[i].state := P_I;
    undefine Procs[i].val;
  endfor;

  -- network initialization
  undefine gBuf;
  for n:Node do
    ackBus[n] := false;
  endfor;
  undefine msgBuf;
  msgBufNonEmpty := false;

  -- FVT
  undefine prevProcReq;
  undefine prevProcs;
  undefine prevProcReq_2;
  undefine prevProcs_2;
  undefine prevHomeNode;

  undefine prevSendMsg;
  undefine prevRecProcMsg;

  start := false;
  tracked := false;

  for n: Proc do
    selc := n;
  endfor;
  cur_idx := 0;
  for j: ProcStateEnum do
    reached_set_val_change [j] := false;
    reached_set_val_match [j] := false;
    reached_set_order [j] := 0;
  endfor;

  undefine msg_sent_set;
  undefine msg_sent_concurrent_state;
  undefine msg_rec_set;
  undefine msg_rec_concurrent_state;

  new_req := false;
  undefine reached_set_h;
  undefine send_msg_h_set;
  tracked_h := false;
  start_h := false;
  proc_h := false;
  -- }

  -- CI {
  undefine req_pending; 
  for i:Proc do
    req_pending[i].vld := false;                            
  endfor;
  -- } CI

endstartstate;


----------------------------------------------------------------------
-- Invariants
----------------------------------------------------------------------

invariant "Invalid implies empty owner"
  (HomeNode.state = H_I) ->
  (forall n: Proc do
    !(Procs[n].state = P_V)
   endforall);

invariant "value in memory matches value of last write, when invalid"
  (HomeNode.state = H_I) ->
  (MainMemory = LastWrite);
 
invariant "values in valid state match last write"
 forall n : Proc Do
   (Procs[n].state = P_V) ->
   (Procs[n].val = LastWrite)
 endforall;

invariant "swmr"
  forall c1: Proc do
  forall c2: Proc do
  ( c1 != c2
  & Procs[c1].state = P_V) 
  ->
  ( Procs[c2].state != P_V )
  endforall
  endforall;



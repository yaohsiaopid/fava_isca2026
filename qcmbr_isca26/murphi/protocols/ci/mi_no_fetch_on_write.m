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
  HomeState:
    Record
      state: enum { H_I, H_V };
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


 		    p.val := v;      
 		    LastWrite := v;  --We use LastWrite to sanity check that reads receive the value of the last write

  	
endrule; 
endalias;

	endruleset;

  rule "evict_P_V"
    -- only if previous transaction is done 
    (p.state = P_V) & !msgBufNonEmpty & IsUndefined(gBuf.src) 
    ==> 

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



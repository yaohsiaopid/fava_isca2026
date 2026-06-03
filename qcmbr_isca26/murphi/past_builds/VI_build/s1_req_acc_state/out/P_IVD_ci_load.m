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
--------------------------------------------------------------------------------
-- Return of load: `RETLD,CL`
-- Getting requests: get_evict_req, get_store_req, get_load_req
-- Sending/Receiving could be both after/before transition of states upon the inspection of message type 
-- - `-- #SENDING,<var_name>` 
-- - `-- #RECEIVING,<var_name>`
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
var
prevProcs: ProcStateEnum;
prevProcReq: CoreReq;
selc: Proc;


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
procedure book_keep(m: Node);

begin

prevProcs := Procs[selc].state;
undefine prevProcReq;
end;
-- Procedures
----------------------------------------------------------------------


procedure get_evict_req(m:Proc); 
begin

if (m = selc) then
  prevProcReq.tp:= ci_evict; 
  prevProcReq.cl:= undefined; 
  prevProcReq.vld := true;
endif;
  -- if (m = selc) then
  --   prevProcReq.tp:= ci_evict; 
  --   prevProcReq.cl:= undefined; 
  --   prevProcReq.vld := false; -- we assume replacemenet returns immediately
  -- endif;
end;
procedure get_store_req(m:Proc; cl:Value);
begin

if (m = selc) then
  prevProcReq.tp:= ci_store; 
  prevProcReq.cl:= cl; 
  prevProcReq.vld := true; 
endif;
  -- if (m = selc) then
  --   prevProcReq.tp:= ci_store; 
  --   prevProcReq.cl:= cl; 
  --   prevProcReq.vld := true; 
  -- endif;
end;
procedure get_load_req(m:Proc);
begin

if (m = selc) then
  prevProcReq.tp:= ci_load; 
  prevProcReq.cl:= undefined; 
  prevProcReq.vld := true; 
endif;
  -- if (m = selc) then
  --   prevProcReq.tp:= ci_load; 
  --   prevProcReq.cl:= UNDEFINED; 
  --   prevProcReq.vld := true; 
  -- endif;
end;
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
  -- #SENDING,gBuf
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
  -- #SENDING,msg
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
        -- #RETLD,CL
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

ruleset n:Proc Do
  alias p:Procs[n] Do

  rule "load_P_I"
    -- only if previous transaction is done 
    (p.state = P_I) & !msgBufNonEmpty & IsUndefined(gBuf.src) 
    ==>
 book_keep(n);
 
      get_load_req(n);
      send_req (GetMsg, n, UNDEFINED, UNDEFINED);
      p.state := P_IVD;


  endrule;

	ruleset v:Value Do
    rule "store_P_I"
      -- only if previous transaction is done 
      (p.state = P_I) & !msgBufNonEmpty & IsUndefined(gBuf.src) 
      ==>
 book_keep(n);
 
        get_store_req(n, v);
        curRequsts[n].vld := true;
        curRequsts[n].tp := store;
        send_req (GetMsg, n, UNDEFINED, UNDEFINED);
        p.state := P_IVD;
        p.val := v; 
    endrule;
  endruleset;

  -- P_IVD: stall all other requests 

  rule "load_P_V"
    (p.state = P_V)
    ==>
 book_keep(n);

      get_load_req(n);
      -- #RETLD,CL
      p.state := P_V;

  endrule;

	ruleset v:Value Do
    rule "store_P_V"
   	  (p.state = P_V)
    	==>
 book_keep(n);


        get_store_req(n, v);
 		    p.val := v;      
 		    LastWrite := v;  --We use LastWrite to sanity check that reads receive the value of the last write

  	endrule;
	endruleset;

  rule "evict_P_V"
    -- only if previous transaction is done 
    (p.state = P_V) & !msgBufNonEmpty & IsUndefined(gBuf.src) 
    ==>
 book_keep(n);
 
      get_evict_req(n);
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

 book_keep(n);
      ackBus[n] := true;
      if IsMember(n, Home) then
        -- #RECEIVING,gBuf
        HomeReceive(gBuf);
      else
        -- #RECEIVING,gBuf
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
            -- #?SENDING? from nMsg.src?
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




undefine prevProcReq;
for n : Proc do
 selc := n;
 endfor;
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



invariant "P_IVD_accept_req_ci_load"
  (!IsUndefined(prevProcs) & (prevProcs = P_IVD)) ->
(IsUndefined(prevProcReq.tp) | (prevProcReq.tp != ci_load));

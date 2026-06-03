-- no tracking request variables; ONLY THE PREVPROC variable
-- python3 ProtoGen.py /cafe/u/yaohsiao/sandbox/murphi_playground/ProtoGen/MSI_Proto.pcc   
-- No fetch-on-miss
const
  ENABLE_QS: false;  VAL_COUNT: 2;
  ADR_COUNT: 1;

  O_NET_MAX: 4;
  U_NET_MAX: 4;

  NrCaches: 3;


type
Access: enum {
  none,
  load,
  store
};

MessageType: enum { 
  Fwd_GetM,
  Fwd_GetS,
  GetM,
  GetM_Ack_AD,
  GetM_Ack_D,
  GetS,
  GetS_Ack,
  Inv,
  Inv_Ack,
  PutM,
  PutS,
  Put_Ack,
  Upgrade,
  WB
};


s_cache: enum { 
  cache_I,
  cache_I_load,
  cache_I_load__Inv_I,
  cache_I_store,
  cache_I_store_GetM_Ack_AD,
  cache_I_store_GetM_Ack_AD__Fwd_GetM_I,
  cache_I_store_GetM_Ack_AD__Fwd_GetS_S,
  cache_I_store_GetM_Ack_AD__Fwd_GetS_S__Inv_I,
  cache_I_store__Fwd_GetM_I,
  cache_I_store__Fwd_GetS_S,
  cache_I_store__Fwd_GetS_S__Inv_I,
  cache_M,
  cache_M_evict,
  cache_M_evict_Fwd_GetM,
  cache_S,
  cache_S_evict,
  cache_S_store,
  cache_S_store_GetM_Ack_AD,
  cache_S_store_GetM_Ack_AD__Fwd_GetS_S,
  cache_S_store__Fwd_GetS_S
};


s_directory: enum { 
  directory_I,
  directory_M,
  directory_M_GetS,
  directory_S
};


Address: scalarset(ADR_COUNT);
ClValue: scalarset(VAL_COUNT);

OBJSET_cache: scalarset(NrCaches);

OBJSET_directory: enum{directory};

Machines: union{OBJSET_cache, OBJSET_directory};

v_NrCaches_OBJSET_cache: multiset[NrCaches] of OBJSET_cache;
cnt_v_NrCaches_OBJSET_cache: 0..NrCaches;

Message: record
  adr: Address;
  mtype: MessageType;
  src: Machines;
  dst: Machines;
  acksExpected: 0..NrCaches;
  cl: ClValue;
end;


FIFO: record
  Queue: array[0..1] of Message;
  QueueInd: 0..1+1;
end;


Buffer: record
  Queue: array[0..2] of Message;
  QueueInd: 0..2+1;
end;

ENTRY_cache: record
  State: s_cache;
  Defermsg: Buffer;
  Perm: Access;
  cl: ClValue;
  acksReceived: 0..NrCaches;
  acksExpected: 0..NrCaches;
end;

ENTRY_directory: record
  State: s_directory;
  Defermsg: Buffer;
  Perm: Access;
  cl: ClValue;
  cache: v_NrCaches_OBJSET_cache;
  owner: Machines;
end;

MACH_cache: record
  CL: array[Address] of ENTRY_cache;
end;

MACH_directory: record
  CL: array[Address] of ENTRY_directory;
end;

OBJ_cache: array[OBJSET_cache] of MACH_cache;

OBJ_directory: array[OBJSET_directory] of MACH_directory;

OBJ_Ordered: array[Machines] of array[0..O_NET_MAX-1] of Message;
OBJ_Orderedcnt: array[Machines] of 0..O_NET_MAX;
OBJ_Unordered: array[Machines] of multiset[U_NET_MAX] of Message;

OBJ_FIFO: array[Machines] of FIFO;

-- CI { 
CoreReq: record
  cl: ClValue;
  vld: boolean;
  tp: enum {ci_store, ci_load, ci_evict}; 
end;
-- * vld = true,  tp determines the type
-- * The coherence protocol should mark vld as false when finishing a store 
-- * The read is poppsed (marked invalid) only if the coherence protocol return
-- values (i.e., `.cl` is no longer undefined)
-- } CI


var 
  i_cache: OBJ_cache;
  i_directory: OBJ_directory;

  fwd: OBJ_Ordered;
  cnt_fwd: OBJ_Orderedcnt;
  resp: OBJ_Unordered;
  req: OBJ_Unordered;

  buf_fwd: OBJ_FIFO;
  buf_resp: OBJ_FIFO;
  buf_req: OBJ_FIFO;

-- -- -- FVT {
-- The request that the randomly selected processor is currently processing
  prevProcReq: CoreReq;  -- acts as the one-entry buffer
  pendingReq: CoreReq;  -- acts as the one-entry buffer
  prevProcs: s_cache; -- STATE_TRANSITION 
  selc: OBJSET_cache; -- STATE_TRANSITION   
  myaddr: Address;    -- STATE_TRANSITION 

   -- MSG_CHK cur_node: Machines;  
-- } FVT

procedure book_keep(m: Machines);
-- var 
--   cur_state: s_cache;
--   in_stable_state: boolean;
begin
  -- MSG_CHK cur_node := m; 
  -- prevProcs_2 := prevProcs;
  prevProcs := i_cache[selc].CL[myaddr].State;  -- STATE_TRANSITION   -- other data are assoc. w/ this prevState


  undefine prevProcReq;
  undefine pendingReq;  -- to indicate if currently returning a requst
end;

function PushQueue(var f: OBJ_FIFO; n:Machines; msg:Message): boolean;
begin
  alias p:f[n] do
  alias q: p.Queue do
  alias qind: p.QueueInd do

    if (qind<=1) then
      q[qind]:=msg;
      qind:=qind+1;
      return true;
    endif;

    return false;

  endalias;
  endalias;
  endalias;
end;

function GetQueue(var f: OBJ_FIFO; n:Machines): Message;
var
  msg: Message;
begin
  alias p:f[n] do
  alias q: p.Queue do
  undefine msg;

  if !isundefined(q[0].mtype) then
    return q[0];
  endif;

  return msg;
  endalias;
  endalias;
end;

procedure PopQueue(var f: OBJ_FIFO; n:Machines);
begin
  alias p:f[n] do
  alias q: p.Queue do
  alias qind: p.QueueInd do


  for i := 0 to qind-1 do
      if i < qind-1 then
        q[i] := q[i+1];
      else
        undefine q[i];
      endif;
    endfor;
    qind := qind - 1;

  endalias;
  endalias;
  endalias;
end;

function Request(adr: Address; mtype: MessageType; src: Machines; dst: Machines) : Message;
var msg: Message;
begin
  msg.adr := adr;
  msg.mtype := mtype;
  msg.src := src;
  msg.dst := dst;
  msg.acksExpected := undefined;
  msg.cl := undefined;
  return msg;
end;

function Ack(adr: Address; mtype: MessageType; src: Machines; dst: Machines) : Message;
var msg: Message;
begin
  msg.adr := adr;
  msg.mtype := mtype;
  msg.src := src;
  msg.dst := dst;
  msg.acksExpected := undefined;
  msg.cl := undefined;
  return msg;
end;

function Resp(adr: Address; mtype: MessageType; src: Machines; dst: Machines; cl: ClValue) : Message;
var msg: Message;
begin
  msg.adr := adr;
  msg.mtype := mtype;
  msg.src := src;
  msg.dst := dst;
  msg.acksExpected := undefined;
  msg.cl := cl;
  return msg;
end;

function RespAck(adr: Address; mtype: MessageType; src: Machines; dst: Machines; cl: ClValue; acksExpected: 0..NrCaches) : Message;
var msg: Message;
begin
  msg.adr := adr;
  msg.mtype := mtype;
  msg.src := src;
  msg.dst := dst;
  msg.acksExpected := acksExpected;
  msg.cl := cl;
  return msg;
end;


procedure Send_fwd(msg:Message);
  Assert(cnt_fwd[msg.dst] < O_NET_MAX) "Too many messages";
  fwd[msg.dst][cnt_fwd[msg.dst]] := msg;
  cnt_fwd[msg.dst] := cnt_fwd[msg.dst] + 1;
  -- #SENDING,msg
  assert (!isundefined(msg.dst)) "undefined";
end;

procedure Pop_fwd(n:Machines);
begin
  Assert (cnt_fwd[n] > 0) "Trying to advance empty Q";
  for i := 0 to cnt_fwd[n]-1 do
    if i < cnt_fwd[n]-1 then
      fwd[n][i] := fwd[n][i+1];
    else
      undefine fwd[n][i];
    endif;
  endfor;
  cnt_fwd[n] := cnt_fwd[n] - 1;
end;


procedure Send_resp(msg:Message;);
  Assert (MultiSetCount(i:resp[msg.dst], true) < U_NET_MAX) "Too many messages";
  MultiSetAdd(msg, resp[msg.dst]);
  -- #SENDING,msg
end;

procedure Send_req(msg:Message;);
  Assert (MultiSetCount(i:req[msg.dst], true) < U_NET_MAX) "Too many messages";
  MultiSetAdd(msg, req[msg.dst]);
  -- #SENDING,msg
end;


procedure Multicast_fwd_v_NrCaches_OBJSET_cache(var msg: Message; dst:v_NrCaches_OBJSET_cache;);
begin
      for iSV:Machines do
          if iSV!=msg.src then
            if MultiSetCount(i:dst, dst[i] = iSV) = 1 then
              msg.dst := iSV;
              Send_fwd(msg);
            endif;
          endif;
      endfor;
end;

procedure Multicast_resp_v_NrCaches_OBJSET_cache(var msg: Message; dst:v_NrCaches_OBJSET_cache;);
begin
      for iSV:Machines do
          if iSV!=msg.src then
            if MultiSetCount(i:dst, dst[i] = iSV) = 1 then
              msg.dst := iSV;
              Send_resp(msg);
            endif;
          endif;
      endfor;
end;

procedure Multicast_req_v_NrCaches_OBJSET_cache(var msg: Message; dst:v_NrCaches_OBJSET_cache;);
begin
      for iSV:Machines do
          if iSV!=msg.src then
            if MultiSetCount(i:dst, dst[i] = iSV) = 1 then
              msg.dst := iSV;
              Send_req(msg);
            endif;
          endif;
      endfor;
end;


-- .add()
procedure AddElement_v_NrCaches_OBJSET_cache(var sv:v_NrCaches_OBJSET_cache; n:OBJSET_cache);
begin
    if MultiSetCount(i:sv, sv[i] = n) = 0 then
      MultiSetAdd(n, sv);
    endif;
end;

-- .del()
procedure RemoveElement_v_NrCaches_OBJSET_cache(var sv:v_NrCaches_OBJSET_cache; n:OBJSET_cache);
begin
    if MultiSetCount(i:sv, sv[i] = n) = 1 then
      MultiSetRemovePred(i:sv, sv[i] = n);
    endif;
end;

-- .clear()
procedure ClearVector_v_NrCaches_OBJSET_cache(var sv:v_NrCaches_OBJSET_cache;);
begin
    MultiSetRemovePred(i:sv, true);
end;

-- .contains()
function IsElement_v_NrCaches_OBJSET_cache(var sv:v_NrCaches_OBJSET_cache; n:OBJSET_cache) : boolean;
begin
    if MultiSetCount(i:sv, sv[i] = n) = 1 then
      return true;
    elsif MultiSetCount(i:sv, sv[i] = n) = 0 then
      return false;
    else
      Error "Multiple Entries of Sharer in SV multiset";
    endif;
  return false;
end;

-- .empty()
function HasElement_v_NrCaches_OBJSET_cache(var sv:v_NrCaches_OBJSET_cache; n:OBJSET_cache) : boolean;
begin
    if MultiSetCount(i:sv, true) = 0 then
      return false;
    endif;

    return true;
end;

-- .count()
function VectorCount_v_NrCaches_OBJSET_cache(var sv:v_NrCaches_OBJSET_cache) : cnt_v_NrCaches_OBJSET_cache;
begin
    return MultiSetCount(i:sv, IsMember(sv[i], OBJSET_cache));
end;



procedure i_cache_Defermsg(msg:Message; adr: Address; m:OBJSET_cache);
begin
	alias cle: i_cache[m].CL[adr] do
	alias q: cle.Defermsg.Queue do
	alias qind: cle.Defermsg.QueueInd do

	if (qind<=2) then
      q[qind]:=msg;
      qind:=qind+1;
    endif;

	endalias;
	endalias;
	endalias;
end;

procedure i_cache_SendDefermsg(adr: Address; m:OBJSET_cache);
begin
  alias cle: i_cache[m].CL[adr] do
  alias q: cle.Defermsg.Queue do
  alias qind: cle.Defermsg.QueueInd do

  for i := 0 to qind-1 do
  		--i_cache_Updatemsg(q[i], adr, m);
  		Send_resp(q[i]);
        undefine q[i];
    endfor;

   qind := 0;

  endalias;
  endalias;
  endalias;
end;


function Func_cache(inmsg:Message; m:OBJSET_cache) : boolean;
var msg: Message;
begin
  alias adr: inmsg.adr do
  alias cle: i_cache[m].CL[adr] do
switch cle.State

case cache_I:
switch inmsg.mtype
   else return false;
endswitch;

case cache_I_load:
switch inmsg.mtype
  case GetS_Ack:
    cle.cl := inmsg.cl;
    cle.State := cache_S;
    cle.Perm := load;
-- --     -- FVT {
   if (m = selc) then
    pendingReq.vld := true;
    pendingReq.cl := cle.cl;
   endif;
    --- } 

  case Inv:
    msg := Resp(adr,Inv_Ack,m,inmsg.src,cle.cl);
    Send_resp(msg);
    cle.State := cache_I_load__Inv_I;
    cle.Perm := none;

   else return false;
endswitch;

case cache_I_load__Inv_I:
switch inmsg.mtype
  case GetS_Ack:
    cle.cl := inmsg.cl;
    cle.State := cache_I;
    cle.Perm := none;
--    -- FVT {
   if (m = selc) then
    pendingReq.vld := true;
    pendingReq.cl := cle.cl; -- one-time read
   endif;
   --- }  

   else return false;
endswitch;

case cache_I_store:
switch inmsg.mtype
  case Fwd_GetM:
    msg := Resp(adr,GetM_Ack_D,m,inmsg.src,cle.cl);
    
    i_cache_Defermsg(msg, adr, m);
    cle.State := cache_I_store__Fwd_GetM_I;
    cle.Perm := none;

  case Fwd_GetS:
    msg := Resp(adr,GetS_Ack,m,inmsg.src,cle.cl);
    
    i_cache_Defermsg(msg, adr, m);
    msg := Resp(adr,WB,m,directory,cle.cl);
    
    i_cache_Defermsg(msg, adr, m);
    cle.State := cache_I_store__Fwd_GetS_S;
    cle.Perm := none;

  case GetM_Ack_AD:
    cle.acksExpected := inmsg.acksExpected;
    if (cle.acksExpected=cle.acksReceived) then
    cle.State := cache_M;
    cle.Perm := store;

    else
    cle.State := cache_I_store_GetM_Ack_AD;
    cle.Perm := none;
    endif;

  case GetM_Ack_D:
    cle.cl := inmsg.cl;
    cle.State := cache_M;
    cle.Perm := store;

  case Inv_Ack:
    cle.acksReceived := cle.acksReceived+1;
    cle.State := cache_I_store;
    cle.Perm := none;

   else return false;
endswitch;

case cache_I_store_GetM_Ack_AD:
switch inmsg.mtype
  case Fwd_GetM:
    msg := Resp(adr,GetM_Ack_D,m,inmsg.src,cle.cl);
    
    i_cache_Defermsg(msg, adr, m);
    cle.State := cache_I_store_GetM_Ack_AD__Fwd_GetM_I;
    cle.Perm := none;

  case Fwd_GetS:
    msg := Resp(adr,GetS_Ack,m,inmsg.src,cle.cl);
    
    i_cache_Defermsg(msg, adr, m);
    msg := Resp(adr,WB,m,directory,cle.cl);
    
    i_cache_Defermsg(msg, adr, m);
    cle.State := cache_I_store_GetM_Ack_AD__Fwd_GetS_S;
    cle.Perm := none;

  case Inv_Ack:
    cle.acksReceived := cle.acksReceived+1;
    if (cle.acksExpected=cle.acksReceived) then
    cle.State := cache_M;
    cle.Perm := store;

    else
    cle.State := cache_I_store_GetM_Ack_AD;
    cle.Perm := none;
    endif;

   else return false;
endswitch;

case cache_I_store_GetM_Ack_AD__Fwd_GetM_I:
switch inmsg.mtype
  case Inv_Ack:
    cle.acksReceived := cle.acksReceived+1;
    if (cle.acksExpected=cle.acksReceived) then
    cle.State := cache_I;
    cle.Perm := none;
    
    i_cache_SendDefermsg(adr, m);

    else
    cle.State := cache_I_store_GetM_Ack_AD__Fwd_GetM_I;
    cle.Perm := none;
    endif;

   else return false;
endswitch;

case cache_I_store_GetM_Ack_AD__Fwd_GetS_S:
switch inmsg.mtype
  case Inv:
    msg := Resp(adr,Inv_Ack,m,inmsg.src,cle.cl);
    Send_resp(msg);
    cle.State := cache_I_store_GetM_Ack_AD__Fwd_GetS_S__Inv_I;
    cle.Perm := none;

  case Inv_Ack:
    cle.acksReceived := cle.acksReceived+1;
    if (cle.acksExpected=cle.acksReceived) then
    cle.State := cache_S;
    cle.Perm := load;
    
    i_cache_SendDefermsg(adr, m);

    else
    cle.State := cache_I_store_GetM_Ack_AD__Fwd_GetS_S;
    cle.Perm := none;
    endif;

   else return false;
endswitch;

case cache_I_store_GetM_Ack_AD__Fwd_GetS_S__Inv_I:
switch inmsg.mtype
  case Inv_Ack:
    cle.acksReceived := cle.acksReceived+1;
    if (cle.acksExpected=cle.acksReceived) then
    cle.State := cache_I;
    cle.Perm := none;
    
    i_cache_SendDefermsg(adr, m);

    else
    cle.State := cache_I_store_GetM_Ack_AD__Fwd_GetS_S__Inv_I;
    cle.Perm := none;
    endif;

   else return false;
endswitch;

case cache_I_store__Fwd_GetM_I:
switch inmsg.mtype
  case GetM_Ack_AD:
    cle.acksExpected := inmsg.acksExpected;
    if (cle.acksExpected=cle.acksReceived) then
    cle.State := cache_I;
    cle.Perm := none;
    
    i_cache_SendDefermsg(adr, m);

    else
    cle.State := cache_I_store_GetM_Ack_AD__Fwd_GetM_I;
    cle.Perm := none;
    endif;

  case GetM_Ack_D:
    cle.cl := inmsg.cl;
    cle.State := cache_I;
    cle.Perm := none;
    
    i_cache_SendDefermsg(adr, m);

  case Inv_Ack:
    cle.acksReceived := cle.acksReceived+1;
    cle.State := cache_I_store__Fwd_GetM_I;
    cle.Perm := none;

   else return false;
endswitch;

case cache_I_store__Fwd_GetS_S:
switch inmsg.mtype
  case GetM_Ack_AD:
    cle.acksExpected := inmsg.acksExpected;
    if (cle.acksExpected=cle.acksReceived) then
    cle.State := cache_S;
    cle.Perm := load;
    
    i_cache_SendDefermsg(adr, m);

    else
    cle.State := cache_I_store_GetM_Ack_AD__Fwd_GetS_S;
    cle.Perm := none;
    endif;

  case GetM_Ack_D:
    cle.cl := inmsg.cl;
    cle.State := cache_S;
    cle.Perm := load;
    
    i_cache_SendDefermsg(adr, m);

  case Inv:
    msg := Resp(adr,Inv_Ack,m,inmsg.src,cle.cl);
    Send_resp(msg);
    cle.State := cache_I_store__Fwd_GetS_S__Inv_I;
    cle.Perm := none;

  case Inv_Ack:
    cle.acksReceived := cle.acksReceived+1;
    cle.State := cache_I_store__Fwd_GetS_S;
    cle.Perm := none;

   else return false;
endswitch;

case cache_I_store__Fwd_GetS_S__Inv_I:
switch inmsg.mtype
  case GetM_Ack_AD:
    cle.acksExpected := inmsg.acksExpected;
    if (cle.acksExpected=cle.acksReceived) then
    cle.State := cache_I;
    cle.Perm := none;
    
    i_cache_SendDefermsg(adr, m);

    else
    cle.State := cache_I_store_GetM_Ack_AD__Fwd_GetS_S__Inv_I;
    cle.Perm := none;
    endif;

  case GetM_Ack_D:
    cle.cl := inmsg.cl;
    cle.State := cache_I;
    cle.Perm := none;
    
    i_cache_SendDefermsg(adr, m);

  case Inv_Ack:
    cle.acksReceived := cle.acksReceived+1;
    cle.State := cache_I_store__Fwd_GetS_S__Inv_I;
    cle.Perm := none;

   else return false;
endswitch;

case cache_M:
switch inmsg.mtype
  case Fwd_GetM:
    msg := Resp(adr,GetM_Ack_D,m,inmsg.src,cle.cl);
    
    i_cache_Defermsg(msg, adr, m);
    
    i_cache_SendDefermsg(adr, m);
    cle.State := cache_I;
    cle.Perm := none;

  case Fwd_GetS:
    msg := Resp(adr,GetS_Ack,m,inmsg.src,cle.cl);
    
    i_cache_Defermsg(msg, adr, m);
    msg := Resp(adr,WB,m,directory,cle.cl);
    
    i_cache_Defermsg(msg, adr, m);
    
    i_cache_SendDefermsg(adr, m);
    cle.State := cache_S;
    cle.Perm := load;

   else return false;
endswitch;

case cache_M_evict:
switch inmsg.mtype
  case Fwd_GetM:
    msg := Resp(adr,GetM_Ack_D,m,inmsg.src,cle.cl);
    
    i_cache_Defermsg(msg, adr, m);
    
    i_cache_SendDefermsg(adr, m);
    cle.State := cache_M_evict_Fwd_GetM;
    cle.Perm := none;

  case Fwd_GetS:
    msg := Resp(adr,GetS_Ack,m,inmsg.src,cle.cl);
    
    i_cache_Defermsg(msg, adr, m);
    msg := Resp(adr,WB,m,directory,cle.cl);
    
    i_cache_Defermsg(msg, adr, m);
    
    i_cache_SendDefermsg(adr, m);
    cle.State := cache_S_evict;
    cle.Perm := none;

  case Put_Ack:
    cle.State := cache_I;
    cle.Perm := none;

   else return false;
endswitch;

case cache_M_evict_Fwd_GetM:
switch inmsg.mtype
  case Put_Ack:
    cle.State := cache_I;
    cle.Perm := none;

   else return false;
endswitch;

case cache_S:
switch inmsg.mtype
  case Inv:
    msg := Resp(adr,Inv_Ack,m,inmsg.src,cle.cl);
    Send_resp(msg);
    cle.State := cache_I;
    cle.Perm := none;

   else return false;
endswitch;

case cache_S_evict:
switch inmsg.mtype
  case Inv:
    msg := Resp(adr,Inv_Ack,m,inmsg.src,cle.cl);
    Send_resp(msg);
    cle.State := cache_M_evict_Fwd_GetM;
    cle.Perm := none;

  case Put_Ack:
    cle.State := cache_I;
    cle.Perm := none;

   else return false;
endswitch;

case cache_S_store:
switch inmsg.mtype
  case Fwd_GetM:
    msg := Resp(adr,GetM_Ack_D,m,inmsg.src,cle.cl);
    
    i_cache_Defermsg(msg, adr, m);
    cle.State := cache_I_store__Fwd_GetM_I;
    cle.Perm := none;

  case Fwd_GetS:
    msg := Resp(adr,GetS_Ack,m,inmsg.src,cle.cl);
    
    i_cache_Defermsg(msg, adr, m);
    msg := Resp(adr,WB,m,directory,cle.cl);
    
    i_cache_Defermsg(msg, adr, m);
    cle.State := cache_S_store__Fwd_GetS_S;
    cle.Perm := load;

  case GetM_Ack_AD:
    cle.acksExpected := inmsg.acksExpected;
    if (cle.acksExpected=cle.acksReceived) then
    cle.State := cache_M;
    cle.Perm := store;

    else
    cle.State := cache_S_store_GetM_Ack_AD;
    cle.Perm := load;
    endif;

  case GetM_Ack_D:
    cle.State := cache_M;
    cle.Perm := store;

  case Inv:
    msg := Resp(adr,Inv_Ack,m,inmsg.src,cle.cl);
    Send_resp(msg);
    cle.State := cache_I_store;
    cle.Perm := none;

  case Inv_Ack:
    cle.acksReceived := cle.acksReceived+1;
    cle.State := cache_S_store;
    cle.Perm := load;

   else return false;
endswitch;

case cache_S_store_GetM_Ack_AD:
switch inmsg.mtype
  case Fwd_GetM:
    msg := Resp(adr,GetM_Ack_D,m,inmsg.src,cle.cl);
    
    i_cache_Defermsg(msg, adr, m);
    cle.State := cache_I_store_GetM_Ack_AD__Fwd_GetM_I;
    cle.Perm := none;

  case Fwd_GetS:
    msg := Resp(adr,GetS_Ack,m,inmsg.src,cle.cl);
    
    i_cache_Defermsg(msg, adr, m);
    msg := Resp(adr,WB,m,directory,cle.cl);
    
    i_cache_Defermsg(msg, adr, m);
    cle.State := cache_S_store_GetM_Ack_AD__Fwd_GetS_S;
    cle.Perm := load;

  case Inv_Ack:
    cle.acksReceived := cle.acksReceived+1;
    if (cle.acksExpected=cle.acksReceived) then
    cle.State := cache_M;
    cle.Perm := store;

    else
    cle.State := cache_S_store_GetM_Ack_AD;
    cle.Perm := load;
    endif;

   else return false;
endswitch;

case cache_S_store_GetM_Ack_AD__Fwd_GetS_S:
switch inmsg.mtype
  case Inv:
    msg := Resp(adr,Inv_Ack,m,inmsg.src,cle.cl);
    Send_resp(msg);
    cle.State := cache_I_store_GetM_Ack_AD__Fwd_GetS_S__Inv_I;
    cle.Perm := none;

  case Inv_Ack:
    cle.acksReceived := cle.acksReceived+1;
    if (cle.acksExpected=cle.acksReceived) then
    cle.State := cache_S;
    cle.Perm := load;
    
    i_cache_SendDefermsg(adr, m);

    else
    cle.State := cache_S_store_GetM_Ack_AD__Fwd_GetS_S;
    cle.Perm := load;
    endif;

   else return false;
endswitch;

case cache_S_store__Fwd_GetS_S:
switch inmsg.mtype
  case GetM_Ack_AD:
    cle.acksExpected := inmsg.acksExpected;
    if (cle.acksExpected=cle.acksReceived) then
    cle.State := cache_S;
    cle.Perm := load;
    
    i_cache_SendDefermsg(adr, m);

    else
    cle.State := cache_S_store_GetM_Ack_AD__Fwd_GetS_S;
    cle.Perm := load;
    endif;

  case GetM_Ack_D:
    cle.State := cache_S;
    cle.Perm := load;
    
    i_cache_SendDefermsg(adr, m);

  case Inv:
    msg := Resp(adr,Inv_Ack,m,inmsg.src,cle.cl);
    Send_resp(msg);
    cle.State := cache_I_store__Fwd_GetS_S__Inv_I;
    cle.Perm := none;

  case Inv_Ack:
    cle.acksReceived := cle.acksReceived+1;
    cle.State := cache_S_store__Fwd_GetS_S;
    cle.Perm := load;

   else return false;
endswitch;

endswitch;
  endalias;
  endalias;

return true;
end;


procedure i_directory_Defermsg(msg:Message; adr: Address; m:OBJSET_directory);
begin
	alias cle: i_directory[m].CL[adr] do
	alias q: cle.Defermsg.Queue do
	alias qind: cle.Defermsg.QueueInd do

	if (qind<=2) then
      q[qind]:=msg;
      qind:=qind+1;
    endif;

	endalias;
	endalias;
	endalias;
end;

procedure i_directory_SendDefermsg(adr: Address; m:OBJSET_directory);
begin
  alias cle: i_directory[m].CL[adr] do
  alias q: cle.Defermsg.Queue do
  alias qind: cle.Defermsg.QueueInd do

  for i := 0 to qind-1 do
  		--i_directory_Updatemsg(q[i], adr, m);
  		Send_resp(q[i]);
        undefine q[i];
    endfor;

   qind := 0;

  endalias;
  endalias;
  endalias;
end;


function Func_directory(inmsg:Message; m:OBJSET_directory) : boolean;
var msg: Message;
begin
  alias adr: inmsg.adr do
  alias cle: i_directory[m].CL[adr] do
switch cle.State

case directory_I:
switch inmsg.mtype
  case GetM:
    msg := RespAck(adr,GetM_Ack_AD,m,inmsg.src,cle.cl,VectorCount_v_NrCaches_OBJSET_cache(cle.cache));
    Send_resp(msg);
    cle.owner := inmsg.src;
    cle.State := directory_M;
    cle.Perm := none;

  case GetS:
    AddElement_v_NrCaches_OBJSET_cache(cle.cache,inmsg.src);
    msg := Resp(adr,GetS_Ack,m,inmsg.src,cle.cl);
    Send_resp(msg);
    cle.State := directory_S;
    cle.Perm := none;

  case PutM:
    msg := Ack(adr,Put_Ack,m,inmsg.src);
    Send_fwd(msg);
    RemoveElement_v_NrCaches_OBJSET_cache(cle.cache,inmsg.src);
    if (cle.owner=inmsg.src) then
    cle.cl := inmsg.cl;
    cle.State := directory_I;
    cle.Perm := none;

    else
    cle.State := directory_I;
    cle.Perm := none;
    endif;

  case PutS:
    msg := Resp(adr,Put_Ack,m,inmsg.src,cle.cl);
    Send_fwd(msg);
    RemoveElement_v_NrCaches_OBJSET_cache(cle.cache,inmsg.src);
    if (VectorCount_v_NrCaches_OBJSET_cache(cle.cache)=0) then
    cle.State := directory_I;
    cle.Perm := none;

    else
    cle.State := directory_I;
    cle.Perm := none;
    endif;

  case Upgrade:
    msg := RespAck(adr,GetM_Ack_AD,m,inmsg.src,cle.cl,VectorCount_v_NrCaches_OBJSET_cache(cle.cache));
    Send_resp(msg);
    cle.owner := inmsg.src;
    cle.State := directory_M;
    cle.Perm := none;

   else return false;
endswitch;

case directory_M:
switch inmsg.mtype
  case GetM:
    msg := Request(adr,Fwd_GetM,inmsg.src,cle.owner);
    Send_fwd(msg);
    cle.owner := inmsg.src;
    cle.State := directory_M;
    cle.Perm := none;

  case GetS:
    msg := Request(adr,Fwd_GetS,inmsg.src,cle.owner);
    Send_fwd(msg);
    AddElement_v_NrCaches_OBJSET_cache(cle.cache,inmsg.src);
    AddElement_v_NrCaches_OBJSET_cache(cle.cache,cle.owner);
    cle.State := directory_M_GetS;
    cle.Perm := none;

  case PutM:
    msg := Ack(adr,Put_Ack,m,inmsg.src);
    Send_fwd(msg);
    RemoveElement_v_NrCaches_OBJSET_cache(cle.cache,inmsg.src);
    if (cle.owner=inmsg.src) then
    cle.cl := inmsg.cl;
    cle.State := directory_I;
    cle.Perm := none;

    else
    cle.State := directory_M;
    cle.Perm := none;
    endif;

  case PutS:
    msg := Resp(adr,Put_Ack,m,inmsg.src,cle.cl);
    Send_fwd(msg);
    RemoveElement_v_NrCaches_OBJSET_cache(cle.cache,inmsg.src);
    if (VectorCount_v_NrCaches_OBJSET_cache(cle.cache)=0) then
    cle.State := directory_M;
    cle.Perm := none;

    else
    cle.State := directory_M;
    cle.Perm := none;
    endif;

  case Upgrade:
    msg := Request(adr,Fwd_GetM,inmsg.src,cle.owner);
    Send_fwd(msg);
    cle.owner := inmsg.src;
    cle.State := directory_M;
    cle.Perm := none;

   else return false;
endswitch;

case directory_M_GetS:
switch inmsg.mtype
  case WB:
    if (inmsg.src=cle.owner) then
    cle.cl := inmsg.cl;
    cle.State := directory_S;
    cle.Perm := none;

    else
    cle.State := directory_M_GetS;
    cle.Perm := none;
    endif;

   else return false;
endswitch;

case directory_S:
switch inmsg.mtype
  case GetM:
    if (IsElement_v_NrCaches_OBJSET_cache(cle.cache,inmsg.src)) then
    RemoveElement_v_NrCaches_OBJSET_cache(cle.cache,inmsg.src);
    msg := RespAck(adr,GetM_Ack_AD,m,inmsg.src,cle.cl,VectorCount_v_NrCaches_OBJSET_cache(cle.cache));
    Send_resp(msg);
    cle.State := directory_M;
    cle.Perm := none;
    msg := Ack(adr,Inv,inmsg.src,inmsg.src);
    Multicast_fwd_v_NrCaches_OBJSET_cache(msg,cle.cache);
    cle.owner := inmsg.src;
    ClearVector_v_NrCaches_OBJSET_cache(cle.cache);

    else
    msg := RespAck(adr,GetM_Ack_AD,m,inmsg.src,cle.cl,VectorCount_v_NrCaches_OBJSET_cache(cle.cache));
    Send_resp(msg);
    cle.State := directory_M;
    cle.Perm := none;
    msg := Ack(adr,Inv,inmsg.src,inmsg.src);
    Multicast_fwd_v_NrCaches_OBJSET_cache(msg,cle.cache);
    cle.owner := inmsg.src;
    ClearVector_v_NrCaches_OBJSET_cache(cle.cache);
    endif;

  case GetS:
    AddElement_v_NrCaches_OBJSET_cache(cle.cache,inmsg.src);
    msg := Resp(adr,GetS_Ack,m,inmsg.src,cle.cl);
    Send_resp(msg);
    cle.State := directory_S;
    cle.Perm := none;

  case PutM:
    msg := Ack(adr,Put_Ack,m,inmsg.src);
    Send_fwd(msg);
    RemoveElement_v_NrCaches_OBJSET_cache(cle.cache,inmsg.src);
    if (cle.owner=inmsg.src) then
    cle.cl := inmsg.cl;
    cle.State := directory_S;
    cle.Perm := none;

    else
    cle.State := directory_S;
    cle.Perm := none;
    endif;

  case PutS:
    msg := Resp(adr,Put_Ack,m,inmsg.src,cle.cl);
    Send_fwd(msg);
    RemoveElement_v_NrCaches_OBJSET_cache(cle.cache,inmsg.src);
    if (VectorCount_v_NrCaches_OBJSET_cache(cle.cache)=0) then
    cle.State := directory_I;
    cle.Perm := none;

    else
    cle.State := directory_S;
    cle.Perm := none;
    endif;

  case Upgrade:
    if (IsElement_v_NrCaches_OBJSET_cache(cle.cache,inmsg.src)) then
    RemoveElement_v_NrCaches_OBJSET_cache(cle.cache,inmsg.src);
    msg := RespAck(adr,GetM_Ack_AD,m,inmsg.src,cle.cl,VectorCount_v_NrCaches_OBJSET_cache(cle.cache));
    Send_resp(msg);
    cle.State := directory_M;
    cle.Perm := none;
    msg := Ack(adr,Inv,inmsg.src,inmsg.src);
    Multicast_fwd_v_NrCaches_OBJSET_cache(msg,cle.cache);
    cle.owner := inmsg.src;
    ClearVector_v_NrCaches_OBJSET_cache(cle.cache);

    else
    msg := RespAck(adr,GetM_Ack_AD,m,inmsg.src,cle.cl,VectorCount_v_NrCaches_OBJSET_cache(cle.cache));
    Send_resp(msg);
    cle.State := directory_M;
    cle.Perm := none;
    msg := Ack(adr,Inv,inmsg.src,inmsg.src);
    Multicast_fwd_v_NrCaches_OBJSET_cache(msg,cle.cache);
    cle.owner := inmsg.src;
    ClearVector_v_NrCaches_OBJSET_cache(cle.cache);
    endif;

   else return false;
endswitch;

endswitch;
  endalias;
  endalias;

return true;
end;



procedure SEND_cache_I_load(adr:Address; m:OBJSET_cache);
var msg: Message;
begin
  alias cle: i_cache[m].CL[adr] do
    msg := Request(adr,GetS,m,directory);
    Send_req(msg);
    cle.State := cache_I_load;
    cle.Perm := none;
endalias;
end;


procedure SEND_cache_I_store(adr:Address; m:OBJSET_cache);
var msg: Message;
begin
  alias cle: i_cache[m].CL[adr] do
    msg := Request(adr,GetM,m,directory);
    Send_req(msg);
    cle.acksReceived := 0;
    cle.State := cache_I_store;
    cle.Perm := none;
endalias;
end;



procedure SEND_cache_M_evict(adr:Address; m:OBJSET_cache);
var msg: Message;
begin
  alias cle: i_cache[m].CL[adr] do
    msg := Resp(adr,PutM,m,directory,cle.cl);
    Send_req(msg);
    cle.State := cache_M_evict;
    cle.Perm := none;
endalias;
end;


procedure SEND_cache_M_load(adr:Address; m:OBJSET_cache);
var msg: Message;
begin
  alias cle: i_cache[m].CL[adr] do
    cle.State := cache_M;
    cle.Perm := store;
endalias;
end;


procedure SEND_cache_M_store(adr:Address; m:OBJSET_cache);
var msg: Message;
begin
  alias cle: i_cache[m].CL[adr] do
    cle.State := cache_M;
    cle.Perm := store;
endalias;
end;



procedure SEND_cache_S_evict(adr:Address; m:OBJSET_cache);
var msg: Message;
begin
  alias cle: i_cache[m].CL[adr] do
    msg := Request(adr,PutS,m,directory);
    Send_req(msg);
    cle.State := cache_S_evict;
    cle.Perm := none;
endalias;
end;


procedure SEND_cache_S_load(adr:Address; m:OBJSET_cache);
var msg: Message;
begin
  alias cle: i_cache[m].CL[adr] do
    cle.State := cache_S;
    cle.Perm := load;
endalias;
end;


procedure SEND_cache_S_store(adr:Address; m:OBJSET_cache);
var msg: Message;
begin
  alias cle: i_cache[m].CL[adr] do
    msg := Request(adr,Upgrade,m,directory);
    Send_req(msg);
    cle.acksReceived := 0;
    cle.State := cache_S_store;
    cle.Perm := load;
endalias;
end;

procedure get_evict_req(m:OBJSET_cache);
begin
  if (m = selc) then
    prevProcReq.tp:= ci_evict; 
    prevProcReq.cl:= undefined; 
    prevProcReq.vld := false; -- we assume replacemenet returns immediately
  endif;
end;
procedure get_store_req(m:OBJSET_cache; cl:ClValue);
begin
  if (m = selc) then
    prevProcReq.tp:= ci_store; 
    prevProcReq.cl:= cl; 
    prevProcReq.vld := true; 
  endif;
end;
procedure fin_st_ev_req(m:OBJSET_cache);
begin
  if (m = selc) then
    prevProcReq.vld := false;
  endif;
end;
procedure fin_load_req(m:OBJSET_cache; v:ClValue);
begin
  if (m = selc) then
    pendingReq.cl := v;
    pendingReq.vld := true;
  endif;
end;
procedure get_load_req(m:OBJSET_cache);
begin
  if (m = selc) then
    prevProcReq.tp:= ci_load; 
    prevProcReq.cl:= UNDEFINED; 
    prevProcReq.vld := true; 
  endif;
end;
-- procedure update_pending_req(m:OBJSET_cache);
-- begin
--   if (m = selc) then
--     if (!isundefined(prevProcReq.vld)) then
--       if (
--         (prevProcReq.vld & prevProcReq.tp = ci_load & isundefined(prevProcReq.cl)) | 
--         (prevProcReq.vld & prevProcReq.tp = ci_store) | 
--         (prevProcReq.vld & prevProcReq.tp = ci_evict)) then
--         -- not completed yet
--         -- pendingReq := prevProcReq;
--         -- DLCHK cntr := 0;
--       endif;
--     endif;
--   endif;
-- end;

ruleset m:OBJSET_cache do
ruleset adr:Address do
  alias cle:i_cache[m].CL[adr] do

  rule "cache_I_load"
    cle.State = cache_I
-- --     & (m != selc | !pendingReq.vld)  -- FVT
  ==>
         book_keep(m); -- FVT
     get_load_req(m); -- FVT
    SEND_cache_I_load(adr, m);
-- --     update_pending_req(m); -- FVT
  endrule;
  
  ruleset vv:ClValue do
  rule "cache_I_store"
    cle.State = cache_I
-- --     & (m != selc | !pendingReq.vld)  -- FVT
  ==>
    book_keep(m); -- FVT
    get_store_req(m, vv); -- FVT
    cle.cl := vv; -- FVT, no-fetch-on-miss
    SEND_cache_I_store(adr, m);
--     fin_st_ev_req(m); -- FVT
--     update_pending_req(m); -- FVT
  endrule;
  endruleset;
  
  
  rule "cache_M_evict"
    cle.State = cache_M
--     & (m != selc | !pendingReq.vld)  -- FVT
  ==>
    book_keep(m); -- FVT
    get_evict_req(m); -- FVT
    SEND_cache_M_evict(adr, m);
--     update_pending_req(m); -- FVT
  endrule;
  
  rule "cache_M_load"
    cle.State = cache_M 
--     & (m != selc | !pendingReq.vld)  -- FVT
  ==>
     book_keep(m); -- FVT
    get_load_req(m); -- FVT
    SEND_cache_M_load(adr, m);
    fin_load_req(m, cle.cl); -- FVT
--     update_pending_req(m); -- FVT
  endrule;

  ruleset vv:ClValue do 
  rule "cache_M_store"
    cle.State = cache_M
--     & (m != selc | !pendingReq.vld)  -- FVT
  ==>
     book_keep(m); -- FVT
    get_store_req(m, vv); -- FVT
    cle.cl := vv; -- FVT
    SEND_cache_M_store(adr, m);
--     fin_st_ev_req(m); -- FVT
--     update_pending_req(m); -- FVT
  endrule;
  endruleset;
  
  
  rule "cache_S_evict"
    cle.State = cache_S
--     & (m != selc | !pendingReq.vld)  -- FVT
  ==>
     book_keep(m); -- FVT
    get_evict_req(m); -- FVT
    SEND_cache_S_evict(adr, m);
--     update_pending_req(m); -- FVT
  endrule;
  
  rule "cache_S_load"
    cle.State = cache_S
--     & (m != selc | !pendingReq.vld)  -- FVT
  
  ==>
     book_keep(m); -- FVT
   get_load_req(m); -- FVT
    SEND_cache_S_load(adr, m);
    fin_load_req(m, cle.cl); -- FVT
--     update_pending_req(m); -- FVT
  endrule;
  
  ruleset vv:ClValue do 
  rule "cache_S_store"
    cle.State = cache_S
--     & (m != selc | !pendingReq.vld)  -- FVT
  
  ==>
     book_keep(m); -- FVT
    get_store_req(m, vv); -- FVT
     cle.cl := vv; -- FVT, no-fetch-on-miss
    SEND_cache_S_store(adr, m);
--     fin_st_ev_req(m); -- FVT
--     update_pending_req(m); -- FVT
  endrule;
  endruleset;

  rule "cache_SM_AD_load"
    cle.State = cache_S_store
--     & (m != selc | !pendingReq.vld)  -- FVT
  ==>
     book_keep(m); -- FVT
    get_load_req(m); -- FVT
    fin_load_req(m, cle.cl); -- FVT
--     update_pending_req(m); -- FVT
  endrule;

  rule "cache_SM_A_load"
    cle.State = cache_S_store_GetM_Ack_AD 
--     & (m != selc | !pendingReq.vld)  -- FVT
  ==>
     book_keep(m); -- FVT
    get_load_req(m); -- FVT
    fin_load_req(m, cle.cl); -- FVT
--     update_pending_req(m); -- FVT
  endrule;
  
  rule "cache_SM_AD_S_load"
    cle.State = cache_S_store__Fwd_GetS_S
--     & (m != selc | !pendingReq.vld)  -- FVT
  ==>
     book_keep(m); -- FVT
    get_load_req(m); -- FVT
    fin_load_req(m, cle.cl); -- FVT
--     update_pending_req(m); -- FVT
  endrule;
  
  endalias;
endruleset;
endruleset;



ruleset n:Machines do
  alias p:buf_fwd[n] do

      rule "buf_fwd"
        (p.QueueInd>0)
      ==>
  book_keep(n);
        alias msg:p.Queue[0] do
          if IsMember(n, OBJSET_directory) then
            if Func_directory(msg, n) then
              PopQueue(buf_fwd, n);
            endif;
          else
            if Func_cache(msg, n) then
              PopQueue(buf_fwd, n);
            endif;
          endif;
        endalias;

      endrule;
  endalias;
endruleset;

ruleset n:Machines do
  alias p:buf_resp[n] do

      rule "buf_resp"
        (p.QueueInd>0)
      ==>
  book_keep(n);
        alias msg:p.Queue[0] do
          if IsMember(n, OBJSET_directory) then
            if Func_directory(msg, n) then
              PopQueue(buf_resp, n);
            endif;
          else
            if Func_cache(msg, n) then
              PopQueue(buf_resp, n);
            endif;
          endif;
        endalias;

      endrule;
  endalias;
endruleset;

ruleset n:Machines do
  alias p:buf_req[n] do

      rule "buf_req"
        (p.QueueInd>0)
      ==>
  book_keep(n);
        alias msg:p.Queue[0] do
          if IsMember(n, OBJSET_directory) then
            if Func_directory(msg, n) then
              PopQueue(buf_req, n);
            endif;
          else
            if Func_cache(msg, n) then
              PopQueue(buf_req, n);
            endif;
          endif;
        endalias;

      endrule;
  endalias;
endruleset;


ruleset n:Machines do

    choose midx:resp[n] do
        alias mach:resp[n] do
        alias msg:mach[midx] do
          rule "Receive resp"
            !isundefined(msg.mtype)
          ==>
  book_keep(n);
            -- #RECEIVING,msg
            if (ENABLE_QS) then
              if PushQueue(buf_resp, n, msg) then
                MultiSetRemove(midx, mach);
              endif;
            else
              -- Without input queues
              if IsMember(n, OBJSET_directory) then
                if Func_directory(msg, n) then
                  MultiSetRemove(midx, mach);
                endif;
              else
                if Func_cache(msg, n) then
                  MultiSetRemove(midx, mach);
                endif;
              endif;
            endif;
          endrule;
        endalias;
        endalias;
    endchoose;

endruleset;

ruleset n:Machines do

    choose midx:req[n] do
        alias mach:req[n] do
        alias msg:mach[midx] do
          rule "Receive req"
            !isundefined(msg.mtype)
          ==>
  book_keep(n);
        -- #RECEIVING,msg
            if (ENABLE_QS) then
              if PushQueue(buf_req, n, msg) then
                MultiSetRemove(midx, mach);
              endif;
            else
              -- Without input queues
              if IsMember(n, OBJSET_directory) then
                if Func_directory(msg, n) then
                  MultiSetRemove(midx, mach);
                endif;
              else
                if Func_cache(msg, n) then
                  MultiSetRemove(midx, mach);
                endif;
              endif;
            endif;
          endrule;
        endalias;
        endalias;
    endchoose;

endruleset;

ruleset n:Machines do
    alias msg:fwd[n][0] do
      rule "Receive fwd"
        cnt_fwd[n] > 0
      ==>
  book_keep(n);
        -- #RECEIVING,msg
        -- With input queues
        if (ENABLE_QS) then
          if PushQueue(buf_fwd, n, msg) then
            Pop_fwd(n);
          endif;
        else
        -- Without input queues
          if IsMember(n, OBJSET_directory) then
            if Func_directory(msg, n) then
              Pop_fwd(n);
            endif;
          else
            if Func_cache(msg, n) then
              Pop_fwd(n);
            endif;
          endif;
        endif;
      endrule;
    endalias;

-- CI {
-- 1-entry buffer getting requests and popping request 
-- } CI 
endruleset;

-- rule "core_pop_read"
--   !isundefined(pendingReq.vld) & 
--   pendingReq.vld & 
--   pendingReq.tp = ci_load & 
--   !isundefined (pendingReq.cl)
--   ==>
--   -- book_keep(selc); 
--   pendingReq.vld := false;
-- endrule;

startstate
var tmpv:ClValue;
begin 
  for vvv: ClValue do
    tmpv := vvv;
  endfor;


  for i:OBJSET_directory do
  for a:Address do
    i_directory[i].CL[a].State := directory_I;
    i_directory[i].CL[a].cl := tmpv;
    i_directory[i].CL[a].Defermsg.QueueInd := 0;
    i_directory[i].CL[a].Perm := none;
  endfor;
  endfor;
  
  for i:OBJSET_cache do
  for a:Address do
    i_cache[i].CL[a].State := cache_I;
    i_cache[i].CL[a].acksExpected := 0;
    i_cache[i].CL[a].acksReceived := 0;
    i_cache[i].CL[a].cl := tmpv;
    i_cache[i].CL[a].Defermsg.QueueInd := 0;
    i_cache[i].CL[a].Perm := none;
  endfor;
  endfor;
  
  for i:Machines do
      undefine buf_fwd[i].Queue;
      buf_fwd[i].QueueInd:=0;
  endfor;
  
  for i:Machines do
      undefine buf_resp[i].Queue;
      buf_resp[i].QueueInd:=0;
  endfor;
  
  for i:Machines do
      undefine buf_req[i].Queue;
      buf_req[i].QueueInd:=0;
  endfor;
  
  undefine resp;
  
  undefine req;
  
  undefine fwd;
  for n:Machines do
    cnt_fwd[n] := 0;
  endfor;

--   -- FVT
  -- undefine trackReq;
  undefine prevProcReq;
  undefine pendingReq;
  -- pendingReq.vld := false;
  -- undefine prevProcReq_2;
  undefine prevProcs; -- STATE_TRANSITION 
  -- undefine prevProcs_2;
  -- undefine prevHomeNode;

  -- undefine prevSendMsg;
  -- undefine prevRecProcMsg;
  -- start := false;
  -- tracked := false;
  -- new_req := false;

  for n: OBJSET_cache do   -- STATE_TRANSITION
    selc := n;  -- STATE_TRANSITION
  endfor;  -- STATE_TRANSITION
  for a: Address do   -- STATE_TRANSITION
    myaddr := a;  -- STATE_TRANSITION
  endfor;  -- STATE_TRANSITION
  -- DLCHK cntr := 0;
  -- MSG_CHK undefine cur_node; 
endstartstate;


-- invariant "Write Serialization"
--     forall c1:OBJSET_cache do
--     forall c2:OBJSET_cache do
--     forall a:Address do
--     ( c1 != c2
--     & i_cache[c1].CL[a].Perm = store )
--     ->
--     ( i_cache[c2].CL[a].Perm != store )
--     endforall
--     endforall
--     endforall;


-- DLCHK invariant "eventual_progress"
-- DLCHK   forall m:OBJSET_cache do 
-- DLCHK   (m != selc) | (
-- DLCHK     cntr <= 10 |
-- DLCHK     !pendingReq.vld
-- DLCHK   )
-- DLCHK   endforall;

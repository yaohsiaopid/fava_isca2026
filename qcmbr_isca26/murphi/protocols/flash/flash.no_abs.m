-- abstracted version form simple PV  `C.-T. Chou, P. K. Mannava, and S. Park, A simple method for parameterized verification of cache coherence protocols, FMCAD 2004.`
-- https://www.markrtuttle.com/fmcad08/
-- Murali Talupur and Mark Tuttle. Going with the flow: Parameterized verification using message flows. In Proceedings of the 8th International Conference on Formal Methods in Computer-Aided Design (FMCAD), November 2008.
-- we used the following murphi models as our examples (grab them all as a single file)
-- The Flash and German cache coherence protocols as modeled by Ching-Tsun Chou and used in the paper C.-T. Chou, P. K. Mannava, and S. Park, A simple method for parameterized verification of cache coherence protocols, FMCAD 2004.
-- prefix:  indicate where the requests are generated from.
--  * PI: Processor Interface
--  * NI: Network Interface
-- PI handlers are initiated by a requesting processor
-- NI handlers are initiated by a message from the network. 
-- The additional notation ‘Local’ or ‘Remote’ indicates whether the processing node is the home of the requested memory address.
-- Each rule will be augmented with "cur" that the rule is handling  
-- #SENDING,<var_name>
-- #SENDING,<var_name>,<type>
-- #SENDING,<var_name>,<type>,<src>,<dst>, where src/dst may either be the <literal_name> or field:<field_name>
-- #RECEIVING,<var_name> right before var_name is dequeued/cleared
-- #RECEIVING,<var_name>,<type>,<src>,<dst>, where src/dst may either be the <literal_name> or field:<field_name>
-- At receiving call site, we assume the dst is receiving and popping out that message
-- At sending call site, we assume  the src is sending out to the dst

const

  NODE_NUM : 3;
  DATA_NUM : 2;

type

  NODE : scalarset(NODE_NUM);
  DATA : scalarset(DATA_NUM);


  CACHE_STATE : enum {CACHE_I, CACHE_S, CACHE_E};

  NODE_CMD : enum {NODE_None, NODE_Get, NODE_GetX};

  FV_CPND_STATE: enum {
    s1, s2, s3, s4, s5, s6,
    s7, s8, s9, s10, s11, s12,
    s13, s14, s15, s16, s17, s18
  };

  FV_CPND_DIR_STATE: enum {
    dir_s0, dir_s1, dir_s2, dir_s3,
    dir_s4, dir_s5, dir_s6, dir_s7,
    dir_s8, dir_s9, dir_s10, dir_s11,
    dir_s12, dir_s13, dir_s14, dir_s15
  };

  NODE_STATE : record
    ProcCmd : NODE_CMD;
    -- ProcCmdData : DATA; -- FVT
    InvMarked : boolean;
    CacheState : CACHE_STATE;
    CacheData : DATA;
  end;

  DIR_STATE : record
    Pending : boolean;
    Local : boolean;
    Dirty : boolean;
    HeadVld : boolean;
    HeadPtr : NODE;
    ShrVld : boolean;
    ShrSet : array [NODE] of boolean;
    InvSet : array [NODE] of boolean;
  end;

  UNI_CMD : enum {UNI_None, UNI_Get, UNI_GetX, UNI_Put, UNI_PutX, UNI_Nak};

  UNI_MSG : record
    Cmd : UNI_CMD;
    Proc : NODE; -- dst
    Data : DATA;
  end;

  INV_CMD : enum {INV_None, INV_Inv, INV_InvAck};

  INV_MSG : record
    Cmd : INV_CMD;
    Proc : NODE; -- src 
  end;

  RP_CMD : enum {RP_None, RP_Replace};

  RP_MSG : record
    Cmd : RP_CMD;
  end;

  WB_CMD : enum {WB_None, WB_Wb};

  WB_MSG : record
    Cmd : WB_CMD;
    Proc : NODE;
    Data : DATA;
  end;

  SHWB_CMD : enum {SHWB_None, SHWB_ShWb, SHWB_FAck};

  SHWB_MSG : record
    Cmd : SHWB_CMD;
    Proc : NODE;
    Data : DATA;
  end;

  NAKC_CMD : enum {NAKC_None, NAKC_Nakc};

  NAKC_MSG : record
    Cmd : NAKC_CMD;
  end;

  STATE : record
  -- Program variables:
    Proc : array [NODE] of NODE_STATE;
    Dir : DIR_STATE;
    MemData : DATA;
    ---------------- all channels of messages
    UniMsg : array [NODE] of UNI_MSG;
    -- UniMsg[src/dst]
    -- .Proc = dst/src
    InvMsg : array [NODE] of INV_MSG;
    -- InvMsg[dst], src always home
    RpMsg : array [NODE] of RP_MSG;
    -- RpMsg[src], dst always home
    WbMsg : WB_MSG;
    -- .Proc: dst
    ShWbMsg : SHWB_MSG;
    NakcMsg : NAKC_MSG;
  -- Auxiliary variables:
    CurrData : DATA;
    PrevData : DATA;
    LastWrVld : boolean;
    LastWrPtr : NODE;
    PendReqSrc : NODE;
    PendReqCmd : UNI_CMD;
    Collecting : boolean;
    FwdCmd : UNI_CMD;
    FwdSrc : NODE;
    LastInvAck : NODE;
    LastOtherInvAck : NODE;
  end;

var

  ActiveReq: array [NODE] of DATA; -- FVT
  Home : NODE;
  Sta : STATE;


-------------------------------------------------------------------------------
procedure get_evict_req(m:NODE);
begin
end;
procedure get_store_req(m:NODE; cl:DATA);
begin
end;
-- rule.*PI_(Remote|Local)_Get(?!X)
procedure get_load_req(m:NODE);
begin
end;

-- Compound per-core control state used by analysis scripts.
-- Mapping order:
--   CacheState in {I, S, E}
--   InvMarked in {false, true}
--   ProcCmd in {None, Get, GetX}
function get_state(src:NODE): FV_CPND_STATE;
begin
  if Sta.Proc[src].CacheState = CACHE_I then
    if !Sta.Proc[src].InvMarked then
      if Sta.Proc[src].ProcCmd = NODE_None then
        return s1;
      elsif Sta.Proc[src].ProcCmd = NODE_Get then
        return s2;
      else
        return s3;
      endif;
    else
      if Sta.Proc[src].ProcCmd = NODE_None then
        return s4;
      elsif Sta.Proc[src].ProcCmd = NODE_Get then
        return s5;
      else
        return s6;
      endif;
    endif;
  elsif Sta.Proc[src].CacheState = CACHE_S then
    if !Sta.Proc[src].InvMarked then
      if Sta.Proc[src].ProcCmd = NODE_None then
        return s7;
      elsif Sta.Proc[src].ProcCmd = NODE_Get then
        return s8;
      else
        return s9;
      endif;
    else
      if Sta.Proc[src].ProcCmd = NODE_None then
        return s10;
      elsif Sta.Proc[src].ProcCmd = NODE_Get then
        return s11;
      else
        return s12;
      endif;
    endif;
  else
    if !Sta.Proc[src].InvMarked then
      if Sta.Proc[src].ProcCmd = NODE_None then
        return s13;
      elsif Sta.Proc[src].ProcCmd = NODE_Get then
        return s14;
      else
        return s15;
      endif;
    else
      if Sta.Proc[src].ProcCmd = NODE_None then
        return s16;
      elsif Sta.Proc[src].ProcCmd = NODE_Get then
        return s17;
      else
        return s18;
      endif;
    endif;
  endif;
end;

function get_dir_state(): FV_CPND_DIR_STATE;
begin
  if !Sta.Dir.HeadVld then
    if !Sta.Dir.Pending then
      if !Sta.Dir.Local then
        if !Sta.Dir.Dirty then
          return dir_s0;
        else
          return dir_s1;
        endif;
      else
        if !Sta.Dir.Dirty then
          return dir_s2;
        else
          return dir_s3;
        endif;
      endif;
    else
      if !Sta.Dir.Local then
        if !Sta.Dir.Dirty then
          return dir_s4;
        else
          return dir_s5;
        endif;
      else
        if !Sta.Dir.Dirty then
          return dir_s6;
        else
          return dir_s7;
        endif;
      endif;
    endif;
  else
    if !Sta.Dir.Pending then
      if !Sta.Dir.Local then
        if !Sta.Dir.Dirty then
          return dir_s8;
        else
          return dir_s9;
        endif;
      else
        if !Sta.Dir.Dirty then
          return dir_s10;
        else
          return dir_s11;
        endif;
      endif;
    else
      if !Sta.Dir.Local then
        if !Sta.Dir.Dirty then
          return dir_s12;
        else
          return dir_s13;
        endif;
      else
        if !Sta.Dir.Dirty then
          return dir_s14;
        else
          return dir_s15;
        endif;
      endif;
    endif;
  endif;
end;

function get_owner_vld(): boolean;
begin
  -- return Sta.Dir.HeadVld | (Sta.Dir.Dirty & Sta.Dir.Local);
  return Sta.Dir.Dirty & (Sta.Dir.Local | Sta.Dir.HeadVld);
end;


function get_owner(): NODE;
begin
  -- Only valid to call when Sta.Dir.Dirty = true
  if Sta.Dir.Local then
    return Home;
  else
    return Sta.Dir.HeadPtr;
  endif;
end;

function sharers_empty(): boolean;
begin
  return !Sta.Dir.HeadVld & !Sta.Dir.ShrVld & !Sta.Dir.Local;
end;

function is_sharer(m: NODE): boolean;
begin
  return !Sta.Dir.Dirty &
    ( ( Sta.Dir.HeadVld & Sta.Dir.HeadPtr = m )
    | ( Sta.Dir.ShrVld  & Sta.Dir.ShrSet[m] )
    | ( Sta.Dir.Local   & m = Home ) );
end;
-- Compound directory state used by analysis scripts.
-- Pending
-- Local 
-- Dirty 
-- ShrVld
-- HeadVld
-------------------------------------------------------------------------------

-------------------------------------------------------------------------------

ruleset h : NODE; d : DATA do
startstate "Init"
  Home := h;
  undefine Sta;
  Sta.MemData := d;
  Sta.Dir.Pending := false;
  Sta.Dir.Local := false;
  Sta.Dir.Dirty := false;
  Sta.Dir.HeadVld := false;
  Sta.Dir.ShrVld := false;
  Sta.WbMsg.Cmd := WB_None;
  Sta.ShWbMsg.Cmd := SHWB_None;
  Sta.NakcMsg.Cmd := NAKC_None;
  for p : NODE do
    Sta.Proc[p].ProcCmd := NODE_None;
    Sta.Proc[p].InvMarked := false;
    Sta.Proc[p].CacheState := CACHE_I;
    Sta.Dir.ShrSet[p] := false;
    Sta.Dir.InvSet[p] := false;
    Sta.UniMsg[p].Cmd := UNI_None;
    Sta.InvMsg[p].Cmd := INV_None;
    Sta.InvMsg[p].Proc := p; -- FVT
    Sta.RpMsg[p].Cmd := RP_None;
  end;
  Sta.CurrData := d;
  Sta.PrevData := d;
  Sta.LastWrVld := false;
  Sta.Collecting := false;
  Sta.FwdCmd := UNI_None;
endstartstate;
endruleset;

-------------------------------------------------------------------------------

-- For FV
ruleset src : NODE do 
rule "Load_S"
  Sta.Proc[src].CacheState = CACHE_S
==>
  get_load_req(src);
-- #RETLD,CL
endrule;

rule "Load_E"
  Sta.Proc[src].CacheState = CACHE_E
==>
  get_load_req(src);
-- #RETLD,CL
endrule;

endruleset;

ruleset src : NODE; data : DATA do
rule "Store"
  Sta.Proc[src].CacheState = CACHE_E
==>
var NxtSta : STATE;
begin
  get_store_req(src, data); -- FVT
  NxtSta := Sta;
--
  NxtSta.Proc[src].CacheData := data;
  NxtSta.CurrData := data;
  NxtSta.LastWrVld := true;
  NxtSta.LastWrPtr := src;
--
  Sta := NxtSta;
endrule;
endruleset;

-- [COMMENT] src:get read request 
ruleset src : NODE do
rule "PI_Remote_Get"
  src != Home &
  Sta.Proc[src].ProcCmd = NODE_None &
  Sta.Proc[src].CacheState = CACHE_I
==>
var NxtSta : STATE;
begin
  get_load_req(src); -- FVT, remote core initiate read request
  NxtSta := Sta;
--
  NxtSta.Proc[src].ProcCmd := NODE_Get;
  NxtSta.UniMsg[src].Cmd := UNI_Get;
  NxtSta.UniMsg[src].Proc := Home;
  -- #SENDING,NxtSta.UniMsg[src],UNI_CMD,src,Home
  undefine NxtSta.UniMsg[src].Data;
--
  Sta := NxtSta;
endrule;
endruleset;

-- [COMMENT] actions of the home when the local processor needs a shared copy of
-- a memory line. 
-- "PI.Local.Get.put" sends a request to a remote if there is a dirty copy (pre- commit step
rule "PI_Local_Get_Get"
  Sta.Proc[Home].ProcCmd = NODE_None &
  Sta.Proc[Home].CacheState = CACHE_I &
  !Sta.Dir.Pending & Sta.Dir.Dirty
==>
var NxtSta : STATE;
begin
  get_load_req(Home); -- FVT, local core initiate read request
  NxtSta := Sta;
--
  NxtSta.Proc[Home].ProcCmd := NODE_Get;
  NxtSta.Dir.Pending := true;
  NxtSta.UniMsg[Home].Cmd := UNI_Get;
  NxtSta.UniMsg[Home].Proc := Sta.Dir.HeadPtr;
  undefine NxtSta.UniMsg[Home].Data;
  -- #SENDING,NxtSta.UniMsg[Home],UNI_CMD,Home,field:Proc
  if (Sta.Dir.HeadPtr != Home) then
    NxtSta.FwdCmd := UNI_Get;
  end;
  NxtSta.PendReqSrc := Home;
  NxtSta.PendReqCmd := UNI_Get;
  NxtSta.Collecting := false;
--
  Sta := NxtSta;
endrule;
-- otherwise (no dirty copy and not pending), it updates the state and data of the local cache which are specification variables (commit step). 
rule "PI_Local_Get_Put"
  Sta.Proc[Home].ProcCmd = NODE_None &
  Sta.Proc[Home].CacheState = CACHE_I &
  !Sta.Dir.Pending & !Sta.Dir.Dirty
==>
var NxtSta : STATE;
begin
  get_load_req(Home); -- FVT, local core initiate read request
  NxtSta := Sta;
--
  NxtSta.Dir.Local := true;
  NxtSta.Proc[Home].ProcCmd := NODE_None;
  if (Sta.Proc[Home].InvMarked) then
    NxtSta.Proc[Home].InvMarked := false;
    NxtSta.Proc[Home].CacheState := CACHE_I;
    undefine NxtSta.Proc[Home].CacheData;
    Sta := NxtSta;
  else
    NxtSta.Proc[Home].CacheState := CACHE_S;
    NxtSta.Proc[Home].CacheData := Sta.MemData;
    Sta := NxtSta;
  -- #RETLD,CL
  end;
--
endrule;

-- [COMMENT] src:get write request 
ruleset mydata: DATA do 
ruleset src : NODE do
rule "PI_Remote_GetX"
  src != Home &
  Sta.Proc[src].ProcCmd = NODE_None &
  Sta.Proc[src].CacheState = CACHE_I
  -- TODO
  -- | Sta.Proc[src].CacheState = CACHE_S ) 
  -- we add the upgrade path here
==>
var NxtSta : STATE;
begin
  get_store_req(src, mydata); -- FVT
  ActiveReq[src] := mydata; -- FVT
  NxtSta := Sta;
--
  NxtSta.Proc[src].ProcCmd := NODE_GetX;
  -- NxtSta.Proc[src].ProcCmdData := data; -- FVT
  NxtSta.UniMsg[src].Cmd := UNI_GetX;
  NxtSta.UniMsg[src].Proc := Home;
  -- #SENDING,NxtSta.UniMsg[src],UNI_CMD,src,Home
  undefine NxtSta.UniMsg[src].Data;
--
  Sta := NxtSta;
endrule;
endruleset;

rule "PI_Local_GetX_GetX"
  Sta.Proc[Home].ProcCmd = NODE_None &
  ( Sta.Proc[Home].CacheState = CACHE_I |
    Sta.Proc[Home].CacheState = CACHE_S ) &
  !Sta.Dir.Pending & Sta.Dir.Dirty
==>
var NxtSta : STATE;
begin
  get_store_req(Home, mydata); -- FVT
  ActiveReq[Home] := mydata; -- FVT
  NxtSta := Sta;
--
  NxtSta.Proc[Home].ProcCmd := NODE_GetX;
  -- NxtSta.Proc[Home].ProcCmdData := data; -- FVT
  NxtSta.Dir.Pending := true;
  NxtSta.UniMsg[Home].Cmd := UNI_GetX;
  NxtSta.UniMsg[Home].Proc := Sta.Dir.HeadPtr;
  -- #SENDING,NxtSta.UniMsg[Home],UNI_CMD,Home,field:Proc
  undefine NxtSta.UniMsg[Home].Data;
  if (Sta.Dir.HeadPtr != Home) then
    NxtSta.FwdCmd := UNI_GetX;
  end;
  NxtSta.PendReqSrc := Home;
  NxtSta.PendReqCmd := UNI_GetX;
  NxtSta.Collecting := false;
--
  Sta := NxtSta;
endrule;

rule "PI_Local_GetX_PutX"
  Sta.Proc[Home].ProcCmd = NODE_None &
  ( Sta.Proc[Home].CacheState = CACHE_I |
    Sta.Proc[Home].CacheState = CACHE_S ) &
  !Sta.Dir.Pending & !Sta.Dir.Dirty
==>
var NxtSta : STATE;
begin
  get_store_req(Home, mydata); -- FVT
  ActiveReq[Home] := mydata; -- FVT
  NxtSta := Sta;
--
  NxtSta.Dir.Local := true;
  NxtSta.Dir.Dirty := true;
  if (Sta.Dir.HeadVld) then
    NxtSta.Dir.Pending := true;
    NxtSta.Dir.HeadVld := false;
    undefine NxtSta.Dir.HeadPtr;
    NxtSta.Dir.ShrVld := false;
    for p : NODE do
      NxtSta.Dir.ShrSet[p] := false;
      if ( p != Home &
           ( Sta.Dir.ShrVld & Sta.Dir.ShrSet[p] |
             Sta.Dir.HeadVld & Sta.Dir.HeadPtr = p ) ) then
        NxtSta.Dir.InvSet[p] := true;
        NxtSta.InvMsg[p].Cmd := INV_Inv;
        -- #SENDING,NxtSta.InvMsg[p],INV_CMD,Home,p
      else
        NxtSta.Dir.InvSet[p] := false;
        NxtSta.InvMsg[p].Cmd := INV_None;
      end;
    end;
    NxtSta.Collecting := true;
    NxtSta.PrevData := Sta.CurrData;
    NxtSta.LastOtherInvAck := Sta.Dir.HeadPtr;
  end;
  NxtSta.Proc[Home].ProcCmd := NODE_None;
  NxtSta.Proc[Home].InvMarked := false;
  NxtSta.Proc[Home].CacheState := CACHE_E;
  -- NxtSta.Proc[Home].CacheData := Sta.MemData;
  -- TODO
  NxtSta.Proc[Home].CacheData := ActiveReq[Home]; -- FVT
  undefine ActiveReq[Home];
--
  Sta := NxtSta;
endrule;
endruleset;

ruleset dst : NODE do
rule "PI_Remote_PutX"
  dst != Home &
  Sta.Proc[dst].ProcCmd = NODE_None &
  Sta.Proc[dst].CacheState = CACHE_E
==>
var NxtSta : STATE;
begin
  get_evict_req(dst);
  NxtSta := Sta;
--
  NxtSta.Proc[dst].CacheState := CACHE_I;
  undefine NxtSta.Proc[dst].CacheData;
  NxtSta.WbMsg.Cmd := WB_Wb;
  NxtSta.WbMsg.Proc := dst;
  NxtSta.WbMsg.Data := Sta.Proc[dst].CacheData;
  -- #SENDING,NxtSta.WbMsg,WB_CMD,field:Proc,Home
--
  Sta := NxtSta;
endrule;
endruleset;

rule "PI_Local_PutX"
  Sta.Proc[Home].ProcCmd = NODE_None &
  Sta.Proc[Home].CacheState = CACHE_E
==>
var NxtSta : STATE;
begin
  get_evict_req(Home);
  NxtSta := Sta;
--
  if (Sta.Dir.Pending) then
    NxtSta.Proc[Home].CacheState := CACHE_I;
    undefine NxtSta.Proc[Home].CacheData;
    NxtSta.Dir.Dirty := false;
    NxtSta.MemData := Sta.Proc[Home].CacheData;
  else
    NxtSta.Proc[Home].CacheState := CACHE_I;
    undefine NxtSta.Proc[Home].CacheData;
    NxtSta.Dir.Local := false;
    NxtSta.Dir.Dirty := false;
    NxtSta.MemData := Sta.Proc[Home].CacheData;
  end;
--
  Sta := NxtSta;
endrule;

ruleset src : NODE do
rule "PI_Remote_Replace"
  src != Home &
  Sta.Proc[src].ProcCmd = NODE_None &
  Sta.Proc[src].CacheState = CACHE_S
==>
var NxtSta : STATE;
begin
  get_evict_req(src);
  NxtSta := Sta;
--
  NxtSta.Proc[src].CacheState := CACHE_I;
  undefine NxtSta.Proc[src].CacheData;
  NxtSta.RpMsg[src].Cmd := RP_Replace;
  -- #SENDING,NxtSta.RpMsg[src],RP_CMD,src,Home
--
  Sta := NxtSta;
endrule;
endruleset;

rule "PI_Local_Replace"
  Sta.Proc[Home].ProcCmd = NODE_None &
  Sta.Proc[Home].CacheState = CACHE_S
==>
var NxtSta : STATE;
begin
  get_evict_req(Home);
  NxtSta := Sta;
--
  NxtSta.Dir.Local := false;
  NxtSta.Proc[Home].CacheState := CACHE_I;
  undefine NxtSta.Proc[Home].CacheData;
--
  Sta := NxtSta;
endrule;

-- a node receiving a NAK reply. The processor clears its waiting flag and invalidation mark.
ruleset dst : NODE do
rule "NI_Nak"
  Sta.UniMsg[dst].Cmd = UNI_Nak
==>
var NxtSta : STATE;
begin
  NxtSta := Sta;
--
  -- #RECEIVING,Sta.UniMsg[dst],UNI_CMD,field:Proc,dst
  NxtSta.UniMsg[dst].Cmd := UNI_None;
  undefine NxtSta.UniMsg[dst].Proc;
  undefine NxtSta.UniMsg[dst].Data;
  NxtSta.Proc[dst].ProcCmd := NODE_None;
  NxtSta.Proc[dst].InvMarked := false;
--
  Sta := NxtSta;
endrule;
endruleset;

-- this handler describes actions of the home receiving a NAKC. Pending is reset.
rule "NI_Nak_Clear"
  Sta.NakcMsg.Cmd = NAKC_Nakc
==>
var NxtSta : STATE;
begin
  NxtSta := Sta;
--
  -- #RECEIVING,Sta.NakcMsg,NAKC_CMD,Unknown,Home
  NxtSta.NakcMsg.Cmd := NAKC_None;
  NxtSta.Dir.Pending := false;
--
  Sta := NxtSta;
endrule;

-- home receiving a GET from a remote; If Pending, the home sends a NAK to the source.
ruleset src : NODE do
rule "NI_Local_Get_Nak"
  src != Home &
  Sta.UniMsg[src].Cmd = UNI_Get &
  Sta.UniMsg[src].Proc = Home &
  Sta.RpMsg[src].Cmd != RP_Replace &
  ( Sta.Dir.Pending |
    Sta.Dir.Dirty & Sta.Dir.Local & Sta.Proc[Home].CacheState != CACHE_E |
    Sta.Dir.Dirty & !Sta.Dir.Local & Sta.Dir.HeadPtr = src )
==>
var NxtSta : STATE;
begin
  NxtSta := Sta;
--
  -- Home is the receiving from src 
  -- #RECEIVING,Sta.UniMsg[src],UNI_CMD,src,Home
  NxtSta.UniMsg[src].Cmd := UNI_Nak;
  NxtSta.UniMsg[src].Proc := Home;
  undefine NxtSta.UniMsg[src].Data;
  -- Home is sending to src
  -- #SENDING,NxtSta.UniMsg[src],UNI_CMD,Home,src
--
  Sta := NxtSta;
endrule;
endruleset;

ruleset src : NODE do
rule "NI_Local_Get_Get"
  src != Home &
  Sta.UniMsg[src].Cmd = UNI_Get &
  Sta.UniMsg[src].Proc = Home &
  Sta.RpMsg[src].Cmd != RP_Replace &
  !Sta.Dir.Pending & Sta.Dir.Dirty & !Sta.Dir.Local & Sta.Dir.HeadPtr != src
==>
var NxtSta : STATE;
begin
  NxtSta := Sta;
--
  -- #RECEIVING,Sta.UniMsg[src],UNI_CMD,src,Home
  NxtSta.Dir.Pending := true;
  NxtSta.UniMsg[src].Cmd := UNI_Get;
  NxtSta.UniMsg[src].Proc := Sta.Dir.HeadPtr;
  -- #SENDING,NxtSta.UniMsg[src],UNI_CMD,Home,field:Proc
  undefine NxtSta.UniMsg[src].Data;
  if (Sta.Dir.HeadPtr != Home) then
    NxtSta.FwdCmd := UNI_Get;
  end;
  NxtSta.PendReqSrc := src;
  NxtSta.PendReqCmd := UNI_Get;
  NxtSta.Collecting := false;
--
  Sta := NxtSta;
endrule;
endruleset;

ruleset src : NODE do
rule "NI_Local_Get_Put"
  src != Home &
  Sta.UniMsg[src].Cmd = UNI_Get &
  Sta.UniMsg[src].Proc = Home &
  Sta.RpMsg[src].Cmd != RP_Replace &
  !Sta.Dir.Pending &
  (Sta.Dir.Dirty -> Sta.Dir.Local & Sta.Proc[Home].CacheState = CACHE_E)
--  !Sta.Proc[src].InvMarked
==>
var NxtSta : STATE;
begin
  NxtSta := Sta;
--
   -- #RECEIVING,Sta.UniMsg[src],UNI_CMD,src,Home
  if (Sta.Dir.Dirty) then
    NxtSta.Dir.Dirty := false;
    NxtSta.Dir.HeadVld := true;
    NxtSta.Dir.HeadPtr := src;
    NxtSta.MemData := Sta.Proc[Home].CacheData;
    NxtSta.Proc[Home].CacheState := CACHE_S;
    NxtSta.UniMsg[src].Cmd := UNI_Put;
    NxtSta.UniMsg[src].Proc := Home;
    NxtSta.UniMsg[src].Data := Sta.Proc[Home].CacheData;
    -- #SENDING,NxtSta.UniMsg[src],UNI_CMD,Home,src
  else
    if (Sta.Dir.HeadVld) then
      NxtSta.Dir.ShrVld := true;
      NxtSta.Dir.ShrSet[src] := true;
      for p : NODE do
        NxtSta.Dir.InvSet[p] := (p = src) | Sta.Dir.ShrSet[p];
      end;
    else
      NxtSta.Dir.HeadVld := true;
      NxtSta.Dir.HeadPtr := src;
    end;
    NxtSta.UniMsg[src].Cmd := UNI_Put;
    NxtSta.UniMsg[src].Proc := Home;
    NxtSta.UniMsg[src].Data := Sta.MemData;
    -- #SENDING,NxtSta.UniMsg[src],UNI_CMD,Home,src
  end;
--
  Sta := NxtSta;
endrule;
endruleset;

ruleset src : NODE; dst : NODE do
rule "NI_Remote_Get_Nak"
  src != dst & dst != Home &
  Sta.UniMsg[src].Cmd = UNI_Get &
  Sta.UniMsg[src].Proc = dst &
  Sta.Proc[dst].CacheState != CACHE_E
==>
var NxtSta : STATE;
begin
  NxtSta := Sta;
--
  -- #RECEIVING,Sta.UniMsg[src],UNI_CMD,src,dst
  NxtSta.UniMsg[src].Cmd := UNI_Nak;
  NxtSta.UniMsg[src].Proc := dst;
  -- #SENDING,NxtSta.UniMsg[src],UNI_CMD,dst,src
  undefine NxtSta.UniMsg[src].Data;
  NxtSta.NakcMsg.Cmd := NAKC_Nakc;
  -- #SENDING,NxtSta.NakcMsg,NAKC_CMD,dst,Home
  NxtSta.FwdCmd := UNI_None;
  NxtSta.FwdSrc := src;
--
  Sta := NxtSta;
endrule;
endruleset;

ruleset src : NODE; dst : NODE do
rule "NI_Remote_Get_Put"
  src != dst & dst != Home &
  Sta.UniMsg[src].Cmd = UNI_Get &
  Sta.UniMsg[src].Proc = dst &
  Sta.Proc[dst].CacheState = CACHE_E
--  !Sta.Proc[src].InvMarked
==>
var NxtSta : STATE;
begin
  NxtSta := Sta;
--
  -- cur should be dst
  -- #RECEIVING,Sta.UniMsg[src],UNI_CMD,src,dst
  NxtSta.Proc[dst].CacheState := CACHE_S;
  NxtSta.UniMsg[src].Cmd := UNI_Put;
  NxtSta.UniMsg[src].Proc := dst;
  NxtSta.UniMsg[src].Data := Sta.Proc[dst].CacheData;
  -- #SENDING,NxtSta.UniMsg[src],UNI_CMD,dst,src
  if (src != Home) then
    NxtSta.ShWbMsg.Cmd := SHWB_ShWb;
    NxtSta.ShWbMsg.Proc := src;
    NxtSta.ShWbMsg.Data := Sta.Proc[dst].CacheData;
    -- #SENDING,NxtSta.ShWbMsg,SHWB_CMD,dst,Home
  end;
  NxtSta.FwdCmd := UNI_None;
  NxtSta.FwdSrc := src;
--
  Sta := NxtSta;
endrule;
endruleset;

ruleset src : NODE do
rule "NI_Local_GetX_Nak"
  src != Home &
  Sta.UniMsg[src].Cmd = UNI_GetX &
  Sta.UniMsg[src].Proc = Home &
  ( Sta.Dir.Pending |
    Sta.Dir.Dirty & Sta.Dir.Local & Sta.Proc[Home].CacheState != CACHE_E |
    Sta.Dir.Dirty & !Sta.Dir.Local & Sta.Dir.HeadPtr = src )
==>
var NxtSta : STATE;
begin
  NxtSta := Sta;
--
  -- home receives
  -- #RECEIVING,Sta.UniMsg[src],UNI_CMD,src,Home
  NxtSta.UniMsg[src].Cmd := UNI_Nak;
  NxtSta.UniMsg[src].Proc := Home;
  -- home sends out to src
  -- #SENDING,NxtSta.UniMsg[src],UNI_CMD,Home,src
  undefine NxtSta.UniMsg[src].Data;
--
  Sta := NxtSta;
endrule;
endruleset;

ruleset src : NODE do
rule "NI_Local_GetX_GetX"
  src != Home &
  Sta.UniMsg[src].Cmd = UNI_GetX &
  Sta.UniMsg[src].Proc = Home &
  !Sta.Dir.Pending & Sta.Dir.Dirty & !Sta.Dir.Local & Sta.Dir.HeadPtr != src
==>
var NxtSta : STATE;
begin
  NxtSta := Sta;
--
  -- home receives
  -- #RECEIVING,Sta.UniMsg[src],UNI_CMD,src,Home
  NxtSta.Dir.Pending := true;
  NxtSta.UniMsg[src].Cmd := UNI_GetX;
  NxtSta.UniMsg[src].Proc := Sta.Dir.HeadPtr;
  -- #SENDING,NxtSta.UniMsg[src],UNI_CMD,Home,field:Proc
  undefine NxtSta.UniMsg[src].Data;
  if (Sta.Dir.HeadPtr != Home) then
    NxtSta.FwdCmd := UNI_GetX;
  end;
  NxtSta.PendReqSrc := src;
  NxtSta.PendReqCmd := UNI_GetX;
  NxtSta.Collecting := false;
--
  Sta := NxtSta;
endrule;
endruleset;

ruleset src : NODE do
rule "NI_Local_GetX_PutX"
  src != Home &
  Sta.UniMsg[src].Cmd = UNI_GetX &
  Sta.UniMsg[src].Proc = Home &
  !Sta.Dir.Pending &
  (Sta.Dir.Dirty -> Sta.Dir.Local & Sta.Proc[Home].CacheState = CACHE_E)
==>
var NxtSta : STATE;
begin
  NxtSta := Sta;
--
  -- home receives
  -- #RECEIVING,Sta.UniMsg[src],UNI_CMD,src,Home
  if (Sta.Dir.Dirty) then
    NxtSta.Dir.Local := false;
    NxtSta.Dir.Dirty := true;
    NxtSta.Dir.HeadVld := true;
    NxtSta.Dir.HeadPtr := src;
    NxtSta.Dir.ShrVld := false;
    for p : NODE do
      NxtSta.Dir.ShrSet[p] := false;
      NxtSta.Dir.InvSet[p] := false;
    end;
    NxtSta.UniMsg[src].Cmd := UNI_PutX;
    NxtSta.UniMsg[src].Proc := Home;
    NxtSta.UniMsg[src].Data := Sta.Proc[Home].CacheData;
    -- #SENDING,NxtSta.UniMsg[src],UNI_CMD,Home,src
    NxtSta.Proc[Home].CacheState := CACHE_I;
    undefine NxtSta.Proc[Home].CacheData;
  elsif (Sta.Dir.HeadVld ->
         Sta.Dir.HeadPtr = src  &
         forall p : NODE do p != src -> !Sta.Dir.ShrSet[p] end) then
    NxtSta.Dir.Local := false;
    NxtSta.Dir.Dirty := true;
    NxtSta.Dir.HeadVld := true;
    NxtSta.Dir.HeadPtr := src;
    NxtSta.Dir.ShrVld := false;
    for p : NODE do
      NxtSta.Dir.ShrSet[p] := false;
      NxtSta.Dir.InvSet[p] := false;
    end;
    NxtSta.UniMsg[src].Cmd := UNI_PutX;
    NxtSta.UniMsg[src].Proc := Home;
    NxtSta.UniMsg[src].Data := Sta.MemData;
    -- #SENDING,NxtSta.UniMsg[src],UNI_CMD,Home,src
    NxtSta.Proc[Home].CacheState := CACHE_I;
    undefine NxtSta.Proc[Home].CacheData;
    if (Sta.Dir.Local) then
      NxtSta.Proc[Home].CacheState := CACHE_I;
      undefine NxtSta.Proc[Home].CacheData;
      if (Sta.Proc[Home].ProcCmd = NODE_Get) then
        NxtSta.Proc[Home].InvMarked := true;
      end;
    end;
  else
    NxtSta.Dir.Pending := true;
    NxtSta.Dir.Local := false;
    NxtSta.Dir.Dirty := true;
    NxtSta.Dir.HeadVld := true;
    NxtSta.Dir.HeadPtr := src;
    NxtSta.Dir.ShrVld := false;
    for p : NODE do
      NxtSta.Dir.ShrSet[p] := false;
      if ( p != Home & p != src &
           ( Sta.Dir.ShrVld & Sta.Dir.ShrSet[p] |
             Sta.Dir.HeadVld & Sta.Dir.HeadPtr = p ) ) then
        NxtSta.Dir.InvSet[p] := true;
        NxtSta.InvMsg[p].Cmd := INV_Inv;
        -- #SENDING,NxtSta.InvMsg[p],INV_CMD,Home,p
      else
        NxtSta.Dir.InvSet[p] := false;
        NxtSta.InvMsg[p].Cmd := INV_None;
      end;
    end;
    NxtSta.UniMsg[src].Cmd := UNI_PutX;
    NxtSta.UniMsg[src].Proc := Home;
    NxtSta.UniMsg[src].Data := Sta.MemData;
    -- #SENDING,NxtSta.UniMsg[src],UNI_CMD,Home,src
    if (Sta.Dir.Local) then
      NxtSta.Proc[Home].CacheState := CACHE_I;
      undefine NxtSta.Proc[Home].CacheData;
      if (Sta.Proc[Home].ProcCmd = NODE_Get) then
        NxtSta.Proc[Home].InvMarked := true;
      end;
    end;
    NxtSta.PendReqSrc := src;
    NxtSta.PendReqCmd := UNI_GetX;
    NxtSta.Collecting := true;
    NxtSta.PrevData := Sta.CurrData;
    if (Sta.Dir.HeadPtr != src) then
      NxtSta.LastOtherInvAck := Sta.Dir.HeadPtr;
    else
      for p : NODE do
        if (p != src & Sta.Dir.ShrSet[p]) then NxtSta.LastOtherInvAck := p end;
      end;
    end;
  end;
--
  Sta := NxtSta;
endrule;
endruleset;

ruleset src : NODE; dst : NODE do
rule "NI_Remote_GetX_Nak"
  src != dst & dst != Home &
  Sta.UniMsg[src].Cmd = UNI_GetX &
  Sta.UniMsg[src].Proc = dst &
  Sta.Proc[dst].CacheState != CACHE_E
==>
var NxtSta : STATE;
begin
  NxtSta := Sta;
--
  -- dst receives here UNI_GetX from src
  -- #RECEIVING,Sta.UniMsg[src],UNI_CMD,src,dst
  NxtSta.UniMsg[src].Cmd := UNI_Nak;
  NxtSta.UniMsg[src].Proc := dst;
  -- #SENDING,NxtSta.UniMsg[src],UNI_CMD,dst,src
  undefine NxtSta.UniMsg[src].Data;
  NxtSta.NakcMsg.Cmd := NAKC_Nakc;
  -- #SENDING,NxtSta.NakcMsg,NAKC_CMD,dst,Home
  NxtSta.FwdCmd := UNI_None;
  NxtSta.FwdSrc := src;
--
  Sta := NxtSta;
endrule;
endruleset;

ruleset src : NODE; dst : NODE do
rule "NI_Remote_GetX_PutX"
  src != dst & dst != Home &
  Sta.UniMsg[src].Cmd = UNI_GetX &
  Sta.UniMsg[src].Proc = dst &
  Sta.Proc[dst].CacheState = CACHE_E
--  !Sta.Proc[src].InvMarked
==>
var NxtSta : STATE;
begin
  NxtSta := Sta;
--
  -- #RECEIVING,Sta.UniMsg[src],UNI_CMD,src,dst
  NxtSta.Proc[dst].CacheState := CACHE_I;
  undefine NxtSta.Proc[dst].CacheData;
  NxtSta.UniMsg[src].Cmd := UNI_PutX;
  NxtSta.UniMsg[src].Proc := dst;
  NxtSta.UniMsg[src].Data := Sta.Proc[dst].CacheData;
  -- #SENDING,NxtSta.UniMsg[src],UNI_CMD,dst,src
  if (src != Home) then
    NxtSta.ShWbMsg.Cmd := SHWB_FAck;
    NxtSta.ShWbMsg.Proc := src;
    undefine NxtSta.ShWbMsg.Data;
    -- #SENDING,NxtSta.ShWbMsg,SHWB_CMD,dst,Home
  end;
  NxtSta.FwdCmd := UNI_None;
  NxtSta.FwdSrc := src;
--
  Sta := NxtSta;
endrule;
endruleset;

rule "NI_Local_Put"
  Sta.UniMsg[Home].Cmd = UNI_Put
==>
var NxtSta : STATE;
begin
  NxtSta := Sta;
--
  -- #RECEIVING,Sta.UniMsg[Home],UNI_CMD,field:Proc,Home
  NxtSta.UniMsg[Home].Cmd := UNI_None;
  undefine NxtSta.UniMsg[Home].Proc;
  undefine NxtSta.UniMsg[Home].Data;
  NxtSta.Dir.Pending := false;
  NxtSta.Dir.Dirty := false;
  NxtSta.Dir.Local := true;
  NxtSta.MemData := Sta.UniMsg[Home].Data;
  NxtSta.Proc[Home].ProcCmd := NODE_None;
  if (Sta.Proc[Home].InvMarked) then
    NxtSta.Proc[Home].InvMarked := false;
    NxtSta.Proc[Home].CacheState := CACHE_I;
    undefine NxtSta.Proc[Home].CacheData;
  Sta := NxtSta;
  else
    NxtSta.Proc[Home].CacheState := CACHE_S;
    NxtSta.Proc[Home].CacheData := Sta.UniMsg[Home].Data;
  Sta := NxtSta;
  -- #RETLD,CL
  end;
--
endrule;

ruleset dst : NODE do
rule "NI_Remote_Put"
  dst != Home &
  Sta.UniMsg[dst].Cmd = UNI_Put
==>
var NxtSta : STATE;
begin
  NxtSta := Sta;
--
  -- #RECEIVING,Sta.UniMsg[dst],UNI_CMD,field:Proc,dst
  NxtSta.UniMsg[dst].Cmd := UNI_None;
  undefine NxtSta.UniMsg[dst].Proc;
  undefine NxtSta.UniMsg[dst].Data;
  NxtSta.Proc[dst].ProcCmd := NODE_None;
  if (Sta.Proc[dst].InvMarked) then
    NxtSta.Proc[dst].InvMarked := false;
    NxtSta.Proc[dst].CacheState := CACHE_I;
    undefine NxtSta.Proc[dst].CacheData;
  Sta := NxtSta;
  else
    NxtSta.Proc[dst].CacheState := CACHE_S;
    NxtSta.Proc[dst].CacheData := Sta.UniMsg[dst].Data;
  Sta := NxtSta;
  -- #RETLD,CL
  end;
--
endrule;
endruleset;

rule "NI_Local_PutXAcksDone"
  Sta.UniMsg[Home].Cmd = UNI_PutX
==>
var NxtSta : STATE;
begin
  NxtSta := Sta;
--
  -- #RECEIVING,Sta.UniMsg[Home],UNI_CMD,field:Proc,Home
  NxtSta.UniMsg[Home].Cmd := UNI_None;
  undefine NxtSta.UniMsg[Home].Proc;
  undefine NxtSta.UniMsg[Home].Data;
  NxtSta.Dir.Pending := false;
  NxtSta.Dir.Local := true;
  NxtSta.Dir.HeadVld := false;
  undefine NxtSta.Dir.HeadPtr;
  NxtSta.Proc[Home].ProcCmd := NODE_None;
  NxtSta.Proc[Home].InvMarked := false;
  NxtSta.Proc[Home].CacheState := CACHE_E;
  -- TODO
  -- NxtSta.Proc[Home].CacheData := Sta.UniMsg[Home].Data;
  NxtSta.Proc[Home].CacheData := ActiveReq[Home]; -- FVT
  undefine ActiveReq[Home];
--
  Sta := NxtSta;
endrule;

-- The exclusive copy is put into the cache.
ruleset dst : NODE do
rule "NI_Remote_PutX"
  dst != Home &
  Sta.UniMsg[dst].Cmd = UNI_PutX &
  Sta.Proc[dst].ProcCmd = NODE_GetX
==>
var NxtSta : STATE;
begin
  NxtSta := Sta;
--
  -- #RECEIVING,Sta.UniMsg[dst],UNI_CMD,field:Proc,dst
  NxtSta.UniMsg[dst].Cmd := UNI_None;
  undefine NxtSta.UniMsg[dst].Proc;
  undefine NxtSta.UniMsg[dst].Data;
  NxtSta.Proc[dst].ProcCmd := NODE_None;
  NxtSta.Proc[dst].InvMarked := false;
  NxtSta.Proc[dst].CacheState := CACHE_E;
  -- TODO
  NxtSta.Proc[dst].CacheData := Sta.UniMsg[dst].Data;
  NxtSta.Proc[dst].CacheData := ActiveReq[dst]; -- FVT
  undefine ActiveReq[dst];
--
  Sta := NxtSta;
endrule;
endruleset;

-- the remote, receiving INV, invalidate the cached copy and send INVAK to Home
ruleset dst : NODE do
rule "NI_Inv"
  dst != Home &
  Sta.InvMsg[dst].Cmd = INV_Inv
==>
var NxtSta : STATE;
begin
  NxtSta := Sta;
--
  -- #RECEIVING,Sta.InvMsg[dst],INV_CMD,Home,dst
  NxtSta.InvMsg[dst].Cmd := INV_InvAck;
  -- #SENDING,NxtSta.InvMsg[dst],INV_CMD,dst,Home
  NxtSta.Proc[dst].CacheState := CACHE_I;
  undefine NxtSta.Proc[dst].CacheData;
  if (Sta.Proc[dst].ProcCmd = NODE_Get) then
    NxtSta.Proc[dst].InvMarked := true;
  end;
--
  Sta := NxtSta;
endrule;
endruleset;

---- This rule is wrong!! Collecting is set to false once invacks are received from concrete procs
---- Thus invacks from "Other" are thrown away! Could have been caught by some kind of syntax checker....

-- home receiving an INVAK
ruleset src : NODE do
rule "NI_InvAck"
  src != Home &
  Sta.InvMsg[src].Cmd = INV_InvAck &
  Sta.Dir.Pending & Sta.Dir.InvSet[src]  
==>
var NxtSta : STATE;
begin
  NxtSta := Sta;
--
  -- #RECEIVING,Sta.InvMsg[src],INV_CMD,src,Home
  NxtSta.InvMsg[src].Cmd := INV_None;
  NxtSta.Dir.InvSet[src] := false;
  if (exists p : NODE do p != src & Sta.Dir.InvSet[p] end) then
    NxtSta.LastInvAck := src;
    for p : NODE do
      if (p != src & Sta.Dir.InvSet[p]) then
        NxtSta.LastOtherInvAck := p;
      end;
    end;
  else
    NxtSta.Dir.Pending := false;
    if (Sta.Dir.Local & !Sta.Dir.Dirty) then
      NxtSta.Dir.Local := false;
    end;
    NxtSta.Collecting := false;
    NxtSta.LastInvAck := src;
  end;
--
  Sta := NxtSta;
endrule;
endruleset;

-- home receiving a wb
rule "NI_Wb"
  Sta.WbMsg.Cmd = WB_Wb
==>
var NxtSta : STATE;
begin
  NxtSta := Sta;
--
-- #RECEIVING,Sta.WbMsg,WB_CMD,field:Proc,Home
  NxtSta.WbMsg.Cmd := WB_None;
  undefine NxtSta.WbMsg.Proc;
  undefine NxtSta.WbMsg.Data;
  NxtSta.Dir.Dirty := false;
  NxtSta.Dir.HeadVld := false;
  undefine NxtSta.Dir.HeadPtr;
  NxtSta.MemData := Sta.WbMsg.Data;
--
  Sta := NxtSta;
endrule;

-- Home receiving a foward ack 
rule "NI_FAck"
  Sta.ShWbMsg.Cmd = SHWB_FAck
==>
var NxtSta : STATE;
begin
  NxtSta := Sta;
--
  -- #RECEIVING,Sta.ShWbMsg,SHWB_CMD,Unknown,Home
  NxtSta.ShWbMsg.Cmd := SHWB_None;
  undefine NxtSta.ShWbMsg.Proc;
  undefine NxtSta.ShWbMsg.Data;
  NxtSta.Dir.Pending := false;
  if (Sta.Dir.Dirty) then
    NxtSta.Dir.HeadPtr := Sta.ShWbMsg.Proc;
  end;
--
  Sta := NxtSta;
endrule;

rule "NI_ShWb"
  Sta.ShWbMsg.Cmd = SHWB_ShWb
==>
var NxtSta : STATE;
begin
  NxtSta := Sta;
--
  -- #RECEIVING,Sta.ShWbMsg,SHWB_CMD,Unknown,Home
  NxtSta.ShWbMsg.Cmd := SHWB_None;
  undefine NxtSta.ShWbMsg.Proc;
  undefine NxtSta.ShWbMsg.Data;
  NxtSta.Dir.Pending := false;
  NxtSta.Dir.Dirty := false;
  NxtSta.Dir.ShrVld := true;
--  NxtSta.Dir.ShrSet[Sta.ShWbMsg.Proc] := true;
  for p : NODE do
    NxtSta.Dir.ShrSet[p] := (p = Sta.ShWbMsg.Proc) | Sta.Dir.ShrSet[p];
    NxtSta.Dir.InvSet[p] := (p = Sta.ShWbMsg.Proc) | Sta.Dir.ShrSet[p];
  end;
  NxtSta.MemData := Sta.ShWbMsg.Data;
--
  Sta := NxtSta;
endrule;

ruleset src : NODE do
rule "NI_Replace"
  Sta.RpMsg[src].Cmd = RP_Replace
==>
var NxtSta : STATE;
begin
  NxtSta := Sta;
--
  -- #RECEIVING,Sta.RpMsg[src],RP_CMD,src,Home
  NxtSta.RpMsg[src].Cmd := RP_None;
  if (Sta.Dir.ShrVld) then
    NxtSta.Dir.ShrSet[src] := false;
    NxtSta.Dir.InvSet[src] := false;
  end;
--
  Sta := NxtSta;
endrule;
endruleset;

-- -------------------------------------------------------------------------------
-- 
-- invariant "CacheStateProp"
--   forall p : NODE do forall q : NODE do
--     p != q ->
--     !(Sta.Proc[p].CacheState = CACHE_E & Sta.Proc[q].CacheState = CACHE_E)
--   end end;
-- 
-- invariant "CacheDataProp"
--   forall p : NODE do
--     ( Sta.Proc[p].CacheState = CACHE_E ->
--       Sta.Proc[p].CacheData = Sta.CurrData ) &
--     ( Sta.Proc[p].CacheState = CACHE_S ->
--       ( Sta.Collecting -> Sta.Proc[p].CacheData = Sta.PrevData ) &
--       (!Sta.Collecting -> Sta.Proc[p].CacheData = Sta.CurrData ) )
--   end;
-- 
-- invariant "MemDataProp"
--   !Sta.Dir.Dirty -> Sta.MemData = Sta.CurrData;

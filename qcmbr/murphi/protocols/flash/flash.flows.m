--| Variable declarations
const
    NODE_NUM : 3;
    DATA_NUM : 1;
    BUF_SIZE : 4;
    TRANS_SIZE : 2;
type
    NODE : scalarset(NODE_NUM);
    absNODE : union { NODE, enum { Other } };
    DATA : scalarset(DATA_NUM);
    BUF_IND : 0..BUF_SIZE - 1;
    BUF_INDP : 0..BUF_SIZE;
    TRANS_IND : 0..TRANS_SIZE - 1;
    TRANS_INDP : 0..TRANS_SIZE;
    --absNODE : union { NODE, enum { Other } };
    CACHE_STATE : enum { CACHE_I, CACHE_S, CACHE_E };
    NODE_CMD : enum { NODE_None, NODE_Get, NODE_GetX };
    NODE_STATE : record
        ProcCmd : NODE_CMD;
        InvMarked : boolean;
        CacheState : CACHE_STATE;
        CacheData : DATA;
    end;
    DIR_STATE : record
        Pending : boolean;
        Local : boolean;
        Dirty : boolean;
        HeadVld : boolean;
        HeadPtr : absNODE;
        ShrVld : boolean;
        ShrSet : array[NODE] of boolean;
        InvSet : array[NODE] of boolean;
    end;
    UNI_CMD : enum { UNI_None, UNI_Get, UNI_GetX, UNI_Put, UNI_PutX, UNI_Nak };
    UNI_MSG : record
        Cmd : UNI_CMD;
        Proc : absNODE;
        Data : DATA;
    end;
    INV_CMD : enum { INV_None, INV_Inv, INV_InvAck };
    INV_MSG : record
        Cmd : INV_CMD;
    end;
    RP_CMD : enum { RP_None, RP_Replace };
    RP_MSG : record
        Cmd : RP_CMD;
    end;
    WB_CMD : enum { WB_None, WB_Wb };
    WB_MSG : record
        Cmd : WB_CMD;
        Proc : absNODE;
        Data : DATA;
    end;
    SHWB_CMD : enum { SHWB_None, SHWB_ShWb, SHWB_FAck };
    SHWB_MSG : record
        Cmd : SHWB_CMD;
        Proc : absNODE;
        Data : DATA;
    end;
    NAKC_CMD : enum { NAKC_None, NAKC_Nakc };
    NAKC_MSG : record
        Cmd : NAKC_CMD;
    end;
    STATE : record
        Proc : array[NODE] of NODE_STATE;
        Dir : DIR_STATE;
        MemData : DATA;
        UniMsg : array[NODE] of UNI_MSG;
        InvMsg : array[NODE] of INV_MSG;
        RpMsg : array[NODE] of RP_MSG;
        WbMsg : WB_MSG;
        ShWbMsg : SHWB_MSG;
        NakcMsg : NAKC_MSG;
        Collecting: boolean;
    end;
    MSG_CMD : enum { Empty, ReqS, ReqE, Inv, InvAck, GntS, GntE };
    MSG : record
        Cmd : MSG_CMD;
        Data : DATA;
    end;
    RNAME : enum { Norule, Store, PI_Remote_Get, PI_Local_Get_Get,
                   PI_Local_Get_Put, NI_Remote_GetX, PI_Local_GetX_GetX,
                   PI_Local_GetX_PutX, PI_Remote_PutX, PI_Local_PutX,
                   PI_Remote_Replace, PI_Local_Replace, NI_Nak, NI_Nak_Clear,
                   NI_Local_Get_Nak, NI_Local_Get_Get, NI_Local_Get_Put,
                   NI_Remote_Get_Nak, NI_Remote_Get_Put, NI_Local_GetX_Nak,
                   NI_Local_GetX_GetX, NI_Local_GetX_PutX,
                   NI_Remote_GetX_Nak, NI_Remote_GetX_PutX, NI_Local_Put,
                   NI_Remote_Put, NI_Local_PutXAcksDone, NI_Remote_PutX,
                   NI_Inv, NI_InvAck, NI_Wb, NI_FAck, NI_ShWb, NI_Replace };
    TNAME : enum { Notrans, Plgg, Nlgg, Plxx, Nlxx };
    BUF_ENT : record
        Rname : RNAME;
        Tname : TNAME;
        multiple : boolean;
    end;
    DIR_REC : record
        Rname : RNAME;
        Tname : TNAME;
        agent : absNODE;
    end;
var
    Home : absNODE;
    Sta : STATE;
    otherbuffer : array[BUF_IND] of BUF_ENT;
    dirrec : DIR_REC;
    concbuffer : array[NODE] of array[TRANS_IND] of BUF_ENT;
    system_nondet : boolean;
    nondet0 : boolean;
--| Function and procedure declarations
function findindex1 ( t : TNAME) : BUF_INDP;
    begin
        for i : BUF_IND do
            if otherbuffer[i].Tname = t then
                return i;
            endif;
        endfor;
        return BUF_SIZE;
    end;
function findindex2 ( m : RNAME;  t : TNAME) : BUF_INDP;
    begin
        for i : BUF_IND do
            if (otherbuffer[i].Rname = m) & (otherbuffer[i].Tname = t) then
                return i;
            endif;
        endfor;
        return BUF_SIZE;
    end;

function find ( r : RNAME;  t : TNAME;  a : NODE) : TRANS_INDP;
    begin
        for i : TRANS_IND do
            if (concbuffer[a][i].Rname = r) & (concbuffer[a][i].Tname = t) then
                return i;
            endif;
        endfor;
        return TRANS_SIZE;
    end;
function findtrans ( t : TNAME;  a : NODE) : TRANS_INDP;
    begin
        for i : TRANS_IND do
            if concbuffer[a][i].Tname = t then
                return i;
            endif;
        endfor;
        return TRANS_SIZE;
    end;
procedure entername ( tn : TNAME;  rn : RNAME;
                      a : NODE);
    var
        i : TRANS_INDP;
    begin
    i := find(rn, tn,a);
   if i < TRANS_SIZE then
    concbuffer[a][i].multiple := true;
   else
   i := find(Norule, Notrans, a);
    if i < TRANS_SIZE then
      concbuffer[a][i].Rname := rn;
      concbuffer[a][i].Tname := tn;
   else
      assert false;
   endif;
endif;
       -- if (dirrec.Tname = tn) & (dirrec.agent = a) then
         --   dirrec.Rname := rn;
        --endif;
    end;
procedure removename ( tn : TNAME;  rp : RNAME;
                       a : NODE);
    var
        i : TRANS_INDP;
    begin
        i := find(rp, tn, a);
        if i < TRANS_SIZE then
         if concbuffer[a][i].multiple then concbuffer[a][i].multiple := system_nondet;
         else
            concbuffer[a][i].Rname := Norule;
            concbuffer[a][i].Tname := Notrans;
        endif;
        else
            assert false;
        endif;
    end;
procedure enternameother ( t : TNAME;  rn : RNAME);
    var
        i : BUF_INDP;
    var
        j : BUF_INDP;
    begin
        i := findindex2(rn, t);
        if i < BUF_SIZE then
            otherbuffer[i].multiple := true;
        else
            j := findindex2(Norule, Notrans);
            if j < BUF_SIZE then
                otherbuffer[j].Rname := rn;
                otherbuffer[j].Tname := t;
                otherbuffer[j].multiple := false;
            else
                assert false;
            endif;
        endif;
        --if (dirrec.Tname = t) & (dirrec.agent = Other) then
          --  dirrec.Rname := rn;
        --endif;
    end;
procedure shiftup ( i : BUF_IND);
    begin
        for j : BUF_IND do
            if (j < (BUF_SIZE - 1)) & (j >= i) then
                otherbuffer[j].Rname := otherbuffer[j + 1].Rname;
                otherbuffer[j].Tname := otherbuffer[j + 1].Tname;
                otherbuffer[j].multiple := otherbuffer[j + 1].multiple;
            endif;
        endfor;
        otherbuffer[BUF_SIZE - 1].Rname := Norule;
        otherbuffer[BUF_SIZE - 1].Tname := Notrans;
        otherbuffer[BUF_SIZE - 1].multiple := false;
    end;
procedure removenameother ( t : TNAME;  r : RNAME);
    var
        i : BUF_INDP;
    begin
        i := findindex2(r, t);
        if i = BUF_SIZE then
            assert false;
        endif;
        if otherbuffer[i].multiple = true then
            otherbuffer[i].multiple := system_nondet;
        else
            shiftup(i);
        endif;
    end;
procedure removenamedir ( rn : RNAME;  tn : TNAME;  agent : absNODE);
    begin
        if ((dirrec.Rname = rn) & (dirrec.Tname = tn)) & (dirrec.agent = agent) then
            dirrec.Rname := Norule;
            dirrec.Tname := Notrans;
            dirrec.agent := Other;
        endif;
    end;
function existsbuf ( t : TNAME;  r : RNAME) : boolean;
    var
        i : BUF_INDP;
    begin
        i := findindex2(r, t);
        if i < BUF_SIZE then
            return true;
        else
            return false;
        endif;
    end;
function existsconc ( t : TNAME;  r : RNAME;
                      a : NODE) : boolean;
    var
        i : TRANS_INDP;
    begin
        i := find(r, t, a);
        if i < TRANS_SIZE then
            return true;
        else
            return false;
        endif;
    end;
function nosubtrans ( t : TNAME) : boolean;
    var
        i : BUF_INDP;
    var
        k : TRANS_INDP;
    begin
        i := findindex1(t);
        for j : NODE do
            k := findtrans(t, j);
            if k < TRANS_SIZE then
                return false;
            endif;
        endfor;
        return true;
    end;
--| Rules

ruleset
    h : NODE;
    d : DATA
do
    startstate "Init"
    begin
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
            Sta.RpMsg[p].Cmd := RP_None;
        endfor;
        
        Sta.Collecting := false;
        
        nondet0 := false;
system_nondet := false;
dirrec.Rname := Norule;
dirrec.Tname := Notrans;
dirrec.agent := Other;
 for i : BUF_IND do
            otherbuffer[i].Rname := Norule;
            otherbuffer[i].Tname := Notrans;
            otherbuffer[i].multiple := false;
        endfor;
        for i : NODE do
            for j : TRANS_IND do
                concbuffer[i][j].Rname := Norule;
                concbuffer[i][j].Tname := Notrans;
                concbuffer[i][j].multiple := false;
            endfor;
        endfor;
    end
;
end;
ruleset
    data : DATA
do
    rule "absStore"
      true
    ==>
    var
        NxtSta : STATE;
    begin
        NxtSta := Sta;
        Sta := NxtSta;
        nondet0 := false;
    end
;
end;
ruleset
    src : NODE;
    data : DATA
do
    rule "Store"
      Sta.Proc[src].CacheState = CACHE_E
    ==>
    var
        NxtSta : STATE;
    begin
        NxtSta := Sta;
        NxtSta.Proc[src].CacheData := data;
       
        Sta := NxtSta;
        nondet0 := false;
    end
;
end;
    rule "absPI_Remote_Get"
      Other != Home
    ==>
    var
        NxtSta : STATE;
    begin
        NxtSta := Sta;
        Sta := NxtSta;
        nondet0 := false;
    end
;
ruleset
    src : NODE
do
    rule "PI_Remote_Get"
      ((src != Home) & (Sta.Proc[src].ProcCmd = NODE_None)) & (Sta.Proc[src].CacheState = CACHE_I)
    ==>
    var
        NxtSta : STATE;
    begin
        NxtSta := Sta;
        NxtSta.Proc[src].ProcCmd := NODE_Get;
        NxtSta.UniMsg[src].Cmd := UNI_Get;
        NxtSta.UniMsg[src].Proc := Home;
        undefine NxtSta.UniMsg[src].Data;
        Sta := NxtSta;
        nondet0 := false;
    end
;
end;
    rule "absPI_Local_Get_Get"
      ((((Sta.Dir.HeadPtr = Other) & (Sta.Proc[Home].ProcCmd = NODE_None)) & (
        Sta.Proc[Home].CacheState = CACHE_I)) & (! (Sta.Dir.Pending))) & Sta.Dir.Dirty
    ==>
    var
        NxtSta : STATE;
    begin
        NxtSta := Sta;
        NxtSta.Proc[Home].ProcCmd := NODE_Get;
        NxtSta.Dir.Pending := true;
        NxtSta.UniMsg[Home].Cmd := UNI_Get;
        NxtSta.UniMsg[Home].Proc := Other;
        undefine NxtSta.UniMsg[Home].Data;
        if Sta.Dir.HeadPtr != Home then
            --NxtSta.FwdCmd := UNI_Get;
        endif;
        
        NxtSta.Collecting := false;
        Sta := NxtSta;
        nondet0 := false;
enternameother(Plgg,PI_Local_Get_Get);
    end
;
ruleset
    tmp : NODE
do
    rule "PI_Local_Get_Get"
      ((((Sta.Dir.HeadPtr = tmp) & (Sta.Proc[Home].ProcCmd = NODE_None)) & (
        Sta.Proc[Home].CacheState = CACHE_I)) & (! (Sta.Dir.Pending))) & Sta.Dir.Dirty
    ==>
    var
        NxtSta : STATE;
    begin
        NxtSta := Sta;
        NxtSta.Proc[Home].ProcCmd := NODE_Get;
        NxtSta.Dir.Pending := true;
        NxtSta.UniMsg[Home].Cmd := UNI_Get;
        NxtSta.UniMsg[Home].Proc := tmp;
        undefine NxtSta.UniMsg[Home].Data;
        if Sta.Dir.HeadPtr != Home then
            --NxtSta.FwdCmd := UNI_Get;
        endif;
        --NxtSta.Requester := Home;
        NxtSta.Collecting := false;
        Sta := NxtSta;
        nondet0 := false;
entername(Plgg,PI_Local_Get_Get,tmp);
    end
;
end;
rule "PI_Local_Get_Put"
  (((Sta.Proc[Home].ProcCmd = NODE_None) & (Sta.Proc[Home].CacheState = CACHE_I)) & (
   ! (Sta.Dir.Pending))) & (! (Sta.Dir.Dirty))
==>
var
    NxtSta : STATE;
begin
    NxtSta := Sta;
    NxtSta.Dir.Local := true;
    NxtSta.Proc[Home].ProcCmd := NODE_None;
    if Sta.Proc[Home].InvMarked then
        NxtSta.Proc[Home].InvMarked := false;
        NxtSta.Proc[Home].CacheState := CACHE_I;
        undefine NxtSta.Proc[Home].CacheData;
    else
        NxtSta.Proc[Home].CacheState := CACHE_S;
        NxtSta.Proc[Home].CacheData := Sta.MemData;
    endif;
    Sta := NxtSta;
    nondet0 := false;
end;
    rule "absPI_Remote_GetX"
      Other != Home
    ==>
    var
        NxtSta : STATE;
    begin
        NxtSta := Sta;
        Sta := NxtSta;
        nondet0 := false;
    end
;
ruleset
    src : NODE
do
    rule "PI_Remote_GetX"
      ((src != Home) & (Sta.Proc[src].ProcCmd = NODE_None)) & (Sta.Proc[src].CacheState = CACHE_I)
    ==>
    var
        NxtSta : STATE;
    begin
        NxtSta := Sta;
        NxtSta.Proc[src].ProcCmd := NODE_GetX;
        NxtSta.UniMsg[src].Cmd := UNI_GetX;
        NxtSta.UniMsg[src].Proc := Home;
        undefine NxtSta.UniMsg[src].Data;
        Sta := NxtSta;
        nondet0 := false;
    end
;
end;
    rule "absPI_Local_GetX_GetX"
      ((((Sta.Dir.HeadPtr = Other) & (Sta.Proc[Home].ProcCmd = NODE_None)) & (
        (Sta.Proc[Home].CacheState = CACHE_I) | (Sta.Proc[Home].CacheState = CACHE_S))) & (
       ! (Sta.Dir.Pending))) & Sta.Dir.Dirty
    ==>
    var
        NxtSta : STATE;
    begin
        NxtSta := Sta;
        NxtSta.Proc[Home].ProcCmd := NODE_GetX;
        NxtSta.Dir.Pending := true;
        NxtSta.UniMsg[Home].Cmd := UNI_GetX;
        NxtSta.UniMsg[Home].Proc := Other;
        undefine NxtSta.UniMsg[Home].Data;
        if Sta.Dir.HeadPtr != Home then
           -- NxtSta.FwdCmd := UNI_GetX;
        endif;
        --NxtSta.Requester := Home;
        NxtSta.Collecting := false;
        Sta := NxtSta;
        nondet0 := false;
enternameother(Plxx,PI_Local_GetX_GetX);
    end
;
ruleset
    tmp : NODE
do
    rule "PI_Local_GetX_GetX"
      ((((Sta.Dir.HeadPtr = tmp) & (Sta.Proc[Home].ProcCmd = NODE_None)) & (
        (Sta.Proc[Home].CacheState = CACHE_I) | (Sta.Proc[Home].CacheState = CACHE_S))) & (
       ! (Sta.Dir.Pending))) & Sta.Dir.Dirty
    ==>
    var
        NxtSta : STATE;
    begin
        NxtSta := Sta;
        NxtSta.Proc[Home].ProcCmd := NODE_GetX;
        NxtSta.Dir.Pending := true;
        NxtSta.UniMsg[Home].Cmd := UNI_GetX;
        NxtSta.UniMsg[Home].Proc := tmp;
        undefine NxtSta.UniMsg[Home].Data;
        if Sta.Dir.HeadPtr != Home then
           -- NxtSta.FwdCmd := UNI_GetX;
        endif;
        --NxtSta.Requester := Home;
        NxtSta.Collecting := false;
        Sta := NxtSta;
        nondet0 := false;
entername(Plxx,PI_Local_GetX_GetX,tmp);
    end
;
end;
rule "PI_Local_GetX_PutX"
  (((Sta.Proc[Home].ProcCmd = NODE_None) & ((Sta.Proc[Home].CacheState = CACHE_I) | (
                                            Sta.Proc[Home].CacheState = CACHE_S))) & (
   ! (Sta.Dir.Pending))) & (! (Sta.Dir.Dirty))
==>
var
    NxtSta : STATE;
begin
    NxtSta := Sta;
    NxtSta.Dir.Local := true;
    NxtSta.Dir.Dirty := true;
    if Sta.Dir.HeadVld then
        NxtSta.Dir.Pending := true;
        NxtSta.Dir.HeadVld := false;
        undefine NxtSta.Dir.HeadPtr;
        NxtSta.Dir.ShrVld := false;
        for p : NODE do
            NxtSta.Dir.ShrSet[p] := false;
            if (p != Home) & ((Sta.Dir.ShrVld & Sta.Dir.ShrSet[p]) | (
                              Sta.Dir.HeadVld & (Sta.Dir.HeadPtr = p))) then
                NxtSta.Dir.InvSet[p] := true;
                NxtSta.InvMsg[p].Cmd := INV_Inv;
            else
                NxtSta.Dir.InvSet[p] := false;
                NxtSta.InvMsg[p].Cmd := INV_None;
            endif;
        endfor;
        NxtSta.Collecting := true;
        --NxtSta.PrevData := Sta.CurrData;
        --NxtSta.LastOtherInvAck := Sta.Dir.HeadPtr;
    endif;
    NxtSta.Proc[Home].ProcCmd := NODE_None;
    NxtSta.Proc[Home].InvMarked := false;
    NxtSta.Proc[Home].CacheState := CACHE_E;
    NxtSta.Proc[Home].CacheData := Sta.MemData;
    Sta := NxtSta;
    nondet0 := false;
end;
    rule "absPI_Remote_PutX"
Other != Home & Sta.Dir.Dirty  & !Sta.Dir.ShrVld & Sta.WbMsg.Cmd != WB_Wb  & Sta.ShWbMsg.Cmd != SHWB_ShWb &  Sta.UniMsg[Home].Cmd != UNI_Put & (forall q: NODE do (Sta.Proc[q].CacheState != CACHE_E & Sta.UniMsg[q].Cmd != UNI_PutX) endforall) --lemma 1
    ==>
    var
        NxtSta : STATE;
    begin
        NxtSta := Sta;
        NxtSta.WbMsg.Cmd := WB_Wb;
        NxtSta.WbMsg.Proc := Other;
        NxtSta.WbMsg.Data := undefined;
        Sta := NxtSta;
        nondet0 := false;
    end
;
ruleset
    dst : NODE
do
    rule "PI_Remote_PutX"
      ((dst != Home) & (Sta.Proc[dst].ProcCmd = NODE_None)) & (Sta.Proc[dst].CacheState = CACHE_E)
    ==>
    var
        NxtSta : STATE;
    begin
        NxtSta := Sta;
        NxtSta.Proc[dst].CacheState := CACHE_I;
        undefine NxtSta.Proc[dst].CacheData;
        NxtSta.WbMsg.Cmd := WB_Wb;
        NxtSta.WbMsg.Proc := dst;
        NxtSta.WbMsg.Data := Sta.Proc[dst].CacheData;
        Sta := NxtSta;
        nondet0 := false;
    end
;
end;
rule "PI_Local_PutX"
  (Sta.Proc[Home].ProcCmd = NODE_None) & (Sta.Proc[Home].CacheState = CACHE_E)
==>
var
    NxtSta : STATE;
begin
    NxtSta := Sta;
    if Sta.Dir.Pending then
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
    endif;
    Sta := NxtSta;
    nondet0 := false;
end;
    rule "absPI_Remote_Replace"
      Other != Home
    ==>
    var
        NxtSta : STATE;
    begin
        NxtSta := Sta;
        Sta := NxtSta;
        nondet0 := false;
    end
;
ruleset
    src : NODE
do
    rule "PI_Remote_Replace"
      ((src != Home) & (Sta.Proc[src].ProcCmd = NODE_None)) & (Sta.Proc[src].CacheState = CACHE_S)
    ==>
    var
        NxtSta : STATE;
    begin
        NxtSta := Sta;
        NxtSta.Proc[src].CacheState := CACHE_I;
        undefine NxtSta.Proc[src].CacheData;
        NxtSta.RpMsg[src].Cmd := RP_Replace;
        Sta := NxtSta;
        nondet0 := false;
    end
;
end;
rule "PI_Local_Replace"
  (Sta.Proc[Home].ProcCmd = NODE_None) & (Sta.Proc[Home].CacheState = CACHE_S)
==>
var
    NxtSta : STATE;
begin
    NxtSta := Sta;
    NxtSta.Dir.Local := false;
    NxtSta.Proc[Home].CacheState := CACHE_I;
    undefine NxtSta.Proc[Home].CacheData;
    Sta := NxtSta;
    nondet0 := false;
end;
    rule "absNI_Nak"
      true
    ==>
    var
        NxtSta : STATE;
    begin
        NxtSta := Sta;
        Sta := NxtSta;
        nondet0 := false;
    end
;
ruleset
    dst : NODE
do
    rule "NI_Nak"
      Sta.UniMsg[dst].Cmd = UNI_Nak
    ==>
    var
        NxtSta : STATE;
    begin
        NxtSta := Sta;
        NxtSta.UniMsg[dst].Cmd := UNI_None;
        undefine NxtSta.UniMsg[dst].Proc;
        undefine NxtSta.UniMsg[dst].Data;
        NxtSta.Proc[dst].ProcCmd := NODE_None;
        NxtSta.Proc[dst].InvMarked := false;
        Sta := NxtSta;
        nondet0 := false;
    end
;
end;
rule "NI_Nak_Clear"
  Sta.NakcMsg.Cmd = NAKC_Nakc
==>
var
    NxtSta : STATE;
begin
    NxtSta := Sta;
    NxtSta.NakcMsg.Cmd := NAKC_None;
    NxtSta.Dir.Pending := false;
    Sta := NxtSta;
    nondet0 := false;
end;
    rule "absNI_Local_Get_Nak"
      (Other != Home) & ((Sta.Dir.Pending | ((Sta.Dir.Dirty & Sta.Dir.Local) & (
                                             Sta.Proc[Home].CacheState != CACHE_E))) | (
                         (Sta.Dir.Dirty & (! (Sta.Dir.Local))) & (Sta.Dir.HeadPtr = Other)))
    ==>
    var
        NxtSta : STATE;
    begin
        NxtSta := Sta;
        Sta := NxtSta;
        nondet0 := false;
    end
;
ruleset
    src : NODE
do
    rule "NI_Local_Get_Nak"
      ((((src != Home) & (Sta.UniMsg[src].Cmd = UNI_Get)) & (Sta.UniMsg[src].Proc = Home)) & (
       Sta.RpMsg[src].Cmd != RP_Replace)) & ((Sta.Dir.Pending | ((Sta.Dir.Dirty & Sta.Dir.Local) & (
                                                                 Sta.Proc[Home].CacheState != CACHE_E))) | (
                                             (Sta.Dir.Dirty & (! (Sta.Dir.Local))) & (
                                             Sta.Dir.HeadPtr = src)))
    ==>
    var
        NxtSta : STATE;
    begin
        NxtSta := Sta;
        NxtSta.UniMsg[src].Cmd := UNI_Nak;
        NxtSta.UniMsg[src].Proc := Home;
        undefine NxtSta.UniMsg[src].Data;
        Sta := NxtSta;
        nondet0 := false;
    end
;
end;
    rule "absabsNI_Local_Get_Get"
      (((((Sta.Dir.HeadPtr = Other) & (Other != Home)) & (! (Sta.Dir.Pending))) & Sta.Dir.Dirty) & (
       ! (Sta.Dir.Local))) & (Sta.Dir.HeadPtr != Other)
    ==>
    var
        NxtSta : STATE;
    begin
        NxtSta := Sta;
        NxtSta.Dir.Pending := true;
        if Sta.Dir.HeadPtr != Home then
          --  NxtSta.FwdCmd := UNI_Get;
        endif;
        --NxtSta.Requester := Other;
        NxtSta.Collecting := false;
        Sta := NxtSta;
        nondet0 := false;
--enternameother(Nlgg,NI_Local_Get_Get,tmp);
    end
;
ruleset
    src : NODE
do
    rule "absNI_Local_Get_Get"
      ((((((((Sta.Dir.HeadPtr = Other) & (src != Home)) & (Sta.UniMsg[src].Cmd = UNI_Get)) & (
           Sta.UniMsg[src].Proc = Home)) & (Sta.RpMsg[src].Cmd != RP_Replace)) & (
         ! (Sta.Dir.Pending))) & Sta.Dir.Dirty) & (! (Sta.Dir.Local))) & (
      Sta.Dir.HeadPtr != src)
    ==>
    var
        NxtSta : STATE;
    begin
        NxtSta := Sta;
        NxtSta.Dir.Pending := true;
        NxtSta.UniMsg[src].Cmd := UNI_Get;
        NxtSta.UniMsg[src].Proc := Other;
        undefine NxtSta.UniMsg[src].Data;
        if Sta.Dir.HeadPtr != Home then
            --NxtSta.FwdCmd := UNI_Get;
        endif;
        --NxtSta.Requester := src;
        NxtSta.Collecting := false;
        Sta := NxtSta;
        nondet0 := false;
enternameother(Nlgg,NI_Local_Get_Get);
entername(Nlgg,NI_Local_Get_Get,src);
    end
;
end;
ruleset
    tmp : NODE
do
    rule "absNI_Local_Get_Get"
      (((((Sta.Dir.HeadPtr = tmp) & (Other != Home)) & (! (Sta.Dir.Pending))) & Sta.Dir.Dirty) & (
       ! (Sta.Dir.Local))) & (Sta.Dir.HeadPtr != Other)
    ==>
    var
        NxtSta : STATE;
    begin
        NxtSta := Sta;
        NxtSta.Dir.Pending := true;
        if Sta.Dir.HeadPtr != Home then
          --  NxtSta.FwdCmd := UNI_Get;
        endif;
        --NxtSta.Requester := Other;
        NxtSta.Collecting := false;
        Sta := NxtSta;
        nondet0 := false;
entername(Nlgg,NI_Local_Get_Get,tmp);
enternameother(Nlgg,NI_Local_Get_Get);
    end
;
end;
ruleset
    src : NODE;
    tmp : NODE
do
    rule "NI_Local_Get_Get"
      ((((((((Sta.Dir.HeadPtr = tmp) & (src != Home)) & (Sta.UniMsg[src].Cmd = UNI_Get)) & (
           Sta.UniMsg[src].Proc = Home)) & (Sta.RpMsg[src].Cmd != RP_Replace)) & (
         ! (Sta.Dir.Pending))) & Sta.Dir.Dirty) & (! (Sta.Dir.Local))) & (
      Sta.Dir.HeadPtr != src)
    ==>
    var
        NxtSta : STATE;
    begin
        NxtSta := Sta;
        NxtSta.Dir.Pending := true;
        NxtSta.UniMsg[src].Cmd := UNI_Get;
        NxtSta.UniMsg[src].Proc := tmp;
        undefine NxtSta.UniMsg[src].Data;
        if Sta.Dir.HeadPtr != Home then
          --  NxtSta.FwdCmd := UNI_Get;
        endif;
        --NxtSta.Requester := src;
        NxtSta.Collecting := false;
        Sta := NxtSta;
        nondet0 := false;
entername(Nlgg,NI_Local_Get_Get,tmp);
entername(Nlgg,NI_Local_Get_Get,src);
    end
;
end;
    rule "absNI_Local_Get_Put"
      ((Other != Home) & (! (Sta.Dir.Pending))) & (Sta.Dir.Dirty -> (
                                                   Sta.Dir.Local & (Sta.Proc[Home].CacheState = CACHE_E)))
    ==>
    var
        NxtSta : STATE;
    begin
        NxtSta := Sta;
        if Sta.Dir.Dirty then
            NxtSta.Dir.Dirty := false;
            NxtSta.Dir.HeadVld := true;
            NxtSta.Dir.HeadPtr := Other;
            NxtSta.MemData := Sta.Proc[Home].CacheData;
            NxtSta.Proc[Home].CacheState := CACHE_S;
        else
            if Sta.Dir.HeadVld then
                NxtSta.Dir.ShrVld := true;
                for p : NODE do
                    NxtSta.Dir.InvSet[p] := false | Sta.Dir.ShrSet[p];
                endfor;
            else
                NxtSta.Dir.HeadVld := true;
                NxtSta.Dir.HeadPtr := Other;
            endif;
        endif;
        Sta := NxtSta;
        nondet0 := false;
    end
;
ruleset
    src : NODE
do
    rule "NI_Local_Get_Put"
      (((((src != Home) & (Sta.UniMsg[src].Cmd = UNI_Get)) & (Sta.UniMsg[src].Proc = Home)) & (
        Sta.RpMsg[src].Cmd != RP_Replace)) & (! (Sta.Dir.Pending))) & (
      Sta.Dir.Dirty -> (Sta.Dir.Local & (Sta.Proc[Home].CacheState = CACHE_E)))
    ==>
    var
        NxtSta : STATE;
    begin
        NxtSta := Sta;
        if Sta.Dir.Dirty then
            NxtSta.Dir.Dirty := false;
            NxtSta.Dir.HeadVld := true;
            NxtSta.Dir.HeadPtr := src;
            NxtSta.MemData := Sta.Proc[Home].CacheData;
            NxtSta.Proc[Home].CacheState := CACHE_S;
            NxtSta.UniMsg[src].Cmd := UNI_Put;
            NxtSta.UniMsg[src].Proc := Home;
            NxtSta.UniMsg[src].Data := Sta.Proc[Home].CacheData;
        else
            if Sta.Dir.HeadVld then
                NxtSta.Dir.ShrVld := true;
                NxtSta.Dir.ShrSet[src] := true;
                for p : NODE do
                    NxtSta.Dir.InvSet[p] := (p = src) | Sta.Dir.ShrSet[p];
                endfor;
            else
                NxtSta.Dir.HeadVld := true;
                NxtSta.Dir.HeadPtr := src;
            endif;
            NxtSta.UniMsg[src].Cmd := UNI_Put;
            NxtSta.UniMsg[src].Proc := Home;
            NxtSta.UniMsg[src].Data := Sta.MemData;
        endif;
        Sta := NxtSta;
        nondet0 := false;
    end
;
end;
    rule "absabsNI_Remote_Get_Nak"
      false
    ==>
    var
        NxtSta : STATE;
    begin
        NxtSta := Sta;
        NxtSta.NakcMsg.Cmd := NAKC_Nakc;
        --NxtSta.FwdCmd := UNI_None;
        --NxtSta.FwdSrc := Other;
        Sta := NxtSta;
        nondet0 := false;
    end
;
ruleset
    src : NODE
do
    rule "absNI_Remote_Get_Nak"
((Other != Home) & (Sta.UniMsg[src].Cmd = UNI_Get)) & (Sta.UniMsg[src].Proc = Other) & existsbuf(Nlgg,NI_Local_Get_Get) & (src = Home | existsconc(Nlgg,NI_Local_Get_Get,src))
    ==>
    var
        NxtSta : STATE;
    begin
        NxtSta := Sta;
        NxtSta.UniMsg[src].Cmd := UNI_Nak;
        NxtSta.UniMsg[src].Proc := Other;
        undefine NxtSta.UniMsg[src].Data;
        NxtSta.NakcMsg.Cmd := NAKC_Nakc;
        --NxtSta.FwdCmd := UNI_None;
        --NxtSta.FwdSrc := src;
        Sta := NxtSta;
        nondet0 := false;
--assert existsconc(Nlgg,NI_Local_Get_Get,src);
if (src != Home) then removename(Nlgg,NI_Local_Get_Get,src);endif;
removenameother(Nlgg,NI_Local_Get_Get);
    end
;
end;

ruleset
    src : NODE
do
    rule "absNI_Remote_Get_Nak"
((Other != Home) & (Sta.UniMsg[src].Cmd = UNI_Get)) & (Sta.UniMsg[src].Proc = Other) & existsbuf(Plgg,PI_Local_Get_Get) & (src = Home | existsconc(Plgg,PI_Local_Get_Get,src))
    ==>
    var
        NxtSta : STATE;
    begin
        NxtSta := Sta;
        NxtSta.UniMsg[src].Cmd := UNI_Nak;
        NxtSta.UniMsg[src].Proc := Other;
        undefine NxtSta.UniMsg[src].Data;
        NxtSta.NakcMsg.Cmd := NAKC_Nakc;
        --NxtSta.FwdCmd := UNI_None;
        --NxtSta.FwdSrc := src;
        Sta := NxtSta;
        nondet0 := false;
--assert existsconc(Plgg,PI_Local_Get_Get,src);
if (src != Home) then removename(Plgg,PI_Local_Get_Get,src);endif;
removenameother(Plgg,PI_Local_Get_Get);
    end
;
end;
ruleset
    dst : NODE
do
    rule "absNI_Remote_Get_Nak"
      (dst != Home) & (Sta.Proc[dst].CacheState != CACHE_E) & existsbuf(Nlgg,NI_Local_Get_Get) & existsconc(Nlgg,NI_Local_Get_Get,dst)
    ==>
    var
        NxtSta : STATE;
    begin
        NxtSta := Sta;
        NxtSta.NakcMsg.Cmd := NAKC_Nakc;
        --NxtSta.FwdCmd := UNI_None;
        --NxtSta.FwdSrc := Other;
        Sta := NxtSta;
        nondet0 := false;
--assert existsconc(Nlgg,NI_Local_Get_Get,dst);
removename(Nlgg,NI_Local_Get_Get,dst);
removenameother(Nlgg,NI_Local_Get_Get);
    end
;
end;
ruleset
    dst : NODE
do
    rule "absNI_Remote_Get_Nak"
      (dst != Home) & (Sta.Proc[dst].CacheState != CACHE_E) & existsbuf(Plgg,PI_Local_Get_Get) & existsconc(Plgg,PI_Local_Get_Get,dst)
    ==>
    var
        NxtSta : STATE;
    begin
        NxtSta := Sta;
        NxtSta.NakcMsg.Cmd := NAKC_Nakc;
       -- NxtSta.FwdCmd := UNI_None;
        --NxtSta.FwdSrc := Other;
        Sta := NxtSta;
        nondet0 := false;
--assert existsconc(Nlgg,NI_Local_Get_Get,dst);
removename(Plgg,PI_Local_Get_Get,dst);
removenameother(Plgg,PI_Local_Get_Get);
    end
;
end;

ruleset
    src : NODE;
    dst : NODE
do
    rule "NI_Remote_Get_Nak"
      ((((src != dst) & (dst != Home)) & (Sta.UniMsg[src].Cmd = UNI_Get)) & (
       Sta.UniMsg[src].Proc = dst)) & (Sta.Proc[dst].CacheState != CACHE_E)
    ==>
    var
        NxtSta : STATE;
    begin
        NxtSta := Sta;
        NxtSta.UniMsg[src].Cmd := UNI_Nak;
        NxtSta.UniMsg[src].Proc := dst;
        undefine NxtSta.UniMsg[src].Data;
        NxtSta.NakcMsg.Cmd := NAKC_Nakc;
        --NxtSta.FwdCmd := UNI_None;
        --NxtSta.FwdSrc := src;
        Sta := NxtSta;
        nondet0 := false;


if src != Home then
assert (existsconc(Plgg,PI_Local_Get_Get,dst)&existsconc(Plgg,PI_Local_Get_Get,src) | existsconc(Nlgg,NI_Local_Get_Get,dst)&existsconc(Nlgg,NI_Local_Get_Get,src));
else 
assert (existsconc(Plgg,PI_Local_Get_Get,dst)| existsconc(Nlgg,NI_Local_Get_Get,dst));
endif;
if existsconc(Plgg,PI_Local_Get_Get,dst) then
removename(Plgg,PI_Local_Get_Get,dst);
if src != Home then removename(Plgg,PI_Local_Get_Get,src);endif;
else
removename(Nlgg,NI_Local_Get_Get,dst);
if src != Home then removename(Nlgg,NI_Local_Get_Get,src);endif;
endif;

    end
;
end;
    rule "absabsNI_Remote_Get_Put"
      false
    ==>
    var
        NxtSta : STATE;
    begin
        NxtSta := Sta;
        if Other != Home then
            NxtSta.ShWbMsg.Cmd := SHWB_ShWb;
            NxtSta.ShWbMsg.Proc := Other;
            NxtSta.ShWbMsg.Data := undefined;
        endif;
        --NxtSta.FwdCmd := UNI_None;
        --NxtSta.FwdSrc := Other;
        Sta := NxtSta;
        nondet0 := false;
    end
;
ruleset
    src : NODE
do
    rule "absNI_Remote_Get_Put"
((Other != Home) & (Sta.UniMsg[src].Cmd = UNI_Get)) & (Sta.UniMsg[src].Proc = Other) & (existsbuf(Plgg,PI_Local_Get_Get) & ((src = Home) | existsconc(Plgg, PI_Local_Get_Get,src)))& Sta.Dir.Dirty  & !Sta.Dir.ShrVld & Sta.WbMsg.Cmd != WB_Wb &  Sta.ShWbMsg.Cmd != SHWB_ShWb &  Sta.UniMsg[Home].Cmd != UNI_Put & (forall q: NODE do (Sta.Proc[q].CacheState != CACHE_E & Sta.UniMsg[q].Cmd != UNI_PutX) endforall) --lemma 1
    ==>
    var
        NxtSta : STATE;
    begin
        NxtSta := Sta;
        NxtSta.UniMsg[src].Cmd := UNI_Put;
        NxtSta.UniMsg[src].Proc := Other;
        NxtSta.UniMsg[src].Data := undefined;
        if src != Home then
            NxtSta.ShWbMsg.Cmd := SHWB_ShWb;
            NxtSta.ShWbMsg.Proc := src;
            NxtSta.ShWbMsg.Data := undefined;
        endif;
        --NxtSta.FwdCmd := UNI_None;
        --NxtSta.FwdSrc := src;
        Sta := NxtSta;
        nondet0 := false;
-- if (src != Home) then assert existsconc(Plgg,PI_Local_Get_Get,src);endif;
removenameother(Plgg,PI_Local_Get_Get);
if (src != Home) then removename(Plgg,PI_Local_Get_Get,src);endif;
    end
;
end;
ruleset
    src : NODE
do
    rule "absNI_Remote_Get_Put"
((Other != Home) & (Sta.UniMsg[src].Cmd = UNI_Get)) & (Sta.UniMsg[src].Proc = Other) & (existsbuf(Nlgg,NI_Local_Get_Get) & ((src = Home)| existsconc(Nlgg,NI_Local_Get_Get,src)))& Sta.Dir.Dirty  & !Sta.Dir.ShrVld & Sta.WbMsg.Cmd != WB_Wb &  Sta.ShWbMsg.Cmd != SHWB_ShWb &  Sta.UniMsg[Home].Cmd != UNI_Put & (forall q: NODE do (Sta.Proc[q].CacheState != CACHE_E & Sta.UniMsg[q].Cmd != UNI_PutX) endforall) --lemma 1
    ==>
    var
        NxtSta : STATE;
    begin
        NxtSta := Sta;
        NxtSta.UniMsg[src].Cmd := UNI_Put;
        NxtSta.UniMsg[src].Proc := Other;
        NxtSta.UniMsg[src].Data := undefined;
        if src != Home then
            NxtSta.ShWbMsg.Cmd := SHWB_ShWb;
            NxtSta.ShWbMsg.Proc := src;
            NxtSta.ShWbMsg.Data := undefined;
        endif;
        --NxtSta.FwdCmd := UNI_None;
        --NxtSta.FwdSrc := src;
        Sta := NxtSta;
        nondet0 := false;
--if (src != Home) then assert existsconc(Nlgg,NI_Local_Get_Get,src);endif;
removenameother(Nlgg,NI_Local_Get_Get);
if (src != Home) then removename(Nlgg,NI_Local_Get_Get,src); endif;
    end
;
end;
ruleset
    dst : NODE
do
    rule "absNI_Remote_Get_Put"
(dst != Home) & (Sta.Proc[dst].CacheState = CACHE_E) & existsbuf(Plgg,PI_Local_Get_Get) & existsconc(Plgg,PI_Local_Get_Get,dst)
    ==>
    var
        NxtSta : STATE;
    begin
        NxtSta := Sta;
        NxtSta.Proc[dst].CacheState := CACHE_S;
        if Other != Home then
            NxtSta.ShWbMsg.Cmd := SHWB_ShWb;
            NxtSta.ShWbMsg.Proc := Other;
            NxtSta.ShWbMsg.Data := Sta.Proc[dst].CacheData;
        endif;
        --NxtSta.FwdCmd := UNI_None;
        --NxtSta.FwdSrc := Other;
        Sta := NxtSta;
        nondet0 := false;
--assert (existsconc(Plgg,PI_Local_Get_Get,dst));
removename(Plgg,PI_Local_Get_Get,dst);
removenameother(Plgg,PI_Local_Get_Get);
    end
;
end;
ruleset
    dst : NODE
do
    rule "absNI_Remote_Get_Put"
(dst != Home) & (Sta.Proc[dst].CacheState = CACHE_E) & existsbuf(Nlgg,NI_Local_Get_Get) & existsconc(Nlgg,NI_Local_Get_Get,dst)
    ==>
    var
        NxtSta : STATE;
    begin
        NxtSta := Sta;
        NxtSta.Proc[dst].CacheState := CACHE_S;
        if Other != Home then
            NxtSta.ShWbMsg.Cmd := SHWB_ShWb;
            NxtSta.ShWbMsg.Proc := Other;
            NxtSta.ShWbMsg.Data := Sta.Proc[dst].CacheData;
        endif;
        --NxtSta.FwdCmd := UNI_None;
        --NxtSta.FwdSrc := Other;
        Sta := NxtSta;
        nondet0 := false;
--assert (existsconc(Nlgg,NI_Local_Get_Get,dst));
removenameother(Nlgg,NI_Local_Get_Get);
removename(Nlgg,NI_Local_Get_Get,dst);
    end
;
end;
ruleset
    src : NODE;
    dst : NODE
do
    rule "NI_Remote_Get_Put"
      ((((src != dst) & (dst != Home)) & (Sta.UniMsg[src].Cmd = UNI_Get)) & (
       Sta.UniMsg[src].Proc = dst)) & (Sta.Proc[dst].CacheState = CACHE_E)
    ==>
    var
        NxtSta : STATE;
    begin
        NxtSta := Sta;
        NxtSta.Proc[dst].CacheState := CACHE_S;
        NxtSta.UniMsg[src].Cmd := UNI_Put;
        NxtSta.UniMsg[src].Proc := dst;
        NxtSta.UniMsg[src].Data := Sta.Proc[dst].CacheData;
        if src != Home then
            NxtSta.ShWbMsg.Cmd := SHWB_ShWb;
            NxtSta.ShWbMsg.Proc := src;
            NxtSta.ShWbMsg.Data := Sta.Proc[dst].CacheData;
        endif;
        --NxtSta.FwdCmd := UNI_None;
        --NxtSta.FwdSrc := src;
        Sta := NxtSta;
        nondet0 := false;
if src != Home then
assert (existsconc(Plgg,PI_Local_Get_Get,dst)&existsconc(Plgg,PI_Local_Get_Get,src) | existsconc(Nlgg,NI_Local_Get_Get,dst)&existsconc(Nlgg,NI_Local_Get_Get,src));
else 
assert (existsconc(Plgg,PI_Local_Get_Get,dst)| existsconc(Nlgg,NI_Local_Get_Get,dst));
endif;
if existsconc(Plgg,PI_Local_Get_Get,dst) then
removename(Plgg,PI_Local_Get_Get,dst);
if src != Home then removename(Plgg,PI_Local_Get_Get,src);endif;
else
removename(Nlgg,NI_Local_Get_Get,dst);
if src != Home then removename(Nlgg,NI_Local_Get_Get,src);endif;
endif;
    end
;
end;
    rule "absNI_Local_GetX_Nak"
      (Other != Home) & ((Sta.Dir.Pending | ((Sta.Dir.Dirty & Sta.Dir.Local) & (
                                             Sta.Proc[Home].CacheState != CACHE_E))) | (
                         (Sta.Dir.Dirty & (! (Sta.Dir.Local))) & (Sta.Dir.HeadPtr = Other)))
    ==>
    var
        NxtSta : STATE;
    begin
        NxtSta := Sta;
        Sta := NxtSta;
        nondet0 := false;
    end
;
ruleset
    src : NODE
do
    rule "NI_Local_GetX_Nak"
      (((src != Home) & (Sta.UniMsg[src].Cmd = UNI_GetX)) & (Sta.UniMsg[src].Proc = Home)) & (
      (Sta.Dir.Pending | ((Sta.Dir.Dirty & Sta.Dir.Local) & (Sta.Proc[Home].CacheState != CACHE_E))) | (
      (Sta.Dir.Dirty & (! (Sta.Dir.Local))) & (Sta.Dir.HeadPtr = src)))
    ==>
    var
        NxtSta : STATE;
    begin
        NxtSta := Sta;
        NxtSta.UniMsg[src].Cmd := UNI_Nak;
        NxtSta.UniMsg[src].Proc := Home;
        undefine NxtSta.UniMsg[src].Data;
        Sta := NxtSta;
        nondet0 := false;
    end
;
end;
    rule "absabsNI_Local_GetX_GetX"
      (((((Sta.Dir.HeadPtr = Other) & (Other != Home)) & (! (Sta.Dir.Pending))) & Sta.Dir.Dirty) & (
       ! (Sta.Dir.Local))) & (Sta.Dir.HeadPtr != Other)
    ==>
    var
        NxtSta : STATE;
    begin
        NxtSta := Sta;
        NxtSta.Dir.Pending := true;
        if Sta.Dir.HeadPtr != Home then
           -- NxtSta.FwdCmd := UNI_GetX;
        endif;
        --NxtSta.Requester := Other;
        NxtSta.Collecting := false;
        Sta := NxtSta;
        nondet0 := false;
--enternameother(Nlxx,NI_Local_GetX_GetX,tmp);
    end
;
ruleset
    src : NODE
do
    rule "absNI_Local_GetX_GetX"
      (((((((Sta.Dir.HeadPtr = Other) & (src != Home)) & (Sta.UniMsg[src].Cmd = UNI_GetX)) & (
          Sta.UniMsg[src].Proc = Home)) & (! (Sta.Dir.Pending))) & Sta.Dir.Dirty) & (
       ! (Sta.Dir.Local))) & (Sta.Dir.HeadPtr != src)
    ==>
    var
        NxtSta : STATE;
    begin
        NxtSta := Sta;
        NxtSta.Dir.Pending := true;
        NxtSta.UniMsg[src].Cmd := UNI_GetX;
        NxtSta.UniMsg[src].Proc := Other;
        undefine NxtSta.UniMsg[src].Data;
        if Sta.Dir.HeadPtr != Home then
          --  NxtSta.FwdCmd := UNI_GetX;
        endif;
        --NxtSta.Requester := src;
        NxtSta.Collecting := false;
        Sta := NxtSta;
        nondet0 := false;
enternameother(Nlxx,NI_Local_GetX_GetX);
entername(Nlxx,NI_Local_GetX_GetX,src);
    end
;
end;
ruleset
    tmp : NODE
do
    rule "absNI_Local_GetX_GetX"
      (((((Sta.Dir.HeadPtr = tmp) & (Other != Home)) & (! (Sta.Dir.Pending))) & Sta.Dir.Dirty) & (
       ! (Sta.Dir.Local))) & (Sta.Dir.HeadPtr != Other)
    ==>
    var
        NxtSta : STATE;
    begin
        NxtSta := Sta;
        NxtSta.Dir.Pending := true;
        if Sta.Dir.HeadPtr != Home then
          --  NxtSta.FwdCmd := UNI_GetX;
        endif;
        --NxtSta.Requester := Other;
        NxtSta.Collecting := false;
        Sta := NxtSta;
        nondet0 := false;
enternameother(Nlxx,NI_Local_GetX_GetX);
entername(Nlxx,NI_Local_GetX_GetX,tmp);
    end
;
end;
ruleset
    src : NODE;
    tmp : NODE
do
    rule "NI_Local_GetX_GetX"
      (((((((Sta.Dir.HeadPtr = tmp) & (src != Home)) & (Sta.UniMsg[src].Cmd = UNI_GetX)) & (
          Sta.UniMsg[src].Proc = Home)) & (! (Sta.Dir.Pending))) & Sta.Dir.Dirty) & (
       ! (Sta.Dir.Local))) & (Sta.Dir.HeadPtr != src)
    ==>
    var
        NxtSta : STATE;
    begin
        NxtSta := Sta;
        NxtSta.Dir.Pending := true;
        NxtSta.UniMsg[src].Cmd := UNI_GetX;
        NxtSta.UniMsg[src].Proc := tmp;
        undefine NxtSta.UniMsg[src].Data;
        if Sta.Dir.HeadPtr != Home then
          --  NxtSta.FwdCmd := UNI_GetX;
        endif;
        --NxtSta.Requester := src;
        NxtSta.Collecting := false;
        Sta := NxtSta;
        nondet0 := false;
entername(Nlxx,NI_Local_GetX_GetX,tmp);
entername(Nlxx,NI_Local_GetX_GetX,src);
    end
;
end;
    rule "absNI_Local_GetX_PutX"
      ((Other != Home) & (! (Sta.Dir.Pending))) & (Sta.Dir.Dirty -> (
                                                   Sta.Dir.Local & (Sta.Proc[Home].CacheState = CACHE_E)))
    ==>
    var
        NxtSta : STATE;
    begin
        NxtSta := Sta;
        if Sta.Dir.Dirty then
            NxtSta.Dir.Local := false;
            NxtSta.Dir.Dirty := true;
            NxtSta.Dir.HeadVld := true;
            NxtSta.Dir.HeadPtr := Other;
            NxtSta.Dir.ShrVld := false;
            for p : NODE do
                NxtSta.Dir.ShrSet[p] := false;
                NxtSta.Dir.InvSet[p] := false;
            endfor;
            NxtSta.Proc[Home].CacheState := CACHE_I;
            undefine NxtSta.Proc[Home].CacheData;
        elsif Sta.Dir.HeadVld -> ((Sta.Dir.HeadPtr = Other) & (forall 
                                                               p : NODE do 
                                                               true -> (
                                                               ! (Sta.Dir.ShrSet[p])) end & nondet0)) then
            NxtSta.Dir.Local := false;
            NxtSta.Dir.Dirty := true;
            NxtSta.Dir.HeadVld := true;
            NxtSta.Dir.HeadPtr := Other;
            NxtSta.Dir.ShrVld := false;
            for p : NODE do
                NxtSta.Dir.ShrSet[p] := false;
                NxtSta.Dir.InvSet[p] := false;
            endfor;
            NxtSta.Proc[Home].CacheState := CACHE_I;
            undefine NxtSta.Proc[Home].CacheData;
            if Sta.Dir.Local then
                NxtSta.Proc[Home].CacheState := CACHE_I;
                undefine NxtSta.Proc[Home].CacheData;
                if Sta.Proc[Home].ProcCmd = NODE_Get then
                    NxtSta.Proc[Home].InvMarked := true;
                endif;
            endif;
        else
            NxtSta.Dir.Pending := true;
            NxtSta.Dir.Local := false;
            NxtSta.Dir.Dirty := true;
            NxtSta.Dir.HeadVld := true;
            NxtSta.Dir.HeadPtr := Other;
            NxtSta.Dir.ShrVld := false;
            for p : NODE do
                NxtSta.Dir.ShrSet[p] := false;
                if ((p != Home) & true) & ((Sta.Dir.ShrVld & Sta.Dir.ShrSet[p]) | (
                                           Sta.Dir.HeadVld & (Sta.Dir.HeadPtr = p))) then
                    NxtSta.Dir.InvSet[p] := true;
                    NxtSta.InvMsg[p].Cmd := INV_Inv;
                else
                    NxtSta.Dir.InvSet[p] := false;
                    NxtSta.InvMsg[p].Cmd := INV_None;
                endif;
            endfor;
            if Sta.Dir.Local then
                NxtSta.Proc[Home].CacheState := CACHE_I;
                undefine NxtSta.Proc[Home].CacheData;
                if Sta.Proc[Home].ProcCmd = NODE_Get then
                    NxtSta.Proc[Home].InvMarked := true;
                endif;
            endif;
           -- NxtSta.Requester := Other;
            NxtSta.Collecting := true;
           -- NxtSta.PrevData := Sta.CurrData;
            if Sta.Dir.HeadPtr != Other then
              --  NxtSta.LastOtherInvAck := Sta.Dir.HeadPtr;
            else
                for p : NODE do
                    if true & Sta.Dir.ShrSet[p] then
                       -- NxtSta.LastOtherInvAck := p;
                    endif;
                endfor;
            endif;
        endif;
        Sta := NxtSta;
        nondet0 := false;
    end
;
ruleset
    src : NODE
do
    rule "NI_Local_GetX_PutX"
      ((((src != Home) & (Sta.UniMsg[src].Cmd = UNI_GetX)) & (Sta.UniMsg[src].Proc = Home)) & (
       ! (Sta.Dir.Pending))) & (Sta.Dir.Dirty -> (Sta.Dir.Local & (Sta.Proc[Home].CacheState = CACHE_E)))
    ==>
    var
        NxtSta : STATE;
    begin
        NxtSta := Sta;
        if Sta.Dir.Dirty then
            NxtSta.Dir.Local := false;
            NxtSta.Dir.Dirty := true;
            NxtSta.Dir.HeadVld := true;
            NxtSta.Dir.HeadPtr := src;
            NxtSta.Dir.ShrVld := false;
            for p : NODE do
                NxtSta.Dir.ShrSet[p] := false;
                NxtSta.Dir.InvSet[p] := false;
            endfor;
            NxtSta.UniMsg[src].Cmd := UNI_PutX;
            NxtSta.UniMsg[src].Proc := Home;
            NxtSta.UniMsg[src].Data := Sta.Proc[Home].CacheData;
            NxtSta.Proc[Home].CacheState := CACHE_I;
            undefine NxtSta.Proc[Home].CacheData;
        elsif Sta.Dir.HeadVld -> ((Sta.Dir.HeadPtr = src) & (forall p : NODE do 
                                                             (p != src) -> (
                                                             ! (Sta.Dir.ShrSet[p])) end & nondet0)) then
            NxtSta.Dir.Local := false;
            NxtSta.Dir.Dirty := true;
            NxtSta.Dir.HeadVld := true;
            NxtSta.Dir.HeadPtr := src;
            NxtSta.Dir.ShrVld := false;
            for p : NODE do
                NxtSta.Dir.ShrSet[p] := false;
                NxtSta.Dir.InvSet[p] := false;
            endfor;
            NxtSta.UniMsg[src].Cmd := UNI_PutX;
            NxtSta.UniMsg[src].Proc := Home;
            NxtSta.UniMsg[src].Data := Sta.MemData;
            NxtSta.Proc[Home].CacheState := CACHE_I;
            undefine NxtSta.Proc[Home].CacheData;
            if Sta.Dir.Local then
                NxtSta.Proc[Home].CacheState := CACHE_I;
                undefine NxtSta.Proc[Home].CacheData;
                if Sta.Proc[Home].ProcCmd = NODE_Get then
                    NxtSta.Proc[Home].InvMarked := true;
                endif;
            endif;
        else
            NxtSta.Dir.Pending := true;
            NxtSta.Dir.Local := false;
            NxtSta.Dir.Dirty := true;
            NxtSta.Dir.HeadVld := true;
            NxtSta.Dir.HeadPtr := src;
            NxtSta.Dir.ShrVld := false;
            for p : NODE do
                NxtSta.Dir.ShrSet[p] := false;
                if ((p != Home) & (p != src)) & ((Sta.Dir.ShrVld & Sta.Dir.ShrSet[p]) | (
                                                 Sta.Dir.HeadVld & (Sta.Dir.HeadPtr = p))) then
                    NxtSta.Dir.InvSet[p] := true;
                    NxtSta.InvMsg[p].Cmd := INV_Inv;
                else
                    NxtSta.Dir.InvSet[p] := false;
                    NxtSta.InvMsg[p].Cmd := INV_None;
                endif;
            endfor;
            NxtSta.UniMsg[src].Cmd := UNI_PutX;
            NxtSta.UniMsg[src].Proc := Home;
            NxtSta.UniMsg[src].Data := Sta.MemData;
            if Sta.Dir.Local then
                NxtSta.Proc[Home].CacheState := CACHE_I;
                undefine NxtSta.Proc[Home].CacheData;
                if Sta.Proc[Home].ProcCmd = NODE_Get then
                    NxtSta.Proc[Home].InvMarked := true;
                endif;
            endif;
            --NxtSta.Requester := src;
            NxtSta.Collecting := true;
            --NxtSta.PrevData := Sta.CurrData;
            if Sta.Dir.HeadPtr != src then
              --  NxtSta.LastOtherInvAck := Sta.Dir.HeadPtr;
            else
                for p : NODE do
                    if (p != src) & Sta.Dir.ShrSet[p] then
                        --NxtSta.LastOtherInvAck := p;
                    endif;
                endfor;
            endif;
        endif;
        Sta := NxtSta;
        nondet0 := false;
    end
;
end;
    rule "absabsNI_Remote_GetX_Nak"
      false
    ==>
    var
        NxtSta : STATE;
    begin
        NxtSta := Sta;
        NxtSta.NakcMsg.Cmd := NAKC_Nakc;
        --NxtSta.FwdCmd := UNI_None;
        --NxtSta.FwdSrc := Other;
        Sta := NxtSta;
        nondet0 := false;
    end
;
ruleset
    src : NODE
do
    rule "absNI_Remote_GetX_Nak"
((Other != Home) & (Sta.UniMsg[src].Cmd = UNI_GetX)) & (Sta.UniMsg[src].Proc = Other) & existsbuf(Nlxx,NI_Local_GetX_GetX) & (src = Home | existsconc(Nlxx,NI_Local_GetX_GetX,src))
    ==>
    var
        NxtSta : STATE;
    begin
        NxtSta := Sta;
        NxtSta.UniMsg[src].Cmd := UNI_Nak;
        NxtSta.UniMsg[src].Proc := Other;
        undefine NxtSta.UniMsg[src].Data;
        NxtSta.NakcMsg.Cmd := NAKC_Nakc;
        --NxtSta.FwdCmd := UNI_None;
        --NxtSta.FwdSrc := src;
        Sta := NxtSta;
        nondet0 := false;
--assert existsconc(Nlxx,NI_Local_GetX_GetX,src);
if src != Home then removename(Nlxx,NI_Local_GetX_GetX,src); endif;
removenameother(Nlxx,NI_Local_GetX_GetX);

    end
;
end;
ruleset
    src : NODE
do
    rule "absNI_Remote_GetX_Nak"
((Other != Home) & (Sta.UniMsg[src].Cmd = UNI_GetX)) & (Sta.UniMsg[src].Proc = Other) & existsbuf(Plxx,PI_Local_GetX_GetX) & (src = Home | existsconc(Plxx,PI_Local_GetX_GetX,src))
    ==>
    var
        NxtSta : STATE;
    begin
        NxtSta := Sta;
        NxtSta.UniMsg[src].Cmd := UNI_Nak;
        NxtSta.UniMsg[src].Proc := Other;
        undefine NxtSta.UniMsg[src].Data;
        NxtSta.NakcMsg.Cmd := NAKC_Nakc;
        --NxtSta.FwdCmd := UNI_None;
        --NxtSta.FwdSrc := src;
        Sta := NxtSta;
        nondet0 := false;
--assert existsconc(Nlxx,NI_Local_GetX_GetX,src);
if src != Home then removename(Plxx,PI_Local_GetX_GetX,src); endif;
removenameother(Plxx,PI_Local_GetX_GetX);

    end
;
end;
ruleset
    dst : NODE
do
    rule "absNI_Remote_GetX_Nak"
      (dst != Home) & (Sta.Proc[dst].CacheState != CACHE_E) & existsbuf(Nlxx,NI_Local_GetX_GetX) & existsconc(Nlxx,NI_Local_GetX_GetX,dst)
    ==>
    var
        NxtSta : STATE;
    begin
        NxtSta := Sta;
        NxtSta.NakcMsg.Cmd := NAKC_Nakc;
        --NxtSta.FwdCmd := UNI_None;
        --NxtSta.FwdSrc := Other;
        Sta := NxtSta;
        nondet0 := false;
assert existsconc(Nlxx,NI_Local_GetX_GetX,dst);
removename(Nlxx,NI_Local_GetX_GetX,dst);
removenameother(Nlxx,NI_Local_GetX_GetX);
    end
;
end;
ruleset
    dst : NODE
do
    rule "absNI_Remote_GetX_Nak"
      (dst != Home) & (Sta.Proc[dst].CacheState != CACHE_E) & existsbuf(Plxx,PI_Local_GetX_GetX) & existsconc(Plxx,PI_Local_GetX_GetX,dst)
    ==>
    var
        NxtSta : STATE;
    begin
        NxtSta := Sta;
        NxtSta.NakcMsg.Cmd := NAKC_Nakc;
        --NxtSta.FwdCmd := UNI_None;
        --NxtSta.FwdSrc := Other;
        Sta := NxtSta;
        nondet0 := false;
assert existsconc(Plxx,PI_Local_GetX_GetX,dst);
removename(Plxx,PI_Local_GetX_GetX,dst);
removenameother(Plxx,PI_Local_GetX_GetX);
    end
;
end;
ruleset
    src : NODE;
    dst : NODE
do
    rule "NI_Remote_GetX_Nak"
      ((((src != dst) & (dst != Home)) & (Sta.UniMsg[src].Cmd = UNI_GetX)) & (
       Sta.UniMsg[src].Proc = dst)) & (Sta.Proc[dst].CacheState != CACHE_E)
    ==>
    var
        NxtSta : STATE;
    begin
        NxtSta := Sta;
        NxtSta.UniMsg[src].Cmd := UNI_Nak;
        NxtSta.UniMsg[src].Proc := dst;
        undefine NxtSta.UniMsg[src].Data;
        NxtSta.NakcMsg.Cmd := NAKC_Nakc;
        --NxtSta.FwdCmd := UNI_None;
        --NxtSta.FwdSrc := src;
        Sta := NxtSta;
        nondet0 := false;


if (src != Home) then
assert (existsconc(Plxx,PI_Local_GetX_GetX,dst)&existsconc(Plxx,PI_Local_GetX_GetX,src) | existsconc(Nlxx,NI_Local_GetX_GetX,dst)&existsconc(Nlxx,NI_Local_GetX_GetX,src));
else 
assert (existsconc(Plxx,PI_Local_GetX_GetX,dst)| existsconc(Nlxx,NI_Local_GetX_GetX,dst));
endif;

if existsconc(Plxx,PI_Local_GetX_GetX,dst) then
removename(Plxx,PI_Local_GetX_GetX,dst);
if (src != Home) then removename(Plxx,PI_Local_GetX_GetX,src);endif;
else
removename(Nlxx,NI_Local_GetX_GetX,dst);
if (src != Home) then removename(Nlxx,NI_Local_GetX_GetX,src);endif;
endif;

    end
;
end;
    rule "absabsNI_Remote_GetX_PutX"
      false
    ==>
    var
        NxtSta : STATE;
    begin
        NxtSta := Sta;
        if Other != Home then
            NxtSta.ShWbMsg.Cmd := SHWB_FAck;
            NxtSta.ShWbMsg.Proc := Other;
            undefine NxtSta.ShWbMsg.Data;
        endif;
        --NxtSta.FwdCmd := UNI_None;
        --NxtSta.FwdSrc := Other;
        Sta := NxtSta;
        nondet0 := false;
    end
;
ruleset
    src : NODE
do
    rule "absNI_Remote_GetX_PutX"
((Other != Home) & (Sta.UniMsg[src].Cmd = UNI_GetX)) & (Sta.UniMsg[src].Proc = Other) & (existsbuf(Plxx,PI_Local_GetX_GetX)) & (src = Home | existsconc(Plxx,PI_Local_GetX_GetX,src))& Sta.Dir.Dirty  & !Sta.Dir.ShrVld & Sta.WbMsg.Cmd != WB_Wb &  Sta.ShWbMsg.Cmd != SHWB_ShWb &  Sta.UniMsg[Home].Cmd != UNI_Put & (forall q: NODE do (Sta.Proc[q].CacheState != CACHE_E & Sta.UniMsg[q].Cmd != UNI_PutX) endforall) --lemma 1
    ==>
    var
        NxtSta : STATE;
    begin
        NxtSta := Sta;
        NxtSta.UniMsg[src].Cmd := UNI_PutX;
        NxtSta.UniMsg[src].Proc := Other;
        NxtSta.UniMsg[src].Data := undefined;
        if src != Home then
            NxtSta.ShWbMsg.Cmd := SHWB_FAck;
            NxtSta.ShWbMsg.Proc := src;
            undefine NxtSta.ShWbMsg.Data;
        endif;
        --NxtSta.FwdCmd := UNI_None;
        --NxtSta.FwdSrc := src;
        Sta := NxtSta;
        nondet0 := false;
--if (src != Home) then assert existsconc(Plxx,PI_Local_GetX_GetX,src);endif;
if (src != Home) then removename(Plxx,PI_Local_GetX_GetX,src);endif;
removenameother(Plxx,PI_Local_GetX_GetX);

    end
;
end;
ruleset
    src : NODE
do
    rule "absNI_Remote_GetX_PutX"
((Other != Home) & (Sta.UniMsg[src].Cmd = UNI_GetX)) & (Sta.UniMsg[src].Proc = Other) & (existsbuf(Nlxx,NI_Local_GetX_GetX)) & (src = Home | existsconc(Nlxx,NI_Local_GetX_GetX,src)) & Sta.Dir.Dirty  & !Sta.Dir.ShrVld & Sta.WbMsg.Cmd != WB_Wb &  Sta.ShWbMsg.Cmd != SHWB_ShWb &  Sta.UniMsg[Home].Cmd != UNI_Put & (forall q: NODE do (Sta.Proc[q].CacheState != CACHE_E & Sta.UniMsg[q].Cmd != UNI_PutX) endforall) --lemma 1
    ==>
    var
        NxtSta : STATE;
    begin
        NxtSta := Sta;
        NxtSta.UniMsg[src].Cmd := UNI_PutX;
        NxtSta.UniMsg[src].Proc := Other;
        NxtSta.UniMsg[src].Data := undefined;
        if src != Home then
            NxtSta.ShWbMsg.Cmd := SHWB_FAck;
            NxtSta.ShWbMsg.Proc := src;
            undefine NxtSta.ShWbMsg.Data;
        endif;
        --NxtSta.FwdCmd := UNI_None;
        --NxtSta.FwdSrc := src;
        Sta := NxtSta;
        nondet0 := false;
--if (src != Home) then assert existsconc(Nlxx,NI_Local_GetX_GetX,src);endif;
--assert existsconc(Nlxx,NI_Local_GetX_GetX,src);
if (src != Home) then removename(Nlxx,NI_Local_GetX_GetX,src);endif;
removenameother(Nlxx,NI_Local_GetX_GetX);
    end
;
end;
ruleset
    dst : NODE
do
    rule "absNI_Remote_GetX_PutX"
(dst != Home) & (Sta.Proc[dst].CacheState = CACHE_E) & existsbuf(Plxx,PI_Local_GetX_GetX) & existsconc(Plxx,PI_Local_GetX_GetX,dst) 
    ==>
    var
        NxtSta : STATE;
    begin
        NxtSta := Sta;
        NxtSta.Proc[dst].CacheState := CACHE_I;
        undefine NxtSta.Proc[dst].CacheData;
        if Other != Home then
            NxtSta.ShWbMsg.Cmd := SHWB_FAck;
            NxtSta.ShWbMsg.Proc := Other;
            undefine NxtSta.ShWbMsg.Data;
        endif;
        --NxtSta.FwdCmd := UNI_None;
        --NxtSta.FwdSrc := Other;
        Sta := NxtSta;
        nondet0 := false;
--assert existsconc(Plxx,PI_Local_GetX_GetX,dst);
--assert (existsconc(Plxx,PI_Local_GetX_GetX,dst));
removename(Plxx,PI_Local_GetX_GetX,dst);
removenameother(Plxx,PI_Local_GetX_GetX);
    end
;
end;
ruleset
    dst : NODE
do
    rule "absNI_Remote_GetX_PutX"
(dst != Home) & (Sta.Proc[dst].CacheState = CACHE_E) & existsbuf(Nlxx,NI_Local_GetX_GetX) & existsconc(Nlxx,NI_Local_GetX_GetX,dst)
    ==>
    var
        NxtSta : STATE;
    begin
        NxtSta := Sta;
        NxtSta.Proc[dst].CacheState := CACHE_I;
        undefine NxtSta.Proc[dst].CacheData;
        if Other != Home then
            NxtSta.ShWbMsg.Cmd := SHWB_FAck;
            NxtSta.ShWbMsg.Proc := Other;
            undefine NxtSta.ShWbMsg.Data;
        endif;
        --NxtSta.FwdCmd := UNI_None;
        --NxtSta.FwdSrc := Other;
        Sta := NxtSta;
        nondet0 := false;
--assert (existsconc(Nlxx,NI_Local_GetX_GetX,dst));
removename(Nlxx,NI_Local_GetX_GetX,dst);
removenameother(Nlxx,NI_Local_GetX_GetX);
    end
;
end;
ruleset
    src : NODE;
    dst : NODE
do
    rule "NI_Remote_GetX_PutX"
      ((((src != dst) & (dst != Home)) & (Sta.UniMsg[src].Cmd = UNI_GetX)) & (
       Sta.UniMsg[src].Proc = dst)) & (Sta.Proc[dst].CacheState = CACHE_E)
    ==>
    var
        NxtSta : STATE;
    begin
        NxtSta := Sta;
        NxtSta.Proc[dst].CacheState := CACHE_I;
        undefine NxtSta.Proc[dst].CacheData;
        NxtSta.UniMsg[src].Cmd := UNI_PutX;
        NxtSta.UniMsg[src].Proc := dst;
        NxtSta.UniMsg[src].Data := Sta.Proc[dst].CacheData;
        if src != Home then
            NxtSta.ShWbMsg.Cmd := SHWB_FAck;
            NxtSta.ShWbMsg.Proc := src;
            undefine NxtSta.ShWbMsg.Data;
        endif;
        --NxtSta.FwdCmd := UNI_None;
        --NxtSta.FwdSrc := src;
        Sta := NxtSta;
        nondet0 := false;
if (src != Home) then
assert (existsconc(Plxx,PI_Local_GetX_GetX,dst)&existsconc(Plxx,PI_Local_GetX_GetX,src) | existsconc(Nlxx,NI_Local_GetX_GetX,dst)&existsconc(Nlxx,NI_Local_GetX_GetX,src));
else 
assert (existsconc(Plxx,PI_Local_GetX_GetX,dst)| existsconc(Nlxx,NI_Local_GetX_GetX,dst));
endif;

if existsconc(Plxx,PI_Local_GetX_GetX,dst) then
removename(Plxx,PI_Local_GetX_GetX,dst);
if (src != Home) then removename(Plxx,PI_Local_GetX_GetX,src);endif;
else
removename(Nlxx,NI_Local_GetX_GetX,dst);
if (src != Home) then removename(Nlxx,NI_Local_GetX_GetX,src);endif;
endif;

    end
;
end;
rule "NI_Local_Put"
  Sta.UniMsg[Home].Cmd = UNI_Put
==>
var
    NxtSta : STATE;
begin
    NxtSta := Sta;
    NxtSta.UniMsg[Home].Cmd := UNI_None;
    undefine NxtSta.UniMsg[Home].Proc;
    undefine NxtSta.UniMsg[Home].Data;
    NxtSta.Dir.Pending := false;
    NxtSta.Dir.Dirty := false;
    NxtSta.Dir.Local := true;
    NxtSta.MemData := Sta.UniMsg[Home].Data;
    NxtSta.Proc[Home].ProcCmd := NODE_None;
    if Sta.Proc[Home].InvMarked then
        NxtSta.Proc[Home].InvMarked := false;
        NxtSta.Proc[Home].CacheState := CACHE_I;
        undefine NxtSta.Proc[Home].CacheData;
    else
        NxtSta.Proc[Home].CacheState := CACHE_S;
        NxtSta.Proc[Home].CacheData := Sta.UniMsg[Home].Data;
    endif;
    Sta := NxtSta;
    nondet0 := false;
end;
    rule "absNI_Remote_Put"
      Other != Home
    ==>
    var
        NxtSta : STATE;
    begin
        NxtSta := Sta;
        Sta := NxtSta;
        nondet0 := false;
    end
;
ruleset
    dst : NODE
do
    rule "NI_Remote_Put"
      (dst != Home) & (Sta.UniMsg[dst].Cmd = UNI_Put)
    ==>
    var
        NxtSta : STATE;
    begin
        NxtSta := Sta;
        NxtSta.UniMsg[dst].Cmd := UNI_None;
        undefine NxtSta.UniMsg[dst].Proc;
        undefine NxtSta.UniMsg[dst].Data;
        NxtSta.Proc[dst].ProcCmd := NODE_None;
        if Sta.Proc[dst].InvMarked then
            NxtSta.Proc[dst].InvMarked := false;
            NxtSta.Proc[dst].CacheState := CACHE_I;
            undefine NxtSta.Proc[dst].CacheData;
        else
            NxtSta.Proc[dst].CacheState := CACHE_S;
            NxtSta.Proc[dst].CacheData := Sta.UniMsg[dst].Data;
        endif;
        Sta := NxtSta;
        nondet0 := false;
    end
;
end;
rule "NI_Local_PutXAcksDone"
  Sta.UniMsg[Home].Cmd = UNI_PutX
==>
var
    NxtSta : STATE;
begin
    NxtSta := Sta;
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
    NxtSta.Proc[Home].CacheData := Sta.UniMsg[Home].Data;
    Sta := NxtSta;
    nondet0 := false;
end;
    rule "absNI_Remote_PutX"
      Other != Home
    ==>
    var
        NxtSta : STATE;
    begin
        NxtSta := Sta;
        Sta := NxtSta;
        nondet0 := false;
    end
;
ruleset
    dst : NODE
do
    rule "NI_Remote_PutX"
      ((dst != Home) & (Sta.UniMsg[dst].Cmd = UNI_PutX)) & (Sta.Proc[dst].ProcCmd = NODE_GetX)
    ==>
    var
        NxtSta : STATE;
    begin
        NxtSta := Sta;
        NxtSta.UniMsg[dst].Cmd := UNI_None;
        undefine NxtSta.UniMsg[dst].Proc;
        undefine NxtSta.UniMsg[dst].Data;
        NxtSta.Proc[dst].ProcCmd := NODE_None;
        NxtSta.Proc[dst].InvMarked := false;
        NxtSta.Proc[dst].CacheState := CACHE_E;
        NxtSta.Proc[dst].CacheData := Sta.UniMsg[dst].Data;
        Sta := NxtSta;
        nondet0 := false;
    end
;
end;
    rule "absNI_Inv"
      Other != Home
    ==>
    var
        NxtSta : STATE;
    begin
        NxtSta := Sta;
        Sta := NxtSta;
        nondet0 := false;
    end
;
ruleset
    dst : NODE
do
    rule "NI_Inv"
      (dst != Home) & (Sta.InvMsg[dst].Cmd = INV_Inv)
    ==>
    var
        NxtSta : STATE;
    begin
        NxtSta := Sta;
        NxtSta.InvMsg[dst].Cmd := INV_InvAck;
        NxtSta.Proc[dst].CacheState := CACHE_I;
        undefine NxtSta.Proc[dst].CacheData;
        if Sta.Proc[dst].ProcCmd = NODE_Get then
            NxtSta.Proc[dst].InvMarked := true;
        endif;
        Sta := NxtSta;
        nondet0 := false;
    end
;
end;
    rule "absNI_InvAck"
      (Other != Home) & Sta.Dir.Pending & (Sta.NakcMsg.Cmd = NAKC_None & Sta.ShWbMsg.Cmd = SHWB_None) & Sta.Collecting
--lemma2
    ==>
    var
        NxtSta : STATE;
    begin
        NxtSta := Sta;
        if exists p : NODE do true & Sta.Dir.InvSet[p] end | nondet0 then
            --NxtSta.LastInvAck := Other;
            for p : NODE do
                if true & Sta.Dir.InvSet[p] then
                   -- NxtSta.LastOtherInvAck := p;
                endif;
            endfor;
        else
            NxtSta.Dir.Pending := false;
            if Sta.Dir.Local & (! (Sta.Dir.Dirty)) then
                NxtSta.Dir.Local := false;
            endif;
            NxtSta.Collecting := false;
            --NxtSta.LastInvAck := Other;
        endif;
        Sta := NxtSta;
        nondet0 := false;
    end
;
ruleset
    src : NODE
do
    rule "NI_InvAck"
      (((src != Home) & (Sta.InvMsg[src].Cmd = INV_InvAck)) & Sta.Dir.Pending) & Sta.Dir.InvSet[src]
    ==>
    var
        NxtSta : STATE;
    begin
        NxtSta := Sta;
        NxtSta.InvMsg[src].Cmd := INV_None;
        NxtSta.Dir.InvSet[src] := false;
        if exists p : NODE do (p != src) & Sta.Dir.InvSet[p] end | nondet0 then
            --NxtSta.LastInvAck := src;
            for p : NODE do
                if (p != src) & Sta.Dir.InvSet[p] then
                   -- NxtSta.LastOtherInvAck := p;
                endif;
            endfor;
        else
            NxtSta.Dir.Pending := false;
            if Sta.Dir.Local & (! (Sta.Dir.Dirty)) then
                NxtSta.Dir.Local := false;
            endif;
            NxtSta.Collecting := false;
            --NxtSta.LastInvAck := src;
        endif;
        Sta := NxtSta;
        nondet0 := false;
    end
;
end;
rule "NI_Wb"
  Sta.WbMsg.Cmd = WB_Wb
==>
var
    NxtSta : STATE;
begin
    NxtSta := Sta;
    NxtSta.WbMsg.Cmd := WB_None;
    undefine NxtSta.WbMsg.Proc;
    undefine NxtSta.WbMsg.Data;
    NxtSta.Dir.Dirty := false;
    NxtSta.Dir.HeadVld := false;
    undefine NxtSta.Dir.HeadPtr;
    NxtSta.MemData := Sta.WbMsg.Data;
    Sta := NxtSta;
    nondet0 := false;
end;
rule "NI_FAck"
  Sta.ShWbMsg.Cmd = SHWB_FAck
==>
var
    NxtSta : STATE;
begin
    NxtSta := Sta;
    NxtSta.ShWbMsg.Cmd := SHWB_None;
    undefine NxtSta.ShWbMsg.Proc;
    undefine NxtSta.ShWbMsg.Data;
    NxtSta.Dir.Pending := false;
    if Sta.Dir.Dirty then
        NxtSta.Dir.HeadPtr := Sta.ShWbMsg.Proc;
    endif;
    Sta := NxtSta;
    nondet0 := false;
end;
rule "NI_ShWb"
  Sta.ShWbMsg.Cmd = SHWB_ShWb
==>
var
    NxtSta : STATE;
begin
    NxtSta := Sta;
    NxtSta.ShWbMsg.Cmd := SHWB_None;
    undefine NxtSta.ShWbMsg.Proc;
    undefine NxtSta.ShWbMsg.Data;
    NxtSta.Dir.Pending := false;
    NxtSta.Dir.Dirty := false;
    NxtSta.Dir.ShrVld := true;
    for p : NODE do
        NxtSta.Dir.ShrSet[p] := (p = Sta.ShWbMsg.Proc) | Sta.Dir.ShrSet[p];
        NxtSta.Dir.InvSet[p] := (p = Sta.ShWbMsg.Proc) | Sta.Dir.ShrSet[p];
    endfor;
    NxtSta.MemData := Sta.ShWbMsg.Data;
    Sta := NxtSta;
    nondet0 := false;
end;
    rule "absNI_Replace"
      true
    ==>
    var
        NxtSta : STATE;
    begin
        NxtSta := Sta;
        Sta := NxtSta;
        nondet0 := false;
    end
;
ruleset
    src : NODE
do
    rule "NI_Replace"
      Sta.RpMsg[src].Cmd = RP_Replace
    ==>
    var
        NxtSta : STATE;
    begin
        NxtSta := Sta;
        NxtSta.RpMsg[src].Cmd := RP_None;
        if Sta.Dir.ShrVld then
            NxtSta.Dir.ShrSet[src] := false;
            NxtSta.Dir.InvSet[src] := false;
        endif;
        Sta := NxtSta;
        nondet0 := false;
    end
;
end;

rule "setnondet"
  TRUE
==>
begin
    system_nondet := TRUE;
end;
rule "resetnondet"
  TRUE
==>
begin
    system_nondet := FALSE;
end;


invariant "lemma1"
forall p: NODE do forall q: NODE do (p != Home & p != q) -> ((Sta.Proc[p].CacheState = CACHE_E) -> (Sta.Dir.Dirty &  Sta.WbMsg.Cmd != WB_Wb  & Sta.ShWbMsg.Cmd != SHWB_ShWb &  Sta.UniMsg[Home].Cmd != UNI_Put & Sta.Proc[q].CacheState != CACHE_E & Sta.UniMsg[q].Cmd != UNI_PutX)) end end;

invariant "lemma2"
forall p : NODE do (Sta.InvMsg[p].Cmd = INV_InvAck ->  (Sta.NakcMsg.Cmd = NAKC_None & Sta.ShWbMsg.Cmd = SHWB_None & Sta.Collecting))
     end;

invariant "CacheStateProp"
    forall p : NODE do forall q : NODE do (p != q) -> (! (((Sta.Proc[p].CacheState = CACHE_E) & (
                                                           Sta.Proc[q].CacheState = CACHE_E)))) end end;

--| End of model

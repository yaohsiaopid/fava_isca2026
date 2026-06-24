// Set up common formal environment for CVA6 with symbolic instruction being
// driven at IF stage and assumptions that constrain the inputs from frontend,
// which is bbox for verificaiton purpose

// Post-trace: any instruction encoding but invalid
// Assume IUV issued at first cycle after reset
// Symbolic reset on the memory and regfile
`define INTRA_TRANSMITTER 

// =============================================================================
// Frontend-legal-setup (since we bbox) and processor in operation
// =============================================================================

//BBOX_AMO_REQ: assume property (@(posedge clk_i) 
//      commit_stage_i.amo_resp_i.ack == 1'b0);
//BRANCH: assume property (@(posedge clk_i) 
//      id_stage_i.fetch_entry_i.branch_predict.predict_address != pc0);

NON_EXCEPTION_FRONTEND: assume property (@(posedge clk_i)
  i_frontend.fetch_entry_o.ex.valid == 1'b0
  // tag this fetched instruction is not exceptioned already at front-end
  // (e.g., INSTR_PAGE_FAULT or INSTR_ACCESS_FAULT)
);
IF_ID_CONTRACT: assume property (@(posedge clk_i)
  // yet ack then hold
  (id_stage_i.fetch_entry_valid_i && !(fetch_ready_id_if)) |=>
  (
  ($past(id_stage_i.fetch_entry_valid_i) == id_stage_i.fetch_entry_valid_i) &&
  ($past(id_stage_i.instruction) == id_stage_i.instruction) &&
  ($past(id_stage_i.fetch_entry_i.address) == id_stage_i.fetch_entry_i.address)
  )
);

IN_OP_MODE: assume property (@(posedge clk_i) rst_ni == 1'd1);
NOHALT: assume property (@(posedge clk_i) commit_stage_i.halt_i == 1'b0);

// =============================================================================
// Set up instruction of interest 
// =============================================================================
wire [32-1:0] i0;
i0_const: assume property (@(posedge clk_i) CONST(i0));

// =============================================================================
// Set up pc value, instruction issue, and execution contexts
// =============================================================================
// (pc0, i0)
wire [64-1:0] pc0;

pc0_const: assume property (@(posedge clk_i) CONST(pc0));
pc0_nozero: assume property (@(posedge clk_i) pc0 != '0);

wire instn_begin = (id_stage_i.fetch_entry_valid_i && 
                    id_stage_i.fetch_entry_i.address == pc0);

pc0_i0_assoc_1: assume property (@(posedge clk_i) 
    id_stage_i.fetch_entry_i.address == pc0 |-> id_stage_i.instruction == i0);
pc0_i0_assoc_2: assume property (@(posedge clk_i) 
    id_stage_i.fetch_entry_i.address == pc0 |-> 
    (id_stage_i.fetch_entry_valid_i == 1'b1 && 
`ifndef SYSINSN
    id_stage_i.decoded_instruction.ex.valid == 1'b0) 
`else
    id_stage_i.fetch_entry_i.ex.valid == 1'b0)
`endif
    // IF issuing a valid request, i.e. no exception raised so far at IF
);

VALID_INSTN: assume property (@(posedge clk_i) id_stage_i.fetch_entry_valid_i);

ISSUE_ONCE: assume property (@(posedge clk_i) instn_begin |=> 
        always !(id_stage_i.fetch_entry_i.address == pc0));
EVENTUAL_ISSUE: assume property (@(posedge clk_i) first |->
    s_eventually(instn_begin));
EXE_IUV: assume property (@(posedge clk_i) instn_begin |-> fetch_ready_id_if);

// Setting up i1
wire [32-1:0] i1;
i1_const: assume property (@(posedge clk_i) CONST(i1));

wire [64-1:0] pc1;

pc1_const: assume property (@(posedge clk_i) CONST(pc1));
pc1_nozero: assume property (@(posedge clk_i) pc1 != '0);
pc1_pc0_distinct: assume property (@(posedge clk_i) pc1 != pc0);

wire i1_instn_begin = (id_stage_i.fetch_entry_valid_i && 
                    id_stage_i.fetch_entry_i.address == pc1);

pc1_i1_assoc_1: assume property (@(posedge clk_i) 
    id_stage_i.fetch_entry_i.address == pc1 |-> id_stage_i.instruction == i1);
pc1_i1_assoc_2: assume property (@(posedge clk_i) 
    id_stage_i.fetch_entry_i.address == pc1 |-> 
    (id_stage_i.fetch_entry_valid_i == 1'b1 && 
    id_stage_i.fetch_entry_i.ex.valid == 1'b0)
    // IF issuing a valid request, i.e. no exception raised so far at IF
);
I1_ISSUE_ONCE: assume property (@(posedge clk_i) i1_instn_begin |=> 
        always !(id_stage_i.fetch_entry_i.address == pc1));
I1_EVENTUAL_ISSUE: assume property (@(posedge clk_i) first |->
    s_eventually(i1_instn_begin));

// i0 is fetched in program order before i1
reg i0_hpn;
always @(posedge clk_i) begin
  if (~rst_ni) begin
    i0_hpn <= '0;
  end else begin
    if (instn_begin) begin
      i0_hpn <= 1'b1;
    end 
  end 
end 
I0_PO_I1: assume property (@(posedge clk_i) !i0_hpn -> !i1_instn_begin);

// =============================================================================
// ## Performing location annotation
// =============================================================================
`include "/cafe/u/yaohsiao/scratch/synthlc_tutorial/fv/InterHBI/i0_pl.sv"
`include "/cafe/u/yaohsiao/scratch/synthlc_tutorial/fv/InterHBI/i1_pl.sv"

// -----------------------
// Same address constraint
// -----------------------

wire [64-1:0] addr0;
addr0_const: assume property (@(posedge clk_i) CONST(addr0));
// register-read stage
i0_addr: assume property (@(posedge clk_i) i0_mem_req_s1 |-> 
  ex_stage_i.lsu_i.dcache_req_ports_o_st.virtual_address == addr0);
i1_addr: assume property (@(posedge clk_i) i1_mem_req_s1 |-> 
  ex_stage_i.lsu_i.dcache_req_ports_o_ld.virtual_address == addr0);


i_SW_0: assume property (i0[14:12] == 3'b010);
i_SW_1: assume property (i0[6:0] == 7'b0100011);
i1_LW_0: assume property (i1[14:12] == 3'b010);
i1_LW_1: assume property (i1[11:7] != 5'd0);
i1_LW_2: assume property (i1[6:0] == 7'b0000011);
wire e0 = i0_mem_req_s1 ;  // Write-PL
wire e1 = i1_mem_req_s1 ;  // Read-PL

reg e0_hpn;
always @(posedge clk_i) begin
    if (!rst_ni) 
        e0_hpn <= 1'b0;
    else if (e0)
        e0_hpn <= 1'b1;
end
reg e1_hpn;
always @(posedge clk_i) begin
    if (!rst_ni) 
        e1_hpn <= 1'b0;
    else if (e1)
        e1_hpn <= 1'b1;
end

reg e0_hb_e1;
always @(posedge clk_i) begin
    if (!rst_ni)
        e0_hb_e1 <= 1'b0;
    else begin
        if (e0 && !e0_hpn) 
          e0_hb_e1 <= !(e1_hpn || e1);  // 1 iff no re-ordering
    end 
end 
reg i0_cmt_hpn;
always @(posedge clk_i) begin
    if (!rst_ni)
        i0_cmt_hpn <= 1'b0;
    else if (i0_scb_0_s13|i0_scb_1_s13|i0_scb_2_s13|i0_scb_3_s13)
        i0_cmt_hpn <= 1'b1;
end
reg i1_cmt_hpn;
always @(posedge clk_i) begin
    if (!rst_ni)
        i1_cmt_hpn <= 1'b0;
    else if (i1_scb_0_s13|i1_scb_1_s13|i1_scb_2_s13|i1_scb_3_s13)
        i1_cmt_hpn <= 1'b1;
end

HB_0: assert property (@(posedge clk_i) 
  (i1_cmt_hpn & i0_cmt_hpn & e0_hpn) |-> e0_hb_e1);
// `ifndef WHB
// HB_6: assert property (@(posedge clk_i) (e0 && !e0_hpn) |-> !(e1_hpn || e1));
// `else 
// //C_6: cover property (@(posedge clk_i) (e0 && !e0_hpn) && (e1 && !e1_hpn));
// WHB_6: assert property (@(posedge clk_i) (e0 && !e0_hpn) |-> !e1_hpn);
// WHB_CONCUR_6: assert property (@(posedge clk_i) (e0 && !e0_hpn) |-> (e1 && !e1_hpn));
// `endif 

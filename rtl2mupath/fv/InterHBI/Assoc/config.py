issue_assoc_addr = ("issue_s16", "issue_stage_i.i_issue_read_operands.fu_data_o.operand_a + issue_stage_i.i_issue_read_operands.fu_data_o.imm")
w_pls = [("mem_req_s1", "ex_stage_i.lsu_i.dcache_req_ports_o_st.virtual_address", "ex_stage_i.lsu_i.dcache_req_ports_o_st.data_wdata")]
r_pls = [("mem_req_s1", "ex_stage_i.lsu_i.dcache_req_ports_o_ld.virtual_address", "ex_stage_i.lsu_i.dcache_req_ports_o_ld.data_wdata")]
pth = os.path.abspath(os.path.join(os.getcwd(), '../'))
with open("out/
h_ += f"`include \"{pth}/i0_pl.sv\" \n"
h_ += f"`include \"{pth}/i1_pl.sv\" \n"

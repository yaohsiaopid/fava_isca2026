cover -name {taint_rs1_src_scb_1_s12_dest_1} {@(posedge clk_i) scb_1_s12 ##1 ( !scb_1_s13 && scb_1_s12 && 1'b1 && (|{scb_1_s12_t0, 1'b0}))}
cover -name {taint_rs1_src_scb_1_s12_dest_2} {@(posedge clk_i) scb_1_s12 ##1 ( scb_1_s13 && !scb_1_s12 && 1'b1 && (|{scb_1_s13_t0, 1'b0}))}
cover -name {taint_rs1_src_scb_2_s12_dest_1} {@(posedge clk_i) scb_2_s12 ##1 ( scb_2_s12 && !scb_2_s13 && 1'b1 && (|{scb_2_s12_t0, 1'b0}))}
cover -name {taint_rs1_src_scb_2_s12_dest_2} {@(posedge clk_i) scb_2_s12 ##1 ( !scb_2_s12 && scb_2_s13 && 1'b1 && (|{scb_2_s13_t0, 1'b0}))}
cover -name {taint_rs1_src_scb_3_s12_dest_1} {@(posedge clk_i) scb_3_s12 ##1 ( scb_3_s12 && !scb_3_s13 && 1'b1 && (|{scb_3_s12_t0, 1'b0}))}
cover -name {taint_rs1_src_scb_3_s12_dest_2} {@(posedge clk_i) scb_3_s12 ##1 ( !scb_3_s12 && scb_3_s13 && 1'b1 && (|{scb_3_s13_t0, 1'b0}))}
cover -name {taint_rs1_src_stb_com_0_s1_dest_0} {@(posedge clk_i) stb_com_0_s1 ##1 ( !mem_req_s1 && !stb_com_0_s1 && 1'b1 && (|{mem_req_s1_t0, stb_com_0_s1_t0, 1'b0}))}
cover -name {taint_rs1_src_stb_com_0_s1_dest_1} {@(posedge clk_i) stb_com_0_s1 ##1 ( !mem_req_s1 && stb_com_0_s1 && 1'b1 && (|{stb_com_0_s1_t0, 1'b0}))}
cover -name {taint_rs1_src_stb_com_0_s1_dest_2} {@(posedge clk_i) stb_com_0_s1 ##1 ( mem_req_s1 && stb_com_0_s1 && 1'b1 && (|{mem_req_s1_t0, stb_com_0_s1_t0, 1'b0}))}
cover -name {taint_rs1_src_stb_com_1_s1_dest_0} {@(posedge clk_i) stb_com_1_s1 ##1 ( !mem_req_s1 && !stb_com_1_s1 && 1'b1 && (|{mem_req_s1_t0, stb_com_1_s1_t0, 1'b0}))}
cover -name {taint_rs1_src_stb_com_1_s1_dest_1} {@(posedge clk_i) stb_com_1_s1 ##1 ( !mem_req_s1 && stb_com_1_s1 && 1'b1 && (|{stb_com_1_s1_t0, 1'b0}))}
cover -name {taint_rs1_src_stb_com_1_s1_dest_2} {@(posedge clk_i) stb_com_1_s1 ##1 ( mem_req_s1 && stb_com_1_s1 && 1'b1 && (|{mem_req_s1_t0, stb_com_1_s1_t0, 1'b0}))}
cover -name {taint_rs1_src_stb_spec_0_s1_dest_1} {@(posedge clk_i) stb_spec_0_s1 ##1 ( !mem_req_s1 && !stb_com_0_s1 && stb_spec_0_s1 && 1'b1 && (|{stb_spec_0_s1_t0, 1'b0}))}
cover -name {taint_rs1_src_stb_spec_0_s1_dest_2} {@(posedge clk_i) stb_spec_0_s1 ##1 ( !mem_req_s1 && stb_com_0_s1 && !stb_spec_0_s1 && 1'b1 && (|{stb_com_0_s1_t0, 1'b0}))}
cover -name {taint_rs1_src_stb_spec_0_s1_dest_3} {@(posedge clk_i) stb_spec_0_s1 ##1 ( mem_req_s1 && stb_com_0_s1 && !stb_spec_0_s1 && 1'b1 && (|{mem_req_s1_t0, stb_com_0_s1_t0, 1'b0}))}
cover -name {taint_rs1_src_stb_spec_1_s1_dest_1} {@(posedge clk_i) stb_spec_1_s1 ##1 ( !mem_req_s1 && !stb_com_1_s1 && stb_spec_1_s1 && 1'b1 && (|{stb_spec_1_s1_t0, 1'b0}))}
cover -name {taint_rs1_src_stb_spec_1_s1_dest_3} {@(posedge clk_i) stb_spec_1_s1 ##1 ( mem_req_s1 && stb_com_1_s1 && !stb_spec_1_s1 && 1'b1 && (|{mem_req_s1_t0, stb_com_1_s1_t0, 1'b0}))}

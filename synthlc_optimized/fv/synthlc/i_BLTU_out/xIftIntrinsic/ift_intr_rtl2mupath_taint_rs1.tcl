cover -name {taint_rs1_src_issue_s1_dest_2} {@(posedge clk_i) issue_s1 ##1 ( !scb_2_s13 && !scb_2_s14 && !scb_1_s12 && !scb_3_s12 && scb_3_s13 && !scb_0_s14 && !scb_3_s14 && !scb_2_s12 && !scb_0_s13 && !scb_0_s12 && !scb_1_s14 && !scb_1_s13 && 1'b1 && (|{scb_3_s13_t0, 1'b0}))}
cover -name {taint_rs1_src_issue_s1_dest_5} {@(posedge clk_i) issue_s1 ##1 ( scb_2_s13 && !scb_2_s14 && !scb_1_s12 && !scb_3_s12 && !scb_3_s13 && !scb_0_s14 && !scb_3_s14 && !scb_2_s12 && !scb_0_s13 && !scb_0_s12 && !scb_1_s14 && !scb_1_s13 && 1'b1 && (|{scb_2_s13_t0, 1'b0}))}
cover -name {taint_rs1_src_issue_s1_dest_8} {@(posedge clk_i) issue_s1 ##1 ( !scb_2_s13 && !scb_2_s14 && !scb_1_s12 && !scb_3_s12 && !scb_3_s13 && !scb_0_s14 && !scb_3_s14 && !scb_2_s12 && !scb_0_s13 && !scb_0_s12 && !scb_1_s14 && scb_1_s13 && 1'b1 && (|{scb_1_s13_t0, 1'b0}))}
cover -name {taint_rs1_src_issue_s1_dest_11} {@(posedge clk_i) issue_s1 ##1 ( !scb_2_s13 && !scb_2_s14 && !scb_1_s12 && !scb_3_s12 && !scb_3_s13 && !scb_0_s14 && !scb_3_s14 && !scb_2_s12 && scb_0_s13 && !scb_0_s12 && !scb_1_s14 && !scb_1_s13 && 1'b1 && (|{scb_0_s13_t0, 1'b0}))}
cover -name {taint_rs1_src_scb_0_s8_dest_2} {@(posedge clk_i) scb_0_s8 ##1 ( !scb_0_s12 && scb_0_s13 && !scb_0_s14 && 1'b1 && (|{scb_0_s13_t0, 1'b0}))}
cover -name {taint_rs1_src_scb_1_s8_dest_2} {@(posedge clk_i) scb_1_s8 ##1 ( !scb_1_s14 && !scb_1_s12 && scb_1_s13 && 1'b1 && (|{scb_1_s13_t0, 1'b0}))}
cover -name {taint_rs1_src_scb_1_s12_dest_1} {@(posedge clk_i) scb_1_s12 ##1 ( scb_1_s12 && !scb_1_s13 && 1'b1 && (|{scb_1_s12_t0, 1'b0}))}
cover -name {taint_rs1_src_scb_1_s12_dest_2} {@(posedge clk_i) scb_1_s12 ##1 ( !scb_1_s12 && scb_1_s13 && 1'b1 && (|{scb_1_s13_t0, 1'b0}))}
cover -name {taint_rs1_src_scb_2_s8_dest_2} {@(posedge clk_i) scb_2_s8 ##1 ( !scb_2_s12 && scb_2_s13 && !scb_2_s14 && 1'b1 && (|{scb_2_s13_t0, 1'b0}))}
cover -name {taint_rs1_src_scb_2_s12_dest_1} {@(posedge clk_i) scb_2_s12 ##1 ( scb_2_s12 && !scb_2_s13 && 1'b1 && (|{scb_2_s12_t0, 1'b0}))}
cover -name {taint_rs1_src_scb_2_s12_dest_2} {@(posedge clk_i) scb_2_s12 ##1 ( !scb_2_s12 && scb_2_s13 && 1'b1 && (|{scb_2_s13_t0, 1'b0}))}
cover -name {taint_rs1_src_scb_3_s8_dest_2} {@(posedge clk_i) scb_3_s8 ##1 ( !scb_3_s12 && scb_3_s13 && !scb_3_s14 && 1'b1 && (|{scb_3_s13_t0, 1'b0}))}
cover -name {taint_rs1_src_scb_3_s12_dest_1} {@(posedge clk_i) scb_3_s12 ##1 ( scb_3_s12 && !scb_3_s13 && 1'b1 && (|{scb_3_s12_t0, 1'b0}))}
cover -name {taint_rs1_src_scb_3_s12_dest_2} {@(posedge clk_i) scb_3_s12 ##1 ( !scb_3_s12 && scb_3_s13 && 1'b1 && (|{scb_3_s13_t0, 1'b0}))}
cover -name {taint_rs1_src_scb_1_s14_dest_0} {@(posedge clk_i) scb_1_s14 ##1 ( !scb_1_s14 && 1'b1 && (|{scb_1_s14_t0, 1'b0}))}
cover -name {taint_rs1_src_scb_1_s14_dest_1} {@(posedge clk_i) scb_1_s14 ##1 ( scb_1_s14 && 1'b1 && (|{scb_1_s14_t0, 1'b0}))}
cover -name {taint_rs1_src_scb_2_s14_dest_1} {@(posedge clk_i) scb_2_s14 ##1 ( scb_2_s14 && 1'b1 && (|{scb_2_s14_t0, 1'b0}))}
cover -name {taint_rs1_src_scb_3_s14_dest_1} {@(posedge clk_i) scb_3_s14 ##1 ( scb_3_s14 && 1'b1 && (|{scb_3_s14_t0, 1'b0}))}

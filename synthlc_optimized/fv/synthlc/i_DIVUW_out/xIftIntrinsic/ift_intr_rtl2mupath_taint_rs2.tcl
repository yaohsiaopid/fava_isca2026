cover -name {taint_rs2_src_div_s1_dest_0} {@(posedge clk_i) div_s1 ##1 ( !div_s2 && !div_s1 && 1'b1 && (|{div_s2_t0, div_s1_t0, 1'b0}))}
cover -name {taint_rs2_src_div_s1_dest_1} {@(posedge clk_i) div_s1 ##1 ( !div_s2 && div_s1 && 1'b1 && (|{div_s1_t0, 1'b0}))}
cover -name {taint_rs2_src_div_s1_dest_2} {@(posedge clk_i) div_s1 ##1 ( div_s2 && !div_s1 && 1'b1 && (|{div_s2_t0, 1'b0}))}
cover -name {taint_rs2_src_scb_0_s8_dest_1} {@(posedge clk_i) scb_0_s8 ##1 ( !scb_0_s12 && scb_0_s8 && !scb_0_s13 && 1'b1 && (|{scb_0_s8_t0, 1'b0}))}
cover -name {taint_rs2_src_scb_0_s8_dest_2} {@(posedge clk_i) scb_0_s8 ##1 ( !scb_0_s12 && !scb_0_s8 && scb_0_s13 && 1'b1 && (|{scb_0_s13_t0, 1'b0}))}
cover -name {taint_rs2_src_scb_0_s8_dest_3} {@(posedge clk_i) scb_0_s8 ##1 ( scb_0_s12 && !scb_0_s8 && !scb_0_s13 && 1'b1 && (|{scb_0_s12_t0, 1'b0}))}
cover -name {taint_rs2_src_scb_0_s12_dest_1} {@(posedge clk_i) scb_0_s12 ##1 ( scb_0_s12 && !scb_0_s13 && 1'b1 && (|{scb_0_s12_t0, 1'b0}))}
cover -name {taint_rs2_src_scb_1_s8_dest_1} {@(posedge clk_i) scb_1_s8 ##1 ( !scb_1_s12 && !scb_1_s13 && scb_1_s8 && 1'b1 && (|{scb_1_s8_t0, 1'b0}))}
cover -name {taint_rs2_src_scb_1_s8_dest_2} {@(posedge clk_i) scb_1_s8 ##1 ( !scb_1_s12 && scb_1_s13 && !scb_1_s8 && 1'b1 && (|{scb_1_s13_t0, 1'b0}))}
cover -name {taint_rs2_src_scb_1_s8_dest_3} {@(posedge clk_i) scb_1_s8 ##1 ( scb_1_s12 && !scb_1_s13 && !scb_1_s8 && 1'b1 && (|{scb_1_s12_t0, 1'b0}))}
cover -name {taint_rs2_src_scb_1_s12_dest_1} {@(posedge clk_i) scb_1_s12 ##1 ( scb_1_s12 && !scb_1_s13 && 1'b1 && (|{scb_1_s12_t0, 1'b0}))}
cover -name {taint_rs2_src_scb_2_s8_dest_1} {@(posedge clk_i) scb_2_s8 ##1 ( !scb_2_s12 && scb_2_s8 && !scb_2_s13 && 1'b1 && (|{scb_2_s8_t0, 1'b0}))}
cover -name {taint_rs2_src_scb_2_s8_dest_2} {@(posedge clk_i) scb_2_s8 ##1 ( !scb_2_s12 && !scb_2_s8 && scb_2_s13 && 1'b1 && (|{scb_2_s13_t0, 1'b0}))}
cover -name {taint_rs2_src_scb_2_s8_dest_3} {@(posedge clk_i) scb_2_s8 ##1 ( scb_2_s12 && !scb_2_s8 && !scb_2_s13 && 1'b1 && (|{scb_2_s12_t0, 1'b0}))}
cover -name {taint_rs2_src_scb_2_s12_dest_1} {@(posedge clk_i) scb_2_s12 ##1 ( scb_2_s12 && !scb_2_s13 && 1'b1 && (|{scb_2_s12_t0, 1'b0}))}
cover -name {taint_rs2_src_scb_2_s12_dest_2} {@(posedge clk_i) scb_2_s12 ##1 ( !scb_2_s12 && scb_2_s13 && 1'b1 && (|{scb_2_s13_t0, 1'b0}))}
cover -name {taint_rs2_src_scb_3_s8_dest_1} {@(posedge clk_i) scb_3_s8 ##1 ( !scb_3_s13 && scb_3_s8 && !scb_3_s12 && 1'b1 && (|{scb_3_s8_t0, 1'b0}))}
cover -name {taint_rs2_src_scb_3_s8_dest_2} {@(posedge clk_i) scb_3_s8 ##1 ( scb_3_s13 && !scb_3_s8 && !scb_3_s12 && 1'b1 && (|{scb_3_s13_t0, 1'b0}))}
cover -name {taint_rs2_src_scb_3_s8_dest_3} {@(posedge clk_i) scb_3_s8 ##1 ( !scb_3_s13 && !scb_3_s8 && scb_3_s12 && 1'b1 && (|{scb_3_s12_t0, 1'b0}))}
cover -name {taint_rs2_src_scb_3_s12_dest_1} {@(posedge clk_i) scb_3_s12 ##1 ( !scb_3_s13 && scb_3_s12 && 1'b1 && (|{scb_3_s12_t0, 1'b0}))}
cover -name {taint_rs2_src_scb_3_s12_dest_2} {@(posedge clk_i) scb_3_s12 ##1 ( scb_3_s13 && !scb_3_s12 && 1'b1 && (|{scb_3_s13_t0, 1'b0}))}

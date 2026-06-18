assume -name {i_ANDI_0} {i0[14:12] == 3'b111}
assume -name {i_ANDI_1} {i0[11:7] != 5'd0}
assume -name {i_ANDI_2} {i0[6:0] == 7'b0010011}
cover -name cvr_src_first__decode_s1 {decode_s1 & !issue_s32 & !scb_0_s8 & !scb_0_s12 & !scb_0_s13 & !scb_1_s8 & !scb_1_s12 & !scb_1_s13 & !scb_2_s8 & !scb_2_s12 & !scb_2_s13 & !scb_3_s8 & !scb_3_s12 & !scb_3_s13 & 1'b1 & ! (decode_s1_hpn | issue_s32_hpn | scb_0_s8_hpn | scb_0_s12_hpn | scb_0_s13_hpn | scb_1_s8_hpn | scb_1_s12_hpn | scb_1_s13_hpn | scb_2_s8_hpn | scb_2_s12_hpn | scb_2_s13_hpn | scb_3_s8_hpn | scb_3_s12_hpn | scb_3_s13_hpn |  1'b0) }

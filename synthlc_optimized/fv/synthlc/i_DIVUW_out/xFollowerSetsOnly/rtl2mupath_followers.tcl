assume -name {i_DIVUW_0} {i0[31:25] == 7'b0000001}
assume -name {i_DIVUW_1} {i0[14:12] == 3'b101}
assume -name {i_DIVUW_2} {i0[11:7] != 5'd0}
assume -name {i_DIVUW_3} {i0[6:0] == 7'b0111011}
cover -name cvr_src_div_s1_dest_set_ {div_s1 ##1 (( 1'b1 ) & ! (div_s2 | div_s1 |  1'b0 )) }
cover -name cvr_src_div_s1_dest_set__div_s1 {div_s1 ##1 ((div_s1 &  1'b1 ) & ! (div_s2 |  1'b0 )) }
cover -name cvr_src_div_s1_dest_set__div_s2 {div_s1 ##1 ((div_s2 &  1'b1 ) & ! (div_s1 |  1'b0 )) }
cover -name cvr_src_decode_s1_dest_set_ {decode_s1 ##1 (( 1'b1 ) & ! (issue_s8 | scb_0_s8 | scb_1_s8 | scb_2_s8 | scb_3_s8 | decode_s1 |  1'b0 )) }
cover -name cvr_src_decode_s1_dest_set__decode_s1 {decode_s1 ##1 ((decode_s1 &  1'b1 ) & ! (issue_s8 | scb_0_s8 | scb_1_s8 | scb_2_s8 | scb_3_s8 |  1'b0 )) }
cover -name cvr_src_decode_s1_dest_set__scb_3_s8 {decode_s1 ##1 ((scb_3_s8 &  1'b1 ) & ! (issue_s8 | scb_0_s8 | scb_1_s8 | scb_2_s8 | decode_s1 |  1'b0 )) }
cover -name cvr_src_decode_s1_dest_set__scb_2_s8 {decode_s1 ##1 ((scb_2_s8 &  1'b1 ) & ! (issue_s8 | scb_0_s8 | scb_1_s8 | scb_3_s8 | decode_s1 |  1'b0 )) }
cover -name cvr_src_decode_s1_dest_set__scb_1_s8 {decode_s1 ##1 ((scb_1_s8 &  1'b1 ) & ! (issue_s8 | scb_0_s8 | scb_2_s8 | scb_3_s8 | decode_s1 |  1'b0 )) }
cover -name cvr_src_decode_s1_dest_set__scb_0_s8 {decode_s1 ##1 ((scb_0_s8 &  1'b1 ) & ! (issue_s8 | scb_1_s8 | scb_2_s8 | scb_3_s8 | decode_s1 |  1'b0 )) }
cover -name cvr_src_decode_s1_dest_set__issue_s8 {decode_s1 ##1 ((issue_s8 &  1'b1 ) & ! (scb_0_s8 | scb_1_s8 | scb_2_s8 | scb_3_s8 | decode_s1 |  1'b0 )) }
cover -name cvr_src_decode_s1_dest_set__issue_s8_scb_3_s8 {decode_s1 ##1 ((issue_s8 & scb_3_s8 &  1'b1 ) & ! (scb_0_s8 | scb_1_s8 | scb_2_s8 | decode_s1 |  1'b0 )) }
cover -name cvr_src_decode_s1_dest_set__issue_s8_scb_2_s8 {decode_s1 ##1 ((issue_s8 & scb_2_s8 &  1'b1 ) & ! (scb_0_s8 | scb_1_s8 | scb_3_s8 | decode_s1 |  1'b0 )) }
cover -name cvr_src_decode_s1_dest_set__issue_s8_scb_1_s8 {decode_s1 ##1 ((issue_s8 & scb_1_s8 &  1'b1 ) & ! (scb_0_s8 | scb_2_s8 | scb_3_s8 | decode_s1 |  1'b0 )) }
cover -name cvr_src_decode_s1_dest_set__issue_s8_scb_0_s8 {decode_s1 ##1 ((issue_s8 & scb_0_s8 &  1'b1 ) & ! (scb_1_s8 | scb_2_s8 | scb_3_s8 | decode_s1 |  1'b0 )) }
cover -name cvr_src_issue_s8_dest_set_ {issue_s8 ##1 (( 1'b1 ) & ! (div_s1 | scb_0_s8 | scb_1_s8 | scb_2_s8 | scb_3_s8 |  1'b0 )) }
cover -name cvr_src_issue_s8_dest_set__scb_3_s8 {issue_s8 ##1 ((scb_3_s8 &  1'b1 ) & ! (div_s1 | scb_0_s8 | scb_1_s8 | scb_2_s8 |  1'b0 )) }
cover -name cvr_src_issue_s8_dest_set__scb_2_s8 {issue_s8 ##1 ((scb_2_s8 &  1'b1 ) & ! (div_s1 | scb_0_s8 | scb_1_s8 | scb_3_s8 |  1'b0 )) }
cover -name cvr_src_issue_s8_dest_set__scb_1_s8 {issue_s8 ##1 ((scb_1_s8 &  1'b1 ) & ! (div_s1 | scb_0_s8 | scb_2_s8 | scb_3_s8 |  1'b0 )) }
cover -name cvr_src_issue_s8_dest_set__scb_0_s8 {issue_s8 ##1 ((scb_0_s8 &  1'b1 ) & ! (div_s1 | scb_1_s8 | scb_2_s8 | scb_3_s8 |  1'b0 )) }
cover -name cvr_src_issue_s8_dest_set__div_s1 {issue_s8 ##1 ((div_s1 &  1'b1 ) & ! (scb_0_s8 | scb_1_s8 | scb_2_s8 | scb_3_s8 |  1'b0 )) }
cover -name cvr_src_issue_s8_dest_set__div_s1_scb_3_s8 {issue_s8 ##1 ((div_s1 & scb_3_s8 &  1'b1 ) & ! (scb_0_s8 | scb_1_s8 | scb_2_s8 |  1'b0 )) }
cover -name cvr_src_issue_s8_dest_set__div_s1_scb_2_s8 {issue_s8 ##1 ((div_s1 & scb_2_s8 &  1'b1 ) & ! (scb_0_s8 | scb_1_s8 | scb_3_s8 |  1'b0 )) }
cover -name cvr_src_issue_s8_dest_set__div_s1_scb_1_s8 {issue_s8 ##1 ((div_s1 & scb_1_s8 &  1'b1 ) & ! (scb_0_s8 | scb_2_s8 | scb_3_s8 |  1'b0 )) }
cover -name cvr_src_issue_s8_dest_set__div_s1_scb_0_s8 {issue_s8 ##1 ((div_s1 & scb_0_s8 &  1'b1 ) & ! (scb_1_s8 | scb_2_s8 | scb_3_s8 |  1'b0 )) }
cover -name cvr_src_scb_0_s8_dest_set_ {scb_0_s8 ##1 (( 1'b1 ) & ! (scb_0_s12 | scb_0_s13 | scb_0_s8 |  1'b0 )) }
cover -name cvr_src_scb_0_s8_dest_set__scb_0_s8 {scb_0_s8 ##1 ((scb_0_s8 &  1'b1 ) & ! (scb_0_s12 | scb_0_s13 |  1'b0 )) }
cover -name cvr_src_scb_0_s8_dest_set__scb_0_s13 {scb_0_s8 ##1 ((scb_0_s13 &  1'b1 ) & ! (scb_0_s12 | scb_0_s8 |  1'b0 )) }
cover -name cvr_src_scb_0_s8_dest_set__scb_0_s12 {scb_0_s8 ##1 ((scb_0_s12 &  1'b1 ) & ! (scb_0_s13 | scb_0_s8 |  1'b0 )) }
cover -name cvr_src_scb_0_s12_dest_set_ {scb_0_s12 ##1 (( 1'b1 ) & ! (scb_0_s13 | scb_0_s12 |  1'b0 )) }
cover -name cvr_src_scb_0_s12_dest_set__scb_0_s12 {scb_0_s12 ##1 ((scb_0_s12 &  1'b1 ) & ! (scb_0_s13 |  1'b0 )) }
cover -name cvr_src_scb_0_s12_dest_set__scb_0_s13 {scb_0_s12 ##1 ((scb_0_s13 &  1'b1 ) & ! (scb_0_s12 |  1'b0 )) }
cover -name cvr_src_scb_1_s8_dest_set_ {scb_1_s8 ##1 (( 1'b1 ) & ! (scb_1_s12 | scb_1_s13 | scb_1_s8 |  1'b0 )) }
cover -name cvr_src_scb_1_s8_dest_set__scb_1_s8 {scb_1_s8 ##1 ((scb_1_s8 &  1'b1 ) & ! (scb_1_s12 | scb_1_s13 |  1'b0 )) }
cover -name cvr_src_scb_1_s8_dest_set__scb_1_s13 {scb_1_s8 ##1 ((scb_1_s13 &  1'b1 ) & ! (scb_1_s12 | scb_1_s8 |  1'b0 )) }
cover -name cvr_src_scb_1_s8_dest_set__scb_1_s12 {scb_1_s8 ##1 ((scb_1_s12 &  1'b1 ) & ! (scb_1_s13 | scb_1_s8 |  1'b0 )) }
cover -name cvr_src_scb_1_s12_dest_set_ {scb_1_s12 ##1 (( 1'b1 ) & ! (scb_1_s13 | scb_1_s12 |  1'b0 )) }
cover -name cvr_src_scb_1_s12_dest_set__scb_1_s12 {scb_1_s12 ##1 ((scb_1_s12 &  1'b1 ) & ! (scb_1_s13 |  1'b0 )) }
cover -name cvr_src_scb_1_s12_dest_set__scb_1_s13 {scb_1_s12 ##1 ((scb_1_s13 &  1'b1 ) & ! (scb_1_s12 |  1'b0 )) }
cover -name cvr_src_scb_2_s8_dest_set_ {scb_2_s8 ##1 (( 1'b1 ) & ! (scb_2_s12 | scb_2_s13 | scb_2_s8 |  1'b0 )) }
cover -name cvr_src_scb_2_s8_dest_set__scb_2_s8 {scb_2_s8 ##1 ((scb_2_s8 &  1'b1 ) & ! (scb_2_s12 | scb_2_s13 |  1'b0 )) }
cover -name cvr_src_scb_2_s8_dest_set__scb_2_s13 {scb_2_s8 ##1 ((scb_2_s13 &  1'b1 ) & ! (scb_2_s12 | scb_2_s8 |  1'b0 )) }
cover -name cvr_src_scb_2_s8_dest_set__scb_2_s12 {scb_2_s8 ##1 ((scb_2_s12 &  1'b1 ) & ! (scb_2_s13 | scb_2_s8 |  1'b0 )) }
cover -name cvr_src_scb_2_s12_dest_set_ {scb_2_s12 ##1 (( 1'b1 ) & ! (scb_2_s13 | scb_2_s12 |  1'b0 )) }
cover -name cvr_src_scb_2_s12_dest_set__scb_2_s12 {scb_2_s12 ##1 ((scb_2_s12 &  1'b1 ) & ! (scb_2_s13 |  1'b0 )) }
cover -name cvr_src_scb_2_s12_dest_set__scb_2_s13 {scb_2_s12 ##1 ((scb_2_s13 &  1'b1 ) & ! (scb_2_s12 |  1'b0 )) }
cover -name cvr_src_scb_3_s8_dest_set_ {scb_3_s8 ##1 (( 1'b1 ) & ! (scb_3_s12 | scb_3_s13 | scb_3_s8 |  1'b0 )) }
cover -name cvr_src_scb_3_s8_dest_set__scb_3_s8 {scb_3_s8 ##1 ((scb_3_s8 &  1'b1 ) & ! (scb_3_s12 | scb_3_s13 |  1'b0 )) }
cover -name cvr_src_scb_3_s8_dest_set__scb_3_s13 {scb_3_s8 ##1 ((scb_3_s13 &  1'b1 ) & ! (scb_3_s12 | scb_3_s8 |  1'b0 )) }
cover -name cvr_src_scb_3_s8_dest_set__scb_3_s12 {scb_3_s8 ##1 ((scb_3_s12 &  1'b1 ) & ! (scb_3_s13 | scb_3_s8 |  1'b0 )) }
cover -name cvr_src_scb_3_s12_dest_set_ {scb_3_s12 ##1 (( 1'b1 ) & ! (scb_3_s13 | scb_3_s12 |  1'b0 )) }
cover -name cvr_src_scb_3_s12_dest_set__scb_3_s12 {scb_3_s12 ##1 ((scb_3_s12 &  1'b1 ) & ! (scb_3_s13 |  1'b0 )) }
cover -name cvr_src_scb_3_s12_dest_set__scb_3_s13 {scb_3_s12 ##1 ((scb_3_s13 &  1'b1 ) & ! (scb_3_s12 |  1'b0 )) }

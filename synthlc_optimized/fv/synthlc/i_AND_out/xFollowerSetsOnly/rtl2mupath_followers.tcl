assume -name {i_AND_0} {i0[31:25] == 7'b0000000}
assume -name {i_AND_1} {i0[14:12] == 3'b111}
assume -name {i_AND_2} {i0[11:7] != 5'd0}
assume -name {i_AND_3} {i0[6:0] == 7'b0110011}
cover -name cvr_src_decode_s1_dest_set_ {decode_s1 ##1 (( 1'b1 ) & ! (issue_s32 | scb_0_s8 | scb_1_s8 | scb_2_s8 | scb_3_s8 | decode_s1 |  1'b0 )) }
cover -name cvr_src_decode_s1_dest_set__decode_s1 {decode_s1 ##1 ((decode_s1 &  1'b1 ) & ! (issue_s32 | scb_0_s8 | scb_1_s8 | scb_2_s8 | scb_3_s8 |  1'b0 )) }
cover -name cvr_src_decode_s1_dest_set__scb_3_s8 {decode_s1 ##1 ((scb_3_s8 &  1'b1 ) & ! (issue_s32 | scb_0_s8 | scb_1_s8 | scb_2_s8 | decode_s1 |  1'b0 )) }
cover -name cvr_src_decode_s1_dest_set__scb_2_s8 {decode_s1 ##1 ((scb_2_s8 &  1'b1 ) & ! (issue_s32 | scb_0_s8 | scb_1_s8 | scb_3_s8 | decode_s1 |  1'b0 )) }
cover -name cvr_src_decode_s1_dest_set__scb_1_s8 {decode_s1 ##1 ((scb_1_s8 &  1'b1 ) & ! (issue_s32 | scb_0_s8 | scb_2_s8 | scb_3_s8 | decode_s1 |  1'b0 )) }
cover -name cvr_src_decode_s1_dest_set__scb_0_s8 {decode_s1 ##1 ((scb_0_s8 &  1'b1 ) & ! (issue_s32 | scb_1_s8 | scb_2_s8 | scb_3_s8 | decode_s1 |  1'b0 )) }
cover -name cvr_src_decode_s1_dest_set__issue_s32 {decode_s1 ##1 ((issue_s32 &  1'b1 ) & ! (scb_0_s8 | scb_1_s8 | scb_2_s8 | scb_3_s8 | decode_s1 |  1'b0 )) }
cover -name cvr_src_decode_s1_dest_set__issue_s32_scb_3_s8 {decode_s1 ##1 ((issue_s32 & scb_3_s8 &  1'b1 ) & ! (scb_0_s8 | scb_1_s8 | scb_2_s8 | decode_s1 |  1'b0 )) }
cover -name cvr_src_decode_s1_dest_set__issue_s32_scb_2_s8 {decode_s1 ##1 ((issue_s32 & scb_2_s8 &  1'b1 ) & ! (scb_0_s8 | scb_1_s8 | scb_3_s8 | decode_s1 |  1'b0 )) }
cover -name cvr_src_decode_s1_dest_set__issue_s32_scb_1_s8 {decode_s1 ##1 ((issue_s32 & scb_1_s8 &  1'b1 ) & ! (scb_0_s8 | scb_2_s8 | scb_3_s8 | decode_s1 |  1'b0 )) }
cover -name cvr_src_decode_s1_dest_set__issue_s32_scb_0_s8 {decode_s1 ##1 ((issue_s32 & scb_0_s8 &  1'b1 ) & ! (scb_1_s8 | scb_2_s8 | scb_3_s8 | decode_s1 |  1'b0 )) }
cover -name cvr_src_issue_s32_dest_set_ {issue_s32 ##1 (( 1'b1 ) & ! (scb_0_s12 | scb_0_s13 | scb_1_s12 | scb_1_s13 | scb_2_s12 | scb_2_s13 | scb_3_s12 | scb_3_s13 |  1'b0 )) }
cover -name cvr_src_issue_s32_dest_set__scb_3_s13 {issue_s32 ##1 ((scb_3_s13 &  1'b1 ) & ! (scb_0_s12 | scb_0_s13 | scb_1_s12 | scb_1_s13 | scb_2_s12 | scb_2_s13 | scb_3_s12 |  1'b0 )) }
cover -name cvr_src_issue_s32_dest_set__scb_3_s12 {issue_s32 ##1 ((scb_3_s12 &  1'b1 ) & ! (scb_0_s12 | scb_0_s13 | scb_1_s12 | scb_1_s13 | scb_2_s12 | scb_2_s13 | scb_3_s13 |  1'b0 )) }
cover -name cvr_src_issue_s32_dest_set__scb_2_s13 {issue_s32 ##1 ((scb_2_s13 &  1'b1 ) & ! (scb_0_s12 | scb_0_s13 | scb_1_s12 | scb_1_s13 | scb_2_s12 | scb_3_s12 | scb_3_s13 |  1'b0 )) }
cover -name cvr_src_issue_s32_dest_set__scb_2_s12 {issue_s32 ##1 ((scb_2_s12 &  1'b1 ) & ! (scb_0_s12 | scb_0_s13 | scb_1_s12 | scb_1_s13 | scb_2_s13 | scb_3_s12 | scb_3_s13 |  1'b0 )) }
cover -name cvr_src_issue_s32_dest_set__scb_1_s13 {issue_s32 ##1 ((scb_1_s13 &  1'b1 ) & ! (scb_0_s12 | scb_0_s13 | scb_1_s12 | scb_2_s12 | scb_2_s13 | scb_3_s12 | scb_3_s13 |  1'b0 )) }
cover -name cvr_src_issue_s32_dest_set__scb_1_s12 {issue_s32 ##1 ((scb_1_s12 &  1'b1 ) & ! (scb_0_s12 | scb_0_s13 | scb_1_s13 | scb_2_s12 | scb_2_s13 | scb_3_s12 | scb_3_s13 |  1'b0 )) }
cover -name cvr_src_issue_s32_dest_set__scb_0_s13 {issue_s32 ##1 ((scb_0_s13 &  1'b1 ) & ! (scb_0_s12 | scb_1_s12 | scb_1_s13 | scb_2_s12 | scb_2_s13 | scb_3_s12 | scb_3_s13 |  1'b0 )) }
cover -name cvr_src_issue_s32_dest_set__scb_0_s12 {issue_s32 ##1 ((scb_0_s12 &  1'b1 ) & ! (scb_0_s13 | scb_1_s12 | scb_1_s13 | scb_2_s12 | scb_2_s13 | scb_3_s12 | scb_3_s13 |  1'b0 )) }
cover -name cvr_src_scb_0_s8_dest_set_ {scb_0_s8 ##1 (( 1'b1 ) & ! (scb_0_s12 | scb_0_s13 |  1'b0 )) }
cover -name cvr_src_scb_0_s8_dest_set__scb_0_s13 {scb_0_s8 ##1 ((scb_0_s13 &  1'b1 ) & ! (scb_0_s12 |  1'b0 )) }
cover -name cvr_src_scb_0_s8_dest_set__scb_0_s12 {scb_0_s8 ##1 ((scb_0_s12 &  1'b1 ) & ! (scb_0_s13 |  1'b0 )) }
cover -name cvr_src_scb_0_s12_dest_set_ {scb_0_s12 ##1 (( 1'b1 ) & ! (scb_0_s13 | scb_0_s12 |  1'b0 )) }
cover -name cvr_src_scb_0_s12_dest_set__scb_0_s12 {scb_0_s12 ##1 ((scb_0_s12 &  1'b1 ) & ! (scb_0_s13 |  1'b0 )) }
cover -name cvr_src_scb_0_s12_dest_set__scb_0_s13 {scb_0_s12 ##1 ((scb_0_s13 &  1'b1 ) & ! (scb_0_s12 |  1'b0 )) }
cover -name cvr_src_scb_1_s8_dest_set_ {scb_1_s8 ##1 (( 1'b1 ) & ! (scb_1_s12 | scb_1_s13 |  1'b0 )) }
cover -name cvr_src_scb_1_s8_dest_set__scb_1_s13 {scb_1_s8 ##1 ((scb_1_s13 &  1'b1 ) & ! (scb_1_s12 |  1'b0 )) }
cover -name cvr_src_scb_1_s8_dest_set__scb_1_s12 {scb_1_s8 ##1 ((scb_1_s12 &  1'b1 ) & ! (scb_1_s13 |  1'b0 )) }
cover -name cvr_src_scb_1_s12_dest_set_ {scb_1_s12 ##1 (( 1'b1 ) & ! (scb_1_s13 | scb_1_s12 |  1'b0 )) }
cover -name cvr_src_scb_1_s12_dest_set__scb_1_s12 {scb_1_s12 ##1 ((scb_1_s12 &  1'b1 ) & ! (scb_1_s13 |  1'b0 )) }
cover -name cvr_src_scb_1_s12_dest_set__scb_1_s13 {scb_1_s12 ##1 ((scb_1_s13 &  1'b1 ) & ! (scb_1_s12 |  1'b0 )) }
cover -name cvr_src_scb_2_s8_dest_set_ {scb_2_s8 ##1 (( 1'b1 ) & ! (scb_2_s12 | scb_2_s13 |  1'b0 )) }
cover -name cvr_src_scb_2_s8_dest_set__scb_2_s13 {scb_2_s8 ##1 ((scb_2_s13 &  1'b1 ) & ! (scb_2_s12 |  1'b0 )) }
cover -name cvr_src_scb_2_s8_dest_set__scb_2_s12 {scb_2_s8 ##1 ((scb_2_s12 &  1'b1 ) & ! (scb_2_s13 |  1'b0 )) }
cover -name cvr_src_scb_2_s12_dest_set_ {scb_2_s12 ##1 (( 1'b1 ) & ! (scb_2_s13 | scb_2_s12 |  1'b0 )) }
cover -name cvr_src_scb_2_s12_dest_set__scb_2_s12 {scb_2_s12 ##1 ((scb_2_s12 &  1'b1 ) & ! (scb_2_s13 |  1'b0 )) }
cover -name cvr_src_scb_2_s12_dest_set__scb_2_s13 {scb_2_s12 ##1 ((scb_2_s13 &  1'b1 ) & ! (scb_2_s12 |  1'b0 )) }
cover -name cvr_src_scb_3_s8_dest_set_ {scb_3_s8 ##1 (( 1'b1 ) & ! (scb_3_s12 | scb_3_s13 |  1'b0 )) }
cover -name cvr_src_scb_3_s8_dest_set__scb_3_s13 {scb_3_s8 ##1 ((scb_3_s13 &  1'b1 ) & ! (scb_3_s12 |  1'b0 )) }
cover -name cvr_src_scb_3_s8_dest_set__scb_3_s12 {scb_3_s8 ##1 ((scb_3_s12 &  1'b1 ) & ! (scb_3_s13 |  1'b0 )) }
cover -name cvr_src_scb_3_s12_dest_set_ {scb_3_s12 ##1 (( 1'b1 ) & ! (scb_3_s13 | scb_3_s12 |  1'b0 )) }
cover -name cvr_src_scb_3_s12_dest_set__scb_3_s12 {scb_3_s12 ##1 ((scb_3_s12 &  1'b1 ) & ! (scb_3_s13 |  1'b0 )) }
cover -name cvr_src_scb_3_s12_dest_set__scb_3_s13 {scb_3_s12 ##1 ((scb_3_s13 &  1'b1 ) & ! (scb_3_s12 |  1'b0 )) }

assume -name {i_CSRRW_0} {i0[14:12] == 3'b001}
assume -name {i_CSRRW_2} {i0[6:0] == 7'b1110011}
cover -name cvr_src_decode_s1_dest_set_ {decode_s1 ##1 (( 1'b1 ) & ! (issue_s2 | scb_0_s8 | scb_1_s8 | scb_2_s8 | scb_3_s8 | decode_s1 |  1'b0 )) }
cover -name cvr_src_decode_s1_dest_set__decode_s1 {decode_s1 ##1 ((decode_s1 &  1'b1 ) & ! (issue_s2 | scb_0_s8 | scb_1_s8 | scb_2_s8 | scb_3_s8 |  1'b0 )) }
cover -name cvr_src_decode_s1_dest_set__scb_3_s8 {decode_s1 ##1 ((scb_3_s8 &  1'b1 ) & ! (issue_s2 | scb_0_s8 | scb_1_s8 | scb_2_s8 | decode_s1 |  1'b0 )) }
cover -name cvr_src_decode_s1_dest_set__scb_2_s8 {decode_s1 ##1 ((scb_2_s8 &  1'b1 ) & ! (issue_s2 | scb_0_s8 | scb_1_s8 | scb_3_s8 | decode_s1 |  1'b0 )) }
cover -name cvr_src_decode_s1_dest_set__scb_1_s8 {decode_s1 ##1 ((scb_1_s8 &  1'b1 ) & ! (issue_s2 | scb_0_s8 | scb_2_s8 | scb_3_s8 | decode_s1 |  1'b0 )) }
cover -name cvr_src_decode_s1_dest_set__scb_0_s8 {decode_s1 ##1 ((scb_0_s8 &  1'b1 ) & ! (issue_s2 | scb_1_s8 | scb_2_s8 | scb_3_s8 | decode_s1 |  1'b0 )) }
cover -name cvr_src_decode_s1_dest_set__issue_s2 {decode_s1 ##1 ((issue_s2 &  1'b1 ) & ! (scb_0_s8 | scb_1_s8 | scb_2_s8 | scb_3_s8 | decode_s1 |  1'b0 )) }
cover -name cvr_src_decode_s1_dest_set__issue_s2_scb_3_s8 {decode_s1 ##1 ((issue_s2 & scb_3_s8 &  1'b1 ) & ! (scb_0_s8 | scb_1_s8 | scb_2_s8 | decode_s1 |  1'b0 )) }
cover -name cvr_src_decode_s1_dest_set__issue_s2_scb_2_s8 {decode_s1 ##1 ((issue_s2 & scb_2_s8 &  1'b1 ) & ! (scb_0_s8 | scb_1_s8 | scb_3_s8 | decode_s1 |  1'b0 )) }
cover -name cvr_src_decode_s1_dest_set__issue_s2_scb_1_s8 {decode_s1 ##1 ((issue_s2 & scb_1_s8 &  1'b1 ) & ! (scb_0_s8 | scb_2_s8 | scb_3_s8 | decode_s1 |  1'b0 )) }
cover -name cvr_src_decode_s1_dest_set__issue_s2_scb_0_s8 {decode_s1 ##1 ((issue_s2 & scb_0_s8 &  1'b1 ) & ! (scb_1_s8 | scb_2_s8 | scb_3_s8 | decode_s1 |  1'b0 )) }
cover -name cvr_src_issue_s2_dest_set_ {issue_s2 ##1 (( 1'b1 ) & ! (scb_0_s12 | scb_0_s13 | scb_1_s12 | scb_1_s13 | scb_2_s12 | scb_2_s13 | scb_3_s12 | scb_3_s13 | csr_buffer_s1 |  1'b0 )) }
cover -name cvr_src_issue_s2_dest_set__csr_buffer_s1 {issue_s2 ##1 ((csr_buffer_s1 &  1'b1 ) & ! (scb_0_s12 | scb_0_s13 | scb_1_s12 | scb_1_s13 | scb_2_s12 | scb_2_s13 | scb_3_s12 | scb_3_s13 |  1'b0 )) }
cover -name cvr_src_issue_s2_dest_set__scb_3_s13 {issue_s2 ##1 ((scb_3_s13 &  1'b1 ) & ! (scb_0_s12 | scb_0_s13 | scb_1_s12 | scb_1_s13 | scb_2_s12 | scb_2_s13 | scb_3_s12 | csr_buffer_s1 |  1'b0 )) }
cover -name cvr_src_issue_s2_dest_set__scb_3_s13_csr_buffer_s1 {issue_s2 ##1 ((scb_3_s13 & csr_buffer_s1 &  1'b1 ) & ! (scb_0_s12 | scb_0_s13 | scb_1_s12 | scb_1_s13 | scb_2_s12 | scb_2_s13 | scb_3_s12 |  1'b0 )) }
cover -name cvr_src_issue_s2_dest_set__scb_3_s12 {issue_s2 ##1 ((scb_3_s12 &  1'b1 ) & ! (scb_0_s12 | scb_0_s13 | scb_1_s12 | scb_1_s13 | scb_2_s12 | scb_2_s13 | scb_3_s13 | csr_buffer_s1 |  1'b0 )) }
cover -name cvr_src_issue_s2_dest_set__scb_3_s12_csr_buffer_s1 {issue_s2 ##1 ((scb_3_s12 & csr_buffer_s1 &  1'b1 ) & ! (scb_0_s12 | scb_0_s13 | scb_1_s12 | scb_1_s13 | scb_2_s12 | scb_2_s13 | scb_3_s13 |  1'b0 )) }
cover -name cvr_src_issue_s2_dest_set__scb_2_s13 {issue_s2 ##1 ((scb_2_s13 &  1'b1 ) & ! (scb_0_s12 | scb_0_s13 | scb_1_s12 | scb_1_s13 | scb_2_s12 | scb_3_s12 | scb_3_s13 | csr_buffer_s1 |  1'b0 )) }
cover -name cvr_src_issue_s2_dest_set__scb_2_s13_csr_buffer_s1 {issue_s2 ##1 ((scb_2_s13 & csr_buffer_s1 &  1'b1 ) & ! (scb_0_s12 | scb_0_s13 | scb_1_s12 | scb_1_s13 | scb_2_s12 | scb_3_s12 | scb_3_s13 |  1'b0 )) }
cover -name cvr_src_issue_s2_dest_set__scb_2_s12 {issue_s2 ##1 ((scb_2_s12 &  1'b1 ) & ! (scb_0_s12 | scb_0_s13 | scb_1_s12 | scb_1_s13 | scb_2_s13 | scb_3_s12 | scb_3_s13 | csr_buffer_s1 |  1'b0 )) }
cover -name cvr_src_issue_s2_dest_set__scb_2_s12_csr_buffer_s1 {issue_s2 ##1 ((scb_2_s12 & csr_buffer_s1 &  1'b1 ) & ! (scb_0_s12 | scb_0_s13 | scb_1_s12 | scb_1_s13 | scb_2_s13 | scb_3_s12 | scb_3_s13 |  1'b0 )) }
cover -name cvr_src_issue_s2_dest_set__scb_1_s13 {issue_s2 ##1 ((scb_1_s13 &  1'b1 ) & ! (scb_0_s12 | scb_0_s13 | scb_1_s12 | scb_2_s12 | scb_2_s13 | scb_3_s12 | scb_3_s13 | csr_buffer_s1 |  1'b0 )) }
cover -name cvr_src_issue_s2_dest_set__scb_1_s13_csr_buffer_s1 {issue_s2 ##1 ((scb_1_s13 & csr_buffer_s1 &  1'b1 ) & ! (scb_0_s12 | scb_0_s13 | scb_1_s12 | scb_2_s12 | scb_2_s13 | scb_3_s12 | scb_3_s13 |  1'b0 )) }
cover -name cvr_src_issue_s2_dest_set__scb_1_s12 {issue_s2 ##1 ((scb_1_s12 &  1'b1 ) & ! (scb_0_s12 | scb_0_s13 | scb_1_s13 | scb_2_s12 | scb_2_s13 | scb_3_s12 | scb_3_s13 | csr_buffer_s1 |  1'b0 )) }
cover -name cvr_src_issue_s2_dest_set__scb_1_s12_csr_buffer_s1 {issue_s2 ##1 ((scb_1_s12 & csr_buffer_s1 &  1'b1 ) & ! (scb_0_s12 | scb_0_s13 | scb_1_s13 | scb_2_s12 | scb_2_s13 | scb_3_s12 | scb_3_s13 |  1'b0 )) }
cover -name cvr_src_issue_s2_dest_set__scb_0_s13 {issue_s2 ##1 ((scb_0_s13 &  1'b1 ) & ! (scb_0_s12 | scb_1_s12 | scb_1_s13 | scb_2_s12 | scb_2_s13 | scb_3_s12 | scb_3_s13 | csr_buffer_s1 |  1'b0 )) }
cover -name cvr_src_issue_s2_dest_set__scb_0_s13_csr_buffer_s1 {issue_s2 ##1 ((scb_0_s13 & csr_buffer_s1 &  1'b1 ) & ! (scb_0_s12 | scb_1_s12 | scb_1_s13 | scb_2_s12 | scb_2_s13 | scb_3_s12 | scb_3_s13 |  1'b0 )) }
cover -name cvr_src_issue_s2_dest_set__scb_0_s12 {issue_s2 ##1 ((scb_0_s12 &  1'b1 ) & ! (scb_0_s13 | scb_1_s12 | scb_1_s13 | scb_2_s12 | scb_2_s13 | scb_3_s12 | scb_3_s13 | csr_buffer_s1 |  1'b0 )) }
cover -name cvr_src_issue_s2_dest_set__scb_0_s12_csr_buffer_s1 {issue_s2 ##1 ((scb_0_s12 & csr_buffer_s1 &  1'b1 ) & ! (scb_0_s13 | scb_1_s12 | scb_1_s13 | scb_2_s12 | scb_2_s13 | scb_3_s12 | scb_3_s13 |  1'b0 )) }
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
cover -name cvr_src_csr_buffer_s1_dest_set_ {csr_buffer_s1 ##1 (( 1'b1 ) & ! (csr_buffer_s1 |  1'b0 )) }
cover -name cvr_src_csr_buffer_s1_dest_set__csr_buffer_s1 {csr_buffer_s1 ##1 ((csr_buffer_s1 &  1'b1 ) & ! ( 1'b0 )) }

assume -name {i_LW_0} {i0[14:12] == 3'b010}
assume -name {i_LW_1} {i0[11:7] != 5'd0}
assume -name {i_LW_2} {i0[6:0] == 7'b0000011}
cover -name cvr_src_decode_s1_dest_set_ {decode_s1 ##1 (( 1'b1 ) & ! (issue_s16 | scb_0_s8 | scb_1_s8 | scb_2_s8 | scb_3_s8 | load_unit_op_s2 | mem_req_s1 | decode_s1 |  1'b0 )) }
cover -name cvr_src_decode_s1_dest_set__decode_s1 {decode_s1 ##1 ((decode_s1 &  1'b1 ) & ! (issue_s16 | scb_0_s8 | scb_1_s8 | scb_2_s8 | scb_3_s8 | load_unit_op_s2 | mem_req_s1 |  1'b0 )) }
cover -name cvr_src_decode_s1_dest_set__mem_req_s1 {decode_s1 ##1 ((mem_req_s1 &  1'b1 ) & ! (issue_s16 | scb_0_s8 | scb_1_s8 | scb_2_s8 | scb_3_s8 | load_unit_op_s2 | decode_s1 |  1'b0 )) }
cover -name cvr_src_decode_s1_dest_set__load_unit_op_s2 {decode_s1 ##1 ((load_unit_op_s2 &  1'b1 ) & ! (issue_s16 | scb_0_s8 | scb_1_s8 | scb_2_s8 | scb_3_s8 | mem_req_s1 | decode_s1 |  1'b0 )) }
cover -name cvr_src_decode_s1_dest_set__load_unit_op_s2_mem_req_s1 {decode_s1 ##1 ((load_unit_op_s2 & mem_req_s1 &  1'b1 ) & ! (issue_s16 | scb_0_s8 | scb_1_s8 | scb_2_s8 | scb_3_s8 | decode_s1 |  1'b0 )) }
cover -name cvr_src_decode_s1_dest_set__scb_3_s8 {decode_s1 ##1 ((scb_3_s8 &  1'b1 ) & ! (issue_s16 | scb_0_s8 | scb_1_s8 | scb_2_s8 | load_unit_op_s2 | mem_req_s1 | decode_s1 |  1'b0 )) }
cover -name cvr_src_decode_s1_dest_set__scb_3_s8_mem_req_s1 {decode_s1 ##1 ((scb_3_s8 & mem_req_s1 &  1'b1 ) & ! (issue_s16 | scb_0_s8 | scb_1_s8 | scb_2_s8 | load_unit_op_s2 | decode_s1 |  1'b0 )) }
cover -name cvr_src_decode_s1_dest_set__scb_3_s8_load_unit_op_s2 {decode_s1 ##1 ((scb_3_s8 & load_unit_op_s2 &  1'b1 ) & ! (issue_s16 | scb_0_s8 | scb_1_s8 | scb_2_s8 | mem_req_s1 | decode_s1 |  1'b0 )) }
cover -name cvr_src_decode_s1_dest_set__scb_3_s8_load_unit_op_s2_mem_req_s1 {decode_s1 ##1 ((scb_3_s8 & load_unit_op_s2 & mem_req_s1 &  1'b1 ) & ! (issue_s16 | scb_0_s8 | scb_1_s8 | scb_2_s8 | decode_s1 |  1'b0 )) }
cover -name cvr_src_decode_s1_dest_set__scb_2_s8 {decode_s1 ##1 ((scb_2_s8 &  1'b1 ) & ! (issue_s16 | scb_0_s8 | scb_1_s8 | scb_3_s8 | load_unit_op_s2 | mem_req_s1 | decode_s1 |  1'b0 )) }
cover -name cvr_src_decode_s1_dest_set__scb_2_s8_mem_req_s1 {decode_s1 ##1 ((scb_2_s8 & mem_req_s1 &  1'b1 ) & ! (issue_s16 | scb_0_s8 | scb_1_s8 | scb_3_s8 | load_unit_op_s2 | decode_s1 |  1'b0 )) }
cover -name cvr_src_decode_s1_dest_set__scb_2_s8_load_unit_op_s2 {decode_s1 ##1 ((scb_2_s8 & load_unit_op_s2 &  1'b1 ) & ! (issue_s16 | scb_0_s8 | scb_1_s8 | scb_3_s8 | mem_req_s1 | decode_s1 |  1'b0 )) }
cover -name cvr_src_decode_s1_dest_set__scb_2_s8_load_unit_op_s2_mem_req_s1 {decode_s1 ##1 ((scb_2_s8 & load_unit_op_s2 & mem_req_s1 &  1'b1 ) & ! (issue_s16 | scb_0_s8 | scb_1_s8 | scb_3_s8 | decode_s1 |  1'b0 )) }
cover -name cvr_src_decode_s1_dest_set__scb_1_s8 {decode_s1 ##1 ((scb_1_s8 &  1'b1 ) & ! (issue_s16 | scb_0_s8 | scb_2_s8 | scb_3_s8 | load_unit_op_s2 | mem_req_s1 | decode_s1 |  1'b0 )) }
cover -name cvr_src_decode_s1_dest_set__scb_1_s8_mem_req_s1 {decode_s1 ##1 ((scb_1_s8 & mem_req_s1 &  1'b1 ) & ! (issue_s16 | scb_0_s8 | scb_2_s8 | scb_3_s8 | load_unit_op_s2 | decode_s1 |  1'b0 )) }
cover -name cvr_src_decode_s1_dest_set__scb_1_s8_load_unit_op_s2 {decode_s1 ##1 ((scb_1_s8 & load_unit_op_s2 &  1'b1 ) & ! (issue_s16 | scb_0_s8 | scb_2_s8 | scb_3_s8 | mem_req_s1 | decode_s1 |  1'b0 )) }
cover -name cvr_src_decode_s1_dest_set__scb_1_s8_load_unit_op_s2_mem_req_s1 {decode_s1 ##1 ((scb_1_s8 & load_unit_op_s2 & mem_req_s1 &  1'b1 ) & ! (issue_s16 | scb_0_s8 | scb_2_s8 | scb_3_s8 | decode_s1 |  1'b0 )) }
cover -name cvr_src_decode_s1_dest_set__scb_0_s8 {decode_s1 ##1 ((scb_0_s8 &  1'b1 ) & ! (issue_s16 | scb_1_s8 | scb_2_s8 | scb_3_s8 | load_unit_op_s2 | mem_req_s1 | decode_s1 |  1'b0 )) }
cover -name cvr_src_decode_s1_dest_set__scb_0_s8_mem_req_s1 {decode_s1 ##1 ((scb_0_s8 & mem_req_s1 &  1'b1 ) & ! (issue_s16 | scb_1_s8 | scb_2_s8 | scb_3_s8 | load_unit_op_s2 | decode_s1 |  1'b0 )) }
cover -name cvr_src_decode_s1_dest_set__scb_0_s8_load_unit_op_s2 {decode_s1 ##1 ((scb_0_s8 & load_unit_op_s2 &  1'b1 ) & ! (issue_s16 | scb_1_s8 | scb_2_s8 | scb_3_s8 | mem_req_s1 | decode_s1 |  1'b0 )) }
cover -name cvr_src_decode_s1_dest_set__scb_0_s8_load_unit_op_s2_mem_req_s1 {decode_s1 ##1 ((scb_0_s8 & load_unit_op_s2 & mem_req_s1 &  1'b1 ) & ! (issue_s16 | scb_1_s8 | scb_2_s8 | scb_3_s8 | decode_s1 |  1'b0 )) }
cover -name cvr_src_decode_s1_dest_set__issue_s16 {decode_s1 ##1 ((issue_s16 &  1'b1 ) & ! (scb_0_s8 | scb_1_s8 | scb_2_s8 | scb_3_s8 | load_unit_op_s2 | mem_req_s1 | decode_s1 |  1'b0 )) }
cover -name cvr_src_decode_s1_dest_set__issue_s16_mem_req_s1 {decode_s1 ##1 ((issue_s16 & mem_req_s1 &  1'b1 ) & ! (scb_0_s8 | scb_1_s8 | scb_2_s8 | scb_3_s8 | load_unit_op_s2 | decode_s1 |  1'b0 )) }
cover -name cvr_src_decode_s1_dest_set__issue_s16_load_unit_op_s2 {decode_s1 ##1 ((issue_s16 & load_unit_op_s2 &  1'b1 ) & ! (scb_0_s8 | scb_1_s8 | scb_2_s8 | scb_3_s8 | mem_req_s1 | decode_s1 |  1'b0 )) }
cover -name cvr_src_decode_s1_dest_set__issue_s16_load_unit_op_s2_mem_req_s1 {decode_s1 ##1 ((issue_s16 & load_unit_op_s2 & mem_req_s1 &  1'b1 ) & ! (scb_0_s8 | scb_1_s8 | scb_2_s8 | scb_3_s8 | decode_s1 |  1'b0 )) }
cover -name cvr_src_decode_s1_dest_set__issue_s16_scb_3_s8 {decode_s1 ##1 ((issue_s16 & scb_3_s8 &  1'b1 ) & ! (scb_0_s8 | scb_1_s8 | scb_2_s8 | load_unit_op_s2 | mem_req_s1 | decode_s1 |  1'b0 )) }
cover -name cvr_src_decode_s1_dest_set__issue_s16_scb_3_s8_mem_req_s1 {decode_s1 ##1 ((issue_s16 & scb_3_s8 & mem_req_s1 &  1'b1 ) & ! (scb_0_s8 | scb_1_s8 | scb_2_s8 | load_unit_op_s2 | decode_s1 |  1'b0 )) }
cover -name cvr_src_decode_s1_dest_set__issue_s16_scb_3_s8_load_unit_op_s2 {decode_s1 ##1 ((issue_s16 & scb_3_s8 & load_unit_op_s2 &  1'b1 ) & ! (scb_0_s8 | scb_1_s8 | scb_2_s8 | mem_req_s1 | decode_s1 |  1'b0 )) }
cover -name cvr_src_decode_s1_dest_set__issue_s16_scb_3_s8_load_unit_op_s2_mem_req_s1 {decode_s1 ##1 ((issue_s16 & scb_3_s8 & load_unit_op_s2 & mem_req_s1 &  1'b1 ) & ! (scb_0_s8 | scb_1_s8 | scb_2_s8 | decode_s1 |  1'b0 )) }
cover -name cvr_src_decode_s1_dest_set__issue_s16_scb_2_s8 {decode_s1 ##1 ((issue_s16 & scb_2_s8 &  1'b1 ) & ! (scb_0_s8 | scb_1_s8 | scb_3_s8 | load_unit_op_s2 | mem_req_s1 | decode_s1 |  1'b0 )) }
cover -name cvr_src_decode_s1_dest_set__issue_s16_scb_2_s8_mem_req_s1 {decode_s1 ##1 ((issue_s16 & scb_2_s8 & mem_req_s1 &  1'b1 ) & ! (scb_0_s8 | scb_1_s8 | scb_3_s8 | load_unit_op_s2 | decode_s1 |  1'b0 )) }
cover -name cvr_src_decode_s1_dest_set__issue_s16_scb_2_s8_load_unit_op_s2 {decode_s1 ##1 ((issue_s16 & scb_2_s8 & load_unit_op_s2 &  1'b1 ) & ! (scb_0_s8 | scb_1_s8 | scb_3_s8 | mem_req_s1 | decode_s1 |  1'b0 )) }
cover -name cvr_src_decode_s1_dest_set__issue_s16_scb_2_s8_load_unit_op_s2_mem_req_s1 {decode_s1 ##1 ((issue_s16 & scb_2_s8 & load_unit_op_s2 & mem_req_s1 &  1'b1 ) & ! (scb_0_s8 | scb_1_s8 | scb_3_s8 | decode_s1 |  1'b0 )) }
cover -name cvr_src_decode_s1_dest_set__issue_s16_scb_1_s8 {decode_s1 ##1 ((issue_s16 & scb_1_s8 &  1'b1 ) & ! (scb_0_s8 | scb_2_s8 | scb_3_s8 | load_unit_op_s2 | mem_req_s1 | decode_s1 |  1'b0 )) }
cover -name cvr_src_decode_s1_dest_set__issue_s16_scb_1_s8_mem_req_s1 {decode_s1 ##1 ((issue_s16 & scb_1_s8 & mem_req_s1 &  1'b1 ) & ! (scb_0_s8 | scb_2_s8 | scb_3_s8 | load_unit_op_s2 | decode_s1 |  1'b0 )) }
cover -name cvr_src_decode_s1_dest_set__issue_s16_scb_1_s8_load_unit_op_s2 {decode_s1 ##1 ((issue_s16 & scb_1_s8 & load_unit_op_s2 &  1'b1 ) & ! (scb_0_s8 | scb_2_s8 | scb_3_s8 | mem_req_s1 | decode_s1 |  1'b0 )) }
cover -name cvr_src_decode_s1_dest_set__issue_s16_scb_1_s8_load_unit_op_s2_mem_req_s1 {decode_s1 ##1 ((issue_s16 & scb_1_s8 & load_unit_op_s2 & mem_req_s1 &  1'b1 ) & ! (scb_0_s8 | scb_2_s8 | scb_3_s8 | decode_s1 |  1'b0 )) }
cover -name cvr_src_decode_s1_dest_set__issue_s16_scb_0_s8 {decode_s1 ##1 ((issue_s16 & scb_0_s8 &  1'b1 ) & ! (scb_1_s8 | scb_2_s8 | scb_3_s8 | load_unit_op_s2 | mem_req_s1 | decode_s1 |  1'b0 )) }
cover -name cvr_src_decode_s1_dest_set__issue_s16_scb_0_s8_mem_req_s1 {decode_s1 ##1 ((issue_s16 & scb_0_s8 & mem_req_s1 &  1'b1 ) & ! (scb_1_s8 | scb_2_s8 | scb_3_s8 | load_unit_op_s2 | decode_s1 |  1'b0 )) }
cover -name cvr_src_decode_s1_dest_set__issue_s16_scb_0_s8_load_unit_op_s2 {decode_s1 ##1 ((issue_s16 & scb_0_s8 & load_unit_op_s2 &  1'b1 ) & ! (scb_1_s8 | scb_2_s8 | scb_3_s8 | mem_req_s1 | decode_s1 |  1'b0 )) }
cover -name cvr_src_decode_s1_dest_set__issue_s16_scb_0_s8_load_unit_op_s2_mem_req_s1 {decode_s1 ##1 ((issue_s16 & scb_0_s8 & load_unit_op_s2 & mem_req_s1 &  1'b1 ) & ! (scb_1_s8 | scb_2_s8 | scb_3_s8 | decode_s1 |  1'b0 )) }
cover -name cvr_src_issue_s16_dest_set_ {issue_s16 ##1 (( 1'b1 ) & ! (lsq_enq_0_s1 | lsq_enq_1_s1 | scb_0_s8 | scb_1_s8 | scb_2_s8 | scb_3_s8 | load_unit_s1 | load_unit_op_s3 |  1'b0 )) }
cover -name cvr_src_issue_s16_dest_set__load_unit_op_s3 {issue_s16 ##1 ((load_unit_op_s3 &  1'b1 ) & ! (lsq_enq_0_s1 | lsq_enq_1_s1 | scb_0_s8 | scb_1_s8 | scb_2_s8 | scb_3_s8 | load_unit_s1 |  1'b0 )) }
cover -name cvr_src_issue_s16_dest_set__load_unit_s1 {issue_s16 ##1 ((load_unit_s1 &  1'b1 ) & ! (lsq_enq_0_s1 | lsq_enq_1_s1 | scb_0_s8 | scb_1_s8 | scb_2_s8 | scb_3_s8 | load_unit_op_s3 |  1'b0 )) }
cover -name cvr_src_issue_s16_dest_set__scb_3_s8 {issue_s16 ##1 ((scb_3_s8 &  1'b1 ) & ! (lsq_enq_0_s1 | lsq_enq_1_s1 | scb_0_s8 | scb_1_s8 | scb_2_s8 | load_unit_s1 | load_unit_op_s3 |  1'b0 )) }
cover -name cvr_src_issue_s16_dest_set__scb_3_s8_load_unit_op_s3 {issue_s16 ##1 ((scb_3_s8 & load_unit_op_s3 &  1'b1 ) & ! (lsq_enq_0_s1 | lsq_enq_1_s1 | scb_0_s8 | scb_1_s8 | scb_2_s8 | load_unit_s1 |  1'b0 )) }
cover -name cvr_src_issue_s16_dest_set__scb_3_s8_load_unit_s1 {issue_s16 ##1 ((scb_3_s8 & load_unit_s1 &  1'b1 ) & ! (lsq_enq_0_s1 | lsq_enq_1_s1 | scb_0_s8 | scb_1_s8 | scb_2_s8 | load_unit_op_s3 |  1'b0 )) }
cover -name cvr_src_issue_s16_dest_set__scb_2_s8 {issue_s16 ##1 ((scb_2_s8 &  1'b1 ) & ! (lsq_enq_0_s1 | lsq_enq_1_s1 | scb_0_s8 | scb_1_s8 | scb_3_s8 | load_unit_s1 | load_unit_op_s3 |  1'b0 )) }
cover -name cvr_src_issue_s16_dest_set__scb_2_s8_load_unit_op_s3 {issue_s16 ##1 ((scb_2_s8 & load_unit_op_s3 &  1'b1 ) & ! (lsq_enq_0_s1 | lsq_enq_1_s1 | scb_0_s8 | scb_1_s8 | scb_3_s8 | load_unit_s1 |  1'b0 )) }
cover -name cvr_src_issue_s16_dest_set__scb_2_s8_load_unit_s1 {issue_s16 ##1 ((scb_2_s8 & load_unit_s1 &  1'b1 ) & ! (lsq_enq_0_s1 | lsq_enq_1_s1 | scb_0_s8 | scb_1_s8 | scb_3_s8 | load_unit_op_s3 |  1'b0 )) }
cover -name cvr_src_issue_s16_dest_set__scb_1_s8 {issue_s16 ##1 ((scb_1_s8 &  1'b1 ) & ! (lsq_enq_0_s1 | lsq_enq_1_s1 | scb_0_s8 | scb_2_s8 | scb_3_s8 | load_unit_s1 | load_unit_op_s3 |  1'b0 )) }
cover -name cvr_src_issue_s16_dest_set__scb_1_s8_load_unit_op_s3 {issue_s16 ##1 ((scb_1_s8 & load_unit_op_s3 &  1'b1 ) & ! (lsq_enq_0_s1 | lsq_enq_1_s1 | scb_0_s8 | scb_2_s8 | scb_3_s8 | load_unit_s1 |  1'b0 )) }
cover -name cvr_src_issue_s16_dest_set__scb_1_s8_load_unit_s1 {issue_s16 ##1 ((scb_1_s8 & load_unit_s1 &  1'b1 ) & ! (lsq_enq_0_s1 | lsq_enq_1_s1 | scb_0_s8 | scb_2_s8 | scb_3_s8 | load_unit_op_s3 |  1'b0 )) }
cover -name cvr_src_issue_s16_dest_set__scb_0_s8 {issue_s16 ##1 ((scb_0_s8 &  1'b1 ) & ! (lsq_enq_0_s1 | lsq_enq_1_s1 | scb_1_s8 | scb_2_s8 | scb_3_s8 | load_unit_s1 | load_unit_op_s3 |  1'b0 )) }
cover -name cvr_src_issue_s16_dest_set__scb_0_s8_load_unit_op_s3 {issue_s16 ##1 ((scb_0_s8 & load_unit_op_s3 &  1'b1 ) & ! (lsq_enq_0_s1 | lsq_enq_1_s1 | scb_1_s8 | scb_2_s8 | scb_3_s8 | load_unit_s1 |  1'b0 )) }
cover -name cvr_src_issue_s16_dest_set__scb_0_s8_load_unit_s1 {issue_s16 ##1 ((scb_0_s8 & load_unit_s1 &  1'b1 ) & ! (lsq_enq_0_s1 | lsq_enq_1_s1 | scb_1_s8 | scb_2_s8 | scb_3_s8 | load_unit_op_s3 |  1'b0 )) }
cover -name cvr_src_issue_s16_dest_set__lsq_enq_1_s1 {issue_s16 ##1 ((lsq_enq_1_s1 &  1'b1 ) & ! (lsq_enq_0_s1 | scb_0_s8 | scb_1_s8 | scb_2_s8 | scb_3_s8 | load_unit_s1 | load_unit_op_s3 |  1'b0 )) }
cover -name cvr_src_issue_s16_dest_set__lsq_enq_1_s1_load_unit_op_s3 {issue_s16 ##1 ((lsq_enq_1_s1 & load_unit_op_s3 &  1'b1 ) & ! (lsq_enq_0_s1 | scb_0_s8 | scb_1_s8 | scb_2_s8 | scb_3_s8 | load_unit_s1 |  1'b0 )) }
cover -name cvr_src_issue_s16_dest_set__lsq_enq_1_s1_scb_3_s8 {issue_s16 ##1 ((lsq_enq_1_s1 & scb_3_s8 &  1'b1 ) & ! (lsq_enq_0_s1 | scb_0_s8 | scb_1_s8 | scb_2_s8 | load_unit_s1 | load_unit_op_s3 |  1'b0 )) }
cover -name cvr_src_issue_s16_dest_set__lsq_enq_1_s1_scb_3_s8_load_unit_op_s3 {issue_s16 ##1 ((lsq_enq_1_s1 & scb_3_s8 & load_unit_op_s3 &  1'b1 ) & ! (lsq_enq_0_s1 | scb_0_s8 | scb_1_s8 | scb_2_s8 | load_unit_s1 |  1'b0 )) }
cover -name cvr_src_issue_s16_dest_set__lsq_enq_1_s1_scb_2_s8 {issue_s16 ##1 ((lsq_enq_1_s1 & scb_2_s8 &  1'b1 ) & ! (lsq_enq_0_s1 | scb_0_s8 | scb_1_s8 | scb_3_s8 | load_unit_s1 | load_unit_op_s3 |  1'b0 )) }
cover -name cvr_src_issue_s16_dest_set__lsq_enq_1_s1_scb_2_s8_load_unit_op_s3 {issue_s16 ##1 ((lsq_enq_1_s1 & scb_2_s8 & load_unit_op_s3 &  1'b1 ) & ! (lsq_enq_0_s1 | scb_0_s8 | scb_1_s8 | scb_3_s8 | load_unit_s1 |  1'b0 )) }
cover -name cvr_src_issue_s16_dest_set__lsq_enq_1_s1_scb_1_s8 {issue_s16 ##1 ((lsq_enq_1_s1 & scb_1_s8 &  1'b1 ) & ! (lsq_enq_0_s1 | scb_0_s8 | scb_2_s8 | scb_3_s8 | load_unit_s1 | load_unit_op_s3 |  1'b0 )) }
cover -name cvr_src_issue_s16_dest_set__lsq_enq_1_s1_scb_1_s8_load_unit_op_s3 {issue_s16 ##1 ((lsq_enq_1_s1 & scb_1_s8 & load_unit_op_s3 &  1'b1 ) & ! (lsq_enq_0_s1 | scb_0_s8 | scb_2_s8 | scb_3_s8 | load_unit_s1 |  1'b0 )) }
cover -name cvr_src_issue_s16_dest_set__lsq_enq_1_s1_scb_0_s8 {issue_s16 ##1 ((lsq_enq_1_s1 & scb_0_s8 &  1'b1 ) & ! (lsq_enq_0_s1 | scb_1_s8 | scb_2_s8 | scb_3_s8 | load_unit_s1 | load_unit_op_s3 |  1'b0 )) }
cover -name cvr_src_issue_s16_dest_set__lsq_enq_1_s1_scb_0_s8_load_unit_op_s3 {issue_s16 ##1 ((lsq_enq_1_s1 & scb_0_s8 & load_unit_op_s3 &  1'b1 ) & ! (lsq_enq_0_s1 | scb_1_s8 | scb_2_s8 | scb_3_s8 | load_unit_s1 |  1'b0 )) }
cover -name cvr_src_issue_s16_dest_set__lsq_enq_0_s1 {issue_s16 ##1 ((lsq_enq_0_s1 &  1'b1 ) & ! (lsq_enq_1_s1 | scb_0_s8 | scb_1_s8 | scb_2_s8 | scb_3_s8 | load_unit_s1 | load_unit_op_s3 |  1'b0 )) }
cover -name cvr_src_issue_s16_dest_set__lsq_enq_0_s1_load_unit_op_s3 {issue_s16 ##1 ((lsq_enq_0_s1 & load_unit_op_s3 &  1'b1 ) & ! (lsq_enq_1_s1 | scb_0_s8 | scb_1_s8 | scb_2_s8 | scb_3_s8 | load_unit_s1 |  1'b0 )) }
cover -name cvr_src_issue_s16_dest_set__lsq_enq_0_s1_scb_3_s8 {issue_s16 ##1 ((lsq_enq_0_s1 & scb_3_s8 &  1'b1 ) & ! (lsq_enq_1_s1 | scb_0_s8 | scb_1_s8 | scb_2_s8 | load_unit_s1 | load_unit_op_s3 |  1'b0 )) }
cover -name cvr_src_issue_s16_dest_set__lsq_enq_0_s1_scb_3_s8_load_unit_op_s3 {issue_s16 ##1 ((lsq_enq_0_s1 & scb_3_s8 & load_unit_op_s3 &  1'b1 ) & ! (lsq_enq_1_s1 | scb_0_s8 | scb_1_s8 | scb_2_s8 | load_unit_s1 |  1'b0 )) }
cover -name cvr_src_issue_s16_dest_set__lsq_enq_0_s1_scb_2_s8 {issue_s16 ##1 ((lsq_enq_0_s1 & scb_2_s8 &  1'b1 ) & ! (lsq_enq_1_s1 | scb_0_s8 | scb_1_s8 | scb_3_s8 | load_unit_s1 | load_unit_op_s3 |  1'b0 )) }
cover -name cvr_src_issue_s16_dest_set__lsq_enq_0_s1_scb_2_s8_load_unit_op_s3 {issue_s16 ##1 ((lsq_enq_0_s1 & scb_2_s8 & load_unit_op_s3 &  1'b1 ) & ! (lsq_enq_1_s1 | scb_0_s8 | scb_1_s8 | scb_3_s8 | load_unit_s1 |  1'b0 )) }
cover -name cvr_src_issue_s16_dest_set__lsq_enq_0_s1_scb_1_s8 {issue_s16 ##1 ((lsq_enq_0_s1 & scb_1_s8 &  1'b1 ) & ! (lsq_enq_1_s1 | scb_0_s8 | scb_2_s8 | scb_3_s8 | load_unit_s1 | load_unit_op_s3 |  1'b0 )) }
cover -name cvr_src_issue_s16_dest_set__lsq_enq_0_s1_scb_1_s8_load_unit_op_s3 {issue_s16 ##1 ((lsq_enq_0_s1 & scb_1_s8 & load_unit_op_s3 &  1'b1 ) & ! (lsq_enq_1_s1 | scb_0_s8 | scb_2_s8 | scb_3_s8 | load_unit_s1 |  1'b0 )) }
cover -name cvr_src_issue_s16_dest_set__lsq_enq_0_s1_scb_0_s8 {issue_s16 ##1 ((lsq_enq_0_s1 & scb_0_s8 &  1'b1 ) & ! (lsq_enq_1_s1 | scb_1_s8 | scb_2_s8 | scb_3_s8 | load_unit_s1 | load_unit_op_s3 |  1'b0 )) }
cover -name cvr_src_issue_s16_dest_set__lsq_enq_0_s1_scb_0_s8_load_unit_op_s3 {issue_s16 ##1 ((lsq_enq_0_s1 & scb_0_s8 & load_unit_op_s3 &  1'b1 ) & ! (lsq_enq_1_s1 | scb_1_s8 | scb_2_s8 | scb_3_s8 | load_unit_s1 |  1'b0 )) }
cover -name cvr_src_lsq_enq_0_s1_dest_set_ {lsq_enq_0_s1 ##1 (( 1'b1 ) & ! (load_unit_s1 | load_unit_op_s1 | load_unit_op_s2 | load_unit_op_s3 | mem_req_s1 | lsq_enq_0_s1 |  1'b0 )) }
cover -name cvr_src_lsq_enq_0_s1_dest_set__lsq_enq_0_s1 {lsq_enq_0_s1 ##1 ((lsq_enq_0_s1 &  1'b1 ) & ! (load_unit_s1 | load_unit_op_s1 | load_unit_op_s2 | load_unit_op_s3 | mem_req_s1 |  1'b0 )) }
cover -name cvr_src_lsq_enq_0_s1_dest_set__mem_req_s1 {lsq_enq_0_s1 ##1 ((mem_req_s1 &  1'b1 ) & ! (load_unit_s1 | load_unit_op_s1 | load_unit_op_s2 | load_unit_op_s3 | lsq_enq_0_s1 |  1'b0 )) }
cover -name cvr_src_lsq_enq_0_s1_dest_set__mem_req_s1_lsq_enq_0_s1 {lsq_enq_0_s1 ##1 ((mem_req_s1 & lsq_enq_0_s1 &  1'b1 ) & ! (load_unit_s1 | load_unit_op_s1 | load_unit_op_s2 | load_unit_op_s3 |  1'b0 )) }
cover -name cvr_src_lsq_enq_0_s1_dest_set__load_unit_op_s3 {lsq_enq_0_s1 ##1 ((load_unit_op_s3 &  1'b1 ) & ! (load_unit_s1 | load_unit_op_s1 | load_unit_op_s2 | mem_req_s1 | lsq_enq_0_s1 |  1'b0 )) }
cover -name cvr_src_lsq_enq_0_s1_dest_set__load_unit_op_s3_lsq_enq_0_s1 {lsq_enq_0_s1 ##1 ((load_unit_op_s3 & lsq_enq_0_s1 &  1'b1 ) & ! (load_unit_s1 | load_unit_op_s1 | load_unit_op_s2 | mem_req_s1 |  1'b0 )) }
cover -name cvr_src_lsq_enq_0_s1_dest_set__load_unit_op_s2 {lsq_enq_0_s1 ##1 ((load_unit_op_s2 &  1'b1 ) & ! (load_unit_s1 | load_unit_op_s1 | load_unit_op_s3 | mem_req_s1 | lsq_enq_0_s1 |  1'b0 )) }
cover -name cvr_src_lsq_enq_0_s1_dest_set__load_unit_op_s2_lsq_enq_0_s1 {lsq_enq_0_s1 ##1 ((load_unit_op_s2 & lsq_enq_0_s1 &  1'b1 ) & ! (load_unit_s1 | load_unit_op_s1 | load_unit_op_s3 | mem_req_s1 |  1'b0 )) }
cover -name cvr_src_lsq_enq_0_s1_dest_set__load_unit_op_s2_mem_req_s1 {lsq_enq_0_s1 ##1 ((load_unit_op_s2 & mem_req_s1 &  1'b1 ) & ! (load_unit_s1 | load_unit_op_s1 | load_unit_op_s3 | lsq_enq_0_s1 |  1'b0 )) }
cover -name cvr_src_lsq_enq_0_s1_dest_set__load_unit_op_s2_mem_req_s1_lsq_enq_0_s1 {lsq_enq_0_s1 ##1 ((load_unit_op_s2 & mem_req_s1 & lsq_enq_0_s1 &  1'b1 ) & ! (load_unit_s1 | load_unit_op_s1 | load_unit_op_s3 |  1'b0 )) }
cover -name cvr_src_lsq_enq_0_s1_dest_set__load_unit_op_s1 {lsq_enq_0_s1 ##1 ((load_unit_op_s1 &  1'b1 ) & ! (load_unit_s1 | load_unit_op_s2 | load_unit_op_s3 | mem_req_s1 | lsq_enq_0_s1 |  1'b0 )) }
cover -name cvr_src_lsq_enq_0_s1_dest_set__load_unit_op_s1_lsq_enq_0_s1 {lsq_enq_0_s1 ##1 ((load_unit_op_s1 & lsq_enq_0_s1 &  1'b1 ) & ! (load_unit_s1 | load_unit_op_s2 | load_unit_op_s3 | mem_req_s1 |  1'b0 )) }
cover -name cvr_src_lsq_enq_0_s1_dest_set__load_unit_op_s1_mem_req_s1 {lsq_enq_0_s1 ##1 ((load_unit_op_s1 & mem_req_s1 &  1'b1 ) & ! (load_unit_s1 | load_unit_op_s2 | load_unit_op_s3 | lsq_enq_0_s1 |  1'b0 )) }
cover -name cvr_src_lsq_enq_0_s1_dest_set__load_unit_op_s1_mem_req_s1_lsq_enq_0_s1 {lsq_enq_0_s1 ##1 ((load_unit_op_s1 & mem_req_s1 & lsq_enq_0_s1 &  1'b1 ) & ! (load_unit_s1 | load_unit_op_s2 | load_unit_op_s3 |  1'b0 )) }
cover -name cvr_src_lsq_enq_0_s1_dest_set__load_unit_s1 {lsq_enq_0_s1 ##1 ((load_unit_s1 &  1'b1 ) & ! (load_unit_op_s1 | load_unit_op_s2 | load_unit_op_s3 | mem_req_s1 | lsq_enq_0_s1 |  1'b0 )) }
cover -name cvr_src_lsq_enq_1_s1_dest_set_ {lsq_enq_1_s1 ##1 (( 1'b1 ) & ! (load_unit_s1 | load_unit_op_s1 | load_unit_op_s2 | load_unit_op_s3 | mem_req_s1 | lsq_enq_1_s1 |  1'b0 )) }
cover -name cvr_src_lsq_enq_1_s1_dest_set__lsq_enq_1_s1 {lsq_enq_1_s1 ##1 ((lsq_enq_1_s1 &  1'b1 ) & ! (load_unit_s1 | load_unit_op_s1 | load_unit_op_s2 | load_unit_op_s3 | mem_req_s1 |  1'b0 )) }
cover -name cvr_src_lsq_enq_1_s1_dest_set__mem_req_s1 {lsq_enq_1_s1 ##1 ((mem_req_s1 &  1'b1 ) & ! (load_unit_s1 | load_unit_op_s1 | load_unit_op_s2 | load_unit_op_s3 | lsq_enq_1_s1 |  1'b0 )) }
cover -name cvr_src_lsq_enq_1_s1_dest_set__mem_req_s1_lsq_enq_1_s1 {lsq_enq_1_s1 ##1 ((mem_req_s1 & lsq_enq_1_s1 &  1'b1 ) & ! (load_unit_s1 | load_unit_op_s1 | load_unit_op_s2 | load_unit_op_s3 |  1'b0 )) }
cover -name cvr_src_lsq_enq_1_s1_dest_set__load_unit_op_s3 {lsq_enq_1_s1 ##1 ((load_unit_op_s3 &  1'b1 ) & ! (load_unit_s1 | load_unit_op_s1 | load_unit_op_s2 | mem_req_s1 | lsq_enq_1_s1 |  1'b0 )) }
cover -name cvr_src_lsq_enq_1_s1_dest_set__load_unit_op_s3_lsq_enq_1_s1 {lsq_enq_1_s1 ##1 ((load_unit_op_s3 & lsq_enq_1_s1 &  1'b1 ) & ! (load_unit_s1 | load_unit_op_s1 | load_unit_op_s2 | mem_req_s1 |  1'b0 )) }
cover -name cvr_src_lsq_enq_1_s1_dest_set__load_unit_op_s2 {lsq_enq_1_s1 ##1 ((load_unit_op_s2 &  1'b1 ) & ! (load_unit_s1 | load_unit_op_s1 | load_unit_op_s3 | mem_req_s1 | lsq_enq_1_s1 |  1'b0 )) }
cover -name cvr_src_lsq_enq_1_s1_dest_set__load_unit_op_s2_lsq_enq_1_s1 {lsq_enq_1_s1 ##1 ((load_unit_op_s2 & lsq_enq_1_s1 &  1'b1 ) & ! (load_unit_s1 | load_unit_op_s1 | load_unit_op_s3 | mem_req_s1 |  1'b0 )) }
cover -name cvr_src_lsq_enq_1_s1_dest_set__load_unit_op_s2_mem_req_s1 {lsq_enq_1_s1 ##1 ((load_unit_op_s2 & mem_req_s1 &  1'b1 ) & ! (load_unit_s1 | load_unit_op_s1 | load_unit_op_s3 | lsq_enq_1_s1 |  1'b0 )) }
cover -name cvr_src_lsq_enq_1_s1_dest_set__load_unit_op_s2_mem_req_s1_lsq_enq_1_s1 {lsq_enq_1_s1 ##1 ((load_unit_op_s2 & mem_req_s1 & lsq_enq_1_s1 &  1'b1 ) & ! (load_unit_s1 | load_unit_op_s1 | load_unit_op_s3 |  1'b0 )) }
cover -name cvr_src_lsq_enq_1_s1_dest_set__load_unit_op_s1 {lsq_enq_1_s1 ##1 ((load_unit_op_s1 &  1'b1 ) & ! (load_unit_s1 | load_unit_op_s2 | load_unit_op_s3 | mem_req_s1 | lsq_enq_1_s1 |  1'b0 )) }
cover -name cvr_src_lsq_enq_1_s1_dest_set__load_unit_op_s1_lsq_enq_1_s1 {lsq_enq_1_s1 ##1 ((load_unit_op_s1 & lsq_enq_1_s1 &  1'b1 ) & ! (load_unit_s1 | load_unit_op_s2 | load_unit_op_s3 | mem_req_s1 |  1'b0 )) }
cover -name cvr_src_lsq_enq_1_s1_dest_set__load_unit_op_s1_mem_req_s1 {lsq_enq_1_s1 ##1 ((load_unit_op_s1 & mem_req_s1 &  1'b1 ) & ! (load_unit_s1 | load_unit_op_s2 | load_unit_op_s3 | lsq_enq_1_s1 |  1'b0 )) }
cover -name cvr_src_lsq_enq_1_s1_dest_set__load_unit_op_s1_mem_req_s1_lsq_enq_1_s1 {lsq_enq_1_s1 ##1 ((load_unit_op_s1 & mem_req_s1 & lsq_enq_1_s1 &  1'b1 ) & ! (load_unit_s1 | load_unit_op_s2 | load_unit_op_s3 |  1'b0 )) }
cover -name cvr_src_lsq_enq_1_s1_dest_set__load_unit_s1 {lsq_enq_1_s1 ##1 ((load_unit_s1 &  1'b1 ) & ! (load_unit_op_s1 | load_unit_op_s2 | load_unit_op_s3 | mem_req_s1 | lsq_enq_1_s1 |  1'b0 )) }
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
cover -name cvr_src_load_unit_s1_dest_set_ {load_unit_s1 ##1 (( 1'b1 ) & ! (load_unit_buff_s1 |  1'b0 )) }
cover -name cvr_src_load_unit_s1_dest_set__load_unit_buff_s1 {load_unit_s1 ##1 ((load_unit_buff_s1 &  1'b1 ) & ! ( 1'b0 )) }
cover -name cvr_src_load_unit_op_s1_dest_set_ {load_unit_op_s1 ##1 (( 1'b1 ) & ! (load_unit_s1 |  1'b0 )) }
cover -name cvr_src_load_unit_op_s1_dest_set__load_unit_s1 {load_unit_op_s1 ##1 ((load_unit_s1 &  1'b1 ) & ! ( 1'b0 )) }
cover -name cvr_src_load_unit_op_s2_dest_set_ {load_unit_op_s2 ##1 (( 1'b1 ) & ! (load_unit_s1 | load_unit_op_s3 |  1'b0 )) }
cover -name cvr_src_load_unit_op_s2_dest_set__load_unit_op_s3 {load_unit_op_s2 ##1 ((load_unit_op_s3 &  1'b1 ) & ! (load_unit_s1 |  1'b0 )) }
cover -name cvr_src_load_unit_op_s2_dest_set__load_unit_s1 {load_unit_op_s2 ##1 ((load_unit_s1 &  1'b1 ) & ! (load_unit_op_s3 |  1'b0 )) }
cover -name cvr_src_load_unit_op_s3_dest_set_ {load_unit_op_s3 ##1 (( 1'b1 ) & ! (load_unit_op_s1 | mem_req_s1 | load_unit_op_s3 |  1'b0 )) }
cover -name cvr_src_load_unit_op_s3_dest_set__load_unit_op_s3 {load_unit_op_s3 ##1 ((load_unit_op_s3 &  1'b1 ) & ! (load_unit_op_s1 | mem_req_s1 |  1'b0 )) }
cover -name cvr_src_load_unit_op_s3_dest_set__mem_req_s1 {load_unit_op_s3 ##1 ((mem_req_s1 &  1'b1 ) & ! (load_unit_op_s1 | load_unit_op_s3 |  1'b0 )) }
cover -name cvr_src_load_unit_op_s3_dest_set__load_unit_op_s1 {load_unit_op_s3 ##1 ((load_unit_op_s1 &  1'b1 ) & ! (mem_req_s1 | load_unit_op_s3 |  1'b0 )) }
cover -name cvr_src_load_unit_op_s3_dest_set__load_unit_op_s1_mem_req_s1 {load_unit_op_s3 ##1 ((load_unit_op_s1 & mem_req_s1 &  1'b1 ) & ! (load_unit_op_s3 |  1'b0 )) }

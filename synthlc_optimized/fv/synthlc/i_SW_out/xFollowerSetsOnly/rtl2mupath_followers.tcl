assume -name {i_SW_0} {i0[14:12] == 3'b010}
assume -name {i_SW_1} {i0[6:0] == 7'b0100011}
cover -name cvr_src_decode_s1_dest_set_ {decode_s1 ##1 (( 1'b1 ) & ! (issue_s16 | scb_0_s8 | scb_1_s8 | scb_2_s8 | scb_3_s8 | decode_s1 |  1'b0 )) }
cover -name cvr_src_decode_s1_dest_set__decode_s1 {decode_s1 ##1 ((decode_s1 &  1'b1 ) & ! (issue_s16 | scb_0_s8 | scb_1_s8 | scb_2_s8 | scb_3_s8 |  1'b0 )) }
cover -name cvr_src_decode_s1_dest_set__scb_3_s8 {decode_s1 ##1 ((scb_3_s8 &  1'b1 ) & ! (issue_s16 | scb_0_s8 | scb_1_s8 | scb_2_s8 | decode_s1 |  1'b0 )) }
cover -name cvr_src_decode_s1_dest_set__scb_2_s8 {decode_s1 ##1 ((scb_2_s8 &  1'b1 ) & ! (issue_s16 | scb_0_s8 | scb_1_s8 | scb_3_s8 | decode_s1 |  1'b0 )) }
cover -name cvr_src_decode_s1_dest_set__scb_1_s8 {decode_s1 ##1 ((scb_1_s8 &  1'b1 ) & ! (issue_s16 | scb_0_s8 | scb_2_s8 | scb_3_s8 | decode_s1 |  1'b0 )) }
cover -name cvr_src_decode_s1_dest_set__scb_0_s8 {decode_s1 ##1 ((scb_0_s8 &  1'b1 ) & ! (issue_s16 | scb_1_s8 | scb_2_s8 | scb_3_s8 | decode_s1 |  1'b0 )) }
cover -name cvr_src_decode_s1_dest_set__issue_s16 {decode_s1 ##1 ((issue_s16 &  1'b1 ) & ! (scb_0_s8 | scb_1_s8 | scb_2_s8 | scb_3_s8 | decode_s1 |  1'b0 )) }
cover -name cvr_src_decode_s1_dest_set__issue_s16_scb_3_s8 {decode_s1 ##1 ((issue_s16 & scb_3_s8 &  1'b1 ) & ! (scb_0_s8 | scb_1_s8 | scb_2_s8 | decode_s1 |  1'b0 )) }
cover -name cvr_src_decode_s1_dest_set__issue_s16_scb_2_s8 {decode_s1 ##1 ((issue_s16 & scb_2_s8 &  1'b1 ) & ! (scb_0_s8 | scb_1_s8 | scb_3_s8 | decode_s1 |  1'b0 )) }
cover -name cvr_src_decode_s1_dest_set__issue_s16_scb_1_s8 {decode_s1 ##1 ((issue_s16 & scb_1_s8 &  1'b1 ) & ! (scb_0_s8 | scb_2_s8 | scb_3_s8 | decode_s1 |  1'b0 )) }
cover -name cvr_src_decode_s1_dest_set__issue_s16_scb_0_s8 {decode_s1 ##1 ((issue_s16 & scb_0_s8 &  1'b1 ) & ! (scb_1_s8 | scb_2_s8 | scb_3_s8 | decode_s1 |  1'b0 )) }
cover -name cvr_src_issue_s16_dest_set_ {issue_s16 ##1 (( 1'b1 ) & ! (lsq_enq_0_s1 | lsq_enq_1_s1 | scb_0_s8 | scb_1_s8 | scb_2_s8 | scb_3_s8 | store_unit_s1 | store_unit_s3 |  1'b0 )) }
cover -name cvr_src_issue_s16_dest_set__store_unit_s3 {issue_s16 ##1 ((store_unit_s3 &  1'b1 ) & ! (lsq_enq_0_s1 | lsq_enq_1_s1 | scb_0_s8 | scb_1_s8 | scb_2_s8 | scb_3_s8 | store_unit_s1 |  1'b0 )) }
cover -name cvr_src_issue_s16_dest_set__store_unit_s1 {issue_s16 ##1 ((store_unit_s1 &  1'b1 ) & ! (lsq_enq_0_s1 | lsq_enq_1_s1 | scb_0_s8 | scb_1_s8 | scb_2_s8 | scb_3_s8 | store_unit_s3 |  1'b0 )) }
cover -name cvr_src_issue_s16_dest_set__scb_3_s8 {issue_s16 ##1 ((scb_3_s8 &  1'b1 ) & ! (lsq_enq_0_s1 | lsq_enq_1_s1 | scb_0_s8 | scb_1_s8 | scb_2_s8 | store_unit_s1 | store_unit_s3 |  1'b0 )) }
cover -name cvr_src_issue_s16_dest_set__scb_3_s8_store_unit_s3 {issue_s16 ##1 ((scb_3_s8 & store_unit_s3 &  1'b1 ) & ! (lsq_enq_0_s1 | lsq_enq_1_s1 | scb_0_s8 | scb_1_s8 | scb_2_s8 | store_unit_s1 |  1'b0 )) }
cover -name cvr_src_issue_s16_dest_set__scb_3_s8_store_unit_s1 {issue_s16 ##1 ((scb_3_s8 & store_unit_s1 &  1'b1 ) & ! (lsq_enq_0_s1 | lsq_enq_1_s1 | scb_0_s8 | scb_1_s8 | scb_2_s8 | store_unit_s3 |  1'b0 )) }
cover -name cvr_src_issue_s16_dest_set__scb_2_s8 {issue_s16 ##1 ((scb_2_s8 &  1'b1 ) & ! (lsq_enq_0_s1 | lsq_enq_1_s1 | scb_0_s8 | scb_1_s8 | scb_3_s8 | store_unit_s1 | store_unit_s3 |  1'b0 )) }
cover -name cvr_src_issue_s16_dest_set__scb_2_s8_store_unit_s3 {issue_s16 ##1 ((scb_2_s8 & store_unit_s3 &  1'b1 ) & ! (lsq_enq_0_s1 | lsq_enq_1_s1 | scb_0_s8 | scb_1_s8 | scb_3_s8 | store_unit_s1 |  1'b0 )) }
cover -name cvr_src_issue_s16_dest_set__scb_2_s8_store_unit_s1 {issue_s16 ##1 ((scb_2_s8 & store_unit_s1 &  1'b1 ) & ! (lsq_enq_0_s1 | lsq_enq_1_s1 | scb_0_s8 | scb_1_s8 | scb_3_s8 | store_unit_s3 |  1'b0 )) }
cover -name cvr_src_issue_s16_dest_set__scb_1_s8 {issue_s16 ##1 ((scb_1_s8 &  1'b1 ) & ! (lsq_enq_0_s1 | lsq_enq_1_s1 | scb_0_s8 | scb_2_s8 | scb_3_s8 | store_unit_s1 | store_unit_s3 |  1'b0 )) }
cover -name cvr_src_issue_s16_dest_set__scb_1_s8_store_unit_s3 {issue_s16 ##1 ((scb_1_s8 & store_unit_s3 &  1'b1 ) & ! (lsq_enq_0_s1 | lsq_enq_1_s1 | scb_0_s8 | scb_2_s8 | scb_3_s8 | store_unit_s1 |  1'b0 )) }
cover -name cvr_src_issue_s16_dest_set__scb_1_s8_store_unit_s1 {issue_s16 ##1 ((scb_1_s8 & store_unit_s1 &  1'b1 ) & ! (lsq_enq_0_s1 | lsq_enq_1_s1 | scb_0_s8 | scb_2_s8 | scb_3_s8 | store_unit_s3 |  1'b0 )) }
cover -name cvr_src_issue_s16_dest_set__scb_0_s8 {issue_s16 ##1 ((scb_0_s8 &  1'b1 ) & ! (lsq_enq_0_s1 | lsq_enq_1_s1 | scb_1_s8 | scb_2_s8 | scb_3_s8 | store_unit_s1 | store_unit_s3 |  1'b0 )) }
cover -name cvr_src_issue_s16_dest_set__scb_0_s8_store_unit_s3 {issue_s16 ##1 ((scb_0_s8 & store_unit_s3 &  1'b1 ) & ! (lsq_enq_0_s1 | lsq_enq_1_s1 | scb_1_s8 | scb_2_s8 | scb_3_s8 | store_unit_s1 |  1'b0 )) }
cover -name cvr_src_issue_s16_dest_set__scb_0_s8_store_unit_s1 {issue_s16 ##1 ((scb_0_s8 & store_unit_s1 &  1'b1 ) & ! (lsq_enq_0_s1 | lsq_enq_1_s1 | scb_1_s8 | scb_2_s8 | scb_3_s8 | store_unit_s3 |  1'b0 )) }
cover -name cvr_src_issue_s16_dest_set__lsq_enq_1_s1 {issue_s16 ##1 ((lsq_enq_1_s1 &  1'b1 ) & ! (lsq_enq_0_s1 | scb_0_s8 | scb_1_s8 | scb_2_s8 | scb_3_s8 | store_unit_s1 | store_unit_s3 |  1'b0 )) }
cover -name cvr_src_issue_s16_dest_set__lsq_enq_1_s1_store_unit_s3 {issue_s16 ##1 ((lsq_enq_1_s1 & store_unit_s3 &  1'b1 ) & ! (lsq_enq_0_s1 | scb_0_s8 | scb_1_s8 | scb_2_s8 | scb_3_s8 | store_unit_s1 |  1'b0 )) }
cover -name cvr_src_issue_s16_dest_set__lsq_enq_1_s1_scb_3_s8 {issue_s16 ##1 ((lsq_enq_1_s1 & scb_3_s8 &  1'b1 ) & ! (lsq_enq_0_s1 | scb_0_s8 | scb_1_s8 | scb_2_s8 | store_unit_s1 | store_unit_s3 |  1'b0 )) }
cover -name cvr_src_issue_s16_dest_set__lsq_enq_1_s1_scb_3_s8_store_unit_s3 {issue_s16 ##1 ((lsq_enq_1_s1 & scb_3_s8 & store_unit_s3 &  1'b1 ) & ! (lsq_enq_0_s1 | scb_0_s8 | scb_1_s8 | scb_2_s8 | store_unit_s1 |  1'b0 )) }
cover -name cvr_src_issue_s16_dest_set__lsq_enq_1_s1_scb_2_s8 {issue_s16 ##1 ((lsq_enq_1_s1 & scb_2_s8 &  1'b1 ) & ! (lsq_enq_0_s1 | scb_0_s8 | scb_1_s8 | scb_3_s8 | store_unit_s1 | store_unit_s3 |  1'b0 )) }
cover -name cvr_src_issue_s16_dest_set__lsq_enq_1_s1_scb_2_s8_store_unit_s3 {issue_s16 ##1 ((lsq_enq_1_s1 & scb_2_s8 & store_unit_s3 &  1'b1 ) & ! (lsq_enq_0_s1 | scb_0_s8 | scb_1_s8 | scb_3_s8 | store_unit_s1 |  1'b0 )) }
cover -name cvr_src_issue_s16_dest_set__lsq_enq_1_s1_scb_1_s8 {issue_s16 ##1 ((lsq_enq_1_s1 & scb_1_s8 &  1'b1 ) & ! (lsq_enq_0_s1 | scb_0_s8 | scb_2_s8 | scb_3_s8 | store_unit_s1 | store_unit_s3 |  1'b0 )) }
cover -name cvr_src_issue_s16_dest_set__lsq_enq_1_s1_scb_1_s8_store_unit_s3 {issue_s16 ##1 ((lsq_enq_1_s1 & scb_1_s8 & store_unit_s3 &  1'b1 ) & ! (lsq_enq_0_s1 | scb_0_s8 | scb_2_s8 | scb_3_s8 | store_unit_s1 |  1'b0 )) }
cover -name cvr_src_issue_s16_dest_set__lsq_enq_1_s1_scb_0_s8 {issue_s16 ##1 ((lsq_enq_1_s1 & scb_0_s8 &  1'b1 ) & ! (lsq_enq_0_s1 | scb_1_s8 | scb_2_s8 | scb_3_s8 | store_unit_s1 | store_unit_s3 |  1'b0 )) }
cover -name cvr_src_issue_s16_dest_set__lsq_enq_1_s1_scb_0_s8_store_unit_s3 {issue_s16 ##1 ((lsq_enq_1_s1 & scb_0_s8 & store_unit_s3 &  1'b1 ) & ! (lsq_enq_0_s1 | scb_1_s8 | scb_2_s8 | scb_3_s8 | store_unit_s1 |  1'b0 )) }
cover -name cvr_src_issue_s16_dest_set__lsq_enq_0_s1 {issue_s16 ##1 ((lsq_enq_0_s1 &  1'b1 ) & ! (lsq_enq_1_s1 | scb_0_s8 | scb_1_s8 | scb_2_s8 | scb_3_s8 | store_unit_s1 | store_unit_s3 |  1'b0 )) }
cover -name cvr_src_issue_s16_dest_set__lsq_enq_0_s1_store_unit_s3 {issue_s16 ##1 ((lsq_enq_0_s1 & store_unit_s3 &  1'b1 ) & ! (lsq_enq_1_s1 | scb_0_s8 | scb_1_s8 | scb_2_s8 | scb_3_s8 | store_unit_s1 |  1'b0 )) }
cover -name cvr_src_issue_s16_dest_set__lsq_enq_0_s1_scb_3_s8 {issue_s16 ##1 ((lsq_enq_0_s1 & scb_3_s8 &  1'b1 ) & ! (lsq_enq_1_s1 | scb_0_s8 | scb_1_s8 | scb_2_s8 | store_unit_s1 | store_unit_s3 |  1'b0 )) }
cover -name cvr_src_issue_s16_dest_set__lsq_enq_0_s1_scb_3_s8_store_unit_s3 {issue_s16 ##1 ((lsq_enq_0_s1 & scb_3_s8 & store_unit_s3 &  1'b1 ) & ! (lsq_enq_1_s1 | scb_0_s8 | scb_1_s8 | scb_2_s8 | store_unit_s1 |  1'b0 )) }
cover -name cvr_src_issue_s16_dest_set__lsq_enq_0_s1_scb_2_s8 {issue_s16 ##1 ((lsq_enq_0_s1 & scb_2_s8 &  1'b1 ) & ! (lsq_enq_1_s1 | scb_0_s8 | scb_1_s8 | scb_3_s8 | store_unit_s1 | store_unit_s3 |  1'b0 )) }
cover -name cvr_src_issue_s16_dest_set__lsq_enq_0_s1_scb_2_s8_store_unit_s3 {issue_s16 ##1 ((lsq_enq_0_s1 & scb_2_s8 & store_unit_s3 &  1'b1 ) & ! (lsq_enq_1_s1 | scb_0_s8 | scb_1_s8 | scb_3_s8 | store_unit_s1 |  1'b0 )) }
cover -name cvr_src_issue_s16_dest_set__lsq_enq_0_s1_scb_1_s8 {issue_s16 ##1 ((lsq_enq_0_s1 & scb_1_s8 &  1'b1 ) & ! (lsq_enq_1_s1 | scb_0_s8 | scb_2_s8 | scb_3_s8 | store_unit_s1 | store_unit_s3 |  1'b0 )) }
cover -name cvr_src_issue_s16_dest_set__lsq_enq_0_s1_scb_1_s8_store_unit_s3 {issue_s16 ##1 ((lsq_enq_0_s1 & scb_1_s8 & store_unit_s3 &  1'b1 ) & ! (lsq_enq_1_s1 | scb_0_s8 | scb_2_s8 | scb_3_s8 | store_unit_s1 |  1'b0 )) }
cover -name cvr_src_issue_s16_dest_set__lsq_enq_0_s1_scb_0_s8 {issue_s16 ##1 ((lsq_enq_0_s1 & scb_0_s8 &  1'b1 ) & ! (lsq_enq_1_s1 | scb_1_s8 | scb_2_s8 | scb_3_s8 | store_unit_s1 | store_unit_s3 |  1'b0 )) }
cover -name cvr_src_issue_s16_dest_set__lsq_enq_0_s1_scb_0_s8_store_unit_s3 {issue_s16 ##1 ((lsq_enq_0_s1 & scb_0_s8 & store_unit_s3 &  1'b1 ) & ! (lsq_enq_1_s1 | scb_1_s8 | scb_2_s8 | scb_3_s8 | store_unit_s1 |  1'b0 )) }
cover -name cvr_src_lsq_enq_0_s1_dest_set_ {lsq_enq_0_s1 ##1 (( 1'b1 ) & ! (store_unit_s1 | lsq_enq_0_s1 |  1'b0 )) }
cover -name cvr_src_lsq_enq_0_s1_dest_set__lsq_enq_0_s1 {lsq_enq_0_s1 ##1 ((lsq_enq_0_s1 &  1'b1 ) & ! (store_unit_s1 |  1'b0 )) }
cover -name cvr_src_lsq_enq_0_s1_dest_set__store_unit_s1 {lsq_enq_0_s1 ##1 ((store_unit_s1 &  1'b1 ) & ! (lsq_enq_0_s1 |  1'b0 )) }
cover -name cvr_src_lsq_enq_1_s1_dest_set_ {lsq_enq_1_s1 ##1 (( 1'b1 ) & ! (store_unit_s1 | lsq_enq_1_s1 |  1'b0 )) }
cover -name cvr_src_lsq_enq_1_s1_dest_set__lsq_enq_1_s1 {lsq_enq_1_s1 ##1 ((lsq_enq_1_s1 &  1'b1 ) & ! (store_unit_s1 |  1'b0 )) }
cover -name cvr_src_lsq_enq_1_s1_dest_set__store_unit_s1 {lsq_enq_1_s1 ##1 ((store_unit_s1 &  1'b1 ) & ! (lsq_enq_1_s1 |  1'b0 )) }
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
cover -name cvr_src_stb_com_0_s1_dest_set_ {stb_com_0_s1 ##1 (( 1'b1 ) & ! (mem_req_s1 | stb_com_0_s1 |  1'b0 )) }
cover -name cvr_src_stb_com_0_s1_dest_set__stb_com_0_s1 {stb_com_0_s1 ##1 ((stb_com_0_s1 &  1'b1 ) & ! (mem_req_s1 |  1'b0 )) }
cover -name cvr_src_stb_com_0_s1_dest_set__mem_req_s1 {stb_com_0_s1 ##1 ((mem_req_s1 &  1'b1 ) & ! (stb_com_0_s1 |  1'b0 )) }
cover -name cvr_src_stb_com_0_s1_dest_set__mem_req_s1_stb_com_0_s1 {stb_com_0_s1 ##1 ((mem_req_s1 & stb_com_0_s1 &  1'b1 ) & ! ( 1'b0 )) }
cover -name cvr_src_stb_com_1_s1_dest_set_ {stb_com_1_s1 ##1 (( 1'b1 ) & ! (mem_req_s1 | stb_com_1_s1 |  1'b0 )) }
cover -name cvr_src_stb_com_1_s1_dest_set__stb_com_1_s1 {stb_com_1_s1 ##1 ((stb_com_1_s1 &  1'b1 ) & ! (mem_req_s1 |  1'b0 )) }
cover -name cvr_src_stb_com_1_s1_dest_set__mem_req_s1 {stb_com_1_s1 ##1 ((mem_req_s1 &  1'b1 ) & ! (stb_com_1_s1 |  1'b0 )) }
cover -name cvr_src_stb_com_1_s1_dest_set__mem_req_s1_stb_com_1_s1 {stb_com_1_s1 ##1 ((mem_req_s1 & stb_com_1_s1 &  1'b1 ) & ! ( 1'b0 )) }
cover -name cvr_src_stb_spec_0_s1_dest_set_ {stb_spec_0_s1 ##1 (( 1'b1 ) & ! (stb_com_0_s1 | mem_req_s1 | stb_spec_0_s1 |  1'b0 )) }
cover -name cvr_src_stb_spec_0_s1_dest_set__stb_spec_0_s1 {stb_spec_0_s1 ##1 ((stb_spec_0_s1 &  1'b1 ) & ! (stb_com_0_s1 | mem_req_s1 |  1'b0 )) }
cover -name cvr_src_stb_spec_0_s1_dest_set__mem_req_s1 {stb_spec_0_s1 ##1 ((mem_req_s1 &  1'b1 ) & ! (stb_com_0_s1 | stb_spec_0_s1 |  1'b0 )) }
cover -name cvr_src_stb_spec_0_s1_dest_set__stb_com_0_s1 {stb_spec_0_s1 ##1 ((stb_com_0_s1 &  1'b1 ) & ! (mem_req_s1 | stb_spec_0_s1 |  1'b0 )) }
cover -name cvr_src_stb_spec_0_s1_dest_set__stb_com_0_s1_mem_req_s1 {stb_spec_0_s1 ##1 ((stb_com_0_s1 & mem_req_s1 &  1'b1 ) & ! (stb_spec_0_s1 |  1'b0 )) }
cover -name cvr_src_stb_spec_1_s1_dest_set_ {stb_spec_1_s1 ##1 (( 1'b1 ) & ! (stb_com_1_s1 | mem_req_s1 | stb_spec_1_s1 |  1'b0 )) }
cover -name cvr_src_stb_spec_1_s1_dest_set__stb_spec_1_s1 {stb_spec_1_s1 ##1 ((stb_spec_1_s1 &  1'b1 ) & ! (stb_com_1_s1 | mem_req_s1 |  1'b0 )) }
cover -name cvr_src_stb_spec_1_s1_dest_set__mem_req_s1 {stb_spec_1_s1 ##1 ((mem_req_s1 &  1'b1 ) & ! (stb_com_1_s1 | stb_spec_1_s1 |  1'b0 )) }
cover -name cvr_src_stb_spec_1_s1_dest_set__stb_com_1_s1 {stb_spec_1_s1 ##1 ((stb_com_1_s1 &  1'b1 ) & ! (mem_req_s1 | stb_spec_1_s1 |  1'b0 )) }
cover -name cvr_src_stb_spec_1_s1_dest_set__stb_com_1_s1_mem_req_s1 {stb_spec_1_s1 ##1 ((stb_com_1_s1 & mem_req_s1 &  1'b1 ) & ! (stb_spec_1_s1 |  1'b0 )) }
cover -name cvr_src_store_unit_s1_dest_set_ {store_unit_s1 ##1 (( 1'b1 ) & ! (stb_spec_0_s1 | stb_spec_1_s1 |  1'b0 )) }
cover -name cvr_src_store_unit_s1_dest_set__stb_spec_1_s1 {store_unit_s1 ##1 ((stb_spec_1_s1 &  1'b1 ) & ! (stb_spec_0_s1 |  1'b0 )) }
cover -name cvr_src_store_unit_s1_dest_set__stb_spec_0_s1 {store_unit_s1 ##1 ((stb_spec_0_s1 &  1'b1 ) & ! (stb_spec_1_s1 |  1'b0 )) }


`define T_FROM_I
`define DYNAMIC
`define RS1
i_ADDW_0: assume property (i0[31:25] == 7'b0000000);
i_ADDW_1: assume property (i0[14:12] == 3'b000);
i_ADDW_2: assume property (i0[11:7] != 5'd0);
i_ADDW_3: assume property (i0[6:0] == 7'b0111011);


group_3_i1: assume property (
((i1[14:12] == 3'b010) && (i1[11:7] != 5'd0) && (i1[6:0] == 7'b0000011) && 1'b1) ||
1'b0);
// LW



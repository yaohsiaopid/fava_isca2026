
`define T_FROM_I
`define DYNAMIC
`define RS1
i_DIVUW_0: assume property (i0[31:25] == 7'b0000001);
i_DIVUW_1: assume property (i0[14:12] == 3'b101);
i_DIVUW_2: assume property (i0[11:7] != 5'd0);
i_DIVUW_3: assume property (i0[6:0] == 7'b0111011);


group_3_i1: assume property (
((i1[14:12] == 3'b010) && (i1[11:7] != 5'd0) && (i1[6:0] == 7'b0000011) && 1'b1) ||
1'b0);
// LW



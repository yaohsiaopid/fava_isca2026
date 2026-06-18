
`define T_FROM_I
`define DYNAMIC
`define YNG
`define RS1
i_BEQ_0: assume property (i0[14:12] == 3'b000);
i_BEQ_1: assume property (i0[6:0] == 7'b1100011);


group_3_i1: assume property (
((i1[14:12] == 3'b010) && (i1[11:7] != 5'd0) && (i1[6:0] == 7'b0000011) && 1'b1) ||
1'b0);
// LW




`define T_FROM_I
`define DYNAMIC
`define RS1
i_BLT_0: assume property (i0[14:12] == 3'b100);
i_BLT_1: assume property (i0[6:0] == 7'b1100011);


group_5_i1: assume property (
((i1[14:12] == 3'b000) && (i1[6:0] == 7'b1100011) && 1'b1) ||
1'b0);
// BEQ




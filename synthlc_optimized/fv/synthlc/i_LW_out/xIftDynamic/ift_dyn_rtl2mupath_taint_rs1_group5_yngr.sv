
`define T_FROM_I
`define DYNAMIC
`define YNG
`define RS1
i_LW_0: assume property (i0[14:12] == 3'b010);
i_LW_1: assume property (i0[11:7] != 5'd0);
i_LW_2: assume property (i0[6:0] == 7'b0000011);


group_5_i1: assume property (
((i1[14:12] == 3'b000) && (i1[6:0] == 7'b1100011) && 1'b1) ||
1'b0);
// BEQ




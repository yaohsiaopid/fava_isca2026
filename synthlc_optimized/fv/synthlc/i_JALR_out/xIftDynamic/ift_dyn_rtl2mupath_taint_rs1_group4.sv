
`define T_FROM_I
`define DYNAMIC
`define RS1
i_JALR_0: assume property (i0[14:12] == 3'b000);
i_JALR_1: assume property (i0[6:0] == 7'b1100111);


group_4_i1: assume property (
((i1[14:12] == 3'b010) && (i1[6:0] == 7'b0100011) && 1'b1) ||
1'b0);
// SW



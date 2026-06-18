
`define T_FROM_I
`define DYNAMIC
`define BOTHRS
i_ANDI_0: assume property (i0[14:12] == 3'b111);
i_ANDI_1: assume property (i0[11:7] != 5'd0);
i_ANDI_2: assume property (i0[6:0] == 7'b0010011);


group_4_i1: assume property (
((i1[14:12] == 3'b010) && (i1[6:0] == 7'b0100011) && 1'b1) ||
1'b0);
// SW



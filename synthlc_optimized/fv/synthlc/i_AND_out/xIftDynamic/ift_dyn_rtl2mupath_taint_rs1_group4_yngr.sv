
`define T_FROM_I
`define DYNAMIC
`define YNG
`define RS1
i_AND_0: assume property (i0[31:25] == 7'b0000000);
i_AND_1: assume property (i0[14:12] == 3'b111);
i_AND_2: assume property (i0[11:7] != 5'd0);
i_AND_3: assume property (i0[6:0] == 7'b0110011);


group_4_i1: assume property (
((i1[14:12] == 3'b010) && (i1[6:0] == 7'b0100011) && 1'b1) ||
1'b0);
// SW



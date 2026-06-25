
`define T_FROM_I
`define DYNAMIC
`define RS1
i_DIVU_0: assume property (i0[31:25] == 7'b0000001);
i_DIVU_1: assume property (i0[14:12] == 3'b101);
i_DIVU_2: assume property (i0[11:7] != 5'd0);
i_DIVU_3: assume property (i0[6:0] == 7'b0110011);


group_4_i1: assume property (
((i1[14:12] == 3'b010) && (i1[6:0] == 7'b0100011) && 1'b1) ||
1'b0);
// SW



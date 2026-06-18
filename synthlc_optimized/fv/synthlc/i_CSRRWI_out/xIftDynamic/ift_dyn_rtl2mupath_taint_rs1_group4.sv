
`define T_FROM_I
`define DYNAMIC
`define RS1
`define SYSINSN
i_CSRRWI_0: assume property (i0[14:12] == 3'b101);
i_CSRRWI_2: assume property (i0[6:0] == 7'b1110011);


group_4_i1: assume property (
((i1[14:12] == 3'b010) && (i1[6:0] == 7'b0100011) && 1'b1) ||
1'b0);
// SW



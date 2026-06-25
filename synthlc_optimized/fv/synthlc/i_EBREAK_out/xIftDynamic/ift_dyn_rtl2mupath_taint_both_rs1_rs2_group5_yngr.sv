
`define T_FROM_I
`define DYNAMIC
`define YNG
`define BOTHRS
`define SYSINSN
i_EBREAK_0: assume property (i0[31:20] == 12'b000000000001);
i_EBREAK_1: assume property (i0[19:15] == 5'b00000);
i_EBREAK_2: assume property (i0[14:12] == 3'b000);
i_EBREAK_3: assume property (i0[11:7] == 5'b00000);
i_EBREAK_4: assume property (i0[6:0] == 7'b1110011);


group_5_i1: assume property (
((i1[14:12] == 3'b000) && (i1[6:0] == 7'b1100011) && 1'b1) ||
1'b0);
// BEQ




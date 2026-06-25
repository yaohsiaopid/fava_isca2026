
`define T_FROM_I
`define DYNAMIC
`define YNG
`define RS1
`define SYSINSN
i_CSRRW_0: assume property (i0[14:12] == 3'b001);
i_CSRRW_2: assume property (i0[6:0] == 7'b1110011);


group_1_i1: assume property (
((i1[31:25] == 7'b0000001) && (i1[14:12] == 3'b100) && (i1[11:7] != 5'd0) && (i1[6:0] ==
7'b0110011) && 1'b1) || 
1'b0);
// DIV



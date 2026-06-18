
`define T_FROM_I
`define DYNAMIC
`define YNG
`define RS1
i_AUIPC_0: assume property (i0[11:7] != 5'd0);
i_AUIPC_1: assume property (i0[6:0] == 7'b0010111);


group_1_i1: assume property (
((i1[31:25] == 7'b0000001) && (i1[14:12] == 3'b100) && (i1[11:7] != 5'd0) && (i1[6:0] ==
7'b0110011) && 1'b1) || 
1'b0);
// DIV



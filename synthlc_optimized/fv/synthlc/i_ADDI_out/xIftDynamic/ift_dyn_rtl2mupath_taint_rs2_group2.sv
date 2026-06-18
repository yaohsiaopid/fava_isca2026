
`define T_FROM_I
`define DYNAMIC
`define RS2
i_ADDI_0: assume property (i0[14:12] == 3'b000);
i_ADDI_1: assume property (i0[11:7] != 5'd0);
i_ADDI_2: assume property (i0[6:0] == 7'b0010011);


group_2_i1: assume property (
((i1[31:25] == 7'b0000000) && (i1[14:12] == 3'b000) && (i1[11:7] != 5'd0) && (i1[6:0] == 7'b0110011) && 1'b1) || 
1'b0);
// ADD



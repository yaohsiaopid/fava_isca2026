
`define T_FROM_I
`define DYNAMIC
`define RS1
`define SYSINSN
i_ECALL_0: assume property (i0[31:20] == 12'b000000000000);
i_ECALL_1: assume property (i0[19:15] == 5'b00000);
i_ECALL_2: assume property (i0[14:12] == 3'b000);
i_ECALL_3: assume property (i0[11:7] == 5'b00000);
i_ECALL_4: assume property (i0[6:0] == 7'b1110011);


group_4_i1: assume property (
((i1[14:12] == 3'b010) && (i1[6:0] == 7'b0100011) && 1'b1) ||
1'b0);
// SW



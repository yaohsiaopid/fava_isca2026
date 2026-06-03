cp same_addr_dep.sv.template same_addr_dep.sv
A=$(realpath ../)
sed -i "s|INC_PATH|\`include \"$A/i0_pl.sv\"\n\`include \"$A/i1_pl.sv\"\n|g" same_addr_dep.sv

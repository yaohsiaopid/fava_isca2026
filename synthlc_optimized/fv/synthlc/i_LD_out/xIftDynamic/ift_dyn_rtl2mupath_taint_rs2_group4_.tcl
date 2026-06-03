
set assert_report_incompletes 1
set FPV 1

#proc exit_if_error {} {
#    if [get_message -number error] {
#        exit -force
#    }
#    after 10000 exit_if_error
#}
#exit_if_error

# 
exec /cafe/u/samanthaarcher/synthlc_tutorial/fava_isca2026/synthlc_optimized/fv/synthlc/i_LD_out/xIftDynamic/ift_dyn_rtl2mupath_taint_rs2_group4_update_file_.sh

analyze -sv09 -f /cafe/u/samanthaarcher/synthlc_tutorial/fava_isca2026/synthlc_optimized/fv/synthlc/i_LD_out/xIftDynamic/ift_dyn_rtl2mupath_taint_rs2_group4_hdls.f
elaborate -bbox_m {\frontend} -top ariane

# Clock specification
clock clk_i

reset !rst_ni
set_proofgrid_per_engine_max_jobs 32
set_proofgrid_max_jobs 32

task -create mytask -copy_assumes   -regexp
task -set mytask

set_prove_time_limit 2h
#set_prove_per_property_time_limit 12m

source /cafe/u/samanthaarcher/synthlc_tutorial/fava_isca2026/synthlc_optimized/fv/synthlc/i_LD_out/xIftDynamic/ift_dyn_rtl2mupath_taint_rs2_group4.tcl

set_engine_mode {K C Tri I N AD AM Hp B}
prove -task mytask
puts "END"
report -task mytask -csv -results -file "/cafe/u/samanthaarcher/synthlc_tutorial/fava_isca2026/synthlc_optimized/fv/synthlc/i_LD_out/xIftDynamic/ift_dyn_rtl2mupath_taint_rs2_group4.csv" -force
save "/cafe/u/samanthaarcher/synthlc_tutorial/fava_isca2026/synthlc_optimized/fv/synthlc/i_LD_out/xIftDynamic/ift_dyn_rtl2mupath_taint_rs2_group4.db" -clean -include {app_data session_data elaborated_design} -force
exit

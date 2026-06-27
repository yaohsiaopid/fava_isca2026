
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
exec UPDATEFILE

analyze -sv09 -f jg_hdl.f
elaborate -bbox_m {\frontend} -top ariane

# Clock specification
clock clk_i

reset !rst_ni
set_proofgrid_per_engine_max_jobs 32
set_proofgrid_max_jobs 32

#TASKCREATION
#task -set mytask

set_prove_time_limit 2h
#set_prove_per_property_time_limit 12m

#CUSTOMTCL
task -set mytask

set_engine_mode {K C Tri I N AD AM Hp B}
#PROVE_ACTION
puts "END"
report -task mytask -csv -results -file "CSVNAME.csv" -force
#save "CSVNAME.db" -clean -include {app_data session_data elaborated_design} -force
exit

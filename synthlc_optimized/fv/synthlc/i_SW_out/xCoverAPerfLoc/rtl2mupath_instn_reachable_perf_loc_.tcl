# Run JG with a TCl file: jg jg_test.tcl
set assert_report_incompletes 1
set RTL_DIR /cafe/u/samanthaarcher/synthlc_tutorial/SynthLC_optimized/cva6
set SRCDIR /cafe/u/samanthaarcher/synthlc_tutorial/SynthLC_optimized/cva6/core

############
set FPV 1
set SPV 0
set REACH 0
set CUSTOMTCL 1
############
exec /cafe/u/samanthaarcher/synthlc_tutorial/fava_isca2026/synthlc_optimized/fv/synthlc/i_SW_out/xCoverAPerfLoc/rtl2mupath_instn_reachable_perf_loc_update_file_.sh
# Analyze RTL files
analyze -sv09 -f /cafe/u/samanthaarcher/synthlc_tutorial/fava_isca2026/synthlc_optimized/fv/synthlc/i_SW_out/xCoverAPerfLoc/rtl2mupath_instn_reachable_perf_loc_hdls.f -y $SRCDIR +incdir+$SRCDIR
if {$SPV == 1} {
    puts "initializing SPV"
    check_spv -init
}
if {$REACH == 1} {
    puts "test bboxing mfpt" 
    #elaborate -bbox_m  {miss_prediction_fix_table} -bbox_m {reorderbuf}
    elaborate 
    source reach_collect.tcl
}
if {$FPV == 1} {
    puts "fpv" 
    # Elaborates
    #elaborate -bbox_m {wt_cache_subsystem} -bbox_m {frontend}
    #puts "multiplier no-bbox"
    elaborate -bbox_m {frontend}
    #elaborate -bbox_m {frontend}
    #stopat -env {issue_stage_i.i_scoreboard.mem_n[0].sbe.is_compressed}  
    #elaborate


    # Initialization
    # Clock specification
    clock clk_i
    # -both_edges: ridecore 
    reset !rst_ni
    set_proofgrid_per_engine_max_jobs 10
    set_proofgrid_max_jobs 30


    #SOURCE_TCL
    # assume -enable {.*ASSUME_W_R} -regexp
    # assume -disable {.*ASSUME_R_W} -regexp

    task -create mytask -copy_assumes   -regexp
    task -set mytask


    if { $CUSTOMTCL == 1 } {
        puts "=========CUSTOMTCL========="

        source /cafe/u/samanthaarcher/synthlc_tutorial/fava_isca2026/synthlc_optimized/fv/synthlc/i_SW_out/xCoverAPerfLoc/rtl2mupath_instn_reachable_perf_loc.tcl
        
        puts "=========EXIT CUSTOMTCL========="
        
    } 
   
    set_prove_time_limit 6h
    #SETPROVETIME
    #set_prove_per_property_time_limit 30m
    
    puts "=============================================================="
    puts "CHECK ASSUMPTION...."
    puts "=============================================================="
    set CA 0
    #ASSUMPTION
    #

    #set ls [get_property_list -task mytask -include {type {assert cover} }]
    #if { [llength $ls] > 10 } { 
    #    set_prove_time_limit 25m 
    #    puts "PROVEN TIME 25min" }  

    if { $CA == 1 } { 
        #set_prove_time_limit 10m
        set CONFLICT [check_assumptions -task mytask -conflict]
        puts "=============================================================="
        puts "CHECK ASSUMPTION CONFLICT result? $CONFLICT"
        puts "=============================================================="
    }  else {
        puts "AUTOPROVE:" 
        #set_prove_time_limit 1h
        #set_prove_per_property_time_limit 1h
        puts "=================================================="
        puts " PROVE TIME LIMIT"
        puts [get_prove_time_limit]     
        #puts [get_prove_per_property_time_limit]
        puts "=================================================="
        set_engine_mode {K C Tri I N AD AM Hp B}

        prove -task mytask
        #prove -all
    }
    
    puts "END"
    report -task mytask -csv -results -file "/cafe/u/samanthaarcher/synthlc_tutorial/fava_isca2026/synthlc_optimized/fv/synthlc/i_SW_out/xCoverAPerfLoc/rtl2mupath_instn_reachable_perf_loc.csv" -force
    save "/cafe/u/samanthaarcher/synthlc_tutorial/fava_isca2026/synthlc_optimized/fv/synthlc/i_SW_out/xCoverAPerfLoc/rtl2mupath_instn_reachable_perf_loc.db" -clean -include {app_data session_data elaborated_design}
    exit
}



proc get_path_info {S1 S2} {
    set s1_exist [catch { get_signal_info -logic $S1 } type1]
    if { $s1_exist == 1 } {
        puts "fail to find $S1"
    }
    set s2_exist [catch {get_signal_info -logic $S2 } type2] 
    if { $s2_exist == 1 } {
        puts "fail to find $S2"
    }
    if { $s1_exist == 0 && $s2_exist == 0 } {
        set path [graph -shortest_path -from  $S1 -to $S2 -type register]  
        puts "$S1 $S2, $path"
        puts "$type1 $type2"
        set len [llength $path]
        if {$len > 0} {
            if { $type1 == "flop" && $type2 == "flop"} {
                if { $len == 2 } {
                    puts "ADD $S1 $S2"
                } elseif { $len == 3 } {
                    set ele0 [lindex $path 0]
                    set ele1 [lindex $path 1]
                    set ele2 [lindex $path 2]
                    if {($ele0 == $ele1) || ($ele1 == $ele2)} {
                        puts "ADD $S1 $S2"
                    }
                }
            }
            if { $type1 == "flop" && $type2 == "wire" && $len <= 3 } {
                puts "ADD $S1 $S2"
            }
            if { $type1 == "wire" && $type2 == "wire" } {
                if { $len == 2 } {
                    puts "ADD(ww2) $S1 $S2"
                } elseif { $len == 3 } {
                    puts "ADD(ww) $S1 $S2"
                } 
            }
            if { $type1 == "wire" && $type2 == "flop" } {
                if { $len == 2 } {
                    puts "ADD $S1 $S2"
                }
            }
        }
    }
    puts "--------------------------------"
    return 0
}

get_path_info {ex_stage_i.i_mult.i_div.pc_q} {ex_stage_i.i_mult.i_div.pc_q}

get_path_info {ex_stage_i.i_mult.i_div.pc_q} {id_stage_i.issue_q.sbe.pc}

get_path_info {ex_stage_i.i_mult.i_div.pc_q} {issue_stage_i.i_issue_read_operands.pc_o}

get_path_info {ex_stage_i.i_mult.i_div.pc_q} {ex_stage_i.lsu_i.lsu_bypass_i.mem_q[0].pc}

get_path_info {ex_stage_i.i_mult.i_div.pc_q} {ex_stage_i.lsu_i.lsu_bypass_i.mem_q[1].pc}

get_path_info {ex_stage_i.i_mult.i_div.pc_q} {issue_stage_i.i_scoreboard.mem_q[0].sbe.pc}

get_path_info {ex_stage_i.i_mult.i_div.pc_q} {issue_stage_i.i_scoreboard.mem_q[1].sbe.pc}

get_path_info {ex_stage_i.i_mult.i_div.pc_q} {issue_stage_i.i_scoreboard.mem_q[2].sbe.pc}

get_path_info {ex_stage_i.i_mult.i_div.pc_q} {issue_stage_i.i_scoreboard.mem_q[3].sbe.pc}

get_path_info {ex_stage_i.i_mult.i_div.pc_q} {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.commit_queue_q[0].pc}

get_path_info {ex_stage_i.i_mult.i_div.pc_q} {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.commit_queue_q[1].pc}

get_path_info {ex_stage_i.i_mult.i_div.pc_q} {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.speculative_queue_q[0].pc}

get_path_info {ex_stage_i.i_mult.i_div.pc_q} {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.speculative_queue_q[1].pc}

get_path_info {ex_stage_i.i_mult.i_div.pc_q} {ex_stage_i.lsu_i.i_load_unit.load_data_q.ld_pc}

get_path_info {ex_stage_i.i_mult.i_div.pc_q} {ex_stage_i.lsu_i.i_store_unit.st_pc_q}

get_path_info {ex_stage_i.i_mult.i_div.pc_q} {ex_stage_i.lsu_i.load_pc_o}

get_path_info {ex_stage_i.i_mult.i_div.pc_q} {ex_stage_i.csr_buffer_i.csr_reg_q.pc}

get_path_info {ex_stage_i.i_mult.i_div.pc_q} {ex_stage_i.i_mult.i_multiplier.pc_q}

get_path_info {ex_stage_i.i_mult.i_div.pc_q} {ex_stage_i.lsu_i.i_load_unit.lsu_ctrl_i.pc}

get_path_info {ex_stage_i.i_mult.i_div.pc_q} {ex_stage_i.lsu_i.i_ord_sram.pc_i}

get_path_info {id_stage_i.issue_q.sbe.pc} {ex_stage_i.i_mult.i_div.pc_q}

get_path_info {id_stage_i.issue_q.sbe.pc} {issue_stage_i.i_issue_read_operands.pc_o}

get_path_info {id_stage_i.issue_q.sbe.pc} {ex_stage_i.lsu_i.lsu_bypass_i.mem_q[0].pc}

get_path_info {id_stage_i.issue_q.sbe.pc} {ex_stage_i.lsu_i.lsu_bypass_i.mem_q[1].pc}

get_path_info {id_stage_i.issue_q.sbe.pc} {issue_stage_i.i_scoreboard.mem_q[0].sbe.pc}

get_path_info {id_stage_i.issue_q.sbe.pc} {issue_stage_i.i_scoreboard.mem_q[1].sbe.pc}

get_path_info {id_stage_i.issue_q.sbe.pc} {issue_stage_i.i_scoreboard.mem_q[2].sbe.pc}

get_path_info {id_stage_i.issue_q.sbe.pc} {issue_stage_i.i_scoreboard.mem_q[3].sbe.pc}

get_path_info {id_stage_i.issue_q.sbe.pc} {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.commit_queue_q[0].pc}

get_path_info {id_stage_i.issue_q.sbe.pc} {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.commit_queue_q[1].pc}

get_path_info {id_stage_i.issue_q.sbe.pc} {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.speculative_queue_q[0].pc}

get_path_info {id_stage_i.issue_q.sbe.pc} {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.speculative_queue_q[1].pc}

get_path_info {id_stage_i.issue_q.sbe.pc} {ex_stage_i.lsu_i.i_load_unit.load_data_q.ld_pc}

get_path_info {id_stage_i.issue_q.sbe.pc} {ex_stage_i.lsu_i.i_store_unit.st_pc_q}

get_path_info {id_stage_i.issue_q.sbe.pc} {ex_stage_i.lsu_i.load_pc_o}

get_path_info {id_stage_i.issue_q.sbe.pc} {ex_stage_i.csr_buffer_i.csr_reg_q.pc}

get_path_info {id_stage_i.issue_q.sbe.pc} {ex_stage_i.i_mult.i_multiplier.pc_q}

get_path_info {id_stage_i.issue_q.sbe.pc} {ex_stage_i.lsu_i.i_load_unit.lsu_ctrl_i.pc}

get_path_info {id_stage_i.issue_q.sbe.pc} {ex_stage_i.lsu_i.i_ord_sram.pc_i}

get_path_info {issue_stage_i.i_issue_read_operands.pc_o} {ex_stage_i.i_mult.i_div.pc_q}

get_path_info {issue_stage_i.i_issue_read_operands.pc_o} {id_stage_i.issue_q.sbe.pc}

get_path_info {issue_stage_i.i_issue_read_operands.pc_o} {issue_stage_i.i_issue_read_operands.pc_o}

get_path_info {issue_stage_i.i_issue_read_operands.pc_o} {ex_stage_i.lsu_i.lsu_bypass_i.mem_q[0].pc}

get_path_info {issue_stage_i.i_issue_read_operands.pc_o} {ex_stage_i.lsu_i.lsu_bypass_i.mem_q[1].pc}

get_path_info {issue_stage_i.i_issue_read_operands.pc_o} {issue_stage_i.i_scoreboard.mem_q[0].sbe.pc}

get_path_info {issue_stage_i.i_issue_read_operands.pc_o} {issue_stage_i.i_scoreboard.mem_q[1].sbe.pc}

get_path_info {issue_stage_i.i_issue_read_operands.pc_o} {issue_stage_i.i_scoreboard.mem_q[2].sbe.pc}

get_path_info {issue_stage_i.i_issue_read_operands.pc_o} {issue_stage_i.i_scoreboard.mem_q[3].sbe.pc}

get_path_info {issue_stage_i.i_issue_read_operands.pc_o} {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.commit_queue_q[0].pc}

get_path_info {issue_stage_i.i_issue_read_operands.pc_o} {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.commit_queue_q[1].pc}

get_path_info {issue_stage_i.i_issue_read_operands.pc_o} {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.speculative_queue_q[0].pc}

get_path_info {issue_stage_i.i_issue_read_operands.pc_o} {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.speculative_queue_q[1].pc}

get_path_info {issue_stage_i.i_issue_read_operands.pc_o} {ex_stage_i.lsu_i.i_load_unit.load_data_q.ld_pc}

get_path_info {issue_stage_i.i_issue_read_operands.pc_o} {ex_stage_i.lsu_i.i_store_unit.st_pc_q}

get_path_info {issue_stage_i.i_issue_read_operands.pc_o} {ex_stage_i.lsu_i.load_pc_o}

get_path_info {issue_stage_i.i_issue_read_operands.pc_o} {ex_stage_i.csr_buffer_i.csr_reg_q.pc}

get_path_info {issue_stage_i.i_issue_read_operands.pc_o} {ex_stage_i.i_mult.i_multiplier.pc_q}

get_path_info {issue_stage_i.i_issue_read_operands.pc_o} {ex_stage_i.lsu_i.i_load_unit.lsu_ctrl_i.pc}

get_path_info {issue_stage_i.i_issue_read_operands.pc_o} {ex_stage_i.lsu_i.i_ord_sram.pc_i}

get_path_info {ex_stage_i.lsu_i.lsu_bypass_i.mem_q[0].pc} {ex_stage_i.i_mult.i_div.pc_q}

get_path_info {ex_stage_i.lsu_i.lsu_bypass_i.mem_q[0].pc} {id_stage_i.issue_q.sbe.pc}

get_path_info {ex_stage_i.lsu_i.lsu_bypass_i.mem_q[0].pc} {issue_stage_i.i_issue_read_operands.pc_o}

get_path_info {ex_stage_i.lsu_i.lsu_bypass_i.mem_q[0].pc} {ex_stage_i.lsu_i.lsu_bypass_i.mem_q[1].pc}

get_path_info {ex_stage_i.lsu_i.lsu_bypass_i.mem_q[0].pc} {issue_stage_i.i_scoreboard.mem_q[0].sbe.pc}

get_path_info {ex_stage_i.lsu_i.lsu_bypass_i.mem_q[0].pc} {issue_stage_i.i_scoreboard.mem_q[1].sbe.pc}

get_path_info {ex_stage_i.lsu_i.lsu_bypass_i.mem_q[0].pc} {issue_stage_i.i_scoreboard.mem_q[2].sbe.pc}

get_path_info {ex_stage_i.lsu_i.lsu_bypass_i.mem_q[0].pc} {issue_stage_i.i_scoreboard.mem_q[3].sbe.pc}

get_path_info {ex_stage_i.lsu_i.lsu_bypass_i.mem_q[0].pc} {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.commit_queue_q[0].pc}

get_path_info {ex_stage_i.lsu_i.lsu_bypass_i.mem_q[0].pc} {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.commit_queue_q[1].pc}

get_path_info {ex_stage_i.lsu_i.lsu_bypass_i.mem_q[0].pc} {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.speculative_queue_q[0].pc}

get_path_info {ex_stage_i.lsu_i.lsu_bypass_i.mem_q[0].pc} {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.speculative_queue_q[1].pc}

get_path_info {ex_stage_i.lsu_i.lsu_bypass_i.mem_q[0].pc} {ex_stage_i.lsu_i.i_load_unit.load_data_q.ld_pc}

get_path_info {ex_stage_i.lsu_i.lsu_bypass_i.mem_q[0].pc} {ex_stage_i.lsu_i.i_store_unit.st_pc_q}

get_path_info {ex_stage_i.lsu_i.lsu_bypass_i.mem_q[0].pc} {ex_stage_i.lsu_i.load_pc_o}

get_path_info {ex_stage_i.lsu_i.lsu_bypass_i.mem_q[0].pc} {ex_stage_i.csr_buffer_i.csr_reg_q.pc}

get_path_info {ex_stage_i.lsu_i.lsu_bypass_i.mem_q[0].pc} {ex_stage_i.i_mult.i_multiplier.pc_q}

get_path_info {ex_stage_i.lsu_i.lsu_bypass_i.mem_q[0].pc} {ex_stage_i.lsu_i.i_load_unit.lsu_ctrl_i.pc}

get_path_info {ex_stage_i.lsu_i.lsu_bypass_i.mem_q[0].pc} {ex_stage_i.lsu_i.i_ord_sram.pc_i}

get_path_info {ex_stage_i.lsu_i.lsu_bypass_i.mem_q[1].pc} {ex_stage_i.i_mult.i_div.pc_q}

get_path_info {ex_stage_i.lsu_i.lsu_bypass_i.mem_q[1].pc} {id_stage_i.issue_q.sbe.pc}

get_path_info {ex_stage_i.lsu_i.lsu_bypass_i.mem_q[1].pc} {issue_stage_i.i_issue_read_operands.pc_o}

get_path_info {ex_stage_i.lsu_i.lsu_bypass_i.mem_q[1].pc} {ex_stage_i.lsu_i.lsu_bypass_i.mem_q[0].pc}

get_path_info {ex_stage_i.lsu_i.lsu_bypass_i.mem_q[1].pc} {issue_stage_i.i_scoreboard.mem_q[0].sbe.pc}

get_path_info {ex_stage_i.lsu_i.lsu_bypass_i.mem_q[1].pc} {issue_stage_i.i_scoreboard.mem_q[1].sbe.pc}

get_path_info {ex_stage_i.lsu_i.lsu_bypass_i.mem_q[1].pc} {issue_stage_i.i_scoreboard.mem_q[2].sbe.pc}

get_path_info {ex_stage_i.lsu_i.lsu_bypass_i.mem_q[1].pc} {issue_stage_i.i_scoreboard.mem_q[3].sbe.pc}

get_path_info {ex_stage_i.lsu_i.lsu_bypass_i.mem_q[1].pc} {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.commit_queue_q[0].pc}

get_path_info {ex_stage_i.lsu_i.lsu_bypass_i.mem_q[1].pc} {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.commit_queue_q[1].pc}

get_path_info {ex_stage_i.lsu_i.lsu_bypass_i.mem_q[1].pc} {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.speculative_queue_q[0].pc}

get_path_info {ex_stage_i.lsu_i.lsu_bypass_i.mem_q[1].pc} {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.speculative_queue_q[1].pc}

get_path_info {ex_stage_i.lsu_i.lsu_bypass_i.mem_q[1].pc} {ex_stage_i.lsu_i.i_load_unit.load_data_q.ld_pc}

get_path_info {ex_stage_i.lsu_i.lsu_bypass_i.mem_q[1].pc} {ex_stage_i.lsu_i.i_store_unit.st_pc_q}

get_path_info {ex_stage_i.lsu_i.lsu_bypass_i.mem_q[1].pc} {ex_stage_i.lsu_i.load_pc_o}

get_path_info {ex_stage_i.lsu_i.lsu_bypass_i.mem_q[1].pc} {ex_stage_i.csr_buffer_i.csr_reg_q.pc}

get_path_info {ex_stage_i.lsu_i.lsu_bypass_i.mem_q[1].pc} {ex_stage_i.i_mult.i_multiplier.pc_q}

get_path_info {ex_stage_i.lsu_i.lsu_bypass_i.mem_q[1].pc} {ex_stage_i.lsu_i.i_load_unit.lsu_ctrl_i.pc}

get_path_info {ex_stage_i.lsu_i.lsu_bypass_i.mem_q[1].pc} {ex_stage_i.lsu_i.i_ord_sram.pc_i}

get_path_info {issue_stage_i.i_scoreboard.mem_q[0].sbe.pc} {ex_stage_i.i_mult.i_div.pc_q}

get_path_info {issue_stage_i.i_scoreboard.mem_q[0].sbe.pc} {id_stage_i.issue_q.sbe.pc}

get_path_info {issue_stage_i.i_scoreboard.mem_q[0].sbe.pc} {issue_stage_i.i_issue_read_operands.pc_o}

get_path_info {issue_stage_i.i_scoreboard.mem_q[0].sbe.pc} {ex_stage_i.lsu_i.lsu_bypass_i.mem_q[0].pc}

get_path_info {issue_stage_i.i_scoreboard.mem_q[0].sbe.pc} {ex_stage_i.lsu_i.lsu_bypass_i.mem_q[1].pc}

get_path_info {issue_stage_i.i_scoreboard.mem_q[0].sbe.pc} {issue_stage_i.i_scoreboard.mem_q[0].sbe.pc}

get_path_info {issue_stage_i.i_scoreboard.mem_q[0].sbe.pc} {issue_stage_i.i_scoreboard.mem_q[1].sbe.pc}

get_path_info {issue_stage_i.i_scoreboard.mem_q[0].sbe.pc} {issue_stage_i.i_scoreboard.mem_q[2].sbe.pc}

get_path_info {issue_stage_i.i_scoreboard.mem_q[0].sbe.pc} {issue_stage_i.i_scoreboard.mem_q[3].sbe.pc}

get_path_info {issue_stage_i.i_scoreboard.mem_q[0].sbe.pc} {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.commit_queue_q[0].pc}

get_path_info {issue_stage_i.i_scoreboard.mem_q[0].sbe.pc} {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.commit_queue_q[1].pc}

get_path_info {issue_stage_i.i_scoreboard.mem_q[0].sbe.pc} {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.speculative_queue_q[0].pc}

get_path_info {issue_stage_i.i_scoreboard.mem_q[0].sbe.pc} {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.speculative_queue_q[1].pc}

get_path_info {issue_stage_i.i_scoreboard.mem_q[0].sbe.pc} {ex_stage_i.lsu_i.i_load_unit.load_data_q.ld_pc}

get_path_info {issue_stage_i.i_scoreboard.mem_q[0].sbe.pc} {ex_stage_i.lsu_i.i_store_unit.st_pc_q}

get_path_info {issue_stage_i.i_scoreboard.mem_q[0].sbe.pc} {ex_stage_i.lsu_i.load_pc_o}

get_path_info {issue_stage_i.i_scoreboard.mem_q[0].sbe.pc} {ex_stage_i.csr_buffer_i.csr_reg_q.pc}

get_path_info {issue_stage_i.i_scoreboard.mem_q[0].sbe.pc} {ex_stage_i.i_mult.i_multiplier.pc_q}

get_path_info {issue_stage_i.i_scoreboard.mem_q[0].sbe.pc} {ex_stage_i.lsu_i.i_load_unit.lsu_ctrl_i.pc}

get_path_info {issue_stage_i.i_scoreboard.mem_q[0].sbe.pc} {ex_stage_i.lsu_i.i_ord_sram.pc_i}

get_path_info {issue_stage_i.i_scoreboard.mem_q[1].sbe.pc} {ex_stage_i.i_mult.i_div.pc_q}

get_path_info {issue_stage_i.i_scoreboard.mem_q[1].sbe.pc} {id_stage_i.issue_q.sbe.pc}

get_path_info {issue_stage_i.i_scoreboard.mem_q[1].sbe.pc} {issue_stage_i.i_issue_read_operands.pc_o}

get_path_info {issue_stage_i.i_scoreboard.mem_q[1].sbe.pc} {ex_stage_i.lsu_i.lsu_bypass_i.mem_q[0].pc}

get_path_info {issue_stage_i.i_scoreboard.mem_q[1].sbe.pc} {ex_stage_i.lsu_i.lsu_bypass_i.mem_q[1].pc}

get_path_info {issue_stage_i.i_scoreboard.mem_q[1].sbe.pc} {issue_stage_i.i_scoreboard.mem_q[0].sbe.pc}

get_path_info {issue_stage_i.i_scoreboard.mem_q[1].sbe.pc} {issue_stage_i.i_scoreboard.mem_q[1].sbe.pc}

get_path_info {issue_stage_i.i_scoreboard.mem_q[1].sbe.pc} {issue_stage_i.i_scoreboard.mem_q[2].sbe.pc}

get_path_info {issue_stage_i.i_scoreboard.mem_q[1].sbe.pc} {issue_stage_i.i_scoreboard.mem_q[3].sbe.pc}

get_path_info {issue_stage_i.i_scoreboard.mem_q[1].sbe.pc} {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.commit_queue_q[0].pc}

get_path_info {issue_stage_i.i_scoreboard.mem_q[1].sbe.pc} {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.commit_queue_q[1].pc}

get_path_info {issue_stage_i.i_scoreboard.mem_q[1].sbe.pc} {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.speculative_queue_q[0].pc}

get_path_info {issue_stage_i.i_scoreboard.mem_q[1].sbe.pc} {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.speculative_queue_q[1].pc}

get_path_info {issue_stage_i.i_scoreboard.mem_q[1].sbe.pc} {ex_stage_i.lsu_i.i_load_unit.load_data_q.ld_pc}

get_path_info {issue_stage_i.i_scoreboard.mem_q[1].sbe.pc} {ex_stage_i.lsu_i.i_store_unit.st_pc_q}

get_path_info {issue_stage_i.i_scoreboard.mem_q[1].sbe.pc} {ex_stage_i.lsu_i.load_pc_o}

get_path_info {issue_stage_i.i_scoreboard.mem_q[1].sbe.pc} {ex_stage_i.csr_buffer_i.csr_reg_q.pc}

get_path_info {issue_stage_i.i_scoreboard.mem_q[1].sbe.pc} {ex_stage_i.i_mult.i_multiplier.pc_q}

get_path_info {issue_stage_i.i_scoreboard.mem_q[1].sbe.pc} {ex_stage_i.lsu_i.i_load_unit.lsu_ctrl_i.pc}

get_path_info {issue_stage_i.i_scoreboard.mem_q[1].sbe.pc} {ex_stage_i.lsu_i.i_ord_sram.pc_i}

get_path_info {issue_stage_i.i_scoreboard.mem_q[2].sbe.pc} {ex_stage_i.i_mult.i_div.pc_q}

get_path_info {issue_stage_i.i_scoreboard.mem_q[2].sbe.pc} {id_stage_i.issue_q.sbe.pc}

get_path_info {issue_stage_i.i_scoreboard.mem_q[2].sbe.pc} {issue_stage_i.i_issue_read_operands.pc_o}

get_path_info {issue_stage_i.i_scoreboard.mem_q[2].sbe.pc} {ex_stage_i.lsu_i.lsu_bypass_i.mem_q[0].pc}

get_path_info {issue_stage_i.i_scoreboard.mem_q[2].sbe.pc} {ex_stage_i.lsu_i.lsu_bypass_i.mem_q[1].pc}

get_path_info {issue_stage_i.i_scoreboard.mem_q[2].sbe.pc} {issue_stage_i.i_scoreboard.mem_q[0].sbe.pc}

get_path_info {issue_stage_i.i_scoreboard.mem_q[2].sbe.pc} {issue_stage_i.i_scoreboard.mem_q[1].sbe.pc}

get_path_info {issue_stage_i.i_scoreboard.mem_q[2].sbe.pc} {issue_stage_i.i_scoreboard.mem_q[2].sbe.pc}

get_path_info {issue_stage_i.i_scoreboard.mem_q[2].sbe.pc} {issue_stage_i.i_scoreboard.mem_q[3].sbe.pc}

get_path_info {issue_stage_i.i_scoreboard.mem_q[2].sbe.pc} {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.commit_queue_q[0].pc}

get_path_info {issue_stage_i.i_scoreboard.mem_q[2].sbe.pc} {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.commit_queue_q[1].pc}

get_path_info {issue_stage_i.i_scoreboard.mem_q[2].sbe.pc} {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.speculative_queue_q[0].pc}

get_path_info {issue_stage_i.i_scoreboard.mem_q[2].sbe.pc} {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.speculative_queue_q[1].pc}

get_path_info {issue_stage_i.i_scoreboard.mem_q[2].sbe.pc} {ex_stage_i.lsu_i.i_load_unit.load_data_q.ld_pc}

get_path_info {issue_stage_i.i_scoreboard.mem_q[2].sbe.pc} {ex_stage_i.lsu_i.i_store_unit.st_pc_q}

get_path_info {issue_stage_i.i_scoreboard.mem_q[2].sbe.pc} {ex_stage_i.lsu_i.load_pc_o}

get_path_info {issue_stage_i.i_scoreboard.mem_q[2].sbe.pc} {ex_stage_i.csr_buffer_i.csr_reg_q.pc}

get_path_info {issue_stage_i.i_scoreboard.mem_q[2].sbe.pc} {ex_stage_i.i_mult.i_multiplier.pc_q}

get_path_info {issue_stage_i.i_scoreboard.mem_q[2].sbe.pc} {ex_stage_i.lsu_i.i_load_unit.lsu_ctrl_i.pc}

get_path_info {issue_stage_i.i_scoreboard.mem_q[2].sbe.pc} {ex_stage_i.lsu_i.i_ord_sram.pc_i}

get_path_info {issue_stage_i.i_scoreboard.mem_q[3].sbe.pc} {ex_stage_i.i_mult.i_div.pc_q}

get_path_info {issue_stage_i.i_scoreboard.mem_q[3].sbe.pc} {id_stage_i.issue_q.sbe.pc}

get_path_info {issue_stage_i.i_scoreboard.mem_q[3].sbe.pc} {issue_stage_i.i_issue_read_operands.pc_o}

get_path_info {issue_stage_i.i_scoreboard.mem_q[3].sbe.pc} {ex_stage_i.lsu_i.lsu_bypass_i.mem_q[0].pc}

get_path_info {issue_stage_i.i_scoreboard.mem_q[3].sbe.pc} {ex_stage_i.lsu_i.lsu_bypass_i.mem_q[1].pc}

get_path_info {issue_stage_i.i_scoreboard.mem_q[3].sbe.pc} {issue_stage_i.i_scoreboard.mem_q[0].sbe.pc}

get_path_info {issue_stage_i.i_scoreboard.mem_q[3].sbe.pc} {issue_stage_i.i_scoreboard.mem_q[1].sbe.pc}

get_path_info {issue_stage_i.i_scoreboard.mem_q[3].sbe.pc} {issue_stage_i.i_scoreboard.mem_q[2].sbe.pc}

get_path_info {issue_stage_i.i_scoreboard.mem_q[3].sbe.pc} {issue_stage_i.i_scoreboard.mem_q[3].sbe.pc}

get_path_info {issue_stage_i.i_scoreboard.mem_q[3].sbe.pc} {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.commit_queue_q[0].pc}

get_path_info {issue_stage_i.i_scoreboard.mem_q[3].sbe.pc} {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.commit_queue_q[1].pc}

get_path_info {issue_stage_i.i_scoreboard.mem_q[3].sbe.pc} {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.speculative_queue_q[0].pc}

get_path_info {issue_stage_i.i_scoreboard.mem_q[3].sbe.pc} {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.speculative_queue_q[1].pc}

get_path_info {issue_stage_i.i_scoreboard.mem_q[3].sbe.pc} {ex_stage_i.lsu_i.i_load_unit.load_data_q.ld_pc}

get_path_info {issue_stage_i.i_scoreboard.mem_q[3].sbe.pc} {ex_stage_i.lsu_i.i_store_unit.st_pc_q}

get_path_info {issue_stage_i.i_scoreboard.mem_q[3].sbe.pc} {ex_stage_i.lsu_i.load_pc_o}

get_path_info {issue_stage_i.i_scoreboard.mem_q[3].sbe.pc} {ex_stage_i.csr_buffer_i.csr_reg_q.pc}

get_path_info {issue_stage_i.i_scoreboard.mem_q[3].sbe.pc} {ex_stage_i.i_mult.i_multiplier.pc_q}

get_path_info {issue_stage_i.i_scoreboard.mem_q[3].sbe.pc} {ex_stage_i.lsu_i.i_load_unit.lsu_ctrl_i.pc}

get_path_info {issue_stage_i.i_scoreboard.mem_q[3].sbe.pc} {ex_stage_i.lsu_i.i_ord_sram.pc_i}

get_path_info {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.commit_queue_q[0].pc} {ex_stage_i.i_mult.i_div.pc_q}

get_path_info {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.commit_queue_q[0].pc} {id_stage_i.issue_q.sbe.pc}

get_path_info {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.commit_queue_q[0].pc} {issue_stage_i.i_issue_read_operands.pc_o}

get_path_info {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.commit_queue_q[0].pc} {ex_stage_i.lsu_i.lsu_bypass_i.mem_q[0].pc}

get_path_info {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.commit_queue_q[0].pc} {ex_stage_i.lsu_i.lsu_bypass_i.mem_q[1].pc}

get_path_info {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.commit_queue_q[0].pc} {issue_stage_i.i_scoreboard.mem_q[0].sbe.pc}

get_path_info {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.commit_queue_q[0].pc} {issue_stage_i.i_scoreboard.mem_q[1].sbe.pc}

get_path_info {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.commit_queue_q[0].pc} {issue_stage_i.i_scoreboard.mem_q[2].sbe.pc}

get_path_info {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.commit_queue_q[0].pc} {issue_stage_i.i_scoreboard.mem_q[3].sbe.pc}

get_path_info {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.commit_queue_q[0].pc} {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.commit_queue_q[1].pc}

get_path_info {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.commit_queue_q[0].pc} {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.speculative_queue_q[0].pc}

get_path_info {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.commit_queue_q[0].pc} {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.speculative_queue_q[1].pc}

get_path_info {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.commit_queue_q[0].pc} {ex_stage_i.lsu_i.i_load_unit.load_data_q.ld_pc}

get_path_info {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.commit_queue_q[0].pc} {ex_stage_i.lsu_i.i_store_unit.st_pc_q}

get_path_info {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.commit_queue_q[0].pc} {ex_stage_i.lsu_i.load_pc_o}

get_path_info {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.commit_queue_q[0].pc} {ex_stage_i.csr_buffer_i.csr_reg_q.pc}

get_path_info {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.commit_queue_q[0].pc} {ex_stage_i.i_mult.i_multiplier.pc_q}

get_path_info {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.commit_queue_q[0].pc} {ex_stage_i.lsu_i.i_load_unit.lsu_ctrl_i.pc}

get_path_info {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.commit_queue_q[0].pc} {ex_stage_i.lsu_i.i_ord_sram.pc_i}

get_path_info {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.commit_queue_q[1].pc} {ex_stage_i.i_mult.i_div.pc_q}

get_path_info {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.commit_queue_q[1].pc} {id_stage_i.issue_q.sbe.pc}

get_path_info {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.commit_queue_q[1].pc} {issue_stage_i.i_issue_read_operands.pc_o}

get_path_info {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.commit_queue_q[1].pc} {ex_stage_i.lsu_i.lsu_bypass_i.mem_q[0].pc}

get_path_info {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.commit_queue_q[1].pc} {ex_stage_i.lsu_i.lsu_bypass_i.mem_q[1].pc}

get_path_info {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.commit_queue_q[1].pc} {issue_stage_i.i_scoreboard.mem_q[0].sbe.pc}

get_path_info {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.commit_queue_q[1].pc} {issue_stage_i.i_scoreboard.mem_q[1].sbe.pc}

get_path_info {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.commit_queue_q[1].pc} {issue_stage_i.i_scoreboard.mem_q[2].sbe.pc}

get_path_info {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.commit_queue_q[1].pc} {issue_stage_i.i_scoreboard.mem_q[3].sbe.pc}

get_path_info {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.commit_queue_q[1].pc} {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.commit_queue_q[0].pc}

get_path_info {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.commit_queue_q[1].pc} {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.speculative_queue_q[0].pc}

get_path_info {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.commit_queue_q[1].pc} {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.speculative_queue_q[1].pc}

get_path_info {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.commit_queue_q[1].pc} {ex_stage_i.lsu_i.i_load_unit.load_data_q.ld_pc}

get_path_info {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.commit_queue_q[1].pc} {ex_stage_i.lsu_i.i_store_unit.st_pc_q}

get_path_info {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.commit_queue_q[1].pc} {ex_stage_i.lsu_i.load_pc_o}

get_path_info {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.commit_queue_q[1].pc} {ex_stage_i.csr_buffer_i.csr_reg_q.pc}

get_path_info {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.commit_queue_q[1].pc} {ex_stage_i.i_mult.i_multiplier.pc_q}

get_path_info {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.commit_queue_q[1].pc} {ex_stage_i.lsu_i.i_load_unit.lsu_ctrl_i.pc}

get_path_info {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.commit_queue_q[1].pc} {ex_stage_i.lsu_i.i_ord_sram.pc_i}

get_path_info {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.speculative_queue_q[0].pc} {ex_stage_i.i_mult.i_div.pc_q}

get_path_info {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.speculative_queue_q[0].pc} {id_stage_i.issue_q.sbe.pc}

get_path_info {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.speculative_queue_q[0].pc} {issue_stage_i.i_issue_read_operands.pc_o}

get_path_info {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.speculative_queue_q[0].pc} {ex_stage_i.lsu_i.lsu_bypass_i.mem_q[0].pc}

get_path_info {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.speculative_queue_q[0].pc} {ex_stage_i.lsu_i.lsu_bypass_i.mem_q[1].pc}

get_path_info {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.speculative_queue_q[0].pc} {issue_stage_i.i_scoreboard.mem_q[0].sbe.pc}

get_path_info {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.speculative_queue_q[0].pc} {issue_stage_i.i_scoreboard.mem_q[1].sbe.pc}

get_path_info {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.speculative_queue_q[0].pc} {issue_stage_i.i_scoreboard.mem_q[2].sbe.pc}

get_path_info {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.speculative_queue_q[0].pc} {issue_stage_i.i_scoreboard.mem_q[3].sbe.pc}

get_path_info {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.speculative_queue_q[0].pc} {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.commit_queue_q[0].pc}

get_path_info {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.speculative_queue_q[0].pc} {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.commit_queue_q[1].pc}

get_path_info {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.speculative_queue_q[0].pc} {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.speculative_queue_q[1].pc}

get_path_info {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.speculative_queue_q[0].pc} {ex_stage_i.lsu_i.i_load_unit.load_data_q.ld_pc}

get_path_info {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.speculative_queue_q[0].pc} {ex_stage_i.lsu_i.i_store_unit.st_pc_q}

get_path_info {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.speculative_queue_q[0].pc} {ex_stage_i.lsu_i.load_pc_o}

get_path_info {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.speculative_queue_q[0].pc} {ex_stage_i.csr_buffer_i.csr_reg_q.pc}

get_path_info {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.speculative_queue_q[0].pc} {ex_stage_i.i_mult.i_multiplier.pc_q}

get_path_info {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.speculative_queue_q[0].pc} {ex_stage_i.lsu_i.i_load_unit.lsu_ctrl_i.pc}

get_path_info {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.speculative_queue_q[0].pc} {ex_stage_i.lsu_i.i_ord_sram.pc_i}

get_path_info {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.speculative_queue_q[1].pc} {ex_stage_i.i_mult.i_div.pc_q}

get_path_info {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.speculative_queue_q[1].pc} {id_stage_i.issue_q.sbe.pc}

get_path_info {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.speculative_queue_q[1].pc} {issue_stage_i.i_issue_read_operands.pc_o}

get_path_info {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.speculative_queue_q[1].pc} {ex_stage_i.lsu_i.lsu_bypass_i.mem_q[0].pc}

get_path_info {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.speculative_queue_q[1].pc} {ex_stage_i.lsu_i.lsu_bypass_i.mem_q[1].pc}

get_path_info {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.speculative_queue_q[1].pc} {issue_stage_i.i_scoreboard.mem_q[0].sbe.pc}

get_path_info {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.speculative_queue_q[1].pc} {issue_stage_i.i_scoreboard.mem_q[1].sbe.pc}

get_path_info {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.speculative_queue_q[1].pc} {issue_stage_i.i_scoreboard.mem_q[2].sbe.pc}

get_path_info {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.speculative_queue_q[1].pc} {issue_stage_i.i_scoreboard.mem_q[3].sbe.pc}

get_path_info {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.speculative_queue_q[1].pc} {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.commit_queue_q[0].pc}

get_path_info {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.speculative_queue_q[1].pc} {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.commit_queue_q[1].pc}

get_path_info {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.speculative_queue_q[1].pc} {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.speculative_queue_q[0].pc}

get_path_info {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.speculative_queue_q[1].pc} {ex_stage_i.lsu_i.i_load_unit.load_data_q.ld_pc}

get_path_info {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.speculative_queue_q[1].pc} {ex_stage_i.lsu_i.i_store_unit.st_pc_q}

get_path_info {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.speculative_queue_q[1].pc} {ex_stage_i.lsu_i.load_pc_o}

get_path_info {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.speculative_queue_q[1].pc} {ex_stage_i.csr_buffer_i.csr_reg_q.pc}

get_path_info {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.speculative_queue_q[1].pc} {ex_stage_i.i_mult.i_multiplier.pc_q}

get_path_info {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.speculative_queue_q[1].pc} {ex_stage_i.lsu_i.i_load_unit.lsu_ctrl_i.pc}

get_path_info {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.speculative_queue_q[1].pc} {ex_stage_i.lsu_i.i_ord_sram.pc_i}

get_path_info {ex_stage_i.lsu_i.i_load_unit.load_data_q.ld_pc} {ex_stage_i.i_mult.i_div.pc_q}

get_path_info {ex_stage_i.lsu_i.i_load_unit.load_data_q.ld_pc} {id_stage_i.issue_q.sbe.pc}

get_path_info {ex_stage_i.lsu_i.i_load_unit.load_data_q.ld_pc} {issue_stage_i.i_issue_read_operands.pc_o}

get_path_info {ex_stage_i.lsu_i.i_load_unit.load_data_q.ld_pc} {ex_stage_i.lsu_i.lsu_bypass_i.mem_q[0].pc}

get_path_info {ex_stage_i.lsu_i.i_load_unit.load_data_q.ld_pc} {ex_stage_i.lsu_i.lsu_bypass_i.mem_q[1].pc}

get_path_info {ex_stage_i.lsu_i.i_load_unit.load_data_q.ld_pc} {issue_stage_i.i_scoreboard.mem_q[0].sbe.pc}

get_path_info {ex_stage_i.lsu_i.i_load_unit.load_data_q.ld_pc} {issue_stage_i.i_scoreboard.mem_q[1].sbe.pc}

get_path_info {ex_stage_i.lsu_i.i_load_unit.load_data_q.ld_pc} {issue_stage_i.i_scoreboard.mem_q[2].sbe.pc}

get_path_info {ex_stage_i.lsu_i.i_load_unit.load_data_q.ld_pc} {issue_stage_i.i_scoreboard.mem_q[3].sbe.pc}

get_path_info {ex_stage_i.lsu_i.i_load_unit.load_data_q.ld_pc} {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.commit_queue_q[0].pc}

get_path_info {ex_stage_i.lsu_i.i_load_unit.load_data_q.ld_pc} {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.commit_queue_q[1].pc}

get_path_info {ex_stage_i.lsu_i.i_load_unit.load_data_q.ld_pc} {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.speculative_queue_q[0].pc}

get_path_info {ex_stage_i.lsu_i.i_load_unit.load_data_q.ld_pc} {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.speculative_queue_q[1].pc}

get_path_info {ex_stage_i.lsu_i.i_load_unit.load_data_q.ld_pc} {ex_stage_i.lsu_i.i_store_unit.st_pc_q}

get_path_info {ex_stage_i.lsu_i.i_load_unit.load_data_q.ld_pc} {ex_stage_i.lsu_i.load_pc_o}

get_path_info {ex_stage_i.lsu_i.i_load_unit.load_data_q.ld_pc} {ex_stage_i.csr_buffer_i.csr_reg_q.pc}

get_path_info {ex_stage_i.lsu_i.i_load_unit.load_data_q.ld_pc} {ex_stage_i.i_mult.i_multiplier.pc_q}

get_path_info {ex_stage_i.lsu_i.i_load_unit.load_data_q.ld_pc} {ex_stage_i.lsu_i.i_load_unit.lsu_ctrl_i.pc}

get_path_info {ex_stage_i.lsu_i.i_load_unit.load_data_q.ld_pc} {ex_stage_i.lsu_i.i_ord_sram.pc_i}

get_path_info {ex_stage_i.lsu_i.i_store_unit.st_pc_q} {ex_stage_i.i_mult.i_div.pc_q}

get_path_info {ex_stage_i.lsu_i.i_store_unit.st_pc_q} {id_stage_i.issue_q.sbe.pc}

get_path_info {ex_stage_i.lsu_i.i_store_unit.st_pc_q} {issue_stage_i.i_issue_read_operands.pc_o}

get_path_info {ex_stage_i.lsu_i.i_store_unit.st_pc_q} {ex_stage_i.lsu_i.lsu_bypass_i.mem_q[0].pc}

get_path_info {ex_stage_i.lsu_i.i_store_unit.st_pc_q} {ex_stage_i.lsu_i.lsu_bypass_i.mem_q[1].pc}

get_path_info {ex_stage_i.lsu_i.i_store_unit.st_pc_q} {issue_stage_i.i_scoreboard.mem_q[0].sbe.pc}

get_path_info {ex_stage_i.lsu_i.i_store_unit.st_pc_q} {issue_stage_i.i_scoreboard.mem_q[1].sbe.pc}

get_path_info {ex_stage_i.lsu_i.i_store_unit.st_pc_q} {issue_stage_i.i_scoreboard.mem_q[2].sbe.pc}

get_path_info {ex_stage_i.lsu_i.i_store_unit.st_pc_q} {issue_stage_i.i_scoreboard.mem_q[3].sbe.pc}

get_path_info {ex_stage_i.lsu_i.i_store_unit.st_pc_q} {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.commit_queue_q[0].pc}

get_path_info {ex_stage_i.lsu_i.i_store_unit.st_pc_q} {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.commit_queue_q[1].pc}

get_path_info {ex_stage_i.lsu_i.i_store_unit.st_pc_q} {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.speculative_queue_q[0].pc}

get_path_info {ex_stage_i.lsu_i.i_store_unit.st_pc_q} {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.speculative_queue_q[1].pc}

get_path_info {ex_stage_i.lsu_i.i_store_unit.st_pc_q} {ex_stage_i.lsu_i.i_load_unit.load_data_q.ld_pc}

get_path_info {ex_stage_i.lsu_i.i_store_unit.st_pc_q} {ex_stage_i.lsu_i.i_store_unit.st_pc_q}

get_path_info {ex_stage_i.lsu_i.i_store_unit.st_pc_q} {ex_stage_i.lsu_i.load_pc_o}

get_path_info {ex_stage_i.lsu_i.i_store_unit.st_pc_q} {ex_stage_i.csr_buffer_i.csr_reg_q.pc}

get_path_info {ex_stage_i.lsu_i.i_store_unit.st_pc_q} {ex_stage_i.i_mult.i_multiplier.pc_q}

get_path_info {ex_stage_i.lsu_i.i_store_unit.st_pc_q} {ex_stage_i.lsu_i.i_load_unit.lsu_ctrl_i.pc}

get_path_info {ex_stage_i.lsu_i.i_store_unit.st_pc_q} {ex_stage_i.lsu_i.i_ord_sram.pc_i}

get_path_info {ex_stage_i.lsu_i.load_pc_o} {ex_stage_i.i_mult.i_div.pc_q}

get_path_info {ex_stage_i.lsu_i.load_pc_o} {id_stage_i.issue_q.sbe.pc}

get_path_info {ex_stage_i.lsu_i.load_pc_o} {issue_stage_i.i_issue_read_operands.pc_o}

get_path_info {ex_stage_i.lsu_i.load_pc_o} {ex_stage_i.lsu_i.lsu_bypass_i.mem_q[0].pc}

get_path_info {ex_stage_i.lsu_i.load_pc_o} {ex_stage_i.lsu_i.lsu_bypass_i.mem_q[1].pc}

get_path_info {ex_stage_i.lsu_i.load_pc_o} {issue_stage_i.i_scoreboard.mem_q[0].sbe.pc}

get_path_info {ex_stage_i.lsu_i.load_pc_o} {issue_stage_i.i_scoreboard.mem_q[1].sbe.pc}

get_path_info {ex_stage_i.lsu_i.load_pc_o} {issue_stage_i.i_scoreboard.mem_q[2].sbe.pc}

get_path_info {ex_stage_i.lsu_i.load_pc_o} {issue_stage_i.i_scoreboard.mem_q[3].sbe.pc}

get_path_info {ex_stage_i.lsu_i.load_pc_o} {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.commit_queue_q[0].pc}

get_path_info {ex_stage_i.lsu_i.load_pc_o} {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.commit_queue_q[1].pc}

get_path_info {ex_stage_i.lsu_i.load_pc_o} {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.speculative_queue_q[0].pc}

get_path_info {ex_stage_i.lsu_i.load_pc_o} {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.speculative_queue_q[1].pc}

get_path_info {ex_stage_i.lsu_i.load_pc_o} {ex_stage_i.lsu_i.i_load_unit.load_data_q.ld_pc}

get_path_info {ex_stage_i.lsu_i.load_pc_o} {ex_stage_i.lsu_i.i_store_unit.st_pc_q}

get_path_info {ex_stage_i.lsu_i.load_pc_o} {ex_stage_i.csr_buffer_i.csr_reg_q.pc}

get_path_info {ex_stage_i.lsu_i.load_pc_o} {ex_stage_i.i_mult.i_multiplier.pc_q}

get_path_info {ex_stage_i.lsu_i.load_pc_o} {ex_stage_i.lsu_i.i_load_unit.lsu_ctrl_i.pc}

get_path_info {ex_stage_i.lsu_i.load_pc_o} {ex_stage_i.lsu_i.i_ord_sram.pc_i}

get_path_info {ex_stage_i.csr_buffer_i.csr_reg_q.pc} {ex_stage_i.i_mult.i_div.pc_q}

get_path_info {ex_stage_i.csr_buffer_i.csr_reg_q.pc} {id_stage_i.issue_q.sbe.pc}

get_path_info {ex_stage_i.csr_buffer_i.csr_reg_q.pc} {issue_stage_i.i_issue_read_operands.pc_o}

get_path_info {ex_stage_i.csr_buffer_i.csr_reg_q.pc} {ex_stage_i.lsu_i.lsu_bypass_i.mem_q[0].pc}

get_path_info {ex_stage_i.csr_buffer_i.csr_reg_q.pc} {ex_stage_i.lsu_i.lsu_bypass_i.mem_q[1].pc}

get_path_info {ex_stage_i.csr_buffer_i.csr_reg_q.pc} {issue_stage_i.i_scoreboard.mem_q[0].sbe.pc}

get_path_info {ex_stage_i.csr_buffer_i.csr_reg_q.pc} {issue_stage_i.i_scoreboard.mem_q[1].sbe.pc}

get_path_info {ex_stage_i.csr_buffer_i.csr_reg_q.pc} {issue_stage_i.i_scoreboard.mem_q[2].sbe.pc}

get_path_info {ex_stage_i.csr_buffer_i.csr_reg_q.pc} {issue_stage_i.i_scoreboard.mem_q[3].sbe.pc}

get_path_info {ex_stage_i.csr_buffer_i.csr_reg_q.pc} {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.commit_queue_q[0].pc}

get_path_info {ex_stage_i.csr_buffer_i.csr_reg_q.pc} {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.commit_queue_q[1].pc}

get_path_info {ex_stage_i.csr_buffer_i.csr_reg_q.pc} {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.speculative_queue_q[0].pc}

get_path_info {ex_stage_i.csr_buffer_i.csr_reg_q.pc} {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.speculative_queue_q[1].pc}

get_path_info {ex_stage_i.csr_buffer_i.csr_reg_q.pc} {ex_stage_i.lsu_i.i_load_unit.load_data_q.ld_pc}

get_path_info {ex_stage_i.csr_buffer_i.csr_reg_q.pc} {ex_stage_i.lsu_i.i_store_unit.st_pc_q}

get_path_info {ex_stage_i.csr_buffer_i.csr_reg_q.pc} {ex_stage_i.lsu_i.load_pc_o}

get_path_info {ex_stage_i.csr_buffer_i.csr_reg_q.pc} {ex_stage_i.i_mult.i_multiplier.pc_q}

get_path_info {ex_stage_i.csr_buffer_i.csr_reg_q.pc} {ex_stage_i.lsu_i.i_load_unit.lsu_ctrl_i.pc}

get_path_info {ex_stage_i.csr_buffer_i.csr_reg_q.pc} {ex_stage_i.lsu_i.i_ord_sram.pc_i}

get_path_info {ex_stage_i.i_mult.i_multiplier.pc_q} {ex_stage_i.i_mult.i_div.pc_q}

get_path_info {ex_stage_i.i_mult.i_multiplier.pc_q} {id_stage_i.issue_q.sbe.pc}

get_path_info {ex_stage_i.i_mult.i_multiplier.pc_q} {issue_stage_i.i_issue_read_operands.pc_o}

get_path_info {ex_stage_i.i_mult.i_multiplier.pc_q} {ex_stage_i.lsu_i.lsu_bypass_i.mem_q[0].pc}

get_path_info {ex_stage_i.i_mult.i_multiplier.pc_q} {ex_stage_i.lsu_i.lsu_bypass_i.mem_q[1].pc}

get_path_info {ex_stage_i.i_mult.i_multiplier.pc_q} {issue_stage_i.i_scoreboard.mem_q[0].sbe.pc}

get_path_info {ex_stage_i.i_mult.i_multiplier.pc_q} {issue_stage_i.i_scoreboard.mem_q[1].sbe.pc}

get_path_info {ex_stage_i.i_mult.i_multiplier.pc_q} {issue_stage_i.i_scoreboard.mem_q[2].sbe.pc}

get_path_info {ex_stage_i.i_mult.i_multiplier.pc_q} {issue_stage_i.i_scoreboard.mem_q[3].sbe.pc}

get_path_info {ex_stage_i.i_mult.i_multiplier.pc_q} {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.commit_queue_q[0].pc}

get_path_info {ex_stage_i.i_mult.i_multiplier.pc_q} {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.commit_queue_q[1].pc}

get_path_info {ex_stage_i.i_mult.i_multiplier.pc_q} {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.speculative_queue_q[0].pc}

get_path_info {ex_stage_i.i_mult.i_multiplier.pc_q} {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.speculative_queue_q[1].pc}

get_path_info {ex_stage_i.i_mult.i_multiplier.pc_q} {ex_stage_i.lsu_i.i_load_unit.load_data_q.ld_pc}

get_path_info {ex_stage_i.i_mult.i_multiplier.pc_q} {ex_stage_i.lsu_i.i_store_unit.st_pc_q}

get_path_info {ex_stage_i.i_mult.i_multiplier.pc_q} {ex_stage_i.lsu_i.load_pc_o}

get_path_info {ex_stage_i.i_mult.i_multiplier.pc_q} {ex_stage_i.csr_buffer_i.csr_reg_q.pc}

get_path_info {ex_stage_i.i_mult.i_multiplier.pc_q} {ex_stage_i.lsu_i.i_load_unit.lsu_ctrl_i.pc}

get_path_info {ex_stage_i.i_mult.i_multiplier.pc_q} {ex_stage_i.lsu_i.i_ord_sram.pc_i}

get_path_info {ex_stage_i.lsu_i.i_load_unit.lsu_ctrl_i.pc} {ex_stage_i.i_mult.i_div.pc_q}

get_path_info {ex_stage_i.lsu_i.i_load_unit.lsu_ctrl_i.pc} {id_stage_i.issue_q.sbe.pc}

get_path_info {ex_stage_i.lsu_i.i_load_unit.lsu_ctrl_i.pc} {issue_stage_i.i_issue_read_operands.pc_o}

get_path_info {ex_stage_i.lsu_i.i_load_unit.lsu_ctrl_i.pc} {ex_stage_i.lsu_i.lsu_bypass_i.mem_q[0].pc}

get_path_info {ex_stage_i.lsu_i.i_load_unit.lsu_ctrl_i.pc} {ex_stage_i.lsu_i.lsu_bypass_i.mem_q[1].pc}

get_path_info {ex_stage_i.lsu_i.i_load_unit.lsu_ctrl_i.pc} {issue_stage_i.i_scoreboard.mem_q[0].sbe.pc}

get_path_info {ex_stage_i.lsu_i.i_load_unit.lsu_ctrl_i.pc} {issue_stage_i.i_scoreboard.mem_q[1].sbe.pc}

get_path_info {ex_stage_i.lsu_i.i_load_unit.lsu_ctrl_i.pc} {issue_stage_i.i_scoreboard.mem_q[2].sbe.pc}

get_path_info {ex_stage_i.lsu_i.i_load_unit.lsu_ctrl_i.pc} {issue_stage_i.i_scoreboard.mem_q[3].sbe.pc}

get_path_info {ex_stage_i.lsu_i.i_load_unit.lsu_ctrl_i.pc} {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.commit_queue_q[0].pc}

get_path_info {ex_stage_i.lsu_i.i_load_unit.lsu_ctrl_i.pc} {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.commit_queue_q[1].pc}

get_path_info {ex_stage_i.lsu_i.i_load_unit.lsu_ctrl_i.pc} {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.speculative_queue_q[0].pc}

get_path_info {ex_stage_i.lsu_i.i_load_unit.lsu_ctrl_i.pc} {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.speculative_queue_q[1].pc}

get_path_info {ex_stage_i.lsu_i.i_load_unit.lsu_ctrl_i.pc} {ex_stage_i.lsu_i.i_load_unit.load_data_q.ld_pc}

get_path_info {ex_stage_i.lsu_i.i_load_unit.lsu_ctrl_i.pc} {ex_stage_i.lsu_i.i_store_unit.st_pc_q}

get_path_info {ex_stage_i.lsu_i.i_load_unit.lsu_ctrl_i.pc} {ex_stage_i.lsu_i.load_pc_o}

get_path_info {ex_stage_i.lsu_i.i_load_unit.lsu_ctrl_i.pc} {ex_stage_i.csr_buffer_i.csr_reg_q.pc}

get_path_info {ex_stage_i.lsu_i.i_load_unit.lsu_ctrl_i.pc} {ex_stage_i.i_mult.i_multiplier.pc_q}

get_path_info {ex_stage_i.lsu_i.i_load_unit.lsu_ctrl_i.pc} {ex_stage_i.lsu_i.i_load_unit.lsu_ctrl_i.pc}

get_path_info {ex_stage_i.lsu_i.i_load_unit.lsu_ctrl_i.pc} {ex_stage_i.lsu_i.i_ord_sram.pc_i}

get_path_info {ex_stage_i.lsu_i.i_ord_sram.pc_i} {ex_stage_i.i_mult.i_div.pc_q}

get_path_info {ex_stage_i.lsu_i.i_ord_sram.pc_i} {id_stage_i.issue_q.sbe.pc}

get_path_info {ex_stage_i.lsu_i.i_ord_sram.pc_i} {issue_stage_i.i_issue_read_operands.pc_o}

get_path_info {ex_stage_i.lsu_i.i_ord_sram.pc_i} {ex_stage_i.lsu_i.lsu_bypass_i.mem_q[0].pc}

get_path_info {ex_stage_i.lsu_i.i_ord_sram.pc_i} {ex_stage_i.lsu_i.lsu_bypass_i.mem_q[1].pc}

get_path_info {ex_stage_i.lsu_i.i_ord_sram.pc_i} {issue_stage_i.i_scoreboard.mem_q[0].sbe.pc}

get_path_info {ex_stage_i.lsu_i.i_ord_sram.pc_i} {issue_stage_i.i_scoreboard.mem_q[1].sbe.pc}

get_path_info {ex_stage_i.lsu_i.i_ord_sram.pc_i} {issue_stage_i.i_scoreboard.mem_q[2].sbe.pc}

get_path_info {ex_stage_i.lsu_i.i_ord_sram.pc_i} {issue_stage_i.i_scoreboard.mem_q[3].sbe.pc}

get_path_info {ex_stage_i.lsu_i.i_ord_sram.pc_i} {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.commit_queue_q[0].pc}

get_path_info {ex_stage_i.lsu_i.i_ord_sram.pc_i} {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.commit_queue_q[1].pc}

get_path_info {ex_stage_i.lsu_i.i_ord_sram.pc_i} {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.speculative_queue_q[0].pc}

get_path_info {ex_stage_i.lsu_i.i_ord_sram.pc_i} {ex_stage_i.lsu_i.i_store_unit.store_buffer_i.speculative_queue_q[1].pc}

get_path_info {ex_stage_i.lsu_i.i_ord_sram.pc_i} {ex_stage_i.lsu_i.i_load_unit.load_data_q.ld_pc}

get_path_info {ex_stage_i.lsu_i.i_ord_sram.pc_i} {ex_stage_i.lsu_i.i_store_unit.st_pc_q}

get_path_info {ex_stage_i.lsu_i.i_ord_sram.pc_i} {ex_stage_i.lsu_i.load_pc_o}

get_path_info {ex_stage_i.lsu_i.i_ord_sram.pc_i} {ex_stage_i.csr_buffer_i.csr_reg_q.pc}

get_path_info {ex_stage_i.lsu_i.i_ord_sram.pc_i} {ex_stage_i.i_mult.i_multiplier.pc_q}

get_path_info {ex_stage_i.lsu_i.i_ord_sram.pc_i} {ex_stage_i.lsu_i.i_load_unit.lsu_ctrl_i.pc}
set sessiondir [glob synthlc/xGenPerfLocDfgDiv/get_dfg*jgsession*]
set f [file readlink $sessiondir/jg.log]
file copy -force $sessiondir/$f /cafe/u/samanthaarcher/synthlc_tutorial/fava_isca2026/synthlc_optimized/fv/synthlc/xGenPerfLocDfgDiv/get_dfg.tcl.log

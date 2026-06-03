same_queue_pcr = [
("ex_stage_i.i_mult.i_div.pc_q", set(["serdiv_unit_divide_s1", "serdiv_unit_divide_s2"])), 
("issue_stage_i.i_issue_read_operands.pc_o", set(["issue_s1", "issue_s2", "issue_s8", "issue_s16", "issue_s32"])), 
("ex_stage_i.lsu_i.i_store_unit.st_rm_q.pc", set(["store_unit_s1", "store_unit_s3"])),
("ex_stage_i.lsu_i.i_load_unit.lsu_ctrl_i.rm_cnt.pc", set(["load_unit_op_s1",
"load_unit_op_s2", "load_unit_op_s3"])),
]
isomorphic_sets = [
# 0
set(["lsq_enq_0_s1", "lsq_enq_1_s1"]), 
# 1
set(["scb_%d_s12" % i for i in range(4)]),
# 2
set(["scb_%d_s13" % i for i in range(4)]),
# 3
set(["scb_%d_s14" % i for i in range(4)]),
# 4
set(["scb_%d_s8" % i for i in range(4)]),
# 5
set(["stb_com_%d_s1" % i for i in range(2)]),
# 6
set(["stb_spec_%d_s1" % i for i in range(2)]),
########## finals ######
# 7
set(["lsq_enq_0_s1___final", "lsq_enq_1_s1___final"]), 
# 8
set(["scb_0_s12___final", "scb_1_s12___final", "scb_2_s12___final", "scb_3_s12___final"]), 
# 9
set(["scb_0_s13___final", "scb_1_s13___final", "scb_2_s13___final", "scb_3_s13___final"]),
# 10
set(["scb_0_s14___final", "scb_1_s14___final", "scb_2_s14___final", "scb_3_s14___final"]), 
# 11
set(["scb_0_s8___final", "scb_1_s8___final", "scb_2_s8___final", "scb_3_s8___final"]),
# 12
set(["stb_com_0_s1___final", "stb_com_1_s1___final"]),
# 13
set(["stb_spec_0_s1___final", "stb_spec_1_s1___final"]),
]
pl_to_iso_set = {}
# check if one is in cv_perflocs then every other should be
for idx, aset in enumerate(isomorphic_sets):
    for itm in aset:
        pl_to_iso_set[itm] = idx
def transform(pl):
    if pl in pl_to_iso_set:
        return "iso_" + str(pl_to_iso_set[pl])
    else:
        return pl
def transform_iso(isopl):
    if "iso_" in isopl:
        theset = isomorphic_sets[int(isopl.split("iso_")[1])]
        return theset
    else:
        return [isopl]
    
def transform_disjunc(isopl, isi1=False):
    if "iso_" in isopl:
        theset = isomorphic_sets[int(isopl.split("iso_")[1])]
        ret = "("
        for n in sorted(list(theset)):
            if isi1:
                ret += ("i1_" + n + " || ")
            else:
                ret += ("i0_" + n + " || ")

        ret += " 1'b0)"
        return ret
    else:
        if "|" in isopl: 
            ret = "("
            for itm in isopl.split("|"):
                if isi1:
                    ret += ("i1_" + itm + " || ")
                else:
                    ret += ("i0_" + itm + " || ")
            ret += " 1'b0)"
            return ret
        else: 
            if isi1:
                return "i1_" + isopl
            return "i0_" + isopl

def transform_iso_t0(isopl):
    if "iso_" in isopl:
        theset = isomorphic_sets[int(isopl.split("iso_")[1])]
        ret = ""
        for n in sorted(list(theset)):
            if ret != "":
                ret += " ,"
            ret += ("({pl} & {pl}_t0 )".format(pl=n)) #n + "_t0")
        return ret
    else:
        return "(" + isopl + " & " + isopl + "_t0 )"
same_ufsm = [{0}, {1,2,3,4}, {5}, {6}]
# for empty set as follower set 
def transform_iso_t0_neg(isopl, decision_node):
    # if decision node is isomorphic then check the corresponding isomorphic PL's taint
    decision_node_g = -1
    dec_node_set = None
    if "iso_" in decision_node:
        decision_node_g  = int(decision_node.split("iso_")[1])
        dec_node_set = isomorphic_sets[decision_node_g]

    if "iso_" in isopl:
        pl_g = int(isopl.split("iso_")[1])
        theset = isomorphic_sets[pl_g]
        ret = ""
        for itm in same_ufsm:
            if decision_node_g in itm and pl_g in itm:
                for prev, n in zip(sorted(list(dec_node_set)), sorted(list(theset))):
                    if ret != "":
                        ret += " ,"
                    ret += ("($past({prevpl}) & {pl}_t0 )".format(prevpl=prev, pl=n)) 
                return ret
        ret = "" 
        for n in sorted(list(theset)):
            if ret != "":
                ret += " ,"
            ret += ("{pl}_t0 ".format(pl=n)) #n + "_t0")
        return ret
    else:
        return isopl + "_t0"
def transform_iso_t0_neg_inactive(isopl, decision_node):
    pass


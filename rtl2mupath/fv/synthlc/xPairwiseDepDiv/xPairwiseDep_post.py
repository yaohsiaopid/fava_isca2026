##################
# * perfloc implication for DIV
##################
import pandas as pd
from itertools import combinations
import numpy as np
import os
import pandas as pd
import sys
sys.path.append("../../src")
from util import *
from HB_template import *
if len(sys.argv) != 2:
    print("gen/pp")
    exit(0)
HEADERFILE="../header.sv"

h_ = ""
with open(HEADERFILE, "r") as f:
    for line in f:
        h_ += line
#perflocs = get_perflocs(HEADERFILE)
#print("perflocs: ", perflocs)

cv_perflocs = get_array("../xCoverAPerflocDiv/cover_individual.txt")
always_ = get_array("../xCoverAPerflocDiv/always_reach.txt")
perflocs = []
for itm in cv_perflocs:
    if not itm in always_:
        perflocs.append(itm)
#print("power set of ", perflocs)

## Get iid map
iid_map = {}        
pl_signals = {}
with open("../../../xDUVPLs/perfloc_signals.txt", "r") as f:
    for line in f:
        pl, sigs = line[:-1].split(" : ")
        pl_signals[pl] = sigs.split(",")
for k, v in pl_signals.items():
    iid_map[k] = v[0]
# iid_map[pl_name] -> iid

# xCommon proven cases
# PLs for IID_1 are exclusive of PLs for IID_2
exclusive_set_iids = get_array("../../xCommon/exclusive_set_iids.txt", exit_on_fail=False)
# At least one of PLs for IID1 should be in the set if there is at least oen PL
# for IID_2
implication_set_iids = get_array("../../xCommon/implication_iid.txt", exit_on_fail=False)
implication_set_pls = get_array("../../xCommon/implication_pl.txt", exit_on_fail=False)
#edge = get_array("../../xGenPerfLocDfgDiv/dfg_e.txt")

# Isomorphic groups: entries are different indices of the same queue slot design.
# For a pair (pl1, pl2), if pl1 is not the canonical representative of its group,
# and the pair (repr(pl1), pl2) is already being checked, we can skip (pl1, pl2).
_ISO_GROUPS = [
    ["scb_%d_s8"  % i for i in range(8)],
    ["scb_%d_s12" % i for i in range(8)],
    ["scb_%d_s13" % i for i in range(8)],
    ["scb_%d_s14" % i for i in range(8)],
    ["stb_com_%d_s1"  % i for i in range(4)],
    ["stb_spec_%d_s1" % i for i in range(4)],
]
# Map each perfloc to its canonical representative (first in the group)
_iso_repr = {}
_iso_group_of = {}  # pl -> full group list
for grp in _ISO_GROUPS:
    for pl in grp:
        _iso_repr[pl] = grp[0]
        _iso_group_of[pl] = grp

def iso_repr(pl):
    return _iso_repr.get(pl, pl)

def iso_skip(pl1, pl2, perfloc_set):
    """Return True if (pl1, pl2) is redundant because (repr(pl1), pl2) covers it."""
    r1 = iso_repr(pl1)
    return r1 != pl1 and r1 in perfloc_set

def iso_skip_pl2(pl2, perfloc_set):
    """Return True if pl2 is non-canonical and its canonical representative is in perfloc_set."""
    r2 = iso_repr(pl2)
    return r2 != pl2 and r2 in perfloc_set

def iso_group_members_in_set(pl, perfloc_set):
    """Return the group members of pl that are present in perfloc_set, or [pl] if not in any group."""
    grp = _iso_group_of.get(pl)
    if grp is None:
        return [pl]
    return [m for m in grp if m in perfloc_set]

def hpn_reg_iso(pl, perfloc_set):
    """Generate hpn_reg always block for pl, using OR over its iso group members in perfloc_set."""
    members = iso_group_members_in_set(pl, perfloc_set)
    condition = " || ".join(members)
    return (
        "\nreg {pl}_hpn;\n"
        "always @(posedge clk_i) begin\n"
        "    if (!rst_ni)\n"
        "        {pl}_hpn <= 1'b0;\n"
        "    else if ({condition})\n"
        "        {pl}_hpn <= 1'b1;\n"
        "end\n"
    ).format(pl=pl, condition=condition)

#print(exclusive_set_iids)
cnt_reachable_pls_iid = {}
for itm in cv_perflocs:
    iid = iid_map[itm]
    if not iid in cnt_reachable_pls_iid:
        cnt_reachable_pls_iid[iid] = 0
    cnt_reachable_pls_iid[iid] += 1 
print(cnt_reachable_pls_iid)
def dom(pc1, pc2):
    cnt1 = cnt_reachable_pls_iid[pc1]
    if cnt1 == 1:
        return ([pc1, pc2] in implication_set_iids)
    else:
        return False


def gen():
    print("========== gen ====================")
    if not os.path.isdir("out"):
        os.mkdir("out")
    print(len(perflocs))
    log_skip = open("pairwise_common.txt", "w")
    properties = ""
    cnt = 0
    todolog = open("todo.log", "w")
    perfloc_set = set(perflocs)
    for idx in range(len(perflocs)):
        for idx2 in range(len(perflocs)):
            if idx != idx2:
                pc_1 = iid_map[perflocs[idx]]
                pc_2 = iid_map[perflocs[idx2]]
                #print(perflocs[idx], perflocs[idx2])
                exclusive_already = False
                if  [pc_1, pc_2] in exclusive_set_iids or \
                    [pc_2, pc_1] in exclusive_set_iids:
                    print("exclusive,%s,%s" % (perflocs[idx], perflocs[idx2]),
                            file=log_skip)
                    exclusive_already = True

                if dom(pc_1, pc_2):
                    print("impl,%s,%s" % (perflocs[idx], perflocs[idx2]),
                            file=log_skip)
                    assert (not exclusive_already)
                elif [perflocs[idx], perflocs[idx2]] in implication_set_pls:
                    print("impl_pl,%s,%s" % (perflocs[idx], perflocs[idx2]),
                            file=log_skip)
                    assert (not exclusive_already)
                elif not exclusive_already:
                    if iso_skip(perflocs[idx], perflocs[idx2], perfloc_set):
                        print("iso_skip,%s,%s" % (perflocs[idx], perflocs[idx2]),
                                file=log_skip)
                    elif iso_skip_pl2(perflocs[idx2], perfloc_set):
                        print("iso_skip,%s,%s" % (perflocs[idx], perflocs[idx2]),
                                file=log_skip)
                    else:
                        ff_ = "out/nunv_anytwo_%d.sv" % cnt
                        print("imp,%s,%s,%d" % (perflocs[idx], perflocs[idx2],cnt), file=todolog)
                        with open (ff_, "w") as f:
                            f.write(h_)
                            f.write(hpn_reg_t2.format(s1 = perflocs[idx]))
                            f.write(hpn_reg_iso(perflocs[idx2], perfloc_set))
                            f.write(pair_dep_t2.format(
                                s1 = perflocs[idx], s2 = perflocs[idx2], cnt=cnt))


                #([pc_1, pc_2] in implication_set_iids) or \
                #([pc_2, pc_1] in implication_set_iids) or \
                imp_already = dom(pc_1, pc_2) or \
                    dom(pc_2, pc_1) or \
                    ([perflocs[idx2], perflocs[idx]] in implication_set_pls) or \
                    ([perflocs[idx], perflocs[idx2]] in implication_set_pls)
                iso_already = iso_skip(perflocs[idx], perflocs[idx2], perfloc_set) or \
                    iso_skip(perflocs[idx2], perflocs[idx], perfloc_set)
                if idx < idx2 and (not exclusive_already) and (not imp_already) and (not iso_already):
                    print("excl,%s,%s,%d" % (perflocs[idx], perflocs[idx2],cnt), file=todolog)
                    ff_ = "out/exclusive_%d.sv" % cnt
                    with open(ff_, "w") as f:
                        f.write(h_)
                        f.write(hpn_reg_t2.format(s1 = perflocs[idx]))
                        f.write(hpn_reg_t2.format(s1 = perflocs[idx2]))
                        f.write(c_two_pl_t.format(
                            s1 = perflocs[idx], s2 = perflocs[idx2], cnt=cnt))
                cnt += 1
    
    log_skip.close()
    todolog.close()

def pp():
    print("========== pp ====================")
    log_skip = get_array("pairwise_common.txt") 
    dep_in_log = []
    excl_in_log = []
    for itm in log_skip:
        t, u, v = itm
        if "impl" in t:
            dep_in_log.append((u, v))
        elif t == "iso_skip":
            pass  # handled via expand_iso_pairs in the todo loop
        else:
            excl_in_log.append((u, v))

    exclu = []
    dep = []

    undetermined_exclu = []
    undetermined_dep = []

    comps = []
    incomps = []

    perfloc_set = set(perflocs)

    def expand_iso_pairs(pl1, pl2):
        """Expand (pl1, pl2) to all isomorphic variants present in perfloc_set."""
        pl1_members = iso_group_members_in_set(iso_repr(pl1), perfloc_set)
        pl2_members = iso_group_members_in_set(iso_repr(pl2), perfloc_set)
        return [(m1, m2) for m1 in pl1_members for m2 in pl2_members if m1 != m2 or pl1 == pl2]

    todo_items = get_array("todo.log")
    for itm in todo_items:
        prop, pl1, pl2, cnt = itm
        if prop == "excl":
            ff, prop = "./exclusive_%s.csv" % cnt, 'C_%s' % cnt
            assert(os.path.exists(ff))
            df = pd.read_csv(ff, dtype=mydtypes)
            res, bnd, time = df_query(df, prop)
            if res == "unreachable":
                for m1, m2 in expand_iso_pairs(pl1, pl2):
                    exclu.append((m1, m2))
            elif res == 'undetermined':
                for m1, m2 in expand_iso_pairs(pl1, pl2):
                    undetermined_exclu.append((m1, m2))

            if res in ["covered", "unreachable", "cex", "proven"]:
                comps.append(time)
            else:
                incomps.append((time, bnd))

        else:
            ff, prop = "./nunv_anytwo_%s.csv" % cnt, 'DEP_%s_b' % cnt
            assert(os.path.exists(ff))
            df = pd.read_csv(ff, dtype=mydtypes)
            res, bnd, time = df_query(df, prop)
            if res == "unreachable":
                dep.append((pl1, pl2))
                #for m1, m2 in expand_iso_pairs(pl1, pl2):
                #    dep.append((m1, m2))
            elif res == 'undetermined':
                undetermined_dep.append((pl1, pl2))
                # for m1, m2 in expand_iso_pairs(pl1, pl2):
                #     undetermined_dep.append((m1, m2))

            if res in ["covered", "unreachable", "cex", "proven"]:
                comps.append(time)
            else:
                incomps.append((time, bnd))

    with open("implication.txt", "w") as f:
        for itm in dep + dep_in_log:
            f.write(",".join(itm) + "\n")

    with open("undetermined_impl.txt", "w") as f:
        for itm in undetermined_dep:
            f.write("%s,%s\n" % (itm[0], itm[1]))


    with open("exclusive.txt", "w") as f:
        for itm in exclu + excl_in_log:
            f.write(",".join(itm) + "\n")

    with open("undetermined_excl.txt", "w") as f:
        for itm in undetermined_exclu:
            f.write("%s,%s\n" % (itm[0], itm[1]))

    with open("stats.txt", "w") as f:
        f.write("%d,%f\n" % (len(comps), sum(comps)))
        for itm in comps:
            f.write("%f," % itm)
        f.write("\n")
        t = sum([r[0] for r in incomps])
        f.write("%d,%f\n" % (len(incomps), t))
        for itm in incomps:
            f.write("%f," % itm[0])
        f.write("\n")
        for itm in incomps:
            f.write("%d," % itm[1])
        f.write("\n")


def stats():
    print("========== stats ====================")
    pp()
    #comps = []
    #incomps = []

    ## nunv_anytwo
    #cnt = 0
    #for idx in range(len(perflocs)):
    #    for idx2 in range(len(perflocs)):
    #        if idx != idx2:
    #            pc_1 = iid_map[perflocs[idx]]
    #            pc_2 = iid_map[perflocs[idx2]]
    #            #print(perflocs[idx], perflocs[idx2])
    #            exclusive_already = False
    #            if  [pc_1, pc_2] in exclusive_set_iids or \
    #                [pc_2, pc_1] in exclusive_set_iids:
    #                exclusive_already = True

    #            if [pc_1, pc_2] in implication_set_iids:
    #                pass
    #            elif [perflocs[idx], perflocs[idx2]] in implication_set_pls: 
    #                pass
    #            elif not exclusive_already: #if [perflocs[idx], perflocs[idx2]] in edge: 
    #                df = pd.read_csv("./nunv_anytwo_%d.csv" % cnt, dtype=mydtypes)
    #                res, bnd, time = df_query(df, 'DEP_%d_b' % cnt)
    #                if res in ["covered", "unreachable", "cex", "proven"]:
    #                    comps.append(time)
    #                else:
    #                    incomps.append((time, bnd))
    #            cnt += 1
    #cnt = 0
    #for idx in range(len(perflocs)):
    #    for idx2 in range(len(perflocs)):
    #        if idx != idx2 :
    #            pc_1 = iid_map[perflocs[idx]]
    #            pc_2 = iid_map[perflocs[idx2]]
    #            exclusive_already = False
    #            if  [pc_1, pc_2] in exclusive_set_iids or \
    #                [pc_2, pc_1] in exclusive_set_iids:
    #                #print("skip %s %s check" % (perflocs[idx], perflocs[idx2]))
    #                exclusive_already = True
    #            imp_already = ([pc_1, pc_2] in implication_set_iids) or \
    #                ([pc_2, pc_1] in implication_set_iids) or \
    #                ([perflocs[idx2], perflocs[idx]] in implication_set_pls) or \
    #                ([perflocs[idx], perflocs[idx2]] in implication_set_pls)
    #            if idx < idx2 and (not exclusive_already) and (not imp_already):
    #            #if idx < idx2:
    #                df = pd.read_csv("./exclusive_%d.csv" % cnt, dtype=mydtypes)
    #                res, bnd, time = df_query(df, 'C_%d' % cnt)
    #                if res in ["covered", "unreachable", "cex", "proven"]:
    #                    comps.append(time)
    #                else:
    #                    incomps.append((time, bnd))
    #            cnt += 1

    #with open("stats.txt", "w") as f:
    #    f.write("%d,%f\n" % (len(comps), sum(comps)))
    #    for itm in comps:
    #        f.write("%f," % itm)
    #    f.write("\n")
    #    t = sum([r[0] for r in incomps])
    #    f.write("%d,%f\n" % (len(incomps), t))
    #    for itm in incomps:
    #        f.write("%f," % itm[0])
    #    f.write("\n")
    #    for itm in incomps:
    #        f.write("%d," % itm[1])
    #    f.write("\n")

if len(sys.argv) != 2:
    print("gen/pp")
    exit(0)

opt = sys.argv[1]
if opt == "gen":
    gen()
elif opt == "pp":
    pp()
elif opt == "stats":
    stats()

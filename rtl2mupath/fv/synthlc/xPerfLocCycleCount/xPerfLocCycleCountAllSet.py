# 1. for all reachable nodes run max cycle **in no specific sets**
# 2. for nodes with greater than 1 max cycle specialize? 

import networkx as nx
import re
from itertools import chain, combinations
import pandas as pd
import numpy as np
import os
import pandas as pd
import sys
sys.path.append("../../src")
from util import *
from HB_template import *


cv_perflocs = get_array("../xCoverAPerflocDiv/cover_individual.txt")
reachable_sets = get_array("../xPerfLocSubsetDiv/reachable_set.txt", arr_as_ele = True)

_ISO_GROUPS = [
    ["scb_%d_s8"  % i for i in range(8)],
    ["scb_%d_s12" % i for i in range(8)],
    ["scb_%d_s13" % i for i in range(8)],
    ["scb_%d_s14" % i for i in range(8)],
    ["stb_com_%d_s1"  % i for i in range(4)],
    ["stb_spec_%d_s1" % i for i in range(4)],
]
_iso_repr = {}
_iso_group_of = {}
for _grp in _ISO_GROUPS:
    for _pl in _grp:
        _iso_repr[_pl] = _grp[0]
        _iso_group_of[_pl] = _grp

def iso_repr(pl):
    return _iso_repr.get(pl, pl)

cv_perflocs_set = set(cv_perflocs)

def is_non_canonical(pl):
    return iso_repr(pl) != pl and iso_repr(pl) in cv_perflocs_set

def iso_group_members_in_set(pl):
    grp = _iso_group_of.get(iso_repr(pl))
    if grp is None:
        return [pl]
    return [m for m in grp if m in cv_perflocs_set]

def hpn_reg_iso(pl):
    members = iso_group_members_in_set(pl)
    condition = " || ".join(members)
    return (
        "\nreg {pl}_hpn;\n"
        "always @(posedge clk_i) begin\n"
        "    if (!rst_ni)\n"
        "        {pl}_hpn <= 1'b0;\n"
        "    else if ({cond})\n"
        "        {pl}_hpn <= 1'b1;\n"
        "end\n"
    ).format(pl=iso_repr(pl), cond=condition)
#interference = False
#cwd = os.getcwd()
#if "III" in cwd:
#    print("interference case")
#    interference = True

interference = True
HEADERFILE="../header.sv"
h_ = ""
with open(HEADERFILE, "r") as f:
    for line in f:
        h_ += line

def gen():
    if not os.path.isdir("out"):
        print("creating dir out")
        os.mkdir("out")

    t_ = ''
    with open("template.tcl", "r") as f:
        for line in f:
            t_ += line.replace("CLK", GLBCLK)

    for itm in cv_perflocs:
        if is_non_canonical(itm):
            continue
        with open("out/cycle_count_%s.tcl" % (itm), "w") as f:
            fnm = os.getcwd() + "/max_cycle_count_%s.csv" % (itm)
            f.write(t_ % (itm, fnm))
        with open("out/cycle_count_%s.sv" % (itm), "w") as f:
            f.write(h_)

def proc(fnm, itm):
    print("-->", fnm)
    """Return (cyc_gt1, max_cyc_covered) where cyc_gt1 is 2 if sig can stay high
    at least 2 cycles (consec_{itm}_2 covered), else 1; max_cyc_covered same value."""
    if not os.path.exists(fnm):
        assert(0)
        return None
    csv_ = pd.read_csv(fnm)
    rows = csv_[csv_['Name'].str.contains('consec_%s_2' % itm)]
    if rows.empty:
        print("empty")
        assert(0)
        return None
    res = rows['Result'].values[0]
    if res == 'covered':
        return (2, 2)
    else:
        return (1, 1)

def gen_s2():
    if not os.path.isdir("out"):
        print("creating dir out")
        os.mkdir("out")

    for itm in cv_perflocs:
        if is_non_canonical(itm):
            continue
        with open("out/cycle_count_%s.sv" % itm, "w") as f:
            f.write(h_)
            f.write("\nconsec_%s_2: cover property (@(posedge clk_i) %s ##1 %s);\n" % (itm, itm, itm))

def gen_s2_perset():
    if not os.path.isdir("out2"):
        print("creating dir out2")
        os.mkdir("out2")

    max_cyc_perloc = []
    max_cyc_perloc_covered = []

    for itm in cv_perflocs:
        if is_non_canonical(itm):
            continue
        fnm = os.getcwd() + "/cycle_count_%s.csv" % (itm)
        cyc, max_cyc_covered = proc(fnm, itm)
        max_cyc_perloc_covered.append((itm, max_cyc_covered))
        if cyc is not None:
            max_cyc_perloc.append((itm, cyc))
            if cyc <= 1:
                continue

            # for each reachable set try see if the performing location can be
            # longer than one cycle
            for set_idx, aSet in enumerate(reachable_sets):
                if not itm in aSet:
                    continue

                with open("out2/over1cyc_%d_%s.sv" % (set_idx, itm), "w") as f:
                    f.write(h_)
                    s = ""
                    ors_ = ""
                    emitted_hpn = set()
                    for pl in cv_perflocs:
                        if not pl in aSet:
                            f.write(no_s1_t.format(s1=pl))
                        else:
                            canon = iso_repr(pl)
                            if canon not in emitted_hpn:
                                emitted_hpn.add(canon)
                                f.write(hpn_reg_iso(pl))
                                s += "{s1}_hpn && ".format(s1=canon)
                            ors_ += "{s1} | ".format(s1=pl)
                    s += "1'b1"
                    ors_ += "1'b0"
                    f.write(assume_path.format(s=s))
                    # f.write(CS_prop_gt.format(itm=itm, cnt=2, s=s))
                    f.write("CS_gt_{itm}_2: cover property (@(posedge clk_i) {itm} [*{cnt}] ##1 !{itm} ##[0:$] ({s} & !({ors}))); ".format(itm=itm, cnt=2,s=s,ors=ors_))
                    # f.write("\nCS_gt_%s_2: cover property (@(posedge clk_i) %s ##1 %s && %s & !(%s));\n" % (itm, itm, itm, s, ors_))

    with open("max_cycle_per_pl.txt", "w") as f:
        for itm in max_cyc_perloc:
            f.write("%s,%d\n" % itm)

    with open("max_cycle_per_pl_covered.txt", "w") as f:
        for itm in max_cyc_perloc_covered:
            f.write("%s,%d\n" % itm)

def pp():
    max_cyc_perloc = get_array("max_cycle_per_pl.txt")
    pl_cyc = {}
    for itm in max_cyc_perloc:
        pl_cyc[itm[0]] = int(itm[1])
    result = [] # (itm,cyc_that_covered,...)
    undetermined_result = []
    # itm, cyc, res
    for itm in cv_perflocs:
        if is_non_canonical(itm):
            continue
        if pl_cyc[itm] == 1:
            continue

        for set_idx, aSet in enumerate(reachable_sets):
            if not itm in aSet:
                continue

            fnm = os.getcwd() + "/over1cyc_%d_%s.csv" % (set_idx, itm)
            check_file(fnm)
            df = pd.read_csv(fnm, dtype=mydtypes)
            res, bnd, time = df_query(df, "CS_gt_%s_%d" % (itm, 2))
            if res == "unreachable":
                result.append((set_idx, itm, 0))
            else:
                result.append((set_idx, itm, 1))

    with open("cycle_count_gt1_perset.txt", "w") as f:
        for itm in result:
            f.write("%d,%s,%d\n" % itm)

def stats():
    max_cyc_perloc = get_array("max_cycle_per_pl.txt")
    pl_cyc = {}
    for itm in max_cyc_perloc:
        pl_cyc[itm[0]] = int(itm[1])

    comps = []
    incomps = []
    for itm in cv_perflocs:
        if is_non_canonical(itm):
            continue
        if pl_cyc[itm] == 1:
            continue

        for set_idx, aSet in enumerate(reachable_sets):
            if not itm in aSet:
                continue

            fnm = os.getcwd() + "/over1cyc_%d_%s.csv" % (set_idx, itm)
            check_file(fnm)
            df = pd.read_csv(fnm, dtype=mydtypes)
            df = df[df['Name'].str.contains("CS_gt_%s_%d" % (itm, 2))]
            for r_, time in zip(list(df['Result'].values), list(df['Time'].values)):
                t_ = float(time[:-2])
                if r_ in ["covered", "unreachable", "cex", "proven"]:
                    comps.append(t_)
                else:
                    incomps.append((t_, -1))

        #     res, bnd, time = df_query(df, "CS_gt_%s_%d" % (itm, 2))
        #     if res == "unreachable":
        #         result.append((set_idx, itm, 0))
        #     else:
        #         result.append((set_idx, itm, 1))

        # fnm = os.getcwd() + "/max_cycle_count_%s.csv" % (itm)
        # df = pd.read_csv(fnm, dtype=mydtypes)
        # df = df[df['Name'].str.contains('consec_%s' % itm)]
        # for r_, time in zip(list(df['Result'].values), list(df['Time'].values)):
        #     t_ = float(time[:-2])
        #     if r_ in ["covered", "unreachable", "cex", "proven"]:
        #         comps.append(t_)
        #     else:
        #         incomps.append((t_, -1))

        #if pl_cyc[itm] != 1:
        #    for set_idx, aSet in enumerate(reachable_sets):
        #        if not itm in aSet:
        #            continue
        #        #fnm = os.getcwd() + "/over1cyc_%d_%s.csv" % (set_idx, itm)
        #        #df = pd.read_csv(fnm, dtype=mydtypes)
        #        #res, bnd, time = df_query(df, "CS_gt_%s_%d" % (itm, 2))
        #        #if res in ["covered", "unreachable", "cex", "proven"]:
        #        #    comps.append(time)
        #        #else:
        #        #    incomps.append((time, bnd))


        #fnm = os.getcwd() + "/max_cycle_count_%s.csv" % (itm)
        #df = pd.read_csv(fnm, dtype=mydtypes)

        #for idx, tar_row in df[df['Name'].str.contains("consec_%s" % itm)].iterrows():
        #    res = tar_row['Result']
        #    bnd = tar_row['Bound']
        #    sr = re.search("([0-9]+)", bnd)
        #    if sr is not None:
        #        bnd = int(sr.group(1))
        #    else:
        #        bnd = None
        #    time = float(tar_row['Time'][:-2])
        #    if res in ["covered", "unreachable", "cex", "proven"]:
        #        comps.append(time)
        #    else:
        #        incomps.append((time, bnd))

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


if len(sys.argv) != 2:
    print("gen/gen_s2/pp")
    exit(0)

opt = sys.argv[1]
if opt == "gen":
    gen()
elif opt == "gen_s2":
    gen_s2()
elif opt == "gen_s2_perset":
    gen_s2_perset()
elif opt == "pp":
    pp()
elif opt == "stats":
    stats()

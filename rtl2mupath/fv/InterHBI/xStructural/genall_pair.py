# Goal: temporal structural dependencies
# - a)
# - Either same PL
# - Or PLs share the same queue -> there must be some order as the queue may not
# be that concurrent 
# - b) Entering or leaving the PL

import re
import networkx as nx
from itertools import chain, combinations
import pandas as pd
import numpy as np
import os
import pandas as pd
import sys
# sys.path.append("../src")
from util import *
from gconst import *
# from HB_template import *

cmt = True
i0_cmt = "|".join([f"i0_scb_{i}_s13" for i in range(4)])
i1_cmt = "|".join([f"i1_scb_{i}_s13" for i in range(4)])
instns = ["LW", "SW", "FENCE"]
instns_h = {}
i_fnm = "../../synthlc/opcodes_gen_all/%s.sv"
for i in instns:
    tmp_h = ""
    with open(i_fnm % i, "r") as f:
        for l in f:
            tmp_h += l
    instns_h[i] = tmp_h

#    assume (i0 - po -> i1)
HEADERFILE='../header_interhbi.sv'
h_ = ""
with open(HEADERFILE, "r") as f:
    for line in f:
        h_ += line
pth = os.path.abspath(os.path.join(os.getcwd(), '../'))
h_ += f"`include \"{pth}/i0_pl.sv\" \n"
h_ += f"`include \"{pth}/i1_pl.sv\" \n"
i_top_dir = "../../synthlc/i_{instn}_out/xCoverAPerflocDiv"

#reahcable -> iso_pl 
if len(sys.argv) != 2:
    print("gen/pp")
    exit(0)

def pp():
    logfile = open("meta.txt", "r")
    arr = []
    proven = []
    undet = [] 
    resf_f = open("res.txt", "w")
    comps = []
    incomps = []
    for ln in logfile:
        arr.append(ln[:-1].split(","))
    for itm in arr:
        ff = "./gen/{i0}_{i1}/HB_{idx}.csv".format(i0 = itm[0], i1 = itm[1], idx = itm[2])
        df = pd.read_csv(ff, dtype=mydtypes)
        prop = "HB_{cnt}".format(cnt = itm[2])
        res, bnd, time = df_query(df, prop)
        if res == "proven":
            proven.append(itm)
        elif res == 'undetermined':
            undet.append(itm)
        else:
            # cex
            pass 
            ff = "./gen/{i0}_{i1}/out/HB_{idx}.sv".format(i0 = itm[0], i1 = itm[1], idx = itm[2])
            outff = "./gen/{i0}_{i1}/out/WHB_{idx}.sv".format(i0 = itm[0], i1 = itm[1], idx = itm[2])
            os.system('echo "\`define WHB" > {outff}'.format(outff = outff))
            os.system("cat {ff} >> {outff}".format(ff = ff, outff = outff))


        if res in ["covered", "unreachable", "cex", "proven"]:
            comps.append(time)
        else:
            incomps.append((time, bnd))
        if len(itm[3:]) == 1:
            p = itm[0:3] + [transform_disjunc(r) for r in itm[3:]] * 2 
        else:
            p = itm[0:3] + [transform_disjunc(r) for r in itm[3:]] 
        ss_ = ",".join(p) + "," + res + "\n"
        if not "s14" in ss_:
            resf_f.write(ss_)
        #print(comps)

    arr = [("../LW_mem_SW_mem/HB_6.csv", "HB_6") ,("../sw_lw_mem/same_addr_dep.csv", "HB_6")
        ,("../FENCE_scb_commit_LW_mem_req_COMMITTED_LW/FENCE_scb_commit_LW_mem_req_COMMITTED_LW.csv", "CON_HB_4") ,("../sw_mem_fence_scb_commit/sw_mem_fence_scb_commit.csv", "HB_0")]
    for itm in arr:
        ff = itm[0]
        df = pd.read_csv(ff, dtype=mydtypes)
        prop = itm[1]
        res, bnd, time = df_query(df, prop)
        if res in ["covered", "unreachable", "cex", "proven"]:
            comps.append(time)
        else:
            incomps.append((time, bnd))

    print("--> completes", len(comps), np.mean(comps))
    print("--> incompletes", len(incomps), np.mean(incomps))


    resf_f.close()
def gen_s2():
    logfile = open("meta.txt", "r")
    arr = []
    proven = []
    undet = [] 

    comps = []
    incomps = []
    for ln in logfile:
        arr.append(ln[:-1].split(","))
    for itm in arr:
        ff = "./gen/{i0}_{i1}/HB_{idx}.csv".format(i0 = itm[0], i1 = itm[1], idx = itm[2])
        df = pd.read_csv(ff, dtype=mydtypes)
        prop = "HB_{cnt}".format(cnt = itm[2])
        res, bnd, time = df_query(df, prop)
        if res == "proven":
            proven.append(itm)
        elif res == 'undetermined':
            undet.append(itm)
        else:
            # cex
            ff = "./gen/{i0}_{i1}/out/HB_{idx}.sv".format(i0 = itm[0], i1 = itm[1], idx = itm[2])
            outff = "./gen/{i0}_{i1}/out/WHB_{idx}.sv".format(i0 = itm[0], i1 = itm[1], idx = itm[2])
            os.system('echo "\`define WHB" > {outff}'.format(outff = outff))
            os.system("cat {ff} >> {outff}".format(ff = ff, outff = outff))


        if res in ["covered", "unreachable", "cex", "proven"]:
            comps.append(time)
        else:
            incomps.append((time, bnd))
        if len(itm[3:]) == 1:
            p = itm[0:3] + [transform_disjunc(r) for r in itm[3:]] * 2 
        else:
            p = itm[0:3] + [transform_disjunc(r) for r in itm[3:]] 
        print(",".join(p), ",", res)


def gen():
    for i0 in instns:
        for i1 in instns:
            sub_path = i_top_dir + "/cover_individual.txt"

            reachable_pl_i0 = get_array(sub_path.format(instn = i0), exit_on_fail = False)

            reachable_pl_i1 = get_array(sub_path.format(instn = i1), exit_on_fail = False)

            print(i0, i1)
            assert(len(reachable_pl_i0) > 0)
            assert(len(reachable_pl_i1) > 0)
            set_inter = set(reachable_pl_i0)
            set_inter = set_inter & set(reachable_pl_i1)
            set_inter_iso = set()
            for itm in sorted(set_inter):
                set_inter_iso.add(transform(itm))
            print(set_inter_iso)
            #set_inter = iso_pl(set_inter)
            
            logfile = open("meta.txt", "a+")
            idx = 0
            for itm in same_queue_pcr:
                if itm[1] & set_inter_iso:
                    logfile.write("%s,%s,%d,%s\n" % (i0, i1, idx, "|".join(itm[1])))
                    ffname = "gen/{i0}_{i1}/out/HB_{idx}.sv".format(i0=i0, i1=i1, idx=idx)
                    dirname = os.path.dirname(ffname)
                    if dirname:
                        os.makedirs(dirname, exist_ok = True)
                    with open(ffname, "w") as f:
                        f.write(h_)
                        f.write(instns_h[i0])
                        f.write(instns_h[i1].replace("i0", "i1").replace("i_", "i1_"))
                        # i0_at_pl
                        f.write("wire e0 = ({pcr} == pc0); \n".format(pcr=itm[0]))
                        f.write("wire e1 = ({pcr} == pc1); \n".format(pcr=itm[0]))
                        f.write(hpn_reg_t.format(s1 = "e0", s2 = "e1"))
                        if not cmt: 
                          f.write(ENTER_A_HP_ENTER_B_t.format(s1 = "e0", s2 = "e1", cnt = idx))
                        else:
                          f.write(CMT_ENTER_A_HP_ENTER_B_t.format(i0_cmt = i0_cmt, i1_cmt = i1_cmt, s1 = "e0", s2 = "e1", cnt = idx))
                    idx += 1

            for pl in (sorted(set_inter_iso)):
                in_same_pcr = False
                for itm in same_queue_pcr:
                    if pl in itm[1]:
                        in_same_pcr = True
                if in_same_pcr:
                    continue

                logfile.write("%s,%s,%d,%s\n" % (i0, i1, idx, pl))
                ffname = "gen/{i0}_{i1}/out/HB_{idx}.sv".format(i0=i0, i1=i1, idx=idx)
                dirname = os.path.dirname(ffname)
                if dirname:
                    os.makedirs(dirname, exist_ok = True)
                with open(ffname, "w") as f:
                    f.write(h_)
                    f.write(instns_h[i0])
                    f.write(instns_h[i1].replace("i0", "i1").replace("i_", "i1_"))
                    # i0_at_pl
                    f.write("wire e0 = " + transform_disjunc(pl) + " ; \n")
                    f.write("wire e1 = " + transform_disjunc(pl, True) + " ; \n")
                    f.write(hpn_reg_t.format(s1 = "e0", s2 = "e1"))
                    if not cmt: 
                      f.write(ENTER_A_HP_ENTER_B_t.format(s1 = "e0", s2 = "e1", cnt = idx))
                    else: 
                      f.write(CMT_ENTER_A_HP_ENTER_B_t.format(i0_cmt = i0_cmt, i1_cmt = i1_cmt, s1 = "e0", s2 = "e1", cnt = idx))
                idx += 1

            # temporal
            for pl1 in ["mem_req_s1", "mem_req_lw_s1"]:
              for pl2 in ["mem_req_s1", "mem_req_lw_s1"]:
                if pl1 == pl2 or  (pl1 not in  reachable_pl_i0) or (pl2 not in reachable_pl_i1):
                  continue
                logfile.write("%s,%s,%d,%s,%s\n" % (i0, i1, idx, pl1, pl2))
                ffname = "gen/{i0}_{i1}/out/HB_{idx}.sv".format(i0=i0, i1=i1, idx=idx)
                dirname = os.path.dirname(ffname)
                if dirname:
                    os.makedirs(dirname, exist_ok = True)
                with open(ffname, "w") as f:
                    f.write(h_)
                    f.write(instns_h[i0])
                    f.write(instns_h[i1].replace("i0", "i1").replace("i_", "i1_"))
                    # i0_at_pl
                    f.write("wire e0 = " + transform_disjunc(pl1) + " ; \n")
                    f.write("wire e1 = " + transform_disjunc(pl2, True) + " ; \n")
                    f.write(hpn_reg_t.format(s1 = "e0", s2 = "e1"))
                    if not cmt: 
                      f.write(ENTER_A_HP_ENTER_B_t.format(s1 = "e0", s2 = "e1", cnt = idx))
                    else:
                      f.write(CMT_ENTER_A_HP_ENTER_B_t.format(i0_cmt = i0_cmt, i1_cmt = i1_cmt, s1 = "e0", s2 = "e1", cnt = idx))
                idx += 1


            for pl1 in (sorted(set_inter_iso)):
                for pl2 in (sorted(set_inter_iso)):
                    if pl1 == pl2:
                        continue

                    # check if its the same queue structure
                    # different state of the scb 
                    print(pl1, pl2)
                    in_same_pcr = False
                    for itm in same_queue_pcr:
                        if pl1 in itm[1] and pl2 in itm[1]:
                            in_same_pcr = True
                    if (not in_same_pcr) and \
                    (pl1 in ["iso_1", "iso_2", "iso_3", "iso_4"] \
                    and pl2 in ["iso_1", "iso_2", "iso_3", "iso_4"]):
                        logfile.write("%s,%s,%d,%s,%s\n" % (i0, i1, idx, pl1, pl2))
                        ffname = "gen/{i0}_{i1}/out/HB_{idx}.sv".format(i0=i0, i1=i1, idx=idx)
                        dirname = os.path.dirname(ffname)
                        if dirname:
                            os.makedirs(dirname, exist_ok = True)
                        with open(ffname, "w") as f:
                            f.write(h_)
                            f.write(instns_h[i0])
                            f.write(instns_h[i1].replace("i0", "i1").replace("i_", "i1_"))
                            # i0_at_pl
                            f.write("wire e0 = " + transform_disjunc(pl1) + " ; \n")
                            f.write("wire e1 = " + transform_disjunc(pl2, True) + " ; \n")
                            f.write(hpn_reg_t.format(s1 = "e0", s2 = "e1"))
                            if not cmt: 
                              f.write(ENTER_A_HP_ENTER_B_t.format(s1 = "e0", s2 = "e1", cnt = idx))
                            else:
                              f.write(CMT_ENTER_A_HP_ENTER_B_t.format(i0_cmt = i0_cmt, i1_cmt = i1_cmt, s1 = "e0", s2 = "e1", cnt = idx))
                        idx += 1

            logfile.close()

            
            #    assert ((i0, pl), (i1, pl))
opt = sys.argv[1]
if opt == "gen":
    print("rm -rf gen && rm meta.txt")
    gen()
elif opt == "gen_s2":
    gen_s2()
elif opt == "pp":
    pp()
        

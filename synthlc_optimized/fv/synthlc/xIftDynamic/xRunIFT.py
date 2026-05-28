import ast
import json
import re
import networkx as nx
from itertools import chain, combinations
import pandas as pd
import numpy as np
import os
import pandas as pd
import sys
sys.path.append("../../src")
from util import *
from HB_template import *
sys.path.append("../../src_ift_utils")
from IFT_template import *


HEADERFILE='../header.sv'
with open(HEADERFILE, "r") as f:
    lines = f.readlines()
# Replace the SPV transmitter define with the IFT T_FROM_IUV define + RS1 taint operand
#h_ = "".join(lines).replace("`define INTRA_TRANSMITTER", "`define T_FROM_IUV\n`define RS1")
h_ = ""
e_ = ""


HEADERTCL="../../../src_ift/jg2.tcl"
htcl_ = ""
with open(HEADERTCL, "r") as f:
    for line in f:
        htcl_ += line


cv_perflocs = get_array("../xCoverAPerflocDiv/cover_individual.txt")


try:
    with open("../../../../user_provided_files/combined_pls.txt", "r") as f:
        combined_pls = f.readlines()
    combined_pl_dict = get_combined_pls_dict(combined_pls)
except FileNotFoundError:
    combined_pl_dict = {}
pl_to_comb = dict()
for comb, pl_list in combined_pl_dict.items():
    for pl in pl_list:
        if pl_to_comb.get(pl) is not None:
            assert(0)
        else:
            pl_to_comb[pl] = comb



arr = []
BATCH_INSTNDIR="../../src/opcodes_batch"
group_items = []
# ISA subset
#group_map_ff = "%s/group_map.txt" % BATCH_INSTNDIR)
group_map_ff = "%s/group_map_subset.txt" % BATCH_INSTNDIR
try:
    with open(group_map_ff, "r") as f:
        for line in f:
            arr = line[:-1].split("|")
            assert(len(arr) == 3)
            group_items.append(arr)
    print("group items:", group_items)
except FileNotFoundError:
    sys.exit(0)
batch_transponder = []
batch_transponder_group_id = []
if os.path.exists(BATCH_INSTNDIR + "/batch_transponder_2.txt"):
    with open(BATCH_INSTNDIR + "/batch_transponder_2.txt", "r") as f:
        for line in f:
            arr = line[:-1].split("|")
            batch_transponder.append(arr)
            #batch_transponder.append(int(line[:-1]))
            batch_transponder_group_id.append(arr[0])



decisions = dict()
with open("../xFollowerSetsOnly/decisions.txt", 'r') as file:
    for line_num, line in enumerate(file, 1):
        line = line.strip()
        if not line:
            continue
        if ', [' in line:
            key_part, value_part = line.split(', [', 1)
            key = key_part.strip()
            list_str = '[' + value_part
            decisions[key] = ast.literal_eval(list_str)

print(decisions)


pl_signals = {}
with open("../../../xDUVPLs/perfloc_signals.txt", "r") as f:
    for line in f:
        pl, sigs = line[:-1].split(" : ")
        pl_signals[pl] = sigs.split(",")
iid_map = {}
for k, v in pl_signals.items():
    iid_map[k] = v[0]
for comb_pl, pl_list in combined_pl_dict.items():
    iid_map[comb_pl] =  iid_map[pl_list[0]]
    pl_signals[comb_pl] = pl_signals[pl_list[0]]

# Parse common_header.sv to get the individual _t0 component signals for each PL.
# Each PL-level wire (e.g. scb_0_s8_t0) is an OR of the underlying CellIFT shadow
# signals; use those directly so we don't depend on the wire declaration being in scope.
COMMON_HEADER = "../../../src_ift/common_header.sv"
pl_t0_sigs = {}
with open(COMMON_HEADER, "r") as f:
    for line in f:
        line = line.strip()
        m = re.match(r'wire\s+(\w+)_t0\s*=\s*\|\{(.+)\}\s*;', line)
        if m:
            pl_name = m.group(1)
            sigs_str = m.group(2)
            sigs = [s.strip() for s in sigs_str.split(',') if s.strip()]
            pl_t0_sigs[pl_name] = sigs

#with open(f"../../../../user_provided_files/{taint}.json", "r") as f:
#    tainted_signals = json.load(f)
#print(tainted_signals)


PROP_TMPLT = '''\
cover -name {{{tnm}_src_{s}_dest_{d}}} {{@(posedge clk_i) {src} ##1 (|{{{t0_sigs}, 1\'b0}})}}
'''

PROP_TMPLT2 = '''\
cover -name {{{tnm}_src_{s}_dest_{d}}} {{@(posedge clk_i) ({src} && i1_in_some_pl) ##1 ( {in_dest} && (|{{{t0_sigs}, 1\'b0}}))}}
'''

def gen(taint):
    global htcl_

    if taint == "taint_both_rs1_rs2":
        DEFINEOPTAINT="`define BOTHRS"
    elif taint == "taint_rs1":
        DEFINEOPTAINT="`define RS1"
    elif taint == "taint_rs2":
        DEFINEOPTAINT="`define RS2"
    else:
        print("invalid taint")
        sys.exit(0)   
 
    JOB="ift_dyn_rtl2mupath_" + taint
    
    tnm = taint

    outstring = dynamic_template_no_props

    i0_constraint = ""
    with open("../idef.sv", "r") as idef:
        for line in idef:
            i0_constraint += line

    for agroup in group_items:
        group_id, field, t_instns = agroup
        if field == "" :
            continue

        i1_constraint = ""
        with open("%s/group_subset_%s.sv" % (BATCH_INSTNDIR, group_id), "r") as idef:
            for line in idef:
                i1_constraint += (line.replace("i0", "i1"))

        outstring = dynamic_template_no_props
        rep_pairs = [
            ("OP_TAINT", DEFINEOPTAINT),
            ("INSTN_CONSTRAINT", i0_constraint),
            ("I1_CONSTRAINT", i1_constraint)]
        for tt in rep_pairs:
            outstring = outstring.replace(tt[0], tt[1])

        with open (f"{JOB}_group{group_id}.sv", "w") as f:
            f.write(h_)
            f.write(outstring)
            f.write(e_)


    all_dest_pls = set()
    for s, dest_set_list in decisions.items():
        all_dest_pls = set()
        for dest_set in dest_set_list:
            for dest in dest_set:
                all_dest_pls.add(dest)

        cnt = 0
        for dest_set in dest_set_list:
            added_t0_sigs = list()
            in_dest = ""
            if len(dest_set) == 0:
                for dest in all_dest_pls:
                    # Use the individual CellIFT shadow signals that compose this
                    # PL's taint wire, so we don't need the wire to be in scope.
                    #for t0_sig in pl_t0_sigs.get(dest, [dest + "_t0"]):
                    t0_sig = prefix + dest + "_t0"
                    if t0_sig not in added_t0_sigs:
                        added_t0_sigs.append(t0_sig)
                    in_dest += f"!{prefix+dest} && "
            else:
                for dest in all_dest_pls:
                    if dest in dest_set:
                        in_dest += f"{prefix+dest} && "
                        # Use the individual CellIFT shadow signals that compose this
                        # PL's taint wire, so we don't need the wire to be in scope.
                        #for t0_sig in pl_t0_sigs.get(dest, [dest + "_t0"]):
                        t0_sig = prefix + dest + "_t0"    
                        if t0_sig not in added_t0_sigs:
                            added_t0_sigs.append(t0_sig)
                    else:
                        in_dest += f"!{prefix+dest} && "
            
            in_dest += "1'b1"
            if added_t0_sigs:
                htcl_ += PROP_TMPLT2.format(
                    tnm=tnm,
                    s=s,
                    d=cnt,
                    src=prefix + s,
                    in_dest=in_dest,
                    t0_sigs=", ".join(added_t0_sigs)
                )
            cnt += 1
    
    with open (f"{JOB}.tcl", "w") as f:
        f.write(htcl_)
        f.write("\nprove -task mytask\n")
        f.write(f"set props [get_property_list -include {{name {tnm}*}}]\n") 
        f.write("report -property $props -csv -results -file %s/%s.csv -force\n" % (os.getcwd(), JOB))
        f.write("save %s/%s.db -force -clean -include {app_data session_data elaborated_design}\n" % (os.getcwd(), JOB))

    return


def pp():


    return


if len(sys.argv) != 3:
    print("gen/pp")
    exit(0)

opt = sys.argv[1]
taint = sys.argv[2]
if opt == "gen":
    gen(taint)
elif opt == "pp":
    pp()

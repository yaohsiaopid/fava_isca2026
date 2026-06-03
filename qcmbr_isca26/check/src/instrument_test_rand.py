# Iterate over each directory (x86tso and coh_tests) and put the rand files
# in <>_rand directory
# 1. For each thread, augment N instructions with access InitAcc where N is the
# number of distinct address in the litmus tests and add po relation for each of
# these N instruction to every other instruction in each thread
# 2. If final state is defined 
from multiprocessing import Semaphore, Pool, Manager, Lock, Array, Semaphore, Value
import os
import random
import subprocess
import sys
from tlib import *
import argparse
#dnm = sys.argv[1]
#fnm = sys.argv[1] 
# op = AugmentTest("x86tso/safe033.test", "t.ext")
# op.proc()
def iter(dnm, last_read=False):
  if not os.path.exists(f"{dnm}_rand"):
    os.mkdir(f"{dnm}_rand")
      
  for itm in os.listdir(dnm):
    if itm[0] == "." or os.path.isdir(f"{dnm}/{itm}"): 
      continue
    print("Processing: ", itm)
    op = RandTest(f"{dnm}/{itm}", f"{dnm}_rand/{itm}")

    op.proc(last_read=last_read)
    op.remap_global_ids_and_export()
    #with open (f"{dnm}_rand/{itm}.val", "w") as f:
    #  f.write(str(op.get_distinct_val()))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Augment litmus tests for coherence checking.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-d", "--directory", dest="folder", help="Directory containing litmus tests to augment.")
    group.add_argument("-f", "--file", dest="ffname", help="A single litmus test file to augment.")
    parser.add_argument("-o", "--outdir", dest="outdir", help="A single litmus test file to augment.")
    parser.set_defaults(read=False)

    args = parser.parse_args()
    if not os.path.isdir(args.outdir):
      os.mkdir(args.outdir)
    if args.folder:
        folder = args.folder
        if not os.path.isdir(folder):
            sys.exit(f"Error: Directory not found at '{folder}'")
        iter(folder, args.read)
    elif args.ffname:
        ffname = args.ffname
        if not os.path.isfile(ffname):
            sys.exit(f"Error: File not found at '{ffname}'")

        b = (os.path.split(ffname)[-1]).split(".")[0]
        print(f"-> Output: {b}.ext.test")
        op = RandTest(f"{ffname}", f"{b}.ext.test")
        # op.remap([0,1,2,3,5,4], ffname, "tmp_.test")
        op.proc(last_read=args.read)
        op.remap_global_ids_and_export(args.outdir)

        print(args.read)

        
        #path, filename = os.path.split(ffname)
        #name, ext = os.path.splitext(filename)
        #output_filename = f"{name}_rand{ext}"
        #output_path = os.path.join(path, output_filename)
        
        #process_file(ffname, output_path)
#itm="W_evict.test"
#op = AugmentTest(f"{dnm}/{itm}", f"{dnm}_rand/{itm}")
#op.proc()
#dnm = "x86tso"
#iter(dnm)
#dnm = "coh_tests"
#iter(dnm)
# iter(dnm)

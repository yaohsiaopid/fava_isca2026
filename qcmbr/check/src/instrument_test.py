# Iterate over each directory (x86tso and coh_tests) and put the augmented files
# in <>_augmented directory
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
  if not os.path.exists(f"{dnm}_augmented"):
    os.mkdir(f"{dnm}_augmented")
  print(f"{dnm}_augmented") 
  for root, dirs, files in os.walk(dnm):
    for itm in files:
      if not itm.endswith(".test"):
        continue
      if "depr" in root:
        continue
      relative_path = os.path.relpath(os.path.join(root, itm), start=dnm)
      print("Processing: ", relative_path)
      op = AugmentTest(f"{dnm}/{relative_path}", f"{dnm}_augmented/{itm}")
      op.proc(last_read=last_read)
      with open(f"{dnm}_augmented/{itm}.val", "w") as f:
          f.write(str(op.get_distinct_val()))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Augment litmus tests for coherence checking.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-d", "--directory", dest="folder", help="Directory containing litmus tests to augment.")
    group.add_argument("-f", "--file", dest="ffname", help="A single litmus test file to augment.")
    parser.add_argument("-r", "--read", action='store_true', dest="read", help="A single litmus test file to augment.")
    parser.set_defaults(read=False)

    args = parser.parse_args()

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
        op = AugmentTest(f"{ffname}", f"{b}.ext.test")
        op.proc(last_read=args.read)

        print(args.read)

        
        #path, filename = os.path.split(ffname)
        #name, ext = os.path.splitext(filename)
        #output_filename = f"{name}_augmented{ext}"
        #output_path = os.path.join(path, output_filename)
        
        #process_file(ffname, output_path)
#itm="W_evict.test"
#op = AugmentTest(f"{dnm}/{itm}", f"{dnm}_augmented/{itm}")
#op.proc()
#dnm = "x86tso"
#iter(dnm)
#dnm = "coh_tests"
#iter(dnm)
# iter(dnm)

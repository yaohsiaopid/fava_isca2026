# Check whether each cache-controller state is reachable.
# We generate one Murphi model per state with an invariant that forbids that state:
#   (!IsUndefined(prevProcs)) -> (prevProcs != state)
# If the invariant is violated, the state is reachable.

import fire
from gconst import *
import pickle
import os
import sys
from util import *

if sys.version_info < (3, 6):
  sys.exit(1)

sys.path.append("src")
from code_gen.parse_rules import *

build_dir = "build"

# If this invariant is violated, then prevProcs = {state} is reachable.
template = '''
invariant "{state}_{scope}_reachable"
  !(!IsUndefined(prevProcs) & !IsUndefined(selc) & ({selc_cond}) & prevProcs = {state});
'''


def gen():
  dirname = f"{build_dir}/s0_state_reachability/out"
  os.makedirs(dirname, exist_ok=True)
  if not design_cfg.get('get_state', False):
    return 
  for itm in all_cc_states:
    is_local_cc = design_cfg.get('is_local_cc')
    is_not_local_cc = design_cfg.get('is_not_local_cc')
    for scope, selc_cond in (("h", f"{is_local_cc}"), ("r", f"{is_not_local_cc}")):
      outff = f"{dirname}/{itm}_{scope}.m"
      outff_h = open(outff, "w")

      parse_murphi_model(
        coh_model_file,
        nodes_iter_types,
        outff_h,
        {"track_req": False, "prevState": True},
      )
      outff_h.write(template.format(state=itm, scope=scope, selc_cond=selc_cond))
      outff_h.close()


def pp():
  reachable = []
  unreachable = []

  if not design_cfg.get('get_state', False):
    return 

  resdirname = f"{build_dir}/s0_state_reachability/_build"
  if not os.path.exists(resdirname):
    sys.exit(0)

  for itm in all_cc_states:
    for scope in ("h", "r"):
      resff = f"{resdirname}/{itm}_{scope}.txt"
      prop = f"{itm}_{scope}_reachable"

    # Follow s1.py's interpretation:
    # ret=True means the invariant was falsified (counterexample exists),
    # therefore the state is reachable.
      ret = get_res_file(resff, prop, assertion=False, inline_prop=False)
      # (ret2, _) = get_res_file_stats(resff, prop, assertion=False, inline_prop=False)
      # if ret2 is None:
      #   print("--> undetermined", resff)

      tag = f"{itm}_{scope}"
      if ret:
        reachable.append(tag)
      else:
        unreachable.append(tag)

  with open(f"{resdirname}/res.txt", "w") as f:
    f.write("Reachable\n")
    for itm in reachable:
      f.write(f"{itm}\n")
    f.write("Unreachable\n")
    for itm in unreachable:
      f.write(f"{itm}\n")

  with open(f"{resdirname}/res.pkl", "wb") as f:
    pickle.dump(reachable, f)

  print(f"==> {resdirname}/res.txt")
  print(f"==> {resdirname}/res.pkl")


if __name__ == "__main__":
  fire.Fire()
  dump_stats()

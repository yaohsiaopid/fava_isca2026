import os
import pickle
import re
import subprocess
import sys


base_ff_name = f"{state}_{state_prime}_{prefix}"
resff = f"{tardir}/{stepname}/_build/{base_ff_name}_trace.txt"
assert_transition_template = '''
invariant "{state}_to_{state_prime}"
  ((!IsUndefined(prevProcs) & (prevProcs = {state}))
  & ({proc_state_expr} = {state_prime})) ->
  ({msg_set_disjunction});
'''


def get_res_file(resff, propname, assertion=False, inline_prop=False):
  assert(os.path.exists(resff))
  tar_s = f'Invariant "{propname}" failed'
  if inline_prop:
    tar_s = f"Assertion failed: {propname}"
  result = subprocess.run(
    ["grep", "-q", tar_s, resff],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
  )
  exit_status = result.returncode
  if exit_status == 0:
    return (not assertion)
  return assertion


def get_set_info(resff):
  msg_set = {}
  pattern = re.compile(rf"msg_imm_{prefix}_set\[(\w+)\]:(\w+)")
  assert(os.path.exists(resff))
  with open(resff, "r") as f:
    found_last_state = False
    for line in f:
      if "The last state" in line:
        found_last_state = True
        continue
      if not found_last_state:
        continue
      match = pattern.search(line)
      if match:
        msg_type = match.group(1)
        is_active = match.group(2).lower()
        msg_set[msg_type] = is_active
  return msg_set


def build_msg_set_clause(msg_set):
  msg_set_ss = []
  for m_, v in msg_set.items():
    msg_set_ss.append(f"msg_imm_{prefix}_set[{m_}] = {v}")
  if len(msg_set_ss) == 0:
    return "false"
  return "(" + " & ".join(msg_set_ss) + ")"


def write_iter_file(iter_count, acc_):
  outff = f"{tardir}/{stepname}/out/{base_ff_name}_{iter_count}.m"
  with open(outff, "w") as outff_h:
    with open(f"{tardir}/{stepname}/out/{base_ff_name}_baseff.m", "r") as f:
      for ln in f:
        outff_h.write(ln)
    outff_h.write(
      assert_transition_template.format(
        state=state,
        state_prime=state_prime,
        proc_state_expr=proc_state_expr,
        msg_set_disjunction=" | ".join(acc_),
      )
    )
  return outff


def run_iter_file(iter_count, proof=False):
  basename = f"{base_ff_name}_{iter_count}"
  resff = f"{tardir}/{stepname}/_build/{basename}.txt"
  cmd = ["./util/mini_eval.sh"]
  if proof:
    cmd.append("-n")
  cmd.extend(["-d", tardir, "-f", basename, "-s", stepname])
  ret = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  print(ret.stdout)
  return resff


def main():
  iter_count = 0
  past = []
  acc_ = []

  msg_set = get_set_info(f"{tardir}/s1_msg_per_transition/_build/{state}_{state_prime}_{prefix}_trace.txt")
  while True:
    print(f"Iteration {iter_count}: {prefix}={msg_set}")
    if len(past) > 0 and msg_set in past:
      break
    past.append(msg_set)
    acc_.append(build_msg_set_clause(msg_set))

    outff = write_iter_file(iter_count, acc_)
    print(f"Running verification on {outff}...")
    cur_resff = run_iter_file(iter_count, proof=False)
    if not os.path.exists(cur_resff):
      print(f"Error: Result file {cur_resff} not found after running mini_eval.sh. Aborting.")
      break

    iter_count += 1
    if iter_count > 10:
      print("Reached max iterations.")
      break

    prop = f"{state}_to_{state_prime}"
    ret = get_res_file(cur_resff, prop, assertion=True, inline_prop=False)
    if ret:
      break
    msg_set = get_set_info(cur_resff)

  with open(f"{tardir}/{stepname}/_build/{base_ff_name}_iter.pkl", "wb") as f:
    pickle.dump(past, f)


if __name__ == "__main__":
  pk_file = f"{tardir}/{stepname}/_build/{base_ff_name}_iter.pkl"
  if len(sys.argv) > 1 and "-n" in sys.argv[1]:
    if os.path.exists(pk_file):
      with open(pk_file, "rb") as f:
        past = pickle.load(f)
      if len(past) == 0:
        sys.exit(0)

      acc_ = []
      for msg_set in past:
        acc_.append(build_msg_set_clause(msg_set))

      iter_count = len(past) - 1
      outff = f"{tardir}/{stepname}/out/{base_ff_name}_{iter_count}.m"
      if not os.path.exists(outff):
        print("NOT FOUND", outff)
        sys.exit(0)

      run_iter_file(iter_count, proof=True)
    else:
      sys.exit(0)
  else:
    main()
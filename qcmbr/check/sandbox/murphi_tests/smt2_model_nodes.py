#!/usr/bin/env python3
import argparse
import re
import sys
from pathlib import Path

import z3

NODE_PATTERN = re.compile(r"^order_node_g(\d+)_c(\d+)_(\d+)_(\d+)$")
EDGE_PATTERN = re.compile(
  r"^edge_node_g(\d+)_c(\d+)_(\d+)_(\d+)_to_node_g(\d+)_c(\d+)_(\d+)_(\d+)$"
)
STAGE_NAME_PATTERN = re.compile(r'StageName (\d+) "([a-zA-Z0-9_]+)"\.')
VT_STAGE_NAME_PATTERN = re.compile(r'VTStageName (\d+) (\d+) "([a-zA-Z0-9_]+)"\.')


def preprocess_smt2_file(smt2_path: str) -> str:
  input_path = Path(smt2_path)
  acc = []
  idx = 0
  ffs = []
  st = 0
  config = {}
  with open(input_path, "r") as src:
    for line in src:
      mat = re.search(r"; offset: (\d+)", line)
      if mat is not None:
        config['offset'] = int(mat.group(1))
      mat = re.search(r"; range: (\d+)", line)
      if mat is not None:
        config['range'] = int(mat.group(1))
      mat = re.search(r"; bottom_y: (\d+)", line)
      if mat is not None:
        config['bottom_y'] = int(mat.group(1))
      st += 1  
      if st <= 5:
        continue
      if re.search(r"check", line) is not None:
        reduced_path = input_path.with_name(f"{input_path.stem}.red.{idx}.smt2")
        ffs.append(reduced_path)
        with open(reduced_path, "w") as dst: 
          dst.writelines(acc)
        acc = []
        idx += 1
      elif re.search(f"pop|push", line) is None:
        acc.append(line)
  print("==> length of ", idx, ffs)
  return str(ffs[0]), config


def extract_node_lines(smt2_path: str, uarch_path: str) -> tuple[bool, list[str]]:
    solver = z3.Solver()
    reduced_smt2_path, config = preprocess_smt2_file(smt2_path)
    print("->", config)
    assertions = z3.parse_smt2_file(reduced_smt2_path)
    solver.add(assertions)
    result = solver.check()
    if result != z3.sat:
        return False, False, []
    model = solver.model()
    edges = []
    nodes_labels  = []
    label = {}
    max_stage = 0
    vt_stages = {} # number to stage name
    with open(uarch_path, "r") as f:
      for line in f:
        m = STAGE_NAME_PATTERN.search(line)
        if m is not None:
          label[int(m.group(1))] = m.group(2)
          t = int(m.group(1)) 
          max_stage = t if max_stage < t else max_stage
          continue

        m = VT_STAGE_NAME_PATTERN.search(line)
        if m is not None:
          label[int(m.group(1))] = m.group(3)
          t = int(m.group(1)) 
          max_stage = t if max_stage < t else max_stage
          vt_stages[t] = m.group(3)
          continue
    print("max stage", max_stage)
    exists = set()
    insts = set()
    rows = set()
    map_ = {}
    raws = []
    for decl in model.decls():
        variable_name = decl.name()
        match = NODE_PATTERN.match(variable_name)
        if match:
          if int(match.group(4)) > max_stage:
            continue
          val = model[decl].as_long()
          if val == 0:
            continue
          col = int(match.group(1))
          insts.add(int(col))
          row_ = int(match.group(4)) 
          raws.append((variable_name, col, row_, val))
          rows.add(row_)
          exists.add(row_)

    used = set()
    print(vt_stages)
    val_of_nodes = {}
    for decl in model.decls():
        variable_name = decl.name()
        match = EDGE_PATTERN.match(variable_name)
        if match:
          n1 = "order_node_g%s_c%s_%s_%s" % (match.group(1),match.group(2), match.group(3), match.group(4))
          n2 = "order_node_g%s_c%s_%s_%s" % (match.group(5),match.group(6), match.group(7), match.group(8))
          val = model[decl]
          if z3.is_true(val):
            # add edge 
            if not (int(match.group(4)) > max_stage or int(match.group(8)) > max_stage):
              edges.append(f"{n1} -> {n2} [label=\"\";constraint=false;];" )
              used.add(n1)
              used.add(n2)
            org_val = None
            if int(match.group(8)) == config['bottom_y']:
              gid = int(match.group(5))
              val = int(match.group(4))
              # (OffSetVal 0) + (RangeVal 0) * l' + val)
              for k, v in vt_stages.items():
                if (config['offset'] + config['range'] * k + 0) <= val and \
                (config['offset'] + config['range'] * k + config['range']) > val: 
                  assert(org_val is None)
                  org_val = val - config['offset'] - config['range'] * k 
                  # print("===> v", gid, v, " has value ", org_val )
                  if not (gid, v) in val_of_nodes:
                    val_of_nodes[(gid,v)] = []
                  val_of_nodes[(gid, v)].append((org_val, val, n1, n2))


    for o_, n_ in zip(sorted(rows), list(range(len(rows)))):
      map_[o_] = n_
    for itm in raws:  
      nm, col, row, val = itm
      if not nm in used:
        continue 
      row_ = map_[row]
      nodes_labels.append(
          f'{nm}  [shape=circle;label="";pos="{col+1},-{row_}!";];'
      )
      print("=> order of inst ", col, " at ", label[row], " is ",  val)
      for k, v in val_of_nodes.items():
        gid, label_ = k
        if label_ == label[row] and col == gid:
          print("===> v", gid, label_, " has value ", v)
          if len(v) > 1:
            print("=============")
            print("FAIL")
            print("=============")
            #return True, None, None
          # assert(len(v) <= 1)
          


    for itm in insts:
      nodes_labels.append(f"inst_{itm}_label [label=\"Inst {itm}\";pos=\"{itm+1},0.5!\";shape=none];")

    exists_list = sorted(exists)
    for val in exists_list:
        if val in label:
            nodes_labels.append(
                f'l{val}_label [label="{label[val]}";pos="0,-{map_[val]}!";shape=none]; '
            )
    output_lines = edges + nodes_labels
    return False, True, output_lines

header = '''
digraph G {
  layout=neato;
  overlap=scale;
  splines=true;
  
'''
footer = '''
}
'''
def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Read an SMT2 file with Z3, run check-sat, and write node_* model "
            "variables to an output file."
        )
    )
    parser.add_argument("smt2_file", help="Path to input SMT2 file")
    parser.add_argument("output_file", help="Path to output text file")
    parser.add_argument("uarch_file", help="Path to uarch file")
    args = parser.parse_args()

    fail, is_sat, lines = extract_node_lines(args.smt2_file, args.uarch_file)
    if fail:
      print("=" * 80)
      print("FAIL")
      print("=" * 80)
      return 1

    with open(args.output_file, "w", encoding="utf-8") as out:
        if is_sat:
          out.write(header)
          for line in lines:
              out.write(line + "\n")
          out.write(footer)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

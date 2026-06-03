import sys
import itertools
import os
import re
from collections import defaultdict, deque
# globalID , coreID  flag
inst_pattern = r'^([0-9]+) ([0-9]+) 0 0'
pattern_op = r'\(([a-zA-Z\s]+) \(VA [0-9]+ [0-9]+\) \(PA ([0-9]+) [0-9]+\) \(Data ([0-9]+)\)'
#pattern_op = r'\(VA [0-9]+ [0-9]+\) \(PA ([0-9]+) [0-9]+\) \(Data ([0-9]+)\)'
final_pa_pattenr = r'\(PA [0-9]+ [0-9]+\)\s*='

def proc_d(addrs, instn_info, next_global_id, cnt_thd, constrained_addrs, final_val, final_state_chk_at={}):
  new_insts = ""
  new_relations = ""
  inst_thd = {}
  inst_thd_final = {}
  new_inst_ids = [] # init acc
  my_gid = next_global_id #+ 1
  for idx, a in enumerate(list(addrs)):
      for core_id in range(cnt_thd): 
        if not len([itm for itm in instn_info  if (itm[2] == a and itm[1] == core_id)]) > 0:
          continue 
        s = "{global_id} {core_id} 0 0 (Read InitAcc (VA {a} 0) (PA {a} 0) (Data 0))\n" 
        s = s.format(global_id = my_gid, core_id = core_id, a=a)
        new_insts += s
        new_inst_ids.append((my_gid, core_id, a))
        inst_thd[(core_id, a)] = my_gid
        my_gid += 1
  # print("->")
  # print(instn_info)
  for instn in instn_info:
    (global_id, core_id, addr) = instn
    if addr is not None:
      # existing memory access to some addr
      new_gid = inst_thd[(core_id, addr)]
      s = "Relationship po {i0} 0 -> {i1} 0\n"
      s = s.format(i0 = new_gid, i1 = global_id)
      new_relations += s
    else:
      # existing fence access or access to no particular addr
      for k, new_gid in inst_thd.items():
        cid, addr = k
        if cid == core_id:
          s = "Relationship po {i0} 0 -> {i1} 0\n"
          s = s.format(i0 = new_gid, i1 = global_id)
          new_relations += s

  if len(constrained_addrs) > 0 and len(final_state_chk_at) != 0:
    for core_id in range(cnt_thd):
        prev_evict = []
        for addr in sorted([a for a, cid in final_state_chk_at.items() if cid == core_id]):
            fval = final_val[addr]
            s = "{global_id} {core_id} 0 0 (Read (VA {a} 0) (PA {a} 0) (Data {fval}))\n" 
            s = s.format(global_id = my_gid, core_id = core_id, a=addr, fval=fval)
            new_insts += s
            inst_thd_final[(core_id, addr)] = my_gid
            for tmp_gid in prev_evict: # j in range(idx):
                print("---> multi constrained addr")
                s = "Relationship po {i0} 0 -> {i1} 0\n"
                s = s.format(i0 = tmp_gid, i1 = my_gid)
                new_relations += s
            prev_evict.append(my_gid)
            my_gid += 1
    # po-after w.r.t all existing and initAcc
    for instn in instn_info + new_inst_ids:
        (global_id, core_id, addr) = instn
        for k, new_gid in inst_thd_final.items():
            # as long as its same core we make it po
            cid, a = k
            if cid == core_id:
                # same thread then we make the existing one po before current Evict acc
                s = "Relationship po {i0} 0 -> {i1} 0\n"
                s = s.format(i0 = global_id, i1 = new_gid)
                new_relations += s

  if len(constrained_addrs) > 0 and len(final_state_chk_at) == 0:
    # evictAcc are serialized (since one request at a time)
    for core_id in range(cnt_thd):
        prev_evict = []
        for idx, a in enumerate(list(constrained_addrs)):
            if not len([itm for itm in instn_info  if (itm[2] == a and itm[1] == core_id)]) > 0:
                continue
            s = "{global_id} {core_id} 0 0 (Write Evict (VA {a} 0) (PA {a} 0) (Data 0))\n" 
            s = s.format(global_id = my_gid, core_id = core_id, a=a)
            new_insts += s
            inst_thd_final[(core_id, a)] = my_gid
            for tmp_gid in prev_evict: # j in range(idx):
                print("---> multi constrained addr")
                s = "Relationship po {i0} 0 -> {i1} 0\n"
                s = s.format(i0 = tmp_gid, i1 = my_gid)
                new_relations += s
            prev_evict.append(my_gid)
            my_gid += 1
    # po-after w.r.t all existing and initAcc
    for instn in instn_info + new_inst_ids:
        (global_id, core_id, addr) = instn
        for k, new_gid in inst_thd_final.items():
            # as long as its same core we make it po
            cid, a = k
            if cid == core_id:
                # same thread then we make the existing one po before current Evict acc
                s = "Relationship po {i0} 0 -> {i1} 0\n"
                s = s.format(i0 = global_id, i1 = new_gid)
                new_relations += s

        #if addr is not None and addr in constrained_addrs:
        #    new_gid = inst_thd_final[(core_id, addr)]
        #    s = "Relationship po {i0} 0 -> {i1} 0\n"
        #    s = s.format(i0 = global_id, i1 = new_gid)
        #    new_relations += s
        #else:
        #    pass
        #    #for k, new_gid in inst_thd.items():
        #    #  cid, addr = k
        #    #  if cid == core_id:
        #    #    s = "Relationship po {i0} 0 -> {i1} 0\n"
        #    #    s = s.format(i0 = new_gid, i1 = global_id)
        #    #    new_relations += s

  return (new_relations, new_insts)

class AugmentTest:
  def __init__(self, fnm, ofnm):
    self.fnm = fnm
    self.ofnm = ofnm
    self.rst()

  def rst(self):
    self.final_constrained_addrs = set()
    self.addrs = set()
    self.val = set()
    self.addr_cnt = 0
    self.cnt_thd = 1
    self.next_global_id = 0
    self.instn_info = []
    self.final_val = {}
  def get_distinct_val(self):
    self.val.add("0")
    print("==> values ", self.val)
    return len(self.val)
  def proc(self, last_read = False):
    #thd = {}
         
    init_acc_per_outcome = []
    each_alt = []

    with open(self.fnm, "r") as f:
        for line in f:
            if "Alternative" in line:
                # new possibility
                if len(self.instn_info) == 0: #thd:
                    continue

                print("---> final constrained", self.final_constrained_addrs)
                print("---> num of addr", len(self.addrs))
                if len(self.addrs) > self.addr_cnt:
                  self.addr_cnt = len(self.addrs)
                new_relations, new_insts = \
                    proc_d(self.addrs, self.instn_info, self.next_global_id, self.cnt_thd, self.final_constrained_addrs, self.final_val)
                init_acc_per_outcome.append((new_relations, new_insts))
                each_alt.append((self.addrs.copy(), self.instn_info.copy(), self.next_global_id, self.cnt_thd, self.final_constrained_addrs.copy(), self.final_val.copy()))

                self.rst()

            match = re.search(inst_pattern, line)
            if match is not None:
                global_id, core_id = int(match.group(1)), int(match.group(2))
                #print("==>",  line)
                match = re.search(pattern_op, line)
                if match is not None:
                    addr = int(match.group(2))
                    self.instn_info.append((global_id, core_id, addr))
                    self.addrs.add(addr)
                    #print("-> here", match.group(2))
                    self.val.add(match.group(3))
                else:
                    print("===> non READ/WRITE??", line)
                    self.instn_info.append((global_id, core_id, None))

                if self.next_global_id <= global_id:
                    self.next_global_id = global_id + 1
                if self.cnt_thd <= core_id:
                    self.cnt_thd = core_id + 1
                continue
            match = re.search(final_pa_pattenr, line)
            if match is not None:
                addr_str = re.search(r'\(PA ([0-9]+)', line).group(1)
                addr_val = re.search(r'\(PA ([0-9]+) 0\)\s*=\s*([0-9]+)', line).group(2)
                self.final_constrained_addrs.add(int(addr_str))
                self.final_val[int(addr_str)] = addr_val

    if len(self.instn_info) != 0: 
        print("---> final constrained", self.final_constrained_addrs)
        print("---> num of addr", len(self.addrs))
        if len(self.addrs) > self.addr_cnt:
          self.addr_cnt = len(self.addrs)
        new_relations, new_insts = \
            proc_d(self.addrs, self.instn_info, self.next_global_id, self.cnt_thd, self.final_constrained_addrs, self.final_val)
        init_acc_per_outcome.append((new_relations, new_insts))
        each_alt.append((self.addrs.copy(), self.instn_info.copy(), self.next_global_id, self.cnt_thd, self.final_constrained_addrs.copy(), self.final_val.copy()))



    fout = open(self.ofnm, "w") 
    cnt = 0
    init = False
    with open(self.fnm, "r") as f:
        for line in f:
            if "Alternative" in line:
                init = True
            if init and (("Relationship" in line) or (re.search(final_pa_pattenr, line) is not None)):
                init = False
                a, b = init_acc_per_outcome[cnt]
                fout.write(b)
                fout.write(a)
                cnt += 1
            fout.write(line)

    fout.close()
    # TODO need to use herd to check whether the cycle still exists 

    return 
    
    if last_read and len(self.final_constrained_addrs) > 0:
        # we get the each address which thread access it
        # if any final constrained addr 
        pools = []
        for addr in sorted(self.final_constrained_addrs):
            pools.append([itm[1] for itm in self.instn_info if (itm[2] == addr)])
        combinations = list(itertools.product(*pools))
        for comb_idx, comb in enumerate(combinations):
            init_acc_per_outcome = []
            # this is for a new file where the final state is check by the thread id in the comb 
            final_state_chk_at = {}
            for idx, addr in enumerate(sorted(self.final_constrained_addrs)):
                final_state_chk_at[addr] = comb[idx]
            for an_alt in each_alt:
               new_relations, new_insts = proc_d(*an_alt, final_state_chk_at = final_state_chk_at)
               init_acc_per_outcome.append((new_relations, new_insts))
            out_name = self.ofnm.split(".test")[0] + f".r{comb_idx}.test"  
            fout = open(out_name, "w") 
            cnt = 0
            init = False
            with open(self.fnm, "r") as f:
                for line in f:
                    if "Alternative" in line:
                        init = True
                    if init and (("Relationship" in line) or (re.search(final_pa_pattenr, line) is not None)):
                        init = False
                        a, b = init_acc_per_outcome[cnt]
                        fout.write(b)
                        fout.write(a)
                        cnt += 1
                    fout.write(line)
            fout.close()
    #if self.final_constrained:
    #    print("======> final state constrained yet augmented: ", self.ofnm)    

class RandTest:
  def __init__(self, fnm, ofnm):
    self.fnm = fnm
    self.ofnm = ofnm
    self.rst()

  def rst(self):
    self.final_constrained_addrs = set()
    self.addrs = set()
    self.val = set()
    self.addr_cnt = 0
    self.cnt_thd = 1
    self.next_global_id = 0
    self.instn_info = []
    self.final_val = {}
  def get_distinct_val(self):
    self.val.add("0")
    print("==> values ", self.val)
    return len(self.val)
  def proc(self, last_read = False):
    #thd = {}
         
    init_acc_per_outcome = []
    each_alt = []

    with open(self.fnm, "r") as f:
        for line in f:
            if "Alternative" in line:
                # new possibility
                if len(self.instn_info) == 0: #thd:
                    continue

                print("---> final constrained", self.final_constrained_addrs)
                print("---> num of addr", len(self.addrs))
                if len(self.addrs) > self.addr_cnt:
                  self.addr_cnt = len(self.addrs)
                new_relations, new_insts = \
                    proc_d(self.addrs, self.instn_info, self.next_global_id, self.cnt_thd, self.final_constrained_addrs, self.final_val)
                init_acc_per_outcome.append((new_relations, new_insts))
                each_alt.append((self.addrs.copy(), self.instn_info.copy(), self.next_global_id, self.cnt_thd, self.final_constrained_addrs.copy(), self.final_val.copy()))

                self.rst()

            match = re.search(inst_pattern, line)
            if match is not None:
                global_id, core_id = int(match.group(1)), int(match.group(2))
                #print("==>",  line)
                match = re.search(pattern_op, line)
                if match is not None:
                    addr = int(match.group(2))
                    self.instn_info.append((global_id, core_id, addr))
                    self.addrs.add(addr)
                    #print("-> here", match.group(2))
                    self.val.add(match.group(3))
                else:
                    print("===> non READ/WRITE??", line)
                    self.instn_info.append((global_id, core_id, None))

                if self.next_global_id <= global_id:
                    self.next_global_id = global_id + 1
                if self.cnt_thd <= core_id:
                    self.cnt_thd = core_id + 1
                continue
            match = re.search(final_pa_pattenr, line)
            if match is not None:
                addr_str = re.search(r'\(PA ([0-9]+)', line).group(1)
                addr_val = re.search(r'\(PA ([0-9]+) 0\)\s*=\s*([0-9]+)', line).group(2)
                self.final_constrained_addrs.add(int(addr_str))
                self.final_val[int(addr_str)] = addr_val

    if len(self.instn_info) != 0: 
        print("---> final constrained", self.final_constrained_addrs)
        print("---> num of addr", len(self.addrs))
        if len(self.addrs) > self.addr_cnt:
          self.addr_cnt = len(self.addrs)
        new_relations, new_insts = \
            proc_d(self.addrs, self.instn_info, self.next_global_id, self.cnt_thd, self.final_constrained_addrs, self.final_val)
        init_acc_per_outcome.append((new_relations, new_insts))
        each_alt.append((self.addrs.copy(), self.instn_info.copy(), self.next_global_id, self.cnt_thd, self.final_constrained_addrs.copy(), self.final_val.copy()))

  def remap_percore(self, perms, fnm, outfnm):
    # 
    input_tests = {}
    po_relations = []
    in_degree = {}
    graph = defaultdict(list)
    cnt = 0
    with open(fnm, "r") as f:
      for line in f:
        if "Alternative" in line:
          # new possibility
          if len(input_tests) == 0:
            continue
          else:
            break
        match = re.search(inst_pattern, line)
        if match is not None:
          global_id, core_id = int(match.group(1)), int(match.group(2))
          input_tests[global_id] = core_id 
          in_degree[global_id] = 0
          graph[global_id] = []
          cnt+=1

        match = re.search(r'Relationship po ([0-9]+) [0-9]+ -> ([0-9]+) [0-9]+', line)
        if match is not None:
          po_relations.append((int(match.group(1)), int(match.group(2))))

    for a, b in po_relations:
        graph[a].append(b)
        in_degree[b] += 1 
    # toplogical sort
    sorted_instructions = []
    queue = deque([node for node in in_degree if in_degree[node] == 0])

    while queue:
      current = queue.popleft()
      sorted_instructions.append(current)
      for neighbor in graph[current]:
        in_degree[neighbor] -= 1
        if in_degree[neighbor] == 0:
          queue.append(neighbor)

    n_input_tests = defaultdict(list)
    for global_id in sorted_instructions:
        if global_id in input_tests:
            core_id = input_tests[global_id]
            n_input_tests[core_id].append(global_id)
    print(n_input_tests)
    new_cnt = sum([len(itm) for k, itm in n_input_tests.items()])

    # mapping form (old_core_id, old_gid) -> new_core_id, new_gid
    mapping_ = {}
    new_input_tests = {}
    ngid = 0
    perms_ = {}
    for idx, itm in enumerate(perms):
      # itm: new core id  to old core id 
      perms_[itm] = idx

    for k in sorted(perms_.keys()):
      # idx: original core id
      new_input_tests[k] = []
      for old_gid in n_input_tests[perms_[k]]:
        new_input_tests[k].append((old_gid, ngid))
        assert(not (perms_[k], old_gid) in mapping_)
        mapping_[(perms_[k], old_gid)] = (k, ngid)
        mapping_[old_gid] = ngid
        ngid += 1
    print(new_input_tests)
    print(mapping_)

    with open(fnm, "r") as infile, open(outfnm, "w") as outfile:
        for line in infile:
            line = line.strip()

            # Match and replace global ID in instruction pattern
            match = re.search(inst_pattern, line)
            if match is not None:
                global_id = int(match.group(1))
                core_id = int(match.group(2))
                n_core_id, n_gid  = mapping_[(core_id, global_id)]
                line = re.sub(rf"^{global_id} {core_id}", f"{n_gid} {n_core_id}", line)
                outfile.write(line + "\n")
                continue

            # Match and replace relationship pattern
            relation_pattern = r"(Relationship [a-zA-Z]+ )([0-9]+)( [0-9]+\s+->\s+)([0-9]+)( [0-9]+)"
            match = re.search(relation_pattern, line)
            if match is not None:
                n0 = int(match.group(2))
                n1 = int(match.group(4))
                new_n0 = mapping_[n0]
                new_n1 = mapping_[n1]
                nl = ""
                for i in range(1, 6):
                  if (i == 2):
                    nl += str(new_n0)
                  elif (i == 4):
                    nl += str(new_n1)
                  else:
                    nl += match.group(i) 
                nl += "\n"
                outfile.write(nl)
                continue

            # Write the line as is if no match
            outfile.write(line + "\n")
    # return mapping_

  def remap(self, perms, fnm, outfnm):
    """
    Create a new file and remap global IDs and relationships based on permutations.

    Args:
        perms (list): List of permutations for remapping.
        fnm (str): Input file name.
        outfnm (str): Output file name.
    """
    with open(fnm, "r") as infile, open(outfnm, "w") as outfile:
        for line in infile:
            line = line.strip()

            # Match and replace global ID in instruction pattern
            match = re.search(inst_pattern, line)
            if match is not None:
                global_id = int(match.group(1))
                core_id = match.group(2)
                new_global_id = perms[global_id]
                line = re.sub(rf"^{global_id}", str(new_global_id), line)
                outfile.write(line + "\n")
                continue

            # Match and replace relationship pattern
            relation_pattern = r"(Relationship [a-zA-Z]+ )([0-9]+)( [0-9]+\s+->\s+)([0-9]+)( [0-9]+)"
            match = re.search(relation_pattern, line)
            if match is not None:
                n0 = int(match.group(2))
                n1 = int(match.group(4))
                new_n0 = perms[n0]
                new_n1 = perms[n1]
                nl = ""
                for i in range(1, 6):
                  if (i == 2):
                    nl += str(new_n0)
                  elif (i == 4):
                    nl += str(new_n1)
                  else:
                    nl += match.group(i) 
                nl += "\n"
                outfile.write(nl)
                continue

            # Write the line as is if no match
            outfile.write(line + "\n")

  def remap_global_ids_and_export(self, outdir):
    """
    Remap global IDs to a new set of IDs and export the updated content to a new file.
    """
    b = (((self.fnm).split("/"))[-1]).split(".test")[0]
    if not os.path.isdir(f"{outdir}/{b}.p"):
      os.mkdir(f"{outdir}/{b}.p")

    rand_gid = False
    if rand_gid:
        print("next global id", self.next_global_id)
        perms = list(itertools.permutations(list(range(self.next_global_id))))
        for idx, perm in enumerate(perms):
            if perm == (3,0,1,2,4,5):
              print("===>", idx)
            self.remap(perm, self.fnm, f"{outdir}/{b}.p/{b}.p{idx}.test")    
        return 

    perms = list(itertools.permutations(list(range(self.cnt_thd))))
    file_meta = {} 
    for idx, perm in enumerate(perms):
      if perm == tuple(list(range(self.cnt_thd))):
        continue
      if perm == (2,0,1,3):
        print("===> here")
      self.remap_percore(perm, self.fnm, f"{outdir}/{b}.p/{b}.p{idx}.test")    
      cur_mapping_ = {}
      for tmpidx, val in enumerate(perm):
        # old core id to new core id 
        cur_mapping_[tmpidx] = val
      file_meta[f"{b}.p{idx}.test"] = cur_mapping_
      print(f"{outdir}/{b}.p/{b}.p{idx}.test")
    import pickle
    with open(f"{outdir}/{b}.p/meta.pkl", "wb") as f:
      pickle.dump(file_meta, f)
    # global_id_map = {}
    # next_new_id = 0

    # with open(input_file, "r") as infile, open(output_file, "w") as outfile:
    #     for line in infile:
    #         match = re.search(inst_pattern, line)
    #         if match is not None:
    #             old_global_id = int(match.group(1))
    #             if old_global_id not in global_id_map:
    #                 global_id_map[old_global_id] = next_new_id
    #                 next_new_id += 1

    #             new_global_id = global_id_map[old_global_id]
    #             # Replace the old global ID with the new one in the line
    #             line = re.sub(rf"^{old_global_id}", str(new_global_id), line)

    #         outfile.write(line)

    # print(f"Global IDs remapped and exported to {output_file}")

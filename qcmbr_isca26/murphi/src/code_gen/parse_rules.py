import re
from pprint import pprint
import sys
import atexit
from builtins import print as _builtin_print

sys.path.append("src")
from gconst import * 

# When this module is imported by other scripts, route all local prints
# to a single temp log to avoid noisy stdout/stderr during batch runs.
_PARSE_RULES_LOG_PATH = "/tmp/parse_rules_import.log"
_parse_rules_log_fh = None
#if False and __name__ != "__main__":
if __name__ != "__main__":
    print("===> print of parse_rules is at ", _PARSE_RULES_LOG_PATH)
    _parse_rules_log_fh = open(_PARSE_RULES_LOG_PATH, "a", buffering=1)

    def print(*args, **kwargs):
        kwargs.pop("file", None)
        kwargs.setdefault("flush", True)
        return _builtin_print(*args, file=_parse_rules_log_fh, **kwargs)

    atexit.register(_parse_rules_log_fh.close)

# define the design_cfg
print(design_cfg)
print_ = False
core_req_type = f'''
-- CI {{ 
CoreReq: record
  cl: {m_val_type_name};
  vld: boolean;
  tp: enum {{ci_store, ci_load, ci_evict}};
end;
-- * vld = true,  tp determines the type
-- * The coherence protocol should mark vld as false when finishing a store 
-- * The read is poppsed (marked invalid) only if the coherence protocol return
-- values (i.e., `.cl` is no longer undefined)
-- }} CI
'''
# selc and prevProcReq
evict_req_t = '''
if (m = selc) then
  prevProcReq.tp:= ci_evict; 
  prevProcReq.cl:= undefined; 
  prevProcReq.vld := true;
endif;
'''
store_req_end_t = '''
if (m = selc) then
  prevProcReq.tp:= ci_store; 
  prevProcReq.cl:= undefined; -- TODO
  prevProcReq.vld := true; 
endif;
'''
store_req_t = '''
if (m = selc) then
  prevProcReq.tp:= ci_store; 
  prevProcReq.cl:= cl; 
  prevProcReq.vld := true; 
endif;
'''
load_req_t = '''
if (m = selc) then
  prevProcReq.tp:= ci_load; 
  prevProcReq.cl:= undefined; 
  prevProcReq.vld := true; 
endif;
'''

rset_t = '''
  cur_state := {proc_state_expr};
  in_stable_state := {stable_state_df};
  if (start) then
    -- BLOCK_WITHIN_START
    {block_within_start}
    if (!in_stable_state) then
      if (prevProcs != cur_state) then
        multisetAdd(cur_state, reached_set);
      endif;
    else 
      if (multisetcount(i:reached_set, reached_set[i] = cur_state) = 0) then
        multisetAdd(cur_state, reached_set);
      else
        assert false "end state exists?";
      endif;
      start := false;
    endif;
  endif;
'''

hrset_tar_idx_t = '''
in_stable_state := {stable_state_df};
if (start) then
  -- BLOCK_WITHIN_START
  {block_within_start}
  if (prevHomeNode != {m_home_cur}.{m_home_state_field}) then
    if (cur_idx <= {tar_target_len}) then
      if (cur_idx < {tar_target_len} & {m_home_cur}.{m_home_state_field} = tar[cur_idx]) then
        cur_idx := cur_idx + 1;
      else 
        cur_idx := {tar_target_len_plus_1};
      endif;
    endif;
  endif;

  if (in_stable_state) then
    start := false;
  endif;
endif;
'''
rset_tar_idx_t = '''
cur_state := {proc_state_expr};
in_stable_state := {stable_state_df};
if (start) then
  -- BLOCK_WITHIN_START
  {block_within_start}
  if (prevProcs != cur_state) then
    if (cur_idx <= {tar_target_len}) then
      if (cur_idx < {tar_target_len} & cur_state = tar[cur_idx]) then
        cur_idx := cur_idx + 1;
      else 
        cur_idx := {tar_target_len_plus_1};
      endif;
    endif;
  endif;

  if (in_stable_state) then
    start := false;
  endif;
endif;
'''

def pp_field(ss, msg_var=None):
    if ss.startswith("field"):
        field = ss.split("field:")[-1]
        return f"{msg_var}.{field}"
    else:
        return ss

def get_proc_state_expr():
    expr_t = design_cfg.get("proc_state_expr_t", "{m_proc_selc}.{m_proc_state_field}")
    return expr_t.format(m_proc_selc=m_proc_selc, m_proc_state_field=m_proc_state_field)
def get_home_select_expr():
    expr_t = design_cfg.get("home_select_expr_t", f"for i: {m_home_iter_type} do\n selh := i;\n endfor;\n")
    return expr_t

def parse_murphi_model(model_file, iterative_types, outff_h, cfg={}, additional_var = {}):
    # - book_keep: str
    # - decl_var: str
    # - init_state: str
    # - types_to_dec: str
    # - track_req: Bool 
    # - prevState: Bool
    # - past_1_prevState: Bool 
    # - prevStateVal: Bool
    # - past_1_prevStateVal: Bool
    # - rset: dictionary

    proc_state_expr = get_proc_state_expr()
    home_select = get_home_select_expr()
    opt_cond_selc = design_cfg.get("opt_cond_selc", "selc := n;")
    my_vars = {
        # name: (type, init, book_keep)
        "selc": (m_proc_iter_type, f"for n : {m_proc_iter_type} do\n {opt_cond_selc}\n endfor;\n", None), 
        "selh": (m_home_iter_type, home_select, ""),  
        "prevProcReq": ("CoreReq", "undefine prevProcReq;\n", "undefine prevProcReq;\n"),
        "prevHomeNode": (m_home_state_type, "", f"prevHomeNode := {m_home_cur}.{m_home_state_field};\n"),
        "prevProcs": (m_proc_state_type, "", f"prevProcs := {proc_state_expr};\n"),
        "myaddr": (addr_type_name, f"for a: {addr_type_name} do\n myaddr := a;\n endfor;\n", None),
        "cur_node": (nodes_iter_types[0], "undefine cur_node;\n", "cur_node := m;\n"), 
        "prevProcs_2": (m_proc_state_type, "", f"prevProcs_2 := prevProcs;\n"), 
        "prevProcReq_2": ("CoreReq", "undefine prevProcReq_2;\n", "prevProcReq_2 := prevProcReq;\n"),
        "prevStateVal": (m_val_type_name, "", f"prevStateVal := {m_proc_selc}.{m_proc_cl_field};\n"), 
        "prevStateVal_2": (m_val_type_name, "", "prevStateVal_2 := prevStateVal;\n"), 
        "reached_set": ("multiset [{num}] of {state_type_name}", "", rset_t),
        "tracked": ("boolean", "tracked := false;\n", ""),
        "start": ("boolean", "start := false;\n", ""), 
        "prevMsg": (msg_type_name, "", "undefine prevMsg;\n"),
        "prevMsgDst": (nodes_iter_types[0], "", "undefine prevMsgDst;\n"),
        "prevMsgSrc": (nodes_iter_types[0], "", "undefine prevMsgSrc;\n"),
        "prevSentMsg": (msg_type_name, "", "undefine prevSentMsg;\n"),
        #"prevMsg_chk": ("{t_msg_type_name}", "", "undefine prevMsg_chk;\n"),
        "msg_sent_set": (f"array [{msg_type_name}] of boolean", f"for m:{msg_type_name} do msg_sent_set[m] := false;\nendfor;\n", ""),
        "msg_rec_set": (f"array [{msg_type_name}] of boolean", f"for m:{msg_type_name} do msg_rec_set[m] := false;\nendfor;\n", ""),

        "msg_imm_sent_set": (f"array [{msg_type_name}] of boolean", f"for m:{msg_type_name} do msg_imm_sent_set[m] := false;\nendfor;\n", ""),
        "msg_imm_rec_set": (f"array [{msg_type_name}] of boolean", f"for m:{msg_type_name} do msg_imm_rec_set[m] := false;\nendfor;\n", ""),
    }

    """
    Parses a Murphi model to find rules within rulesets quantified over a specific type.
    
    Args:
        model_file (str): Path to the Murphi model file.
        iterative_type (str): The name of the iterative type to look for.
    """
    try:
        with open(model_file, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: File not found at {model_file}", file=sys.stderr)
        sys.exit(1)

    ruleset_pattern = re.compile(r'^\s*ruleset\s+([a-zA-Z0-9_]+)\s*:\s*([a-zA-Z0-9_]+).*?\bdo\b', re.IGNORECASE)
    rule_pattern = re.compile(r'^\s*rule\s+"([a-zA-Z0-9_\s]+)"', re.IGNORECASE)
    endruleset_pattern = re.compile(r'^\s*endruleset', re.IGNORECASE)

    bk_def = False
    defer_book_keep_after_get_state = bool(design_cfg.get("get_state", False))
    book_keep_insert_idx = None

    if defer_book_keep_after_get_state:
        in_get_state_def = False
        get_state_start_pattern = re.compile(r'^\s*(function|procedure)\s+get_state\b', re.IGNORECASE)
        fn_end_pattern = re.compile(r'^\s*end\s*;', re.IGNORECASE)
        for scan_idx, scan_line in enumerate(lines):
            if (not in_get_state_def) and get_state_start_pattern.match(scan_line):
                in_get_state_def = True
                continue
            if in_get_state_def and fn_end_pattern.match(scan_line):
                book_keep_insert_idx = scan_idx
                break

        if book_keep_insert_idx is None:
            print("Warning: design_cfg['get_state'] is true but get_state definition was not found; falling back to first procedure/function insertion point.", file=sys.stderr)

    ret = {}
    st = []
    rule_st = False
    cur_var_name = None
    rule_for_vars = set()
    # current rule 
    cur_block = ""

    dec = False 
    type_dec = False
    type_st = False

    class MyList: 
        def __init__(self):
            self.arr = []
        def add(self, item):
            if not item in self.arr:
                self.arr = [item] + self.arr 
        def iter(self):
            return self.arr    
    need_var = MyList()
    for k, v in additional_var.items():
        need_var.add(k)
        assert (not k in my_vars)
        my_vars[k] = v
    if ('track_req' in cfg and cfg['track_req']) or \
        ("past_1_prevProcReq" in cfg and cfg['past_1_prevProcReq']):
        need_var.add("selc")
        need_var.add("prevProcReq")
    if ("prevState" in cfg and cfg['prevState']) or \
       ("past_1_prevState" in cfg and cfg['past_1_prevState']):
        if addr_type_name != "":
            need_var.add("myaddr")
        need_var.add("selc")
        need_var.add("prevProcs")

    rset_book_keep = None
    need_rset_locals = False
    if "rset" in cfg and len(cfg['rset']) > 0:
        cfg_rset = dict(cfg['rset'])
        if not 'proc_state_expr' in cfg_rset:
            cfg_rset.setdefault("proc_state_expr", proc_state_expr)
        # print("===>JJJ", cfg_rset)
        cfg_rset.setdefault("prev_state_var", "prevProcs")
        rset_mode = cfg_rset.get("mode", "reached_set")
        need_rset_locals = True
        if rset_mode == "tar_idx":
            tar_states = list(cfg_rset.get("tar_states", []))
            tar_target_len = int(cfg_rset.get("tar_target_len", len(tar_states)))
            assert(tar_target_len > 0)
            cfg_rset["tar_target_len"] = tar_target_len
            cfg_rset["tar_target_len_plus_1"] = tar_target_len + 1
            if cfg_rset.get('home', False):
                rset_book_keep = hrset_tar_idx_t.format(**cfg_rset)
            else:
                rset_book_keep = rset_tar_idx_t.format(**cfg_rset)

            tar_array_len = max(1, tar_target_len)
            my_vars["tar"] = (
                f"array[0..{tar_array_len - 1}] of {cfg_rset['state_type_name']}",
                "".join([f"tar[{i}] := {s};\n" for i, s in enumerate(tar_states)]),
                None,
            )
            my_vars["cur_idx"] = (f"0..{tar_target_len + 1}", "cur_idx := 0;\n", None)
            need_var.add("tar")
            need_var.add("cur_idx")
        else:
            need_var.add("reached_set")
            tup = []
            for t_itm in my_vars["reached_set"]:
                tup.append(t_itm.format(**cfg_rset))
            my_vars["reached_set"] = tuple(tup)
            rset_book_keep = my_vars["reached_set"][2]

        need_var.add("start")
        need_var.add("tracked")

    if "start" in cfg and cfg['start']:
        need_var.add("start")

    if ("prevStateVal" in cfg and cfg['prevStateVal']) or \
       ("past_1_prevStateVal" in cfg and cfg['past_1_prevStateVal']):
        if addr_type_name != "":
            need_var.add("myaddr")
        need_var.add("selc")
        need_var.add("prevStateVal")

    if "past_1_prevState" in cfg and cfg['past_1_prevState']:
        need_var.add("prevProcs_2")
    if "past_1_prevProcReq" in cfg and cfg['past_1_prevProcReq']:
        need_var.add("prevProcReq_2")

    if "past_1_prevStateVal" in cfg and cfg['past_1_prevStateVal']:
        need_var.add("prevStateVal_2")

    if "prevMsgSet_sent" in cfg and cfg['prevMsgSet_sent']:
        need_var.add("prevMsg")
        need_var.add("msg_imm_sent_set")
    if "prevMsgSet_rec" in cfg and cfg['prevMsgSet_rec']:
        need_var.add("msg_imm_rec_set")

    if "msg_chk" in cfg and (cfg['msg_chk']):
        need_var.add("prevMsg")
        need_var.add("msg_sent_set")
        need_var.add("msg_rec_set")

    if "msg_sent" in cfg and (cfg['msg_sent']):
        need_var.add("prevMsg")
        need_var.add("msg_sent_set")

    if "msg_rec" in cfg and (cfg['msg_rec']):
        need_var.add("prevMsg")
        need_var.add("msg_rec_set")

    if "g_msg" in cfg and cfg['g_msg']:
        need_var.add("prevMsg")
        need_var.add("prevMsgSrc")
        need_var.add("prevMsgDst")
        need_var.add("prevSentMsg")
    if cfg.get("msg_prevsent", False): # in cfg and cfg['msg_prevsent']:
        need_var.add("prevSentMsg")
    if "home" in cfg and cfg['home']:
        need_var.add("selh")
        need_var.add("prevHomeNode")
        if addr_type_name != "":
            need_var.add("myaddr")

    if ("cur_node" in cfg and cfg['cur_node']) or  \
    ("msg_chk" in cfg and len(cfg['msg_chk']) > 0) or \
    ("msg_sent" in cfg and len(cfg['msg_sent']) > 0):
        need_var.add("cur_node")
    #print("=>", need_var.iter())
    get_req_def = {}
    cur_req_f = None
    pattern = re.compile(r'procedure get_(evict_req|store_req_end|store_req|load_req)')
    for idx, line in enumerate(lines):
        m = pattern.search(line)
        if m:
            cur_req_f = m.group(1)
        if cur_req_f is not None and "begin" in line:
            get_req_def[cur_req_f] = idx
            cur_req_f = None

    rule_unk = set()
    for idx, line in enumerate(lines):
        if rule_st:
            for_decl = re.match(r'^\s*for\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*:\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*do\b', line, re.IGNORECASE)
            if for_decl:
                rule_for_vars.add(for_decl.group(1))
        line_prime = None
        if "#SENDING" in line and dec:
            line_prime = line
            if "SENDING" in cfg:
                parts = line[:-1].split(",")
                cur_sender = "cur_node"
                if len(parts) <= 2:
                    # meaning the m_msg_dst_fields is defined 
                    msg_var = parts[1].strip() if len(parts) > 1 else parts[-1].strip()
                    line_prime = cfg['SENDING'].format(msg_var=msg_var, dst=f"{msg_var}.{m_msg_dst_field}")
                else: 
                    msg_var = parts[1].strip() if len(parts) > 1 else parts[-1].strip()
                    msg_type = parts[2].strip() if len(parts) > 2 else None
                    raw_dst = parts[4].strip() if len(parts) > 4 else None
                    src = pp_field(parts[3].strip(), msg_var) if len(parts) > 3 else None 
                    dst = pp_field(parts[4].strip(), msg_var) if len(parts) > 4 else None
                    cur_sender = src if src is not None else cur_sender 

                    if isinstance(cfg['SENDING'],tuple):
                        m_type, ss = cfg['SENDING']
                        if msg_type == m_type:
                            line_prime = ss.format(msg_var=msg_var,
                            msg_type=msg_type or "", src=src, dst=dst,
                            raw_dst=raw_dst or "", cur_sender=cur_sender)
                    else:
                        dst_assert_expr = "true"
                        if dst is not None:
                            dst_is_identifier = re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', raw_dst or "") is not None
                            dst_is_loop_var = dst_is_identifier and (raw_dst in rule_for_vars)
                            if not dst_is_loop_var:
                                dst_assert_expr = f"!isundefined({dst})"
                            else:
                                print("HDEBUG ==>", raw_dst)

                        line_prime = cfg['SENDING'].format(
                            msg_var=msg_var,
                            msg_type=msg_type or "",
                            src=src,
                            dst=dst,
                            raw_dst=raw_dst or "",
                            dst_assert_expr=dst_assert_expr, 
                            cur_sender=cur_sender
                        )
                        # line_prime = cfg['SENDING'].format(msg_var=msg_var)
            
        if "#RECEIVING" in line and dec:
            line_prime = line
            if "RECEIVING" in cfg:
                cur_receiver = "cur_node"
                parts = line[:-1].split(",")
                msg_var = parts[1].strip() if len(parts) > 1 else parts[-1].strip()
                if len(parts) <= 2:
                    # meaning the m_msg_dst_fields is defined 
                    line_prime = cfg['RECEIVING'].format(msg_var=msg_var, cur_receiver = cur_receiver)
                else:
                    msg_type = parts[2].strip() if len(parts) > 2 else None
                    raw_src = parts[3].strip() if len(parts) > 3 else None
                    raw_dst = parts[4].strip() if len(parts) > 4 else None
                    if raw_src is None:
                        print("DEB --->", line)
                    src = pp_field(raw_src, msg_var)
                    dst = pp_field(raw_dst, msg_var)
                    cur_receiver = dst if dst is not None else "cur_node"

                    if isinstance(cfg['RECEIVING'], tuple):
                        m_type, ss = cfg['RECEIVING']
                        if msg_type == m_type:
                            line_prime = ss.format(
                                msg_var=msg_var,
                                msg_type=msg_type or "",
                                src=src,
                                dst=dst,
                                raw_src=raw_src or "",
                                raw_dst=raw_dst or "",
                                cur_receiver=cur_receiver,
                            )
                    else:
                        line_prime = cfg['RECEIVING'].format(
                            msg_var=msg_var,
                            msg_type=msg_type or "",
                            src=src,
                            dst=dst,
                            raw_src=raw_src or "",
                            raw_dst=raw_dst or "",
                            cur_receiver=cur_receiver,
                        )
        if "#RETLD" in line and dec: 
            line_prime = line
            if "RETLD" in cfg:
                ret = line[:-1].split(",")[-1]
                # To be relaxed currently return always cachel ine 
                assert(ret == "CL")
                line_prime = cfg['RETLD'] 

        if line_prime is not None:
            if rule_st:
                # within a rule 
                cur_block += line_prime
            else:
                outff_h.write(line_prime)
                # outside a rule
            continue

        match = ruleset_pattern.match(line)
        if match:
            pair_pattern = r"(\w+)\s*:\s*(\w+)"
            pairs = re.findall(pair_pattern, line)
            st.append(("ruleset", pairs)) #match.group(1), match.group(2)))
            print("==> ruleset", pairs)
            outff_h.write(line)
        elif endruleset_pattern.match(line):
            if st:
                st.pop()
            else:
                print(f"Warning: unmatched endruleset at line {idx + 1}: {line.strip()}", file=sys.stderr)
                assert(0)
            outff_h.write(line)
        else:
            rule_match = rule_pattern.match(line)
            if rule_match:
                rule_st = True
                rule_for_vars = set()
                rule_name = rule_match.group(1)
                fnd = False
                print("==->", st)
                for tmpitem in st:
                    # if tmpitem[2] in iterative_types:
                    for pair_ in tmpitem[1]:
                        if pair_[1] in iterative_types:
                            if fnd: 
                                print(f"Unsure which iterative type {rule_name} to use")
                                fnd = False
                                break
                            else:
                                print(f"--> rule {rule_name}, under iterative type", pair_[1], " var name :", pair_[0])
                                fnd = True
                                cur_var_name = pair_[0]
                if not fnd:
                    if 'rule_actor_map' in design_cfg and rule_name in design_cfg['rule_actor_map']: 
                        cur_var_name = design_cfg['rule_actor_map'][rule_name]
                        fnd = True
                    else:
                        print("HERE")
                        rule_unk.add(rule_name)
            if re.search(re.compile(r'endrule;', re.IGNORECASE), line):
                if cur_block:
                    # outff
                    rule_arrow_idx = cur_block.index("==>")
                    # idx = cur_block.index("==>")
                    match = re.search(re.compile("begin", re.IGNORECASE), cur_block)
                    if match: 
                        tar_idx = match.span()[1] + 1 
                    else:
                        tar_idx = rule_arrow_idx + 3
                        # tar_idx = idx + 3
                    if fnd:
                        cur_block = cur_block[:tar_idx] + f"\n book_keep({cur_var_name});\n" + cur_block[tar_idx:]
                    outff_h.write(cur_block)
                    cur_block = ""
                rule_st = False
            if rule_st: 
               cur_block += line 
            else:
                var_start_pattern = re.compile(r'^\s*var\s*', re.IGNORECASE)

                type_start_pattern = re.compile(r'^\s*type\s*', re.IGNORECASE)
                type_st = type_st or type_start_pattern.match(line)

                terminating_keywords = ['var', 'const', 'procedure', 'function', 'rule', 'ruleset', 'startstate', 'invariant', 'externfun', 'externproc' ]
                terminating_pattern = re.compile(r'^\s*(' + '|'.join(terminating_keywords) + r')\b', re.IGNORECASE)
                if not type_dec and type_st and terminating_pattern.match(line):
                    type_dec = True
                    outff_h.write(core_req_type)

                def emit_book_keep():
                    book_keep_s = cfg.get("book_keep", "")
                    opt_var=""
                    # if "reached_set" in need_var.iter():
                    if need_rset_locals:
                        opt_var = f"var\ncur_state:{m_proc_state_type};\nin_stable_state:boolean;\n"
                    outff_h.write(f"procedure book_keep(m: {iterative_types [0]});\n{opt_var}\nbegin\n{book_keep_s}\n")
                    # if "reached_set" in need_var.iter():
                    #     if my_vars["reached_set"][2] is not None:
                    #         outff_h.write(my_vars["reached_set"][2])
                    if rset_book_keep is not None:
                        outff_h.write(rset_book_keep)
                    
                    for itm in need_var.iter():
                        if "reached_set" == itm:
                            continue
                        if my_vars[itm][2] is not None and my_vars[itm][0] is not None:
                            outff_h.write(my_vars[itm][2])
                    outff_h.write("end;\n")

                # if not bk_def and (("procedure" in line.lower()) or ("function" in line.lower())):
                if not bk_def:
                    is_proc_or_func_line = (("procedure" in line.lower()) or ("function" in line.lower()))
                    if defer_book_keep_after_get_state and (book_keep_insert_idx is not None):
                        if idx == book_keep_insert_idx + 1:
                            emit_book_keep()
                            bk_def = True
                    elif is_proc_or_func_line:
                        emit_book_keep()
                        bk_def = True

                if not dec and var_start_pattern.match(line):
                    dec = True
                    outff_h.write(line)
                    decl_s = cfg.get("decl_var", "")
                    for itm in need_var.iter():
                        assert (itm in my_vars)
                        if my_vars[itm][0] is not None:
                            outff_h.write("%s: %s;\n" % (itm, my_vars[itm][0]))
                    outff_h.write(f"\n{decl_s}\n")
                elif "endstartstate" in line:
                    init_state_s = cfg.get("init_state", "")
                    outff_h.write("\n" + init_state_s + "\n")
                    for itm in need_var.iter():
                        if my_vars[itm][1] is not None and my_vars[itm][0] is not None:
                            outff_h.write(my_vars[itm][1])
                    outff_h.write(line)
                else:
                    outff_h.write(line)
                    if not ('track_req' in cfg and cfg['track_req']):
                        continue
                    for k, v in get_req_def.items():
                        # k: type of req 
                        # v: idx
                        if v == idx:
                            if k == "evict_req":
                                outff_h.write(evict_req_t)
                            if k == "store_req":
                                outff_h.write(store_req_t)
                            if k == "store_req_end":
                                outff_h.write(store_req_end_t)
                            if k == "load_req":
                                outff_h.write(load_req_t)
                            
    global print_
    # if not print_:
    for rule_name in rule_unk: 
        print("[WARNING] we don't know which core is being processed by rule: ", rule_name)
    # print_ = True
    print("================================================================================")
def main():
    """Main function to handle command-line arguments."""
    if len(sys.argv) < 3:
        print("Usage: python parse_rules.py <murphi_model_file> <iterative_type_name>", file=sys.stderr)
        sys.exit(1)

    model_file = sys.argv[1]
    iterative_type = []
    for i in range(2, len(sys.argv)):
        iterative_type.append(sys.argv[i])
    # parse_murphi_model(model_file, iterative_type, open("/dev/null", "w"))
    th = open("test.m", "w")
    # parse_murphi_model(model_file, iterative_type, th, {"track_req": True, "prevState": True})
    #parse_murphi_model(model_file, iterative_type, th, {"track_req": False, "prevState": True})
    # parse_murphi_model(model_file, iterative_type, th, {"track_req": False, "prevState": False, "cur_node": True})
    # parse_murphi_model(model_file, iterative_type, th, {"track_req": True, "prevState": True, "past_1_prevState": True, "past_1_prevProcReq": True})
    # with value
    # parse_murphi_model(model_file, iterative_type, th, {"track_req": True, "prevState": True, "past_1_prevState": True, "past_1_prevProcReq": True, "prevStateVal": True, "past_1_prevStateVal": True})
    # reached sete
    # parse_murphi_model(model_file, iterative_type, th, {"track_req": True, "prevState": True, "rset": {"num": 6, "state_type_name": m_proc_state_type, "m_proc_selc": m_proc_selc, "m_proc_state_field": m_proc_state_field, "stable_state_df": "TMP", "block_within_start": ""} })
    # 
    parse_murphi_model(model_file, iterative_type, th, {"track_req": True, "prevState": True, "rset": {"num": 6, "state_type_name": m_proc_state_type, "m_proc_selc": m_proc_selc, "m_proc_state_field": m_proc_state_field, "stable_state_df": "false", "block_within_start": ""}, "prevStateVal": True}, {"val_chk": ("boolean", "val_chk := false;\n", "")})

    th.close()


# Keep star-import behavior but avoid exporting this module's local print wrapper.
__all__ = [name for name in globals() if not name.startswith("_") and name != "print"]

if __name__ == "__main__":
    main()

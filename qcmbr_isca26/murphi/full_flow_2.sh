set -e
D=past_builds/MESI_build
D=past_builds/MSI_fixed_build
D=past_builds/VI_buggy_build

python3 src/s1.py gen
./util/eval_props.sh -n -s s1_req_acc_state -d $D -t 10m -m 65536 
python3 src/s1.py gen_s2
python3 src/s1.py gen_s3
./util/eval_props.sh -n -s s1_3_global_msg -d $D -t 10m -m 65536 
./util/eval_props.sh -n -s s1_2_transition -d $D -t 10m -m 65536
python3 src/s1.py gen_s4 
./util/eval_props.sh -n -s s1_gmsg_cnt -d $D -t 10m -m 65536
python3 src/s1.py pp 

# based on s1_req_acc_state, we see which can perform directly
python3 src/s2.py gen
./util/eval_props.sh -n -s s2_req_proc_state -d $D -t 10m -m 65536
# for those perform without txn, does it feature state/value change
python3 src/s2.py gen_s1
./util/eval_props.sh -n -s s2_2_req_proc_state_to_state_prime_val -d $D -t 10m -m 65536
# if value change, does it always match the argument
python3 src/s2.py gen_s2
./util/eval_props.sh -n -s s2_3_req_proc_val -d $D -t 10m -m 65536
python3 src/s2.py pp


# for getting proof 
# each transition what message sets are sent/received 
# if $SND; then 
python3 src/s1_msg.py gen 
./util/eval_props.sh -n -s s1_msg_per_transition -d $D -t 10m -m 65536
python3 src/s1_msg.py gen_s2
./util/eval_props_py.sh -n -s s1_msg_per_transition_iter -d $D
python3 src/s1_msg.py gen_s3
python3 src/s1_msg.py gen_s4
./util/eval_props.sh -n -s s1_msg_per_transition_cl -d $D -t 10m -m 65536
python3 src/s1_msg.py gen_s5
python3 src/s1_msg.py gen_s6
./util/eval_props.sh -n -s s1_msg_per_transition_val_src -d $D -t 10m -m 65536
python3 src/s1_msg.py gen_s7
./util/eval_props.sh -n -s s1_msg_per_transition_val_change -d $D -t 10m -m 65536
python3 src/s1_msg.py pp

# # fi 
# 
# # for those perform with txn, we see the set of vpicl
python3 src/s3.py gen  
./util/eval_props.sh -n -s s3_rset_txn -d $D -t 10m -m 65536
# what values does each state in a upath take
python3 src/s3.py gen_s2
./util/eval_props.sh -n -s s3_2_reachable_set_val -d $D -t 10m -m 65536
python3 src/s3.py pp

# # if $SND; then 
# # we collect for each rset, the message associated 
python3 src/s4_constrained.py gen
./util/eval_props.sh -n -s s4_constrained -d $D -t 10m -m 65536
python3 src/s4_constrained.py gen_s2
python3 src/s4_constrained.py gen_s3
./util/eval_props.sh -n -s s4_3_v2_src_dst -d $D -t 10m -m 65536

python3 src/s5_core.py gen_assoc_s5
./util/eval_props.sh -n -s s4_4_picl_val_from_msg -d $D -t 10m -m 65536
python3 src/s5_core.py gen_assoc_s6
./util/eval_props.sh -n -s s4_5_msg_val_from_picl -d $D -t 10m -m 65536
python3 src/s5_core.py gen_assoc_s7
./util/eval_props.sh -n -s s4_6_ret_val -d $D -t 10m -m 65536
python3 src/s5_core.py gen_assoc_s8

python3 src/global_chk.py gen
python3 src/global_chk.py gen_s2
./util/eval_props.sh -n -s globl_dir_imp -d $D -t 10m -m 65536
./util/eval_props.sh -n -s global_chk -d $D -t 10m -m 65536
python3 src/global_chk.py pp

dst_always_defined=$(python3 - <<'PY'
import pickle

try:
    with open("build/s1_3_global_msg/_build/aggdict.pkl", "rb") as f:
        data = pickle.load(f)
    print(str(bool(data.get("dst_always_defined", False))).lower())
except Exception:
    print("false")
PY
)
echo $dst_always_defined
if [ "$dst_always_defined" = "true" ]; then
  echo "JJ"
  exit 0
python3 src/home_upath_dir.py gen
./util/eval_props.sh -n -s home_s1_req_acc_state -d $D -t 10m -m 65536
./util/eval_props.sh -n -s home_s0_transition -d $D -t 10m -m 65536

# can home at {s} take in message {m} 1) with owner undefined? 2) with empty sharer lis? 3) with non-empty sharer list ? 4) transition to new coherence state? 
python3 src/home_upath_dir.py gen_s1
./util/eval_props.sh -n -s home_s2_req_acc_proc_state -d $D -t 10m -m 65536


# home_s3_req_acc_msg_src_cond:
# 1) {s} takes in message {m} transitions to {s_prime} always with owner defined and {m}.src is owner?  
# 2) always not owner? 
# 3) {s} takes in message {m} transitions to {s_prime} with {m}.src last sharer
# 4)  {s} takes in message {m} transitions to {s_prime} with {m}.src not last sharer
# home_s3_msg_out_val_sharere_owner
# 1) {s} takes in message {m} transitions to {s_prime} did value change? 
# 2) {s} takes in message {m} transitions to {s_prime} did shaere list change?  
# 3) {s} takes in message {m} transitions to {s_prime} did owner  change?   
python3 src/home_upath_dir.py gen_s1_2

./util/eval_props.sh -n -s home_s3_req_acc_msg_src_cond -d $D -t 10m -m 65536
# home_s3_req_acc_msg_src_cond/agg.pkl: refined conditions
./util/eval_props.sh -n -s home_s3_msg_out_val_sharere_owner -d $D -t 10m -m 65536

python3 src/home_upath_dir.py gen_s2
# out msg set
./util/eval_props_py.sh -s home_s3_msg_out_set -d $D
# 1) if {s} takes in message {m} transition to {s_prime} change value, asser the value same as the message value 
# 2) if {s} takes in message {m} transition to {s_prime} has change of owner, assert the new owner to be the {m}.src
# 3) if {s} takes in message {m} transition to {s_prime} has change of sharere list, see if a) empty b) add src, c) remove src 
./util/eval_props.sh -n -s home_s3_src_owner_sharere_extract -d $D -t 10m -m 65536
python3 src/home_upath_dir.py gen_s3
./util/eval_props.sh -n -s home_s3_msg_val_src_dst -d $D -t 10m -m 65536
# 
python3 src/home_upath_dir.py gen_s4

else 

  python3 src/home_upath.py gen
  ./util/eval_props.sh -n -s home_s0_transition -d $D -t 10m -m 65536
  ./util/eval_props.sh -n -s home_s1_req_acc_state -d $D -t 10m -m 65536
  python3 src/home_upath.py gen_s1
  ./util/eval_props.sh -n -s home_s2_req_acc_proc_state -d $D -t 10m -m 65536
  python3 src/home_upath.py gen_s1_2
  ./util/eval_props.sh -n -s home_s2_msg_out  -d $D -t 10m -m 65536
  python3 src/home_upath.py gen_s2
  ./util/eval_props.sh -n -s home_s3_msg_out_info -d $D -t 10m -m 65536
  python3 src/home_upath.py gen_s3

fi 
# at what state does it take in message
python3 src/postfix_upath.py gen
./util/eval_props.sh -n -s core_s1_req_acc_state -d $D -t 10m -m 65536

# if at state takes in message, what state prime
python3 src/postfix_upath.py gen_s2
./util/eval_props.sh -n -s core_s2_req_acc_state_prime -d $D -t 10m -m 65536

# if at state takes in message, any value change and what message are sent out 
python3 src/postfix_upath.py gen_s3
./util/eval_props.sh -n -s core_s3_req_send -d $D -t 10m -m 65536

# if any message is sent out, its value is the same as cache lien value 
python3 src/postfix_upath.py gen_s4
./util/eval_props.sh -n -s core_s4_req_send_val -d $D -t 10m -m 65536
python3 src/postfix_upath.py pp

echo "SUCCESS"
exit 



################################################################################
# current 
################################################################################


  # python3 src/home_upath_dir.py gen
  # ./util/eval_props.sh -s home_s1_req_acc_state 
  # ./util/eval_props.sh -s home_s0_transition

  # # can home at {s} take in message {m} 1) with owner undefined? 2) with empty sharer lis? 3) with non-empty sharer list ? 4) transition to new coherence state? 
  # python3 src/home_upath_dir.py gen_s1
  # ./util/eval_props.sh -s home_s2_req_acc_proc_state

  # # home_s3_req_acc_msg_src_cond:
  # # 1) {s} takes in message {m} transitions to {s_prime} always with owner defined and {m}.src is owner?  
  # # 2) always not owner? 
  # # 3) {s} takes in message {m} transitions to {s_prime} with {m}.src last sharer
  # # 4)  {s} takes in message {m} transitions to {s_prime} with {m}.src not last sharer
  # # home_s3_msg_out_val_sharere_owner
  # # 1) {s} takes in message {m} transitions to {s_prime} did value change? 
  # # 2) {s} takes in message {m} transitions to {s_prime} did shaere list change?  
  # # 3) {s} takes in message {m} transitions to {s_prime} did owner  change?   
  # python3 src/home_upath_dir.py gen_s1_2

  # ./util/eval_props.sh -s home_s3_req_acc_msg_src_cond
  # # home_s3_req_acc_msg_src_cond/agg.pkl: refined conditions
  # ./util/eval_props.sh -s home_s3_msg_out_val_sharere_owner

  # python3 src/home_upath_dir.py gen_s2
  # # out msg set
  # ./util/eval_props_py.sh -s home_s3_msg_out_set
  # # 1) if {s} takes in message {m} transition to {s_prime} change value, asser the value same as the message value 
  # # 2) if {s} takes in message {m} transition to {s_prime} has change of owner, assert the new owner to be the {m}.src
  # # 3) if {s} takes in message {m} transition to {s_prime} has change of sharere list, see if a) empty b) add src, c) remove src 
  # ./util/eval_props.sh -s home_s3_src_owner_sharere_extract

  # # given result in home_s3_msg_out_set we go on to see 
  # # a. dst: 1) dst always (not) src for each msg in the msg set, 2) dst always owner or not, 3) dst always shaere or not except requester
  # # b. value 
  # python3 src/home_upath_dir.py gen_s3
  # ./util/eval_props.sh -s home_s3_msg_val_src_dst
  # # 
  # python3 src/home_upath_dir.py gen_s4

# # fi
# 
# # TARDIR=build python3 src/s4.py gen_assoc_s4
# # ./util/eval_props.sh -s s4_3_msg_cnt_src_dst
# 

# 
# OLD_DIR=past_builds/VI_build_v0
# 
# compare_stage() {
#   s_arg="$1"
#   echo "==> compare stage: $s_arg"
#   for itm in build/"$s_arg"/out/*.m; do
#     [ -e "$itm" ] || continue
#     base_name=$(basename "$itm")
#     old_file="$OLD_DIR/$s_arg/out/$base_name"
#     if [ ! -f "$old_file" ]; then
#       echo "MISSING_OLD $old_file"
#       continue
#     fi
#     #echo "$old_file"
#     #echo "$itm"
#     diff "$old_file" "$itm"
#   done
# }
# 
# copy_old_build() {
#   s_arg="$1"
#   src_dir="$OLD_DIR/$s_arg/_build"
#   dst_dir="build/$s_arg"
#   if [ ! -d "$src_dir" ]; then
#     echo "MISSING_OLD_BUILD $src_dir"
#     return
#   fi
#   cp -r "$src_dir" "$dst_dir"
# }
# 
# python3 src/postfix_upath.py gen
# #compare_stage core_s1_req_acc_state
# #copy_old_build core_s1_req_acc_state
# 
#  # if at state takes in message, what state prime
# #python3 src/postfix_upath.py gen_s2
# # compare_stage core_s2_req_acc_state_prime
# #copy_old_build core_s2_req_acc_state_prime
# # 
# # if at state takes in message, any value change and what message are sent out 
# # python3 src/postfix_upath.py gen_s3
# # compare_stage core_s3_req_send
# # copy_old_build core_s3_req_send
# # 
# # if any message is sent out, its value is the same as cache lien value 
# # python3 src/postfix_upath.py gen_s4
# # compare_stage core_s4_req_send_val
# # copy_old_build core_s4_req_send_val
# # python3 src/postfix_upath.py pp
# # 
#  # for not dst_always_defined
# # python3 src/home_upath.py gen
# # compare_stage home_s0_transition
# # copy_old_build home_s0_transition
# #  compare_stage home_s1_req_acc_state
# #  copy_old_build home_s1_req_acc_state
# #  python3 src/home_upath.py gen_s1
# #  compare_stage home_s2_req_acc_proc_state
# #  copy_old_build home_s2_req_acc_proc_state
# #   python3 src/home_upath.py gen_s1_2
# #   compare_stage home_s2_msg_out
# #   copy_old_build home_s2_msg_out
# #   python3 src/home_upath.py gen_s2
# #   compare_stage home_s3_msg_out_info
# #   copy_old_build home_s3_msg_out_info

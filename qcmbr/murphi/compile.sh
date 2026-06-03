RUN_FULL=false
if [ $1 == "1" ]; then
  echo "buggy vi"
  ./switch.sh VI_BUGGY
  if $RUN_FULL; then 
    ./full_flow_2.sh
  fi
  python3 asm_test.py vi_buggy_test_tmp.uarch no > asm_buggy_vi.log
else 
  echo "fixed vi"
  ./switch.sh VI
  if $RUN_FULL; then 
    ./full_flow_2.sh
  fi
  python3 asm_test.py vi_buggy_test_tmp.uarch no > asm_buggy_vi.log
fi 

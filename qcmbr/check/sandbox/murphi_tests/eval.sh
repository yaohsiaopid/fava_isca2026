if [ $1 == "run" ]; then
mkdir -p results_new
../../util/runtests_loop.sh -m  ../../../murphi/artifact/vi_buggy_test.uarch -p ../../tests/coherence_augmented
column -s, -t < results_new/latest/vi_buggy_test.csv
fi

if [ $1 == "run_fix" ]; then
mkdir -p results_new
../../util/runtests_loop.sh -m  ../../../murphi/artifact/vi_test.uarch -p ../../tests/coherence_augmented
column -s, -t < results_new/latest/vi_test.csv
fi

if [ $1 == "view" ]; then
  ./mini.sh  ../../tests/coherence_augmented/coWR_1thd.test ../../../murphi/artifact/vi_buggy_test.uarch | grep "===> v"
  xdg-open t.smt2.c.trd.png
fi

if [ $1 == "mcm" ]; then
mkdir -p results_new
../../util/runtests_loop.sh -m  ../../../murphi/artifact/vi_test.uarch -p ../../tests/SC_augmented
column -s, -t < results_new/latest/vi_test.csv
fi



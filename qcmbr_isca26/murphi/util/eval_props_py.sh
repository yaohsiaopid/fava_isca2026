#!/bin/bash
# all_inputs = {stage: glob_wildcards(f"build/{stage}/out/{{filename}}.m") for stage in STAGES}
# all_outputs = {stage: expand(f"build/{stage}/_build/{{filename}}.txt", filename=all_inputs[stage].filename) for stage in STAGES}

step_dirname=""
no_overwrite=0
while getopts "d:s:n" opt; do
  case $opt in
    d) tardir="$OPTARG" ;;
    s) step_dirname="$OPTARG" ;;
    n) no_overwrite=1 ;;
    \?) usage ;;
  esac
done
if [ -z "$tardir" ]; then
  exit 0
fi
echo $tardir
if [ -z "$step_dirname" ]; then
  echo "Error: Stage name must be provided with -s."
  exit 0
fi
INPUT_DIR="${tardir}/${step_dirname}/out"
echo "---> $step_dirname"
echo "--> $INPUT_DIR"
if [ ! -d "$INPUT_DIR" ]; then
    echo "Error: Input directory not found: $INPUT_DIR"
    exit 1
fi

# Enumerate all basenames of .m files (e.g., "prop_1", "prop_2")

# TESTS=$(find "$INPUT_DIR" -name "*.m" -exec basename {} .m \;)
TESTS=$(find "$INPUT_DIR" -name "*.py" -exec basename {} .py \;)

OUTPUTDIR="${tardir}/${step_dirname}/_build"

declare -a TESTS_TO_RUN
if [ "$no_overwrite" -eq 1 ]; then
    echo "No-overwrite mode enabled. Checking for completed tests..."
    for t in $TESTS; do
    tmp_nm="${t%baseff}"
    r="${t%_iter}"
    if [ -f "${OUTPUTDIR}/${r}_19.txt" ]; then
      TESTS_TO_RUN+=("$tmp_nm")
      echo $tmp_nm
    else 
      if [ -f "${OUTPUTDIR}/${t}.pkl" ]; then
      echo "Skipping completed test: $tmp_nm"
      else
      TESTS_TO_RUN+=("$tmp_nm")
      echo $tmp_nm
      fi
    fi 
    done
else
    while read -r -d '' R;
    do 
      A=$(basename $R)
      TESTS_TO_RUN+=("${A%.*}")
      echo "${A%.*}"
    done < <(find "$INPUT_DIR" -name "*.py" -print0 )
fi
echo "JOBS: ${#TESTS_TO_RUN[@]}"

if [ ${#TESTS_TO_RUN[@]} -eq 0 ]; then
    echo "All tests are already complete. Nothing to do."
    exit 0
fi

if [ ! -f "util/mini_eval.sh" ]; then
  exit 0
fi 

if [ ! -d $OUTPUTDIR ]; then
    mkdir -p  $OUTPUTDIR
fi
run_single_test() {
    basename=$1
    sed -i 's/iter_count > 20/iter_count > 30/g' ${tardir}/${step_dirname}/out/${basename}.py

    python3 ${tardir}/${step_dirname}/out/${basename}.py > ${tardir}/${step_dirname}/_build/${basename}.py.log
}

export -f run_single_test
export step_dirname OUTPUTDIR tardir

# --halt now,fail=1 

# parallel --jobs 0 --bar run_single_test ::: $TESTS_TO_RUN
# parallel -j 32 --memfree 64G --bar run_single_test ::: $TESTS_TO_RUN
parallel -j 10 --memfree 64G --bar run_single_test ::: "${TESTS_TO_RUN[@]}"

#echo "Found tests to process for stage '$step_dirname':"
#echo "$TESTS"
#for t in $TESTS
#do
#    echo "--> $t"
#done 
#echo "---"
#exit 0




#!/bin/bash
# This script is a modified version of eval_props_py.sh to use SLURM for job scheduling instead of GNU Parallel.

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

# Enumerate all basenames of .py files
TESTS=()

# TESTS=()
# TESTS+=("cache_I_ci_load_1_trace_rec_iter")

OUTPUTDIR="${tardir}/${step_dirname}/_build"

if [ "$no_overwrite" -eq 1 ]; then
  shopt -s nullglob
  for txt_file in "${tardir}/${step_dirname}/_build/"*.txt; do
    if ! grep -Eq "Assertion failed|Invariant.*failed|No error found" "$txt_file"; then
      txt_base=$(basename "$txt_file" .txt)
      ff_t="${txt_base%_*}"
      candidate="${ff_t}_iter"
      exists=0
      for t in "${TESTS[@]}"; do
        if [ "$t" = "$candidate" ]; then
          exists=1
          break
        fi
      done
      if [ "$exists" -eq 0 ]; then
        TESTS+=("$candidate")
      fi
    fi
  done
  shopt -u nullglob
else
  while IFS= read -r t; do
    TESTS+=("$t")
  done < <(find "$INPUT_DIR" -name "*.py" -exec basename {} .py \;)
fi

if [ ! -d $OUTPUTDIR ]; then
    mkdir -p  $OUTPUTDIR
fi

# Build array for SLURM
tests=("${TESTS[@]}")
ntests=${#tests[@]}
echo $ntests
TESTLIST="${OUTPUTDIR}/tests.list"
printf "%s\n" "${tests[@]}" > "$TESTLIST"

OPTARG=""
if [ "$no_overwrite" -eq 1 ]; then
  OPTARG=" -n"
fi
sbatch <<EOF
#!/bin/bash
#SBATCH --job-name=${step_dirname}
#SBATCH --output=${OUTPUTDIR}/%x_%A_%a.py.log
#SBATCH --error=${OUTPUTDIR}/%x_%A_%a.py.err
#SBATCH --mem=70G
#SBATCH --cpus-per-task=1
#SBATCH --time=00:40:00
#SBATCH --partition=cafe-lo
#SBATCH --mail-user=yaohsiao@stanford.edu
#SBATCH --mail-type=END
#SBATCH --account=cafe
#SBATCH --array=0-$(($ntests-1))

test=\$(sed -n "\$((SLURM_ARRAY_TASK_ID+1))p" "$TESTLIST")
python3 ${tardir}/${step_dirname}/out/\${test}.py $OPTARG
EOF

echo "Job array submitted."


# echo "Submitting jobs to SLURM..."
# for test in $TESTS; do
#     if [ "$no_overwrite" -eq 1 ] && [ -f "${OUTPUTDIR}/${test}.py.log" ]; then
#         echo "Skipping completed test: $test"
#         continue
#     fi
#     # if [ -f "${OUTPUTDIR}/${test}.pkl" ]; then
#     #   continue
#     # fi

#     echo $test
#     sbatch <<EOF
# #!/bin/bash
# #SBATCH --job-name=${test}_job
# #SBATCH --output=${OUTPUTDIR}/${test}.py.log
# #SBATCH --error=${OUTPUTDIR}/${test}.py.err
# #SBATCH --mem=40G
# #SBATCH --cpus-per-task=1
# #SBATCH --time=01:00:00
# #SBATCH --partition=cafe-lo
# #SBATCH --mail-user=yaohsiao@stanford.edu
# #SBATCH --mail-type=END
# #SBATCH --account=cafe

# python3 ${tardir}/${step_dirname}/out/${test}.py
# EOF

# done

echo "All jobs submitted."


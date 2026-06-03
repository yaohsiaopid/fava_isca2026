#!/bin/bash
# Slurm version of eval_props.sh (submit jobs via sbatch --array)

step_dirname=""
no_overwrite=0
tar_build="build"
partition="cafe-lo"
time_limit="20:00:00"
mytimelimit="3h"
mymem="131072"
mem_per_task="140G"
# mem_per_task="70G"
cpus_per_task=1
job_name="eval_props"

usage() {
  echo "Usage: $0 -s <stage> [-d <build_dir>] [-n] [-p <partition>] [-t <time>] [-m <mem>] [-c <cpus>] [-J <job_name>]"
}

while getopts "d:s:np:t:m:c:J:" opt; do
  case $opt in
    d) tar_build="$OPTARG";;
    s) step_dirname="$OPTARG";;
    n) no_overwrite=1;;
    p) partition="$OPTARG";;
    t) mytimelimit="$OPTARG";;
    m) mymem="$OPTARG";;
    c) cpus_per_task="$OPTARG";;
    J) job_name="$OPTARG";;
    \?) usage; exit 1;;
  esac
done

if [[ "$mymem" =~ ^[0-9]+$ ]] && (( mymem < 70000 )); then
  mem_per_task="70G"
fi
echo "--> $mem_per_task"

if [ -z "$tar_build" ]; then
  echo "-d <> tar build empty"
  exit 0
fi
if [ -z "$step_dirname" ]; then
  echo "Error: Stage name must be provided with -s."
  exit 0
fi

INPUT_DIR="${tar_build}/${step_dirname}/out"
OUTPUTDIR="${tar_build}/${step_dirname}/_build"

OUT_DIR="${tar_build}/${step_dirname}/out"
BUILD_DIR="${tar_build}/${step_dirname}/_build"
if [ ! -d "$INPUT_DIR" ]; then
  echo "Error: Input directory not found: $INPUT_DIR"
  exit 1
fi

shopt -s nullglob
txt_files=("$BUILD_DIR"/*.txt)
shopt -u nullglob

if [ ${#txt_files[@]} -eq 0 ]; then
  echo "No .txt files found under $BUILD_DIR. Nothing to re-evaluate."
  exit 0
fi

# Enumerate all basenames of .m files
TESTS=$(find "$INPUT_DIR" -name "*.m" -exec basename {} .m \;)

if [ ! -d "$OUTPUTDIR" ]; then
  mkdir -p "$OUTPUTDIR"
fi

TEST_LIST_FILE="${OUTPUTDIR}/tests_to_run.list"
: > "$TEST_LIST_FILE"


declare -a TESTS_TO_RUN
while IFS= read -r txt_path; do
  base_name="$(basename "$txt_path" .txt)"
  if [ -f "${OUT_DIR}/${base_name}.m" ]; then
    # TESTS_TO_RUN+=("$base_name")
    echo "$base_name" >> "$TEST_LIST_FILE"
  else
    echo "Skipping $base_name: missing source ${OUT_DIR}/${base_name}.m"
  fi
done < <(grep -EL "Assertion failed|Invariant.*failed|No error found" "${txt_files[@]}" || true)



NUM_TESTS=$(wc -l < "$TEST_LIST_FILE" | tr -d ' ')
if [ "$NUM_TESTS" -eq 0 ]; then
  echo "All tests are already complete. Nothing to do."
  exit 0
fi

echo "Submitting $NUM_TESTS tests via Slurm array..."

SLURM_SCRIPT="${OUTPUTDIR}/eval_props_slurm_job.sh"
cat > "$SLURM_SCRIPT" <<'EOF'
#!/bin/bash


basename=$(sed -n "${SLURM_ARRAY_TASK_ID}p" "${TEST_LIST_FILE}")
if [ -z "$basename" ]; then
  echo "No test name found for SLURM_ARRAY_TASK_ID=$SLURM_ARRAY_TASK_ID"
  exit 1
fi

output_log="${OUTPUTDIR}/${basename}.txt"
err_log="${OUTPUTDIR}/${basename}.err.log"
input="${tar_build}/${step_dirname}/out/${basename}.m"

: > "$output_log"
: > "$err_log"

mu "$input" &> "$err_log"
res="${tar_build}/${step_dirname}/out/${basename}.cpp"
if [ -f "$res" ]; then
  output_cpp="${OUTPUTDIR}/${basename}.cpp"
  mv "$res" "$output_cpp"
  output_bin="${OUTPUTDIR}/${basename}"
  g++ -g -w -I/cafe/u/yaohsiao/sandbox/murphi_playground/HeteroGen/CMurphi/include "$output_cpp" -o "$output_bin"
  echo "${mytimelimit}"
  while :; do
      # stdbuf -oL -eL timeout 3h /usr/bin/time -f "Time: %e seconds" "$output_bin" -m131072 -tv &>> "$output_log"
      stdbuf -oL -eL timeout "${mytimelimit}" /usr/bin/time -f "Time: %e seconds" "$output_bin" -m"${mymem}" -tv &>> "$output_log"
      log_size=$(stat -c%s "$output_log" 2>/dev/null || echo 0)
      [ "$log_size" -gt 1 ] && break
      : > "$output_log"
  done
  # ( timeout 2h /usr/bin/time -f "Time: %e seconds" "$output_bin" -m32768 -tv ) &>> "$output_log"
  cp "$input" "${OUTPUTDIR}/${basename}.m"
else
  echo "ERROR COMPILE" >> "$err_log"
fi
EOF

chmod +x "$SLURM_SCRIPT"

SBATCH_ARGS=("--mail-user=yaohsiao@stanford.edu" "--mail-type=END" "--account=cafe" "--job-name=${job_name}" "--array=1-${NUM_TESTS}" "--cpus-per-task=${cpus_per_task}" "--mem=${mem_per_task}" "--time=${time_limit}" "--output=${OUTPUTDIR}/slurm-%A_%a.out" "--error=${OUTPUTDIR}/slurm-%A_%a.err")
if [ -n "$partition" ]; then
  SBATCH_ARGS+=("--partition=${partition}")
fi

sbatch "${SBATCH_ARGS[@]}" \
  --export=ALL,tar_build="$tar_build",step_dirname="$step_dirname",OUTPUTDIR="$OUTPUTDIR",TEST_LIST_FILE="$TEST_LIST_FILE",mytimelimit="$mytimelimit",mymem="$mymem" \
  "$SLURM_SCRIPT"


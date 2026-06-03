#!/bin/bash
# all_inputs = {stage: glob_wildcards(f"build/{stage}/out/{{filename}}.m") for stage in STAGES}
# all_outputs = {stage: expand(f"build/{stage}/_build/{{filename}}.txt", filename=all_inputs[stage].filename) for stage in STAGES}
time_limit=
mem=
step_dirnames=()
no_overwrite=0
tar_build="build"
proof=0
while getopts "d:s:t:m:np" opt; do
  case $opt in
    d) tar_build="$OPTARG";;
    s) step_dirnames+=("$OPTARG") ;;
    t) time_limit="$OPTARG" ;;
    m) mem="$OPTARG" ;;
    n) no_overwrite=1 ;;
    p) proof=1 ;;
    \?) usage ;;
  esac
done
if [ -z "$tar_build" ]; then
  echo "-d <> tar build empty"
  exit 0
fi
if [ ${#step_dirnames[@]} -eq 0 ]; then
  echo "Error: At least one stage name must be provided with -s."
  exit 0
fi
if [ -z "$time_limit" ]; then echo "time limit?"; exit 0; fi
if [ -z "$mem" ]; then echo "mem limit?"; exit 0; fi

for step_dirname in "${step_dirnames[@]}"; do
INPUT_DIR="${tar_build}/${step_dirname}/out"
echo "---> $step_dirname"
echo "--> $INPUT_DIR"
if [ ! -d "$INPUT_DIR" ]; then
    echo "Error: Input directory not found: $INPUT_DIR"
    exit 1
fi

# Enumerate all basenames of .m files (e.g., "prop_1", "prop_2")

TESTS=$(find "$INPUT_DIR" -name "*.m" -exec basename {} .m \;)

OUTPUTDIR="${tar_build}/${step_dirname}/_build"

declare -a TESTS_TO_RUN
if [ "$no_overwrite" -eq 1 ]; then
    echo "No-overwrite mode enabled. Checking for completed tests..."
    for t in $TESTS; do
        if [ -f "${OUTPUTDIR}/${t}.txt" ]; then
            if { [ "$proof" -eq 1 ] && grep -Eq "Assertion failed|Invariant.*failed|No error found" "${OUTPUTDIR}/${t}.txt"; } || [ "$proof" -ne 1 ]; then
                echo "Skipping completed test: $t"
            else
                TESTS_TO_RUN+=("$t")
            fi
        else
            TESTS_TO_RUN+=("$t")
        fi
    done
else
    while read -r -d '' R;
    do 
      A=$(basename $R)
      TESTS_TO_RUN+=("${A%.*}")
      echo "${A%.*}"
    done < <(find "$INPUT_DIR" -name "*.m" -print0 )
fi
echo "${#TESTS_TO_RUN[@]}"
if [ ${#TESTS_TO_RUN[@]} -eq 0 ]; then
    echo "All tests are already complete. Nothing to do."
    #exit 0
fi
# echo "${TESTS_TO_RUN[@]}"

if [ ! -d $OUTPUTDIR ]; then
    mkdir -p  $OUTPUTDIR
fi
run_single_test() {
    basename=$1
    output_log="${OUTPUTDIR}/${basename}.txt"
    echo "" > $output_log
    err_log="${OUTPUTDIR}/${basename}.err.log"
    input="${tar_build}/${step_dirname}/out/${basename}.m"
    mu ${input} &> $err_log
    res="${tar_build}/${step_dirname}/out/${basename}.cpp"
    if [ -f $res ]; then 
        output_cpp="${OUTPUTDIR}/${basename}.cpp"
        mv ${res} ${output_cpp}
        output_bin="${OUTPUTDIR}/${basename}"
        g++ -g -w -I/cafe/u/yaohsiao/sandbox/murphi_playground/HeteroGen/CMurphi/include ${output_cpp} -o ${output_bin}
        # run 
        # timeout? 
        # timeout 15m  /usr/bin/time -f "Time: %e seconds" "$output_bin" -m16384 -tv >>"$output_log" 2>&1 || true
        # ( timeout 75m  /usr/bin/time -f "Time: %e seconds" "$output_bin" -m32768 -tv ) &>> $output_log 
        ( timeout $time_limit  /usr/bin/time -f "Time: %e seconds" "$output_bin" -m"${mem}" -tv ) &>> $output_log 

        # : > "$output_log"
        # while :; do
        #     stdbuf -oL -eL timeout 1h /usr/bin/time -f "Time: %e seconds" "$output_bin" -m32768 -tv &>> "$output_log"
        #     log_size=$(stat -c%s "$output_log" 2>/dev/null || echo 0)
        #     [ "$log_size" -gt 1 ] && break
        #     : > "$output_log"
        # done
        # /usr/bin/time -o ${time_log} -f "Time: %e seconds" ${output_bin} -m8192 > ${output_log} || true
        cp $input "${OUTPUTDIR}/${basename}.m"
    else 
        echo "ERROR COMPILE" >> $err_log
    fi 
}

export -f run_single_test
export step_dirname OUTPUTDIR tar_build mem time_limit

# --halt now,fail=1 

#
JOBNUM=5
RESERVE_GB=64

# GNU parallel --memfree is a global floor, not a per-job limit.
# Derive a safer job cap from total RAM and the per-test Murphi -m setting.
effective_jobs="$JOBNUM"
if [[ "$mem" =~ ^[0-9]+$ ]]; then
    TOTAL_MEM_KB=$(awk '/MemTotal/ {print $2}' /proc/meminfo)
    RESERVE_KB=$(( RESERVE_GB * 1024 * 1024 ))
    MEM_PER_JOB_KB=$(( mem * 1024 ))

    if [ -n "$TOTAL_MEM_KB" ] && [ "$TOTAL_MEM_KB" -gt "$RESERVE_KB" ] && [ "$MEM_PER_JOB_KB" -gt 0 ]; then
        max_jobs_by_mem=$(( (TOTAL_MEM_KB - RESERVE_KB) / MEM_PER_JOB_KB ))
        if [ "$max_jobs_by_mem" -lt 1 ]; then
            max_jobs_by_mem=1
        fi
        if [ "$effective_jobs" -gt "$max_jobs_by_mem" ]; then
            effective_jobs="$max_jobs_by_mem"
        fi
    fi
else
    echo "Warning: mem limit '$mem' is not a plain MB integer; skipping memory-based job cap."
fi

echo "parallel jobs requested: $JOBNUM"
echo "parallel jobs effective: $effective_jobs (reserve ${RESERVE_GB}G free)"
# if [[ $(hostname) == *"cafe1"* ]]; then
#   TOTAL_MEM_MB=${SLURM_MEM_PER_NODE:-131072}
#   JOBNUM=$(( TOTAL_MEM_MB / 32768 ))
#   if [ "$JOBNUM" -lt 1 ]; then JOBNUM=1; fi
#   echo "Hostname matched 'cafe1'. Setting parallel jobs to: $JOBNUM"
# fi
# parallel --jobs 0 --bar run_single_test ::: $TESTS_TO_RUN
# parallel -j 32 --memfree 64G --bar run_single_test ::: $TESTS_TO_RUN
parallel --load 80% -j "$effective_jobs" --memfree "${RESERVE_GB}G" --delay 5s --bar run_single_test ::: "${TESTS_TO_RUN[@]}"
#parallel --memfree 64G --bar run_single_test ::: "${TESTS_TO_RUN[@]}"

#echo "Found tests to process for stage '$step_dirname':"
#echo "$TESTS"
#for t in $TESTS
#do
#    echo "--> $t"
#done 
#echo "---"
#exit 0
echo "--> checking if any compilation fail: "
pushd $OUTPUTDIR
find . -name "*.err.log" -exec grep -L "Code generated" {} \;
popd

TESTS=$(find "$INPUT_DIR" -name "*.m" -exec basename {} .m \;)
for t in $TESTS; do
    if [ -f "${OUTPUTDIR}/${t}.txt" ]; then
        if { [ "$proof" -eq 1 ] && grep -Eq "Assertion failed|Invariant.*failed|No error found" "${OUTPUTDIR}/${t}.txt"; } || [ "$proof" -ne 1 ]; then
            continue
        else
            echo "undetermined!!!!  ${OUTPUDIR}/${t}.txt"    
        fi
    else
        echo "no txt?  ${OUTPUDIR}/${t}.txt"
    fi
done

done  # end for step_dirname

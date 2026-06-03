#!/bin/bash
# 1. testdir
# 2. if augment not exists and need augment, then augment
# 3. copy the tests to results_new 
PIPEBIN=/usr/local/bin/pipecheck
echo "---> pipecheck at $PIPEBIN"
DOTBIN=$(which dot)
if [[ $(hostname) =~ cafe-jg* ]]; then
  DOTBIN=/bin/dot
  NEATOBIN=/bin/neato
fi
TIMEOUT_DURATION="1h"
# --- Argument Parsing ---
PIPELINE_NAME=""
TEST_PATH=""
OUTPUT_DIR=""
GGRAPH=false
COH=false
RDIR=""
NATIVE=false
STATS_DIR=""
# Use getopts for named arguments
while getopts m:p:o:t:cnr:s: opt; do
  case $opt in
    m)
      PIPELINE_NAME="$OPTARG"
      ;;
    p)
      TEST_PATH="$OPTARG"
      ;;
    o)
      OUTPUT_DIR="$OPTARG"
      GGRAPH=true  # If -o is provided, GGRAPH is true
      ;;
    t)
      TIMEOUT_DURATION="$OPTARG"
      ;;
    c)
      COH=true
      ;;
    n)
      NATIVE=true;
      ;;
    r) 
    RDIR="$OPTARG"
    ;;
    s)
      STATS_DIR="$OPTARG"
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      exit 1
      ;;
    :)
      echo "Option -$OPTARG requires an argument." >&2
      exit 1
      ;;
  esac
done

if [ -z "$PIPELINE_NAME" ] || [ -z "$TEST_PATH" ]
then
  echo "Usage: ./runtests.sh -m <pipeline name> -p <path to tests> [-o <output dir>] [-c] [-s <existing results dir>]"
  echo "  -m : pipeline name (required)"
  echo "  -p : path to tests (required)"
  echo "  -o : output directory (optional, enables graph generation)"
  echo "  -c : enable COH (optional, sets COH boolean to true)"
  echo "  -s : existing results directory for stats-only mode (optional, skips parallel test execution)"
  echo "Examples:"
  echo "  sc: /cafe/u/yaohsiao/sandbox/check_suite/rtlcheck/tests/rtlcheck/SC/ "
  echo "  tso: /cafe/u/yaohsiao/opt/coatcheck/tests/x86tso/ "
  echo "  coh_test: ./tests"
  exit 1
fi
# --- End Argument Parsing ---
OPT=""
if [ -f "$PIPELINE_NAME" ]; then
  LAST_STAGE_NUMBER=$(grep -E "StageName ([0-9]+) " "$PIPELINE_NAME" | tail -n 1 | awk '{print $2}')
  if [ "$LAST_STAGE_NUMBER" -gt 30 ]; then
    #PIPEBIN=/cafe/u/yaohsiao/docs/coatcheck_dev/src/pipecheck_140
    OPT+=" -s $((LAST_STAGE_NUMBER + 2)) "
  fi 
else
  exit 0
fi


tmpdir=$TEST_PATH
TESTBASE="${tmpdir##*/}"
TARNAME=$(basename $PIPELINE_NAME)
TARNAME="${TARNAME%.*}"
#mkdir -p fig 
# Store all of the tests in the path tests/x86tso into TESTS
if [ ! -d "$TEST_PATH" ]; then
  exit 1 
fi 
DIRNAME="$TEST_PATH"
#if $COH ; then
#    tdir=$(dirname $(realpath $0))
#    tdir="${tdir%/*}"
#    python3 $tdir/src/instrument_test.py -d $TEST_PATH
#    DIRNAME="${DIRNAME}_augmented"
#fi

echo "--> $DIRNAME"
if [ ! -d "$DIRNAME" ]; then
  exit 1 
fi 
if [ -n "$RDIR" ]; then
  TESTS=$(ls $DIRNAME | sed "s/.test//" | while read -r test; do
    if grep -q "timeout" "$RDIR/$test/$test.log"; then
      echo "$test"
    fi
  done)
else
  # Ensure TESTS are treated as strings and not commands
  # TESTS=$(ls $DIRNAME | grep "test$" | sed "s/.test//")
  TESTS=$(ls $DIRNAME | grep "test$" | sed "s/.test//" | while read -r test; do
    echo "$test"
  done)
fi

if [ -z "$OUTPUT_DIR" ]; then
    OUTPUTDIR=results_new/graphs-$TARNAME-$(date +"%m-%d-%y--%H-%M-%S-%p")-$TESTBASE
else
    OUTPUTDIR=$OUTPUT_DIR/results_new/graphs-$TARNAME-$(date +"%m-%d-%y--%H-%M-%S-%p")-$TESTBASE
fi

if [ -n "$STATS_DIR" ]; then 
OUTPUTDIR=$STATS_DIR
echo "HERE"
else 
mkdir -p $OUTPUTDIR

# rm -f latest
# ln -s $OUTPUTDIR latest

cp $PIPELINE_NAME $OUTPUTDIR
mkdir -p $OUTPUTDIR/tests
cp $DIRNAME/*.test $OUTPUTDIR/tests

echo "Running with COH enabled." | tee $OUTPUTDIR/$TARNAME.log
date | tee $OUTPUTDIR/$TARNAME.log
echo "Test,Time,TimeSMT,Bugs,Strict,Inst#" > $OUTPUTDIR/$TARNAME.csv


run_single_test() {
  t=$1
  echo "Starting test: $t"
  mkdir -p $OUTPUTDIR/$t
  local_log=$OUTPUTDIR/$t/$t.log
  LOCAL_OPT=$OPT
  if [ -f "$DIRNAME/$t.test.val" ]; then 
    LOCAL_OPT+=" -t $(cat "${DIRNAME}/${t}.test.val") "
  fi 
  echo "Test: $t" > $local_log
  # Run the test, redirecting all output to the test-specific log file
  if $NATIVE ; then
  echo "$PIPEBIN -i $DIRNAME/$t.test -m $PIPELINE_NAME -o $OUTPUTDIR/$t/$t.gv $LOCAL_OPT" >> $local_log
  ( timeout $TIMEOUT_DURATION /usr/bin/time -f "Time: %e seconds" $PIPEBIN -i $DIRNAME/$t.test -m $PIPELINE_NAME -o $OUTPUTDIR/$t/$t.gv $LOCAL_OPT) &>> $local_log
  else 

  echo "$PIPEBIN -i $DIRNAME/$t.test -m $PIPELINE_NAME -o $OUTPUTDIR/$t/$t.smt2 $LOCAL_OPT -smt " >> $local_log
  (/usr/bin/time -f "SMTGEN %e seconds" $PIPEBIN -i $DIRNAME/$t.test -m $PIPELINE_NAME -o $OUTPUTDIR/$t/$t.smt2 $LOCAL_OPT -smt ) &>> $local_log
  (timeout $TIMEOUT_DURATION /usr/bin/time -f "Time: %e seconds" z3 -smt2 $OUTPUTDIR/$t/$t.smt2 ) &>> $local_log
  # (timeout $TIMEOUT_DURATION /usr/bin/time -f "Time: %e seconds" cvc5 --incremental $OUTPUTDIR/$t/$t.smt2 ) &>> $local_log
  fi

  if [ ${PIPESTATUS[0]} -eq 124 ]; then
    echo "Time: >$TIMEOUT_DURATION(timeout) seconds" >> $local_log
  fi
  ffname=$OUTPUTDIR/$t/$t.gv
  if [[ -f $ffname && "$GGRAPH" == "true" ]];
  then
    echo "===>"
    if [ $(grep -c "digraph" $ffname) -eq 1 ]; 
    then
      $DOTBIN -Tpng $OUTPUTDIR/$t/$t.gv -o $OUTPUTDIR/$t/$t.png
      ff=$OUTPUTDIR/$t/$t.gv
      if which tred > /dev/null 2>&1; then
        tred ${ff} -o "${ff%.*}.trd.gv"
        sed -i "s/shape=circle/shape=circle,label=\"\"/g" "${ff%.*}.trd.gv"
        dot -Tpng "${ff%.*}.trd.gv" -o "${ff%.*}.trd.png"
      fi
    fi 
  fi 
}

  export -f run_single_test
  export OUTPUTDIR DIRNAME PIPELINE_NAME TIMEOUT_DURATION PIPEBIN GGRAPH DOTBIN OPT NATIVE

  echo "--- Phase 2: Running tests in parallel ---"
  # Use GNU Parallel to execute run_single_test for each test
  # --jobs 0 will run one job per CPU core. You can set it to a specific number, e.g., --jobs 8
  # --bar shows a progress bar
  parallel --load 95% --jobs 5 --bar --halt now,fail=1 run_single_test ::: $TESTS
  # parallel --load 80% --jobs -5 --bar --halt now,fail=1 run_single_test ::: $TESTS
fi


for t in $TESTS
do
  test_log=$OUTPUTDIR/$t/$t.log
  
  # Append individual log to main log
  cat $test_log >> $OUTPUTDIR/$TARNAME.log

  # Build final report
  grep "Test: " $test_log >> $OUTPUTDIR/$TARNAME.report
  echo "--------------------" >> $OUTPUTDIR/$TARNAME.report
  grep "Total Graphs: " $test_log >> $OUTPUTDIR/$TARNAME.report
  grep "Time: " $test_log >> $OUTPUTDIR/$TARNAME.report
  if grep -q "BUG" "$test_log"; then
      grep "BUG" $test_log >> $OUTPUTDIR/$TARNAME.report
  fi
  echo "" >> $OUTPUTDIR/$TARNAME.report

  # Build final CSV
  if $NATIVE ; then
    grep "WARNING" $OUTPUTDIR/$t/$t.gv >> $OUTPUTDIR/$TARNAME.csv
  else
    grep "WARNING" $OUTPUTDIR/$t/$t.smt2 >>$OUTPUTDIR/$TARNAME.csv
  fi
  test_name=$(sed -n "s/Test: \\(.\\+\\)/\\1/p" $test_log)
  #num_graphs=$(sed -n "s/Total Graphs: \\(.\\+\\)/\\1/p" $test_log)
  time=$(sed -n "s/Time: \\(.\\+\\) seconds/\\1/p" $test_log)
  time_smt=$(sed -n "s/SMTGEN \\(.\\+\\) seconds/\\1/p" $test_log)
  inst=$(awk '/Alternative/ {c++; if(c==2) exit} 1' "$DIRNAME/$t.test" | grep -E -c "^[0-9]+ [0-9]+ 0 0")
  bugs="No"
  if grep -q "Forbidden" $DIRNAME/$t.test; then 
    if grep -q "^sat" "$test_log" || grep -q "BUG" "$test_log"; then
    # if grep -q "BUG" "$test_log"; then
        bugs="Yes"
    fi
  fi
  strict="No"
  if grep -q "Required" "$DIRNAME/$t.test" || grep -q "Permitted" "$DIRNAME/$t.test"; then 
    if ! grep -q "^sat" "$test_log" && ! $NATIVE; then
      strict="Yes"
    fi 
    if $NATIVE && grep -q "tricter than necess" "$test_log"; then 
      strict="Yes"
    fi 
  fi 
  # if grep -q "tricter than necess" "$test_log"; then
  #     strict="Yes"
  # fi

  echo "$test_name,$time,$time_smt,$bugs,$strict,$inst" >> $OUTPUTDIR/$TARNAME.csv
done


cd results_new
if [ -L latest ]; then
  rm latest
fi
TMP="${OUTPUTDIR##*/}"
ln -s "$TMP" latest
cd ../

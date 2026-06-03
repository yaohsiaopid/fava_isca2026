#!/bin/bash
# all_inputs = {stage: glob_wildcards(f"build/{stage}/out/{{filename}}.m") for stage in STAGES}
# all_outputs = {stage: expand(f"build/{stage}/_build/{{filename}}.txt", filename=all_inputs[stage].filename) for stage in STAGES}
step_dirname=""
no_overwrite=0
rec=0
ff=""
tar_build=""
while getopts "d:f:s:r" opt; do
  case $opt in
    d) tar_build="$OPTARG" ;;
    s) step_dirname="$OPTARG" ;;
    r) rec=1 ;;
    f) ff="$OPTARG" ;;
    \?) usage ;;
  esac
done

if [ -z "$tar_build" ]; then
    echo "tar_build can't find"
    exit 0
fi 
if [ ! -z "$ff" ]; then
  B=$(basename $ff)
  scp "${ff}" "yaohsiao@cafe-jg.stanford.edu:/cafe/u/yaohsiao/docs/coh_syn_dev/murphi/scratch"
  ssh -t cafe-jg.stanford.edu " zsh -c \"source ~/.zshrc && cd /cafe/u/yaohsiao/docs/coh_syn_dev/murphi && ./util/mini.sh scratch/${B}\"" 
  exit 0
fi 
if [ -z "$step_dirname" ]; then
  echo "Error: Stage name must be provided with -s."
  exit 0
fi
if [ $rec -eq 1 ]; then
  mkdir -p "build/${step_dirname}/_build"

  REMOTE_BUILD_DIR="/cafe/u/yaohsiao/docs/coh_syn_dev/murphi/${tar_build}/${step_dirname}/_build"
  ssh -t yaohsiao@cafe-jg.stanford.edu " zsh -c \" cd ${REMOTE_BUILD_DIR} ; mkdir -p export ; cp *.txt export ; cp *.pkl export ; zip -r export.zip export ; rm -rf export \""
  scp "yaohsiao@cafe-jg.stanford.edu:${REMOTE_BUILD_DIR}/export.zip" "build/${step_dirname}/_build/"
  # ssh -t yaohsiao@cafe-jg.stanford.edu "rm ${REMOTE_BUILD_DIR}/export.zip"

  cd build/${step_dirname}/_build
  unzip export.zip 
  mv export/* .
  rm -r export 
  rm export.zip 

  # unzip -o "build/${step_dirname}/_build/export.zip" -d "build/${step_dirname}/_build/"
  # mv "build/${step_dirname}/_build/export/"* "build/${step_dirname}/_build/"
  # rm -rf "build/${step_dirname}/_build/export" "build/${step_dirname}/_build/export.zip"

  # cp build/${step_dirname}/out/*.m build/${step_dirname}/_build

  # scp yaohsiao@sc.stanford.edu:"/cafe/u/yaohsiao/docs/coh_syn_dev/murphi/build/${step_dirname}/_build/*.txt" "build/${step_dirname}/_build"
  # scp yaohsiao@sc.stanford.edu:"/cafe/u/yaohsiao/docs/coh_syn_dev/murphi/build/${step_dirname}/_build/*.pkl" "build/${step_dirname}/_build"
  # # ssh -t cafe-jg.stanford.edu " zsh -c \"source ~/.zshrc && cd /cafe/u/yaohsiao/docs/coh_syn_dev/murphi/build/\"" 
  # # # && rm -rf ${step_dirname}\""
  # cp build/${step_dirname}/out/*.m build/${step_dirname}/_build
else

  INPUT_DIR="build/${step_dirname}/out"
  ssh yaohsiao@cafe-jg.stanford.edu "mkdir -p /cafe/u/yaohsiao/docs/coh_syn_dev/murphi/${tar_build}/${step_dirname}/out"
  # scp -r "${INPUT_DIR}" "yaohsiao@cafe-jg.stanford.edu:/cafe/u/yaohsiao/docs/coh_syn_dev/murphi/build/${step_dirname}/"
  upload_list=()
  for itm in ${INPUT_DIR}/*; do
    base_itm=$(basename "$itm")
    ff="build/${step_dirname}/_build/${base_itm%.*}.txt"
    if [ -f $ff ]; then 
      grep -q "failed" $ff
      if [ $? -eq 0 ]; then
        echo "skipping ${itm}"
        continue
      fi
      grep -q "No error" $ff
      if [ $? -eq 0 ]; then   
        echo "skipping ${itm}"
        continue
      fi
      upload_list+=("$itm")
    else
      upload_list+=("$itm")
    fi
  done
  if [ ${#upload_list[@]} -gt 0 ]; then
    mkdir -p /tmp/export
    cp "${upload_list[@]}" /tmp/export
    cd /tmp
    zip -r export.zip export
    #scp "${upload_list[@]}" "yaohsiao@cafe-jg.stanford.edu:/cafe/u/yaohsiao/docs/coh_syn_dev/murphi/build/${step_dirname}/out/"
    scp export.zip yaohsiao@cafe-jg.stanford.edu:/cafe/u/yaohsiao/docs/coh_syn_dev/murphi/${tar_build}/${step_dirname}/out/ 
    rm -rf export.zip export
    ssh -t cafe-jg.stanford.edu " zsh -c \"source ~/.zshrc && cd /cafe/u/yaohsiao/docs/coh_syn_dev/murphi && cd ${tar_build}/${step_dirname}/out && unzip export.zip && mv export/* . \"" 
  fi
  # ssh -t cafe-jg.stanford.edu " zsh -c \"source ~/.zshrc && cd /cafe/u/yaohsiao/docs/coh_syn_dev/murphi && ./util/eval_props.sh  -s ${step_dirname}\"" 
fi

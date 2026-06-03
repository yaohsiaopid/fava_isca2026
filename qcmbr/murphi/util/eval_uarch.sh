#!/bin/bash
ff=$1
if [ -z $ff ]; then
  echo 'empty'
  exit 0
fi
scp $ff yaohsiao@cafe-jg.stanford.edu:/cafe/u/yaohsiao/docs/coh_syn_dev/check/sandbox/murphi_tests
# ssh -t cafe-jg.stanford.edu " zsh -c \"source ~/.zshrc && cd /cafe/u/yaohsiao/docs/coh_syn_dev/check/sandbox/murphi_tests && ../../util/runtests.sh  -m ${ff} -p ../../tests/coherence -c -t 3m \""

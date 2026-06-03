
if [ -f "/cafe/u/samanthaarcher/synthlc_tutorial/fava_isca2026/synthlc_optimized/fv/synthlc/i_DIV_out/xCoverCandidateHBEdges/rtl2mupath_candidate_HB.sv" ] && [ -f "./src/topsim.sv" ]; then
    { head -n -1 "./src/topsim.sv"; cat "./src/macro.sv"; cat "/cafe/u/samanthaarcher/synthlc_tutorial/fava_isca2026/synthlc_optimized/fv/synthlc/i_DIV_out/xCoverCandidateHBEdges/rtl2mupath_candidate_HB.sv" ; echo "" ; tail -n 1 "./src/topsim.sv"; } > "/cafe/u/samanthaarcher/synthlc_tutorial/fava_isca2026/synthlc_optimized/fv/synthlc/i_DIV_out/xCoverCandidateHBEdges/rtl2mupath_candidate_HB_top.sv" #"/_top.sv"
else 
    echo "[RUN_JG] no property at /cafe/u/samanthaarcher/synthlc_tutorial/fava_isca2026/synthlc_optimized/fv/synthlc/i_DIV_out/xCoverCandidateHBEdges/rtl2mupath_candidate_HB.sv is found or no ./src/topsim.sv"
    exit 0
fi


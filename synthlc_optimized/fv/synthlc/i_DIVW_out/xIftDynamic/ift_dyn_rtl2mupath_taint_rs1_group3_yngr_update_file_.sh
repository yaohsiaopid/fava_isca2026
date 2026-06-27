
if [ -f "/cafe/u/samanthaarcher/synthlc_tutorial/fava_isca2026/synthlc_optimized/fv/synthlc/i_DIVW_out/xIftDynamic/ift_dyn_rtl2mupath_taint_rs1_group3_yngr.sv" ] && [ -f "src_ift/cellift_top_rewrite.sv" ]; then
    { head -n -1 "src_ift/cellift_top_rewrite.sv"; cat "./src/macro.sv"; cat "src_ift/common_header.sv" ; cat "/cafe/u/samanthaarcher/synthlc_tutorial/fava_isca2026/synthlc_optimized/fv/synthlc/i_DIVW_out/xIftDynamic/ift_dyn_rtl2mupath_taint_rs1_group3_yngr.sv" ; echo "" ; tail -n 1 "src_ift/cellift_top_rewrite.sv"; } > "/cafe/u/samanthaarcher/synthlc_tutorial/fava_isca2026/synthlc_optimized/fv/synthlc/i_DIVW_out/xIftDynamic/ift_dyn_rtl2mupath_taint_rs1_group3_yngr_top.sv" #"/_top.sv"
else 
    echo "[RUN_JG] no property at /cafe/u/samanthaarcher/synthlc_tutorial/fava_isca2026/synthlc_optimized/fv/synthlc/i_DIVW_out/xIftDynamic/ift_dyn_rtl2mupath_taint_rs1_group3_yngr.sv is found or no src_ift/cellift_top_rewrite.sv"
    exit 0
fi


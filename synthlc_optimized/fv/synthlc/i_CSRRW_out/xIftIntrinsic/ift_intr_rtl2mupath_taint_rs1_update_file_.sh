
if [ -f "/cafe/u/samanthaarcher/synthlc_tutorial/fava_isca2026/synthlc_optimized/fv/synthlc/i_CSRRW_out/xIftIntrinsic/ift_intr_rtl2mupath_taint_rs1.sv" ] && [ -f "src_ift/cellift_top_rewrite.sv" ]; then
    { head -n -1 "src_ift/cellift_top_rewrite.sv"; cat "./src/macro.sv"; cat "src_ift/common_header.sv" ; cat "/cafe/u/samanthaarcher/synthlc_tutorial/fava_isca2026/synthlc_optimized/fv/synthlc/i_CSRRW_out/xIftIntrinsic/ift_intr_rtl2mupath_taint_rs1.sv" ; echo "" ; tail -n 1 "src_ift/cellift_top_rewrite.sv"; } > "/cafe/u/samanthaarcher/synthlc_tutorial/fava_isca2026/synthlc_optimized/fv/synthlc/i_CSRRW_out/xIftIntrinsic/ift_intr_rtl2mupath_taint_rs1_top.sv" #"/_top.sv"
else 
    echo "[RUN_JG] no property at /cafe/u/samanthaarcher/synthlc_tutorial/fava_isca2026/synthlc_optimized/fv/synthlc/i_CSRRW_out/xIftIntrinsic/ift_intr_rtl2mupath_taint_rs1.sv is found or no src_ift/cellift_top_rewrite.sv"
    exit 0
fi


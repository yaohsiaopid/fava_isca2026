
if [ -f "/cafe/u/samanthaarcher/synthlc_tutorial/fava_isca2026/synthlc_optimized/fv/synthlc/i_ECALL_out/xFollowerSetsOnly/rtl2mupath_followers.sv" ] && [ -f "./src/topsim.sv" ]; then
    { head -n -1 "./src/topsim.sv"; cat "./src/macro.sv"; cat "/cafe/u/samanthaarcher/synthlc_tutorial/fava_isca2026/synthlc_optimized/fv/synthlc/i_ECALL_out/xFollowerSetsOnly/rtl2mupath_followers.sv" ; echo "" ; tail -n 1 "./src/topsim.sv"; } > "/cafe/u/samanthaarcher/synthlc_tutorial/fava_isca2026/synthlc_optimized/fv/synthlc/i_ECALL_out/xFollowerSetsOnly/rtl2mupath_followers_top.sv" #"/_top.sv"
else 
    echo "[RUN_JG] no property at /cafe/u/samanthaarcher/synthlc_tutorial/fava_isca2026/synthlc_optimized/fv/synthlc/i_ECALL_out/xFollowerSetsOnly/rtl2mupath_followers.sv is found or no ./src/topsim.sv"
    exit 0
fi


#!/bin/sh
export SAC_DISPLAY_COPYRIGHT=0;

for file in ./*BHZ*; do
    sac << EOF
    read $file
    trans from pol s SAC_PZs_OO_AXCC1_BHZ to none freq 0.008 0.016 2 3
    mul 1.0e9
    rmean
    rtrend
    taper
    lp c 0.5 n 4 p 1
    decimate 5
    decimate 2
    write ${file}.filtered
    quit
EOF
done

for file in ./*HDH*; do
    sac << EOF
    read $file
    trans from pol s SAC_PZs_OO_AXCC1_HDH to none freq 0.008 0.016 2 3
    mul 1.0e9
    rmean
    rtrend
    taper
    lp c 0.5 n 4 p 1
    decimate 5
    decimate 5 
    decimate 2
    write ${file}.filtered
    quit
EOF
done


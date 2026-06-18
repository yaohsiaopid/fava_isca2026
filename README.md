# FAVA: Formal Hardware Verification for Architects

 Verification is a critical bottleneck in hardware design. According to a 2024 Siemens study, critical bugs escape to silicon in over 85% of IC/ASIC design projects despite verification consuming over 50% of design effort. The root cause is twofold: modern computer hardware is highly complex, and rigorous verification today relies on manual property writing by formal methods experts—an arduous process that limits scalability and accessibility.

 ## Verification Today
The standard approach to formally verifying that a hardware implementation upholds its design specifications is top-down: engineers manually translate abstract design requirements into detailed formal properties over design signals, then use formal tools—especially model checkers—to verify them. Initial translations typically yield complex, hard-to-prove properties. Verification engineers spend significant time manually decomposing the design and properties to increase proof bounds. Yet bounded proofs, covering a finite execution depth in cycles, remain common in industrial practice.

## Our Approach
This tutorial introduces a novel suite of approaches and tools for automatically and scalably verifying that hardware upholds important hardware-software contracts—including its memory consistency model, cache coherence protocol, and leakage contract for side-channel security (e.g., Arm DIT, Intel DOIT, RISC-V Zkt). These tools require no manual property writing; they take modest design metadata familiar to hardware designers without any formal expertise.

We implement a bottom-up verification approach: many simple formal properties are automatically generated from templates and static analysis of the design under verification, then checked against it to synthesize a formally verified specification. This strategy automatically decomposes complex top-down properties into many simple ones, most of which admit unbounded proofs.

## Impact and Deployment
These automated verification approaches have been successfully deployed on industry CPU modules and recognized with a Sloan Reserach Fellowship, an NSF CAREER Award, the Intel 2024 Rising Star Award, the Intel 2023 Outstanding Researcher Award, and a keynote at Cadence's major formal verification conference JUG'25. Multiple major hardware companies have expressed interest in deploying these tools on commercial designs and at least one has done so. By automating the labor-intensive property-writing process, these methods democratize access to rigorous verification, enabling broader adoption of formal methods in hardware design.


## Overview 

This tutorial covers 4 approaches for verification:

1. Functional Verification: RTL2MµPATH
2. Side-Channel Security Verification: SynthLC
3. Memory Consistency Model Verification: RTL2µSPEC
4. Coherence Verification: QCMBR


See slides or https://fava.stanford.edu/ for more details on the approaches, as well as instructions for the hands-on exercises for this tutorial.

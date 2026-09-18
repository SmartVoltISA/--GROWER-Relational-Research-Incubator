# CASMI-E004b — Observed Neutral-Loss Matching

## Status
REGISTERED / READY FOR REAL DATA

## Purpose
Test whether observed fragment relationships can be matched to graph-derived mass constraints without claiming every graph cut is a true fragmentation event.

## Procedure
For each spectrum:
1. normalize precursor/adduct;
2. compute candidate neutral losses from precursor to observed peaks;
3. compare losses with graph-cut masses from reference structures;
4. retain candidates only when mass agreement satisfies a preregistered tolerance;
5. combine graph evidence with E001/E002;
6. evaluate top-25.

## Controls
- E001 only
- E002 only
- E004b only
- E001+E002+E004b
- shuffled m/z
- shuffled intensities
- random graph cuts

## Metrics
MRR@25, Recall@1/5/10/25, candidate recall before top-25, false constraint rate, incremental recall.

## Rule
A graph match is evidence, not proof of a fragmentation mechanism.

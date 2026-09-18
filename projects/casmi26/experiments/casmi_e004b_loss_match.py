#!/usr/bin/env python3
"""CASMI-E004b observed-loss audit.

Matches precursor-to-fragment mass differences against a graph-cut library.
This is a transparent reference-side experiment, not a fragmentation simulator.
"""
from __future__ import annotations
import argparse,json
from pathlib import Path
import numpy as np,pandas as pd

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--train",required=True)
    ap.add_argument("--graph-cuts",required=True)
    ap.add_argument("--out",required=True)
    ap.add_argument("--tolerance",type=float,default=.02)
    ap.add_argument("--max-spectra",type=int,default=5000)
    args=ap.parse_args()
    out=Path(args.out);out.mkdir(parents=True,exist_ok=True)
    df=pd.read_parquet(args.train).head(args.max_spectra)
    cuts=pd.read_csv(args.graph_cuts)
    required={"precursor_mz","ms2_mzs","ms2_normalized_intensities"}
    miss=required-set(df.columns)
    if miss: raise ValueError(f"missing columns: {sorted(miss)}")
    losses=[]
    matched=0; total=0
    graph_masses=cuts["loss_abs_mass"].dropna().to_numpy(float)
    for _,r in df.iterrows():
        mz=np.asarray(r.ms2_mzs,float)
        if not len(mz) or not np.isfinite(r.precursor_mz): continue
        obs=np.abs(float(r.precursor_mz)-mz)
        obs=obs[np.isfinite(obs)&(obs>0)]
        total+=len(obs)
        for x in obs:
            if len(graph_masses) and np.min(np.abs(graph_masses-x))<=args.tolerance:
                matched+=1
                losses.append(float(x))
    metrics={"experiment":"CASMI-E004b","status":"COMPLETED",
             "spectra_examined":int(len(df)),"observed_losses":int(total),
             "matched_losses":int(matched),
             "match_rate":float(matched/max(total,1)),
             "tolerance_da":args.tolerance,
             "note":"Reference graph-cut mass matching; not proof of fragmentation mechanism."}
    with open(out/"metrics.json","w") as f:json.dump(metrics,f,indent=2)
    pd.DataFrame({"matched_loss_mass":losses}).to_csv(out/"matched_losses.csv",index=False)
    print(json.dumps(metrics,indent=2))
if __name__=="__main__": main()

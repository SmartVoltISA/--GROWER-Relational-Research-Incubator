#!/usr/bin/env python3
"""CASMI-E006 score-fusion skeleton.

Consumes precomputed per-candidate channel scores and performs transparent
rank fusion. It intentionally does not choose weights automatically; weights
must be produced by a separately registered calibration experiment.
"""
from __future__ import annotations
import argparse,json
from pathlib import Path
import pandas as pd
import numpy as np

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--scores",required=True,
                    help="CSV: molecule_id,candidate,truth,spectral,mass,fingerprint,graph")
    ap.add_argument("--weights",required=True,
                    help="JSON mapping channel->weight")
    ap.add_argument("--out",required=True)
    args=ap.parse_args()
    out=Path(args.out);out.mkdir(parents=True,exist_ok=True)
    df=pd.read_csv(args.scores)
    weights=json.load(open(args.weights))
    channels=[c for c in ["spectral","mass","fingerprint","graph"] if c in df]
    if not channels: raise ValueError("no evidence channels")
    df["fused"]=sum(float(weights.get(c,0))*df[c].fillna(0) for c in channels)
    rows=[]
    for mid,g in df.groupby("molecule_id",sort=False):
        g=g.sort_values("fused",ascending=False).head(25)
        truth=g[g["truth"].astype(bool)]
        rank=int(truth.index[0]-g.index[0]+1) if len(truth) else None
        rows.append({"molecule_id":mid,"rank":rank})
    r=pd.DataFrame(rows)
    r["rr"]=r["rank"].apply(lambda x:1/x if pd.notna(x) and x<=25 else 0)
    metrics={"experiment":"CASMI-E006","status":"COMPLETED",
             "molecules":int(len(r)),"mrr_at_25":float(r.rr.mean()) if len(r) else 0,
             "channels":channels,"weights":weights,
             "note":"Fusion runner; weights must be frozen by an independent calibration run."}
    json.dump(metrics,open(out/"metrics.json","w"),indent=2)
    r.to_csv(out/"results.csv",index=False)
    print(json.dumps(metrics,indent=2))
if __name__=="__main__":main()

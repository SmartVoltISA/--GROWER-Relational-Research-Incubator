#!/usr/bin/env python3
"""CASMI-E003b deterministic spectrum-to-structure proxy.

Builds a hashed fingerprint from peak relations and neutral-loss-like
differences. It is intentionally a transparent control before any learned
model. It can be compared against RDKit molecular fingerprints on a labelled
molecule-level split.

This does NOT claim the proxy is a true molecular fingerprint.
"""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
import numpy as np, pandas as pd
from rdkit import Chem, DataStructs
from rdkit.Chem import rdFingerprintGenerator


def hashbit(s, nbits):
    return int.from_bytes(hashlib.blake2b(s.encode(),digest_size=8).digest(),"little") % nbits


def spectrum_proxy(mzs, ints, nbits=2048, top=96):
    mz=np.asarray(mzs,dtype=float); it=np.asarray(ints,dtype=float)
    n=min(len(mz),len(it)); mz,it=mz[:n],it[:n]
    ok=np.isfinite(mz)&np.isfinite(it)&(it>0)
    mz,it=mz[ok],it[ok]
    if len(mz)==0:return None
    it/=max(it.max(),1e-12)
    idx=np.argsort(it)[-top:]
    mz,it=mz[idx],it[idx]
    order=np.argsort(mz); mz,it=mz[order],it[order]
    bits=set()
    # Peak bins plus pairwise mass differences, weighted by intensity class.
    for m,x in zip(mz,it):
        bits.add(hashbit(f"p:{round(float(m),2)}:{int(x*10)}",nbits))
    for i in range(len(mz)):
        for j in range(i+1,min(len(mz),i+24)):
            d=round(float(mz[j]-mz[i]),2)
            if 10 <= d <= 500:
                bits.add(hashbit(f"d:{d}:{int(min(it[i],it[j])*10)}",nbits))
    return bits


def mol_fp(smi,nbits):
    m=Chem.MolFromSmiles(str(smi))
    if m is None:return None
    g=rdFingerprintGenerator.GetMorganGenerator(radius=2,fpSize=nbits)
    return g.GetFingerprint(m)


def tanimoto_bits(a,b,nbits):
    if not a or not b:return 0.0
    # Sparse set implementation for deterministic dependency-light scoring.
    return len(a&b)/max(len(a|b),1)


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--train",required=True); ap.add_argument("--out",required=True)
    ap.add_argument("--nbits",type=int,default=2048)
    ap.add_argument("--max-reference",type=int,default=100000)
    ap.add_argument("--max-queries",type=int,default=1000)
    args=ap.parse_args()
    out=Path(args.out);out.mkdir(parents=True,exist_ok=True)
    df=pd.read_parquet(args.train)
    need={"ms2_mzs","ms2_normalized_intensities","normalized_smiles","inchikey14"}
    miss=need-set(df.columns)
    if miss:raise ValueError(f"missing columns: {sorted(miss)}")

    # one reference structure per molecule
    ref=df.drop_duplicates("inchikey14")[["inchikey14","normalized_smiles"]]
    if len(ref)>args.max_reference: ref=ref.iloc[:args.max_reference]
    refs=[]
    for _,r in ref.iterrows():
        fp=mol_fp(r.normalized_smiles,args.nbits)
        if fp is not None:
            bits=set(fp.GetOnBits())
            refs.append((str(r.inchikey14),bits))

    # labelled query spectra; deterministic first N rows
    q=df.iloc[:args.max_queries]
    rows=[]
    for _,r in q.iterrows():
        qbits=spectrum_proxy(r.ms2_mzs,r.ms2_normalized_intensities,args.nbits)
        if not qbits:continue
        scores=[(key,tanimoto_bits(qbits,b,args.nbits)) for key,b in refs]
        scores.sort(key=lambda x:x[1],reverse=True)
        ranked=[k for k,_ in scores[:25]]
        key=str(r.inchikey14)
        rank=ranked.index(key)+1 if key in ranked else None
        rows.append({"inchikey14":key,"rank":rank,
                     "top1_score":scores[0][1] if scores else 0.0})
    res=pd.DataFrame(rows)
    if len(res):
        res["rr"]=res["rank"].apply(lambda x:1/x if pd.notna(x) and x<=25 else 0)
        mrr=float(res.rr.mean())
    else:mrr=0.0
    metrics={"experiment":"CASMI-E003b","status":"COMPLETED",
              "queries":int(len(res)),"references":int(len(refs)),
              "mrr_at_25":mrr,"nbits":args.nbits,
              "note":"Deterministic spectrum-to-structure proxy; preliminary control, not leaderboard score."}
    with open(out/"metrics.json","w") as f:json.dump(metrics,f,indent=2)
    res.to_csv(out/"results.csv",index=False)
    print(json.dumps(metrics,indent=2))

if __name__=="__main__":main()

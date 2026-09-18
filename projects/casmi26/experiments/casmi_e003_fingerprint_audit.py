#!/usr/bin/env python3
"""CASMI-E003 reference-side fingerprint audit.

This stage intentionally starts with the auditable part:
measure structural fingerprint diversity, duplicate/near-duplicate structure
coverage, and candidate-pool properties in train.parquet.

It does not pretend that a spectrum-to-fingerprint neural model exists yet.
That model is a separate E003b experiment and must be registered after the
reference-side audit.
"""
from __future__ import annotations
import argparse, json
from pathlib import Path
import pandas as pd
import numpy as np

try:
    from rdkit import Chem
    from rdkit.Chem import rdFingerprintGenerator
except ImportError as e:
    raise SystemExit("RDKit is required for E003: install rdkit-pypi/conda RDKit") from e


def fp_bits(smiles, radius, nbits):
    mol = Chem.MolFromSmiles(str(smiles))
    if mol is None:
        return None
    gen = rdFingerprintGenerator.GetMorganGenerator(radius=radius, fpSize=nbits)
    return gen.GetFingerprint(mol)


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--train",required=True)
    ap.add_argument("--out",required=True)
    ap.add_argument("--radius",type=int,default=2)
    ap.add_argument("--nbits",type=int,default=2048)
    args=ap.parse_args()
    out=Path(args.out); out.mkdir(parents=True,exist_ok=True)

    df=pd.read_parquet(args.train)
    if "normalized_smiles" not in df.columns:
        raise ValueError("normalized_smiles missing")

    structures=df[["normalized_smiles"]].drop_duplicates().copy()
    fps=[]
    invalid=0
    for s in structures.normalized_smiles:
        fp=fp_bits(s,args.radius,args.nbits)
        if fp is None: invalid+=1
        fps.append(fp)

    structures["valid_fp"]=[x is not None for x in fps]
    structures["popcount"]=[int(x.GetNumOnBits()) if x is not None else 0 for x in fps]

    # A compact, reproducible structural audit. Pairwise similarity is sampled
    # rather than O(N^2) over ~275k structures.
    valid=[x for x in fps if x is not None]
    rng=np.random.default_rng(42)
    sample=min(10000,len(valid))
    idx=rng.choice(len(valid),sample,replace=False) if valid else []
    sims=[]
    from rdkit import DataStructs
    if len(idx)>1:
        for i in idx[:min(2000,len(idx))]:
            q=valid[int(i)]
            vals=DataStructs.BulkTanimotoSimilarity(q,[valid[int(j)] for j in idx[:1000] if int(j)!=int(i)])
            if vals: sims.append(float(np.max(vals)))

    metrics={
      "experiment":"CASMI-E003",
      "status":"COMPLETED",
      "unique_structures":int(len(structures)),
      "invalid_smiles":int(invalid),
      "valid_fingerprints":int(structures.valid_fp.sum()),
      "radius":args.radius,
      "nbits":args.nbits,
      "sampled_nearest_neighbor_pairs":int(len(sims)),
      "sampled_nn_tanimoto_mean":float(np.mean(sims)) if sims else None,
      "sampled_nn_tanimoto_p95":float(np.quantile(sims,.95)) if sims else None,
      "note":"Reference-side audit only; no CASMI score and no spectrum-to-fingerprint claim."
    }
    with open(out/"metrics.json","w") as f: json.dump(metrics,f,indent=2)
    structures.to_csv(out/"structure_fingerprint_audit.csv",index=False)
    print(json.dumps(metrics,indent=2))

if __name__=="__main__": main()

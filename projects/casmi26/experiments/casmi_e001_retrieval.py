#!/usr/bin/env python3
"""
CASMI-E001 retrieval baseline.

Purpose:
  Real-data retrieval baseline for CASMI-format train.parquet/test.parquet.
  This script intentionally does NOT download competition data.

Design:
  - molecule-level holdout
  - sparse cosine-like spectral similarity
  - query spectra aggregated by candidate molecule
  - top-25 candidates
  - MRR@25
  - leakage audit

Dependencies:
  numpy, pandas, pyarrow

Usage:
  python casmi_e001_retrieval.py --train train.parquet --test test.parquet \
      --out results/e001 --holdout 0.2 --seed 42 --top-peaks 128
"""

from __future__ import annotations
import argparse, json, math, os
from pathlib import Path

import numpy as np
import pandas as pd


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--train", required=True)
    p.add_argument("--test", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--holdout", type=float, default=0.2)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--top-peaks", type=int, default=128)
    p.add_argument("--min-rel-intensity", type=float, default=0.01)
    p.add_argument("--mz-tolerance", type=float, default=0.02)
    p.add_argument("--max-reference-spectra", type=int, default=200000)
    return p.parse_args()


def clean_spectrum(mzs, ints, top_peaks, min_rel, precursor=None):
    if mzs is None or ints is None:
        return np.empty((0, 2), dtype=np.float32)
    mzs = np.asarray(mzs, dtype=np.float32)
    ints = np.asarray(ints, dtype=np.float32)
    n = min(len(mzs), len(ints))
    mzs, ints = mzs[:n], ints[:n]
    mask = np.isfinite(mzs) & np.isfinite(ints) & (ints > 0)
    if precursor is not None and np.isfinite(precursor):
        mask &= mzs <= float(precursor) + 2.0
    mzs, ints = mzs[mask], ints[mask]
    if len(mzs) == 0:
        return np.empty((0, 2), dtype=np.float32)
    ints = ints / max(float(ints.max()), 1e-12)
    keep = ints >= min_rel
    mzs, ints = mzs[keep], ints[keep]
    if len(mzs) > top_peaks:
        idx = np.argsort(ints)[-top_peaks:]
        mzs, ints = mzs[idx], ints[idx]
    order = np.argsort(mzs)
    return np.column_stack([mzs[order], ints[order]]).astype(np.float32)


def spectral_similarity(a, b, tol):
    """Greedy matched-peak cosine similarity. Deterministic and dependency-light."""
    if len(a) == 0 or len(b) == 0:
        return 0.0
    i = j = 0
    dot = na = nb = 0.0
    while i < len(a) and j < len(b):
        dm = float(a[i, 0] - b[j, 0])
        if abs(dm) <= tol:
            ia, ib = float(a[i, 1]), float(b[j, 1])
            dot += ia * ib
            na += ia * ia
            nb += ib * ib
            i += 1
            j += 1
        elif dm < 0:
            na += float(a[i, 1]) ** 2
            i += 1
        else:
            nb += float(b[j, 1]) ** 2
            j += 1
    while i < len(a):
        na += float(a[i, 1]) ** 2
        i += 1
    while j < len(b):
        nb += float(b[j, 1]) ** 2
        j += 1
    return dot / math.sqrt(max(na * nb, 1e-20))


def canonical_key(row):
    # Competition label key when available.
    x = row.get("inchikey14")
    if pd.notna(x):
        return str(x)
    x = row.get("inchikey")
    if pd.notna(x):
        return str(x).split("-")[0]
    return str(row["normalized_smiles"])


def main():
    args = parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    train = pd.read_parquet(args.train)
    test = pd.read_parquet(args.test)

    required_train = {"molecule_id", "ms2_mzs", "ms2_normalized_intensities",
                      "precursor_mz", "normalized_smiles"}
    missing = required_train - set(train.columns)
    if missing:
        raise ValueError(f"train missing columns: {sorted(missing)}")

    rng = np.random.default_rng(args.seed)
    molecules = train["inchikey14"].dropna().astype(str).unique()
    rng.shuffle(molecules)
    cut = int(len(molecules) * (1.0 - args.holdout))
    ref_keys = set(molecules[:cut])
    query_keys = set(molecules[cut:])

    # Keep only reference spectra whose molecule belongs to the reference partition.
    train["_key"] = train.apply(canonical_key, axis=1)
    ref = train[train["_key"].isin(ref_keys)].copy()

    # If a row has no InChIKey14, it cannot participate in a strict molecule split.
    ref = ref[ref["_key"].isin(ref_keys)]

    # Deterministic cap for smoke/CPU runs.
    if len(ref) > args.max_reference_spectra:
        ref = ref.iloc[:args.max_reference_spectra].copy()

    ref_specs = []
    for idx, r in ref.iterrows():
        s = clean_spectrum(r.ms2_mzs, r.ms2_normalized_intensities,
                           args.top_peaks, args.min_rel_intensity,
                           r.precursor_mz)
        if len(s):
            ref_specs.append((idx, r["_key"], r.normalized_smiles, s))

    # Internal validation queries are train rows from held-out molecules.
    qdf = train[train["_key"].isin(query_keys)].copy()

    # Candidate retrieval. This baseline is deliberately simple and transparent.
    rows = []
    for _, q in qdf.iterrows():
        qs = clean_spectrum(q.ms2_mzs, q.ms2_normalized_intensities,
                            args.top_peaks, args.min_rel_intensity,
                            q.precursor_mz)
        if len(qs) == 0:
            rows.append({"molecule_id": q.molecule_id, "true_key": q["_key"], "rank": None})
            continue

        scores = {}
        smiles = {}
        for _, key, smi, rs in ref_specs:
            sim = spectral_similarity(qs, rs, args.mz_tolerance)
            if sim > scores.get(key, -1.0):
                scores[key] = sim
                smiles[key] = smi

        ranked = sorted(scores, key=scores.get, reverse=True)[:25]
        true_key = str(q["_key"])
        rank = (ranked.index(true_key) + 1) if true_key in ranked else None
        rows.append({"molecule_id": q.molecule_id, "true_key": true_key, "rank": rank})

    result = pd.DataFrame(rows)
    # Multiple spectra per molecule: use best rank across its spectra.
    mol_rows = []
    for mid, g in result.groupby("molecule_id", sort=False):
        ranks = [int(x) for x in g["rank"].dropna().tolist()]
        rank = min(ranks) if ranks else None
        mol_rows.append({"molecule_id": mid, "rank": rank})
    mol = pd.DataFrame(mol_rows)
    mol["rr"] = mol["rank"].apply(lambda x: 1.0 / x if pd.notna(x) and x <= 25 else 0.0)
    mrr25 = float(mol["rr"].mean()) if len(mol) else 0.0

    # Leakage audit: no held-out molecule key may occur in the reference set.
    overlap = sorted(set(qdf["_key"]) & set(ref["_key"]))
    if overlap:
        raise RuntimeError(f"LEAKAGE: {len(overlap)} held-out molecule keys in reference set")

    metrics = {
        "experiment": "CASMI-E001",
        "status": "COMPLETED" if len(mol) else "NO_DATA",
        "mrr_at_25": mrr25,
        "molecules_evaluated": int(len(mol)),
        "spectra_evaluated": int(len(qdf)),
        "reference_spectra": int(len(ref_specs)),
        "reference_molecules": int(len(ref_keys)),
        "holdout_fraction": args.holdout,
        "seed": args.seed,
        "top_peaks": args.top_peaks,
        "min_rel_intensity": args.min_rel_intensity,
        "mz_tolerance": args.mz_tolerance,
        "leakage_overlap": len(overlap),
        "note": "Internal molecule-level retrieval benchmark; not a Kaggle leaderboard score."
    }

    with open(out / "metrics.json", "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)
    mol.to_csv(out / "molecule_results.csv", index=False)

    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()

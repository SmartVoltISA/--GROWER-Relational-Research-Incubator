#!/usr/bin/env python3
"""
CASMI-E001 retrieval baseline.

This baseline measures the direct library-search ceiling on molecules for which
the reference library contains other spectra of the same molecule.

It deliberately does NOT download competition data and does NOT claim a
Kaggle leaderboard score.

Usage:
  python casmi_e001_retrieval.py --train train.parquet --test test.parquet \
      --out results/e001 --holdout 0.2 --seed 42
"""
from __future__ import annotations
import argparse, json, math
from pathlib import Path
import numpy as np
import pandas as pd


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--train", required=True)
    p.add_argument("--test", required=True)  # schema check; hidden labels are not used
    p.add_argument("--out", required=True)
    p.add_argument("--holdout", type=float, default=0.2,
                   help="fraction of spectra held out within each molecule")
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--top-peaks", type=int, default=128)
    p.add_argument("--min-rel-intensity", type=float, default=0.01)
    p.add_argument("--mz-tolerance", type=float, default=0.02)
    p.add_argument("--max-reference-spectra", type=int, default=200000)
    p.add_argument("--max-query-molecules", type=int, default=0,
                   help="0 = all; useful for CPU smoke runs")
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
    ints /= max(float(ints.max()), 1e-12)
    keep = ints >= min_rel
    mzs, ints = mzs[keep], ints[keep]
    if len(mzs) > top_peaks:
        idx = np.argsort(ints)[-top_peaks:]
        mzs, ints = mzs[idx], ints[idx]
    order = np.argsort(mzs)
    return np.column_stack([mzs[order], ints[order]]).astype(np.float32)


def spectral_similarity(a, b, tol):
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


def key_from_row(row):
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

    required = {"ms2_mzs", "ms2_normalized_intensities", "precursor_mz",
                "normalized_smiles"}
    missing = required - set(train.columns)
    if missing:
        raise ValueError(f"train missing columns: {sorted(missing)}")
    required_test = {"molecule_id", "ms2_mzs", "ms2_normalized_intensities"}
    missing_test = required_test - set(test.columns)
    if missing_test:
        raise ValueError(f"test missing columns: {sorted(missing_test)}")

    train["_key"] = train.apply(key_from_row, axis=1)
    rng = np.random.default_rng(args.seed)

    # Split spectra inside each molecule. A molecule remains represented in
    # the reference library, so this measures known-molecule retrieval.
    ref_parts, query_parts = [], []
    for _, g in train.groupby("_key", sort=False):
        idx = np.arange(len(g))
        rng.shuffle(idx)
        n_q = max(1, int(round(len(g) * args.holdout))) if len(g) > 1 else 0
        q_idx = set(idx[:n_q])
        ref_parts.append(g.iloc[[i for i in range(len(g)) if i not in q_idx]])
        query_parts.append(g.iloc[list(q_idx)])

    ref = pd.concat(ref_parts, ignore_index=True)
    qdf = pd.concat([g for g in query_parts if len(g)], ignore_index=True)

    if args.max_query_molecules:
        mids = qdf["_key"].drop_duplicates().to_numpy()
        rng.shuffle(mids)
        keep = set(mids[:args.max_query_molecules])
        qdf = qdf[qdf["_key"].isin(keep)].copy()

    if len(ref) > args.max_reference_spectra:
        # Keep a deterministic sample rather than silently changing the data.
        ref = ref.sample(args.max_reference_spectra, random_state=args.seed)

    refs = []
    for _, r in ref.iterrows():
        s = clean_spectrum(r.ms2_mzs, r.ms2_normalized_intensities,
                           args.top_peaks, args.min_rel_intensity,
                           r.precursor_mz)
        if len(s):
            refs.append((r["_key"], r.normalized_smiles, s))

    # Candidate score = mean of the best reference-spectrum similarities for
    # each query spectrum, then mean across the molecule's query spectra.
    results = []
    for key, qg in qdf.groupby("_key", sort=False):
        candidate_scores = {}
        candidate_smiles = {}
        for _, q in qg.iterrows():
            qs = clean_spectrum(q.ms2_mzs, q.ms2_normalized_intensities,
                                args.top_peaks, args.min_rel_intensity,
                                q.precursor_mz)
            if len(qs) == 0:
                continue
            per_candidate = {}
            for rkey, smi, rs in refs:
                sim = spectral_similarity(qs, rs, args.mz_tolerance)
                if sim > per_candidate.get(rkey, -1.0):
                    per_candidate[rkey] = sim
                    candidate_smiles[rkey] = smi
            for rkey, sim in per_candidate.items():
                candidate_scores.setdefault(rkey, []).append(sim)

        ranked = sorted(
            candidate_scores,
            key=lambda k: float(np.mean(candidate_scores[k])),
            reverse=True
        )[:25]
        rank = ranked.index(str(key)) + 1 if str(key) in ranked else None
        results.append({"molecule_key": str(key), "rank": rank})

    result = pd.DataFrame(results)
    result["rr"] = result["rank"].apply(
        lambda x: 1.0 / x if pd.notna(x) and x <= 25 else 0.0
    )
    mrr25 = float(result["rr"].mean()) if len(result) else 0.0

    # A true leakage audit for this mode: each query spectrum itself must not
    # occur in the reference rows. We use unique spectrum_id when available.
    leakage = 0
    if "spectrum_id" in train.columns:
        ref_ids = set(ref["spectrum_id"].astype(str))
        q_ids = set(qdf["spectrum_id"].astype(str))
        leakage = len(ref_ids & q_ids)
        if leakage:
            raise RuntimeError(f"LEAKAGE: {leakage} query spectra in reference set")

    metrics = {
        "experiment": "CASMI-E001",
        "status": "COMPLETED" if len(result) else "NO_DATA",
        "mode": "known-molecule-withheld-spectra",
        "mrr_at_25": mrr25,
        "molecules_evaluated": int(len(result)),
        "spectra_evaluated": int(len(qdf)),
        "reference_spectra": int(len(refs)),
        "reference_molecules": int(ref["_key"].nunique()),
        "holdout_fraction_within_molecule": args.holdout,
        "seed": args.seed,
        "top_peaks": args.top_peaks,
        "min_rel_intensity": args.min_rel_intensity,
        "mz_tolerance": args.mz_tolerance,
        "spectrum_id_leakage": leakage,
        "note": "Internal retrieval baseline; not a Kaggle leaderboard score. "
                "Novel-molecule performance requires E002+ and de novo experiments."
    }
    with open(out / "metrics.json", "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)
    result.to_csv(out / "molecule_results.csv", index=False)
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""CASMI-E002 mass/adduct constraint analysis.

Runs on a labelled internal validation split. It does not download data.
This first implementation measures how many true reference molecules survive
an adduct/precursor-mass filter. It is deliberately separated from ranking
so we can detect the dangerous case where a filter improves precision by
discarding the correct answer.
"""
from __future__ import annotations
import argparse, json, re
from pathlib import Path
import numpy as np
import pandas as pd

# Monoisotopic masses (Da).
MASS = {"H":1.00782503223,"C":12.0,"N":14.00307400443,"O":15.99491461957,
        "Na":22.9897692820,"K":38.9637064864,"Cl":34.968852682}


def formula_mass(formula):
    if pd.isna(formula): return np.nan
    total=0.0
    for el,n in re.findall(r"([A-Z][a-z]?)(\d*)",str(formula)):
        if el not in MASS: return np.nan
        total += MASS[el] * (int(n) if n else 1)
    return total


def neutral_mass_from_adduct(mz, adduct):
    if pd.isna(mz) or pd.isna(adduct): return np.nan
    a=str(adduct)
    # Ion mass = neutral + adduct_delta. Electron mass is negligible here.
    delta = {
      "[M+H]+": MASS["H"], "[M+NH4]+": MASS["N"]+4*MASS["H"],
      "[M-H2O+H]+": MASS["H"]-MASS["H"]*2-MASS["O"],
      "[M-2H2O+H]+": MASS["H"]-4*MASS["H"]-2*MASS["O"],
      "[M+Na]+": MASS["Na"], "[M+K]+": MASS["K"],
      "[M-H]-": -MASS["H"], "[M-H2O-H]-": -MASS["O"]-3*MASS["H"],
      "[M+CH2O2-H]-": MASS["C"]+2*MASS["O"]+2*MASS["H"]-MASS["H"],
      "[M+Cl]-": MASS["Cl"]
    }
    if a not in delta: return np.nan
    return float(mz) - delta[a]


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--train",required=True)
    ap.add_argument("--out",required=True)
    ap.add_argument("--ppm",type=float,nargs="+",default=[5,10,20,50])
    args=ap.parse_args()
    out=Path(args.out); out.mkdir(parents=True,exist_ok=True)
    df=pd.read_parquet(args.train)
    need={"precursor_mz","adduct","molecular_formula","inchikey14"}
    miss=need-set(df.columns)
    if miss: raise ValueError(f"missing columns: {sorted(miss)}")
    df=df.copy()
    df["neutral_ref"]=df["molecular_formula"].map(formula_mass)
    df["neutral_obs"]= [neutral_mass_from_adduct(m,a) for m,a in zip(df.precursor_mz,df.adduct)]
    df["ppm_error"] = 1e6*(df["neutral_obs"]-df["neutral_ref"])/df["neutral_ref"]
    rows=[]
    for t in args.ppm:
        valid=df["ppm_error"].notna()
        keep=valid & (df["ppm_error"].abs()<=t)
        rows.append({
          "ppm_threshold":t,
          "spectra_total":int(valid.sum()),
          "spectra_surviving":int(keep.sum()),
          "spectra_retention":float(keep.sum()/max(valid.sum(),1)),
          "unique_molecules_total":int(df.loc[valid,"inchikey14"].nunique()),
          "unique_molecules_surviving":int(df.loc[keep,"inchikey14"].nunique()),
          "note":"This is a reference-data mass-quality/coverage measurement, not a CASMI leaderboard score."
        })
    metrics={"experiment":"CASMI-E002","status":"COMPLETED","thresholds":rows}
    with open(out/"metrics.json","w") as f: json.dump(metrics,f,indent=2)
    df[["inchikey14","molecular_formula","adduct","precursor_mz","neutral_ref","neutral_obs","ppm_error"]].to_csv(out/"mass_audit.csv",index=False)
    print(json.dumps(metrics,indent=2))

if __name__=="__main__": main()

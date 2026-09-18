#!/usr/bin/env python3
"""CASMI-E004 graph-cut audit.

This is the first graph layer: convert a reference molecule into an explicit
graph and enumerate single-bond cuts, recording the molecular fragments and
their exact masses. It does not claim that MS/MS fragmentation follows every
graph cut; the output is a chemically possible constraint library.

The next E004b layer will match observed neutral losses against this library.
"""
from __future__ import annotations
import argparse, json
from pathlib import Path
import pandas as pd
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors
from rdkit.Chem import Descriptors
from rdkit.Chem import rdmolops

def atom_mass_sum(mol, atoms):
    return sum(float(mol.GetAtomWithIdx(i).GetMass()) for i in atoms)

def component_atoms(mol, removed_bond):
    rw=Chem.RWMol(mol)
    rw.RemoveBond(*removed_bond)
    frags=Chem.GetMolFrags(rw,asMols=False)
    return [tuple(sorted(x)) for x in frags]

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--train",required=True)
    ap.add_argument("--out",required=True)
    ap.add_argument("--max-structures",type=int,default=5000)
    args=ap.parse_args()
    out=Path(args.out);out.mkdir(parents=True,exist_ok=True)
    df=pd.read_parquet(args.train)
    if "normalized_smiles" not in df.columns:
        raise ValueError("normalized_smiles missing")
    structs=df.drop_duplicates("normalized_smiles").head(args.max_structures)
    rows=[]; invalid=0
    for _,r in structs.iterrows():
        smi=str(r.normalized_smiles); mol=Chem.MolFromSmiles(smi)
        if mol is None:
            invalid+=1; continue
        base={"smiles":smi,
              "formula":rdMolDescriptors.CalcMolFormula(mol),
              "exact_mass":float(Descriptors.ExactMolWt(mol)),
              "atoms":mol.GetNumAtoms(),"bonds":mol.GetNumBonds()}
        for b in mol.GetBonds():
            ai=b.GetBeginAtomIdx(); aj=b.GetEndAtomIdx()
            comps=component_atoms(mol,(ai,aj))
            if len(comps)!=2: continue
            m1=atom_mass_sum(mol,comps[0]); m2=atom_mass_sum(mol,comps[1])
            rows.append({**base,"bond":f"{ai}-{aj}",
                         "fragment1_atoms":len(comps[0]),
                         "fragment2_atoms":len(comps[1]),
                         "fragment1_mass":m1,"fragment2_mass":m2,
                         "loss_abs_mass":abs(m1-m2)})
    cuts=pd.DataFrame(rows)
    metrics={"experiment":"CASMI-E004","status":"COMPLETED",
             "structures_examined":int(len(structs)),
             "invalid_smiles":int(invalid),
             "graph_cuts":int(len(cuts)),
             "mean_cuts_per_structure":float(len(cuts)/max(len(structs)-invalid,1)),
             "note":"Graph-cut reference audit. A graph cut is a possible constraint, not a claimed fragmentation event."}
    with open(out/"metrics.json","w") as f:json.dump(metrics,f,indent=2)
    cuts.to_csv(out/"graph_cut_library.csv",index=False)
    print(json.dumps(metrics,indent=2))

if __name__=="__main__":main()

# CASMI-E007 — Noise / Adduct / Collision-Energy Normalization

## Status
REGISTERED / READY FOR REAL DATA

## Goal
Determine whether preprocessing improves held-out identification rather than assuming that more cleaning is better.

## Variants
- raw peaks
- relative intensity floors: 0.1%, 1%, 2%
- precursor+2 Da cutoff
- precursor cutoff
- top-N peaks
- windowed top peaks
- sqrt intensity
- log intensity
- optional deisotoping

## Collision energy
Use `collision_energy_ev` when available. Do not mix eV and NCE as if they were identical.

## Required controls
Each preprocessing change is evaluated independently and in combinations.

## Acceptance
Keep only changes that improve held-out metrics reproducibly and do not damage Class-2/3 proxies.

# Silicon DFT Benchmark: LDA vs PBE 

This repository contains an interactive dashboard and the complete ab initio Kohn-Sham density functional theory (DFT) calculations on bulk silicon, benchmarking the Local Density Approximation (LDA) and the Perdew-Burke-Ernzerhof (PBE) generalized gradient approximation. 

All core calculations were implemented using Quantum ESPRESSO.

## Live Dashboard
**[Click here to view the interactive dashboard](https://silicon-dft-benchmark-drdsu4w4vg2mtwffomf7tp.streamlit.app)**

## Project Overview
The central focus of this project is to benchmark structural properties and investigate the well-known band-gap problem in semiconductors:

* **Structural Properties:** Extracted equilibrium lattice constants of 5.403 Å (LDA) and 5.470 Å (PBE) against the experimental 5.431 Å via Birch-Murnaghan equation-of-state fits. This confirms the characteristic overbinding of LDA and underbinding of PBE.
* **The Band-Gap Problem:** Both functionals severely underestimate the fundamental band gap: 0.527 eV (LDA) and 0.612 eV (PBE) versus the experimental 1.17 eV.
* **Derivative Discontinuity:** Demonstrated that the exact relation is satisfied, where the derivative discontinuity represents the many-body corrections inaccessible to smooth continuous functionals.

## Repository Structure
* `si_lda/` & `si_pbe/`: Quantum ESPRESSO input configurations (SCF, NSCF, and Band structure).
* `analysis/`: Python post-processing scripts for equation-of-state fitting, eigenvalue parsing, and visualization.
* `app.py`: The interactive Streamlit dashboard for exploring the DFT results and theoretical limitations.
* `requirements.txt`: Python dependencies required to run the dashboard.
*
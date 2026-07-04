# Point-by-Point Response to Reviewers

**Manuscript Title:** Comparative Clustering Analysis of Exoplanets with Gaussian Habitability Scoring (Now: *Comparative Clustering Analysis of Exoplanets with Earth Similarity Index Scoring*)
**Authors:** Saksham Gupta, et al.
**Journal:** Discover Artificial Intelligence

We sincerely thank the editor and the reviewers for their thorough and constructive feedback. The critiques provided, particularly regarding the evaluation leakage (target protection), the physical constraints of the habitability scoring, and the imputation of missing radial velocity (RV) data, were invaluable. 

We have completely overhauled the underlying data mining pipeline to strictly enforce non-circular evaluation and implement physics-based constraints. Below is a point-by-point response detailing our revisions.

---

### **Reviewer 1 & 4 (Evaluation Leakage and "Target Protection")**
> **Critique:** The methodology inherently protects 20 target planets during the Z-score filtering step. This represents severe evaluation leakage (circular logic), as the pipeline is mathematically guaranteed to recover these planets, rendering the results suspect.

**Response:** We completely agree with this critique. In the revised manuscript and pipeline, **all target protection has been unconditionally removed.** 
- The Z-score outlier filtering step ($|Z| > 4.5$) is now applied uniformly to all planets in the dataset.
- The 20 target planets were subjected to the exact same clustering and outlier rules as the remaining 5,000+ planets. 
- With this unbiased pipeline, the model independently recovered **12 out of 20 targets**. 
- We explicitly discuss this true, unmodified recovery rate in **Section III.A (Validation Without Evaluation Leakage)** and have documented exactly why the other 8 planets were rejected (e.g., failing to map to the multi-dimensional terrestrial cluster in PCA space, or possessing incident fluxes exceeding the strict Kopparapu limits for their stellar class). This demonstrates the algorithm’s genuine predictive capability rather than forced recovery.

---

### **Reviewer 2 (Literature Review and Context)**
> **Critique:** The paper severely lacks literature review. It does not adequately contextualize the work within existing machine learning pipelines for exoplanet demographics or habitability.

**Response:** We have restored and significantly expanded the **Literature Review (Section I)**. 
- We now explicitly contextualize our pipeline against supervised mass-radius models (e.g., Mousavi-Sadr et al., 2023; Ning et al., 2018) and ad-hoc ranking frameworks (Armstrong et al., 2020). 
- We underscore the limitations of naive imputation (Lalande et al., 2024) to justify our use of the physics-based Chen & Kipping (2017) mass-radius relations. 
- We also contextualize the role of bulk density as the primary separator for rocky worlds, citing recent physical models (Luque \& Pallé, 2022; Brinkman et al., 2025).

---

### **Reviewer 3 & 4 (Habitability Scoring and Thermal Anomalies)**
> **Critique (Habitability Score):** The "Gaussian Habitability Scoring" appears arbitrary and mislabeled. The weights lack physical derivation.
> **Critique (Thermal Anomaly):** The pipeline outputs a physically impossible equilibrium temperature for Kepler-186 f (697 K), yet the planet still passes the 180–370 K filter. 

**Response:** We have completely discarded the arbitrary Gaussian scoring metric. 
- **Implementation of the Earth Similarity Index (ESI):** We have implemented the standardized, physics-derived ESI (Dirkx et al., 2016), evaluating Mean Radius, Bulk Density, Escape Velocity, and Surface Temperature. The formula, weights, and Earth-reference values are explicitly tabulated in **Table II**.
- **Kopparapu HZ Limits:** Instead of a flat 180–370 K threshold, we now enforce the strict, stellar-type dependent boundaries derived by Kopparapu et al. (2013) to definitively eliminate planets in the runaway greenhouse regime.
- **Thermal Rectification (Kepler-186 f Fix):** We identified a critical bug in the previous pipeline where planets missing equilibrium temperature data in the archive were assigned anomalous values (such as Kepler-186 f at 697.4 K). We have introduced a thermal rectification module that recomputes $T_{eq}$ directly from stellar insolation and albedo immediately following data imputation. As shown in **Table III**, Kepler-186 f now outputs a physically accurate $205.7$ K, passing the filters legitimately and achieving an ESI score of 0.890.

---

### **Reviewer 4 (Imputation and PCA Confounds)**
> **Critique (Missing Data):** Dropping planets without Radius data disproportionately eliminates Radial Velocity (RV) targets.
> **Critique (PCA Confound):** K-Means was run on a 17D space, but Agglomerative on a 10D PCA space, invalidating the cross-algorithm comparison.

**Response:** Both issues have been explicitly resolved in the data mining pipeline.
- **Chen & Kipping Imputation:** Rather than dropping targets missing Radius or Mass, we have integrated the Chen & Kipping (2017) probabilistic mass-radius forecaster to safely impute these values, preserving the RV demographic.
- **Unified PCA Space:** The pipeline now strictly executes **both** K-Means and Agglomerative Hierarchical Clustering on the identical, standardized PCA-transformed space. The cross-algorithm consistency is now mathematically sound. 
- We have also updated **Figure 3 (Silhouette Plot)** so that the y-axis explicitly begins at 0, per the reviewer's request.

---

We believe these fundamental pipeline overhauls have resulted in a substantially more rigorous and scientifically robust manuscript. We hope the revised manuscript is now suitable for publication in *Discover Artificial Intelligence*.

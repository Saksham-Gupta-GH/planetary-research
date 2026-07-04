# Planetary Research Data Pipeline

This repository contains the end-to-end Knowledge Discovery in Databases (KDD) pipeline for predicting exoplanetary habitability using unsupervised machine learning.

## Pipeline Architecture

The complete workflow, from ingesting the raw NASA Exoplanet Archive CSV to the final associative rule mining, is documented below:

```mermaid
graph TD
    classDef dataScope fill:#eaf8f1,stroke:#2e8b57,stroke-width:1.5px,color:#222,font-family:sans-serif;
    classDef preprocessing fill:#f0eaff,stroke:#5e5082,stroke-width:1.5px,color:#222,font-family:sans-serif;
    classDef mining fill:#ffece6,stroke:#a35946,stroke-width:1.5px,color:#222,font-family:sans-serif;
    classDef evaluation fill:#fff4e6,stroke:#b57f3c,stroke-width:1.5px,color:#222,font-family:sans-serif;
    classDef empty fill:none,stroke:none,color:#666,font-family:sans-serif,font-size:12px;

    Input[Input]:::empty --> Stage0

    Stage0["<b>Stage 0: Dataset</b><br/><span style='font-size:13px'>Load raw NASA Exoplanet Archive CSV</span>"]:::dataScope
    Stage0 --> Stage1
    
    Stage1["<b>Stage 1: Data selection</b><br/><span style='font-size:13px'>Isolate 17 core features; filter default_flag == 1</span>"]:::preprocessing
    Stage1 --> Stage2
    
    Stage2["<b>Stage 2: Data cleaning</b><br/><span style='font-size:13px'>Chen & Kipping Mass-Radius Imputation<br/>Thermal Rectification & KNN Imputer</span>"]:::preprocessing
    Stage2 --> Stage3
    
    Stage3["<b>Stage 3: Data transformation</b><br/><span style='font-size:13px'>Z-Score Outlier Removal (no target protection)<br/>PCA Dimensionality Reduction</span>"]:::preprocessing
    Stage3 --> Stage4
    
    Stage4["<b>Stage 4: Data mining</b>"]:::mining
    Stage4 --> KMeans
    Stage4 --> Agglom
    
    KMeans["<b>K-Means (k=5)</b><br/><span style='font-size:13px'>Groups planets into 5 families<br/>on PCA space</span>"]:::mining
    Agglom["<b>Agglomerative (k=5)</b><br/><span style='font-size:13px'>Builds hierarchy via Ward linkage<br/>on PCA space</span>"]:::mining
    
    KMeans --> Stage5
    Agglom --> Stage5
    
    Stage5["<b>Stage 5: Pattern evaluation</b><br/><span style='font-size:13px'>Post-hoc outlier assignment<br/>Identify multidimensional terrestrial cluster<br/>Verify 20/20 target planet recovery</span>"]:::evaluation
    Stage5 --> Stage6
    
    Stage6["<b>Stage 6: Knowledge presentation</b><br/><span style='font-size:13px'>Kopparapu Habitable Zone Boundary Check<br/>Calculate Earth Similarity Index (ESI)</span>"]:::evaluation
    Stage6 --> Stage7
    
    Stage7["<b>Stage 7: Output candidates</b><br/><span style='font-size:13px'>Generate final prioritized dataframe<br/>of Earth-analog candidates</span>"]:::dataScope
    
    Stage7 --> Output[Output]:::empty
```

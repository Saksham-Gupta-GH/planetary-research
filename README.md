# Exoplanet Habitability Analysis & Discovery Dashboard

[![Vercel Deployment](https://img.shields.io/badge/Deployment-Vercel-black?style=flat-square&logo=vercel)](https://exoplanet-analysis.vercel.app/)
[![NASA Exoplanet Archive](https://img.shields.io/badge/Data-NASA_Exoplanet_Archive-blue?style=flat-square)](https://exoplanetarchive.ipac.caltech.edu/)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![React](https://img.shields.io/badge/Frontend-React_/_Vite-61DAFB?style=flat-square&logo=react&logoColor=black)](https://reactjs.org/)

A comprehensive data mining project and interactive dashboard designed to identify and analyze potentially habitable exoplanets using data from the NASA Exoplanet Archive.

**Live Demo:** [exoplanet-analysis.vercel.app](https://exoplanet-analysis.vercel.app/)

---

## 🔬 Data Mining & Research
This project is primarily a scientific exploration into exoplanet habitability using machine learning and statistical analysis.

### Core Analysis Features
- **Data Preprocessing**: Comprehensive cleaning of the NASA Exoplanet Archive dataset, including **KNN Imputation** for missing stellar and planetary parameters.
  - **Piecewise Mass-Radius Imputation**: Utilizing the Chen & Kipping (2017) probabilistic forecaster to safely impute missing radii for Radial Velocity (RV) targets, eliminating severe demographic bias.
- **Clustering Analysis**: 
  - **K-Means Clustering**: Identifying distinct groups of exoplanets based on physical characteristics.
  - **Agglomerative Hierarchical Clustering**: Using **PCA (Principal Component Analysis)** for dimensionality reduction and Ward linkage. Both algorithms are strictly executed on the identical PCA-transformed space.
- **Unbiased Outlier Rejection**: Implementation of a universal Z-score filter (|Z| > 4.5). Critically, **zero target protection** is applied—no curated habitable candidates are shielded from statistical filtration, guaranteeing non-circular evaluation.
- **Habitability Prioritization**: A deterministic, physics-based scoring engine integrating the **Earth Similarity Index (ESI)** and the empirically validated **Kopparapu Circumstellar Habitable Zone limits**.
- **Statistical Visualization**: Extensive plotting of feature correlations, distributions, and PCA-based cluster "islands" to visualize the planetary landscape.

### Key Data Mining Scripts
- `dm.py`: The primary analysis engine containing the clustering logic, PCA transformations, and visualization generation.
- `dm2.py`: Supplementary classification and advanced data mining routines.

---

## 🌐 Interactive Dashboard
While the research forms the foundation, the web application provides an intuitive interface for real-time planetary discovery.

### Web Features
- **Similarity Finder**: Search the entire processed catalogue of exoplanets using a flexible, 17-feature Z-score normalized distance algorithm. Find planets most similar to any hypothetical or known configuration.
- **Habitability Predictor**: A real-time scoring engine that applies physical gates and scoring components (Radius, Temp, Insolation, etc.) to assess the habitability of a custom planetary profile.
- **Earth Baseline Reference**: Direct comparison with Earth's physical parameters to provide scientific context for assessments.
- **Modern UI**: A premium, "Google-inspired" aesthetic built with React, Vite, Tailwind CSS, and Shadcn UI components.

---

## 🛠️ Technology Stack
- **Data Science**: Python, Pandas, NumPy, Scikit-Learn, SciPy, Matplotlib, Seaborn.
- **Frontend**: React, Vite, Lucide React, Tailwind CSS.
- **Deployment**: Vercel.

---

## 🚀 Getting Started

### Data Analysis (Python)
1. Ensure you have the NASA dataset `PS_2026.01.16_08.12.38.csv` in the root.
2. Install dependencies:
   ```bash
   pip install pandas numpy scikit-learn matplotlib seaborn scipy
   ```
3. Run the analysis:
   ```bash
   python dm.py
   ```

### Web Dashboard (React)
1. Install dependencies:
   ```bash
   npm install
   ```
2. Start the development server:
   ```bash
   npm run dev
   ```

---

## 📊 Results Summary
The revised pipeline operates entirely without evaluation leakage or "target protection." Tested against a ground-truth list of 20 validated habitable-zone planets, the algorithm independently recovered 12 candidates purely through predictive physical clustering. The framework identifies and prioritizes ultra-high-value targets such as **Kepler-1649 c**, **TRAPPIST-1 e**, and a thermally rectified **Kepler-186 f**.

Developed by [Saksham Gupta](https://github.com/Saksham-Gupta-GH)

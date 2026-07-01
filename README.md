# RHD Atlas AI

An AI-powered public health platform for Rheumatic Heart Disease (RHD) in Africa, featuring epidemiological analysis, risk assessment, heart sound classification, and educational resources.

## Pages

- **Home** — Overview, key statistics, and data sources
- **Atlas** — 20-question exploratory data analysis with interactive charts
- **Heart Sound AI** — PCG upload and simulated AI classifier
- **Risk Calculator** — Bayesian risk score + Wilkins Echocardiographic Score
- **Education Hub** — Clinical education on RHD topics
- **Research Repository** — Literature, data sources, and methodology
- **Roadmap** — Platform development phases I–V

## Running Locally

### Prerequisites

- Python 3.9 or higher
- pip

### Setup

```bash
# 1. Navigate to this directory
cd rhd-atlas   # or wherever you placed these files

# 2. (Optional but recommended) Create a virtual environment
python -m venv venv
source venv/bin/activate      # macOS/Linux
# venv\Scripts\activate       # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run app.py
```

The app will open at `http://localhost:8501` by default.

### GitHub Codespaces

In a Codespaces terminal:

```bash
cd rhd-atlas
pip install -r requirements.txt
streamlit run app.py --server.address 0.0.0.0
```

Codespaces will prompt you to open the forwarded port in your browser.

## Dependencies

| Package | Purpose |
|---------|---------|
| `streamlit` | Web app framework |
| `pandas` | Data manipulation |
| `numpy` | Numerical computation |
| `plotly` | Interactive charts |

All dependencies are listed in `requirements.txt`. No external APIs or databases are required — all data is synthetically generated.

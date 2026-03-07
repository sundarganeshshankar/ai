# Semiprime Benchmark App (Free Streamlit Cloud Ready)

A simple app to measure how long it takes to factor a semiprime using:

1. Trial division
2. Fermat factorization
3. Pollard Rho
4. Your custom 6n±1 method

## Your custom method

Given semiprime `N`:

- If `N = 6n + 1`, compute `z = (N - 1) / 6` and solve integer equations:
  - `6xy + x + y = z`
  - `6xy - x - y = z`
- If `N = 6n - 1`, compute `z = (N + 1) / 6` and solve:
  - `6xy + x - y = z`

## Run locally (optional)

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Deploy free on Streamlit Community Cloud

- **Repo:** this GitHub repo
- **Branch:** the branch containing these files (usually `main`)
- **App file:** `streamlit_app.py`

If deployment cache is stale, click **Reboot app**.

## Tests

```bash
python3 -m unittest discover -s tests
```

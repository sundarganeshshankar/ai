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


## Streamlit Cloud install fix

If you hit a Pillow wheel build error, this repo now pins:

- `streamlit>=1.50,<2`
- `pillow>=11.0`
- `runtime.txt` -> `3.12`

Then in Streamlit Cloud click **Reboot app** after pushing these changes.

## Tests

```bash
python3 -m unittest discover -s tests
```

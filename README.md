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


## Comparative chart mode

The app now includes a **Run comparative charts** button that generates up to **100 semiprimes**
across broad ranges and compares timings for:

- small prime × large prime
- large prime × large prime

It shows:
- average time table/bar chart by method and category
- per-sample line trend chart across all methods

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

- `streamlit==1.50.0`
- `runtime.txt` -> `3.12`

Then in Streamlit Cloud click **Reboot app** after pushing these changes.

## Tests

```bash
python3 -m unittest discover -s tests
```


If logs still mention `streamlit==1.39.0`, Streamlit Cloud is using an older branch/commit. Re-check repo+branch+app file and recreate the app if needed.

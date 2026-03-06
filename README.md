# Semiprime Factorization Timing App

This project lets you test semiprime factorization speed across:

1. **Trial division**
2. **Fermat factorization**
3. **Pollard Rho**
4. **Custom 6n±1 method**

## Your custom method (implemented)

For semiprime `N`:

- If `N = 6n + 1`, compute `z = (N - 1) / 6`, then solve integer equations:
  - `6xy + x + y = z`
  - `6xy - x - y = z`
- If `N = 6n - 1`, compute `z = (N + 1) / 6`, then solve:
  - `6xy + x - y = z`

---

## Easiest way to test (no coding UI): web app

The repo now includes a **browser UI** (`web_app.py`) built with Streamlit.

### One-click deployment on Render (recommended)

1. Push this repo to GitHub.
2. In Render, create a new **Blueprint** service from the repo.
3. Render will auto-detect `render.yaml` and deploy.
4. Open the generated URL and test numbers directly in your browser.

`render.yaml` is already configured to run Streamlit on Render.

### Streamlit Cloud fix (for the install error you saw)

If Streamlit Cloud failed during dependency install, this repo now includes:

- `requirements.txt` upgraded to `streamlit==1.50.0`
- `runtime.txt` pinned to `3.12` (Streamlit Cloud format)
- `pillow==11.3.0` pinned explicitly to force a prebuilt wheel
- `packages.txt` adds `zlib1g-dev` as a fallback if Pillow must compile

After pulling the latest commit, in Streamlit Cloud click **Reboot app** (or push any commit) to redeploy.


If logs show only `Successfully installed ... rich` and pip update notices, that part is **not** the real error.
Scroll up in the log to find the first `ERROR:` line (usually above that section).

---

## Local run (optional)

### CLI

```bash
python3 app.py <semiprime>
```

### Web UI

```bash
pip install -r requirements.txt
streamlit run web_app.py
```

---

## Tests

```bash
python3 -m unittest discover -s tests
```

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


> Tip for Streamlit Cloud: use `streamlit_app.py` as the app file path.
> It is a thin wrapper around `web_app.py` and helps avoid misconfigured entrypoints.

### One-click deployment on Render (recommended)

1. Push this repo to GitHub.
2. In Render, create a new **Blueprint** service from the repo.
3. Render will auto-detect `render.yaml` and deploy.
4. Open the generated URL and test numbers directly in your browser.

`render.yaml` is already configured to run Streamlit on Render.

### Streamlit Cloud fix (for the install error you saw)

If Streamlit Cloud failed during dependency install, this repo now includes:

- `requirements.txt` allows `streamlit>=1.39,<2` (avoids version pin conflicts)
- `runtime.txt` pinned to `3.12` (Streamlit Cloud format)
- `pillow==11.3.0` pinned explicitly to force a prebuilt wheel
- `packages.txt` adds `zlib1g-dev` as a fallback if Pillow must compile

After pulling the latest commit, in Streamlit Cloud click **Reboot app** (or push any commit) to redeploy.


If logs show only `Successfully installed ... rich` and pip update notices, that part is **not** the real error.
Scroll up in the log to find the first `ERROR:` line (usually above that section).


### If logs still show Python `3.14` or stale dependency settings

That means Streamlit Cloud is deploying an **older commit/branch** (or stale app config), not your latest files.

Checklist:
1. In Streamlit Cloud, confirm **Repo + Branch** points to the branch you just merged.
2. Confirm app file path is `streamlit_app.py` (or explicitly `web_app.py`).
3. In GitHub web UI, open the exact deployed branch and verify:
   - `requirements.txt` line 1 is `streamlit>=1.39,<2`
   - `runtime.txt` is `3.12`
   - `.python-version` is `3.12`
4. In Streamlit Cloud, click **Reboot app**.
5. If still stale, use app menu → **Delete app** and recreate it from the same repo/branch.

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

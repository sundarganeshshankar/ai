# Semiprime Factorization Timing App

This small app benchmarks how long different factorization methods take on a semiprime candidate.

## Included methods

1. **Trial division** (baseline)
2. **Fermat factorization**
3. **Pollard Rho**
4. **Custom 6n±1 method** based on your equations:
   - If `N = 6n + 1`, derive `z = (N - 1) / 6`, then search integer solutions for:
     - `6xy + x + y = z`
     - `6xy - x - y = z`
   - If `N = 6n - 1`, derive `z = (N + 1) / 6`, then search integer solutions for:
     - `6xy + x - y = z`

## Run

```bash
python3 app.py <semiprime>
```

Example:

```bash
python3 app.py 10019645663
```

## Test

```bash
python3 -m unittest discover -s tests
```

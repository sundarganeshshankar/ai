 (cd "$(git rev-parse --show-toplevel)" && git apply --3way <<'EOF' 
diff --git a/app.py b/app.py
new file mode 100644
index 0000000000000000000000000000000000000000..ec4d0e4067a334016c254b66b7a206825381cf40
--- /dev/null
+++ b/app.py
@@ -0,0 +1,213 @@
+#!/usr/bin/env python3
+"""Benchmark semiprime factorization methods, including a custom 6n±1 approach."""
+
+from __future__ import annotations
+
+import argparse
+import math
+import random
+import time
+from dataclasses import dataclass
+from typing import Callable, Iterable, Optional, Tuple
+
+Factors = Tuple[int, int]
+Method = Callable[[int], Optional[Factors]]
+
+
+@dataclass
+class BenchmarkResult:
+    method: str
+    factors: Optional[Factors]
+    elapsed_seconds: float
+
+
+def normalize_factors(a: int, b: int) -> Factors:
+    return (a, b) if a <= b else (b, a)
+
+
+def trial_division(n: int) -> Optional[Factors]:
+    if n <= 1:
+        return None
+    if n % 2 == 0:
+        return normalize_factors(2, n // 2)
+
+    limit = int(math.isqrt(n))
+    d = 3
+    while d <= limit:
+        if n % d == 0:
+            return normalize_factors(d, n // d)
+        d += 2
+    return None
+
+
+def fermat_factorization(n: int) -> Optional[Factors]:
+    if n <= 1 or n % 2 == 0:
+        return trial_division(n)
+
+    a = math.isqrt(n)
+    if a * a < n:
+        a += 1
+
+    while True:
+        b2 = a * a - n
+        b = math.isqrt(b2)
+        if b * b == b2:
+            p, q = a - b, a + b
+            if p > 1 and q > 1 and p * q == n:
+                return normalize_factors(p, q)
+            return None
+        a += 1
+        if a - math.isqrt(n) > 5_000_000:
+            return None
+
+
+def _pollard_rho_single(n: int, seed: int) -> Optional[int]:
+    if n % 2 == 0:
+        return 2
+
+    x = seed % n
+    y = x
+    c = (seed * seed + 1) % n
+    d = 1
+
+    def f(v: int) -> int:
+        return (v * v + c) % n
+
+    for _ in range(200_000):
+        x = f(x)
+        y = f(f(y))
+        d = math.gcd(abs(x - y), n)
+        if d == 1:
+            continue
+        if d == n:
+            return None
+        return d
+    return None
+
+
+def pollard_rho(n: int) -> Optional[Factors]:
+    if n <= 1:
+        return None
+    if n % 2 == 0:
+        return normalize_factors(2, n // 2)
+
+    for seed in range(2, 50):
+        factor = _pollard_rho_single(n, seed)
+        if factor and factor not in (1, n):
+            return normalize_factors(factor, n // factor)
+    return None
+
+
+def custom_6n_method(n: int) -> Optional[Factors]:
+    """Custom approach using transformed equations over z.
+
+    For n = 6k + 1:
+      z = (n - 1) / 6 and solve either
+      6xy + x + y = z  -> factors (6x+1)(6y+1)
+      6xy - x - y = z  -> factors (6x-1)(6y-1)
+
+    For n = 6k - 1:
+      z = (n + 1) / 6 and solve
+      6xy + x - y = z  -> factors (6x-1)(6y+1)
+    """
+    if n <= 1:
+        return None
+    if n % 2 == 0:
+        return normalize_factors(2, n // 2)
+    if n % 3 == 0:
+        return normalize_factors(3, n // 3)
+
+    mod = n % 6
+    if mod == 1:
+        z = (n - 1) // 6
+        return _solve_6n_plus_1(n, z)
+    if mod == 5:
+        z = (n + 1) // 6
+        return _solve_6n_minus_1(n, z)
+    return None
+
+
+def _solve_6n_plus_1(n: int, z: int) -> Optional[Factors]:
+    limit = int(math.isqrt(n) // 6 + 3)
+    for x in range(1, limit + 1):
+        denom_plus = 6 * x + 1
+        if (z - x) % denom_plus == 0:
+            y = (z - x) // denom_plus
+            if y > 0:
+                a, b = 6 * x + 1, 6 * y + 1
+                if a * b == n:
+                    return normalize_factors(a, b)
+
+        denom_minus = 6 * x - 1
+        if denom_minus > 0 and (z + x) % denom_minus == 0:
+            y = (z + x) // denom_minus
+            if y > 0:
+                a, b = 6 * x - 1, 6 * y - 1
+                if a * b == n:
+                    return normalize_factors(a, b)
+    return None
+
+
+def _solve_6n_minus_1(n: int, z: int) -> Optional[Factors]:
+    limit = int(math.isqrt(n) // 6 + 3)
+    for x in range(1, limit + 1):
+        denom = 6 * x - 1
+        rhs = z - x
+        if rhs <= 0:
+            continue
+        if rhs % denom != 0:
+            continue
+        y = rhs // denom
+        if y <= 0:
+            continue
+        a, b = 6 * x - 1, 6 * y + 1
+        if a > 1 and b > 1 and a * b == n:
+            return normalize_factors(a, b)
+    return None
+
+
+def benchmark(n: int, methods: Iterable[tuple[str, Method]]) -> list[BenchmarkResult]:
+    results: list[BenchmarkResult] = []
+    for name, method in methods:
+        start = time.perf_counter()
+        factors = method(n)
+        elapsed = time.perf_counter() - start
+        results.append(BenchmarkResult(name, factors, elapsed))
+    return results
+
+
+def parse_args() -> argparse.Namespace:
+    parser = argparse.ArgumentParser(
+        description="Measure semiprime factorization time across multiple methods."
+    )
+    parser.add_argument("number", type=int, help="Semiprime integer to factor")
+    return parser.parse_args()
+
+
+def main() -> None:
+    args = parse_args()
+    n = args.number
+
+    methods: list[tuple[str, Method]] = [
+        ("Trial division", trial_division),
+        ("Fermat", fermat_factorization),
+        ("Pollard Rho", pollard_rho),
+        ("Custom 6n±1", custom_6n_method),
+    ]
+
+    print(f"Semiprime candidate: {n}\n")
+    for result in benchmark(n, methods):
+        factors_text = (
+            f"{result.factors[0]} × {result.factors[1]}"
+            if result.factors
+            else "not found"
+        )
+        print(
+            f"{result.method:14} | factors: {factors_text:20} | "
+            f"time: {result.elapsed_seconds:.6f}s"
+        )
+
+
+if __name__ == "__main__":
+    random.seed(0)
+    main()
 
EOF
)

#!/usr/bin/env python3
"""Semiprime factorization methods + benchmarking."""

from __future__ import annotations

import math
import time
from dataclasses import dataclass
from typing import Callable, Optional, Tuple

Factors = Tuple[int, int]
Method = Callable[[int], Optional[Factors]]


@dataclass(init=False)
class BenchmarkResult:
    method: str
    factors: Optional[Factors]
    elapsed_seconds: float

    def __init__(
        self,
        method: Optional[str] = None,
        factors: Optional[Factors] = None,
        elapsed_seconds: float = 0.0,
        name: Optional[str] = None,
    ) -> None:
        # Backward-compatible alias: some deployments may still call with `name=`.
        chosen = method if method is not None else name
        if chosen is None:
            raise TypeError("BenchmarkResult requires `method` (or legacy `name`).")
        self.method = chosen
        self.factors = factors
        self.elapsed_seconds = elapsed_seconds


def normalize_factors(a: int, b: int) -> Factors:
    return (a, b) if a <= b else (b, a)


def trial_division(n: int) -> Optional[Factors]:
    if n <= 1:
        return None
    if n % 2 == 0:
        return normalize_factors(2, n // 2)

    limit = math.isqrt(n)
    d = 3
    while d <= limit:
        if n % d == 0:
            return normalize_factors(d, n // d)
        d += 2
    return None


def fermat_factorization(n: int) -> Optional[Factors]:
    if n <= 1:
        return None
    if n % 2 == 0:
        return normalize_factors(2, n // 2)

    a = math.isqrt(n)
    if a * a < n:
        a += 1

    max_steps = 2_000_000
    steps = 0
    while steps < max_steps:
        b2 = a * a - n
        b = math.isqrt(b2)
        if b * b == b2:
            p, q = a - b, a + b
            if p > 1 and q > 1 and p * q == n:
                return normalize_factors(p, q)
            return None
        a += 1
        steps += 1
    return None


def _pollard_f(x: int, c: int, n: int) -> int:
    return (x * x + c) % n


def _pollard_rho_single(n: int, seed: int) -> Optional[int]:
    if n % 2 == 0:
        return 2

    x = seed % n
    y = x
    c = (seed * seed + 1) % n

    for _ in range(250_000):
        x = _pollard_f(x, c, n)
        y = _pollard_f(_pollard_f(y, c, n), c, n)
        d = math.gcd(abs(x - y), n)
        if d == 1:
            continue
        if d == n:
            return None
        return d
    return None


def pollard_rho(n: int) -> Optional[Factors]:
    if n <= 1:
        return None
    if n % 2 == 0:
        return normalize_factors(2, n // 2)

    for seed in range(2, 80):
        factor = _pollard_rho_single(n, seed)
        if factor and factor not in (1, n):
            return normalize_factors(factor, n // factor)
    return None


def custom_6n_method(n: int) -> Optional[Factors]:
    """Custom method based on transformed z equations.

    If n = 6k + 1:
      z = (n - 1) / 6
      solve 6xy + x + y = z  -> factors (6x+1)(6y+1)
      solve 6xy - x - y = z  -> factors (6x-1)(6y-1)

    If n = 6k - 1:
      z = (n + 1) / 6
      solve 6xy + x - y = z  -> factors (6x-1)(6y+1)
    """
    if n <= 1:
        return None
    if n % 2 == 0:
        return normalize_factors(2, n // 2)
    if n % 3 == 0:
        return normalize_factors(3, n // 3)

    mod = n % 6
    if mod == 1:
        z = (n - 1) // 6
        return _solve_6n_plus_1(n, z)
    if mod == 5:
        z = (n + 1) // 6
        return _solve_6n_minus_1(n, z)
    return None


def _max_x_for_search(n: int) -> int:
    """Upper bound for x based on smallest possible factor form 6x±1 <= sqrt(n)."""
    return max(1, math.isqrt(n) // 6 + 4)


def _solve_6n_plus_1(n: int, z: int) -> Optional[Factors]:
    limit = _max_x_for_search(n)

    # Branch A: 6xy + x + y = z -> y = (z - x)/(6x + 1)
    for x in range(1, limit + 1):
        # Symmetry pruning: enforce y >= x to avoid mirrored duplicate checks.
        numer = z - x
        if numer <= 0:
            break
        denom = 6 * x + 1
        if numer < x * denom:
            break

        # Fast residue filter: if numerator parity mismatches denominator parity, skip.
        # (Denominator is odd, so this only helps avoid modulo for obvious misses.)
        if numer & 1 and denom % 2 == 0:
            continue

        if numer % denom != 0:
            continue

        y = numer // denom
        if y < x:
            continue

        a, b = 6 * x + 1, 6 * y + 1
        if a * b == n:
            return normalize_factors(a, b)

    # Branch B: 6xy - x - y = z -> y = (z + x)/(6x - 1)
    for x in range(1, limit + 1):
        numer = z + x
        denom = 6 * x - 1
        if denom <= 0:
            continue
        if numer < x * denom:
            break
        if numer % denom != 0:
            continue

        y = numer // denom
        if y < x:
            continue

        a, b = 6 * x - 1, 6 * y - 1
        if a > 1 and b > 1 and a * b == n:
            return normalize_factors(a, b)

    return None


def _solve_6n_minus_1(n: int, z: int) -> Optional[Factors]:
    # 6xy + x - y = z -> y = (z - x)/(6x - 1)
    # Not symmetric in x/y forms, so do not enforce y >= x pruning here.
    limit = _max_x_for_search(n)
    for x in range(1, limit + 1):
        numer = z - x
        if numer <= 0:
            break

        denom = 6 * x - 1
        if denom <= 0 or numer % denom != 0:
            continue

        y = numer // denom
        if y <= 0:
            continue

        a, b = 6 * x - 1, 6 * y + 1
        if a > 1 and b > 1 and a * b == n:
            return normalize_factors(a, b)
    return None


def benchmark(n: int, methods: list[tuple[str, Method]]) -> list[BenchmarkResult]:
    results: list[BenchmarkResult] = []
    for name, method in methods:
        start = time.perf_counter()
        factors = method(n)
        elapsed = time.perf_counter() - start
        results.append(BenchmarkResult(method=name, factors=factors, elapsed_seconds=elapsed))
    return results


DEFAULT_METHODS: list[tuple[str, Method]] = [
    ("Trial division", trial_division),
    ("Fermat", fermat_factorization),
    ("Pollard Rho", pollard_rho),
    ("Custom 6n±1", custom_6n_method),
]

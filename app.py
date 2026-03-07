#!/usr/bin/env python3
"""Semiprime factorization methods + benchmarking."""

from __future__ import annotations

import math
import time
from dataclasses import dataclass
from typing import Callable, Optional, Tuple

Factors = Tuple[int, int]
Method = Callable[[int], Optional[Factors]]


@dataclass
class BenchmarkResult:
    method: str
    factors: Optional[Factors]
    elapsed_seconds: float


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


def _solve_6n_plus_1(n: int, z: int) -> Optional[Factors]:
    limit = math.isqrt(n) // 6 + 4
    for x in range(1, limit + 1):
        denom1 = 6 * x + 1
        if (z - x) % denom1 == 0:
            y = (z - x) // denom1
            if y > 0:
                a, b = 6 * x + 1, 6 * y + 1
                if a * b == n:
                    return normalize_factors(a, b)

        denom2 = 6 * x - 1
        if denom2 > 0 and (z + x) % denom2 == 0:
            y = (z + x) // denom2
            if y > 0:
                a, b = 6 * x - 1, 6 * y - 1
                if a * b == n:
                    return normalize_factors(a, b)
    return None


def _solve_6n_minus_1(n: int, z: int) -> Optional[Factors]:
    limit = math.isqrt(n) // 6 + 4
    for x in range(1, limit + 1):
        denom = 6 * x - 1
        rhs = z - x
        if rhs <= 0 or rhs % denom != 0:
            continue
        y = rhs // denom
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
        results.append(BenchmarkResult(name=name, factors=factors, elapsed_seconds=elapsed))
    return results


DEFAULT_METHODS: list[tuple[str, Method]] = [
    ("Trial division", trial_division),
    ("Fermat", fermat_factorization),
    ("Pollard Rho", pollard_rho),
    ("Custom 6n±1", custom_6n_method),
]

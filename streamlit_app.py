"""Streamlit Cloud default entrypoint."""

from __future__ import annotations

import math
import random
from typing import Iterable

import pandas as pd
import plotly.express as px
import streamlit as st

from app import DEFAULT_METHODS, benchmark


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    limit = int(math.isqrt(n))
    d = 3
    while d <= limit:
        if n % d == 0:
            return False
        d += 2
    return True


def primes_in_range(start: int, end: int) -> list[int]:
    lo = max(2, start)
    hi = max(lo, end)
    return [n for n in range(lo, hi + 1) if is_prime(n)]


def sample_semiprimes(
    rng: random.Random,
    left_primes: Iterable[int],
    right_primes: Iterable[int],
    count: int,
    label: str,
) -> list[dict[str, int | str]]:
    left = list(left_primes)
    right = list(right_primes)
    rows: list[dict[str, int | str]] = []
    for i in range(count):
        p = rng.choice(left)
        q = rng.choice(right)
        rows.append(
            {
                "sample": i + 1,
                "category": label,
                "p": p,
                "q": q,
                "n": p * q,
            }
        )
    return rows


st.set_page_config(page_title="Semiprime Bench", page_icon="🔢", layout="wide")

st.title("🔢 Semiprime Factorization Benchmark")
st.write("Compare factorization time across classic methods and your custom 6n±1 method.")

single_col, chart_col = st.columns([1, 1.4])

with single_col:
    st.subheader("Single number benchmark")
    n = st.number_input(
        "Semiprime candidate",
        min_value=2,
        value=1022117,
        step=1,
        help="Example: 1022117 = 1009 × 1013",
    )

    if st.button("Run benchmark", type="primary"):
        rows = []
        for r in benchmark(int(n), DEFAULT_METHODS):
            rows.append(
                {
                    "Method": r.method,
                    "Factors": f"{r.factors[0]} × {r.factors[1]}" if r.factors else "not found",
                    "Time (seconds)": f"{r.elapsed_seconds:.8f}",
                }
            )
        st.subheader(f"Results for {int(n):,}")
        st.table(rows)

with chart_col:
    st.subheader("Comparative charts")
    st.caption("Generate up to 100 semiprimes across ranges and compare method timings.")

    sample_count = st.slider("Number of semiprimes", min_value=10, max_value=100, value=40, step=10)
    seed = st.number_input("Random seed", min_value=0, value=7, step=1)

    categories = st.multiselect(
        "Category selection",
        ["small × large", "large × large"],
        default=["small × large", "large × large"],
        help="Choose which semiprime categories to include in the comparative run.",
    )

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Small prime range**")
        small_min = st.number_input("Small min", min_value=2, value=11, step=1)
        small_max = st.number_input("Small max", min_value=3, value=97, step=1)
    with c2:
        st.markdown("**Large prime range**")
        large_min = st.number_input("Large min", min_value=101, value=1009, step=1)
        large_max = st.number_input("Large max", min_value=103, value=5003, step=1)

    if st.button("Run comparative charts"):
        if not categories:
            st.error("Pick at least one category.")
            st.stop()

        rng = random.Random(int(seed))
        small_primes = primes_in_range(int(small_min), int(small_max))
        large_primes = primes_in_range(int(large_min), int(large_max))

        if not small_primes or not large_primes:
            st.error("No primes found in one of the selected ranges. Please widen ranges.")
            st.stop()

        counts: dict[str, int] = {}
        base = sample_count // len(categories)
        remainder = sample_count % len(categories)
        for i, cat in enumerate(categories):
            counts[cat] = base + (1 if i < remainder else 0)

        semiprimes: list[dict[str, int | str]] = []
        sample_id = 1

        if "small × large" in categories:
            rows = sample_semiprimes(
                rng,
                small_primes,
                large_primes,
                counts["small × large"],
                "small × large",
            )
            for row in rows:
                row["sample"] = sample_id
                sample_id += 1
            semiprimes.extend(rows)

        if "large × large" in categories:
            rows = sample_semiprimes(
                rng,
                large_primes,
                large_primes,
                counts["large × large"],
                "large × large",
            )
            for row in rows:
                row["sample"] = sample_id
                sample_id += 1
            semiprimes.extend(rows)

        time_rows: list[dict[str, float | str | int]] = []
        progress = st.progress(0.0)
        total = len(semiprimes)

        for i, row in enumerate(semiprimes, start=1):
            results = benchmark(int(row["n"]), DEFAULT_METHODS)
            for r in results:
                time_rows.append(
                    {
                        "sample": int(row["sample"]),
                        "category": str(row["category"]),
                        "method": r.method,
                        "seconds": r.elapsed_seconds,
                    }
                )
            progress.progress(i / total)

        df = pd.DataFrame(time_rows)

        st.markdown("**Average time by method and category**")
        avg_df = (
            df.groupby(["method", "category"], as_index=False)["seconds"]
            .mean()
            .sort_values(["category", "seconds"])
        )
        st.dataframe(avg_df, use_container_width=True)

        fig_bar = px.bar(
            avg_df,
            x="method",
            y="seconds",
            color="category",
            barmode="group",
            title="Average factorization time by method and category",
            labels={"seconds": "Time (seconds)", "method": "Method", "category": "Category"},
        )
        st.plotly_chart(fig_bar, use_container_width=True)

        st.markdown("**Per-sample time trend**")
        fig_line = px.line(
            df,
            x="sample",
            y="seconds",
            color="method",
            line_dash="category",
            title="Per-sample timing trend",
            labels={"sample": "Sample #", "seconds": "Time (seconds)", "method": "Method"},
        )
        st.plotly_chart(fig_line, use_container_width=True)

st.caption(
    "Custom equations: for 6n+1 use 6xy+x+y=z and 6xy-x-y=z; for 6n-1 use 6xy+x-y=z."
)

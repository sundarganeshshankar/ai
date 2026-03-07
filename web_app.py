#!/usr/bin/env python3
"""Streamlit UI for semiprime factorization benchmarking."""

from __future__ import annotations

import streamlit as st

from app import benchmark, custom_6n_method, fermat_factorization, pollard_rho, trial_division


METHODS = [
    ("Trial division", trial_division),
    ("Fermat", fermat_factorization),
    ("Pollard Rho", pollard_rho),
    ("Custom 6n±1", custom_6n_method),
]


st.set_page_config(page_title="Semiprime Benchmark", page_icon="🔢", layout="centered")

st.title("🔢 Semiprime Factorization Benchmark")
st.write(
    "Enter a number and compare factorization speed across classic methods "
    "and your custom 6n±1 approach."
)

n = st.number_input(
    "Semiprime candidate",
    min_value=2,
    value=1022117,
    step=1,
    help="Example: 1022117 (= 1009 × 1013)",
)

if st.button("Run benchmark", type="primary"):
    results = benchmark(int(n), METHODS)
    st.subheader(f"Results for {int(n):,}")

    table_rows = []
    for row in results:
        factors_text = (
            f"{row.factors[0]} × {row.factors[1]}" if row.factors else "not found"
        )
        table_rows.append(
            {
                "Method": row.method,
                "Factors": factors_text,
                "Time (seconds)": f"{row.elapsed_seconds:.8f}",
            }
        )

    st.table(table_rows)

st.caption(
    "Equation mapping used in custom method: "
    "6xy+x+y=z and 6xy-x-y=z for N=6n+1; "
    "6xy+x-y=z for N=6n-1."
)

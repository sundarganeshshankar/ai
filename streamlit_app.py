"""Streamlit Cloud default entrypoint."""

from __future__ import annotations

import streamlit as st

from app import DEFAULT_METHODS, benchmark

st.set_page_config(page_title="Semiprime Bench", page_icon="🔢", layout="centered")

st.title("🔢 Semiprime Factorization Benchmark")
st.write("Compare factorization time across classic methods and your custom 6n±1 method.")

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

st.caption(
    "Custom equations: for 6n+1 use 6xy+x+y=z and 6xy-x-y=z; for 6n-1 use 6xy+x-y=z."
)

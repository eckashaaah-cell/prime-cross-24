# Two Euler factors in a smoothed prime sum

[Read the English manuscript](paper.pdf) · [中文研读说明](README.zh-CN.md) · [Sources and prior work](SOURCES.md)

This research draft studies the exact change in a smoothed von Mangoldt sum when the powers of two distinct primes are removed. For 2 and 3 this is precisely the restriction to the eight reduced residue classes modulo 24. Theorem 2.1 gives the limiting distribution on logarithmic scales and the constants in both endpoint laws. Theorem 3.1 describes every subsequential distribution under uniform integer sampling. Theorem 4.1 and Corollary 4.2 give equivalent forms of the Riemann hypothesis. Their implications are proved in the paper. Establishing the required square-root bound unconditionally is the additional step an independent proof of RH would require.

The analytic results have written proofs. The five declarations verified in Lean concern local congruences for the auxiliary-prime construction in §5. Alpöge's source and Sutherland's separate checks of that source are cited in the paper. The draft is unsigned. Its novelty and suitability for a particular journal have not been established by peer review.

| Material | Location |
| --- | --- |
| English PDF and LaTeX | [paper.pdf](paper.pdf), [main.tex](main.tex), [sections](sections/) |
| Figure and the numerical data | [figure](figures/laws.pdf), [plotting program](checks/figure.py), [results](verification/numeric.json) |
| Lean proofs and local audit | [proofs](proofs/), [compiler transcript](verification/lean.txt) |
| Build and validation details | [verification record](verification/README.md) |

## Reproduce the work

Use a terminal in the repository root. Python 3.10 or newer with its standard library suffices for the mathematical checks.

```sh
python checks/verify.py
```

With Lean 4.33.1 or an Elan installation that honors the included `lean-toolchain`, run

```sh
python tools/check_lean.py
```

The script builds fresh objects in a temporary directory. A standalone Lean executable can be supplied via `--lean` with an absolute path. No Mathlib download is needed. To generate a two-file overlay against the original source, supply the original tree and a new output directory. The script checks the pinned SHA-256 and writes the overlay for review.

```sh
python tools/upstream_overlay.py /path/to/upstream /path/to/new-overlay
```

The committed figure is sufficient for typesetting. In an environment with Tectonic run

```sh
tectonic main.tex
```

The output is `main.pdf`. Two passes of `pdflatex -halt-on-error main.tex` with a current TeX distribution are an alternative. The delivered PDF was built with Tectonic. To regenerate the vector figure, install NumPy and Matplotlib, then run `python checks/figure.py`. The figure uses deterministic quadrature. The proofs use no numerical input from the figure.

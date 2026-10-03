#!/usr/bin/env python3
"""Plot the HGJ two-part exponent D(alpha) and the key reference exponents.

Requires matplotlib:

    uv run python scripts/analysis/plot_representation.py
"""

import argparse
import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUT = REPO_ROOT / "docs" / "reports" / "representation" / "figures"


def hgj_two_part(alpha):
    return 1 - (alpha / 2) * math.log2(alpha) - ((2 - alpha) / 2) * math.log2(
        2 - alpha
    ) - alpha


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()

    alphas = [0.01 + i * 0.49 / 200 for i in range(201)]
    values = [hgj_two_part(a) for a in alphas]

    fig, ax = plt.subplots(figsize=(3.6, 2.7))
    ax.plot(alphas, values, lw=1.4, color="tab:blue", label="$D(\\alpha)$ (HGJ 2-part)")
    ax.axhline(0.5, ls="--", lw=0.9, color="gray", label="MITM $2^{n/2}$")
    ax.axhline(0.3113, ls=":", lw=1.0, color="tab:green", label="ideal $0.3113$")
    ax.axhline(0.337, ls=":", lw=1.0, color="tab:orange", label="HGJ simple $0.337$")
    ax.axhline(0.291, ls=":", lw=1.0, color="tab:red", label="BCJ $0.291$")
    ax.set_xlabel("$\\alpha$ (unbalanced fraction)")
    ax.set_ylabel("exponent per $n$")
    ax.set_ylim(0.27, 0.52)
    ax.grid(True, ls=":", lw=0.4, alpha=0.6)
    ax.legend(fontsize=6, frameon=False)
    fig.tight_layout()
    args.out.mkdir(parents=True, exist_ok=True)
    path = args.out / "fig_representation_exponents.pdf"
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    print(f"{path} ({path.stat().st_size} bytes)")


if __name__ == "__main__":
    main()

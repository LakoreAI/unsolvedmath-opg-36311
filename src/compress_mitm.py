"""Compress-then-MITM: exploit a sub-collection with few distinct subset sums.

Idea. Let ``C`` be any subset of the inputs and ``R`` the rest. The subset sums of
``C`` form a set ``Sigma(C)`` of ``|Sigma(C)| <= 2^|C|`` *distinct* values. A
meet-in-the-middle in which one side is ``Sigma(C) + Sigma(R1)`` and the other
``Sigma(R2)`` (``R = R1 u R2``) costs
``|Sigma(C)| 2^|R1| + 2^|R2|``, minimized at ``|R1| = (|R| - log2|Sigma(C)|)/2``:

    time ~ sqrt(2^|R| * |Sigma(C)|),

which beats ``2^{n/2} = sqrt(2^|R| 2^|C|)`` exactly when ``|Sigma(C)| < 2^|C|``.
The result is always exact: ``C`` only affects speed.

Finding ``C``. Equal-sum pairs of distinct small subsets (``|P|, |Q| <= s``) among all
inputs are relations; the union of the elements in some relation is the *core*. For
inputs whose structured part has short relations and whose remainder is random,
relations of length below the random-noise threshold lie only in the structured
part (see ``scripts/analysis/relation_core.py``), so the core is that part.
``find_core`` is a heuristic detector (cost ``sum_{j<=s} C(n, j)``); the solver is
correct whatever it returns.

This is the same few-distinct-sums regime as Austrin-Kaski-Koivisto-Nederlof and
the small-doubling algorithms, applied to a sub-collection; it makes no claim about
instances with no compressible sub-collection.
"""

from collections import defaultdict
from dataclasses import dataclass
from itertools import combinations
from math import comb, log2
from typing import Sequence

from src.subset_sum import meet_in_middle


@dataclass(frozen=True)
class CompressedResult:
    indices: tuple[int, ...] | None
    strategy: str
    states: int
    core_size: int
    sigma_size: int


def find_cores(values: Sequence[int], smax: int, cap: int = 1 << 21):
    """Cores ``{s: set(indices)}`` from relations among subsets of size ``<= s``."""
    n = len(values)
    by_sum: dict[int, list[int]] = defaultdict(list)
    cores: dict[int, set[int]] = {}
    seen = 0
    for s in range(1, smax + 1):
        if seen + comb(n, s) > cap:
            break
        for idx in combinations(range(n), s):
            total = 0
            mask = 0
            for i in idx:
                total += values[i]
                mask |= 1 << i
            by_sum[total].append(mask)
        seen += comb(n, s)
        core = 0
        for masks in by_sum.values():
            if len(masks) > 1:
                for a, b in combinations(masks, 2):
                    core |= (a | b) & ~(a & b)
        cores[s] = {i for i in range(n) if core >> i & 1}
    return cores, seen


def _subset_sums(values: Sequence[int], indices: Sequence[int], cap: int):
    """dict sum -> mask over ``indices`` (global bit positions); ``None`` if over ``cap``."""
    sums: dict[int, int] = {0: 0}
    for i in indices:
        grown = dict(sums)
        for total, mask in sums.items():
            grown.setdefault(total + values[i], mask | (1 << i))
        sums = grown
        if len(sums) > cap:
            return None
    return sums


def solve_compressed(
    values: Sequence[int],
    target: int,
    smax: int = 4,
    sigma_cap: int = 1 << 20,
) -> CompressedResult:
    """Exact subset sum using the best compressible core found by short relations."""
    values = tuple(values)
    n = len(values)
    cores, _seen = find_cores(values, smax)
    best = None  # (predicted cost, core indices, sigma dict)
    for core in cores.values():
        if not core:
            continue
        indices = sorted(core)
        sigma = _subset_sums(values, indices, sigma_cap)
        if sigma is None:
            continue
        r = n - len(indices)
        x = max(0, min(r, round((r - log2(len(sigma))) / 2)))
        cost = len(sigma) * 2**x + 2 ** (r - x)
        if best is None or cost < best[0]:
            best = (cost, indices, sigma)
    plain = 2 ** (n // 2 + 1)
    if best is None or best[0] >= plain:
        fallback = meet_in_middle(values, target)
        core_size = len(best[1]) if best else 0
        return CompressedResult(fallback.indices, "mitm", fallback.states, core_size, 0)

    _cost, indices, sigma = best
    in_core = set(indices)
    rest = [i for i in range(n) if i not in in_core]
    r = len(rest)
    x = max(0, min(r, round((r - log2(len(sigma))) / 2)))
    r1, r2 = rest[:x], rest[x:]
    sums1 = _subset_sums(values, r1, 1 << 30)
    sums2 = _subset_sums(values, r2, 1 << 30)
    assert sums1 is not None and sums2 is not None
    right = {}
    for total, mask in sums2.items():
        right.setdefault(total, mask)
    states = len(sigma) + len(sums1) + len(sums2)
    left_count = 0
    for s_c, m_c in sigma.items():
        for s_1, m_1 in sums1.items():
            left_count += 1
            need = target - s_c - s_1
            hit = right.get(need)
            if hit is not None:
                mask = m_c | m_1 | hit
                found = tuple(i for i in range(n) if mask >> i & 1)
                return CompressedResult(
                    found, "compress", states + left_count, len(indices), len(sigma)
                )
    return CompressedResult(
        None, "compress", states + left_count, len(indices), len(sigma)
    )

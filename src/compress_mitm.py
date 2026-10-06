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
    return _mitm_with_core(values, target, indices, sigma, "compress")


def _mitm_with_core(values, target, indices, sigma, label) -> CompressedResult:
    """Exact MITM with ``Sigma(core) + Sigma(R1)`` on one side and ``Sigma(R2)`` on the other."""
    n = len(values)
    in_core = set(indices)
    rest = [i for i in range(n) if i not in in_core]
    r = len(rest)
    x = max(0, min(r, round((r - log2(len(sigma))) / 2)))
    r1, r2 = rest[:x], rest[x:]
    sums1 = _subset_sums(values, r1, 1 << 30)
    sums2 = _subset_sums(values, r2, 1 << 30)
    assert sums1 is not None and sums2 is not None
    states = len(sigma) + len(sums1) + len(sums2)
    left_count = 0
    for s_c, m_c in sigma.items():
        for s_1, m_1 in sums1.items():
            left_count += 1
            hit = sums2.get(target - s_c - s_1)
            if hit is not None:
                mask = m_c | m_1 | hit
                found = tuple(i for i in range(n) if mask >> i & 1)
                return CompressedResult(
                    found, label, states + left_count, len(indices), len(sigma)
                )
    return CompressedResult(None, label, states + left_count, len(indices), len(sigma))


def relation_components(values: Sequence[int], smax: int, cap: int = 1 << 21):
    """``{s: [component, ...]}``: connected components of the relation graph.

    Two elements are joined when they occur in the same relation (an equal-sum pair of
    distinct subsets of size ``<= s``, common elements removed).
    """
    n = len(values)
    by_sum: dict[int, list[int]] = defaultdict(list)
    parent = list(range(n))

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    out: dict[int, list[set[int]]] = {}
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
        involved = set()
        for masks in by_sum.values():
            if len(masks) > 1:
                for a, b in combinations(masks, 2):
                    rel = (a | b) & ~(a & b)
                    members = [i for i in range(n) if rel >> i & 1]
                    involved.update(members)
                    for i in members[1:]:
                        ra, rb = find(members[0]), find(i)
                        if ra != rb:
                            parent[rb] = ra
        groups: dict[int, set[int]] = defaultdict(set)
        for i in involved:
            groups[find(i)].add(i)
        out[s] = list(groups.values())
    return out


def solve_components(
    values: Sequence[int],
    target: int,
    smax: int = 4,
    sigma_cap: int = 1 << 20,
    min_gain: float = 0.5,
) -> CompressedResult:
    """Like ``solve_compressed`` but builds the core from compressible components only.

    Each relation-graph component ``K`` has gain ``|K| - log2 |Sigma(K)|``; components are
    added in decreasing gain per element while the total predicted cost
    ``|Sigma(C)| + 2 sqrt(2^{n-|C|} |Sigma(C)|)`` decreases. Elements in short relations
    that do not compress (adversarial decoy gadgets) are therefore left out.
    """
    values = tuple(values)
    n = len(values)
    best = None
    for comps in relation_components(values, smax).values():
        scored = []
        for comp in comps:
            sig = _subset_sums(values, sorted(comp), sigma_cap)
            if sig is None:
                continue
            gain = len(comp) - log2(len(sig))
            if gain >= min_gain:
                scored.append((gain / len(comp), sorted(comp)))
        scored.sort(reverse=True)
        chosen: list[int] = []
        sigma = {0: 0}
        cost = 2 * 2 ** (n / 2)
        for _ratio, comp in scored:
            trial = sorted(chosen + comp)
            sig = _subset_sums(values, trial, sigma_cap)
            if sig is None:
                break
            new_cost = len(sig) + 2 * (2 ** (n - len(trial)) * len(sig)) ** 0.5
            if new_cost < cost:
                chosen, sigma, cost = trial, sig, new_cost
        if chosen and (best is None or cost < best[0]):
            best = (cost, chosen, sigma)
    if best is None or best[0] >= 2 ** (n // 2 + 1):
        fallback = meet_in_middle(values, target)
        return CompressedResult(fallback.indices, "mitm", fallback.states, 0, 0)
    return _mitm_with_core(values, target, best[1], best[2], "components")


def solve_grow(
    values: Sequence[int],
    target: int,
    smax: int = 3,
    sigma_cap: int = 1 << 21,
) -> CompressedResult:
    """Greedy element-wise core growth, robust to decoys glued into relation components.

    Starting from the empty set, repeatedly add the element (preferring elements that occur
    in a short relation) whose addition makes ``Sigma(C)`` grow least; an element unrelated
    to ``C`` doubles it, a structured one grows it by less. The prefix of this order with the
    smallest predicted cost ``|Sigma(C)| + 2 sqrt(2^{n-|C|} |Sigma(C)|)`` is used. Exact
    whatever the order is.
    """
    values = tuple(values)
    n = len(values)
    cores, _ = find_cores(values, smax)
    related = set().union(*cores.values()) if cores else set()
    sigma: dict[int, int] = {0: 0}
    chosen: list[int] = []
    best = (2 * 2 ** (n / 2), [], {0: 0})
    remaining = set(range(n))
    while remaining:
        pick = None
        for e in sorted(remaining, key=lambda i: (i not in related, i)):
            size = len(sigma.keys() | {t + values[e] for t in sigma})
            if pick is None or size < pick[0]:
                pick = (size, e)
        _size, e = pick
        grown = dict(sigma)
        for t, mask in sigma.items():
            grown.setdefault(t + values[e], mask | (1 << e))
        if len(grown) > sigma_cap:
            break
        sigma = grown
        chosen.append(e)
        remaining.discard(e)
        cost = len(sigma) + 2 * (2 ** (n - len(chosen)) * len(sigma)) ** 0.5
        if cost < best[0]:
            best = (cost, list(chosen), sigma)
    if not best[1] or best[0] >= 2 ** (n // 2 + 1):
        fallback = meet_in_middle(values, target)
        return CompressedResult(fallback.indices, "mitm", fallback.states, 0, 0)
    return _mitm_with_core(values, target, sorted(best[1]), best[2], "grow")

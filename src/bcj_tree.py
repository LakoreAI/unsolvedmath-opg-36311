"""Three-level Becker-Coron-Joux tree (ePrint 2011/474, Sect. 3.3).

Ports the concrete algorithm: a balanced solution ``eps in {0,1}^n`` with
``n/2`` ones is written ``eps = nu1 + nu2``; each ``nu`` splits into two
``kappa`` vectors, each of which splits into two ``omega`` vectors (eight
leaves), with ``alpha``, ``beta``, ``gamma`` extra ``-1``s added at the three
levels. Leaf lists are filtered modulo ``M_omega`` with random residues
``R_omega^(j)`` (the last fixed by the sum), the middle level by ``M_kappa``,
the top level by ``M_nu``, and the two top lists are matched on the exact
integer target. Every merge keeps only *consistent* pairs: no coordinate of
``+-2`` and exactly the prescribed number of ``1``s and ``-1``s.

Parameters here are integer *counts* (``a``, ``b``, ``g`` = ``alpha n``,
``beta n``, ``gamma n``), not proportions, because the profile counts must be
integral and the halvings even. The leaves are enumerated directly (all vectors
of the leaf profile, bucketed by residue) rather than by BCJ's birthday split,
so the leaf cost is the leaf *ambient* size; the list-size bookkeeping
(``stats``) is what this module is for. It is a faithful structural port at toy
``n``, not a performance implementation: the poly(n) and constant factors
dominate there.
"""

from dataclasses import dataclass
from math import comb, factorial
from random import Random
from collections.abc import Sequence

from src.bcj import enumerate_profile
from src.subset_sum import meet_in_middle

Vec = tuple[int, int, int]  # (plus_mask, minus_mask, integer sum)


@dataclass(frozen=True)
class Profile:
    ones: int
    minus: int


@dataclass(frozen=True)
class TreeParams:
    n: int
    a: int
    b: int
    g: int

    def __post_init__(self) -> None:
        if self.n % 8:
            raise ValueError("n must be a multiple of 8")
        nu, kappa = self.nu, self.kappa
        if nu.ones % 2 or nu.minus % 2 or kappa.ones % 2 or kappa.minus % 2:
            raise ValueError("profile counts must be even where they are halved")

    @property
    def nu(self) -> Profile:
        return Profile(self.n // 4 + self.a, self.a)

    @property
    def kappa(self) -> Profile:
        nu = self.nu
        return Profile(nu.ones // 2 + self.b, nu.minus // 2 + self.b)

    @property
    def omega(self) -> Profile:
        kappa = self.kappa
        return Profile(kappa.ones // 2 + self.g, kappa.minus // 2 + self.g)


def _multinomial(total: int, *parts: int) -> int:
    rest = total - sum(parts)
    if rest < 0 or any(p < 0 for p in parts):
        return 0
    value = factorial(total) // factorial(rest)
    for part in parts:
        value //= factorial(part)
    return value


def modulus_targets(params: TreeParams) -> tuple[int, int, int]:
    """Targets for ``M_omega``, ``M_kappa * M_omega``, ``M_nu * M_kappa * M_omega``.

    Each equals the number of decompositions of a vector one level up into two
    vectors one level down (BCJ Sect. 3.3), so that on average one survives.
    """
    n = params.n
    nu, kappa, omega = params.nu, params.kappa, params.omega
    g1 = omega.ones - kappa.ones // 2
    gm = omega.minus - kappa.minus // 2
    t_omega = (
        comb(kappa.ones, kappa.ones // 2)
        * comb(kappa.minus, kappa.minus // 2)
        * _multinomial(n - kappa.ones - kappa.minus, g1, gm)
    )
    b1 = kappa.ones - nu.ones // 2
    bm = kappa.minus - nu.minus // 2
    t_kappa = (
        comb(nu.ones, nu.ones // 2)
        * comb(nu.minus, nu.minus // 2)
        * _multinomial(n - nu.ones - nu.minus, b1, bm)
    )
    t_nu = comb(n // 2, n // 4) * _multinomial(n // 2, params.a, params.a)
    return max(2, t_omega), max(2, t_kappa), max(2, t_nu)


def _next_prime(lower: int, avoid: Sequence[int] = ()) -> int:
    candidate = max(2, lower)
    while candidate in avoid or any(
        candidate % d == 0 for d in range(2, int(candidate**0.5) + 1)
    ):
        candidate += 1
    return candidate


def tree_moduli(params: TreeParams) -> tuple[int, int, int]:
    """Distinct primes ``(M_omega, M_kappa, M_nu)`` near the BCJ targets."""
    t_omega, t_kappa, t_nu = modulus_targets(params)
    m_omega = _next_prime(t_omega)
    m_kappa = _next_prime(max(2, t_kappa // m_omega), (m_omega,))
    m_nu = _next_prime(max(2, t_nu // (m_omega * m_kappa)), (m_omega, m_kappa))
    return m_omega, m_kappa, m_nu


def _combine(left: Vec, right: Vec, profile: Profile | None) -> Vec | None:
    """Sum two ternary vectors; ``None`` if inconsistent (``+-2`` or wrong profile)."""
    lp, lm, ls = left
    rp, rm, rs = right
    if lp & rp or lm & rm:
        return None
    plus = (lp | rp) & ~(lm | rm)
    minus = (lm | rm) & ~(lp | rp)
    if profile is not None and (
        plus.bit_count() != profile.ones or minus.bit_count() != profile.minus
    ):
        return None
    return plus, minus, ls + rs


def _merge(
    left: list[Vec],
    right: list[Vec],
    modulus: int,
    residue: int,
    profile: Profile,
) -> tuple[list[Vec], int]:
    """Modular match (Algorithm 1) + consistency; returns (list, raw match count)."""
    by_residue: dict[int, list[Vec]] = {}
    for vec in right:
        by_residue.setdefault(vec[2] % modulus, []).append(vec)
    out: list[Vec] = []
    raw = 0
    for vec in left:
        for other in by_residue.get((residue - vec[2]) % modulus, ()):
            raw += 1
            merged = _combine(vec, other, profile)
            if merged is not None:
                out.append(merged)
    return out, raw


@dataclass
class TreeStats:
    leaf: list[int]
    kappa_raw: list[int]
    kappa: list[int]
    nu_raw: list[int]
    nu: list[int]
    k0: int


@dataclass(frozen=True)
class TreeResult:
    indices: tuple[int, ...] | None
    strategy: str
    attempts: int
    stats: TreeStats | None


def _leaf_buckets(
    values: Sequence[int], profile: Profile, modulus: int
) -> dict[int, list[Vec]]:
    n = len(values)
    buckets: dict[int, list[Vec]] = {}
    for plus, minus in enumerate_profile(n, profile.ones, profile.minus):
        total = 0
        for i in range(n):
            if plus >> i & 1:
                total += values[i]
            elif minus >> i & 1:
                total -= values[i]
        buckets.setdefault(total % modulus, []).append((plus, minus, total))
    return buckets


def bcj_tree_attempt(
    values: Sequence[int],
    target: int,
    params: TreeParams,
    moduli: tuple[int, int, int],
    rng: Random,
    buckets: dict[int, list[Vec]] | None = None,
) -> tuple[tuple[int, ...] | None, TreeStats]:
    """One run with fresh random residues; returns a solution or ``None``."""
    values = tuple(values)
    n = len(values)
    m_omega, m_kappa, m_nu = moduli
    if buckets is None:
        buckets = _leaf_buckets(values, params.omega, m_omega)

    r_omega = [rng.randrange(m_omega) for _ in range(7)]
    r_omega.append((target - sum(r_omega)) % m_omega)
    leaves = [buckets.get(r, []) for r in r_omega]

    r_kappa = [rng.randrange(m_kappa) for _ in range(3)]
    r_kappa.append((target - sum(r_kappa)) % m_kappa)
    kappa_lists, kappa_raw = [], []
    for j in range(4):
        got, raw = _merge(
            leaves[2 * j], leaves[2 * j + 1], m_kappa, r_kappa[j], params.kappa
        )
        kappa_lists.append(got)
        kappa_raw.append(raw)

    r_nu = [rng.randrange(m_nu)]
    r_nu.append((target - r_nu[0]) % m_nu)
    nu_lists, nu_raw = [], []
    for j in range(2):
        got, raw = _merge(
            kappa_lists[2 * j], kappa_lists[2 * j + 1], m_nu, r_nu[j], params.nu
        )
        nu_lists.append(got)
        nu_raw.append(raw)

    final = Profile(n // 2, 0)
    by_sum: dict[int, list[Vec]] = {}
    for vec in nu_lists[1]:
        by_sum.setdefault(vec[2], []).append(vec)
    k0 = 0
    solution: tuple[int, ...] | None = None
    for vec in nu_lists[0]:
        for other in by_sum.get(target - vec[2], ()):
            k0 += 1
            merged = _combine(vec, other, final)
            if merged is not None and solution is None:
                solution = tuple(i for i in range(n) if merged[0] >> i & 1)
    stats = TreeStats(
        leaf=[len(x) for x in leaves],
        kappa_raw=kappa_raw,
        kappa=[len(x) for x in kappa_lists],
        nu_raw=nu_raw,
        nu=[len(x) for x in nu_lists],
        k0=k0,
    )
    return solution, stats


def bcj_tree_subset_sum(
    values: Sequence[int],
    target: int,
    params: TreeParams,
    attempts: int = 16,
    seed: int = 0,
) -> TreeResult:
    """Three-level BCJ search for a weight-``n/2`` solution; MITM fallback."""
    values = tuple(values)
    n = len(values)
    if n != params.n:
        raise ValueError("params.n must equal len(values)")
    moduli = tree_moduli(params)
    buckets = _leaf_buckets(values, params.omega, moduli[0])
    rng = Random(seed)
    last: TreeStats | None = None
    for attempt in range(1, attempts + 1):
        solution, last = bcj_tree_attempt(values, target, params, moduli, rng, buckets)
        if solution is not None:
            return TreeResult(solution, "bcj-tree", attempt, last)
    fallback = meet_in_middle(values, target)
    return TreeResult(fallback.indices, "mitm", attempts, last)

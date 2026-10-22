/-! # Floating-Point Reproduction of the Filtering Moments (Proposition 3.1)

Executable `Float` recomputation of the preprint's Section 3 filter: the
normalizers, the convolution table `P̂_j, Ŷ_j`, the node integrands
`X̂_j, X̂'_j` (Appendix A, Table 1), and the `N`-point averages of
`M(x)² 2^(8.5(Δ-u))` and `M(x)² 2^(8.3(av-u))` compared with `2^0.5168`.

This is an independent numerical check, not a proof: IEEE `Float` evaluation is
outside the kernel. The kernel-checked scalar steps are in
`SubsetSum.Audit049Constants`. -/
namespace SubsetSum.Audit049Filter

def rCoeffs : List Float := [0.851, 0.466, 0.325, 0.253, 0.224, -0.314]
def sCoeffs : List Float := [1.281, -0.938, 0.731, -0.559, 0.391, 0.110]
def kappa : Float := 1.0315
def eta : Float := 0.51772
def tau : Float := 0.48996
def bigDelta : Float := eta - tau
def bigGamma : Float := 2 * tau - eta
def aRatio : Float := bigDelta / bigGamma

def pi : Float := 3.14159265358979323846

/-- `Σ_j c_j cos(j x)` for `j = 1, 2, …`. -/
def trig (cs : List Float) (x : Float) : Float :=
  (cs.foldl (fun (acc : Float × Float) c => (acc.1 + c * Float.cos (acc.2 * x), acc.2 + 1))
    (0, 1)).1

def grid (n : Nat) : Array Float :=
  (Array.range n).map fun j => 2 * pi * j.toFloat / n.toFloat

def mean (xs : Array Float) : Float :=
  xs.foldl (· + ·) 0 / xs.size.toFloat

/-- Normalizers, convolution columns, node integrands, and the two moments. -/
structure FilterTable where
  zf : Float
  zg : Float
  zfk : Float
  zgk : Float
  h : Float
  p : Array Float
  y : Array Float
  x1 : Array Float
  x2 : Array Float
  moment1 : Float
  moment2 : Float

/-- Equations (3.2), (A.1), and (A.2) with every circle integral replaced by
the `n`-point average. -/
def filterTable (n : Nat) : FilterTable :=
  let xs := grid n
  let r := xs.map (trig rCoeffs)
  let s := xs.map (trig sCoeffs)
  let f := r.map (Float.exp2 ·)
  let g := s.map (Float.exp2 ·)
  let zf := mean f
  let zg := mean g
  let zfk := mean (f.map (· ^ kappa))
  let zgk := mean (g.map (· ^ kappa))
  let lz := Float.log2 (zf * zg)
  let h := Float.log2 zfk + Float.log2 zgk - kappa * lz
  let rows := (Array.range n).map fun j =>
    let pj := mean ((Array.range n).map fun i => f[(i + j) % n]! * g[i]!)
    let yj := mean ((Array.range n).map fun i =>
      f[(i + j) % n]! * g[i]! * (r[(i + j) % n]! + s[i]!))
    let l := Float.log2 pj - lz
    let b := yj / pj - lz
    let u := l + (kappa - 1) * b - h
    let v := (2 - kappa) * b - 2 * l + h
    let m2 := 2 + 2 * Float.cos xs[j]!
    (pj, yj, m2 * Float.exp2 (8.5 * (bigDelta - u)), m2 * Float.exp2 (8.3 * (aRatio * v - u)))
  let x1 := rows.map (·.2.2.1)
  let x2 := rows.map (·.2.2.2)
  { zf, zg, zfk, zgk, h,
    p := rows.map (·.1), y := rows.map (·.2.1), x1, x2,
    moment1 := mean x1, moment2 := mean x2 }

/-- Threshold `2^0.5168` of Proposition 3.1. -/
def threshold : Float := Float.exp2 0.5168

end SubsetSum.Audit049Filter

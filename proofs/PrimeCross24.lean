import Std

/-!
Congruence lemmas for the auxiliary primes in Alpöge's WinPair.
The argument uses the Lean standard library. The analytic hypotheses on these
primes belong to the original proof and are not among these statements.
-/
namespace PrimeCross24

/-- The admissible spokes for a prime q > 3 with q ≡ 3 mod 8. -/
theorem q_spokes (q : Nat) (h8 : q % 8 = 3) (h3 : q % 3 ≠ 0) :
    q % 24 = 11 ∨ q % 24 = 19 := by
  omega

/-- The two local restrictions on d determine one class modulo 48. -/
theorem d_spoke (d : Nat) :
    (d % 16 = 7 ∧ d % 3 = 2) ↔ d % 48 = 23 := by
  omega

private theorem odd_factor (a b : Fin 16) (ha : a.val % 2 = 1)
    (hab : (a.val * b.val) % 16 = 8) : b.val = 8 := by
  have hall : ∀ i j : Fin 16, i.val % 2 = 1 →
      (i.val * j.val) % 16 = 8 → j.val = 8 := by decide
  exact hall a b ha hab

/-- For odd M, the CRT representative for d is explicitly 8*M - 1. -/
theorem auxiliary_congruence (M d : Nat) (hodd : M % 2 = 1) :
    (d % 16 = 7 ∧ M ∣ d + 1) ↔ d % (16 * M) = 8 * M - 1 := by
  have hM : 0 < M := by omega
  have hres : 8 * M - 1 < 16 * M := by omega
  constructor
  · rintro ⟨hd, k, hk⟩
    have hp : (M * k) % 16 = 8 := by omega
    have h₁₆ : k % 16 = 8 := by
      apply odd_factor ⟨M % 16, Nat.mod_lt _ (by decide)⟩
        ⟨k % 16, Nat.mod_lt _ (by decide)⟩
      · change M % 16 % 2 = 1
        omega
      · change ((M % 16) * (k % 16)) % 16 = 8
        rw [← Nat.mul_mod]
        exact hp
    have hk' : k = 8 + 16 * (k / 16) := by omega
    have hprod : M * k = 8 * M + (16 * M) * (k / 16) := calc
      M * k = M * (8 + 16 * (k / 16)) := congrArg (M * ·) hk'
      _ = _ := by simp [Nat.mul_add, Nat.mul_left_comm, Nat.mul_comm]
    have hd' : d = (8 * M - 1) + (16 * M) * (k / 16) := by omega
    rw [hd', Nat.add_mul_mod_self_left, Nat.mod_eq_of_lt hres]
  · intro h
    let j := d / (16 * M)
    have hd' : d = (8 * M - 1) + (16 * M) * j := by
      simpa [j, h] using (Nat.mod_add_div d (16 * M)).symm
    have hprod : (16 * M) * j = 16 * (M * j) := Nat.mul_assoc _ _ _
    have h8 : (8 * M) % 16 = 8 := by omega
    constructor
    · omega
    · refine ⟨8 + 16 * j, ?_⟩
      have hmul : M * (8 + 16 * j) = 8 * M + (16 * M) * j := by
        simp [Nat.mul_add, Nat.mul_assoc, Nat.mul_comm]
      omega

/-- The representative is coprime to the modulus, as needed for Dirichlet's theorem. -/
theorem auxiliary_coprime (M : Nat) (hM : 0 < M) :
    Nat.gcd (8 * M - 1) (16 * M) = 1 := by
  have hlt : 2 < 8 * M - 1 := by omega
  have hodd : (8 * M - 1) % 2 = 1 := by omega
  have heq : 16 * M = 2 + (8 * M - 1) * 2 := by omega
  have hrem : (16 * M) % (8 * M - 1) = 2 := calc
    _ = (2 + (8 * M - 1) * 2) % (8 * M - 1) := congrArg (· % (8 * M - 1)) heq
    _ = 2 := by rw [Nat.add_mul_mod_self_left, Nat.mod_eq_of_lt hlt]
  rw [Nat.gcd_rec (8 * M - 1) (16 * M), hrem,
    Nat.gcd_rec 2 (8 * M - 1), hodd, Nat.gcd_one_left]

/-- The original CRT lemma, with an explicit witness and the same statement. -/
theorem exists_coprime_class (M : Nat) (h : Nat.Coprime 2 M) :
    ∃ a : Nat, Nat.Coprime a (16 * M) ∧
      ∀ d : Nat, (d % 16 = 7 ∧ M ∣ d + 1) ↔
        d % (16 * M) = a % (16 * M) := by
  change Nat.gcd 2 M = 1 at h
  have hodd : M % 2 = 1 := by
    have hn : M % 2 ≠ 0 := by
      intro hz
      rw [Nat.gcd_rec 2 M, hz, Nat.gcd_zero_left] at h
      contradiction
    omega
  have hM : 0 < M := by omega
  refine ⟨8 * M - 1, auxiliary_coprime M hM, fun d => ?_⟩
  rw [Nat.mod_eq_of_lt (show 8 * M - 1 < 16 * M by omega)]
  exact auxiliary_congruence M d hodd

end PrimeCross24

#print axioms PrimeCross24.q_spokes
#print axioms PrimeCross24.d_spoke
#print axioms PrimeCross24.auxiliary_congruence
#print axioms PrimeCross24.auxiliary_coprime
#print axioms PrimeCross24.exists_coprime_class

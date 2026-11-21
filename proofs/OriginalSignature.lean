import PrimeCross24

/- The upstream private declaration written with Std's Nat notation. -/
namespace QH

private theorem chineseRemainder_finiteCover (M : Nat) (h : Nat.Coprime 2 M) :
    ∃ a : Nat, a.Coprime (16 * M) ∧
      ∀ d : Nat, (d % 16 = 7 ∧ M ∣ d + 1) ↔
        d % (16 * M) = a % (16 * M) := by
  exact PrimeCross24.exists_coprime_class M h

#print axioms chineseRemainder_finiteCover

end QH

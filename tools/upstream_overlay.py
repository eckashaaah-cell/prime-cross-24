"""Write the two modified modules to a new directory for review."""
import argparse
import hashlib
from pathlib import Path

MODULE = Path("src/Development/AutomorphicArithmetic/MeanSquareBounds/"
              "ExistsCoprimePrimePairSetSecondEqPPset.lean")
DIGEST = "3f84b9311e74e47e3b0ab92ab04a56f89f15021e323f153b409c9d9422624a9b"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("upstream", type=Path, help="root containing the original src tree")
    parser.add_argument("destination", type=Path, help="new directory for the overlay")
    args = parser.parse_args()
    original = (args.upstream / MODULE).read_bytes()
    if hashlib.sha256(original).hexdigest() != DIGEST:
        raise SystemExit("Upstream file does not match the pinned revision in SOURCES.md.")
    text = original.decode("utf-8")
    start = text.index("private theorem chineseRemainder_finiteCover ")
    proof = text.index(":= by\n", start) + len(":= by\n")
    next_decl = text.index("\ntheorem exists_coprime_primePairSetSecond_eq_PPset", proof)
    replacement = ("import PrimeCross24\n" + text[:proof] +
                   "  exact PrimeCross24.exists_coprime_class M h\n" + text[next_decl:])
    root = Path(__file__).resolve().parents[1]
    # Drop the audit commands from the helper used in the upstream tree.
    helper = (root / "proofs/PrimeCross24.lean").read_bytes()
    helper = helper.split(b"\n#print axioms ", maxsplit=1)[0]
    args.destination.mkdir(parents=True, exist_ok=False)
    target = args.destination / MODULE
    target.parent.mkdir(parents=True)
    target.write_bytes(replacement.encode("utf-8"))
    (args.destination / "src/PrimeCross24.lean").write_bytes(helper)
    print(f"Wrote {MODULE.as_posix()} and src/PrimeCross24.lean")


if __name__ == "__main__":
    main()

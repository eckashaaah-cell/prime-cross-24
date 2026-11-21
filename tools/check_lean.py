"""Check the two local Lean modules with fresh compiled objects."""
import argparse
import os
from pathlib import Path
import subprocess
import tempfile


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lean", default="lean", help="Lean executable (4.33.1)")
    args = parser.parse_args()
    source = Path(__file__).resolve().parents[1] / "proofs"
    version = subprocess.check_output([args.lean, "--version"], text=True).strip()
    if "version 4.33.1," not in version:
        raise SystemExit(f"Expected the release pinned in lean-toolchain. Found {version}")
    print(version, flush=True)
    with tempfile.TemporaryDirectory(prefix="prime-cross-lean-") as build:
        env = os.environ.copy()
        env["LEAN_PATH"] = build
        for module in ("PrimeCross24", "OriginalSignature"):
            target = Path(build) / f"{module}.olean"
            print(f"Checking {module}.lean", flush=True)
            subprocess.run([args.lean, "-DwarningAsError=true", "-o", str(target),
                            f"{module}.lean"], cwd=source, env=env, check=True)
    print("Both local modules compiled.")


if __name__ == "__main__":
    main()

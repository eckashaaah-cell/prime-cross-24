"""Reproducible checks of the formulas in the paper. Only Python 3.10+ is needed."""
import argparse
import json
import math
from fractions import Fraction
from pathlib import Path


def check(test, message):
    if not test:
        raise ArithmeticError(message)


def local(prime, phase):
    length = math.log(prime)
    v = phase % 1.0
    return length * (math.exp(length * v) / (prime - 1) - v)


def constants(prime):
    length = math.log(prime)
    a = length / (prime - 1)
    b = 1 + math.log(a)
    h = (1 / (1 - a) + 1 / (prime * a - 1)) / length
    return a, b, h


def check_deletion():
    inputs = {Fraction(n, d) for d in (1, 2, 7) for n in range(d, 601)}
    for prime in (2, 3, 5):
        for exponent in range(1, 45):
            for delta in (-1, 0, 1):
                inputs.add(Fraction(37 * prime ** exponent + delta, 37))
    for x in inputs:
        for prime in (2, 3, 5):
            power = prime
            exponent = 0
            brute = Fraction()
            while power <= x:
                brute += x / power - 1
                power *= prime
                exponent += 1
            u = x / (power // prime)
            closed = (x - u) / (prime - 1) - exponent
            check(closed == brute, f"finite geometric coefficient at {x}, {prime}")
    return {"distinct_rational_inputs": len(inputs), "coefficient_comparisons": 3 * len(inputs)}


def check_aggregate():
    # Independent sieve for the unrestricted and eight-class prime sums.
    limit = 2500
    weights = [0.0] * (limit + 1)
    for n in range(2, limit + 1):
        if any(n % d == 0 for d in range(2, math.isqrt(n) + 1)):
            continue
        power = n
        while power <= limit:
            weights[power] = math.log(n)
            power *= n
    c = constants(2)[0] + constants(3)[0]
    worst = 0.0
    for x in [1.0, 1.5, 19 / 3, 24.25] + [float(i) for i in range(2, limit, 13)]:
        terms = [weights[n] * (x / n - 1) for n in range(1, int(x) + 1)]
        total = math.fsum(terms)
        reduced = math.fsum(v for n, v in enumerate(terms, 1) if math.gcd(n, 24) == 1)
        t = math.log(x)
        exact_shift = 2 * t + sum(local(p, t / math.log(p)) for p in (2, 3))
        worst = max(worst, abs((reduced - total) + c * x - exact_shift))
    check(worst < 2e-10, "aggregate normalization")
    return worst


class Branches:
    """Solve f(v)=y on the closed interval, keeping the two inverse branches."""
    def __init__(self, prime):
        self.length = math.log(prime)
        self.a, self.b, self.h = constants(prime)
        self.turn = -math.log(self.a) / self.length

    def interval(self, y):
        if y <= self.b:
            return self.turn, self.turn
        if y >= self.a:
            return 0.0, 1.0
        roots = []
        for left, right, rising in ((0.0, self.turn, False), (self.turn, 1.0, True)):
            for _ in range(51):
                mid = (left + right) / 2
                value = self.a * math.exp(self.length * mid) - self.length * mid
                if (value < y) == rising:
                    left = mid
                else:
                    right = mid
            roots.append((left + right) / 2)
        return roots


def endpoint_check(s, upper, steps=2048):
    # Integrate inverse-branch widths against independent phase in base 2.
    x, y = Branches(2), Branches(3)
    cut = x.a + y.a - s if upper else x.b + y.b + s
    q0, q1 = x.interval(x.a - s if upper else x.b + s)
    intervals = [(0, q0), (q1, 1)] if upper else [(q0, q1)]
    total = 0.0
    for lo, hi in intervals:
        segment = []
        for i in range(steps):
            v = lo + (i + 0.5) * (hi - lo) / steps
            v0, v1 = y.interval(cut - local(2, v))
            segment.append(v0 + 1 - v1 if upper else v1 - v0)
        total += (hi - lo) * math.fsum(segment) / steps
    coefficient = x.h * y.h / 2 if upper else 2 * math.pi / (x.length * y.length)
    return total / (coefficient * (s ** 2 if upper else s))


def check_sampling():
    p, q = 2, 3
    lp, lq = math.log(p), math.log(q)
    n = 60000
    t = math.log(n)
    actual = math.fsum(local(p, math.log(i) / lp) + local(q, math.log(i) / lq)
                       for i in range(1, n + 1)) / n
    # Midpoint quadrature in exponential time, independent of integer endpoints.
    count, dt = 50000, 25 / 50000
    def term(index):
        u = (index + 0.5) * dt
        return (local(p, (t - u) / lp) + local(q, (t - u) / lq)) * math.exp(-u)
    predicted = dt * math.fsum(term(i) for i in range(count))
    check(abs(actual - predicted) < 4e-5, "integer sampling mean and phase law")
    circle_mean = sum(math.fsum(local(j, (i + 0.5) / 10000)
                                for i in range(10000)) / 10000 for j in (p, q))
    mean = 2 - math.log(p * q) / 2
    check(abs(circle_mean - mean) < 2e-9, "logarithmic mean")
    return {"integer_cutoff": n, "integer_mean": actual, "phase_mean": predicted,
            "logarithmic_mean": mean, "torus_quadrature": circle_mean}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", type=Path)
    args = parser.parse_args()
    a2, b2, h2 = constants(2)
    a3, b3, h3 = constants(3)
    tails = []
    for s in (1e-3, 1e-4, 1e-5):
        tails.append({"s": s, "lower_ratio_to_asymptotic": endpoint_check(s, False),
                      "upper_ratio_to_asymptotic": endpoint_check(s, True)})
    for key in ("lower_ratio_to_asymptotic", "upper_ratio_to_asymptotic"):
        check(abs(tails[-1][key] - 1) < 4e-4, f"tail quadrature: {key}")
    gamma = 0.5772156649015328606
    c = 2 + gamma - math.log(4 * math.pi)
    j1 = 1 - math.log(2)
    # Evaluate W_24(1) from the original normalization, including both local terms.
    w1 = (1 + gamma + a2 + a3) - (local(2, 0) + local(3, 0)) - math.log(2 * math.pi) + j1
    check(abs(w1 - c) < 8e-16, "endpoint normalization for the RH criterion")
    report = {"exact_deletion": check_deletion(), "max_aggregate_abs_error": check_aggregate(),
              "support": [b2 + b3, a2 + a3],
              "endpoint_coefficients": [2 * math.pi / (math.log(2) * math.log(3)), h2 * h3 / 2],
              "tail_quadrature": tails, "sampling": check_sampling(), "RH_constant": c}
    output = json.dumps(report, indent=2, sort_keys=True) + "\n"
    print(output, end="")
    if args.json:
        with args.json.open("w", encoding="utf-8", newline="\n") as stream:
            stream.write(output)


if __name__ == "__main__":
    main()

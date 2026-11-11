# Python 3.13 (CPython) — native int for big integers, tuple trees, bytearray sieve
import sys

MOD = 1_000_000_007


def factmod(n):
    r = 1
    for i in range(1, n + 1):
        r = (r * i) % MOD
    return r


def bigfact(n):
    r = 1
    for i in range(2, n + 1):
        r *= i
    return r.bit_length()


def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)


def make(d):
    return (make(d - 1), make(d - 1)) if d > 0 else (None, None)


def check(node):
    l, r = node
    return 1 if l is None else 1 + check(l) + check(r)


def trees(maxd):
    keep = make(maxd)
    total = 0
    for d in range(4, maxd + 1, 2):
        for _ in range(1 << (maxd - d + 4)):
            total += check(make(d))
    return total + check(keep)


def sieve(n):
    # Idiomatic Python: slice assignment does the inner loop in C.
    s = bytearray([1]) * (n + 1)
    s[0] = s[1] = 0
    i = 2
    while i * i <= n:
        if s[i]:
            s[i * i :: i] = bytes(len(range(i * i, n + 1, i)))
        i += 1
    return s.count(1)


def main():
    w = sys.argv[1]
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    fns = {"factmod": factmod, "bigfact": bigfact, "fib": fib, "trees": trees, "sieve": sieve}
    print(fns[w](n) if w in fns else 0)


if __name__ == "__main__":
    main()

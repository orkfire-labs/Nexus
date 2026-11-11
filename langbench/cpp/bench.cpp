// C++20 (g++ -O2) — gmpxx for big integers, unique_ptr trees
#include <cstdint>
#include <cstdio>
#include <memory>
#include <string>
#include <vector>
#include <gmpxx.h>

constexpr uint64_t MOD = 1000000007ULL;

uint64_t factmod(long n) {
    uint64_t r = 1;
    for (long i = 1; i <= n; ++i) r = (r * static_cast<uint64_t>(i)) % MOD;
    return r;
}

long bigfact(long n) {
    mpz_class r = 1;
    for (long i = 2; i <= n; ++i) r *= static_cast<unsigned long>(i);
    return static_cast<long>(mpz_sizeinbase(r.get_mpz_t(), 2));
}

long fib(int n) { return n < 2 ? n : fib(n - 1) + fib(n - 2); }

struct Node { std::unique_ptr<Node> l, r; };
std::unique_ptr<Node> make(int d) {
    auto n = std::make_unique<Node>();
    if (d > 0) { n->l = make(d - 1); n->r = make(d - 1); }
    return n;
}
long check(const Node& n) { return n.l ? 1 + check(*n.l) + check(*n.r) : 1; }

long trees(int maxd) {
    auto keep = make(maxd);
    long total = 0;
    for (int d = 4; d <= maxd; d += 2) {
        long it = 1L << (maxd - d + 4);
        for (long i = 0; i < it; ++i) { auto t = make(d); total += check(*t); }
    }
    return total + check(*keep);
}

long sieve(long n) {
    std::vector<uint8_t> s(n + 1, 1);
    s[0] = s[1] = 0;
    for (long i = 2; i * i <= n; ++i)
        if (s[i]) for (long j = i * i; j <= n; j += i) s[j] = 0;
    long c = 0;
    for (auto v : s) c += v;
    return c;
}

int main(int argc, char** argv) {
    std::string w = argv[1];
    long n = argc > 2 ? std::stol(argv[2]) : 0;
    long long out = 0;
    if (w == "factmod") out = static_cast<long long>(factmod(n));
    else if (w == "bigfact") out = bigfact(n);
    else if (w == "fib") out = fib(static_cast<int>(n));
    else if (w == "trees") out = trees(static_cast<int>(n));
    else if (w == "sieve") out = sieve(n);
    std::printf("%lld\n", out);
}

// C (gcc -O2) — GMP for big integers
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <gmp.h>

#define MOD 1000000007ULL

static uint64_t factmod(long n) {
    uint64_t r = 1;
    for (long i = 1; i <= n; i++) r = (r * (uint64_t)i) % MOD;
    return r;
}

static long bigfact(long n) {
    mpz_t r; mpz_init_set_ui(r, 1);
    for (long i = 2; i <= n; i++) mpz_mul_ui(r, r, (unsigned long)i);
    long bits = (long)mpz_sizeinbase(r, 2);
    mpz_clear(r);
    return bits;
}

static long fib(int n) { return n < 2 ? n : fib(n - 1) + fib(n - 2); }

typedef struct Node { struct Node *l, *r; } Node;
static Node *make(int d) {
    Node *n = malloc(sizeof(Node));
    if (d > 0) { n->l = make(d - 1); n->r = make(d - 1); } else { n->l = n->r = NULL; }
    return n;
}
static long check(Node *n) { return n->l ? 1 + check(n->l) + check(n->r) : 1; }
static void freet(Node *n) { if (n->l) { freet(n->l); freet(n->r); } free(n); }

static long trees(int maxd) {
    Node *keep = make(maxd);
    long total = 0;
    for (int d = 4; d <= maxd; d += 2) {
        long it = 1L << (maxd - d + 4);
        for (long i = 0; i < it; i++) { Node *t = make(d); total += check(t); freet(t); }
    }
    total += check(keep); freet(keep);
    return total;
}

static long sieve(long n) {
    unsigned char *s = malloc(n + 1);
    memset(s, 1, n + 1); s[0] = s[1] = 0;
    for (long i = 2; i * i <= n; i++)
        if (s[i]) for (long j = i * i; j <= n; j += i) s[j] = 0;
    long c = 0;
    for (long i = 0; i <= n; i++) c += s[i];
    free(s);
    return c;
}

int main(int argc, char **argv) {
    const char *w = argv[1];
    long n = argc > 2 ? atol(argv[2]) : 0;
    long long out = 0;
    if (!strcmp(w, "noop")) out = 0;
    else if (!strcmp(w, "factmod")) out = (long long)factmod(n);
    else if (!strcmp(w, "bigfact")) out = bigfact(n);
    else if (!strcmp(w, "fib")) out = fib((int)n);
    else if (!strcmp(w, "trees")) out = trees((int)n);
    else if (!strcmp(w, "sieve")) out = sieve(n);
    printf("%lld\n", out);
    return 0;
}

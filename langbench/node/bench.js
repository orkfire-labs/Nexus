// Node.js 22 (V8) — BigInt for big integers, object trees, Uint8Array sieve
"use strict";

const MOD = 1000000007;

function factmod(n) {
  // r * i can exceed 2^53, so fixed-width math must go through BigInt or split multiply.
  // Idiomatic choice: BigInt 64-bit arithmetic.
  let r = 1n;
  const m = BigInt(MOD);
  for (let i = 1n, N = BigInt(n); i <= N; i++) r = (r * i) % m;
  return r;
}

function bigfact(n) {
  let r = 1n;
  for (let i = 2n, N = BigInt(n); i <= N; i++) r *= i;
  return r.toString(2).length;
}

function fib(n) {
  return n < 2 ? n : fib(n - 1) + fib(n - 2);
}

function make(d) {
  return d > 0 ? { l: make(d - 1), r: make(d - 1) } : { l: null, r: null };
}

function check(n) {
  return n.l === null ? 1 : 1 + check(n.l) + check(n.r);
}

function trees(maxd) {
  const keep = make(maxd);
  let total = 0;
  for (let d = 4; d <= maxd; d += 2) {
    const it = 2 ** (maxd - d + 4);
    for (let i = 0; i < it; i++) total += check(make(d));
  }
  return total + check(keep);
}

function sieve(n) {
  const s = new Uint8Array(n + 1).fill(1);
  s[0] = s[1] = 0;
  for (let i = 2; i * i <= n; i++)
    if (s[i]) for (let j = i * i; j <= n; j += i) s[j] = 0;
  let c = 0;
  for (let i = 0; i <= n; i++) c += s[i];
  return c;
}

const [w, a] = process.argv.slice(2);
const n = a ? Number(a) : 0;
const fns = { factmod, bigfact, fib, trees, sieve };
console.log(String(fns[w] ? fns[w](n) : 0));

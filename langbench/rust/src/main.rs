// Rust (cargo --release) — num-bigint for big integers, Box trees
use num_bigint::BigUint;
use std::env;

const MOD: u64 = 1_000_000_007;

fn factmod(n: u64) -> u64 {
    let mut r: u64 = 1;
    for i in 1..=n {
        r = (r * i) % MOD;
    }
    r
}

fn bigfact(n: u64) -> u64 {
    let mut r = BigUint::from(1u32);
    for i in 2..=n {
        r *= i;
    }
    r.bits()
}

fn fib(n: u32) -> u64 {
    if n < 2 { n as u64 } else { fib(n - 1) + fib(n - 2) }
}

struct Node {
    kids: Option<(Box<Node>, Box<Node>)>,
}

fn make(d: u32) -> Box<Node> {
    if d > 0 {
        Box::new(Node { kids: Some((make(d - 1), make(d - 1))) })
    } else {
        Box::new(Node { kids: None })
    }
}

fn check(n: &Node) -> u64 {
    match &n.kids {
        Some((l, r)) => 1 + check(l) + check(r),
        None => 1,
    }
}

fn trees(maxd: u32) -> u64 {
    let keep = make(maxd);
    let mut total = 0;
    let mut d = 4;
    while d <= maxd {
        let it = 1u64 << (maxd - d + 4);
        for _ in 0..it {
            let t = make(d);
            total += check(&t);
        }
        d += 2;
    }
    total + check(&keep)
}

fn sieve(n: usize) -> u64 {
    let mut s = vec![true; n + 1];
    s[0] = false;
    s[1] = false;
    let mut i = 2;
    while i * i <= n {
        if s[i] {
            let mut j = i * i;
            while j <= n {
                s[j] = false;
                j += i;
            }
        }
        i += 1;
    }
    s.iter().filter(|&&b| b).count() as u64
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let w = args[1].as_str();
    let n: u64 = args.get(2).map(|s| s.parse().unwrap()).unwrap_or(0);
    let out = match w {
        "factmod" => factmod(n),
        "bigfact" => bigfact(n),
        "fib" => fib(n as u32),
        "trees" => trees(n as u32),
        "sieve" => sieve(n as usize),
        _ => 0,
    };
    println!("{}", out);
}

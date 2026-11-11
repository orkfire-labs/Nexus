# langbench — CPU & memory benchmark across 8 languages

C, C++, Rust, Go, Java, C#, Python and Node.js each implement the same six workloads.
Every program prints a checksum, and the harness checks that all languages agree, so
no implementation can win by doing less work.

| Workload | n | What it stresses |
|---|---|---|
| `noop` | – | Runtime start-up cost and baseline memory |
| `factmod` | 50,000,000 | `n! mod 1e9+7`, iterative: tight integer loop (pure CPU) |
| `bigfact` | 100,000 | Exact `n!` with big integers: bigint library + heap growth |
| `fib` | 37 | Naive recursive Fibonacci: function-call overhead |
| `trees` | 18 | Allocate/free millions of tree nodes: allocator & GC |
| `sieve` | 100,000,000 | Sieve of Eratosthenes: memory bandwidth & array layout |

## Run it

Prerequisites: gcc/g++, libgmp-dev, Rust (cargo), Go, JDK 21, .NET 8 SDK, Python 3, Node.js, GNU time (`/usr/bin/time`).

```bash
./build.sh                       # optimised/release builds into bin/
python3 run.py                   # 1 warm-up + 5 measured runs per (language, workload)
python3 run.py --runs 10 --only "C#,Java,Go" --workloads trees,bigfact
```

Results go to `results/raw.csv` (every run), `results/summary.csv` (medians) and `results/env.txt`.

## What is measured

Each run is a fresh process measured with GNU time:

- **wall_s** — elapsed time
- **cpu_s** — user + system CPU time, including start-up, JIT and GC threads (can exceed wall)
- **peak_rss_mb** — maximum resident set size

## For trustworthy numbers on your machine

- Use a quiet, dedicated machine; on Linux, set the `performance` governor and disable turbo.
- Pin to a core with `taskset -c 2 python3 run.py` to cut scheduler noise.
- Treat differences inside the min–max spread as ties.
- For in-process, steady-state numbers, use each language's harness instead: BenchmarkDotNet (.NET),
  JMH (Java), criterion (Rust), `testing.B` + benchstat (Go), pyperf (Python), mitata (Node).

## Fairness rule used

Same algorithm in every language, written idiomatically, using each ecosystem's standard
big-integer library. Notes:

- Python's sieve uses slice assignment, which is idiomatic and runs the inner loop in C.
- Node's `factmod` uses BigInt because `r * i` overflows 2^53.
- C# runs on the JIT with the default workstation GC. Native AOT or Server GC would change start-up and memory.
- Java uses default JVM flags (G1, heap sized from machine RAM), which explains its large RSS.

## Added 16 Oct 2026

### Memory-capped reruns (`run_capped.py`)
Java (`-Xmx256m -XX:+UseSerialGC`), .NET (`DOTNET_GCHeapHardLimit=256MB`, non-concurrent GC),
Node.js (`--max-old-space-size=256`) and Go (`GOMEMLIMIT=256MiB`) on the same six tests.
Output: `results/summary_capped.csv`, `results/overall_vs_c.csv` (geometric-mean ratios to C).

### Agent hot path: Python vs Python+Rust vs Rust (`hotpath/`)
RAG-style chunking of a JSONL corpus (parse, normalise, 200-word windows with step 150, CRC32 per chunk).

```bash
cd hotpath
python3 python/make_corpus.py 60000 data/corpus.jsonl      # ~260 MB, deterministic
(cd core && cargo build --release)                          # pure Rust binary + shared logic
(cd pyext && maturin build --release && pip install target/wheels/*.whl)   # PyO3 module
python3 bench_hotpath.py 5                                  # -> ../results/hotpath.csv
```

Variants: `pure` (Python, stdlib json + zlib), `per_doc` (Python loop, Rust per document),
`job` (one Rust call for the whole file), and the standalone Rust binary. All must print the same checksum.

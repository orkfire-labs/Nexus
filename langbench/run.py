#!/usr/bin/env python3
"""Cross-language benchmark harness.

For every (language, workload) pair it launches a fresh process, measures it with
GNU time, and records wall time, CPU time (user + sys) and peak RSS.
1 warm-up run is discarded (fills OS file cache, page cache, JIT on-disk caches),
then RUNS measured runs are kept. Each program prints a checksum; the harness
verifies all languages agree, so no implementation can "win" by doing less work.

Usage:  python3 run.py [--runs 5] [--only python,node] [--workloads fib,trees]
Output: results/raw.csv (one row per run) and results/summary.csv (medians)
"""
import argparse, csv, os, statistics, subprocess, sys, tempfile, time, platform

HERE = os.path.dirname(os.path.abspath(__file__))

LANGS = {
    "C":       ["bin/c"],
    "C++":     ["bin/cpp"],
    "Rust":    ["bin/rust"],
    "Go":      ["bin/go"],
    "Java":    ["java", "-cp", "bin/java", "Bench"],
    "C#":      ["dotnet", "bin/csharp/bench.dll"],
    "Python":  ["python3", "python/bench.py"],
    "Node.js": ["node", "node/bench.js"],
}

# name -> (argument, what it stresses)
WORKLOADS = {
    "noop":    ("0",         "Runtime start-up cost and baseline memory"),
    "factmod": ("50000000",  "n! mod 1e9+7, iterative: tight integer loop (pure CPU)"),
    "bigfact": ("100000",    "Exact 100000! with big integers: bigint library + heap growth"),
    "fib":     ("37",        "Naive recursive Fibonacci: function-call overhead"),
    "trees":   ("18",        "Allocate/free millions of binary-tree nodes: allocator & GC"),
    "sieve":   ("100000000", "Sieve of Eratosthenes over 100M flags: memory bandwidth & array layout"),
}


def measure(cmd, timeout):
    with tempfile.NamedTemporaryFile("r", suffix=".time") as tf:
        full = ["/usr/bin/time", "-f", "%e %U %S %M", "-o", tf.name] + cmd
        p = subprocess.run(full, cwd=HERE, capture_output=True, text=True, timeout=timeout,
                           env={**os.environ, "JAVA_TOOL_OPTIONS": "", "DOTNET_CLI_TELEMETRY_OPTOUT": "1"})
        if p.returncode != 0:
            raise RuntimeError(f"{cmd} failed: {p.stderr.strip()[:300]}")
        wall, user, sys_, rss_kb = tf.read().split()[-4:]
    return {"wall_s": float(wall), "cpu_s": float(user) + float(sys_),
            "user_s": float(user), "sys_s": float(sys_), "peak_rss_mb": int(rss_kb) / 1024,
            "checksum": p.stdout.strip()}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", type=int, default=5)
    ap.add_argument("--only", default="")
    ap.add_argument("--workloads", default="")
    ap.add_argument("--timeout", type=int, default=300)
    a = ap.parse_args()
    langs = [l for l in LANGS if not a.only or l in a.only.split(",")]
    wls = [w for w in WORKLOADS if not a.workloads or w in a.workloads.split(",")]

    os.makedirs(os.path.join(HERE, "results"), exist_ok=True)
    raw_rows, summary = [], []
    for w in wls:
        arg, desc = WORKLOADS[w]
        checks = {}
        for lang in langs:
            cmd = LANGS[lang] + [w, arg]
            measure(cmd, a.timeout)  # warm-up, discarded
            runs = []
            for i in range(a.runs):
                r = measure(cmd, a.timeout)
                runs.append(r)
                raw_rows.append({"workload": w, "language": lang, "run": i + 1, **r})
            checks[lang] = {r["checksum"] for r in runs}
            med = lambda k: statistics.median(r[k] for r in runs)
            row = {"workload": w, "language": lang,
                   "wall_s_median": round(med("wall_s"), 3),
                   "wall_s_min": min(r["wall_s"] for r in runs),
                   "wall_s_max": max(r["wall_s"] for r in runs),
                   "cpu_s_median": round(med("cpu_s"), 3),
                   "peak_rss_mb_median": round(med("peak_rss_mb"), 1),
                   "checksum": runs[0]["checksum"]}
            summary.append(row)
            print(f"{w:8} {lang:8} wall {row['wall_s_median']:7.3f}s  cpu {row['cpu_s_median']:7.3f}s  "
                  f"rss {row['peak_rss_mb_median']:8.1f} MB  -> {row['checksum']}", flush=True)
        distinct = set().union(*checks.values())
        if len(distinct) != 1:
            print(f"!! CHECKSUM MISMATCH for {w}: {checks}", file=sys.stderr)

    for name, rows in (("raw.csv", raw_rows), ("summary.csv", summary)):
        with open(os.path.join(HERE, "results", name), "w", newline="") as f:
            wr = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            wr.writeheader(); wr.writerows(rows)
    with open(os.path.join(HERE, "results", "env.txt"), "w") as f:
        f.write(f"date: {time.strftime('%Y-%m-%d %H:%M %Z')}\nhost: {platform.platform()}\n"
                f"cpus: {os.cpu_count()}\nruns: 1 warm-up + {a.runs} measured, fresh process each\n")
    print("wrote results/raw.csv and results/summary.csv")


if __name__ == "__main__":
    main()

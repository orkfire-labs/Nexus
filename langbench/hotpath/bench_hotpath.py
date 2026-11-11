#!/usr/bin/env python3
"""Measure the four hot-path variants: 1 warm-up + RUNS measured, fresh process each."""
import csv, os, statistics, subprocess, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
CORPUS = os.path.join(HERE, "data", "corpus.jsonl")
RUNS = int(sys.argv[1]) if len(sys.argv) > 1 else 5
VARIANTS = [
    ("pure_python", "Pure Python", ["python3", "python/chunk.py", "pure", CORPUS]),
    ("per_doc", "Python + Rust, one call per document", ["python3", "python/chunk.py", "per_doc", CORPUS]),
    ("job", "Python + Rust, one call for the whole job", ["python3", "python/chunk.py", "job", CORPUS]),
    ("pure_rust", "Pure Rust", ["core/target/release/chunk", CORPUS]),
]
def measure(cmd):
    with tempfile.NamedTemporaryFile("r") as tf:
        p = subprocess.run(["/usr/bin/time", "-f", "%e %U %S %M", "-o", tf.name] + cmd, cwd=HERE, capture_output=True, text=True, check=True)
        e, u, s, m = tf.read().split()[-4:]
    return float(e), float(u) + float(s), int(m) / 1024, p.stdout.strip()
rows = []
for key, label, cmd in VARIANTS:
    measure(cmd)
    rs = [measure(cmd) for _ in range(RUNS)]
    row = {"variant": key, "label": label,
           "cpu_s_median": round(statistics.median(r[1] for r in rs), 2),
           "cpu_s_min": min(r[1] for r in rs), "cpu_s_max": max(r[1] for r in rs),
           "wall_s_median": round(statistics.median(r[0] for r in rs), 2),
           "peak_rss_mb_median": round(statistics.median(r[2] for r in rs), 1),
           "checksum": rs[0][3]}
    rows.append(row); print(row, flush=True)
assert len({r["checksum"] for r in rows}) == 1, "checksum mismatch"
os.makedirs(os.path.join(HERE, "..", "results"), exist_ok=True)
with open(os.path.join(HERE, "..", "results", "hotpath.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
print("wrote results/hotpath.csv")

#!/usr/bin/env python3
"""Rerun the garbage-collected runtimes with container-style memory caps (256 MB heap).

Same workloads, same harness as run.py; only the runtime settings change.
"""
import csv, os, statistics, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import run

CAPPED = {
    "Java (capped)":    (["java", "-Xmx256m", "-XX:+UseSerialGC", "-cp", "bin/java", "Bench"], {}),
    "C# (capped)":      (["dotnet", "bin/csharp/bench.dll"], {"DOTNET_GCHeapHardLimit": "0x10000000", "DOTNET_gcConcurrent": "0"}),
    "Node.js (capped)": (["node", "--max-old-space-size=256", "node/bench.js"], {}),
    "Go (capped)":      (["bin/go"], {"GOMEMLIMIT": "256MiB"}),
}
RUNS = 5
rows = []
base = dict(os.environ)
for w, (arg, _) in run.WORKLOADS.items():
    for lang, (cmd, env) in CAPPED.items():
        os.environ.clear(); os.environ.update(base); os.environ.update(env)
        full = cmd + [w, arg]
        run.measure(full, 300)
        rs = [run.measure(full, 300) for _ in range(RUNS)]
        med = lambda k: statistics.median(r[k] for r in rs)
        row = {"workload": w, "language": lang, "wall_s_median": round(med("wall_s"), 3),
               "cpu_s_median": round(med("cpu_s"), 3), "peak_rss_mb_median": round(med("peak_rss_mb"), 1),
               "checksum": rs[0]["checksum"]}
        rows.append(row); print(row, flush=True)
os.environ.clear(); os.environ.update(base)
with open("results/summary_capped.csv", "w", newline="") as f:
    wr = csv.DictWriter(f, fieldnames=list(rows[0])); wr.writeheader(); wr.writerows(rows)
print("wrote results/summary_capped.csv")

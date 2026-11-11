#!/usr/bin/env bash
# Builds every implementation with release/optimised settings.
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p bin

echo "[c]      gcc -O2"
gcc -O2 -o bin/c c/bench.c -lgmp

echo "[cpp]    g++ -O2 -std=c++20"
g++ -O2 -std=c++20 -o bin/cpp cpp/bench.cpp -lgmpxx -lgmp

echo "[rust]   cargo build --release"
(cd rust && cargo build --release -q) && cp rust/target/release/bench bin/rust

echo "[go]     go build"
(cd go && go build -o ../bin/go .)

echo "[java]   javac"
mkdir -p bin/java && javac -d bin/java java/Bench.java 2>&1 | grep -v JAVA_TOOL_OPTIONS || true

echo "[csharp] dotnet build -c Release"
(cd csharp && dotnet build -c Release -o ../bin/csharp --nologo -v q) >/dev/null

echo "done"

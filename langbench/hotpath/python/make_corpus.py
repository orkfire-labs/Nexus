"""Deterministic synthetic corpus: N JSON documents of 150-900 ASCII words."""
import json
import random
import sys

n = int(sys.argv[1]); out = sys.argv[2]
rng = random.Random(42)
vocab = ["".join(rng.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(rng.randint(2, 11))) for _ in range(20000)]
punct = ["", "", "", "", "", ".", ",", ";", ":", "!", "?"]
with open(out, "w") as f:
    for i in range(n):
        words = []
        for _ in range(rng.randint(150, 900)):
            w = rng.choice(vocab)
            if rng.random() < 0.1:
                w = w.capitalize()
            words.append(w + rng.choice(punct))
        f.write(json.dumps({"id": i, "title": " ".join(words[:6]), "source": "kb", "body": " ".join(words)}) + "\n")

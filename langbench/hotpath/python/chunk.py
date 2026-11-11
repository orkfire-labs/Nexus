"""RAG-style chunking of a JSONL corpus, three ways.

  python3 chunk.py pure    corpus.jsonl   # all Python (json and zlib are C-backed, as in real code)
  python3 chunk.py per_doc corpus.jsonl   # Python loop, Rust (PyO3) per document
  python3 chunk.py job     corpus.jsonl   # one call: Rust does the whole file
"""
import json
import sys
import zlib

PUNCT = ".,;:!?\"'()"
CHUNK, STEP = 200, 150
MASK = (1 << 64) - 1


def process_doc(line):
    body = json.loads(line)["body"].lower()
    words = [w for w in (t.strip(PUNCT) for t in body.split()) if w]
    n = s = 0
    for start in range(0, len(words), STEP):
        chunk = words[start:start + CHUNK]
        s = (s + zlib.crc32(" ".join(chunk).encode()) + len(chunk)) & MASK
        n += 1
    return n, s


def main():
    mode, path = sys.argv[1], sys.argv[2]
    if mode == "job":
        import chunker_rs
        n, s = chunker_rs.process_file(path)
    else:
        fn = process_doc
        if mode == "per_doc":
            import chunker_rs
            fn = chunker_rs.process_doc
        n = s = 0
        with open(path, encoding="utf-8") as f:
            for line in f:
                a, b = fn(line)
                n += a
                s = (s + b) & MASK
    print(n, s)


if __name__ == "__main__":
    main()

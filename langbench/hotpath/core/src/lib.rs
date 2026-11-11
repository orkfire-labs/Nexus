//! RAG-style chunking of one JSON document: parse, normalise, split into
//! overlapping 200-word windows (step 150), CRC32 each chunk.
use serde::Deserialize;

const PUNCT: &[char] = &['.', ',', ';', ':', '!', '?', '"', '\'', '(', ')'];
pub const CHUNK: usize = 200;
pub const STEP: usize = 150;

#[derive(Deserialize)]
struct Doc {
    body: String,
}

/// Returns (chunks, checksum) for one JSON line.
pub fn process_doc(line: &str) -> (u64, u64) {
    let doc: Doc = serde_json::from_str(line).expect("bad json");
    let lower = doc.body.to_ascii_lowercase();
    let words: Vec<&str> = lower
        .split_whitespace()
        .map(|w| w.trim_matches(PUNCT))
        .filter(|w| !w.is_empty())
        .collect();
    let (mut n, mut sum) = (0u64, 0u64);
    let mut start = 0;
    while start < words.len() {
        let end = (start + CHUNK).min(words.len());
        let text = words[start..end].join(" ");
        sum = sum
            .wrapping_add(crc32fast::hash(text.as_bytes()) as u64)
            .wrapping_add((end - start) as u64);
        n += 1;
        start += STEP;
    }
    (n, sum)
}

/// Streams a JSONL file and processes every line.
pub fn process_file(path: &str) -> (u64, u64) {
    use std::io::{BufRead, BufReader};
    let f = std::fs::File::open(path).expect("open");
    let (mut n, mut sum) = (0u64, 0u64);
    for line in BufReader::new(f).lines() {
        let (a, b) = process_doc(&line.expect("read"));
        n += a;
        sum = sum.wrapping_add(b);
    }
    (n, sum)
}

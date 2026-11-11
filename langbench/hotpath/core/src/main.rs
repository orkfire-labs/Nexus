fn main() {
    let path = std::env::args().nth(1).expect("path");
    let (n, sum) = chunker::process_file(&path);
    println!("{} {}", n, sum);
}

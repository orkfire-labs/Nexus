use pyo3::prelude::*;

/// One document per call: Python keeps the loop, Rust does each document.
#[pyfunction]
fn process_doc(line: &str) -> (u64, u64) {
    chunker::process_doc(line)
}

/// The whole job in one call: Python hands over the file, Rust does the loop.
#[pyfunction]
fn process_file(py: Python<'_>, path: &str) -> (u64, u64) {
    let p = path.to_owned();
    py.allow_threads(move || chunker::process_file(&p))
}

#[pymodule]
fn chunker_rs(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(process_doc, m)?)?;
    m.add_function(wrap_pyfunction!(process_file, m)?)?;
    Ok(())
}

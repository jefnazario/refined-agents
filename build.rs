use std::env;
use std::fs;
use std::io;
use std::path::{Path, PathBuf};

fn collect_markdown_files(path: &Path, files: &mut Vec<PathBuf>) -> io::Result<()> {
    if !path.exists() {
        return Ok(());
    }

    for entry in fs::read_dir(path)? {
        let entry = entry?;
        let path = entry.path();
        if path.is_dir() {
            collect_markdown_files(&path, files)?;
        } else if path.extension().and_then(|ext| ext.to_str()) == Some("md") {
            files.push(path);
        }
    }

    Ok(())
}

fn main() -> io::Result<()> {
    println!("cargo:rerun-if-changed=refined_agents/prompts");

    let out_dir = PathBuf::from(env::var("OUT_DIR").expect("OUT_DIR is set by Cargo"));
    let catalog_path = out_dir.join("prompt_catalog.rs");
    let prompts_root = PathBuf::from("refined_agents/prompts");
    let mut files = Vec::new();
    collect_markdown_files(&prompts_root, &mut files)?;
    files.sort();

    let mut output = String::from("static EMBEDDED_PROMPTS: &[(&str, &str)] = &[\n");
    for file in files {
        let rel_path = file
            .strip_prefix(&prompts_root)
            .expect("file lives under prompts root")
            .to_string_lossy()
            .replace('\\', "/");
        let content = fs::read_to_string(&file)?;
        output.push_str(&format!("    ({rel_path:?}, {content:?}),\n"));
    }
    output.push_str("];\n");

    fs::write(catalog_path, output)
}

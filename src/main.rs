use std::collections::HashSet;
use std::env;
use std::error::Error;
use std::fs;
use std::path::{Path, PathBuf};

const PROJECT_CONTEXT_FILE: &str = "000_project_context.md";

include!(concat!(env!("OUT_DIR"), "/prompt_catalog.rs"));

#[derive(Debug, Clone)]
struct TaskPreset {
    name: &'static str,
    mode: Option<&'static str>,
    tags: &'static [&'static str],
    exclude_tags: &'static [&'static str],
    description: &'static str,
}

#[derive(Debug, Clone)]
struct AgentProfile {
    name: &'static str,
    tag: &'static str,
    display_name: &'static str,
}

#[derive(Debug)]
struct PromptChunk {
    path: PathBuf,
    priority: i32,
    tags: HashSet<String>,
    content: String,
}

#[derive(Debug)]
struct Args {
    agent: String,
    language: String,
    task: String,
    objective: String,
    framework: Option<String>,
    extra_context: Option<String>,
    output: Option<PathBuf>,
    output_format: String,
    cursor_rule_type: String,
    cursor_globs: Option<String>,
    cursor_description: Option<String>,
    prompts_root: PathBuf,
}

fn task_preset(name: &str) -> Option<TaskPreset> {
    match name {
        "api" => Some(TaskPreset {
            name: "api",
            mode: Some("api"),
            tags: &["api", "backend"],
            exclude_tags: &["data_pipeline", "refactor", "bugfix", "test"],
            description: "Design and implement an API service or endpoint.",
        }),
        "backend" => Some(TaskPreset {
            name: "backend",
            mode: Some("backend"),
            tags: &["backend"],
            exclude_tags: &["data_pipeline", "refactor", "bugfix", "test"],
            description: "Implement backend/service layer logic.",
        }),
        "data_pipeline" => Some(TaskPreset {
            name: "data_pipeline",
            mode: Some("data_pipeline"),
            tags: &["data_pipeline"],
            exclude_tags: &["api", "backend", "refactor", "bugfix", "test"],
            description: "Build or update a deterministic data pipeline.",
        }),
        "bugfix" => Some(TaskPreset {
            name: "bugfix",
            mode: Some("bugfix"),
            tags: &["bugfix"],
            exclude_tags: &["api", "backend", "data_pipeline", "refactor", "test"],
            description: "Fix an existing bug with minimal, safe changes.",
        }),
        "refactor" => Some(TaskPreset {
            name: "refactor",
            mode: Some("refactor"),
            tags: &["refactor"],
            exclude_tags: &["api", "backend", "data_pipeline", "bugfix", "test"],
            description: "Refactor code without changing behavior.",
        }),
        "test_generation" => Some(TaskPreset {
            name: "test_generation",
            mode: Some("test_generation"),
            tags: &["test"],
            exclude_tags: &["api", "backend", "data_pipeline", "refactor", "bugfix"],
            description: "Generate or extend tests for behavior coverage.",
        }),
        _ => None,
    }
}

fn normalize_agent(agent: &str) -> Option<AgentProfile> {
    match agent.trim().to_ascii_lowercase().as_str() {
        "codex" | "openai-codex" | "openai codex" => Some(AgentProfile {
            name: "codex",
            tag: "codex",
            display_name: "Codex",
        }),
        "claude-code" | "claude_code" | "claude" | "anthropic-claude-code" => Some(AgentProfile {
            name: "claude-code",
            tag: "claude_code",
            display_name: "Claude Code",
        }),
        "cursor" | "cursor-agent" | "cursor agent" => Some(AgentProfile {
            name: "cursor",
            tag: "cursor",
            display_name: "Cursor",
        }),
        _ => None,
    }
}

fn usage() -> &'static str {
    "Usage: refined-agents-rs --agent <codex|claude-code|cursor> --language <python|rust|csharp|vue|vuejs> --task <task> --objective <text> [options]

Options:
  --framework <text>
  --extra-context <text>
  --output <path>
  --format <prompt|cursor-rule|agents-md>
  --cursor-rule-type <always|intelligent|files|manual>
  --cursor-globs <globs>
  --cursor-description <text>
  --prompts-root <path>
"
}

fn parse_args() -> Result<Args, String> {
    let mut agent = env::var("REFINED_AGENTS_AGENT").unwrap_or_else(|_| "codex".to_string());
    let mut language = env::var("REFINED_AGENTS_LANGUAGE").unwrap_or_else(|_| "python".to_string());
    let mut task = env::var("REFINED_AGENTS_TASK").unwrap_or_else(|_| "api".to_string());
    let mut objective: Option<String> = None;
    let mut framework = None;
    let mut extra_context = None;
    let mut output = None;
    let mut output_format = "prompt".to_string();
    let mut cursor_rule_type = "always".to_string();
    let mut cursor_globs = None;
    let mut cursor_description = None;
    let mut prompts_root = env::var("REFINED_AGENTS_PROMPTS_ROOT")
        .map(PathBuf::from)
        .unwrap_or_else(|_| PathBuf::from("refined_agents/prompts"));

    let mut iter = env::args().skip(1);
    while let Some(flag) = iter.next() {
        let value = match flag.as_str() {
            "--help" | "-h" => return Err(usage().to_string()),
            "--agent"
            | "--language"
            | "--task"
            | "--objective"
            | "--framework"
            | "--extra-context"
            | "--output"
            | "--format"
            | "--cursor-rule-type"
            | "--cursor-globs"
            | "--cursor-description"
            | "--prompts-root" => iter
                .next()
                .ok_or_else(|| format!("Missing value for {flag}"))?,
            _ => return Err(format!("Unknown argument: {flag}\n\n{}", usage())),
        };

        match flag.as_str() {
            "--agent" => agent = value,
            "--language" => language = value,
            "--task" => task = value,
            "--objective" => objective = Some(value),
            "--framework" => framework = Some(value),
            "--extra-context" => extra_context = Some(value),
            "--output" => output = Some(PathBuf::from(value)),
            "--format" => output_format = value,
            "--cursor-rule-type" => cursor_rule_type = value,
            "--cursor-globs" => cursor_globs = Some(value),
            "--cursor-description" => cursor_description = Some(value),
            "--prompts-root" => prompts_root = PathBuf::from(value),
            _ => unreachable!(),
        }
    }

    let objective =
        objective.ok_or_else(|| "Missing required argument: --objective".to_string())?;
    if !matches!(language.as_str(), "python" | "rust" | "csharp" | "vue" | "vuejs") {
        return Err("Unknown language. Expected one of: python, rust, csharp, vue, vuejs".to_string());
    }
    if task_preset(&task).is_none() {
        return Err(
            "Unknown task. Expected one of: api, backend, bugfix, data_pipeline, refactor, test_generation"
                .to_string(),
        );
    }
    if normalize_agent(&agent).is_none() {
        return Err("Unknown agent. Expected one of: codex, claude-code, cursor".to_string());
    }
    if !matches!(
        output_format.as_str(),
        "prompt" | "cursor-rule" | "agents-md"
    ) {
        return Err("Unknown format. Expected one of: prompt, cursor-rule, agents-md".to_string());
    }
    if !matches!(
        cursor_rule_type.as_str(),
        "always" | "intelligent" | "files" | "manual"
    ) {
        return Err(
            "Unknown Cursor rule type. Expected one of: always, intelligent, files, manual"
                .to_string(),
        );
    }

    Ok(Args {
        agent,
        language,
        task,
        objective,
        framework,
        extra_context,
        output,
        output_format,
        cursor_rule_type,
        cursor_globs,
        cursor_description,
        prompts_root,
    })
}

fn parse_front_matter(text: &str, path: &Path) -> (i32, HashSet<String>, String) {
    let mut priority = filename_priority(path);
    let mut tags = HashSet::new();

    let trimmed_start = text.trim_start();
    if !trimmed_start.starts_with("---") {
        return (priority, tags, text.trim().to_string());
    }

    let front_matter_start = match trimmed_start.strip_prefix("---") {
        Some(rest) => rest.trim_start_matches(['\r', '\n']),
        None => return (priority, tags, text.trim().to_string()),
    };

    let Some((front_matter, body)) = front_matter_start.split_once("\n---") else {
        return (priority, tags, text.trim().to_string());
    };

    for line in front_matter.lines() {
        let trimmed = line.trim();
        if let Some(raw) = trimmed.strip_prefix("priority:") {
            if let Ok(parsed) = raw.trim().parse::<i32>() {
                priority = parsed;
            }
        } else if let Some(raw) = trimmed.strip_prefix("tags:") {
            let raw = raw.trim().trim_start_matches('[').trim_end_matches(']');
            for tag in raw.split(',') {
                let tag = tag.trim();
                if !tag.is_empty() {
                    tags.insert(tag.to_string());
                }
            }
        }
    }

    let body = body.trim_start_matches(['\r', '\n']).trim();
    (priority, tags, body.to_string())
}

fn filename_priority(path: &Path) -> i32 {
    path.file_stem()
        .and_then(|stem| stem.to_str())
        .and_then(|stem| stem.split_once('_').map(|(prefix, _)| prefix))
        .and_then(|prefix| prefix.parse::<i32>().ok())
        .unwrap_or(1000)
}

fn collect_markdown_files(path: &Path, files: &mut Vec<PathBuf>) -> Result<(), Box<dyn Error>> {
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

fn load_chunks(root: &Path) -> Result<Vec<PromptChunk>, Box<dyn Error>> {
    if !root.join("system").exists() {
        return load_embedded_chunks();
    }

    let mut paths = Vec::new();
    collect_markdown_files(&root.join("system"), &mut paths)?;
    paths.sort();

    let mut chunks = Vec::new();
    for path in paths {
        let text = fs::read_to_string(&path)?;
        let (priority, tags, content) = parse_front_matter(&text, &path);
        let rel_path = path.strip_prefix(root).unwrap_or(&path).to_path_buf();
        chunks.push(PromptChunk {
            path: rel_path,
            priority,
            tags,
            content,
        });
    }

    chunks.sort_by(|a, b| {
        a.priority
            .cmp(&b.priority)
            .then_with(|| a.path.file_name().cmp(&b.path.file_name()))
    });
    Ok(chunks)
}

fn load_embedded_chunks() -> Result<Vec<PromptChunk>, Box<dyn Error>> {
    let mut chunks = Vec::new();
    for (rel_path, content) in EMBEDDED_PROMPTS {
        let path = PathBuf::from(rel_path);
        let (priority, tags, body) = parse_front_matter(content, &path);
        chunks.push(PromptChunk {
            path,
            priority,
            tags,
            content: body,
        });
    }

    chunks.sort_by(|a, b| {
        a.priority
            .cmp(&b.priority)
            .then_with(|| a.path.file_name().cmp(&b.path.file_name()))
    });
    Ok(chunks)
}

fn mode_from_path(path: &Path) -> Option<String> {
    let mut saw_modes = false;
    for component in path.components() {
        let part = component.as_os_str().to_string_lossy();
        if saw_modes {
            return Some(part.to_string());
        }
        if part == "modes" {
            saw_modes = true;
        }
    }
    None
}

fn chunk_matches_tags(
    tags: &HashSet<String>,
    include: &HashSet<String>,
    exclude: &HashSet<String>,
) -> bool {
    if tags.is_empty() {
        return true;
    }
    if tags.iter().any(|tag| exclude.contains(tag)) {
        return false;
    }

    let exclusive_groups: [&[&str]; 2] = [&["python", "rust", "csharp", "vue", "vuejs"], &["codex", "claude_code", "cursor"]];
    for exclusive_group in exclusive_groups {
        let chunk_has_group_tag = exclusive_group.iter().any(|tag| tags.contains(*tag));
        let include_has_group_tag = exclusive_group.iter().any(|tag| include.contains(*tag));
        if chunk_has_group_tag && !include_has_group_tag {
            return false;
        }
        if chunk_has_group_tag
            && !exclusive_group
                .iter()
                .any(|tag| tags.contains(*tag) && include.contains(*tag))
        {
            return false;
        }
    }

    include.is_empty() || tags.iter().any(|tag| include.contains(tag))
}

fn build_system_prompt(
    root: &Path,
    include: &HashSet<String>,
    exclude: &HashSet<String>,
    mode: Option<&str>,
) -> Result<String, Box<dyn Error>> {
    let chunks = load_chunks(root)?;
    let mut selected = Vec::new();

    for chunk in chunks {
        if chunk.path.file_name().and_then(|name| name.to_str()) == Some(PROJECT_CONTEXT_FILE) {
            continue;
        }

        let chunk_mode = mode_from_path(&chunk.path);
        if mode.is_none() && chunk_mode.is_some() {
            continue;
        }
        if let (Some(expected), Some(actual)) = (mode, chunk_mode.as_deref()) {
            if expected != actual {
                continue;
            }
        }

        if !chunk_matches_tags(&chunk.tags, include, exclude) {
            continue;
        }

        let rel_path = chunk.path.to_string_lossy().replace('\\', "/");
        selected.push(format!("<!-- {rel_path} -->\n{}", chunk.content));
    }

    Ok(selected.join("\n\n").trim().to_string())
}

fn build_execution_brief(args: &Args, agent: &AgentProfile) -> String {
    let mut lines = vec![
        "# Execution Brief".to_string(),
        format!("- Target coding agent: {}", agent.display_name),
        format!("- Primary language: {}", args.language),
        format!("- Task type: {}", args.task),
    ];

    if let Some(framework) = &args.framework {
        lines.push(format!("- Framework/stack: {framework}"));
    }

    lines.extend([
        String::new(),
        "## Objective".to_string(),
        args.objective.trim().to_string(),
        String::new(),
    ]);

    if let Some(extra_context) = &args.extra_context {
        lines.extend([
            "## Extra Context".to_string(),
            extra_context.trim().to_string(),
            String::new(),
        ]);
    }

    lines.extend([
        "## Output Requirements".to_string(),
        "- Produce production-ready code and tests when applicable.".to_string(),
        "- Keep changes minimal and aligned with existing architecture.".to_string(),
        "- Explain important tradeoffs and assumptions briefly.".to_string(),
    ]);

    lines.join("\n")
}

fn build_agent_prompt(args: &Args) -> Result<String, Box<dyn Error>> {
    let agent = normalize_agent(&args.agent).ok_or("unknown agent")?;
    let preset = task_preset(&args.task).ok_or("unknown task")?;

    let mut include = HashSet::from([
        "always".to_string(),
        agent.tag.to_string(),
        args.language.clone(),
    ]);
    include.extend(preset.tags.iter().map(|tag| tag.to_string()));
    let exclude = preset
        .exclude_tags
        .iter()
        .map(|tag| tag.to_string())
        .collect::<HashSet<_>>();

    let system_prompt = build_system_prompt(&args.prompts_root, &include, &exclude, preset.mode)?;
    let brief = build_execution_brief(args, &agent);

    Ok(format!(
        "# Prompt For Coding Agent\n\nThis prompt is tailored for {}.\nTask preset: {} ({})\n\n\n{}\n\n{}",
        agent.display_name, preset.name, preset.description, system_prompt, brief
    )
    .trim()
    .to_string()
        + "\n")
}

fn build_cursor_rule(args: &Args, prompt: &str) -> String {
    let mut lines = vec!["---".to_string()];
    if let Some(description) = &args.cursor_description {
        lines.push(format!(
            "description: \"{}\"",
            description.replace('"', "\\\"")
        ));
    }
    if args.cursor_rule_type == "files" {
        if let Some(globs) = &args.cursor_globs {
            lines.push(format!("globs: {globs}"));
        }
    }
    lines.push(format!(
        "alwaysApply: {}",
        if args.cursor_rule_type == "always" {
            "true"
        } else {
            "false"
        }
    ));
    lines.push("---".to_string());
    format!("{}\n\n{}\n", lines.join("\n"), prompt.trim())
}

fn render_output(args: &Args) -> Result<String, Box<dyn Error>> {
    let prompt = build_agent_prompt(args)?;
    match args.output_format.as_str() {
        "prompt" => Ok(prompt),
        "agents-md" => Ok(format!("# Project Agent Instructions\n\n{}", prompt.trim())),
        "cursor-rule" => {
            let agent = normalize_agent(&args.agent).ok_or("unknown agent")?;
            if agent.name != "cursor" {
                return Err("--format cursor-rule requires --agent cursor".into());
            }
            Ok(build_cursor_rule(args, &prompt))
        }
        _ => Err("unsupported output format".into()),
    }
}

fn main() {
    let args = match parse_args() {
        Ok(args) => args,
        Err(message) => {
            eprintln!("{message}");
            std::process::exit(2);
        }
    };

    let output = match render_output(&args) {
        Ok(output) => output,
        Err(err) => {
            eprintln!("error: {err}");
            std::process::exit(1);
        }
    };

    if let Some(path) = &args.output {
        if let Some(parent) = path.parent() {
            if let Err(err) = fs::create_dir_all(parent) {
                eprintln!("error: failed to create output directory: {err}");
                std::process::exit(1);
            }
        }
        if let Err(err) = fs::write(path, output) {
            eprintln!("error: failed to write output file: {err}");
            std::process::exit(1);
        }
        println!("Prompt written to {}", path.display());
    } else {
        print!("{output}");
    }
}

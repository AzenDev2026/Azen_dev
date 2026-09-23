// main.rs
use serde::{Deserialize, Serialize};
use std::env;
use std::fs;
use std::path::PathBuf;

#[derive(Debug, Serialize, Deserialize, Clone)]
struct Todo {
    id: u32,
    content: String,
    completed: bool,
    created_at: String,
}

impl Todo {
    fn new(id: u32, content: String) -> Self {
        use chrono::Local;
        let now = Local::now().format("%Y-%m-%d %H:%M:%S").to_string();
        Todo {
            id,
            content,
            completed: false,
            created_at: now,
        }
    }
}

// ... 加载、保存、增删改查等函数
fn main() {
    let args: Vec<String> = env::args().collect();
    // 解析 args，分发到不同的操作函数
}
# 2026-09-16 code-lab-evening（21:00 档，3 cycles 全 keep）

commits: b7217db (a2a-minimal) + 6779750 (wget-rust) + 89fd0a9 (agent-log)，tsv 行 20260916_2200+08。

## C1 a2a-minimal 32→48（11d stale）
- do_POST 的 `int(Content-Length)` 无守卫：header 传 `abc` → ValueError 裸抛断连（09-05 畸形 JSON 家族走 header 路径的兄弟）；负数 → `read(-1)` 阻塞悬挂。守卫后回 -32600。
- 终态语义：cancel 盲改状态（已完成任务被"成功取消"=假成功）；message/send 复活已取消任务。修：终态拒 cancel；cancelled 拒 send（completed 仍可多轮，pin 住）。
- 测试技巧：raw socket 助手绕过 http.client 自动补头才能注入垃圾 header；test_cancel_task 重写为 store 直接 seed working 任务（同步 executor 下 HTTP 任务发出即完成，外部永远观察不到 working 窗口）。

## C2 wget-rust 25→25（hygiene，11d stale）
- **red-verified 仓库状态 bug**：`git ls-tree HEAD` 证明 4 个历史 cycle 只提交过 src/lib.rs + tests/e2e.rs，Cargo.toml 和 src/main.rs 只存在于 worktree → 新 clone 根本 build 不起来。补交全部 build 文件 + .gitignore(target)。
- 教训：**查项目完整性用 git ls-tree，别只看 worktree 存在**。

## C3 agent-log 69→75（8d stale）
- stats --json latest_note 未过 esc_json（hot 都转义了）→ 引号文件名打穿 JSON。
- **esc_json 潜伏 bug**：反斜杠翻倍从来就是 no-op！`${s//\\\\/...}` 双引号内是 bash 解析坑，必须单引号变量中转。hot --json 同根因。
- stats 计数递归 vs latest 顶层 glob 两套文件集 → 子目录最新笔记永远当不了 latest。
- **META 教训（家族第 2 例）**：edit 工具改反斜杠密集块时吃掉闭合引号 → 语法错误全 suite 崩。Python 字节级重放修复（09-08 规则）。反斜杠转义类编辑直接用 Python，勿用 edit。

## 流程注记
- 基线扫描选 stalest：a2a-minimal / wget-rust 并列 11d，agent-log 8d 次之。
- git status 里 ai-iot-orchestrator / catalyst-agent-mesh / edge-agent-micro 等 submodule 变动非本会话产物，未触碰未提交。

# 🦀 mini-wget

Rust 实现的 wget 原型，展示 async HTTP 下载的核心模式：流式传输、断点续传、重试退避和进度条。

## 功能

- **HTTP/HTTPS 下载** — 基于 reqwest + rustls（纯 Rust TLS，不依赖 OpenSSL）
- **断点续传** — `--resume` 通过 `Range` header 续传已下载部分
- **自动重试** — 指数退避，可配置重试次数
- **进度条** — indicatif 驱动，显示速度/百分比/ETA
- **预 DNS 解析** — 下载前探测网络可达性

## 快速开始

```bash
# 构建
cargo build --release

# 基本下载
cargo run -- https://example.com/file.tar.gz

# 指定输出文件
cargo run -- https://example.com/file.tar.gz -o /tmp/file.tar.gz

# 断点续传（中断后重新运行同一命令）
cargo run -- https://example.com/file.tar.gz --resume

# 调整超时和重试
cargo run -- https://example.com/file.tar.gz --timeout 60 --retries 5
```

## 命令行参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `url` | （必需） | HTTP/HTTPS 下载地址 |
| `-o, --output` | URL 文件名 | 保存路径 |
| `--resume` | false | 启用断点续传 |
| `--timeout` | 30 | 单次请求超时（秒） |
| `--retries` | 3 | 失败重试次数 |

## 架构

```
src/
├── main.rs          # 入口：解析参数 → DNS 预检 → 启动下载
└── lib.rs           # 模块化核心逻辑
    ├── cli          # clap 参数定义
    ├── url_parser   # URL 解析 + 默认文件名提取
    ├── dns_resolver # 异步 DNS 解析
    ├── ssl          # rustls TLS 配置
    ├── http_client  # reqwest 封装（连接池复用）
    ├── progress     # indicatif 进度条
    └── downloader   # 下载引擎（流式写入 + 断点 + 重试）
```

### 关键设计决策

- **流式处理**：`bytes_stream()` 逐块写入磁盘，不把整个文件加载到内存
- **Range 协商**：发送 `Range: bytes=N-` 请求剩余部分；若服务器忽略 Range（返回 200 而非 206），删除旧文件从头下载，避免数据损坏
- **模块分离**：lib.rs 把逻辑拆为独立模块（URL 解析、DNS、HTTP、进度），便于单独测试和复用

## 依赖

| crate | 用途 |
|-------|------|
| reqwest | HTTP 客户端（rustls TLS + stream） |
| tokio | 异步运行时 + 文件 IO |
| clap | 命令行参数解析 |
| indicatif | 进度条 |
| anyhow | 错误处理 |
| url | URL 解析 |

## 测试

```bash
cargo test
```

## 扩展方向

- 多线程分段下载（`Range: bytes=A-B` 并发）
- 递归下载 / 镜像模式
- 代理支持（HTTP/SOCKS5）
- SHA256 校验和验证
- 配置文件（`~/.mini-wget.toml`）

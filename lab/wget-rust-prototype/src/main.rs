use std::time::Duration;

use anyhow::{Context, Result};
use clap::Parser;
use wget_rust::{Cli, DownloadConfig, Downloader, ParsedUrl, output_path};

#[tokio::main]
async fn main() -> Result<()> {
    let cli = Cli::parse();
    let parsed_url = ParsedUrl::parse(&cli.url)?;

    // 提前做一次 DNS 解析，让网络问题尽早暴露；实际连接仍由 reqwest 管理连接池。
    let _endpoint =
        wget_rust::dns_resolver::resolve(parsed_url.host()?, parsed_url.port_or_default()?)
            .await
            .context("下载前 DNS 解析失败")?;

    let timeout = Duration::from_secs(cli.timeout);
    let config = DownloadConfig {
        output_file: output_path(&parsed_url, cli.output_file),
        url: parsed_url,
        resume: cli.resume,
        timeout,
        retries: cli.retries,
    };

    let downloader = Downloader::new(config.timeout)?;
    downloader.download(&config).await
}

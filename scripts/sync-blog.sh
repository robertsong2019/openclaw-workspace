#!/bin/bash
# 同步本地草稿到博客（智能匹配已有文件名）

DRAFTS_DIR="$HOME/.openclaw/workspace/memory/daily-posts"
BLOG_DIR="$HOME/.openclaw/workspace/robertsong2019.github.io"
SCRIPT="$HOME/.openclaw/workspace/scripts/md-to-html.py"
ESSAYS_FILE="$BLOG_DIR/essays.html"

cd "$BLOG_DIR" || exit 1

echo "🔍 检查草稿更新..."

updated=0
changes=""

for md_file in "$DRAFTS_DIR"/*.md; do
    [ -f "$md_file" ] || continue
    
    # 提取日期
    basename=$(basename "$md_file" .md)
    date_prefix="${basename:0:10}"
    
    # 在 essays.html 中查找对应日期的 URL
    existing_url=$(grep -A 5 "date: '$date_prefix'" "$ESSAYS_FILE" | grep "url:" | head -1 | sed "s/.*url: '\(.*\)'.*/\1/")
    
    if [ -n "$existing_url" ]; then
        # 使用已有的文件名
        html_file="$BLOG_DIR/$existing_url"
        html_name=$(basename "$existing_url")
        echo "📄 $basename → 已有: $html_name"
    else
        # 新文章，使用默认命名
        title_slug="${basename:11}"
        html_file="$BLOG_DIR/posts/${title_slug}.html"
        html_name="${title_slug}.html"
        echo "📄 $basename → 新文章: $html_name"
    fi
    
    # 如果 HTML 不存在或草稿更新
    if [ ! -f "$html_file" ] || [ "$md_file" -nt "$html_file" ]; then
        echo "   🔄 需要更新"
        
        if [ -n "$existing_url" ]; then
            # 使用已有文件名
            python3 "$SCRIPT" "$md_file" "$BLOG_DIR/posts/" --output "$html_name"
        else
            # 新文章
            python3 "$SCRIPT" "$md_file" "$BLOG_DIR/posts/"
        fi
        
        changes="$changes $html_name"
        updated=1
    else
        echo "   ✅ 已是最新"
    fi
done

if [ $updated -eq 1 ]; then
    echo ""
    echo "📝 更新的文章:$changes"
    echo ""
    git add posts/*.html
    git status --short
    echo ""
    echo "运行以下命令完成推送："
    echo "  cd $BLOG_DIR && git commit -m 'docs: sync blog posts' && git push"
else
    echo ""
    echo "✅ 所有文章已是最新"
fi

#!/bin/bash
cd "$(dirname "$0")"
node --test tests/embed-sync.test.js tests/embedding.test.js tests/embed-openai.test.js tests/embedCacheEviction.test.js 2>&1

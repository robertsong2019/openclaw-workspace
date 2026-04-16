const fs = require('fs');
const path = require('path');

async function writeOutput(filePath, content, target) {
  const dir = path.dirname(filePath);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
  fs.writeFileSync(filePath, content, 'utf8');
}

module.exports = { writeOutput };

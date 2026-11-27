import { readdirSync, readFileSync } from 'node:fs';
import { join, relative } from 'node:path';
import { fileURLToPath } from 'node:url';
import { isMap, parseDocument } from 'yaml';

const root = fileURLToPath(new URL('../', import.meta.url));
const frontmatter = /^---\r?\n([\s\S]*?)(?<=\n)---(?=\r?\n|$)/;

function* skillFiles(directory) {
  for (const entry of readdirSync(directory, { withFileTypes: true })) {
    const path = join(directory, entry.name);
    if (entry.isDirectory() && entry.name !== 'node_modules') {
      yield* skillFiles(path);
    } else if (entry.isFile() && entry.name === 'SKILL.md') {
      yield path;
    }
  }
}

function check(path) {
  const match = frontmatter.exec(readFileSync(path, 'utf8'));
  if (!match) return 'missing frontmatter block';

  const doc = parseDocument(match[1], { strict: true, uniqueKeys: true });
  if (doc.errors.length) return doc.errors[0].message.split('\n', 1)[0];
  if (!isMap(doc.contents)) return 'frontmatter must be a mapping';

  for (const key of ['name', 'description']) {
    const value = doc.get(key);
    if (typeof value !== 'string' || !value.trim()) {
      return `\`${key}\` must be a nonempty string`;
    }
  }
}

let checked = 0;
let failures = 0;
for (const directory of ['skills', 'in-progress']) {
  for (const path of skillFiles(join(root, directory))) {
    checked++;
    const problem = check(path);
    if (problem) {
      failures++;
      console.error(`${relative(root, path)}: ${problem}`);
    }
  }
}

if (failures) {
  console.error(`${failures} of ${checked} skill frontmatter blocks failed validation.`);
  process.exitCode = 1;
} else {
  console.log(`Validated ${checked} skill frontmatter blocks.`);
}

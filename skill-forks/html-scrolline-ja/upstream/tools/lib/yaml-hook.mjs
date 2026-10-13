/** Node module hook: `import x from './deck.yaml'` → parsed default export, like tools/vite/deck-plugin.js. */
import { readFile } from 'node:fs/promises';
import YAML from 'yaml';

export async function load(url, context, next) {
  if (url.startsWith('file:') && /\.ya?ml$/.test(new URL(url).pathname)) {
    const source = `export default ${JSON.stringify(YAML.parse(await readFile(new URL(url), 'utf8')))};`;
    return { format: 'module', shortCircuit: true, source };
  }
  return next(url, context);
}

/**
 * vite plugin: *.yaml import → 파싱된 객체(default export). deck.yaml을 덱 main.js가 그대로 import한다(CONTRACTS C15).
 */
import YAML from 'yaml';

export function deckYaml() {
  return {
    name: 'scrolline-deck-yaml',
    transform(code, id) {
      if (!/\.ya?ml(\?.*)?$/.test(id)) return null;
      return { code: `export default ${JSON.stringify(YAML.parse(code))};`, map: null };
    },
  };
}

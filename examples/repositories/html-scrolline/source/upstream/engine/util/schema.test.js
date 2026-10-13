import { describe, expect, it } from 'vitest';
import { resolveParams, SchemaError, validateSchema } from './schema.js';

const schema = {
  duration: { type: 'number', default: 1, min: 0.2, max: 4, doc: 'length' },
  mode: { type: 'enum', default: 'in', values: ['in', 'out'], doc: 'direction' },
  parts: { type: 'array', default: [], of: { type: 'string', doc: 'part' }, doc: 'parts' },
};
describe('schema', () => {
  it('fills defaults and accepts valid overrides', () =>
    expect(resolveParams(schema, { duration: 2, parts: ['word'] })).toEqual({
      duration: 2,
      mode: 'in',
      parts: ['word'],
    }));
  it('reports unknown keys, ranges, and required fields', () => {
    expect(() => resolveParams(schema, { duration: 9, stray: true })).toThrow(SchemaError);
    expect(
      validateSchema({ title: { type: 'string', required: true, doc: 'title' } }, {}).map((x) => x.path),
    ).toEqual(['title']);
  });
});

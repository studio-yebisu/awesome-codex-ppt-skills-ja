export class SchemaError extends Error {
  /** @param {import('../types.js').SchemaIssue[]} issues */
  constructor(issues) {
    super(issues.map((i) => `${i.path}: ${i.message}`).join('\n'));
    this.name = 'SchemaError';
    this.issues = issues;
  }
}

/**
 * value를 schema로 검사. 문제 목록 반환(없으면 []).
 * @param {import('../types.js').FieldSchema} schema
 * @param {Record<string, any>} value
 * @param {string} [path]
 * @returns {import('../types.js').SchemaIssue[]}
 */
export function validateSchema(schema, value, path = '') {
  const issues = [];
  const at = (key) => (path ? `${path}.${key}` : key);
  if (!isPlainObject(value)) return [{ path: path || '$', message: 'must be an object' }];
  for (const key of Object.keys(value))
    if (!(key in schema)) issues.push({ path: at(key), message: 'unknown key' });
  for (const [key, field] of Object.entries(schema)) {
    const valueAtKey = value[key];
    if (valueAtKey === undefined) {
      if (field.required) issues.push({ path: at(key), message: 'is required' });
      continue;
    }
    issues.push(...validateField(field, valueAtKey, at(key)));
  }
  return issues;
}

/**
 * 기본값을 채운 새 객체 반환. 모르는 키·범위 위반·필수 누락이면 SchemaError.
 * @param {import('../types.js').FieldSchema} schema
 * @param {Record<string, any>} [given]
 * @returns {Record<string, any>}
 */
export function resolveParams(schema, given = {}) {
  const resolved = {};
  const supplied = given === undefined ? {} : given;
  const preflight = !isPlainObject(supplied)
    ? [{ path: '$', message: 'must be an object' }]
    : Object.keys(supplied)
        .filter((key) => !(key in schema))
        .map((key) => ({ path: key, message: 'unknown key' }));
  for (const [key, field] of Object.entries(schema)) {
    if (Object.hasOwn(supplied, key)) resolved[key] = supplied[key];
    else if (Object.hasOwn(field, 'default')) resolved[key] = clone(field.default);
  }
  const issues = [...preflight, ...validateSchema(schema, resolved)];
  if (issues.length) throw new SchemaError(issues);
  return resolved;
}

const isPlainObject = (value) => value !== null && typeof value === 'object' && !Array.isArray(value);
const clone = (value) => (value && typeof value === 'object' ? structuredClone(value) : value);

function validateField(field, value, path) {
  const issues = [];
  const error = (message) => issues.push({ path, message });
  const numeric = field.type === 'number' || field.type === 'integer';
  if (field.type === 'any') return issues;
  if (numeric) {
    if (typeof value !== 'number' || !Number.isFinite(value)) error('must be a finite number');
    else {
      if (field.type === 'integer' && !Number.isInteger(value)) error('must be an integer');
      if (field.min !== undefined && value < field.min) error(`must be >= ${field.min}`);
      if (field.max !== undefined && value > field.max) error(`must be <= ${field.max}`);
    }
  } else if (['string', 'ease', 'part', 'asset'].includes(field.type)) {
    if (typeof value !== 'string') error('must be a string');
  } else if (field.type === 'boolean') {
    if (typeof value !== 'boolean') error('must be a boolean');
  } else if (field.type === 'enum') {
    if (typeof value !== 'string' || !field.values?.includes(value))
      error(`must be one of: ${(field.values || []).join(', ')}`);
  } else if (field.type === 'array') {
    if (!Array.isArray(value)) error('must be an array');
    else if (field.of)
      value.forEach((item, index) => issues.push(...validateField(field.of, item, `${path}[${index}]`)));
  } else if (field.type === 'object') {
    if (!isPlainObject(value)) error('must be an object');
    else if (field.fields) issues.push(...validateSchema(field.fields, value, path));
  } else error(`unknown schema type: ${field.type}`);
  return issues;
}

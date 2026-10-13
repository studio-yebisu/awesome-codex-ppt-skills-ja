/**
 * JSON Schema 부분 검사기(의존 없이 state/schema/*.json 검사용).
 * 지원: type(배열 포함), enum, const, required, properties, additionalProperties(bool|schema),
 *       items, pattern, minimum, maximum, minLength, oneOf, $ref(#/$defs/<name>만)
 */
export function validate(schema, value, path = '$', root = schema, out = []) {
  if (schema.$ref) {
    const name = schema.$ref.replace('#/$defs/', '');
    return validate(root.$defs[name], value, path, root, out);
  }
  const typeOf = (v) =>
    v === null ? 'null' : Array.isArray(v) ? 'array' : Number.isInteger(v) ? 'integer' : typeof v;
  if (schema.type) {
    const types = [].concat(schema.type);
    const t = typeOf(value);
    if (!types.includes(t) && !(t === 'integer' && types.includes('number'))) {
      out.push(`${path}: 형 ${types.join('|')} 필요, 실제 ${t}`);
      return out;
    }
  }
  if (schema.const !== undefined && value !== schema.const)
    out.push(`${path}: ${JSON.stringify(schema.const)} 이어야 함`);
  if (schema.enum && !schema.enum.includes(value))
    out.push(`${path}: ${schema.enum.join('|')} 중 하나여야 함`);
  if (typeof value === 'string') {
    if (schema.pattern && !new RegExp(schema.pattern).test(value))
      out.push(`${path}: 형식 ${schema.pattern} 불일치`);
    if (schema.minLength != null && value.length < schema.minLength)
      out.push(`${path}: 길이 ${schema.minLength} 이상`);
  }
  if (typeof value === 'number') {
    if (schema.minimum != null && value < schema.minimum) out.push(`${path}: ${schema.minimum} 이상`);
    if (schema.maximum != null && value > schema.maximum) out.push(`${path}: ${schema.maximum} 이하`);
  }
  if (Array.isArray(value) && schema.items)
    value.forEach((v, i) => validate(schema.items, v, `${path}[${i}]`, root, out));
  if (value && typeof value === 'object' && !Array.isArray(value)) {
    for (const k of schema.required || []) if (!(k in value)) out.push(`${path}: 필수 키 ${k} 없음`);
    for (const [k, v] of Object.entries(value)) {
      if (schema.properties && k in schema.properties)
        validate(schema.properties[k], v, `${path}.${k}`, root, out);
      else if (schema.additionalProperties === false) out.push(`${path}: 모르는 키 ${k}`);
      else if (typeof schema.additionalProperties === 'object')
        validate(schema.additionalProperties, v, `${path}.${k}`, root, out);
    }
  }
  if (schema.oneOf) {
    const ok = schema.oneOf.filter((s) => validate(s, value, path, root, []).length === 0).length;
    if (ok !== 1) out.push(`${path}: oneOf 중 정확히 1개와 맞아야 함(맞은 수 ${ok})`);
  }
  return out;
}

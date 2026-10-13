/** Internal DOM helpers shared by C4 beat renderers. */
const SVG_NS = 'http://www.w3.org/2000/svg';

export function node(rc, tag, cls, parent, text) {
  if (rc.el) return rc.el(tag, cls, parent, text);
  // engine/util/dom.js el()과 같은 규칙: svg와 SVG 부모의 자식은 SVG 이름공간.
  const svg = tag === 'svg' || (parent?.namespaceURI === SVG_NS && parent.localName !== 'foreignObject');
  const value = svg ? document.createElementNS(SVG_NS, tag) : document.createElement(tag);
  if (cls) value.setAttribute('class', cls);
  if (text != null) value.textContent = text;
  parent?.append(value);
  return value;
}

export function root(type, rc) {
  return node(rc, 'section', `sl-beat sl-beat--${type}`);
}

export function add(parts, name, element) {
  (parts[name] ??= []).push(element);
  element.dataset.part = name;
  return element;
}

export function asset(rc, path) {
  return rc.asset ? rc.asset(path) : path;
}

/** Format one or more deck source ids for a presentational source part. */
export function sourceText(rc, source) {
  const ids = Array.isArray(source) ? source : source ? [source] : [];
  return ids.map((id) => rc.sources?.[id]?.short ?? rc.sources?.[id]?.title ?? id).join(' · ');
}

export function textWords(rc, parent, text, parts) {
  const values = rc.words
    ? rc.words(parent, text)
    : String(text)
        .split(/(\s+)/)
        .filter(Boolean)
        .filter((v) => !/^\s+$/.test(v))
        .map((word) => node(rc, 'span', 'sl-word', parent, word));
  values.forEach((value) => add(parts, 'word', value));
  return values;
}

export function textChars(rc, parent, text, parts) {
  const values = rc.chars
    ? rc.chars(parent, text)
    : Array.from(String(text)).map((char) => node(rc, 'span', 'sl-char', parent, char));
  values.forEach((value) => add(parts, 'char', value));
  return values;
}

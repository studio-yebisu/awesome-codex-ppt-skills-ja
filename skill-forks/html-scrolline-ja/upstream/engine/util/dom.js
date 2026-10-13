const SVG_NS = 'http://www.w3.org/2000/svg';

/** `svg` 태그와 SVG 부모(foreignObject 제외) 안의 자식은 SVG 이름공간으로 만든다(HTML 이름공간이면 브라우저가 그리지 않음). */
function inSvg(tag, parent) {
  if (tag === 'svg') return true;
  return parent?.namespaceURI === SVG_NS && parent.localName !== 'foreignObject';
}

/**
 * @param {string} tag
 * @param {string|null} [cls]
 * @param {Element|null} [parent]
 * @param {string|null} [text]
 * @returns {HTMLElement|SVGElement}
 */
export function el(tag, cls, parent, text) {
  const node = inSvg(tag, parent) ? document.createElementNS(SVG_NS, tag) : document.createElement(tag);
  if (cls) node.setAttribute('class', cls);
  if (text !== null && text !== undefined) node.textContent = text;
  if (parent) parent.append(node);
  return node;
}

/**
 * 어절 단위(공백 분리) span.sl-word[data-part="word"]를 parent에 붙이고 목록 반환. 어절 사이 공백은 텍스트 노드.
 * @param {Element} parent
 * @param {string} text
 * @returns {HTMLElement[]}
 */
export function words(parent, text) {
  const result = [];
  for (const token of String(text).split(/(\s+)/)) {
    if (!token) continue;
    if (/^\s+$/.test(token)) parent.append(document.createTextNode(token));
    else {
      const node = el('span', 'sl-word', parent, token);
      node.dataset.part = 'word';
      result.push(node);
    }
  }
  return result;
}

/**
 * 글자 단위 span.sl-char[data-part="char"]. '\n'은 <br>. 공백도 글자 1개로 센다.
 * @param {Element} parent
 * @param {string} text
 * @returns {HTMLElement[]}
 */
export function chars(parent, text) {
  const result = [];
  for (const char of Array.from(String(text))) {
    if (char === '\n') {
      parent.append(document.createElement('br'));
      continue;
    }
    const node = el('span', 'sl-char', parent, char);
    node.dataset.part = 'char';
    result.push(node);
  }
  return result;
}

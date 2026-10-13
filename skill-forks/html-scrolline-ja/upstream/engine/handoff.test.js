import { describe, expect, it } from 'vitest';
import { anchorOf, defaultMeasure, measure, rectIn, toInset, transferVars } from './handoff.js';

const rect = (x, y, w, h) => ({ x, y, left: x, top: y, width: w, height: h, right: x + w, bottom: y + h });

describe('handoff 좌표 도우미', () => {
  it('rectIn은 root-local 수치를 반환하고 transform을 측정에서 제외한다', () => {
    const root = document.createElement('div');
    const node = document.createElement('div');
    root.append(node);
    document.body.append(root);
    root.getBoundingClientRect = () => rect(100, 50, 800, 600);
    node.style.transform = 'translate(99px, 66px)';
    node.getBoundingClientRect = () =>
      node.style.transform === 'none' ? rect(120, 80, 30, 40) : rect(219, 146, 30, 40);
    expect(rectIn(node, root)).toEqual({ x: 20, y: 30, w: 30, h: 40 });
    expect(node.style.transform).toBe('translate(99px, 66px)');
    root.remove();
  });

  it('snapshot은 각 part를 한 번 측정하며 primary anchor를 기본 선택한다', () => {
    const root = document.createElement('div'),
      node = document.createElement('div');
    root.append(node);
    document.body.append(root);
    const beat = { id: 'one', primary: 'hero', parts: { hero: [node], duplicate: [node] } };
    let calls = 0;
    const snapshot = measure(root, [beat], () => {
      calls += 1;
      return { x: 10, y: 20, w: 30, h: 40 };
    });
    node.style.color = 'rgb(1, 2, 3)';
    node.style.borderRadius = '8px';
    node.style.fontSize = '22px';
    const anchor = anchorOf(beat, undefined, snapshot);
    expect(calls).toBe(1);
    expect(anchor).toMatchObject({
      beat: 'one',
      part: 'hero',
      kind: 'rect',
      rect: { x: 10, y: 20, w: 30, h: 40 },
      point: { x: 25, y: 40 },
      style: { radius: 8, fontSize: 22 },
    });
    root.remove();
  });

  it('inset와 transfer vars를 정확한 px 좌표로 계산한다', () => {
    expect(toInset({ x: 100, y: 80, w: 300, h: 200 }, { w: 1920, h: 1080 })).toBe(
      'inset(80px 1520px 800px 100px)',
    );
    expect(transferVars({ x: 10, y: 20, w: 40, h: 50 }, { x: 110, y: 70, w: 100, h: 25 })).toEqual({
      x: 100,
      y: 50,
      scaleX: 2.5,
      scaleY: 0.5,
      transformOrigin: '0 0',
    });
  });

  it('selects indexed anchors and normalizes negative indices', () => {
    const nodes = [
      document.createElement('span'),
      document.createElement('span'),
      document.createElement('span'),
    ];
    const beat = { id: 'bars', primary: 'mark', parts: { mark: nodes } };
    const snapshot = new Map(nodes.map((node, index) => [node, { x: index * 10, y: 0, w: 8, h: 8 }]));
    expect(anchorOf(beat, 'mark', snapshot, undefined, 1)).toMatchObject({ index: 1, node: nodes[1] });
    expect(anchorOf(beat, 'mark', snapshot, undefined, -1)).toMatchObject({ index: 2, node: nodes[2] });
    expect(() => anchorOf(beat, 'mark', snapshot, undefined, 3)).toThrow('Beat "bars" has no mark[3]');
    expect(() => anchorOf(beat, 'mark', snapshot, undefined, -4)).toThrow('Beat "bars" has no mark[-1]');
  });
});

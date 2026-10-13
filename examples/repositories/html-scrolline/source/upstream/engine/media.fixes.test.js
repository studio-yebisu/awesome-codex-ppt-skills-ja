// 계약 v2 수리 회귀 테스트(C13). 기존 media.test.js는 그대로 둔다(Hat: refactor).
import { describe, expect, it, vi } from 'vitest';
import { textMask, videoClip } from './media.js';

describe('media v2 수리', () => {
  it('textMask: 배경이 투명이라 mask alpha가 글자 모양만 남긴다', () => {
    const svg = decodeURIComponent(textMask('AI', { font: '800 120px sans-serif', width: 400, height: 200 }));
    expect(svg).not.toMatch(/<rect/);
    expect(svg).toMatch(/<text[^>]*fill="white"[^>]*>AI<\/text>/);
    expect(svg).toContain('width="400"');
  });
  it('videoClip: host 이벤트로 스스로 재생하지 않는다(boot가 activate 호출)', () => {
    const host = document.createElement('div');
    const clip = videoClip(host, { src: 'a.mp4', mode: 'play' }, { exportMode: false });
    const play = vi.spyOn(clip.el, 'play').mockResolvedValue();
    host.dispatchEvent(new CustomEvent('scrolline:active'));
    expect(play).not.toHaveBeenCalled();
    clip.activate();
    expect(play).toHaveBeenCalledTimes(1);
    clip.destroy();
  });
});

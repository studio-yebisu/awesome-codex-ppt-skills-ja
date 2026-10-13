import { describe, expect, it, vi } from 'vitest';
import beat from './video.js';
describe('video beat', () => {
  it('renders a playable video media part', () => {
    const view = beat.render(
      { src: 'assets/a.mp4', poster: 'assets/a.webp', alt: '시연', mode: 'loop', caption: '데모' },
      { asset: (p) => `/d/${p}` },
    );
    expect(beat.fields.src.required).toBe(true);
    expect(view.parts.frame).toHaveLength(1);
    expect(view.parts.media[0].tagName).toBe('VIDEO');
    expect(view.parts.media[0].loop).toBe(true);
    expect(view.parts.caption[0].textContent).toBe('데모');
  });
  it('requires poster and mode', () => {
    expect(beat.fields.poster.required).toBe(true);
    expect(beat.fields.mode.required).toBe(true);
  });
  it('keeps the v1 video fallback when media helpers are unavailable', () => {
    const view = beat.render(
      { src: 'assets/a.mp4', poster: 'assets/a.webp', alt: '시연', mode: 'scrub', frames: 'assets/f.json' },
      {},
    );
    expect(view.parts.media[0].tagName).toBe('VIDEO');
  });
  it('uses a frame sequence for scrub video and exposes its handle', () => {
    const canvas = document.createElement('canvas');
    const seq = { canvas, setProgress() {} };
    const frameSequence = vi.fn(() => seq);
    const view = beat.render(
      { src: 'assets/a.mp4', poster: 'assets/a.webp', alt: '시연', mode: 'scrub', frames: 'assets/f.json' },
      { asset: (path) => `/d/${path}`, media: { frameSequence } },
    );
    expect(frameSequence).toHaveBeenCalledWith(expect.any(HTMLDivElement), '/d/assets/f.json');
    expect(view.parts.media).toEqual([canvas]);
    expect(view.media.seq).toBe(seq);
  });
  it('uses a clip handle for play and loop video', () => {
    const el = document.createElement('video');
    const clip = { el };
    const videoClip = vi.fn(() => clip);
    const view = beat.render(
      { src: 'assets/a.mp4', poster: 'assets/a.webp', alt: '시연', mode: 'loop' },
      { asset: (path) => `/d/${path}`, media: { videoClip }, mode: 'export' },
    );
    expect(videoClip).toHaveBeenCalledWith(
      expect.any(HTMLDivElement),
      { src: '/d/assets/a.mp4', poster: '/d/assets/a.webp', loop: true, mode: 'loop' },
      { exportMode: true },
    );
    expect(view.parts.media).toEqual([el]);
    expect(view.media.clip).toBe(clip);
  });
  it('marks text masks without applying a CSS mask and renders credit', () => {
    const view = beat.render(
      {
        src: 'assets/a.mp4',
        poster: 'assets/a.webp',
        alt: '시연',
        mode: 'play',
        credit: 'Stock Inc.',
        mask: { type: 'text', text: 'OPEN' },
      },
      {},
    );
    expect(view.parts.media[0].dataset.maskText).toBe('OPEN');
    expect(view.parts.media[0].classList).toContain('sl-mask');
    expect(view.parts.media[0].style.maskImage).toBe('');
    expect(view.parts.credit[0].textContent).toBe('Stock Inc.');
  });
});

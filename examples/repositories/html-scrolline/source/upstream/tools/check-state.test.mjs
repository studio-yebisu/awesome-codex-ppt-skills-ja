// @vitest-environment node
import { describe, it, expect } from 'vitest';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { validate } from './lib/jsonschema-lite.mjs';
import { checkState } from './check-state.mjs';

const REPO = path.join(path.dirname(fileURLToPath(import.meta.url)), '..');
const schema = (n) => JSON.parse(fs.readFileSync(path.join(REPO, 'state/schema', n), 'utf8'));

describe('state 스키마', () => {
  it('현재 레포 state는 통과', () => {
    const r = checkState(REPO);
    expect(r.board).toEqual([]);
    expect(r.runs).toEqual([]);
  });
  it('run 이벤트 줄: 시작 줄과 끝 줄', () => {
    const s = schema('runs.schema.json');
    const start = {
      run_id: 'a1',
      parent_run_id: null,
      root_run_id: 'a1',
      run_type: 'wave',
      name: 'W2',
      status: 'running',
      started_at: '2026-10-08T14:00:00',
    };
    expect(validate(s, start)).toEqual([]);
    const end = {
      ...start,
      run_id: 'b2',
      parent_run_id: 'a1',
      run_type: 'build',
      name: 'E2',
      model: 'codex gpt-5.6-terra medium',
      hat: 'feature',
      target: { kind: 'engine', id: 'E2' },
      outputs: { files: { 'engine/timeline.js': 'a'.repeat(64) }, commit: 'abc' },
      status: 'success',
      ended_at: '2026-10-08T15:00:00',
      tokens: { input: 1, output: 2, total: 3 },
    };
    expect(validate(s, end)).toEqual([]);
  });
  it('feedback 줄', () => {
    const s = schema('runs.schema.json');
    const fb = {
      kind: 'feedback',
      feedback_id: 'f1',
      run_id: 'b2',
      key: 'wow',
      score: 0.7,
      value: 'PASS',
      by_run_id: 'j1',
      time: '2026-10-08T16:00:00',
    };
    expect(validate(s, fb)).toEqual([]);
    expect(validate(s, { ...fb, score: 7 })).not.toEqual([]);
    expect(validate(s, { ...fb, key: 'vibe' })).not.toEqual([]);
  });
  it('board: 모르는 status·stage는 오류', () => {
    const s = schema('board.schema.json');
    const b = {
      version: 1,
      updated: '2026-10-08T14:00:00Z',
      waves: {},
      engine: {},
      concepts: {},
      moves: {},
      decks: {},
    };
    expect(validate(s, b)).toEqual([]);
    expect(
      validate(s, { ...b, decks: { x: { concept: 'rail', stage: 'brief', status: 'done', runs: [] } } }),
    ).not.toEqual([]);
    expect(
      validate(s, { ...b, moves: { m: { family: 'morph', stage: 'shipping', status: 'todo', runs: [] } } }),
    ).not.toEqual([]);
  });
});

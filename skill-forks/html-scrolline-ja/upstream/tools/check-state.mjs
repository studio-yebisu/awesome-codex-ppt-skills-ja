#!/usr/bin/env node
/**
 * state/board.json·state/runs.jsonl 스키마 검사(plan/CONTRACTS.md C18). 파일이 없으면 통과.
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { validate } from './lib/jsonschema-lite.mjs';

/** @returns {{ board: string[], runs: string[], runLines: number }} */
export function checkState(root) {
  const read = (p) => JSON.parse(fs.readFileSync(path.join(root, p), 'utf8'));
  const res = { board: [], runs: [], runLines: 0 };
  const boardPath = path.join(root, 'state/board.json');
  if (fs.existsSync(boardPath)) {
    try {
      res.board = validate(
        read('state/schema/board.schema.json'),
        JSON.parse(fs.readFileSync(boardPath, 'utf8')),
      );
    } catch (e) {
      res.board = [`board.json 파싱 실패: ${e.message}`];
    }
  }
  const runsPath = path.join(root, 'state/runs.jsonl');
  if (fs.existsSync(runsPath)) {
    const schema = read('state/schema/runs.schema.json');
    fs.readFileSync(runsPath, 'utf8')
      .split('\n')
      .forEach((line, i) => {
        if (!line.trim()) return;
        res.runLines++;
        try {
          res.runs.push(...validate(schema, JSON.parse(line), `line${i + 1}`));
        } catch (e) {
          res.runs.push(`line${i + 1}: JSON 파싱 실패 ${e.message}`);
        }
      });
  }
  return res;
}

const isMain = process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url);
if (isMain) {
  const root = path.resolve(process.argv[2] || path.join(path.dirname(fileURLToPath(import.meta.url)), '..'));
  const r = checkState(root);
  for (const m of [...r.board, ...r.runs]) console.log(m);
  console.log(`check-state: board 오류 ${r.board.length}, runs ${r.runLines}줄 오류 ${r.runs.length}`);
  process.exit(r.board.length + r.runs.length ? 1 : 0);
}

import { randomUUID } from 'node:crypto';
import { existsSync, mkdirSync, readFileSync, renameSync, writeFileSync } from 'node:fs';
import path from 'node:path';

export function workflowTelemetryPath(goalPath, explicit = process.env.DASHI_PPT_TELEMETRY_FILE) {
  return path.resolve(explicit || path.join(path.dirname(path.resolve(goalPath)), 'workflow-telemetry.json'));
}

export function createWorkflowRunId(now = Date.now()) {
  const timestamp = typeof now === 'function' ? Number(now()) : Number(now);
  return `${new Date(timestamp).toISOString().replace(/[-:.TZ]/g, '')}-${randomUUID().slice(0, 8)}`;
}

export function workflowRunIdForGoal(goalPath, explicit = process.env.DASHI_PPT_WORKFLOW_RUN_ID) {
  if (explicit) return String(explicit);
  try {
    const goal = JSON.parse(readFileSync(path.resolve(goalPath), 'utf8'));
    if (goal?.workflowRunId) return String(goal.workflowRunId);
  } catch {
    // A new task without a goal file starts a new run.
  }
  return createWorkflowRunId();
}

export function workflowRunIdForScaffold(goalPath, explicit = process.env.DASHI_PPT_WORKFLOW_RUN_ID, telemetryFile = workflowTelemetryPath(goalPath)) {
  if (explicit) return String(explicit);
  const resolvedGoalPath = path.resolve(goalPath);
  const previous = readWorkflowTelemetry(telemetryFile, true);
  if (previous?.goalPath !== resolvedGoalPath || !previous?.runId) return createWorkflowRunId();
  if (['failed', 'running'].includes(previous.stages?.scaffold?.lastStatus)) {
    return String(previous.runId);
  }
  let goalRunId = null;
  try {
    goalRunId = JSON.parse(readFileSync(resolvedGoalPath, 'utf8'))?.workflowRunId || null;
  } catch {
    // A scaffold retry can start before a goal file exists.
  }
  if (
    String(goalRunId || '') === String(previous.runId)
    && ['failed', 'running'].includes(previous.stages?.render?.lastStatus)
  ) {
    return String(previous.runId);
  }
  return createWorkflowRunId();
}

export function beginWorkflowStage({
  goalPath,
  stage,
  runId = workflowRunIdForGoal(goalPath),
  telemetryFile = workflowTelemetryPath(goalPath),
  now = Date.now,
}) {
  if (!goalPath || !stage) throw new Error('workflow telemetry requires goalPath and stage');
  const file = path.resolve(telemetryFile);
  const startedAtMs = Number(now());
  const previous = readWorkflowTelemetry(file, true);
  const report = previous?.runId === runId ? previous : emptyReport(goalPath, runId, startedAtMs);
  const stageReport = report.stages[stage] || emptyStageReport();
  const retry = stageReport.count > 0 && ['failed', 'running'].includes(stageReport.lastStatus);
  stageReport.count += 1;
  stageReport.retryCount += Number(retry);
  stageReport.lastStatus = 'running';
  report.stages[stage] = stageReport;
  updateReportTotals(report, startedAtMs);
  writeTelemetry(file, report);
  let finished = false;
  return {
    file,
    runId,
    finish({ ok = true, error = null, metrics = null } = {}) {
      if (finished) return readWorkflowTelemetry(file, true);
      finished = true;
      const finishedAtMs = Number(now());
      const current = readWorkflowTelemetry(file, true);
      const report = current?.runId === runId ? current : previous?.runId === runId ? previous : emptyReport(goalPath, runId, startedAtMs);
      const stageReport = report.stages[stage] || emptyStageReport();
      stageReport.successCount += Number(ok);
      stageReport.failureCount += Number(!ok);
      stageReport.durationMs += Math.max(0, Math.round(finishedAtMs - startedAtMs));
      stageReport.lastStatus = ok ? 'passed' : 'failed';
      if (!ok) {
        stageReport.lastFailureCategory = failureCategory(error);
        stageReport.lastFailureReason = failureReason(error);
        report.failures.push({
          stage,
          category: stageReport.lastFailureCategory,
          reason: stageReport.lastFailureReason,
        });
      }
      if (metrics) stageReport.metrics = { ...(stageReport.metrics || {}), ...metrics };
      report.stages[stage] = stageReport;
      updateReportTotals(report, finishedAtMs);
      writeTelemetry(file, report);
      return report;
    },
  };
}

export function readWorkflowTelemetry(file, allowMissing = false) {
  const resolved = path.resolve(file);
  if (!existsSync(resolved)) {
    if (allowMissing) return null;
    throw new Error(`Workflow telemetry not found: ${resolved}`);
  }
  return JSON.parse(readFileSync(resolved, 'utf8'));
}

function emptyStageReport() {
  return { count: 0, successCount: 0, failureCount: 0, retryCount: 0, durationMs: 0,
    lastStatus: null, lastFailureCategory: null, lastFailureReason: null };
}

function updateReportTotals(report, nowMs) {
  report.failureCount = Object.values(report.stages).reduce((sum, item) => sum + item.failureCount, 0);
  report.retryCount = Object.values(report.stages).reduce((sum, item) => sum + item.retryCount, 0);
  report.totalStageCount = Object.values(report.stages).reduce((sum, item) => sum + item.count, 0);
  report.updatedAt = new Date(nowMs).toISOString();
  report.totalDurationMs = Math.max(0, Math.round(nowMs - new Date(report.startedAt).getTime()));
}

function emptyReport(goalPath, runId, startedAtMs) {
  return {
    schemaVersion: 1,
    runId,
    goalPath: path.resolve(goalPath),
    startedAt: new Date(startedAtMs).toISOString(),
    updatedAt: null,
    totalDurationMs: 0,
    totalStageCount: 0,
    failureCount: 0,
    retryCount: 0,
    stages: {},
    failures: [],
  };
}

function failureCategory(error) {
  const text = failureReason(error).toLowerCase();
  if (/layout|candidate|capacity/.test(text)) return 'layout';
  if (/content|fact|projection/.test(text)) return 'content';
  if (/valid|schema|prop/.test(text)) return 'validation';
  if (/render|browser|chrom/.test(text)) return 'render';
  if (/enoent|read|write|file/.test(text)) return 'io';
  return 'unknown';
}

function failureReason(error) {
  return String(error?.message || error || 'unknown failure').replace(/\s+/g, ' ').trim().slice(0, 500);
}

function writeTelemetry(file, report) {
  mkdirSync(path.dirname(file), { recursive: true });
  const temp = `${file}.${process.pid}.tmp`;
  writeFileSync(temp, `${JSON.stringify(report, null, 2)}\n`);
  renameSync(temp, file);
}

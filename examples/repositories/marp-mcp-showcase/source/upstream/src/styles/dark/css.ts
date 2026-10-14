/**
 * Dark style CSS definitions
 * Dark mode with indigo and emerald accents
 */

export const darkCss = `
/* ===== Dark Style for Marp ===== */

/* --- Base: All slides dark --- */
section {
  background: #0f172a;
  color: #e2e8f0;
}
section h1, section h2, section h3, section h4 {
  color: #f1f5f9;
}
section a {
  color: #818cf8;
}
section code {
  background: #1e293b;
  color: #34d399;
}

/* --- Dark Title --- */
section.dk-title {
  background: linear-gradient(135deg, #312e81 0%, #4c1d95 50%, #1e1b4b 100%);
  color: #ffffff;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
}
section.dk-title h1 {
  color: #ffffff;
  font-size: 2.5em;
  font-weight: 700;
  margin-bottom: 0.3em;
  text-shadow: 0 2px 12px rgba(0,0,0,0.4);
}
section.dk-title p {
  color: rgba(255,255,255,0.75);
  font-size: 1.2em;
}

/* --- Dark Section --- */
section.dk-section {
  background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
  color: #ffffff;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
}
section.dk-section h2 {
  color: #818cf8;
  font-size: 2em;
}
section.dk-section p {
  color: rgba(255,255,255,0.7);
}

/* --- Dark Table --- */
section.dk-table table {
  border-collapse: collapse;
  width: 100%;
  margin: 1rem auto;
  font-size: 0.9em;
}
section.dk-table thead th {
  background: #3730a3;
  color: #ffffff;
  padding: 0.7rem 1rem;
  font-weight: 600;
  border: 1px solid #4338ca;
  text-align: left;
}
section.dk-table tbody tr {
  background: #0f172a;
}
section.dk-table tbody tr:nth-child(even) {
  background: #1e293b;
}
section.dk-table tbody td {
  padding: 0.6rem 1rem;
  color: #e2e8f0;
  border: 1px solid #334155;
  text-align: left;
}

/* --- Dark Card Grid --- */
.dk-card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-top: 1rem;
}
.dk-card {
  background: #1e293b;
  border: 1px solid #334155;
  border-radius: 12px;
  padding: 1.2rem;
  text-align: center;
}
.dk-card-icon {
  font-size: 2em;
  margin-bottom: 0.5rem;
}
.dk-card h4 {
  margin: 0.3rem 0;
  color: #f1f5f9;
  font-size: 1em;
}
.dk-card p {
  margin: 0;
  color: #94a3b8;
  font-size: 0.85em;
}

/* --- Dark Timeline --- */
.dk-timeline {
  position: relative;
  padding-left: 36px;
  margin-top: 1rem;
}
.dk-timeline::before {
  content: '';
  position: absolute;
  left: 13px;
  top: 0;
  bottom: 0;
  width: 2px;
  background: linear-gradient(180deg, #818cf8 0%, #34d399 100%);
  border-radius: 2px;
}
.dk-timeline-item {
  position: relative;
  margin-bottom: 1.2rem;
}
.dk-timeline-item::before {
  content: '';
  position: absolute;
  left: -29px;
  top: 0.4em;
  width: 10px;
  height: 10px;
  background: #818cf8;
  border-radius: 50%;
  border: 2px solid #0f172a;
  box-shadow: 0 0 0 2px #818cf8;
}
.dk-timeline-item strong {
  color: #818cf8;
}
.dk-timeline-item span {
  color: #94a3b8;
  margin-left: 0.3rem;
}

/* --- Dark Statistics --- */
.dk-stat-box {
  display: flex;
  justify-content: center;
  gap: 2rem;
  margin-top: 1rem;
  flex-wrap: wrap;
}
.dk-stat-box > div {
  background: #1e293b;
  border: 1px solid #334155;
  border-radius: 12px;
  padding: 1.2rem 2rem;
  text-align: center;
  min-width: 140px;
  flex: 1 1 calc(33.333% - 1.5rem);
  max-width: calc(50% - 1rem);
}
.dk-stat-number {
  font-size: 2.2em;
  font-weight: 700;
  color: #818cf8;
  line-height: 1.1;
}
.dk-stat-label {
  font-size: 0.85em;
  color: #94a3b8;
  margin-top: 0.3rem;
}
.dk-stat-trend {
  font-size: 0.75em;
  color: #34d399;
  margin-top: 0.2rem;
}

/* --- Dark Image Right --- */
.dk-split {
  display: grid;
  grid-template-columns: 3fr 2fr;
  gap: 1.5rem;
  align-items: center;
  margin-top: 1rem;
}
.dk-split img {
  width: 100%;
  object-fit: cover;
  border-radius: 8px;
}
.dk-split-content ul {
  padding-left: 1.2rem;
}
.dk-split-content li {
  margin-bottom: 0.4rem;
  color: #cbd5e1;
}

/* --- Dark Terminal --- */
.dk-terminal-box {
  background: #020617;
  border: 1px solid #334155;
  border-radius: 8px;
  margin-top: 1rem;
  overflow: hidden;
  font-family: 'Courier New', Courier, monospace;
}
.dk-terminal-header {
  background: #1e293b;
  color: #94a3b8;
  padding: 0.5rem 1rem;
  font-size: 0.85em;
  border-bottom: 1px solid #334155;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.dk-terminal-header::before {
  content: '● ● ●';
  color: #475569;
  font-size: 0.8em;
}
.dk-terminal-body {
  padding: 1rem 1.2rem;
}
.dk-terminal-line {
  color: #e2e8f0;
  font-size: 0.85em;
  line-height: 1.8;
  white-space: pre-wrap;
}
.dk-terminal-line[data-cmd]::before,
.dk-terminal-line:not([data-out])::first-line {
  color: #34d399;
}

/* --- Dark Quote --- */
section.dk-quote {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
section.dk-quote blockquote {
  border-left: 4px solid #818cf8;
  padding: 1.5rem 2rem;
  margin: 1rem auto;
  max-width: 80%;
  background: #1e293b;
  border-radius: 0 12px 12px 0;
  font-size: 1.2em;
  font-style: italic;
  color: #cbd5e1;
}
section.dk-quote blockquote p:last-child {
  font-style: normal;
  font-size: 0.85em;
  color: #94a3b8;
  margin-top: 0.5rem;
}

/* --- Dark Image Center --- */
section.dk-img-center {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}
.dk-image-center-wrap {
  text-align: center;
  margin-top: 1rem;
}
.dk-image-center-wrap img {
  max-height: 400px;
  border-radius: 8px;
  object-fit: contain;
}

/* --- Dark Process --- */
.dk-process-steps {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0;
  margin-top: 1.5rem;
  flex-wrap: nowrap;
}
.dk-process-step {
  background: #1e293b;
  border: 1px solid #334155;
  border-radius: 12px;
  padding: 1rem 1.2rem;
  text-align: center;
  flex: 1;
  min-width: 0;
}
.dk-process-step-number {
  font-size: 1.4em;
  font-weight: 700;
  color: #818cf8;
  line-height: 1.2;
}
.dk-process-step-label {
  font-size: 0.85em;
  color: #cbd5e1;
  margin-top: 0.3rem;
}
.dk-process-arrow {
  font-size: 1.5em;
  color: #818cf8;
  padding: 0 0.4rem;
  flex-shrink: 0;
}

/* --- Dark Two Column --- */
.dk-2col {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
  margin-top: 1rem;
}
.dk-2col-panel {
  background: #1e293b;
  border: 1px solid #334155;
  border-radius: 12px;
  padding: 1.2rem;
}
.dk-2col-panel h3 {
  margin-top: 0;
  color: #818cf8;
  font-size: 1.05em;
  border-bottom: 1px solid #334155;
  padding-bottom: 0.4rem;
  margin-bottom: 0.6rem;
}
.dk-2col-panel ul {
  margin: 0;
  padding-left: 1.2rem;
}
.dk-2col-panel li {
  margin-bottom: 0.3rem;
  color: #cbd5e1;
}

/* --- Dark Big Statement --- */
section.dk-statement {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  background: linear-gradient(135deg, #312e81 0%, #1e1b4b 100%);
}
section.dk-statement h1 {
  color: #ffffff;
  font-size: 2.8em;
  font-weight: 800;
  line-height: 1.1;
  max-width: 80%;
  text-shadow: 0 2px 12px rgba(0,0,0,0.4);
}
section.dk-statement p {
  color: rgba(255,255,255,0.7);
  font-size: 1.1em;
  margin-top: 0.5rem;
}

/* --- Dark Highlight Box --- */
.dk-highlight {
  background: linear-gradient(135deg, #818cf8 0%, #34d399 100%);
  color: #fff;
  border-radius: 16px;
  padding: 2rem;
  text-align: center;
  margin: 1.5rem auto;
  max-width: 80%;
}
.dk-highlight h3 {
  margin-top: 0;
  font-size: 1.3em;
  color: #fff;
}
.dk-highlight p {
  margin-bottom: 0;
  font-size: 1.05em;
  color: rgba(255,255,255,0.95);
}

/* --- Dark Progress Bar --- */
.dk-progress-container {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-top: 1rem;
}
.dk-progress-item {
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
}
.dk-progress-header {
  display: flex;
  justify-content: space-between;
  font-size: 0.9em;
}
.dk-progress-label {
  font-weight: 600;
  color: #f1f5f9;
}
.dk-progress-value {
  color: #94a3b8;
}
.dk-progress-track {
  height: 12px;
  background: #334155;
  border-radius: 6px;
  overflow: hidden;
}
.dk-progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #818cf8, #34d399);
  border-radius: 6px;
}

/* --- Dark Chart Bar --- */
.dk-chart-bar-container {
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
  margin-top: 1rem;
}
.dk-chart-bar-row {
  display: flex;
  align-items: center;
  gap: 0.8rem;
}
.dk-chart-bar-label {
  width: 120px;
  flex-shrink: 0;
  font-size: 0.85em;
  font-weight: 600;
  color: #f1f5f9;
  text-align: right;
}
.dk-chart-bar-track {
  flex: 1;
  height: 24px;
  background: #334155;
  border-radius: 4px;
  overflow: hidden;
}
.dk-chart-bar-fill {
  height: 100%;
  background: linear-gradient(90deg, #818cf8, #a78bfa);
  border-radius: 4px;
}
.dk-chart-bar-value {
  width: 50px;
  flex-shrink: 0;
  font-size: 0.85em;
  font-weight: 600;
  color: #818cf8;
}

/* --- Dark Horizontal Timeline --- */
.dk-h-timeline {
  position: relative;
  margin-top: 2rem;
}
.dk-h-timeline-line {
  position: absolute;
  top: 9px;
  left: 5%;
  right: 5%;
  height: 3px;
  background: linear-gradient(90deg, #818cf8, #34d399);
  border-radius: 2px;
}
.dk-h-timeline-items {
  display: flex;
  justify-content: space-around;
  position: relative;
}
.dk-h-timeline-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  max-width: 150px;
}
.dk-h-timeline-dot {
  width: 14px;
  height: 14px;
  background: #818cf8;
  border: 3px solid #0f172a;
  border-radius: 50%;
  box-shadow: 0 0 0 2px #818cf8;
  margin-bottom: 0.8rem;
  flex-shrink: 0;
}
.dk-h-timeline-item strong {
  font-size: 0.85em;
  color: #f1f5f9;
}
.dk-h-timeline-item span {
  font-size: 0.75em;
  color: #94a3b8;
  margin-top: 0.2rem;
}

/* --- Dark Code Comparison --- */
.dk-code-compare {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  margin-top: 1rem;
}
.dk-code-panel {
  background: #020617;
  border: 1px solid #334155;
  border-radius: 8px;
  overflow: hidden;
  font-family: 'Courier New', Courier, monospace;
}

/* --- Card Grid Improvement --- */
.dk-card-icon {
  width: 2.5em;
  height: 2.5em;
  line-height: 2.5em;
  border-radius: 50%;
  background: rgba(129,140,248,0.15);
  display: inline-block;
  margin-bottom: 0.5rem;
}
.dk-card {
  box-shadow: 0 2px 8px rgba(0,0,0,0.2);
}

/* --- Code Showcase --- */
.dk-code-showcase {
  background: #0f172a;
  border: 1px solid #334155;
  border-radius: 8px;
  overflow: hidden;
  margin-top: 0.5rem;
}
.dk-code-header {
  background: #1e293b;
  padding: 0.4rem 1rem;
  display: flex;
  align-items: center;
  min-height: 1.8rem;
  border-bottom: 1px solid #334155;
}
.dk-code-lang-badge {
  font-size: 0.75em;
  font-family: monospace;
  color: #818cf8;
  background: rgba(129,140,248,0.12);
  padding: 0.1rem 0.6rem;
  border-radius: 4px;
  border: 1px solid rgba(129,140,248,0.25);
}
.dk-code-body {
  padding: 0.8rem 1rem;
  font-family: "Cascadia Code", "Fira Code", "JetBrains Mono", monospace;
  font-size: 0.82em;
  line-height: 1.6;
  overflow-x: auto;
}
.dk-code-line {
  color: #e2e8f0;
  white-space: pre;
}
.dk-code-explanation {
  font-size: 0.9em;
  color: #94a3b8;
  margin-top: 0.6rem;
  line-height: 1.5;
}
.dk-code-highlights {
  margin-top: 0.5rem;
  padding-left: 1.2rem;
}
.dk-code-highlights li {
  font-size: 0.88em;
  color: #a5b4fc;
  margin-bottom: 0.25rem;
}
`;

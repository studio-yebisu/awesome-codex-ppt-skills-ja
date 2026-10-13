import React from 'react';
import { useSlideViewModel } from '../../view-model/context.jsx';
import { getBespokeThemeProfile } from './theme-profiles.mjs';

export const BESPOKE_GRID_COLUMNS = 12;
export const BESPOKE_GRID_ROWS = 8;

const ALIGNMENTS = {
  left: 'left',
  center: 'center',
  right: 'right',
};

const TEXT_ROLES = {
  kicker: { fontSize: 21, lineHeight: 1.2, fontWeight: 780, letterSpacing: '.15em', textTransform: 'uppercase' },
  title: { fontSize: 76, lineHeight: 1.02, fontWeight: 900, letterSpacing: '-.035em' },
  subtitle: { fontSize: 38, lineHeight: 1.24, fontWeight: 650, letterSpacing: '-.012em' },
  body: { fontSize: 28, lineHeight: 1.5, fontWeight: 450, letterSpacing: 0 },
  label: { fontSize: 19, lineHeight: 1.2, fontWeight: 750, letterSpacing: '.14em', textTransform: 'uppercase' },
  caption: { fontSize: 21, lineHeight: 1.4, fontWeight: 500, letterSpacing: '.02em' },
};

export function BespokeSlide({ composition = {} }) {
  const viewModel = useSlideViewModel() || {};
  const themePack = viewModel.themePack || 'theme01';
  const profile = profileForBackground(getBespokeThemeProfile(themePack), composition.background);
  const physicalId = viewModel.physicalId || viewModel.stateId || viewModel.id;
  const sourceSlideId = viewModel.sourceSlideId || viewModel.pageId || viewModel.logicalId || viewModel.id;
  const stateId = viewModel.stateId || physicalId;
  const elements = Array.isArray(composition?.elements) ? composition.elements.slice(0, 32) : [];
  const family = profile.editorial ? inferTheme05Family(elements) : '';

  return (
    <section
      className="slide bespoke-slide"
      data-vm-slide-id={physicalId}
      data-vm-source-slide-id={sourceSlideId}
      data-vm-slide-key={viewModel.key || physicalId}
      data-vm-index={viewModel.index}
      data-vm-variant-state-id={stateId}
      data-vm-variant-id={viewModel.variantId}
      data-vm-variant-index={viewModel.variantIndex}
      data-vm-variant-count={viewModel.variantCount}
      data-vm-variant-kind="bespoke"
      data-vm-variant-mode={viewModel.variantMode || 'comparison'}
      data-theme-pack={themePack}
      data-bespoke-family={family || undefined}
      data-logical-slide={viewModel.logicalIndex}
      data-label={viewModel.label || 'Agent 定制方案'}
      aria-label={viewModel.label || 'Agent 定制方案'}
    >
      <div className="bespoke-root" style={rootStyle(profile)}>
        {!profile.editorial && <>
          <div aria-hidden="true" data-editable-skip="true" style={ambientStyle(profile.accent, { top: -240, right: -150 })} />
          <div aria-hidden="true" data-editable-skip="true" style={ambientStyle(profile.accent2, { bottom: -280, left: -170 })} />
        </>}
        {profile.editorial && <div aria-hidden="true" data-editable-skip="true" style={{ position: 'absolute', top: 0, left: profile.padX, right: profile.padX, height: profile.strongRule, display: 'flex' }}>
          {profile.spectrum.map(color => <span key={color} style={{ flex: 1, background: color }} />)}
        </div>}
        <div className="bespoke-grid" style={canvasStyle(profile)}>
          {elements.map((element, index) => (
            <BespokeElement
              key={element?.id || `${element?.type || 'element'}-${index + 1}`}
              element={element || {}}
              index={index}
              profile={profile}
              family={family}
            />
          ))}
        </div>
      </div>
    </section>
  );
}

function BespokeElement({ element, index, profile, family }) {
  switch (element.type) {
    case 'text':
      return <TextElement element={element} index={index} profile={profile} family={family} />;
    case 'metric':
      return <MetricElement element={element} index={index} profile={profile} />;
    case 'list':
      return <ListElement element={element} index={index} profile={profile} />;
    case 'quote':
      return <QuoteElement element={element} index={index} profile={profile} />;
    case 'media':
      return <MediaElement element={element} index={index} profile={profile} />;
    case 'shape':
      return <ShapeElement element={element} index={index} profile={profile} />;
    case 'chart':
      return <ChartElement element={element} index={index} profile={profile} />;
    default:
      return null;
  }
}

function TextElement({ element, index, profile, family }) {
  const role = TEXT_ROLES[element.role] || TEXT_ROLES.body;
  const text = plainText(element.text);
  const color = toneColor(profile, element.tone);
  return (
    <div
      data-bespoke-element="text"
      style={{
        ...elementGridStyle(element),
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'flex-start',
        color,
        textAlign: ALIGNMENTS[element.align] || 'left',
        fontFamily: element.role === 'label' || element.role === 'kicker' ? profile.fontMono : profile.fontDisplay,
        paddingTop: profile.editorial && Number(element?.grid?.row) === 1 && element.role !== 'label' ? 24 : 0,
        paddingBottom: profile.editorial && element.role === 'title' ? 12 : 0,
        borderBottom: profile.editorial && element.role === 'title' ? `${profile.strongRule}px solid ${profile.ink}` : undefined,
        overflow: 'hidden',
      }}
    >
      <div
        data-editable-path={editablePath(element, index, 'text')}
        style={{
          ...(profile.editorial ? theme05TextRole(element, family, text) : role),
          overflowWrap: 'anywhere',
          textWrap: element.role === 'title' ? 'balance' : 'pretty',
        }}
      >
        {text}
      </div>
    </div>
  );
}

function MetricElement({ element, index, profile }) {
  const editorial = profile.editorial === true;
  const inverse = editorial && element.tone === 'inverse';
  const value = plainText(element.value);
  return (
    <div
      data-bespoke-element="metric"
      style={{
        ...elementGridStyle(element),
        ...cardStyle(profile, true),
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'space-between',
        color: inverse ? profile.onDark : profile.ink,
        padding: editorial ? (inverse ? '34px 38px' : '18px 0 0') : 30,
        background: inverse ? profile.dark : editorial ? 'transparent' : profile.surface,
        borderTop: editorial && !inverse ? `${profile.strongRule}px solid ${profile.ink}` : undefined,
        overflow: 'hidden',
      }}
    >
      <div
        data-editable-path={editablePath(element, index, 'label')}
        style={{
          color: inverse ? profile.onDark : profile.muted,
          fontFamily: profile.fontMono,
          fontSize: 19,
          fontWeight: 700,
          letterSpacing: '.12em',
          lineHeight: 1.2,
          textTransform: 'uppercase',
        }}
      >
        {plainText(element.label)}
      </div>
      <div style={{ display: 'flex', alignItems: 'baseline', gap: 14, minWidth: 0 }}>
        <strong
          data-editable-path={editablePath(element, index, 'value')}
          style={{
            color: inverse ? profile.onDark : toneColor(profile, element.tone || 'accent'),
            fontFamily: profile.fontDisplay,
            fontSize: editorial ? theme05MetricSize(element, value) : 88,
            fontWeight: 900,
            letterSpacing: '-.045em',
            lineHeight: 0.9,
            overflowWrap: 'anywhere',
          }}
        >
          {value}
        </strong>
      </div>
      {element.detail != null && (
        <div
          data-editable-path={editablePath(element, index, 'detail')}
          style={{ color: inverse ? profile.onDark : profile.muted, fontSize: editorial ? 19 : 22, lineHeight: 1.4, overflowWrap: 'anywhere' }}
        >
          {plainText(element.detail)}
        </div>
      )}
      {element.trend != null && (
        <div
          data-editable-path={editablePath(element, index, 'trend')}
          style={{
            alignSelf: 'flex-start',
            color: toneColor(profile, element.tone === 'critical' ? 'critical' : 'positive'),
            fontFamily: profile.fontMono,
            fontSize: 18,
            fontWeight: 750,
            lineHeight: 1.2,
            padding: '7px 10px',
            border: `1px solid ${profile.line}`,
            borderRadius: editorial ? 0 : Math.max(3, profile.radius / 2),
          }}
        >
          {plainText(element.trend)}
        </div>
      )}
    </div>
  );
}

function ListElement({ element, index, profile }) {
  const source = Array.isArray(element.items) ? element.items : [];
  const items = source;
  const dense = profile.editorial && items.length > 6;
  return (
    <div
      data-bespoke-element="list"
      style={{
        ...elementGridStyle(element),
        ...cardStyle(profile, true),
        display: 'flex',
        flexDirection: 'column',
        gap: dense ? 8 : 16,
        color: profile.ink,
        padding: profile.editorial ? '12px 0 0' : 30,
        borderTop: profile.editorial ? `${profile.strongRule}px solid ${profile.ink}` : undefined,
        overflow: 'hidden',
      }}
    >
      <div style={{ display: 'grid', gap: dense ? 6 : 12, minHeight: 0, overflow: 'hidden' }}>
        {items.map((item, itemIndex) => {
          const normalized = normalizeListItem(item);
          return (
            <div
              key={normalized.id || itemIndex}
              style={{
                display: 'grid',
                gridTemplateColumns: '30px minmax(0,1fr)',
                gap: 12,
                alignItems: 'start',
                paddingTop: itemIndex ? (dense ? 6 : 12) : 0,
                borderTop: itemIndex ? `1px solid ${profile.line}` : '0',
              }}
            >
              <span
                aria-hidden="true"
                data-editable-skip="true"
                style={{
                  color: toneColor(profile, element.tone || 'accent'),
                  fontFamily: profile.fontMono,
                  fontSize: 18,
                  fontWeight: 800,
                  lineHeight: 1.45,
                }}
              >
                {element.ordered ? String(itemIndex + 1).padStart(2, '0') : profile.editorial ? '—' : '•'}
              </span>
              <div style={{ minWidth: 0 }}>
                <div
                  data-editable-path={editablePath(element, index, `items.${itemIndex}.title`)}
                  style={{ fontSize: dense ? 19 : profile.editorial ? 22 : 25, fontWeight: profile.editorial ? 760 : 720, lineHeight: 1.3, overflowWrap: 'anywhere' }}
                >
                  {normalized.title}
                </div>
                {normalized.body && (
                  <div
                    data-editable-path={editablePath(element, index, `items.${itemIndex}.body`)}
                    style={{ color: profile.muted, fontSize: dense ? 16 : profile.editorial ? 18 : 20, lineHeight: 1.42, marginTop: dense ? 2 : 5, overflowWrap: 'anywhere' }}
                  >
                    {normalized.body}
                  </div>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

function QuoteElement({ element, index, profile }) {
  const quote = plainText(element.quote);
  return (
    <blockquote
      data-bespoke-element="quote"
      style={{
        ...elementGridStyle(element),
        ...cardStyle(profile, true),
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        gap: profile.editorial ? 18 : 26,
        padding: profile.editorial ? '20px 0 0' : 30,
        borderTop: profile.editorial ? `${profile.strongRule}px solid ${profile.ink}` : undefined,
        margin: 0,
        overflow: 'hidden',
      }}
    >
      {!profile.editorial && <div
        aria-hidden="true"
        data-editable-skip="true"
        style={{
          color: toneColor(profile, element.tone || 'accent'),
          fontFamily: profile.fontDisplay,
          fontSize: 100,
          fontWeight: 900,
          lineHeight: 0.5,
        }}
      >
        “
      </div>}
      <div
        data-editable-path={editablePath(element, index, 'text')}
        style={{
          color: profile.ink,
          fontFamily: profile.fontDisplay,
          fontSize: profile.editorial ? theme05StatementSize(quote) : 42,
          fontWeight: profile.editorial ? 800 : 760,
          letterSpacing: '-.018em',
          lineHeight: 1.24,
          textAlign: 'left',
          textWrap: 'balance',
          overflowWrap: 'anywhere',
        }}
      >
        {quote}
      </div>
      {element.attribution != null && (
        <cite
          data-editable-path={editablePath(element, index, 'attribution')}
          style={{
            color: profile.muted,
            fontFamily: profile.fontMono,
            fontSize: 20,
            fontStyle: 'normal',
            letterSpacing: '.07em',
          }}
        >
          {plainText(element.attribution)}
        </cite>
      )}
    </blockquote>
  );
}

function MediaElement({ element, index, profile }) {
  const src = safeMediaSource(element.src);
  const fit = element.fit === 'contain' ? 'contain' : 'cover';
  const isVideo = /\.(mp4|webm|mov|m4v)(?:[?#].*)?$/i.test(src) || /^data:video\//i.test(src);
  return (
    <figure
      data-bespoke-element="media"
      style={{
        ...elementGridStyle(element),
        position: 'relative',
        margin: 0,
        overflow: 'hidden',
        borderRadius: profile.mediaTreatment.radius,
        border: profile.mediaTreatment.border,
        background: profile.surface,
        boxShadow: profile.shadow,
      }}
    >
      {src ? (
        isVideo ? (
          <video
            src={src}
            muted
            loop
            playsInline
            preload="metadata"
            style={{ width: '100%', height: '100%', display: 'block', objectFit: fit, filter: profile.mediaTreatment.filter }}
          />
        ) : (
          <img
            src={src}
            alt={plainText(element.alt)}
            loading="lazy"
            decoding="async"
            style={{ width: '100%', height: '100%', display: 'block', objectFit: fit, filter: profile.mediaTreatment.filter }}
          />
        )
      ) : (
        <div
          aria-hidden="true"
          data-editable-skip="true"
          style={{
            width: '100%',
            height: '100%',
            display: 'grid',
            placeItems: 'center',
            color: profile.muted,
            fontFamily: profile.fontMono,
            fontSize: 18,
            letterSpacing: '.14em',
            background: profile.editorial ? profile.bg : `linear-gradient(135deg,${profile.surface},transparent)`,
          }}
        >
          MEDIA
        </div>
      )}
      <div
        aria-hidden="true"
        data-editable-skip="true"
        style={{ position: 'absolute', inset: 0, pointerEvents: 'none', background: profile.mediaTreatment.overlay }}
      />
    </figure>
  );
}

function ShapeElement({ element, index, profile }) {
  const shape = ['rect', 'circle', 'line', 'panel'].includes(element.shape)
    ? element.shape
    : 'panel';
  const color = shape === 'panel' && (!element.tone || element.tone === 'default')
    ? profile.surface
    : toneColor(profile, element.tone || 'accent');
  const direction = Number(element?.grid?.width) >= Number(element?.grid?.height) ? 'horizontal' : 'vertical';
  const line = shape === 'line';
  return (
    <div
      aria-hidden="true"
      data-editable-skip="true"
      data-bespoke-element="shape"
      data-bespoke-shape={shape}
      data-bespoke-index={index}
      style={{
        ...elementGridStyle(element),
        width: line && direction === 'vertical' ? (profile.editorial ? profile.strongRule : 3) : '100%',
        height: line && direction === 'horizontal' ? (profile.editorial ? profile.strongRule : 3) : '100%',
        alignSelf: line ? 'center' : 'stretch',
        justifySelf: line ? 'center' : 'stretch',
        borderRadius: shape === 'circle'
          ? 999
          : shape === 'panel'
            ? profile.radius
            : 0,
        border: shape === 'panel' ? `1px solid ${profile.line}` : '0',
        background: color,
        boxShadow: shape === 'panel' ? profile.shadow : 'none',
        opacity: element.tone === 'muted' ? 0.32 : 1,
        pointerEvents: 'none',
      }}
    />
  );
}

function ChartElement({ element, index, profile }) {
  const data = normalizeChartData(element.data);
  const chartType = ['bar', 'line', 'donut', 'progress'].includes(element.chartType) ? element.chartType : 'bar';
  return (
    <div
      data-bespoke-element="chart"
      data-bespoke-chart={chartType}
      style={{
        ...elementGridStyle(element),
        ...cardStyle(profile, true),
        display: 'flex',
        flexDirection: 'column',
        gap: 18,
        padding: profile.editorial ? '18px 0 0' : 30,
        borderTop: profile.editorial ? `${profile.strongRule}px solid ${profile.ink}` : undefined,
        overflow: 'hidden',
      }}
    >
      <div style={{ flex: '1 1 auto', minHeight: 0 }}>
        {chartType === 'line' && <LineChart data={data} profile={profile} showValues={element.showValues === true} />}
        {chartType === 'donut' && <DonutChart data={data} profile={profile} showValues={element.showValues === true} />}
        {chartType === 'progress' && <ProgressChart data={data} profile={profile} showValues={element.showValues === true} />}
        {chartType === 'bar' && <BarChart data={data} profile={profile} showValues={element.showValues === true} />}
      </div>
    </div>
  );
}

function BarChart({ data, profile, showValues }) {
  const domain = signedChartDomain(data);
  const slot = 900 / Math.max(1, data.length);
  const barWidth = Math.min(96, slot * 0.58);
  return (
    <svg viewBox="0 0 1000 420" width="100%" height="100%" preserveAspectRatio="none" aria-hidden="true" data-editable-skip="true">
      {gridLines(profile, domain.zeroY)}
      {data.map((item, index) => {
        const valueY = domain.y(item.value);
        const height = Math.max(2, Math.abs(valueY - domain.zeroY));
        const x = 60 + index * slot + (slot - barWidth) / 2;
        const y = item.value > 0 ? valueY : item.value < 0 ? domain.zeroY : domain.zeroY - 1;
        const color = chartColor(profile, index);
        return (
          <g key={`${item.label}-${index}`}>
            <rect x={x} y={y} width={barWidth} height={height} rx={profile.chartTreatment.barRadius} fill={color} />
            {showValues && (
              <text x={x + barWidth / 2} y={item.value < 0 ? Math.min(368, y + height + 24) : Math.max(28, y - 12)} textAnchor="middle" fill={profile.ink} fontSize="19" fontWeight="700">
                {formatChartDatum(item)}
              </text>
            )}
            <text x={x + barWidth / 2} y="382" textAnchor="middle" fill={profile.chartTreatment.label} fontSize="20">
              {truncateLabel(item.label)}
            </text>
          </g>
        );
      })}
    </svg>
  );
}

function LineChart({ data, profile, showValues }) {
  const domain = signedChartDomain(data);
  const denominator = Math.max(1, data.length - 1);
  const points = data.map((item, index) => ({
    ...item,
    x: 70 + index / denominator * 860,
    y: domain.y(item.value),
  }));
  return (
    <svg viewBox="0 0 1000 420" width="100%" height="100%" preserveAspectRatio="none" aria-hidden="true" data-editable-skip="true">
      {gridLines(profile, domain.zeroY)}
      <polyline
        points={points.map(point => `${point.x},${point.y}`).join(' ')}
        fill="none"
        stroke={profile.chartTreatment.series[0] || profile.accent}
        strokeWidth={profile.chartTreatment.strokeWidth}
        strokeLinejoin="round"
        strokeLinecap="round"
      />
      {points.map((point, index) => (
        <g key={`${point.label}-${index}`}>
          <circle cx={point.x} cy={point.y} r="9" fill={chartColor(profile, index)} />
          {showValues && (
            <text x={point.x} y={point.value < 0 ? Math.min(365, point.y + 28) : Math.max(24, point.y - 18)} textAnchor="middle" fill={profile.ink} fontSize="18" fontWeight="700">
              {formatChartDatum(point)}
            </text>
          )}
          <text x={point.x} y="382" textAnchor="middle" fill={profile.chartTreatment.label} fontSize="20">
            {truncateLabel(point.label)}
          </text>
        </g>
      ))}
    </svg>
  );
}

function DonutChart({ data, profile, showValues }) {
  const total = Math.max(1, data.reduce((sum, item) => sum + item.value, 0));
  const radius = 125;
  const circumference = 2 * Math.PI * radius;
  let offset = 0;
  const segments = data.map((item, index) => {
    const length = item.value / total * circumference;
    const segment = { ...item, index, length, offset };
    offset += length;
    return segment;
  });
  return (
    <div style={{ width: '100%', height: '100%', display: 'grid', gridTemplateColumns: 'minmax(0,1fr) minmax(180px,.72fr)', gap: 24, alignItems: 'center' }}>
      <svg viewBox="0 0 420 420" width="100%" height="100%" aria-hidden="true" data-editable-skip="true">
        <circle cx="210" cy="210" r={radius} fill="none" stroke={profile.chartTreatment.grid} strokeWidth="58" />
        {segments.map(segment => (
          <circle
            key={`${segment.label}-${segment.index}`}
            cx="210"
            cy="210"
            r={radius}
            fill="none"
            stroke={chartColor(profile, segment.index)}
            strokeWidth="58"
            strokeDasharray={`${segment.length} ${Math.max(0, circumference - segment.length)}`}
            strokeDashoffset={-segment.offset}
            transform="rotate(-90 210 210)"
          />
        ))}
      </svg>
      <div style={{ display: 'grid', gap: 12, minWidth: 0 }}>
        {segments.map(segment => (
          <div key={`${segment.label}-${segment.index}`} style={{ display: 'grid', gridTemplateColumns: '12px minmax(0,1fr) auto', gap: 10, alignItems: 'center' }}>
            <span aria-hidden="true" data-editable-skip="true" style={{ width: 10, height: 10, borderRadius: 99, background: chartColor(profile, segment.index) }} />
            <span style={{ color: profile.muted, fontSize: 18, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
              {segment.label}
            </span>
            {showValues && (
              <strong style={{ color: profile.ink, fontFamily: profile.fontMono, fontSize: 18 }}>
                {formatChartDatum(segment)}
              </strong>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

function ProgressChart({ data, profile, showValues }) {
  const max = Math.max(100, ...data.map(item => item.value));
  return (
    <div style={{ width: '100%', height: '100%', display: 'grid', alignContent: 'center', gap: 18 }}>
      {data.map((item, index) => {
        const width = Math.min(100, item.value / max * 100);
        return (
          <div key={`${item.label}-${index}`} style={{ display: 'grid', gridTemplateColumns: showValues ? 'minmax(120px,.8fr) minmax(0,2fr) 70px' : 'minmax(120px,.8fr) minmax(0,2fr)', gap: 16, alignItems: 'center' }}>
            <span style={{ color: profile.muted, fontSize: 20, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
              {item.label}
            </span>
            <span aria-hidden="true" data-editable-skip="true" style={{ height: 14, overflow: 'hidden', borderRadius: profile.editorial ? 0 : 999, background: profile.chartTreatment.grid }}>
              <span style={{ display: 'block', width: `${width}%`, height: '100%', borderRadius: profile.editorial ? 0 : 999, background: chartColor(profile, index) }} />
            </span>
            {showValues && (
              <strong style={{ color: profile.ink, fontFamily: profile.fontMono, fontSize: 18, textAlign: 'right' }}>
                {formatChartDatum(item)}
              </strong>
            )}
          </div>
        );
      })}
    </div>
  );
}

function gridLines(profile, zeroY) {
  const lines = [0, 1, 2, 3].map(index => {
    const y = 66 + index * 91;
    return <line key={y} x1="50" x2="950" y1={y} y2={y} stroke={profile.chartTreatment.grid} strokeWidth={profile.editorial ? profile.hairline : 2} />;
  });
  lines.push(<line key="baseline" x1="50" x2="950" y1={zeroY} y2={zeroY} stroke={profile.ink} strokeWidth={profile.editorial ? profile.strongRule : 2} />);
  return lines;
}

function signedChartDomain(data) {
  let min = Math.min(0, ...data.map(item => item.value));
  let max = Math.max(0, ...data.map(item => item.value));
  if (min === max) [min, max] = [-1, 1];
  const y = value => 340 - (value - min) / (max - min) * 290;
  return { zeroY: y(0), y };
}

function inferTheme05Family(elements) {
  if (elements.some(element => element.type === 'chart')) return 'chart-led';
  if (elements.some(element => element.type === 'media')) return 'media-split';
  if (elements.some(element => element.type === 'metric')) return 'metric-hero';
  if (elements.some(element => element.type === 'quote')) return 'statement';
  return 'ledger';
}

function theme05TextRole(element, family, text) {
  const length = [...text].length;
  if (element.role === 'label' || element.role === 'kicker') {
    return { fontSize: 18, lineHeight: 1.2, fontWeight: 800, letterSpacing: '.14em', textTransform: 'uppercase' };
  }
  if (element.role === 'title') {
    const base = family === 'ledger' ? 78 : family === 'media-split' ? 68 : family === 'chart-led' ? 58 : 46;
    return {
      fontSize: length <= 14 ? base : length <= 24 ? base - 10 : Math.max(38, base - 20),
      lineHeight: 1.02,
      fontWeight: 800,
      letterSpacing: '-.035em',
    };
  }
  if (element.role === 'subtitle') return { fontSize: length > 70 ? 24 : 30, lineHeight: 1.22, fontWeight: 650, letterSpacing: '-.012em' };
  if (element.role === 'body') return { fontSize: length > 90 ? 21 : 25, lineHeight: 1.45, fontWeight: 500 };
  return { fontSize: length > 70 ? 17 : 20, lineHeight: 1.4, fontWeight: 520, letterSpacing: '.01em' };
}

function theme05MetricSize(element, value) {
  const length = [...value].length;
  if (element.tone !== 'inverse') return length <= 8 ? 104 : 76;
  return length <= 6 ? 312 : length <= 10 ? 220 : 154;
}

function theme05StatementSize(text) {
  const length = [...text].length;
  return length <= 18 ? 132 : length <= 34 ? 112 : length <= 60 ? 92 : 72;
}

function rootStyle(profile) {
  return {
    '--bespoke-bg': profile.bg,
    '--bespoke-surface': profile.surface,
    '--bespoke-ink': profile.ink,
    '--bespoke-muted': profile.muted,
    '--bespoke-accent': profile.accent,
    '--bespoke-accent-2': profile.accent2,
    '--bespoke-line': profile.line,
    '--bespoke-pad': `${profile.pad}px`,
    '--bespoke-gap': `${profile.gap}px`,
    '--bespoke-radius': `${profile.radius}px`,
    position: 'absolute',
    top: 0,
    left: 0,
    width: 1920,
    height: 1080,
    overflow: 'hidden',
    transform: 'scale(var(--deck-scale,1))',
    transformOrigin: 'top left',
    isolation: 'isolate',
    background: profile.bg,
    color: profile.ink,
    fontFamily: profile.fontBody,
    WebkitFontSmoothing: 'antialiased',
  };
}

function profileForBackground(profile, background) {
  if (profile.editorial) return profile;
  if (background === 'surface') {
    return { ...profile, bg: profile.surface };
  }
  if (background === 'muted') {
    return {
      ...profile,
      bg: `linear-gradient(145deg,${profile.surface},${profile.bg})`,
    };
  }
  if (background === 'accent') {
    return {
      ...profile,
      bg: profile.accent,
      surface: 'rgba(0,0,0,.14)',
      ink: '#ffffff',
      muted: 'rgba(255,255,255,.74)',
      line: 'rgba(255,255,255,.24)',
      accent: profile.accent2,
    };
  }
  if (background === 'dark') {
    return {
      ...profile,
      bg: '#0b0b0d',
      surface: 'rgba(255,255,255,.08)',
      ink: '#f7f7f4',
      muted: 'rgba(247,247,244,.68)',
      line: 'rgba(247,247,244,.18)',
    };
  }
  if (background === 'light') {
    return {
      ...profile,
      bg: '#f4f3ef',
      surface: 'rgba(255,255,255,.78)',
      ink: '#171714',
      muted: '#6f706b',
      line: 'rgba(23,23,20,.16)',
    };
  }
  return profile;
}

function ambientStyle(color, position) {
  return {
    position: 'absolute',
    width: 620,
    height: 620,
    borderRadius: '50%',
    background: color,
    filter: 'blur(130px)',
    opacity: 0.1,
    pointerEvents: 'none',
    zIndex: 0,
    ...position,
  };
}

function canvasStyle(profile) {
  return {
    position: 'absolute',
    inset: 0,
    zIndex: 1,
    display: 'grid',
    gridTemplateColumns: `repeat(${BESPOKE_GRID_COLUMNS},minmax(0,1fr))`,
    gridTemplateRows: `repeat(${BESPOKE_GRID_ROWS},minmax(0,1fr))`,
    gap: 'var(--bespoke-gap)',
    padding: `${profile.padY ?? profile.pad}px ${profile.padX ?? profile.pad}px`,
  };
}

function elementGridStyle(element) {
  const grid = element?.grid || {};
  const column = clampInteger(grid.column, 1, BESPOKE_GRID_COLUMNS, 1);
  const row = clampInteger(grid.row, 1, BESPOKE_GRID_ROWS, 1);
  const width = clampInteger(grid.width, 1, BESPOKE_GRID_COLUMNS - column + 1, 1);
  const height = clampInteger(grid.height, 1, BESPOKE_GRID_ROWS - row + 1, 1);
  return {
    gridColumn: `${column} / span ${width}`,
    gridRow: `${row} / span ${height}`,
    minWidth: 0,
    minHeight: 0,
    position: 'relative',
    zIndex: element.type === 'shape' ? 0 : 2,
  };
}

function cardStyle(profile, enabled) {
  if (!enabled) return { padding: 0, background: 'transparent', border: 0, borderRadius: 0, boxShadow: 'none' };
  if (profile.editorial) return { padding: 0, background: 'transparent', border: 0, borderRadius: 0, boxShadow: 'none' };
  return {
    padding: 30,
    background: profile.surface,
    border: `1px solid ${profile.line}`,
    borderRadius: profile.radius,
    boxShadow: profile.shadow,
  };
}

function toneColor(profile, tone) {
  if (tone === 'accent') return profile.accent;
  if (tone === 'positive') return profile.accent2;
  if (tone === 'warning') return profile.chartTreatment.series[2] || profile.accent2;
  if (tone === 'critical') return profile.chartTreatment.series[3] || profile.accent;
  if (tone === 'inverse') return '#ffffff';
  if (tone === 'muted') return profile.muted;
  return profile.ink;
}

function chartColor(profile, index) {
  const series = profile.chartTreatment.series;
  return series[index % series.length] || profile.accent;
}

function normalizeChartData(source) {
  if (!Array.isArray(source)) return [];
  return source.map((item, index) => {
    if (typeof item === 'number') return { label: String(index + 1), value: Number.isFinite(item) ? item : 0 };
    const value = Number(item?.value);
    return {
      sourceId: plainText(item?.sourceId),
      label: plainText(item?.label ?? item?.name ?? index + 1),
      value: Number.isFinite(value) ? value : 0,
      displayValue: plainText(item?.displayValue),
      unit: plainText(item?.unit),
    };
  });
}

function formatChartDatum(item) {
  const display = item.displayValue || formatChartValue(item.value);
  if (!item.unit || display.includes(item.unit)) return display;
  return `${display}${/^[%‰°℃℉]/.test(item.unit) ? '' : ' '}${item.unit}`;
}

function normalizeListItem(item) {
  if (typeof item === 'string' || typeof item === 'number') {
    return { title: plainText(item), body: '' };
  }
  return {
    title: plainText(item?.title),
    body: plainText(item?.body),
  };
}

function safeMediaSource(value) {
  const source = plainText(value).trim();
  if (!source || /^(?:javascript|vbscript):/i.test(source)) return '';
  if (/^data:/i.test(source) && !/^data:(?:image|video)\//i.test(source)) return '';
  return source;
}

function editablePath(element, index, slot) {
  const id = String(element?.id || `element-${index + 1}`).replace(/[^a-zA-Z0-9_-]/g, '-');
  return `composition.${id}.${slot}`;
}

function truncateLabel(value) {
  const text = plainText(value);
  return text.length > 10 ? `${text.slice(0, 9)}…` : text;
}

function formatChartValue(value) {
  return Number.isInteger(value) ? String(value) : Number(value).toFixed(1);
}

function plainText(value) {
  if (value == null) return '';
  if (typeof value === 'string' || typeof value === 'number') return String(value);
  return '';
}

function clampInteger(value, min, max, fallback) {
  const number = Math.round(Number(value));
  if (!Number.isFinite(number)) return fallback;
  return Math.max(min, Math.min(max, number));
}

export default BespokeSlide;

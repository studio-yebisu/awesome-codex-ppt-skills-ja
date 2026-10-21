#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <deck.html>" >&2
  exit 2
fi

deck="$1"

if [[ ! -f "$deck" ]]; then
  echo "Deck not found: $deck" >&2
  exit 2
fi

perl -0ne '
  my $file = $_;
  my @slides = split(/<section\b/i, $_);
  shift @slides;
  my $failed = 0;
  my $i = 0;
  if ($file =~ /<(script|link|img|source|video|audio|iframe)\b[^>]*(src|href)=["\x27]https?:\/\//i
      || $file =~ /@import\s+(url\()?["\x27]?https?:\/\//i
      || $file =~ /url\(["\x27]?https?:\/\//i) {
    print STDERR "Quality check failed: deck contains a remote runtime, stylesheet, image, font, or media reference. Use local or embedded assets only.\n";
    $failed = 1;
  }
  my $component_re = qr/
    table|metric-strip|column-chart|ranked-bars|chart-block|heatmap|
    comparison-table|weighted-scorecard|sensitivity-grid|portfolio-prioritization-matrix|raci-governance-grid|outcome-support|process-flow|phase-roadmap|
    numbered-list-grid|decision-log|pros-cons-table|filter-cascade|
    framework-map|risk-matrix|range-competency-chart|range-comparison-plot|
    dot-scale-comparison|pie-chart|donut-chart|stacked-bars|scatter-plot|
    quote-insight|quote-large|quote-small|quote-grid|dense-list|callout|card-grid|card\b|
    quadrant-matrix|waterfall|roadmap|timeline|stage-gate|value-chain|
    funnel-steps|loop-cycle|cycle-flow|cascading-flow|decision-flowchart|fishbone-cause-effect|
    vertical-process-takeaway|process-deep-dive|triangle-steps|screen-filter-grid|
    journey-map|journey-arc|horizon-curve|gantt-workplan|status-table|wide-data-table|
    stair-step-timeline|journey-wave|calendar-workplan|schedule-list|
    contents-card-grid|six-column-list|milestone-track|pyramid-stack|
    conversion-list|story-block-list|step-explanation-strip|icon-outcome-grid|
    cause-effect|diverging-textboxes|from-to-multi|compass-choice|
    profile|contact-card|contact-roster|contact-network|
    line-chart|combo-chart|paired-bars|likert-bars|waterfall-bridge|checkmark-bar-table|
    ranked-evidence-table|driver-recap-columns|matrix-table|issue-tree|iceberg-model|
    capability-coverage-map|chevron-process-ribbon|swimlane-process-map|customer-journey-loop|
    input-process-output-layers|phase-meeting-plan|team-wall|bio-card-grid|
    competency-gap-range-table|tornado-bars|stacked-waterfall-bridge|
    part-to-whole-comparison|donut-explanation|small-multiples-chart|cohort-retention-grid|
    distribution-plot|variance-bridge-table|option-funnel-scorecard|tradeoff-frontier|
    scenario-comparison-table|assumption-register-table|system-context-map|dependency-map|
    sequence-interaction-flow|architecture-option-comparison|stakeholder-map|
    decision-capture-board|workshop-breakout-synthesis
  /x;
  my $visual_re = qr/
    visual-architecture-stack|visual-operating-system|visual-market-map|visual-value-bridge|
    visual-risk-control|visual-customer-journey|visual-team-network|visual-data-flywheel
  /x;
  for my $slide (@slides) {
    $i++;
    next unless $slide =~ /class=["][^"]*\bslide\b/i;
    next if $slide =~ /data-allow-divider=["]true["]/i;
    next if $slide =~ /class=["][^"]*\b(cover|default-ending)\b/i;
    next if $slide =~ /data-title=["][^"]*(cover|closing|ending|thank you)["]/i;
    my $plain = $slide;
    $plain =~ s/<script\b.*?<\/script>//gis;
    $plain =~ s/<style\b.*?<\/style>//gis;
    $plain =~ s/<[^>]+>/ /g;
    $plain =~ s/\s+/ /g;
    my $has_component = $slide =~ /class=["][^"]*($component_re)[^"]*["]/i;
    my $has_visual = $slide =~ /class=["][^"]*($visual_re)[^"]*["]/i;
    my $title = "";
    if ($slide =~ /data-title=["\x27]([^"\x27]+)["\x27]/i) {
      $title = $1;
    } elsif ($slide =~ /<h[12]\b[^>]*>(.*?)<\/h[12]>/is) {
      $title = $1;
      $title =~ s/<[^>]+>/ /g;
      $title =~ s/\s+/ /g;
      $title =~ s/^\s+|\s+$//g;
    }
    if ($title =~ /^(overview|analysis|findings|data|chart|discussion|market overview|cost analysis)$/i) {
      print STDERR "Quality check failed: slide $i uses a generic body-slide title \"$title\". Use an answer-first message title.\n";
      $failed = 1;
    }
    my $is_sectionish = $slide =~ /data-title=["][^"]*section/i
      || $plain =~ /\bSection\s*\d+/i
      || $plain =~ /数据支撑|基本面分析|板块与行业分析|行业分析|Section\s+/i;
    if ($has_visual && !$has_component && $slide !~ /data-allow-visual=["]true["]/i) {
      print STDERR "Quality check failed: slide $i uses a visual primitive without an evidence/component structure. Add a real component, remove the visual, or mark a deliberate exception with data-allow-visual=\"true\".\n";
      $failed = 1;
    }
    if (($is_sectionish || length($plain) < 220) && !$has_component) {
      print STDERR "Quality check failed: slide $i has no evidence/component structure. Add a real component or mark an intentional divider with data-allow-divider=\"true\".\n";
      $failed = 1;
    }
  }
  exit($failed ? 1 : 0);
' "$deck"

echo "Deck quality check passed: $deck"

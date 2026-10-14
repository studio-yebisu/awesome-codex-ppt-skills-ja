import * as zod from 'zod';
import { z } from 'zod';
import * as zod_v4_core from 'zod/v4/core';
export { D as DecodedImageSize, P as PptwisePlatform, R as RasterizedImage, i as installPlatform } from './registry-C9YsvcP8.js';

declare const VERSION = "0.44.0";

/** Error class thrown by pptwise's public API surface (validation, rendering, export). */
declare class PptwiseError extends Error {
}

declare const STRATEGY_VALUES: readonly ["pyramid", "storytelling", "instructional", "showcase", "briefing"];
declare const PACING_VALUES: readonly ["dense", "balanced", "spacious"];
declare const AUDIENCE_VALUES: readonly ["executive", "technical", "customer", "public"];
/**
 * The complete page-kind vocabulary for content slides. A kind is the
 * semantic posture shared by a spec and a theme menu. It is not a layout,
 * pacing hint, component type, or inferred property of filled content.
 */
declare const KIND_VALUES: readonly ["points", "list", "comparison", "process", "data", "photo", "statement", "quote", "fact", "evidence", "hierarchy"];

/**
 * The v5 IR schema root: theme/meta/assets/brand/branding/footer/background/slide/narrative
 * and the top-level `PptxIRSchema` a deck document parses against
 * (`parsePptxIR`). Versions 1 through 4 are rejected at this boundary.
 *
 * **The `ComponentSchema` union below is a pure aggregator (src domain reorg
 * wave 2, spec §4.3), same discipline as `src/layouts/registry.ts`'s T1d
 * precedent.** Every one of the component schemas used to live here as a
 * literal `z.object({...})` entry directly inside the `discriminatedUnion`
 * array. Each now lives in its own `src/ir/components/<name>.ts` domain file
 * instead (schema + field aliases + render-trait declaration together, spec
 * §4.1) — imported below and referenced by name, in the exact union position
 * its literal used to occupy, so "take one component away whole" is a
 * single-file operation instead of an edit split across this file,
 * `field-aliases.ts`, and `component-traits.ts`. This file's own job for
 * components is now purely computational: import every component schema, construct
 * `ComponentSchema` via `z.discriminatedUnion`, and derive `COMPONENT_TYPES`
 * from the result — never a hand-copied literal, never a re-export relay. A
 * handful of schema fragments genuinely shared by ≥2 components (only the
 * icon-name enum, as of this wave) live in `src/ir/components/shared.ts`
 * instead of any one domain file; every other named sub-schema that reads as
 * "shared" at a glance (e.g. `GanttItemSchema`, `PestQuadrantSchema`,
 * `SankeyNodeSchema`/`SankeyLinkSchema`) turned out to be single-consumer and
 * moved into its own component's domain file with it.
 *
 * The rest of this module — everything outside the `// ── Components` section
 * — is unrelated to the component-domain split and was never in its scope:
 * background/theme/meta/assets/brand/branding/slide/narrative and the top-level
 * `PptxIRSchema` are genuinely this file's own content, not aggregated from
 * elsewhere.
 */

declare const BUILTIN_THEME_IDS: readonly ["brief", "bulletin", "thesis", "ledger", "rally", "homeroom", "ink", "terminal", "runway", "journal", "luxe", "clinic", "almanac", "ember", "vermilion", "crayon", "museum", "stage", "lecture", "swiss", "memo", "proposal", "profile", "recap"];
declare const BackgroundSpecSchema: z.ZodDiscriminatedUnion<[z.ZodObject<{
    kind: z.ZodLiteral<"color">;
    value: z.ZodString;
}, z.core.$strict>, z.ZodObject<{
    kind: z.ZodLiteral<"gradient">;
    from: z.ZodString;
    to: z.ZodString;
    direction: z.ZodOptional<z.ZodEnum<{
        tb: "tb";
        lr: "lr";
        diagonal: "diagonal";
    }>>;
}, z.core.$strict>, z.ZodObject<{
    kind: z.ZodLiteral<"asset">;
    asset_id: z.ZodString;
    overlay: z.ZodOptional<z.ZodObject<{
        color: z.ZodString;
        opacity: z.ZodNumber;
    }, z.core.$strict>>;
    fit: z.ZodOptional<z.ZodEnum<{
        cover: "cover";
        contain: "contain";
    }>>;
}, z.core.$strict>], "kind">;
/**
 * Brand (logical slide-master) config: branding behavior owned by a theme.
 * W1 scope was exactly the two flags migrated from the old theme-manifest footer flags;
 * the ink v3 redesign (2026-08-18) added a third, since retired.
 * Single source of truth: the TS type is inferred, never hand-written.
 *
 * The live switches are independent, not a ladder: a theme may set any
 * combination, and each names exactly one piece of brand footer.
 */
declare const BrandConfigSchema: z.ZodObject<{
    suppressFooterOnCardContent: z.ZodOptional<z.ZodBoolean>;
    suppressFooterRule: z.ZodOptional<z.ZodBoolean>;
    suppressFooterMeta: z.ZodOptional<z.ZodBoolean>;
}, z.core.$strict>;
type BrandConfig = z.infer<typeof BrandConfigSchema>;
declare const ThemeSchema: z.ZodObject<{
    id: z.ZodString;
}, z.core.$strict>;
declare const MetaSchema: z.ZodObject<{
    organization: z.ZodOptional<z.ZodString>;
    authors: z.ZodOptional<z.ZodArray<z.ZodObject<{
        name: z.ZodString;
        role: z.ZodOptional<z.ZodString>;
        org: z.ZodOptional<z.ZodString>;
    }, z.core.$strict>>>;
    date: z.ZodOptional<z.ZodString>;
    version: z.ZodOptional<z.ZodString>;
    confidentiality: z.ZodOptional<z.ZodEnum<{
        public: "public";
        internal: "internal";
        confidential: "confidential";
        restricted: "restricted";
    }>>;
    classification: z.ZodOptional<z.ZodString>;
    contact: z.ZodOptional<z.ZodObject<{
        name: z.ZodOptional<z.ZodString>;
        email: z.ZodOptional<z.ZodString>;
        phone: z.ZodOptional<z.ZodString>;
        website: z.ZodOptional<z.ZodString>;
    }, z.core.$strict>>;
    copyright: z.ZodOptional<z.ZodString>;
    animation: z.ZodOptional<z.ZodObject<{
        transition: z.ZodOptional<z.ZodEnum<{
            push: "push";
            none: "none";
            fade: "fade";
            wipe: "wipe";
        }>>;
        elements: z.ZodOptional<z.ZodEnum<{
            none: "none";
            auto: "auto";
        }>>;
    }, z.core.$strict>>;
}, z.core.$strict>;
declare const AssetsSchema: z.ZodObject<{
    images: z.ZodDefault<z.ZodRecord<z.ZodString, z.ZodObject<{
        src: z.ZodString;
        alt: z.ZodOptional<z.ZodString>;
        error: z.ZodOptional<z.ZodString>;
    }, z.core.$strict>>>;
}, z.core.$strict>;
declare const ComponentSchema: z.ZodDiscriminatedUnion<[z.ZodObject<{
    type: z.ZodLiteral<"bullets">;
    items: z.ZodArray<z.ZodString>;
    style: z.ZodOptional<z.ZodEnum<{
        default: "default";
        checklist: "checklist";
        numbered: "numbered";
        plain: "plain";
        divided: "divided";
    }>>;
}, z.core.$strict>, z.ZodObject<{
    type: z.ZodLiteral<"paragraph">;
    text: z.ZodString;
}, z.core.$strict>, z.ZodObject<{
    type: z.ZodLiteral<"blockquote">;
    text: z.ZodString;
    attribution: z.ZodOptional<z.ZodString>;
}, z.core.$strict>, z.ZodObject<{
    type: z.ZodLiteral<"callout">;
    variant: z.ZodEnum<{
        info: "info";
        warn: "warn";
        tip: "tip";
    }>;
    title: z.ZodOptional<z.ZodString>;
    text: z.ZodString;
    icon: z.ZodOptional<z.ZodEnum<{
        [x: string]: string;
    }>>;
    tag: z.ZodOptional<z.ZodObject<{
        text: z.ZodString;
        quiet: z.ZodOptional<z.ZodBoolean>;
        evidence: z.ZodOptional<z.ZodEnum<{
            label: "label";
            draft: "draft";
            trial: "trial";
            company: "company";
            press: "press";
            official: "official";
            registry: "registry";
            preprint: "preprint";
        }>>;
        settled: z.ZodOptional<z.ZodBoolean>;
        tone: z.ZodOptional<z.ZodEnum<{
            danger: "danger";
            warning: "warning";
            success: "success";
        }>>;
        basis: z.ZodOptional<z.ZodEnum<{
            law: "law";
            estimate: "estimate";
            pending: "pending";
            proposal: "proposal";
        }>>;
    }, z.core.$strict>>;
}, z.core.$strict>, z.ZodObject<{
    type: z.ZodLiteral<"code">;
    language: z.ZodString;
    code: z.ZodString;
    title: z.ZodOptional<z.ZodString>;
    highlight_lines: z.ZodOptional<z.ZodArray<z.ZodNumber>>;
}, z.core.$strict>, z.ZodObject<{
    type: z.ZodLiteral<"kpi_cards">;
    items: z.ZodArray<z.ZodObject<{
        value: z.ZodString;
        unit: z.ZodOptional<z.ZodString>;
        label: z.ZodString;
        note: z.ZodOptional<z.ZodString>;
        tag: z.ZodOptional<z.ZodObject<{
            text: z.ZodString;
            quiet: z.ZodOptional<z.ZodBoolean>;
            evidence: z.ZodOptional<z.ZodEnum<{
                label: "label";
                draft: "draft";
                trial: "trial";
                company: "company";
                press: "press";
                official: "official";
                registry: "registry";
                preprint: "preprint";
            }>>;
            settled: z.ZodOptional<z.ZodBoolean>;
            tone: z.ZodOptional<z.ZodEnum<{
                danger: "danger";
                warning: "warning";
                success: "success";
            }>>;
            basis: z.ZodOptional<z.ZodEnum<{
                law: "law";
                estimate: "estimate";
                pending: "pending";
                proposal: "proposal";
            }>>;
        }, z.core.$strict>>;
        delta: z.ZodOptional<z.ZodEnum<{
            flat: "flat";
            up: "up";
            down: "down";
        }>>;
        delta_good: z.ZodOptional<z.ZodBoolean>;
        icon: z.ZodOptional<z.ZodEnum<{
            [x: string]: string;
        }>>;
        tone: z.ZodOptional<z.ZodEnum<{
            danger: "danger";
            warning: "warning";
            success: "success";
        }>>;
        source: z.ZodOptional<z.ZodString>;
    }, z.core.$strict>>;
}, z.core.$strict>, z.ZodObject<{
    type: z.ZodLiteral<"chart">;
    title: z.ZodOptional<z.ZodString>;
    chart_type: z.ZodEnum<{
        line: "line";
        donut: "donut";
        dumbbell: "dumbbell";
        funnel: "funnel";
        gauge: "gauge";
        bar: "bar";
        stacked: "stacked";
        percent_stacked: "percent_stacked";
        pie: "pie";
        area: "area";
        combo: "combo";
        scatter: "scatter";
    }>;
    direction: z.ZodOptional<z.ZodEnum<{
        horizontal: "horizontal";
        vertical: "vertical";
    }>>;
    style: z.ZodOptional<z.ZodEnum<{
        donut: "donut";
    }>>;
    center_total: z.ZodOptional<z.ZodBoolean>;
    gauge: z.ZodOptional<z.ZodObject<{
        min: z.ZodOptional<z.ZodNumber>;
        max: z.ZodOptional<z.ZodNumber>;
    }, z.core.$strict>>;
    axes: z.ZodOptional<z.ZodObject<{
        x_title: z.ZodOptional<z.ZodString>;
        y_title: z.ZodOptional<z.ZodString>;
        x_unit: z.ZodOptional<z.ZodString>;
        y_unit: z.ZodOptional<z.ZodString>;
        y2_title: z.ZodOptional<z.ZodString>;
        y2_unit: z.ZodOptional<z.ZodString>;
        show_grid: z.ZodOptional<z.ZodBoolean>;
    }, z.core.$strict>>;
    tag: z.ZodOptional<z.ZodObject<{
        text: z.ZodString;
        quiet: z.ZodOptional<z.ZodBoolean>;
        evidence: z.ZodOptional<z.ZodEnum<{
            label: "label";
            draft: "draft";
            trial: "trial";
            company: "company";
            press: "press";
            official: "official";
            registry: "registry";
            preprint: "preprint";
        }>>;
        settled: z.ZodOptional<z.ZodBoolean>;
        tone: z.ZodOptional<z.ZodEnum<{
            danger: "danger";
            warning: "warning";
            success: "success";
        }>>;
        basis: z.ZodOptional<z.ZodEnum<{
            law: "law";
            estimate: "estimate";
            pending: "pending";
            proposal: "proposal";
        }>>;
    }, z.core.$strict>>;
    changes: z.ZodOptional<z.ZodArray<z.ZodObject<{
        from: z.ZodString;
        to: z.ZodString;
        at: z.ZodOptional<z.ZodString>;
    }, z.core.$strict>>>;
    bands: z.ZodOptional<z.ZodArray<z.ZodObject<{
        from: z.ZodNumber;
        to: z.ZodNumber;
        label: z.ZodOptional<z.ZodString>;
    }, z.core.$strict>>>;
    emphasis_label: z.ZodOptional<z.ZodString>;
    reference: z.ZodOptional<z.ZodObject<{
        value: z.ZodNumber;
        label: z.ZodString;
    }, z.core.$strict>>;
    markers: z.ZodOptional<z.ZodArray<z.ZodObject<{
        before: z.ZodString;
        label: z.ZodString;
    }, z.core.$strict>>>;
    gaps: z.ZodOptional<z.ZodArray<z.ZodObject<{
        after: z.ZodString;
        x: z.ZodString;
        label: z.ZodString;
    }, z.core.$strict>>>;
    series: z.ZodArray<z.ZodObject<{
        name: z.ZodString;
        data: z.ZodArray<z.ZodObject<{
            x: z.ZodUnion<readonly [z.ZodString, z.ZodNumber]>;
            y: z.ZodNumber;
            size: z.ZodOptional<z.ZodNumber>;
            status: z.ZodOptional<z.ZodEnum<{
                target: "target";
                estimate: "estimate";
                forecast: "forecast";
            }>>;
            emphasis: z.ZodOptional<z.ZodBoolean>;
            note: z.ZodOptional<z.ZodString>;
            icon: z.ZodOptional<z.ZodEnum<{
                [x: string]: string;
            }>>;
            upper: z.ZodOptional<z.ZodNumber>;
        }, z.core.$strict>>;
        plot: z.ZodOptional<z.ZodEnum<{
            line: "line";
            bar: "bar";
        }>>;
        axis: z.ZodOptional<z.ZodEnum<{
            left: "left";
            right: "right";
        }>>;
        emphasis: z.ZodOptional<z.ZodBoolean>;
        steps: z.ZodOptional<z.ZodBoolean>;
        tone: z.ZodOptional<z.ZodEnum<{
            danger: "danger";
            warning: "warning";
            success: "success";
        }>>;
    }, z.core.$strict>>;
}, z.core.$strict>, z.ZodObject<{
    type: z.ZodLiteral<"flowchart">;
    nodes: z.ZodArray<z.ZodObject<{
        id: z.ZodString;
        label: z.ZodString;
        kind: z.ZodOptional<z.ZodEnum<{
            rect: "rect";
            diamond: "diamond";
            round: "round";
        }>>;
    }, z.core.$strict>>;
    edges: z.ZodArray<z.ZodObject<{
        from: z.ZodString;
        to: z.ZodString;
        label: z.ZodOptional<z.ZodString>;
    }, z.core.$strict>>;
    direction: z.ZodOptional<z.ZodEnum<{
        TB: "TB";
        TD: "TD";
        BT: "BT";
        LR: "LR";
        RL: "RL";
    }>>;
}, z.core.$strict>, z.ZodObject<{
    type: z.ZodLiteral<"architecture">;
    layers: z.ZodArray<z.ZodObject<{
        title: z.ZodString;
        items: z.ZodArray<z.ZodString>;
    }, z.core.$strict>>;
    direction: z.ZodOptional<z.ZodEnum<{
        top_down: "top_down";
        bottom_up: "bottom_up";
    }>>;
}, z.core.$strict>, z.ZodObject<{
    type: z.ZodLiteral<"timeline">;
    title: z.ZodOptional<z.ZodString>;
    layout: z.ZodOptional<z.ZodEnum<{
        horizontal: "horizontal";
        vertical: "vertical";
    }>>;
    lanes: z.ZodOptional<z.ZodArray<z.ZodString>>;
    periods: z.ZodOptional<z.ZodArray<z.ZodObject<{
        from: z.ZodString;
        to: z.ZodString;
        label: z.ZodString;
        basis: z.ZodOptional<z.ZodEnum<{
            law: "law";
            estimate: "estimate";
            pending: "pending";
            proposal: "proposal";
        }>>;
    }, z.core.$strict>>>;
    milestones: z.ZodArray<z.ZodObject<{
        date: z.ZodString;
        title: z.ZodString;
        desc: z.ZodOptional<z.ZodString>;
        highlight: z.ZodOptional<z.ZodBoolean>;
        icon: z.ZodOptional<z.ZodEnum<{
            [x: string]: string;
        }>>;
        tone: z.ZodOptional<z.ZodEnum<{
            danger: "danger";
            warning: "warning";
            success: "success";
        }>>;
        status: z.ZodOptional<z.ZodEnum<{
            pending: "pending";
        }>>;
        tag: z.ZodOptional<z.ZodObject<{
            text: z.ZodString;
            quiet: z.ZodOptional<z.ZodBoolean>;
            evidence: z.ZodOptional<z.ZodEnum<{
                label: "label";
                draft: "draft";
                trial: "trial";
                company: "company";
                press: "press";
                official: "official";
                registry: "registry";
                preprint: "preprint";
            }>>;
            settled: z.ZodOptional<z.ZodBoolean>;
            tone: z.ZodOptional<z.ZodEnum<{
                danger: "danger";
                warning: "warning";
                success: "success";
            }>>;
            basis: z.ZodOptional<z.ZodEnum<{
                law: "law";
                estimate: "estimate";
                pending: "pending";
                proposal: "proposal";
            }>>;
        }, z.core.$strict>>;
        source: z.ZodOptional<z.ZodString>;
        lane: z.ZodOptional<z.ZodString>;
    }, z.core.$strict>>;
}, z.core.$strict>, z.ZodObject<{
    type: z.ZodLiteral<"comparison">;
    title: z.ZodOptional<z.ZodString>;
    columns: z.ZodArray<z.ZodString>;
    label_column: z.ZodOptional<z.ZodString>;
    rows: z.ZodArray<z.ZodObject<{
        label: z.ZodString;
        cells: z.ZodArray<z.ZodString>;
        icon: z.ZodOptional<z.ZodEnum<{
            [x: string]: string;
        }>>;
        tag: z.ZodOptional<z.ZodObject<{
            text: z.ZodString;
            quiet: z.ZodOptional<z.ZodBoolean>;
            evidence: z.ZodOptional<z.ZodEnum<{
                label: "label";
                draft: "draft";
                trial: "trial";
                company: "company";
                press: "press";
                official: "official";
                registry: "registry";
                preprint: "preprint";
            }>>;
            settled: z.ZodOptional<z.ZodBoolean>;
            tone: z.ZodOptional<z.ZodEnum<{
                danger: "danger";
                warning: "warning";
                success: "success";
            }>>;
            basis: z.ZodOptional<z.ZodEnum<{
                law: "law";
                estimate: "estimate";
                pending: "pending";
                proposal: "proposal";
            }>>;
        }, z.core.$strict>>;
        emphasis: z.ZodOptional<z.ZodBoolean>;
    }, z.core.$strict>>;
    tag_column: z.ZodOptional<z.ZodString>;
    recommended: z.ZodOptional<z.ZodNumber>;
    recommended_label: z.ZodOptional<z.ZodString>;
}, z.core.$strict>, z.ZodObject<{
    type: z.ZodLiteral<"icon_cards">;
    title: z.ZodOptional<z.ZodString>;
    items: z.ZodArray<z.ZodObject<{
        icon: z.ZodEnum<{
            [x: string]: string;
        }>;
        title: z.ZodString;
        text: z.ZodString;
        tag: z.ZodOptional<z.ZodObject<{
            text: z.ZodString;
            quiet: z.ZodOptional<z.ZodBoolean>;
            evidence: z.ZodOptional<z.ZodEnum<{
                label: "label";
                draft: "draft";
                trial: "trial";
                company: "company";
                press: "press";
                official: "official";
                registry: "registry";
                preprint: "preprint";
            }>>;
            settled: z.ZodOptional<z.ZodBoolean>;
            tone: z.ZodOptional<z.ZodEnum<{
                danger: "danger";
                warning: "warning";
                success: "success";
            }>>;
            basis: z.ZodOptional<z.ZodEnum<{
                law: "law";
                estimate: "estimate";
                pending: "pending";
                proposal: "proposal";
            }>>;
        }, z.core.$strict>>;
        tone: z.ZodOptional<z.ZodEnum<{
            danger: "danger";
            warning: "warning";
            success: "success";
        }>>;
    }, z.core.$strict>>;
}, z.core.$strict>, z.ZodObject<{
    type: z.ZodLiteral<"row_cards">;
    items: z.ZodArray<z.ZodObject<{
        icon: z.ZodOptional<z.ZodEnum<{
            [x: string]: string;
        }>>;
        title: z.ZodString;
        text: z.ZodOptional<z.ZodString>;
        sub: z.ZodOptional<z.ZodString>;
        highlight: z.ZodOptional<z.ZodBoolean>;
        tone: z.ZodOptional<z.ZodEnum<{
            danger: "danger";
            warning: "warning";
            success: "success";
        }>>;
    }, z.core.$strict>>;
}, z.core.$strict>, z.ZodObject<{
    type: z.ZodLiteral<"steps">;
    items: z.ZodArray<z.ZodObject<{
        title: z.ZodString;
        text: z.ZodString;
        icon: z.ZodOptional<z.ZodEnum<{
            [x: string]: string;
        }>>;
        tone: z.ZodOptional<z.ZodEnum<{
            danger: "danger";
            warning: "warning";
            success: "success";
        }>>;
    }, z.core.$strict>>;
}, z.core.$strict>, z.ZodObject<{
    type: z.ZodLiteral<"rings">;
    items: z.ZodArray<z.ZodObject<{
        label: z.ZodString;
        desc: z.ZodOptional<z.ZodString>;
    }, z.core.$strict>>;
}, z.core.$strict>, z.ZodObject<{
    type: z.ZodLiteral<"numbered_cards">;
    items: z.ZodArray<z.ZodObject<{
        title: z.ZodString;
        text: z.ZodOptional<z.ZodString>;
        sub: z.ZodOptional<z.ZodString>;
        icon: z.ZodOptional<z.ZodEnum<{
            [x: string]: string;
        }>>;
        emphasis: z.ZodOptional<z.ZodBoolean>;
    }, z.core.$strict>>;
}, z.core.$strict>, z.ZodObject<{
    type: z.ZodLiteral<"roadmap">;
    items: z.ZodArray<z.ZodObject<{
        title: z.ZodString;
        period: z.ZodOptional<z.ZodString>;
        icon: z.ZodOptional<z.ZodEnum<{
            [x: string]: string;
        }>>;
        rows: z.ZodOptional<z.ZodArray<z.ZodObject<{
            label: z.ZodString;
            value: z.ZodString;
            basis: z.ZodOptional<z.ZodEnum<{
                law: "law";
                estimate: "estimate";
                pending: "pending";
                proposal: "proposal";
            }>>;
        }, z.core.$strict>>>;
        duration: z.ZodOptional<z.ZodNumber>;
        checkpoint: z.ZodOptional<z.ZodString>;
        points: z.ZodOptional<z.ZodArray<z.ZodString>>;
        emphasis: z.ZodOptional<z.ZodBoolean>;
    }, z.core.$strict>>;
    duration_unit: z.ZodOptional<z.ZodString>;
}, z.core.$strict>, z.ZodObject<{
    type: z.ZodLiteral<"matrix">;
    title: z.ZodOptional<z.ZodString>;
    x_title: z.ZodOptional<z.ZodString>;
    y_title: z.ZodOptional<z.ZodString>;
    cols: z.ZodNumber;
    columns: z.ZodOptional<z.ZodArray<z.ZodString>>;
    rows: z.ZodOptional<z.ZodArray<z.ZodObject<{
        label: z.ZodString;
        icon: z.ZodOptional<z.ZodEnum<{
            [x: string]: string;
        }>>;
    }, z.core.$strict>>>;
    items: z.ZodArray<z.ZodObject<{
        title: z.ZodString;
        tag: z.ZodOptional<z.ZodString>;
        tone: z.ZodOptional<z.ZodEnum<{
            info: "info";
            neutral: "neutral";
            accent: "accent";
        }>>;
        empty: z.ZodOptional<z.ZodBoolean>;
    }, z.core.$strict>>;
}, z.core.$strict>, z.ZodObject<{
    type: z.ZodLiteral<"insight_panel">;
    title: z.ZodString;
    icon: z.ZodOptional<z.ZodEnum<{
        [x: string]: string;
    }>>;
    rows: z.ZodArray<z.ZodObject<{
        label: z.ZodString;
        text: z.ZodString;
    }, z.core.$strict>>;
    footnote: z.ZodOptional<z.ZodString>;
}, z.core.$strict>, z.ZodObject<{
    type: z.ZodLiteral<"verdict_banner">;
    text: z.ZodString;
    tone: z.ZodEnum<{
        warning: "warning";
        positive: "positive";
        neutral: "neutral";
    }>;
    icon: z.ZodOptional<z.ZodEnum<{
        [x: string]: string;
    }>>;
}, z.core.$strict>, z.ZodObject<{
    type: z.ZodLiteral<"image">;
    asset_id: z.ZodString;
    caption: z.ZodOptional<z.ZodString>;
    fit: z.ZodDefault<z.ZodEnum<{
        cover: "cover";
        contain: "contain";
    }>>;
    crop: z.ZodOptional<z.ZodArray<z.ZodNumber>>;
}, z.core.$strict>, z.ZodObject<{
    type: z.ZodLiteral<"image_grid">;
    items: z.ZodArray<z.ZodObject<{
        asset_id: z.ZodString;
        caption: z.ZodOptional<z.ZodString>;
        icon: z.ZodOptional<z.ZodEnum<{
            [x: string]: string;
        }>>;
        tag: z.ZodOptional<z.ZodObject<{
            text: z.ZodString;
            quiet: z.ZodOptional<z.ZodBoolean>;
            evidence: z.ZodOptional<z.ZodEnum<{
                label: "label";
                draft: "draft";
                trial: "trial";
                company: "company";
                press: "press";
                official: "official";
                registry: "registry";
                preprint: "preprint";
            }>>;
            settled: z.ZodOptional<z.ZodBoolean>;
            tone: z.ZodOptional<z.ZodEnum<{
                danger: "danger";
                warning: "warning";
                success: "success";
            }>>;
            basis: z.ZodOptional<z.ZodEnum<{
                law: "law";
                estimate: "estimate";
                pending: "pending";
                proposal: "proposal";
            }>>;
        }, z.core.$strict>>;
        crop: z.ZodOptional<z.ZodArray<z.ZodNumber>>;
    }, z.core.$strict>>;
    emphasis: z.ZodOptional<z.ZodEnum<{
        none: "none";
        first: "first";
    }>>;
}, z.core.$strict>, z.ZodObject<{
    type: z.ZodLiteral<"image_compare">;
    left: z.ZodObject<{
        asset_id: z.ZodString;
        label: z.ZodString;
    }, z.core.$strict>;
    right: z.ZodObject<{
        asset_id: z.ZodString;
        label: z.ZodString;
    }, z.core.$strict>;
    style: z.ZodOptional<z.ZodEnum<{
        vs: "vs";
        before_after: "before_after";
    }>>;
}, z.core.$strict>, z.ZodObject<{
    type: z.ZodLiteral<"logo_wall">;
    title: z.ZodOptional<z.ZodString>;
    items: z.ZodArray<z.ZodObject<{
        name: z.ZodString;
        asset_id: z.ZodOptional<z.ZodString>;
    }, z.core.$strict>>;
}, z.core.$strict>, z.ZodObject<{
    type: z.ZodLiteral<"product_cards">;
    items: z.ZodArray<z.ZodObject<{
        asset_id: z.ZodString;
        name: z.ZodString;
        note: z.ZodOptional<z.ZodString>;
        price: z.ZodOptional<z.ZodString>;
        price_unit: z.ZodOptional<z.ZodString>;
        featured: z.ZodOptional<z.ZodLiteral<true>>;
    }, z.core.$strict>>;
}, z.core.$strict>, z.ZodObject<{
    type: z.ZodLiteral<"quote_wall">;
    quotes: z.ZodArray<z.ZodObject<{
        text: z.ZodString;
        name: z.ZodString;
        role: z.ZodOptional<z.ZodString>;
        featured: z.ZodOptional<z.ZodLiteral<true>>;
    }, z.core.$strict>>;
}, z.core.$strict>, z.ZodObject<{
    type: z.ZodLiteral<"swot">;
    strengths: z.ZodArray<z.ZodString>;
    weaknesses: z.ZodArray<z.ZodString>;
    opportunities: z.ZodArray<z.ZodString>;
    threats: z.ZodArray<z.ZodString>;
    labels: z.ZodOptional<z.ZodObject<{
        strengths: z.ZodOptional<z.ZodString>;
        weaknesses: z.ZodOptional<z.ZodString>;
        opportunities: z.ZodOptional<z.ZodString>;
        threats: z.ZodOptional<z.ZodString>;
    }, z.core.$strict>>;
}, z.core.$strict>, z.ZodObject<{
    type: z.ZodLiteral<"bmc">;
    key_partners: z.ZodArray<z.ZodString>;
    key_activities: z.ZodArray<z.ZodString>;
    key_resources: z.ZodArray<z.ZodString>;
    value_propositions: z.ZodArray<z.ZodString>;
    customer_relationships: z.ZodArray<z.ZodString>;
    channels: z.ZodArray<z.ZodString>;
    customer_segments: z.ZodArray<z.ZodString>;
    cost_structure: z.ZodArray<z.ZodString>;
    revenue_streams: z.ZodArray<z.ZodString>;
}, z.core.$strict>, z.ZodObject<{
    type: z.ZodLiteral<"waterfall">;
    title: z.ZodOptional<z.ZodString>;
    items: z.ZodArray<z.ZodObject<{
        label: z.ZodString;
        value: z.ZodNumber;
        kind: z.ZodOptional<z.ZodEnum<{
            delta: "delta";
            total: "total";
        }>>;
        note: z.ZodOptional<z.ZodString>;
        emphasis: z.ZodOptional<z.ZodBoolean>;
    }, z.core.$strict>>;
    unit: z.ZodOptional<z.ZodString>;
    emphasis_label: z.ZodOptional<z.ZodString>;
}, z.core.$strict>, z.ZodObject<{
    type: z.ZodLiteral<"gantt">;
    items: z.ZodArray<z.ZodObject<{
        label: z.ZodString;
        start: z.ZodNumber;
        end: z.ZodNumber;
        text: z.ZodOptional<z.ZodString>;
        emphasis: z.ZodOptional<z.ZodBoolean>;
        icon: z.ZodOptional<z.ZodEnum<{
            [x: string]: string;
        }>>;
        period: z.ZodOptional<z.ZodString>;
        basis: z.ZodOptional<z.ZodEnum<{
            law: "law";
            estimate: "estimate";
            pending: "pending";
            proposal: "proposal";
        }>>;
    }, z.core.$strict>>;
    axis_labels: z.ZodOptional<z.ZodArray<z.ZodString>>;
    range: z.ZodOptional<z.ZodObject<{
        from: z.ZodNumber;
        to: z.ZodNumber;
    }, z.core.$strict>>;
    milestones: z.ZodOptional<z.ZodArray<z.ZodObject<{
        at: z.ZodNumber;
        label: z.ZodString;
    }, z.core.$strict>>>;
    bands: z.ZodOptional<z.ZodArray<z.ZodObject<{
        from: z.ZodNumber;
        to: z.ZodNumber;
        label: z.ZodString;
    }, z.core.$strict>>>;
}, z.core.$strict>, z.ZodObject<{
    type: z.ZodLiteral<"pest">;
    political: z.ZodObject<{
        title: z.ZodOptional<z.ZodString>;
        items: z.ZodArray<z.ZodString>;
    }, z.core.$strict>;
    economic: z.ZodObject<{
        title: z.ZodOptional<z.ZodString>;
        items: z.ZodArray<z.ZodString>;
    }, z.core.$strict>;
    social: z.ZodObject<{
        title: z.ZodOptional<z.ZodString>;
        items: z.ZodArray<z.ZodString>;
    }, z.core.$strict>;
    technological: z.ZodObject<{
        title: z.ZodOptional<z.ZodString>;
        items: z.ZodArray<z.ZodString>;
    }, z.core.$strict>;
}, z.core.$strict>, z.ZodObject<{
    type: z.ZodLiteral<"five_forces">;
    rivalry: z.ZodObject<{
        label: z.ZodOptional<z.ZodString>;
        intensity: z.ZodOptional<z.ZodEnum<{
            low: "low";
            medium: "medium";
            high: "high";
        }>>;
        items: z.ZodArray<z.ZodString>;
    }, z.core.$strict>;
    new_entrants: z.ZodObject<{
        label: z.ZodOptional<z.ZodString>;
        intensity: z.ZodOptional<z.ZodEnum<{
            low: "low";
            medium: "medium";
            high: "high";
        }>>;
        items: z.ZodArray<z.ZodString>;
    }, z.core.$strict>;
    supplier_power: z.ZodObject<{
        label: z.ZodOptional<z.ZodString>;
        intensity: z.ZodOptional<z.ZodEnum<{
            low: "low";
            medium: "medium";
            high: "high";
        }>>;
        items: z.ZodArray<z.ZodString>;
    }, z.core.$strict>;
    buyer_power: z.ZodObject<{
        label: z.ZodOptional<z.ZodString>;
        intensity: z.ZodOptional<z.ZodEnum<{
            low: "low";
            medium: "medium";
            high: "high";
        }>>;
        items: z.ZodArray<z.ZodString>;
    }, z.core.$strict>;
    substitutes: z.ZodObject<{
        label: z.ZodOptional<z.ZodString>;
        intensity: z.ZodOptional<z.ZodEnum<{
            low: "low";
            medium: "medium";
            high: "high";
        }>>;
        items: z.ZodArray<z.ZodString>;
    }, z.core.$strict>;
}, z.core.$strict>, z.ZodObject<{
    type: z.ZodLiteral<"heatmap">;
    x_labels: z.ZodArray<z.ZodString>;
    y_labels: z.ZodArray<z.ZodString>;
    values: z.ZodArray<z.ZodArray<z.ZodNumber>>;
    domain: z.ZodOptional<z.ZodObject<{
        min: z.ZodNumber;
        max: z.ZodNumber;
    }, z.core.$strict>>;
    show_values: z.ZodOptional<z.ZodBoolean>;
    x_title: z.ZodOptional<z.ZodString>;
    y_title: z.ZodOptional<z.ZodString>;
    label_every: z.ZodOptional<z.ZodNumber>;
    steps: z.ZodOptional<z.ZodArray<z.ZodObject<{
        max: z.ZodOptional<z.ZodNumber>;
        label: z.ZodString;
        short: z.ZodOptional<z.ZodString>;
    }, z.core.$strict>>>;
    bands: z.ZodOptional<z.ZodArray<z.ZodObject<{
        from: z.ZodString;
        to: z.ZodString;
        label: z.ZodString;
        icon: z.ZodOptional<z.ZodEnum<{
            [x: string]: string;
        }>>;
    }, z.core.$strict>>>;
}, z.core.$strict>, z.ZodObject<{
    type: z.ZodLiteral<"sankey">;
    nodes: z.ZodArray<z.ZodObject<{
        id: z.ZodString;
        label: z.ZodString;
    }, z.core.$strict>>;
    links: z.ZodArray<z.ZodObject<{
        from: z.ZodString;
        to: z.ZodString;
        value: z.ZodNumber;
    }, z.core.$strict>>;
}, z.core.$strict>, z.ZodObject<{
    type: z.ZodLiteral<"data_table">;
    title: z.ZodOptional<z.ZodString>;
    columns: z.ZodArray<z.ZodObject<{
        key: z.ZodString;
        label: z.ZodString;
        align: z.ZodOptional<z.ZodEnum<{
            left: "left";
            right: "right";
            center: "center";
        }>>;
        emphasis: z.ZodOptional<z.ZodBoolean>;
        icon: z.ZodOptional<z.ZodEnum<{
            [x: string]: string;
        }>>;
    }, z.core.$strict>>;
    rows: z.ZodArray<z.ZodObject<{
        cells: z.ZodRecord<z.ZodString, z.ZodUnion<readonly [z.ZodString, z.ZodNumber]>>;
        emphasis: z.ZodOptional<z.ZodEnum<{
            highlight: "highlight";
            total: "total";
        }>>;
        icon: z.ZodOptional<z.ZodEnum<{
            [x: string]: string;
        }>>;
        tag: z.ZodOptional<z.ZodObject<{
            text: z.ZodString;
            quiet: z.ZodOptional<z.ZodBoolean>;
            evidence: z.ZodOptional<z.ZodEnum<{
                label: "label";
                draft: "draft";
                trial: "trial";
                company: "company";
                press: "press";
                official: "official";
                registry: "registry";
                preprint: "preprint";
            }>>;
            settled: z.ZodOptional<z.ZodBoolean>;
            tone: z.ZodOptional<z.ZodEnum<{
                danger: "danger";
                warning: "warning";
                success: "success";
            }>>;
            basis: z.ZodOptional<z.ZodEnum<{
                law: "law";
                estimate: "estimate";
                pending: "pending";
                proposal: "proposal";
            }>>;
        }, z.core.$strict>>;
    }, z.core.$strict>>;
    source: z.ZodOptional<z.ZodString>;
}, z.core.$strict>, z.ZodObject<{
    type: z.ZodLiteral<"device_mockup">;
    device: z.ZodEnum<{
        phone: "phone";
        browser: "browser";
    }>;
    asset_id: z.ZodString;
    caption: z.ZodOptional<z.ZodString>;
    url: z.ZodOptional<z.ZodString>;
}, z.core.$strict>, z.ZodObject<{
    type: z.ZodLiteral<"cycle">;
    title: z.ZodOptional<z.ZodString>;
    items: z.ZodArray<z.ZodObject<{
        label: z.ZodString;
        description: z.ZodOptional<z.ZodString>;
    }, z.core.$strict>>;
}, z.core.$strict>, z.ZodObject<{
    type: z.ZodLiteral<"people_cards">;
    title: z.ZodOptional<z.ZodString>;
    people: z.ZodArray<z.ZodObject<{
        name: z.ZodString;
        role: z.ZodOptional<z.ZodString>;
        org: z.ZodOptional<z.ZodString>;
    }, z.core.$strict>>;
}, z.core.$strict>, z.ZodObject<{
    type: z.ZodLiteral<"hub_spoke">;
    center: z.ZodString;
    items: z.ZodArray<z.ZodObject<{
        label: z.ZodString;
        description: z.ZodOptional<z.ZodString>;
    }, z.core.$strict>>;
}, z.core.$strict>, z.ZodObject<{
    type: z.ZodLiteral<"progress_donuts">;
    items: z.ZodArray<z.ZodObject<{
        value: z.ZodString;
        unit: z.ZodOptional<z.ZodString>;
        label: z.ZodString;
        icon: z.ZodOptional<z.ZodEnum<{
            [x: string]: string;
        }>>;
        source: z.ZodOptional<z.ZodString>;
        detail: z.ZodOptional<z.ZodString>;
        emphasis: z.ZodOptional<z.ZodBoolean>;
    }, z.core.$strict>>;
}, z.core.$strict>, z.ZodObject<{
    type: z.ZodLiteral<"staircase">;
    items: z.ZodArray<z.ZodObject<{
        title: z.ZodString;
        value: z.ZodString;
        unit: z.ZodOptional<z.ZodString>;
        note: z.ZodOptional<z.ZodString>;
    }, z.core.$strict>>;
}, z.core.$strict>, z.ZodObject<{
    type: z.ZodLiteral<"chevron_process">;
    items: z.ZodArray<z.ZodObject<{
        title: z.ZodString;
        text: z.ZodOptional<z.ZodString>;
        icon: z.ZodOptional<z.ZodEnum<{
            [x: string]: string;
        }>>;
    }, z.core.$strict>>;
}, z.core.$strict>, z.ZodObject<{
    type: z.ZodLiteral<"swimlane">;
    lanes: z.ZodArray<z.ZodObject<{
        label: z.ZodString;
        role: z.ZodOptional<z.ZodString>;
    }, z.core.$strict>>;
    steps: z.ZodArray<z.ZodObject<{
        lane: z.ZodString;
        title: z.ZodString;
        detail: z.ZodOptional<z.ZodString>;
    }, z.core.$strict>>;
    handoff_note: z.ZodOptional<z.ZodString>;
}, z.core.$strict>, z.ZodObject<{
    type: z.ZodLiteral<"journey_map">;
    stages: z.ZodArray<z.ZodObject<{
        label: z.ZodString;
        touchpoints: z.ZodOptional<z.ZodArray<z.ZodString>>;
        action: z.ZodOptional<z.ZodString>;
        emotion: z.ZodNumber;
        opportunity: z.ZodOptional<z.ZodString>;
    }, z.core.$strict>>;
    row_labels: z.ZodOptional<z.ZodObject<{
        touchpoints: z.ZodOptional<z.ZodString>;
        action: z.ZodOptional<z.ZodString>;
        emotion: z.ZodOptional<z.ZodString>;
        opportunity: z.ZodOptional<z.ZodString>;
    }, z.core.$strict>>;
}, z.core.$strict>, z.ZodObject<{
    type: z.ZodLiteral<"decision_tree">;
    question: z.ZodString;
    branches: z.ZodArray<z.ZodObject<{
        edge: z.ZodString;
        title: z.ZodString;
        detail: z.ZodOptional<z.ZodString>;
        outcomes: z.ZodArray<z.ZodObject<{
            edge: z.ZodString;
            title: z.ZodString;
            detail: z.ZodOptional<z.ZodString>;
            value: z.ZodOptional<z.ZodString>;
            unit: z.ZodOptional<z.ZodString>;
            recommended: z.ZodOptional<z.ZodBoolean>;
        }, z.core.$strict>>;
    }, z.core.$strict>>;
}, z.core.$strict>, z.ZodObject<{
    type: z.ZodLiteral<"from_to">;
    from: z.ZodObject<{
        kicker: z.ZodOptional<z.ZodString>;
        title: z.ZodString;
    }, z.core.$strict>;
    to: z.ZodObject<{
        kicker: z.ZodOptional<z.ZodString>;
        title: z.ZodString;
    }, z.core.$strict>;
    rows: z.ZodArray<z.ZodObject<{
        label: z.ZodString;
        icon: z.ZodOptional<z.ZodEnum<{
            [x: string]: string;
        }>>;
        note: z.ZodOptional<z.ZodString>;
        from: z.ZodString;
        to: z.ZodString;
        unit: z.ZodOptional<z.ZodString>;
        change: z.ZodOptional<z.ZodString>;
        tag: z.ZodOptional<z.ZodObject<{
            text: z.ZodString;
            quiet: z.ZodOptional<z.ZodBoolean>;
            evidence: z.ZodOptional<z.ZodEnum<{
                label: "label";
                draft: "draft";
                trial: "trial";
                company: "company";
                press: "press";
                official: "official";
                registry: "registry";
                preprint: "preprint";
            }>>;
            settled: z.ZodOptional<z.ZodBoolean>;
            tone: z.ZodOptional<z.ZodEnum<{
                danger: "danger";
                warning: "warning";
                success: "success";
            }>>;
            basis: z.ZodOptional<z.ZodEnum<{
                law: "law";
                estimate: "estimate";
                pending: "pending";
                proposal: "proposal";
            }>>;
        }, z.core.$strict>>;
        emphasis: z.ZodOptional<z.ZodBoolean>;
    }, z.core.$strict>>;
    label_column: z.ZodOptional<z.ZodString>;
    span: z.ZodOptional<z.ZodString>;
}, z.core.$strict>, z.ZodObject<{
    type: z.ZodLiteral<"org_tree">;
    root: z.ZodObject<{
        name: z.ZodString;
        role: z.ZodOptional<z.ZodString>;
    }, z.core.$strict>;
    children: z.ZodArray<z.ZodObject<{
        name: z.ZodString;
        role: z.ZodOptional<z.ZodString>;
        children: z.ZodOptional<z.ZodArray<z.ZodObject<{
            name: z.ZodString;
            role: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>>>;
    }, z.core.$strict>>;
}, z.core.$strict>, z.ZodObject<{
    type: z.ZodLiteral<"issue_tree">;
    question: z.ZodString;
    children_column: z.ZodOptional<z.ZodString>;
    branches: z.ZodArray<z.ZodObject<{
        label: z.ZodString;
        note: z.ZodOptional<z.ZodString>;
        icon: z.ZodOptional<z.ZodEnum<{
            [x: string]: string;
        }>>;
        emphasis: z.ZodOptional<z.ZodLiteral<true>>;
        children: z.ZodOptional<z.ZodArray<z.ZodObject<{
            label: z.ZodString;
        }, z.core.$strict>>>;
    }, z.core.$strict>>;
}, z.core.$strict>, z.ZodObject<{
    type: z.ZodLiteral<"pyramid">;
    layers: z.ZodArray<z.ZodObject<{
        label: z.ZodString;
        note: z.ZodOptional<z.ZodString>;
        tone: z.ZodOptional<z.ZodEnum<{
            danger: "danger";
            warning: "warning";
            success: "success";
        }>>;
    }, z.core.$strict>>;
}, z.core.$strict>, z.ZodObject<{
    type: z.ZodLiteral<"iceberg">;
    above: z.ZodArray<z.ZodString>;
    below: z.ZodArray<z.ZodString>;
    waterline: z.ZodOptional<z.ZodString>;
    above_label: z.ZodOptional<z.ZodString>;
    below_label: z.ZodOptional<z.ZodString>;
}, z.core.$strict>, z.ZodObject<{
    type: z.ZodLiteral<"pillar_model">;
    goal: z.ZodString;
    pillars: z.ZodArray<z.ZodObject<{
        title: z.ZodString;
        value: z.ZodString;
        unit: z.ZodOptional<z.ZodString>;
    }, z.core.$strict>>;
    base: z.ZodString;
}, z.core.$strict>, z.ZodObject<{
    type: z.ZodLiteral<"value_chain">;
    primary: z.ZodArray<z.ZodObject<{
        label: z.ZodString;
        value: z.ZodOptional<z.ZodString>;
        unit: z.ZodOptional<z.ZodString>;
        emphasis: z.ZodOptional<z.ZodLiteral<true>>;
    }, z.core.$strict>>;
    support: z.ZodArray<z.ZodObject<{
        label: z.ZodString;
        note: z.ZodOptional<z.ZodString>;
    }, z.core.$strict>>;
    margin: z.ZodOptional<z.ZodObject<{
        label: z.ZodString;
        value: z.ZodOptional<z.ZodString>;
    }, z.core.$strict>>;
}, z.core.$strict>, z.ZodObject<{
    type: z.ZodLiteral<"harvey_balls">;
    criteria: z.ZodArray<z.ZodString>;
    options: z.ZodArray<z.ZodObject<{
        label: z.ZodString;
        scores: z.ZodArray<z.ZodUnion<readonly [z.ZodLiteral<0>, z.ZodLiteral<25>, z.ZodLiteral<50>, z.ZodLiteral<75>, z.ZodLiteral<100>]>>;
        total: z.ZodOptional<z.ZodUnion<readonly [z.ZodString, z.ZodNumber]>>;
        highlight: z.ZodOptional<z.ZodBoolean>;
    }, z.core.$strict>>;
    legend: z.ZodOptional<z.ZodBoolean>;
    labels: z.ZodOptional<z.ZodObject<{
        option: z.ZodOptional<z.ZodString>;
        total: z.ZodOptional<z.ZodString>;
        none: z.ZodOptional<z.ZodString>;
        partial: z.ZodOptional<z.ZodString>;
        full: z.ZodOptional<z.ZodString>;
    }, z.core.$strict>>;
}, z.core.$strict>, z.ZodObject<{
    type: z.ZodLiteral<"scorecard">;
    labels: z.ZodOptional<z.ZodObject<{
        metric: z.ZodOptional<z.ZodString>;
        target: z.ZodOptional<z.ZodString>;
        actual: z.ZodOptional<z.ZodString>;
        gap: z.ZodOptional<z.ZodString>;
        status: z.ZodOptional<z.ZodString>;
    }, z.core.$strict>>;
    rows: z.ZodArray<z.ZodObject<{
        label: z.ZodString;
        target: z.ZodString;
        actual: z.ZodString;
        gap: z.ZodString;
        status: z.ZodEnum<{
            watch: "watch";
            on_track: "on_track";
            off_track: "off_track";
        }>;
        status_label: z.ZodOptional<z.ZodString>;
    }, z.core.$strict>>;
    note: z.ZodOptional<z.ZodString>;
}, z.core.$strict>, z.ZodObject<{
    type: z.ZodLiteral<"pictogram">;
    rows: z.ZodArray<z.ZodObject<{
        filled: z.ZodNumber;
        label: z.ZodString;
        caption: z.ZodOptional<z.ZodString>;
        highlight: z.ZodOptional<z.ZodBoolean>;
    }, z.core.$strict>>;
}, z.core.$strict>, z.ZodObject<{
    type: z.ZodLiteral<"word_cloud">;
    words: z.ZodArray<z.ZodObject<{
        text: z.ZodString;
        weight: z.ZodUnion<readonly [z.ZodLiteral<1>, z.ZodLiteral<2>, z.ZodLiteral<3>, z.ZodLiteral<4>]>;
    }, z.core.$strict>>;
}, z.core.$strict>, z.ZodObject<{
    type: z.ZodLiteral<"venn">;
    sets: z.ZodArray<z.ZodObject<{
        label: z.ZodString;
    }, z.core.$strict>>;
    center: z.ZodString;
}, z.core.$strict>, z.ZodObject<{
    type: z.ZodLiteral<"fishbone">;
    effect: z.ZodString;
    ribs: z.ZodArray<z.ZodObject<{
        label: z.ZodString;
        causes: z.ZodArray<z.ZodString>;
    }, z.core.$strict>>;
}, z.core.$strict>, z.ZodObject<{
    type: z.ZodLiteral<"positioning_map">;
    x_axis: z.ZodObject<{
        title: z.ZodString;
        low: z.ZodString;
        high: z.ZodString;
    }, z.core.$strict>;
    y_axis: z.ZodObject<{
        title: z.ZodString;
        low: z.ZodString;
        high: z.ZodString;
    }, z.core.$strict>;
    quadrants: z.ZodOptional<z.ZodObject<{
        top_left: z.ZodString;
        top_right: z.ZodString;
        bottom_left: z.ZodString;
        bottom_right: z.ZodString;
    }, z.core.$strict>>;
    points: z.ZodArray<z.ZodObject<{
        label: z.ZodString;
        x: z.ZodNumber;
        y: z.ZodNumber;
        emphasis: z.ZodOptional<z.ZodLiteral<true>>;
    }, z.core.$strict>>;
}, z.core.$strict>, z.ZodObject<{
    type: z.ZodLiteral<"concept_equation">;
    operands: z.ZodArray<z.ZodObject<{
        label: z.ZodString;
        value: z.ZodOptional<z.ZodString>;
        note: z.ZodOptional<z.ZodString>;
        icon: z.ZodOptional<z.ZodEnum<{
            [x: string]: string;
        }>>;
    }, z.core.$strict>>;
    result: z.ZodObject<{
        label: z.ZodString;
        value: z.ZodOptional<z.ZodString>;
        note: z.ZodOptional<z.ZodString>;
        icon: z.ZodOptional<z.ZodEnum<{
            [x: string]: string;
        }>>;
    }, z.core.$strict>;
    excluded: z.ZodOptional<z.ZodObject<{
        label: z.ZodString;
        value: z.ZodOptional<z.ZodString>;
        note: z.ZodOptional<z.ZodString>;
        icon: z.ZodOptional<z.ZodEnum<{
            [x: string]: string;
        }>>;
    }, z.core.$strict>>;
}, z.core.$strict>, z.ZodObject<{
    type: z.ZodLiteral<"segmented_wheel">;
    center: z.ZodString;
    segments: z.ZodArray<z.ZodObject<{
        label: z.ZodString;
        value: z.ZodOptional<z.ZodString>;
        emphasis: z.ZodOptional<z.ZodLiteral<true>>;
    }, z.core.$strict>>;
}, z.core.$strict>, z.ZodObject<{
    type: z.ZodLiteral<"pros_cons">;
    pros: z.ZodObject<{
        title: z.ZodString;
        items: z.ZodArray<z.ZodObject<{
            label: z.ZodString;
            note: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>>;
    }, z.core.$strict>;
    cons: z.ZodObject<{
        title: z.ZodString;
        items: z.ZodArray<z.ZodObject<{
            label: z.ZodString;
            note: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>>;
    }, z.core.$strict>;
    verdict: z.ZodString;
}, z.core.$strict>, z.ZodObject<{
    type: z.ZodLiteral<"sketch">;
    kind: z.ZodEnum<{
        discontinuity: "discontinuity";
        difference_in_differences: "difference_in_differences";
    }>;
    at: z.ZodString;
    x_title: z.ZodString;
    y_title: z.ZodOptional<z.ZodString>;
    effect: z.ZodOptional<z.ZodString>;
    groups: z.ZodOptional<z.ZodArray<z.ZodString>>;
    direction: z.ZodOptional<z.ZodEnum<{
        up: "up";
        down: "down";
    }>>;
}, z.core.$strict>], "type">;
/**
 * All component `type` discriminant values, derived from `ComponentSchema`
 * itself (never hand-copied) so this list can't drift from the union above.
 * Typed as plain `readonly string[]` rather than `Component["type"][]` —
 * every consumer of this list (W5's plan `focus` vocabulary gate,
 * `src/spec/index.ts`) tests membership of an arbitrary author-supplied
 * string, and TS's `Array.includes` is invariant in its element type, so a
 * narrower literal-union type would reject that call at the caller.
 */
declare const COMPONENT_TYPES: readonly string[];
/**
 * IR v5 slide contract. Content slides require `kind`. Cover, chapter, and
 * ending slides have no `kind` field because page type already determines
 * their menu entry. Omitting `type` still means `content`, but therefore also
 * requires an explicit `kind`.
 */
declare const SlideSchema: z.ZodPreprocess<z.ZodDiscriminatedUnion<[z.ZodObject<{
    id: z.ZodOptional<z.ZodString>;
    placeholder: z.ZodOptional<z.ZodLiteral<true>>;
    heading: z.ZodOptional<z.ZodString>;
    subheading: z.ZodOptional<z.ZodString>;
    kicker: z.ZodOptional<z.ZodString>;
    fields: z.ZodOptional<z.ZodArray<z.ZodObject<{
        label: z.ZodString;
        value: z.ZodString;
        note: z.ZodOptional<z.ZodString>;
    }, z.core.$strict>>>;
    stamp: z.ZodOptional<z.ZodObject<{
        text: z.ZodString;
        date: z.ZodOptional<z.ZodString>;
    }, z.core.$strict>>;
    ballot: z.ZodOptional<z.ZodObject<{
        choices: z.ZodArray<z.ZodString>;
        signature: z.ZodOptional<z.ZodString>;
        item_choices: z.ZodOptional<z.ZodArray<z.ZodObject<{
            item: z.ZodNumber;
            choices: z.ZodArray<z.ZodString>;
        }, z.core.$strict>>>;
    }, z.core.$strict>>;
    tag: z.ZodOptional<z.ZodObject<{
        text: z.ZodString;
        quiet: z.ZodOptional<z.ZodBoolean>;
        evidence: z.ZodOptional<z.ZodEnum<{
            label: "label";
            draft: "draft";
            trial: "trial";
            company: "company";
            press: "press";
            official: "official";
            registry: "registry";
            preprint: "preprint";
        }>>;
        settled: z.ZodOptional<z.ZodBoolean>;
        tone: z.ZodOptional<z.ZodEnum<{
            danger: "danger";
            warning: "warning";
            success: "success";
        }>>;
        basis: z.ZodOptional<z.ZodEnum<{
            law: "law";
            estimate: "estimate";
            pending: "pending";
            proposal: "proposal";
        }>>;
    }, z.core.$strict>>;
    years: z.ZodOptional<z.ZodObject<{
        from: z.ZodNumber;
        to: z.ZodNumber;
        marked: z.ZodArray<z.ZodNumber>;
    }, z.core.$strict>>;
    stage: z.ZodOptional<z.ZodString>;
    components: z.ZodDefault<z.ZodArray<z.ZodDiscriminatedUnion<[z.ZodObject<{
        type: z.ZodLiteral<"bullets">;
        items: z.ZodArray<z.ZodString>;
        style: z.ZodOptional<z.ZodEnum<{
            default: "default";
            checklist: "checklist";
            numbered: "numbered";
            plain: "plain";
            divided: "divided";
        }>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"paragraph">;
        text: z.ZodString;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"blockquote">;
        text: z.ZodString;
        attribution: z.ZodOptional<z.ZodString>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"callout">;
        variant: z.ZodEnum<{
            info: "info";
            warn: "warn";
            tip: "tip";
        }>;
        title: z.ZodOptional<z.ZodString>;
        text: z.ZodString;
        icon: z.ZodOptional<z.ZodEnum<{
            [x: string]: string;
        }>>;
        tag: z.ZodOptional<z.ZodObject<{
            text: z.ZodString;
            quiet: z.ZodOptional<z.ZodBoolean>;
            evidence: z.ZodOptional<z.ZodEnum<{
                label: "label";
                draft: "draft";
                trial: "trial";
                company: "company";
                press: "press";
                official: "official";
                registry: "registry";
                preprint: "preprint";
            }>>;
            settled: z.ZodOptional<z.ZodBoolean>;
            tone: z.ZodOptional<z.ZodEnum<{
                danger: "danger";
                warning: "warning";
                success: "success";
            }>>;
            basis: z.ZodOptional<z.ZodEnum<{
                law: "law";
                estimate: "estimate";
                pending: "pending";
                proposal: "proposal";
            }>>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"code">;
        language: z.ZodString;
        code: z.ZodString;
        title: z.ZodOptional<z.ZodString>;
        highlight_lines: z.ZodOptional<z.ZodArray<z.ZodNumber>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"kpi_cards">;
        items: z.ZodArray<z.ZodObject<{
            value: z.ZodString;
            unit: z.ZodOptional<z.ZodString>;
            label: z.ZodString;
            note: z.ZodOptional<z.ZodString>;
            tag: z.ZodOptional<z.ZodObject<{
                text: z.ZodString;
                quiet: z.ZodOptional<z.ZodBoolean>;
                evidence: z.ZodOptional<z.ZodEnum<{
                    label: "label";
                    draft: "draft";
                    trial: "trial";
                    company: "company";
                    press: "press";
                    official: "official";
                    registry: "registry";
                    preprint: "preprint";
                }>>;
                settled: z.ZodOptional<z.ZodBoolean>;
                tone: z.ZodOptional<z.ZodEnum<{
                    danger: "danger";
                    warning: "warning";
                    success: "success";
                }>>;
                basis: z.ZodOptional<z.ZodEnum<{
                    law: "law";
                    estimate: "estimate";
                    pending: "pending";
                    proposal: "proposal";
                }>>;
            }, z.core.$strict>>;
            delta: z.ZodOptional<z.ZodEnum<{
                flat: "flat";
                up: "up";
                down: "down";
            }>>;
            delta_good: z.ZodOptional<z.ZodBoolean>;
            icon: z.ZodOptional<z.ZodEnum<{
                [x: string]: string;
            }>>;
            tone: z.ZodOptional<z.ZodEnum<{
                danger: "danger";
                warning: "warning";
                success: "success";
            }>>;
            source: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"chart">;
        title: z.ZodOptional<z.ZodString>;
        chart_type: z.ZodEnum<{
            line: "line";
            donut: "donut";
            dumbbell: "dumbbell";
            funnel: "funnel";
            gauge: "gauge";
            bar: "bar";
            stacked: "stacked";
            percent_stacked: "percent_stacked";
            pie: "pie";
            area: "area";
            combo: "combo";
            scatter: "scatter";
        }>;
        direction: z.ZodOptional<z.ZodEnum<{
            horizontal: "horizontal";
            vertical: "vertical";
        }>>;
        style: z.ZodOptional<z.ZodEnum<{
            donut: "donut";
        }>>;
        center_total: z.ZodOptional<z.ZodBoolean>;
        gauge: z.ZodOptional<z.ZodObject<{
            min: z.ZodOptional<z.ZodNumber>;
            max: z.ZodOptional<z.ZodNumber>;
        }, z.core.$strict>>;
        axes: z.ZodOptional<z.ZodObject<{
            x_title: z.ZodOptional<z.ZodString>;
            y_title: z.ZodOptional<z.ZodString>;
            x_unit: z.ZodOptional<z.ZodString>;
            y_unit: z.ZodOptional<z.ZodString>;
            y2_title: z.ZodOptional<z.ZodString>;
            y2_unit: z.ZodOptional<z.ZodString>;
            show_grid: z.ZodOptional<z.ZodBoolean>;
        }, z.core.$strict>>;
        tag: z.ZodOptional<z.ZodObject<{
            text: z.ZodString;
            quiet: z.ZodOptional<z.ZodBoolean>;
            evidence: z.ZodOptional<z.ZodEnum<{
                label: "label";
                draft: "draft";
                trial: "trial";
                company: "company";
                press: "press";
                official: "official";
                registry: "registry";
                preprint: "preprint";
            }>>;
            settled: z.ZodOptional<z.ZodBoolean>;
            tone: z.ZodOptional<z.ZodEnum<{
                danger: "danger";
                warning: "warning";
                success: "success";
            }>>;
            basis: z.ZodOptional<z.ZodEnum<{
                law: "law";
                estimate: "estimate";
                pending: "pending";
                proposal: "proposal";
            }>>;
        }, z.core.$strict>>;
        changes: z.ZodOptional<z.ZodArray<z.ZodObject<{
            from: z.ZodString;
            to: z.ZodString;
            at: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>>>;
        bands: z.ZodOptional<z.ZodArray<z.ZodObject<{
            from: z.ZodNumber;
            to: z.ZodNumber;
            label: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>>>;
        emphasis_label: z.ZodOptional<z.ZodString>;
        reference: z.ZodOptional<z.ZodObject<{
            value: z.ZodNumber;
            label: z.ZodString;
        }, z.core.$strict>>;
        markers: z.ZodOptional<z.ZodArray<z.ZodObject<{
            before: z.ZodString;
            label: z.ZodString;
        }, z.core.$strict>>>;
        gaps: z.ZodOptional<z.ZodArray<z.ZodObject<{
            after: z.ZodString;
            x: z.ZodString;
            label: z.ZodString;
        }, z.core.$strict>>>;
        series: z.ZodArray<z.ZodObject<{
            name: z.ZodString;
            data: z.ZodArray<z.ZodObject<{
                x: z.ZodUnion<readonly [z.ZodString, z.ZodNumber]>;
                y: z.ZodNumber;
                size: z.ZodOptional<z.ZodNumber>;
                status: z.ZodOptional<z.ZodEnum<{
                    target: "target";
                    estimate: "estimate";
                    forecast: "forecast";
                }>>;
                emphasis: z.ZodOptional<z.ZodBoolean>;
                note: z.ZodOptional<z.ZodString>;
                icon: z.ZodOptional<z.ZodEnum<{
                    [x: string]: string;
                }>>;
                upper: z.ZodOptional<z.ZodNumber>;
            }, z.core.$strict>>;
            plot: z.ZodOptional<z.ZodEnum<{
                line: "line";
                bar: "bar";
            }>>;
            axis: z.ZodOptional<z.ZodEnum<{
                left: "left";
                right: "right";
            }>>;
            emphasis: z.ZodOptional<z.ZodBoolean>;
            steps: z.ZodOptional<z.ZodBoolean>;
            tone: z.ZodOptional<z.ZodEnum<{
                danger: "danger";
                warning: "warning";
                success: "success";
            }>>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"flowchart">;
        nodes: z.ZodArray<z.ZodObject<{
            id: z.ZodString;
            label: z.ZodString;
            kind: z.ZodOptional<z.ZodEnum<{
                rect: "rect";
                diamond: "diamond";
                round: "round";
            }>>;
        }, z.core.$strict>>;
        edges: z.ZodArray<z.ZodObject<{
            from: z.ZodString;
            to: z.ZodString;
            label: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>>;
        direction: z.ZodOptional<z.ZodEnum<{
            TB: "TB";
            TD: "TD";
            BT: "BT";
            LR: "LR";
            RL: "RL";
        }>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"architecture">;
        layers: z.ZodArray<z.ZodObject<{
            title: z.ZodString;
            items: z.ZodArray<z.ZodString>;
        }, z.core.$strict>>;
        direction: z.ZodOptional<z.ZodEnum<{
            top_down: "top_down";
            bottom_up: "bottom_up";
        }>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"timeline">;
        title: z.ZodOptional<z.ZodString>;
        layout: z.ZodOptional<z.ZodEnum<{
            horizontal: "horizontal";
            vertical: "vertical";
        }>>;
        lanes: z.ZodOptional<z.ZodArray<z.ZodString>>;
        periods: z.ZodOptional<z.ZodArray<z.ZodObject<{
            from: z.ZodString;
            to: z.ZodString;
            label: z.ZodString;
            basis: z.ZodOptional<z.ZodEnum<{
                law: "law";
                estimate: "estimate";
                pending: "pending";
                proposal: "proposal";
            }>>;
        }, z.core.$strict>>>;
        milestones: z.ZodArray<z.ZodObject<{
            date: z.ZodString;
            title: z.ZodString;
            desc: z.ZodOptional<z.ZodString>;
            highlight: z.ZodOptional<z.ZodBoolean>;
            icon: z.ZodOptional<z.ZodEnum<{
                [x: string]: string;
            }>>;
            tone: z.ZodOptional<z.ZodEnum<{
                danger: "danger";
                warning: "warning";
                success: "success";
            }>>;
            status: z.ZodOptional<z.ZodEnum<{
                pending: "pending";
            }>>;
            tag: z.ZodOptional<z.ZodObject<{
                text: z.ZodString;
                quiet: z.ZodOptional<z.ZodBoolean>;
                evidence: z.ZodOptional<z.ZodEnum<{
                    label: "label";
                    draft: "draft";
                    trial: "trial";
                    company: "company";
                    press: "press";
                    official: "official";
                    registry: "registry";
                    preprint: "preprint";
                }>>;
                settled: z.ZodOptional<z.ZodBoolean>;
                tone: z.ZodOptional<z.ZodEnum<{
                    danger: "danger";
                    warning: "warning";
                    success: "success";
                }>>;
                basis: z.ZodOptional<z.ZodEnum<{
                    law: "law";
                    estimate: "estimate";
                    pending: "pending";
                    proposal: "proposal";
                }>>;
            }, z.core.$strict>>;
            source: z.ZodOptional<z.ZodString>;
            lane: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"comparison">;
        title: z.ZodOptional<z.ZodString>;
        columns: z.ZodArray<z.ZodString>;
        label_column: z.ZodOptional<z.ZodString>;
        rows: z.ZodArray<z.ZodObject<{
            label: z.ZodString;
            cells: z.ZodArray<z.ZodString>;
            icon: z.ZodOptional<z.ZodEnum<{
                [x: string]: string;
            }>>;
            tag: z.ZodOptional<z.ZodObject<{
                text: z.ZodString;
                quiet: z.ZodOptional<z.ZodBoolean>;
                evidence: z.ZodOptional<z.ZodEnum<{
                    label: "label";
                    draft: "draft";
                    trial: "trial";
                    company: "company";
                    press: "press";
                    official: "official";
                    registry: "registry";
                    preprint: "preprint";
                }>>;
                settled: z.ZodOptional<z.ZodBoolean>;
                tone: z.ZodOptional<z.ZodEnum<{
                    danger: "danger";
                    warning: "warning";
                    success: "success";
                }>>;
                basis: z.ZodOptional<z.ZodEnum<{
                    law: "law";
                    estimate: "estimate";
                    pending: "pending";
                    proposal: "proposal";
                }>>;
            }, z.core.$strict>>;
            emphasis: z.ZodOptional<z.ZodBoolean>;
        }, z.core.$strict>>;
        tag_column: z.ZodOptional<z.ZodString>;
        recommended: z.ZodOptional<z.ZodNumber>;
        recommended_label: z.ZodOptional<z.ZodString>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"icon_cards">;
        title: z.ZodOptional<z.ZodString>;
        items: z.ZodArray<z.ZodObject<{
            icon: z.ZodEnum<{
                [x: string]: string;
            }>;
            title: z.ZodString;
            text: z.ZodString;
            tag: z.ZodOptional<z.ZodObject<{
                text: z.ZodString;
                quiet: z.ZodOptional<z.ZodBoolean>;
                evidence: z.ZodOptional<z.ZodEnum<{
                    label: "label";
                    draft: "draft";
                    trial: "trial";
                    company: "company";
                    press: "press";
                    official: "official";
                    registry: "registry";
                    preprint: "preprint";
                }>>;
                settled: z.ZodOptional<z.ZodBoolean>;
                tone: z.ZodOptional<z.ZodEnum<{
                    danger: "danger";
                    warning: "warning";
                    success: "success";
                }>>;
                basis: z.ZodOptional<z.ZodEnum<{
                    law: "law";
                    estimate: "estimate";
                    pending: "pending";
                    proposal: "proposal";
                }>>;
            }, z.core.$strict>>;
            tone: z.ZodOptional<z.ZodEnum<{
                danger: "danger";
                warning: "warning";
                success: "success";
            }>>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"row_cards">;
        items: z.ZodArray<z.ZodObject<{
            icon: z.ZodOptional<z.ZodEnum<{
                [x: string]: string;
            }>>;
            title: z.ZodString;
            text: z.ZodOptional<z.ZodString>;
            sub: z.ZodOptional<z.ZodString>;
            highlight: z.ZodOptional<z.ZodBoolean>;
            tone: z.ZodOptional<z.ZodEnum<{
                danger: "danger";
                warning: "warning";
                success: "success";
            }>>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"steps">;
        items: z.ZodArray<z.ZodObject<{
            title: z.ZodString;
            text: z.ZodString;
            icon: z.ZodOptional<z.ZodEnum<{
                [x: string]: string;
            }>>;
            tone: z.ZodOptional<z.ZodEnum<{
                danger: "danger";
                warning: "warning";
                success: "success";
            }>>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"rings">;
        items: z.ZodArray<z.ZodObject<{
            label: z.ZodString;
            desc: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"numbered_cards">;
        items: z.ZodArray<z.ZodObject<{
            title: z.ZodString;
            text: z.ZodOptional<z.ZodString>;
            sub: z.ZodOptional<z.ZodString>;
            icon: z.ZodOptional<z.ZodEnum<{
                [x: string]: string;
            }>>;
            emphasis: z.ZodOptional<z.ZodBoolean>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"roadmap">;
        items: z.ZodArray<z.ZodObject<{
            title: z.ZodString;
            period: z.ZodOptional<z.ZodString>;
            icon: z.ZodOptional<z.ZodEnum<{
                [x: string]: string;
            }>>;
            rows: z.ZodOptional<z.ZodArray<z.ZodObject<{
                label: z.ZodString;
                value: z.ZodString;
                basis: z.ZodOptional<z.ZodEnum<{
                    law: "law";
                    estimate: "estimate";
                    pending: "pending";
                    proposal: "proposal";
                }>>;
            }, z.core.$strict>>>;
            duration: z.ZodOptional<z.ZodNumber>;
            checkpoint: z.ZodOptional<z.ZodString>;
            points: z.ZodOptional<z.ZodArray<z.ZodString>>;
            emphasis: z.ZodOptional<z.ZodBoolean>;
        }, z.core.$strict>>;
        duration_unit: z.ZodOptional<z.ZodString>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"matrix">;
        title: z.ZodOptional<z.ZodString>;
        x_title: z.ZodOptional<z.ZodString>;
        y_title: z.ZodOptional<z.ZodString>;
        cols: z.ZodNumber;
        columns: z.ZodOptional<z.ZodArray<z.ZodString>>;
        rows: z.ZodOptional<z.ZodArray<z.ZodObject<{
            label: z.ZodString;
            icon: z.ZodOptional<z.ZodEnum<{
                [x: string]: string;
            }>>;
        }, z.core.$strict>>>;
        items: z.ZodArray<z.ZodObject<{
            title: z.ZodString;
            tag: z.ZodOptional<z.ZodString>;
            tone: z.ZodOptional<z.ZodEnum<{
                info: "info";
                neutral: "neutral";
                accent: "accent";
            }>>;
            empty: z.ZodOptional<z.ZodBoolean>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"insight_panel">;
        title: z.ZodString;
        icon: z.ZodOptional<z.ZodEnum<{
            [x: string]: string;
        }>>;
        rows: z.ZodArray<z.ZodObject<{
            label: z.ZodString;
            text: z.ZodString;
        }, z.core.$strict>>;
        footnote: z.ZodOptional<z.ZodString>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"verdict_banner">;
        text: z.ZodString;
        tone: z.ZodEnum<{
            warning: "warning";
            positive: "positive";
            neutral: "neutral";
        }>;
        icon: z.ZodOptional<z.ZodEnum<{
            [x: string]: string;
        }>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"image">;
        asset_id: z.ZodString;
        caption: z.ZodOptional<z.ZodString>;
        fit: z.ZodDefault<z.ZodEnum<{
            cover: "cover";
            contain: "contain";
        }>>;
        crop: z.ZodOptional<z.ZodArray<z.ZodNumber>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"image_grid">;
        items: z.ZodArray<z.ZodObject<{
            asset_id: z.ZodString;
            caption: z.ZodOptional<z.ZodString>;
            icon: z.ZodOptional<z.ZodEnum<{
                [x: string]: string;
            }>>;
            tag: z.ZodOptional<z.ZodObject<{
                text: z.ZodString;
                quiet: z.ZodOptional<z.ZodBoolean>;
                evidence: z.ZodOptional<z.ZodEnum<{
                    label: "label";
                    draft: "draft";
                    trial: "trial";
                    company: "company";
                    press: "press";
                    official: "official";
                    registry: "registry";
                    preprint: "preprint";
                }>>;
                settled: z.ZodOptional<z.ZodBoolean>;
                tone: z.ZodOptional<z.ZodEnum<{
                    danger: "danger";
                    warning: "warning";
                    success: "success";
                }>>;
                basis: z.ZodOptional<z.ZodEnum<{
                    law: "law";
                    estimate: "estimate";
                    pending: "pending";
                    proposal: "proposal";
                }>>;
            }, z.core.$strict>>;
            crop: z.ZodOptional<z.ZodArray<z.ZodNumber>>;
        }, z.core.$strict>>;
        emphasis: z.ZodOptional<z.ZodEnum<{
            none: "none";
            first: "first";
        }>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"image_compare">;
        left: z.ZodObject<{
            asset_id: z.ZodString;
            label: z.ZodString;
        }, z.core.$strict>;
        right: z.ZodObject<{
            asset_id: z.ZodString;
            label: z.ZodString;
        }, z.core.$strict>;
        style: z.ZodOptional<z.ZodEnum<{
            vs: "vs";
            before_after: "before_after";
        }>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"logo_wall">;
        title: z.ZodOptional<z.ZodString>;
        items: z.ZodArray<z.ZodObject<{
            name: z.ZodString;
            asset_id: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"product_cards">;
        items: z.ZodArray<z.ZodObject<{
            asset_id: z.ZodString;
            name: z.ZodString;
            note: z.ZodOptional<z.ZodString>;
            price: z.ZodOptional<z.ZodString>;
            price_unit: z.ZodOptional<z.ZodString>;
            featured: z.ZodOptional<z.ZodLiteral<true>>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"quote_wall">;
        quotes: z.ZodArray<z.ZodObject<{
            text: z.ZodString;
            name: z.ZodString;
            role: z.ZodOptional<z.ZodString>;
            featured: z.ZodOptional<z.ZodLiteral<true>>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"swot">;
        strengths: z.ZodArray<z.ZodString>;
        weaknesses: z.ZodArray<z.ZodString>;
        opportunities: z.ZodArray<z.ZodString>;
        threats: z.ZodArray<z.ZodString>;
        labels: z.ZodOptional<z.ZodObject<{
            strengths: z.ZodOptional<z.ZodString>;
            weaknesses: z.ZodOptional<z.ZodString>;
            opportunities: z.ZodOptional<z.ZodString>;
            threats: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"bmc">;
        key_partners: z.ZodArray<z.ZodString>;
        key_activities: z.ZodArray<z.ZodString>;
        key_resources: z.ZodArray<z.ZodString>;
        value_propositions: z.ZodArray<z.ZodString>;
        customer_relationships: z.ZodArray<z.ZodString>;
        channels: z.ZodArray<z.ZodString>;
        customer_segments: z.ZodArray<z.ZodString>;
        cost_structure: z.ZodArray<z.ZodString>;
        revenue_streams: z.ZodArray<z.ZodString>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"waterfall">;
        title: z.ZodOptional<z.ZodString>;
        items: z.ZodArray<z.ZodObject<{
            label: z.ZodString;
            value: z.ZodNumber;
            kind: z.ZodOptional<z.ZodEnum<{
                delta: "delta";
                total: "total";
            }>>;
            note: z.ZodOptional<z.ZodString>;
            emphasis: z.ZodOptional<z.ZodBoolean>;
        }, z.core.$strict>>;
        unit: z.ZodOptional<z.ZodString>;
        emphasis_label: z.ZodOptional<z.ZodString>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"gantt">;
        items: z.ZodArray<z.ZodObject<{
            label: z.ZodString;
            start: z.ZodNumber;
            end: z.ZodNumber;
            text: z.ZodOptional<z.ZodString>;
            emphasis: z.ZodOptional<z.ZodBoolean>;
            icon: z.ZodOptional<z.ZodEnum<{
                [x: string]: string;
            }>>;
            period: z.ZodOptional<z.ZodString>;
            basis: z.ZodOptional<z.ZodEnum<{
                law: "law";
                estimate: "estimate";
                pending: "pending";
                proposal: "proposal";
            }>>;
        }, z.core.$strict>>;
        axis_labels: z.ZodOptional<z.ZodArray<z.ZodString>>;
        range: z.ZodOptional<z.ZodObject<{
            from: z.ZodNumber;
            to: z.ZodNumber;
        }, z.core.$strict>>;
        milestones: z.ZodOptional<z.ZodArray<z.ZodObject<{
            at: z.ZodNumber;
            label: z.ZodString;
        }, z.core.$strict>>>;
        bands: z.ZodOptional<z.ZodArray<z.ZodObject<{
            from: z.ZodNumber;
            to: z.ZodNumber;
            label: z.ZodString;
        }, z.core.$strict>>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"pest">;
        political: z.ZodObject<{
            title: z.ZodOptional<z.ZodString>;
            items: z.ZodArray<z.ZodString>;
        }, z.core.$strict>;
        economic: z.ZodObject<{
            title: z.ZodOptional<z.ZodString>;
            items: z.ZodArray<z.ZodString>;
        }, z.core.$strict>;
        social: z.ZodObject<{
            title: z.ZodOptional<z.ZodString>;
            items: z.ZodArray<z.ZodString>;
        }, z.core.$strict>;
        technological: z.ZodObject<{
            title: z.ZodOptional<z.ZodString>;
            items: z.ZodArray<z.ZodString>;
        }, z.core.$strict>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"five_forces">;
        rivalry: z.ZodObject<{
            label: z.ZodOptional<z.ZodString>;
            intensity: z.ZodOptional<z.ZodEnum<{
                low: "low";
                medium: "medium";
                high: "high";
            }>>;
            items: z.ZodArray<z.ZodString>;
        }, z.core.$strict>;
        new_entrants: z.ZodObject<{
            label: z.ZodOptional<z.ZodString>;
            intensity: z.ZodOptional<z.ZodEnum<{
                low: "low";
                medium: "medium";
                high: "high";
            }>>;
            items: z.ZodArray<z.ZodString>;
        }, z.core.$strict>;
        supplier_power: z.ZodObject<{
            label: z.ZodOptional<z.ZodString>;
            intensity: z.ZodOptional<z.ZodEnum<{
                low: "low";
                medium: "medium";
                high: "high";
            }>>;
            items: z.ZodArray<z.ZodString>;
        }, z.core.$strict>;
        buyer_power: z.ZodObject<{
            label: z.ZodOptional<z.ZodString>;
            intensity: z.ZodOptional<z.ZodEnum<{
                low: "low";
                medium: "medium";
                high: "high";
            }>>;
            items: z.ZodArray<z.ZodString>;
        }, z.core.$strict>;
        substitutes: z.ZodObject<{
            label: z.ZodOptional<z.ZodString>;
            intensity: z.ZodOptional<z.ZodEnum<{
                low: "low";
                medium: "medium";
                high: "high";
            }>>;
            items: z.ZodArray<z.ZodString>;
        }, z.core.$strict>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"heatmap">;
        x_labels: z.ZodArray<z.ZodString>;
        y_labels: z.ZodArray<z.ZodString>;
        values: z.ZodArray<z.ZodArray<z.ZodNumber>>;
        domain: z.ZodOptional<z.ZodObject<{
            min: z.ZodNumber;
            max: z.ZodNumber;
        }, z.core.$strict>>;
        show_values: z.ZodOptional<z.ZodBoolean>;
        x_title: z.ZodOptional<z.ZodString>;
        y_title: z.ZodOptional<z.ZodString>;
        label_every: z.ZodOptional<z.ZodNumber>;
        steps: z.ZodOptional<z.ZodArray<z.ZodObject<{
            max: z.ZodOptional<z.ZodNumber>;
            label: z.ZodString;
            short: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>>>;
        bands: z.ZodOptional<z.ZodArray<z.ZodObject<{
            from: z.ZodString;
            to: z.ZodString;
            label: z.ZodString;
            icon: z.ZodOptional<z.ZodEnum<{
                [x: string]: string;
            }>>;
        }, z.core.$strict>>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"sankey">;
        nodes: z.ZodArray<z.ZodObject<{
            id: z.ZodString;
            label: z.ZodString;
        }, z.core.$strict>>;
        links: z.ZodArray<z.ZodObject<{
            from: z.ZodString;
            to: z.ZodString;
            value: z.ZodNumber;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"data_table">;
        title: z.ZodOptional<z.ZodString>;
        columns: z.ZodArray<z.ZodObject<{
            key: z.ZodString;
            label: z.ZodString;
            align: z.ZodOptional<z.ZodEnum<{
                left: "left";
                right: "right";
                center: "center";
            }>>;
            emphasis: z.ZodOptional<z.ZodBoolean>;
            icon: z.ZodOptional<z.ZodEnum<{
                [x: string]: string;
            }>>;
        }, z.core.$strict>>;
        rows: z.ZodArray<z.ZodObject<{
            cells: z.ZodRecord<z.ZodString, z.ZodUnion<readonly [z.ZodString, z.ZodNumber]>>;
            emphasis: z.ZodOptional<z.ZodEnum<{
                highlight: "highlight";
                total: "total";
            }>>;
            icon: z.ZodOptional<z.ZodEnum<{
                [x: string]: string;
            }>>;
            tag: z.ZodOptional<z.ZodObject<{
                text: z.ZodString;
                quiet: z.ZodOptional<z.ZodBoolean>;
                evidence: z.ZodOptional<z.ZodEnum<{
                    label: "label";
                    draft: "draft";
                    trial: "trial";
                    company: "company";
                    press: "press";
                    official: "official";
                    registry: "registry";
                    preprint: "preprint";
                }>>;
                settled: z.ZodOptional<z.ZodBoolean>;
                tone: z.ZodOptional<z.ZodEnum<{
                    danger: "danger";
                    warning: "warning";
                    success: "success";
                }>>;
                basis: z.ZodOptional<z.ZodEnum<{
                    law: "law";
                    estimate: "estimate";
                    pending: "pending";
                    proposal: "proposal";
                }>>;
            }, z.core.$strict>>;
        }, z.core.$strict>>;
        source: z.ZodOptional<z.ZodString>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"device_mockup">;
        device: z.ZodEnum<{
            phone: "phone";
            browser: "browser";
        }>;
        asset_id: z.ZodString;
        caption: z.ZodOptional<z.ZodString>;
        url: z.ZodOptional<z.ZodString>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"cycle">;
        title: z.ZodOptional<z.ZodString>;
        items: z.ZodArray<z.ZodObject<{
            label: z.ZodString;
            description: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"people_cards">;
        title: z.ZodOptional<z.ZodString>;
        people: z.ZodArray<z.ZodObject<{
            name: z.ZodString;
            role: z.ZodOptional<z.ZodString>;
            org: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"hub_spoke">;
        center: z.ZodString;
        items: z.ZodArray<z.ZodObject<{
            label: z.ZodString;
            description: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"progress_donuts">;
        items: z.ZodArray<z.ZodObject<{
            value: z.ZodString;
            unit: z.ZodOptional<z.ZodString>;
            label: z.ZodString;
            icon: z.ZodOptional<z.ZodEnum<{
                [x: string]: string;
            }>>;
            source: z.ZodOptional<z.ZodString>;
            detail: z.ZodOptional<z.ZodString>;
            emphasis: z.ZodOptional<z.ZodBoolean>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"staircase">;
        items: z.ZodArray<z.ZodObject<{
            title: z.ZodString;
            value: z.ZodString;
            unit: z.ZodOptional<z.ZodString>;
            note: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"chevron_process">;
        items: z.ZodArray<z.ZodObject<{
            title: z.ZodString;
            text: z.ZodOptional<z.ZodString>;
            icon: z.ZodOptional<z.ZodEnum<{
                [x: string]: string;
            }>>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"swimlane">;
        lanes: z.ZodArray<z.ZodObject<{
            label: z.ZodString;
            role: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>>;
        steps: z.ZodArray<z.ZodObject<{
            lane: z.ZodString;
            title: z.ZodString;
            detail: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>>;
        handoff_note: z.ZodOptional<z.ZodString>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"journey_map">;
        stages: z.ZodArray<z.ZodObject<{
            label: z.ZodString;
            touchpoints: z.ZodOptional<z.ZodArray<z.ZodString>>;
            action: z.ZodOptional<z.ZodString>;
            emotion: z.ZodNumber;
            opportunity: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>>;
        row_labels: z.ZodOptional<z.ZodObject<{
            touchpoints: z.ZodOptional<z.ZodString>;
            action: z.ZodOptional<z.ZodString>;
            emotion: z.ZodOptional<z.ZodString>;
            opportunity: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"decision_tree">;
        question: z.ZodString;
        branches: z.ZodArray<z.ZodObject<{
            edge: z.ZodString;
            title: z.ZodString;
            detail: z.ZodOptional<z.ZodString>;
            outcomes: z.ZodArray<z.ZodObject<{
                edge: z.ZodString;
                title: z.ZodString;
                detail: z.ZodOptional<z.ZodString>;
                value: z.ZodOptional<z.ZodString>;
                unit: z.ZodOptional<z.ZodString>;
                recommended: z.ZodOptional<z.ZodBoolean>;
            }, z.core.$strict>>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"from_to">;
        from: z.ZodObject<{
            kicker: z.ZodOptional<z.ZodString>;
            title: z.ZodString;
        }, z.core.$strict>;
        to: z.ZodObject<{
            kicker: z.ZodOptional<z.ZodString>;
            title: z.ZodString;
        }, z.core.$strict>;
        rows: z.ZodArray<z.ZodObject<{
            label: z.ZodString;
            icon: z.ZodOptional<z.ZodEnum<{
                [x: string]: string;
            }>>;
            note: z.ZodOptional<z.ZodString>;
            from: z.ZodString;
            to: z.ZodString;
            unit: z.ZodOptional<z.ZodString>;
            change: z.ZodOptional<z.ZodString>;
            tag: z.ZodOptional<z.ZodObject<{
                text: z.ZodString;
                quiet: z.ZodOptional<z.ZodBoolean>;
                evidence: z.ZodOptional<z.ZodEnum<{
                    label: "label";
                    draft: "draft";
                    trial: "trial";
                    company: "company";
                    press: "press";
                    official: "official";
                    registry: "registry";
                    preprint: "preprint";
                }>>;
                settled: z.ZodOptional<z.ZodBoolean>;
                tone: z.ZodOptional<z.ZodEnum<{
                    danger: "danger";
                    warning: "warning";
                    success: "success";
                }>>;
                basis: z.ZodOptional<z.ZodEnum<{
                    law: "law";
                    estimate: "estimate";
                    pending: "pending";
                    proposal: "proposal";
                }>>;
            }, z.core.$strict>>;
            emphasis: z.ZodOptional<z.ZodBoolean>;
        }, z.core.$strict>>;
        label_column: z.ZodOptional<z.ZodString>;
        span: z.ZodOptional<z.ZodString>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"org_tree">;
        root: z.ZodObject<{
            name: z.ZodString;
            role: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>;
        children: z.ZodArray<z.ZodObject<{
            name: z.ZodString;
            role: z.ZodOptional<z.ZodString>;
            children: z.ZodOptional<z.ZodArray<z.ZodObject<{
                name: z.ZodString;
                role: z.ZodOptional<z.ZodString>;
            }, z.core.$strict>>>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"issue_tree">;
        question: z.ZodString;
        children_column: z.ZodOptional<z.ZodString>;
        branches: z.ZodArray<z.ZodObject<{
            label: z.ZodString;
            note: z.ZodOptional<z.ZodString>;
            icon: z.ZodOptional<z.ZodEnum<{
                [x: string]: string;
            }>>;
            emphasis: z.ZodOptional<z.ZodLiteral<true>>;
            children: z.ZodOptional<z.ZodArray<z.ZodObject<{
                label: z.ZodString;
            }, z.core.$strict>>>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"pyramid">;
        layers: z.ZodArray<z.ZodObject<{
            label: z.ZodString;
            note: z.ZodOptional<z.ZodString>;
            tone: z.ZodOptional<z.ZodEnum<{
                danger: "danger";
                warning: "warning";
                success: "success";
            }>>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"iceberg">;
        above: z.ZodArray<z.ZodString>;
        below: z.ZodArray<z.ZodString>;
        waterline: z.ZodOptional<z.ZodString>;
        above_label: z.ZodOptional<z.ZodString>;
        below_label: z.ZodOptional<z.ZodString>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"pillar_model">;
        goal: z.ZodString;
        pillars: z.ZodArray<z.ZodObject<{
            title: z.ZodString;
            value: z.ZodString;
            unit: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>>;
        base: z.ZodString;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"value_chain">;
        primary: z.ZodArray<z.ZodObject<{
            label: z.ZodString;
            value: z.ZodOptional<z.ZodString>;
            unit: z.ZodOptional<z.ZodString>;
            emphasis: z.ZodOptional<z.ZodLiteral<true>>;
        }, z.core.$strict>>;
        support: z.ZodArray<z.ZodObject<{
            label: z.ZodString;
            note: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>>;
        margin: z.ZodOptional<z.ZodObject<{
            label: z.ZodString;
            value: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"harvey_balls">;
        criteria: z.ZodArray<z.ZodString>;
        options: z.ZodArray<z.ZodObject<{
            label: z.ZodString;
            scores: z.ZodArray<z.ZodUnion<readonly [z.ZodLiteral<0>, z.ZodLiteral<25>, z.ZodLiteral<50>, z.ZodLiteral<75>, z.ZodLiteral<100>]>>;
            total: z.ZodOptional<z.ZodUnion<readonly [z.ZodString, z.ZodNumber]>>;
            highlight: z.ZodOptional<z.ZodBoolean>;
        }, z.core.$strict>>;
        legend: z.ZodOptional<z.ZodBoolean>;
        labels: z.ZodOptional<z.ZodObject<{
            option: z.ZodOptional<z.ZodString>;
            total: z.ZodOptional<z.ZodString>;
            none: z.ZodOptional<z.ZodString>;
            partial: z.ZodOptional<z.ZodString>;
            full: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"scorecard">;
        labels: z.ZodOptional<z.ZodObject<{
            metric: z.ZodOptional<z.ZodString>;
            target: z.ZodOptional<z.ZodString>;
            actual: z.ZodOptional<z.ZodString>;
            gap: z.ZodOptional<z.ZodString>;
            status: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>>;
        rows: z.ZodArray<z.ZodObject<{
            label: z.ZodString;
            target: z.ZodString;
            actual: z.ZodString;
            gap: z.ZodString;
            status: z.ZodEnum<{
                watch: "watch";
                on_track: "on_track";
                off_track: "off_track";
            }>;
            status_label: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>>;
        note: z.ZodOptional<z.ZodString>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"pictogram">;
        rows: z.ZodArray<z.ZodObject<{
            filled: z.ZodNumber;
            label: z.ZodString;
            caption: z.ZodOptional<z.ZodString>;
            highlight: z.ZodOptional<z.ZodBoolean>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"word_cloud">;
        words: z.ZodArray<z.ZodObject<{
            text: z.ZodString;
            weight: z.ZodUnion<readonly [z.ZodLiteral<1>, z.ZodLiteral<2>, z.ZodLiteral<3>, z.ZodLiteral<4>]>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"venn">;
        sets: z.ZodArray<z.ZodObject<{
            label: z.ZodString;
        }, z.core.$strict>>;
        center: z.ZodString;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"fishbone">;
        effect: z.ZodString;
        ribs: z.ZodArray<z.ZodObject<{
            label: z.ZodString;
            causes: z.ZodArray<z.ZodString>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"positioning_map">;
        x_axis: z.ZodObject<{
            title: z.ZodString;
            low: z.ZodString;
            high: z.ZodString;
        }, z.core.$strict>;
        y_axis: z.ZodObject<{
            title: z.ZodString;
            low: z.ZodString;
            high: z.ZodString;
        }, z.core.$strict>;
        quadrants: z.ZodOptional<z.ZodObject<{
            top_left: z.ZodString;
            top_right: z.ZodString;
            bottom_left: z.ZodString;
            bottom_right: z.ZodString;
        }, z.core.$strict>>;
        points: z.ZodArray<z.ZodObject<{
            label: z.ZodString;
            x: z.ZodNumber;
            y: z.ZodNumber;
            emphasis: z.ZodOptional<z.ZodLiteral<true>>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"concept_equation">;
        operands: z.ZodArray<z.ZodObject<{
            label: z.ZodString;
            value: z.ZodOptional<z.ZodString>;
            note: z.ZodOptional<z.ZodString>;
            icon: z.ZodOptional<z.ZodEnum<{
                [x: string]: string;
            }>>;
        }, z.core.$strict>>;
        result: z.ZodObject<{
            label: z.ZodString;
            value: z.ZodOptional<z.ZodString>;
            note: z.ZodOptional<z.ZodString>;
            icon: z.ZodOptional<z.ZodEnum<{
                [x: string]: string;
            }>>;
        }, z.core.$strict>;
        excluded: z.ZodOptional<z.ZodObject<{
            label: z.ZodString;
            value: z.ZodOptional<z.ZodString>;
            note: z.ZodOptional<z.ZodString>;
            icon: z.ZodOptional<z.ZodEnum<{
                [x: string]: string;
            }>>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"segmented_wheel">;
        center: z.ZodString;
        segments: z.ZodArray<z.ZodObject<{
            label: z.ZodString;
            value: z.ZodOptional<z.ZodString>;
            emphasis: z.ZodOptional<z.ZodLiteral<true>>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"pros_cons">;
        pros: z.ZodObject<{
            title: z.ZodString;
            items: z.ZodArray<z.ZodObject<{
                label: z.ZodString;
                note: z.ZodOptional<z.ZodString>;
            }, z.core.$strict>>;
        }, z.core.$strict>;
        cons: z.ZodObject<{
            title: z.ZodString;
            items: z.ZodArray<z.ZodObject<{
                label: z.ZodString;
                note: z.ZodOptional<z.ZodString>;
            }, z.core.$strict>>;
        }, z.core.$strict>;
        verdict: z.ZodString;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"sketch">;
        kind: z.ZodEnum<{
            discontinuity: "discontinuity";
            difference_in_differences: "difference_in_differences";
        }>;
        at: z.ZodString;
        x_title: z.ZodString;
        y_title: z.ZodOptional<z.ZodString>;
        effect: z.ZodOptional<z.ZodString>;
        groups: z.ZodOptional<z.ZodArray<z.ZodString>>;
        direction: z.ZodOptional<z.ZodEnum<{
            up: "up";
            down: "down";
        }>>;
    }, z.core.$strict>], "type">>>;
    background: z.ZodOptional<z.ZodDiscriminatedUnion<[z.ZodObject<{
        kind: z.ZodLiteral<"color">;
        value: z.ZodString;
    }, z.core.$strict>, z.ZodObject<{
        kind: z.ZodLiteral<"gradient">;
        from: z.ZodString;
        to: z.ZodString;
        direction: z.ZodOptional<z.ZodEnum<{
            tb: "tb";
            lr: "lr";
            diagonal: "diagonal";
        }>>;
    }, z.core.$strict>, z.ZodObject<{
        kind: z.ZodLiteral<"asset">;
        asset_id: z.ZodString;
        overlay: z.ZodOptional<z.ZodObject<{
            color: z.ZodString;
            opacity: z.ZodNumber;
        }, z.core.$strict>>;
        fit: z.ZodOptional<z.ZodEnum<{
            cover: "cover";
            contain: "contain";
        }>>;
    }, z.core.$strict>], "kind">>;
    decor: z.ZodOptional<z.ZodObject<{
        kind: z.ZodEnum<{
            big_number: "big_number";
            corner_tag: "corner_tag";
            rule_line: "rule_line";
            quote_marks: "quote_marks";
            geo_dots: "geo_dots";
        }>;
        intensity: z.ZodOptional<z.ZodEnum<{
            subtle: "subtle";
            normal: "normal";
        }>>;
        text: z.ZodOptional<z.ZodString>;
    }, z.core.$strict>>;
    image_side: z.ZodOptional<z.ZodEnum<{
        left: "left";
        right: "right";
    }>>;
    footnote: z.ZodOptional<z.ZodString>;
    notes: z.ZodOptional<z.ZodString>;
    type: z.ZodLiteral<"cover">;
}, z.core.$strict>, z.ZodObject<{
    id: z.ZodOptional<z.ZodString>;
    placeholder: z.ZodOptional<z.ZodLiteral<true>>;
    heading: z.ZodOptional<z.ZodString>;
    subheading: z.ZodOptional<z.ZodString>;
    kicker: z.ZodOptional<z.ZodString>;
    fields: z.ZodOptional<z.ZodArray<z.ZodObject<{
        label: z.ZodString;
        value: z.ZodString;
        note: z.ZodOptional<z.ZodString>;
    }, z.core.$strict>>>;
    stamp: z.ZodOptional<z.ZodObject<{
        text: z.ZodString;
        date: z.ZodOptional<z.ZodString>;
    }, z.core.$strict>>;
    ballot: z.ZodOptional<z.ZodObject<{
        choices: z.ZodArray<z.ZodString>;
        signature: z.ZodOptional<z.ZodString>;
        item_choices: z.ZodOptional<z.ZodArray<z.ZodObject<{
            item: z.ZodNumber;
            choices: z.ZodArray<z.ZodString>;
        }, z.core.$strict>>>;
    }, z.core.$strict>>;
    tag: z.ZodOptional<z.ZodObject<{
        text: z.ZodString;
        quiet: z.ZodOptional<z.ZodBoolean>;
        evidence: z.ZodOptional<z.ZodEnum<{
            label: "label";
            draft: "draft";
            trial: "trial";
            company: "company";
            press: "press";
            official: "official";
            registry: "registry";
            preprint: "preprint";
        }>>;
        settled: z.ZodOptional<z.ZodBoolean>;
        tone: z.ZodOptional<z.ZodEnum<{
            danger: "danger";
            warning: "warning";
            success: "success";
        }>>;
        basis: z.ZodOptional<z.ZodEnum<{
            law: "law";
            estimate: "estimate";
            pending: "pending";
            proposal: "proposal";
        }>>;
    }, z.core.$strict>>;
    years: z.ZodOptional<z.ZodObject<{
        from: z.ZodNumber;
        to: z.ZodNumber;
        marked: z.ZodArray<z.ZodNumber>;
    }, z.core.$strict>>;
    stage: z.ZodOptional<z.ZodString>;
    components: z.ZodDefault<z.ZodArray<z.ZodDiscriminatedUnion<[z.ZodObject<{
        type: z.ZodLiteral<"bullets">;
        items: z.ZodArray<z.ZodString>;
        style: z.ZodOptional<z.ZodEnum<{
            default: "default";
            checklist: "checklist";
            numbered: "numbered";
            plain: "plain";
            divided: "divided";
        }>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"paragraph">;
        text: z.ZodString;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"blockquote">;
        text: z.ZodString;
        attribution: z.ZodOptional<z.ZodString>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"callout">;
        variant: z.ZodEnum<{
            info: "info";
            warn: "warn";
            tip: "tip";
        }>;
        title: z.ZodOptional<z.ZodString>;
        text: z.ZodString;
        icon: z.ZodOptional<z.ZodEnum<{
            [x: string]: string;
        }>>;
        tag: z.ZodOptional<z.ZodObject<{
            text: z.ZodString;
            quiet: z.ZodOptional<z.ZodBoolean>;
            evidence: z.ZodOptional<z.ZodEnum<{
                label: "label";
                draft: "draft";
                trial: "trial";
                company: "company";
                press: "press";
                official: "official";
                registry: "registry";
                preprint: "preprint";
            }>>;
            settled: z.ZodOptional<z.ZodBoolean>;
            tone: z.ZodOptional<z.ZodEnum<{
                danger: "danger";
                warning: "warning";
                success: "success";
            }>>;
            basis: z.ZodOptional<z.ZodEnum<{
                law: "law";
                estimate: "estimate";
                pending: "pending";
                proposal: "proposal";
            }>>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"code">;
        language: z.ZodString;
        code: z.ZodString;
        title: z.ZodOptional<z.ZodString>;
        highlight_lines: z.ZodOptional<z.ZodArray<z.ZodNumber>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"kpi_cards">;
        items: z.ZodArray<z.ZodObject<{
            value: z.ZodString;
            unit: z.ZodOptional<z.ZodString>;
            label: z.ZodString;
            note: z.ZodOptional<z.ZodString>;
            tag: z.ZodOptional<z.ZodObject<{
                text: z.ZodString;
                quiet: z.ZodOptional<z.ZodBoolean>;
                evidence: z.ZodOptional<z.ZodEnum<{
                    label: "label";
                    draft: "draft";
                    trial: "trial";
                    company: "company";
                    press: "press";
                    official: "official";
                    registry: "registry";
                    preprint: "preprint";
                }>>;
                settled: z.ZodOptional<z.ZodBoolean>;
                tone: z.ZodOptional<z.ZodEnum<{
                    danger: "danger";
                    warning: "warning";
                    success: "success";
                }>>;
                basis: z.ZodOptional<z.ZodEnum<{
                    law: "law";
                    estimate: "estimate";
                    pending: "pending";
                    proposal: "proposal";
                }>>;
            }, z.core.$strict>>;
            delta: z.ZodOptional<z.ZodEnum<{
                flat: "flat";
                up: "up";
                down: "down";
            }>>;
            delta_good: z.ZodOptional<z.ZodBoolean>;
            icon: z.ZodOptional<z.ZodEnum<{
                [x: string]: string;
            }>>;
            tone: z.ZodOptional<z.ZodEnum<{
                danger: "danger";
                warning: "warning";
                success: "success";
            }>>;
            source: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"chart">;
        title: z.ZodOptional<z.ZodString>;
        chart_type: z.ZodEnum<{
            line: "line";
            donut: "donut";
            dumbbell: "dumbbell";
            funnel: "funnel";
            gauge: "gauge";
            bar: "bar";
            stacked: "stacked";
            percent_stacked: "percent_stacked";
            pie: "pie";
            area: "area";
            combo: "combo";
            scatter: "scatter";
        }>;
        direction: z.ZodOptional<z.ZodEnum<{
            horizontal: "horizontal";
            vertical: "vertical";
        }>>;
        style: z.ZodOptional<z.ZodEnum<{
            donut: "donut";
        }>>;
        center_total: z.ZodOptional<z.ZodBoolean>;
        gauge: z.ZodOptional<z.ZodObject<{
            min: z.ZodOptional<z.ZodNumber>;
            max: z.ZodOptional<z.ZodNumber>;
        }, z.core.$strict>>;
        axes: z.ZodOptional<z.ZodObject<{
            x_title: z.ZodOptional<z.ZodString>;
            y_title: z.ZodOptional<z.ZodString>;
            x_unit: z.ZodOptional<z.ZodString>;
            y_unit: z.ZodOptional<z.ZodString>;
            y2_title: z.ZodOptional<z.ZodString>;
            y2_unit: z.ZodOptional<z.ZodString>;
            show_grid: z.ZodOptional<z.ZodBoolean>;
        }, z.core.$strict>>;
        tag: z.ZodOptional<z.ZodObject<{
            text: z.ZodString;
            quiet: z.ZodOptional<z.ZodBoolean>;
            evidence: z.ZodOptional<z.ZodEnum<{
                label: "label";
                draft: "draft";
                trial: "trial";
                company: "company";
                press: "press";
                official: "official";
                registry: "registry";
                preprint: "preprint";
            }>>;
            settled: z.ZodOptional<z.ZodBoolean>;
            tone: z.ZodOptional<z.ZodEnum<{
                danger: "danger";
                warning: "warning";
                success: "success";
            }>>;
            basis: z.ZodOptional<z.ZodEnum<{
                law: "law";
                estimate: "estimate";
                pending: "pending";
                proposal: "proposal";
            }>>;
        }, z.core.$strict>>;
        changes: z.ZodOptional<z.ZodArray<z.ZodObject<{
            from: z.ZodString;
            to: z.ZodString;
            at: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>>>;
        bands: z.ZodOptional<z.ZodArray<z.ZodObject<{
            from: z.ZodNumber;
            to: z.ZodNumber;
            label: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>>>;
        emphasis_label: z.ZodOptional<z.ZodString>;
        reference: z.ZodOptional<z.ZodObject<{
            value: z.ZodNumber;
            label: z.ZodString;
        }, z.core.$strict>>;
        markers: z.ZodOptional<z.ZodArray<z.ZodObject<{
            before: z.ZodString;
            label: z.ZodString;
        }, z.core.$strict>>>;
        gaps: z.ZodOptional<z.ZodArray<z.ZodObject<{
            after: z.ZodString;
            x: z.ZodString;
            label: z.ZodString;
        }, z.core.$strict>>>;
        series: z.ZodArray<z.ZodObject<{
            name: z.ZodString;
            data: z.ZodArray<z.ZodObject<{
                x: z.ZodUnion<readonly [z.ZodString, z.ZodNumber]>;
                y: z.ZodNumber;
                size: z.ZodOptional<z.ZodNumber>;
                status: z.ZodOptional<z.ZodEnum<{
                    target: "target";
                    estimate: "estimate";
                    forecast: "forecast";
                }>>;
                emphasis: z.ZodOptional<z.ZodBoolean>;
                note: z.ZodOptional<z.ZodString>;
                icon: z.ZodOptional<z.ZodEnum<{
                    [x: string]: string;
                }>>;
                upper: z.ZodOptional<z.ZodNumber>;
            }, z.core.$strict>>;
            plot: z.ZodOptional<z.ZodEnum<{
                line: "line";
                bar: "bar";
            }>>;
            axis: z.ZodOptional<z.ZodEnum<{
                left: "left";
                right: "right";
            }>>;
            emphasis: z.ZodOptional<z.ZodBoolean>;
            steps: z.ZodOptional<z.ZodBoolean>;
            tone: z.ZodOptional<z.ZodEnum<{
                danger: "danger";
                warning: "warning";
                success: "success";
            }>>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"flowchart">;
        nodes: z.ZodArray<z.ZodObject<{
            id: z.ZodString;
            label: z.ZodString;
            kind: z.ZodOptional<z.ZodEnum<{
                rect: "rect";
                diamond: "diamond";
                round: "round";
            }>>;
        }, z.core.$strict>>;
        edges: z.ZodArray<z.ZodObject<{
            from: z.ZodString;
            to: z.ZodString;
            label: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>>;
        direction: z.ZodOptional<z.ZodEnum<{
            TB: "TB";
            TD: "TD";
            BT: "BT";
            LR: "LR";
            RL: "RL";
        }>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"architecture">;
        layers: z.ZodArray<z.ZodObject<{
            title: z.ZodString;
            items: z.ZodArray<z.ZodString>;
        }, z.core.$strict>>;
        direction: z.ZodOptional<z.ZodEnum<{
            top_down: "top_down";
            bottom_up: "bottom_up";
        }>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"timeline">;
        title: z.ZodOptional<z.ZodString>;
        layout: z.ZodOptional<z.ZodEnum<{
            horizontal: "horizontal";
            vertical: "vertical";
        }>>;
        lanes: z.ZodOptional<z.ZodArray<z.ZodString>>;
        periods: z.ZodOptional<z.ZodArray<z.ZodObject<{
            from: z.ZodString;
            to: z.ZodString;
            label: z.ZodString;
            basis: z.ZodOptional<z.ZodEnum<{
                law: "law";
                estimate: "estimate";
                pending: "pending";
                proposal: "proposal";
            }>>;
        }, z.core.$strict>>>;
        milestones: z.ZodArray<z.ZodObject<{
            date: z.ZodString;
            title: z.ZodString;
            desc: z.ZodOptional<z.ZodString>;
            highlight: z.ZodOptional<z.ZodBoolean>;
            icon: z.ZodOptional<z.ZodEnum<{
                [x: string]: string;
            }>>;
            tone: z.ZodOptional<z.ZodEnum<{
                danger: "danger";
                warning: "warning";
                success: "success";
            }>>;
            status: z.ZodOptional<z.ZodEnum<{
                pending: "pending";
            }>>;
            tag: z.ZodOptional<z.ZodObject<{
                text: z.ZodString;
                quiet: z.ZodOptional<z.ZodBoolean>;
                evidence: z.ZodOptional<z.ZodEnum<{
                    label: "label";
                    draft: "draft";
                    trial: "trial";
                    company: "company";
                    press: "press";
                    official: "official";
                    registry: "registry";
                    preprint: "preprint";
                }>>;
                settled: z.ZodOptional<z.ZodBoolean>;
                tone: z.ZodOptional<z.ZodEnum<{
                    danger: "danger";
                    warning: "warning";
                    success: "success";
                }>>;
                basis: z.ZodOptional<z.ZodEnum<{
                    law: "law";
                    estimate: "estimate";
                    pending: "pending";
                    proposal: "proposal";
                }>>;
            }, z.core.$strict>>;
            source: z.ZodOptional<z.ZodString>;
            lane: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"comparison">;
        title: z.ZodOptional<z.ZodString>;
        columns: z.ZodArray<z.ZodString>;
        label_column: z.ZodOptional<z.ZodString>;
        rows: z.ZodArray<z.ZodObject<{
            label: z.ZodString;
            cells: z.ZodArray<z.ZodString>;
            icon: z.ZodOptional<z.ZodEnum<{
                [x: string]: string;
            }>>;
            tag: z.ZodOptional<z.ZodObject<{
                text: z.ZodString;
                quiet: z.ZodOptional<z.ZodBoolean>;
                evidence: z.ZodOptional<z.ZodEnum<{
                    label: "label";
                    draft: "draft";
                    trial: "trial";
                    company: "company";
                    press: "press";
                    official: "official";
                    registry: "registry";
                    preprint: "preprint";
                }>>;
                settled: z.ZodOptional<z.ZodBoolean>;
                tone: z.ZodOptional<z.ZodEnum<{
                    danger: "danger";
                    warning: "warning";
                    success: "success";
                }>>;
                basis: z.ZodOptional<z.ZodEnum<{
                    law: "law";
                    estimate: "estimate";
                    pending: "pending";
                    proposal: "proposal";
                }>>;
            }, z.core.$strict>>;
            emphasis: z.ZodOptional<z.ZodBoolean>;
        }, z.core.$strict>>;
        tag_column: z.ZodOptional<z.ZodString>;
        recommended: z.ZodOptional<z.ZodNumber>;
        recommended_label: z.ZodOptional<z.ZodString>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"icon_cards">;
        title: z.ZodOptional<z.ZodString>;
        items: z.ZodArray<z.ZodObject<{
            icon: z.ZodEnum<{
                [x: string]: string;
            }>;
            title: z.ZodString;
            text: z.ZodString;
            tag: z.ZodOptional<z.ZodObject<{
                text: z.ZodString;
                quiet: z.ZodOptional<z.ZodBoolean>;
                evidence: z.ZodOptional<z.ZodEnum<{
                    label: "label";
                    draft: "draft";
                    trial: "trial";
                    company: "company";
                    press: "press";
                    official: "official";
                    registry: "registry";
                    preprint: "preprint";
                }>>;
                settled: z.ZodOptional<z.ZodBoolean>;
                tone: z.ZodOptional<z.ZodEnum<{
                    danger: "danger";
                    warning: "warning";
                    success: "success";
                }>>;
                basis: z.ZodOptional<z.ZodEnum<{
                    law: "law";
                    estimate: "estimate";
                    pending: "pending";
                    proposal: "proposal";
                }>>;
            }, z.core.$strict>>;
            tone: z.ZodOptional<z.ZodEnum<{
                danger: "danger";
                warning: "warning";
                success: "success";
            }>>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"row_cards">;
        items: z.ZodArray<z.ZodObject<{
            icon: z.ZodOptional<z.ZodEnum<{
                [x: string]: string;
            }>>;
            title: z.ZodString;
            text: z.ZodOptional<z.ZodString>;
            sub: z.ZodOptional<z.ZodString>;
            highlight: z.ZodOptional<z.ZodBoolean>;
            tone: z.ZodOptional<z.ZodEnum<{
                danger: "danger";
                warning: "warning";
                success: "success";
            }>>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"steps">;
        items: z.ZodArray<z.ZodObject<{
            title: z.ZodString;
            text: z.ZodString;
            icon: z.ZodOptional<z.ZodEnum<{
                [x: string]: string;
            }>>;
            tone: z.ZodOptional<z.ZodEnum<{
                danger: "danger";
                warning: "warning";
                success: "success";
            }>>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"rings">;
        items: z.ZodArray<z.ZodObject<{
            label: z.ZodString;
            desc: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"numbered_cards">;
        items: z.ZodArray<z.ZodObject<{
            title: z.ZodString;
            text: z.ZodOptional<z.ZodString>;
            sub: z.ZodOptional<z.ZodString>;
            icon: z.ZodOptional<z.ZodEnum<{
                [x: string]: string;
            }>>;
            emphasis: z.ZodOptional<z.ZodBoolean>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"roadmap">;
        items: z.ZodArray<z.ZodObject<{
            title: z.ZodString;
            period: z.ZodOptional<z.ZodString>;
            icon: z.ZodOptional<z.ZodEnum<{
                [x: string]: string;
            }>>;
            rows: z.ZodOptional<z.ZodArray<z.ZodObject<{
                label: z.ZodString;
                value: z.ZodString;
                basis: z.ZodOptional<z.ZodEnum<{
                    law: "law";
                    estimate: "estimate";
                    pending: "pending";
                    proposal: "proposal";
                }>>;
            }, z.core.$strict>>>;
            duration: z.ZodOptional<z.ZodNumber>;
            checkpoint: z.ZodOptional<z.ZodString>;
            points: z.ZodOptional<z.ZodArray<z.ZodString>>;
            emphasis: z.ZodOptional<z.ZodBoolean>;
        }, z.core.$strict>>;
        duration_unit: z.ZodOptional<z.ZodString>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"matrix">;
        title: z.ZodOptional<z.ZodString>;
        x_title: z.ZodOptional<z.ZodString>;
        y_title: z.ZodOptional<z.ZodString>;
        cols: z.ZodNumber;
        columns: z.ZodOptional<z.ZodArray<z.ZodString>>;
        rows: z.ZodOptional<z.ZodArray<z.ZodObject<{
            label: z.ZodString;
            icon: z.ZodOptional<z.ZodEnum<{
                [x: string]: string;
            }>>;
        }, z.core.$strict>>>;
        items: z.ZodArray<z.ZodObject<{
            title: z.ZodString;
            tag: z.ZodOptional<z.ZodString>;
            tone: z.ZodOptional<z.ZodEnum<{
                info: "info";
                neutral: "neutral";
                accent: "accent";
            }>>;
            empty: z.ZodOptional<z.ZodBoolean>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"insight_panel">;
        title: z.ZodString;
        icon: z.ZodOptional<z.ZodEnum<{
            [x: string]: string;
        }>>;
        rows: z.ZodArray<z.ZodObject<{
            label: z.ZodString;
            text: z.ZodString;
        }, z.core.$strict>>;
        footnote: z.ZodOptional<z.ZodString>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"verdict_banner">;
        text: z.ZodString;
        tone: z.ZodEnum<{
            warning: "warning";
            positive: "positive";
            neutral: "neutral";
        }>;
        icon: z.ZodOptional<z.ZodEnum<{
            [x: string]: string;
        }>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"image">;
        asset_id: z.ZodString;
        caption: z.ZodOptional<z.ZodString>;
        fit: z.ZodDefault<z.ZodEnum<{
            cover: "cover";
            contain: "contain";
        }>>;
        crop: z.ZodOptional<z.ZodArray<z.ZodNumber>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"image_grid">;
        items: z.ZodArray<z.ZodObject<{
            asset_id: z.ZodString;
            caption: z.ZodOptional<z.ZodString>;
            icon: z.ZodOptional<z.ZodEnum<{
                [x: string]: string;
            }>>;
            tag: z.ZodOptional<z.ZodObject<{
                text: z.ZodString;
                quiet: z.ZodOptional<z.ZodBoolean>;
                evidence: z.ZodOptional<z.ZodEnum<{
                    label: "label";
                    draft: "draft";
                    trial: "trial";
                    company: "company";
                    press: "press";
                    official: "official";
                    registry: "registry";
                    preprint: "preprint";
                }>>;
                settled: z.ZodOptional<z.ZodBoolean>;
                tone: z.ZodOptional<z.ZodEnum<{
                    danger: "danger";
                    warning: "warning";
                    success: "success";
                }>>;
                basis: z.ZodOptional<z.ZodEnum<{
                    law: "law";
                    estimate: "estimate";
                    pending: "pending";
                    proposal: "proposal";
                }>>;
            }, z.core.$strict>>;
            crop: z.ZodOptional<z.ZodArray<z.ZodNumber>>;
        }, z.core.$strict>>;
        emphasis: z.ZodOptional<z.ZodEnum<{
            none: "none";
            first: "first";
        }>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"image_compare">;
        left: z.ZodObject<{
            asset_id: z.ZodString;
            label: z.ZodString;
        }, z.core.$strict>;
        right: z.ZodObject<{
            asset_id: z.ZodString;
            label: z.ZodString;
        }, z.core.$strict>;
        style: z.ZodOptional<z.ZodEnum<{
            vs: "vs";
            before_after: "before_after";
        }>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"logo_wall">;
        title: z.ZodOptional<z.ZodString>;
        items: z.ZodArray<z.ZodObject<{
            name: z.ZodString;
            asset_id: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"product_cards">;
        items: z.ZodArray<z.ZodObject<{
            asset_id: z.ZodString;
            name: z.ZodString;
            note: z.ZodOptional<z.ZodString>;
            price: z.ZodOptional<z.ZodString>;
            price_unit: z.ZodOptional<z.ZodString>;
            featured: z.ZodOptional<z.ZodLiteral<true>>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"quote_wall">;
        quotes: z.ZodArray<z.ZodObject<{
            text: z.ZodString;
            name: z.ZodString;
            role: z.ZodOptional<z.ZodString>;
            featured: z.ZodOptional<z.ZodLiteral<true>>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"swot">;
        strengths: z.ZodArray<z.ZodString>;
        weaknesses: z.ZodArray<z.ZodString>;
        opportunities: z.ZodArray<z.ZodString>;
        threats: z.ZodArray<z.ZodString>;
        labels: z.ZodOptional<z.ZodObject<{
            strengths: z.ZodOptional<z.ZodString>;
            weaknesses: z.ZodOptional<z.ZodString>;
            opportunities: z.ZodOptional<z.ZodString>;
            threats: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"bmc">;
        key_partners: z.ZodArray<z.ZodString>;
        key_activities: z.ZodArray<z.ZodString>;
        key_resources: z.ZodArray<z.ZodString>;
        value_propositions: z.ZodArray<z.ZodString>;
        customer_relationships: z.ZodArray<z.ZodString>;
        channels: z.ZodArray<z.ZodString>;
        customer_segments: z.ZodArray<z.ZodString>;
        cost_structure: z.ZodArray<z.ZodString>;
        revenue_streams: z.ZodArray<z.ZodString>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"waterfall">;
        title: z.ZodOptional<z.ZodString>;
        items: z.ZodArray<z.ZodObject<{
            label: z.ZodString;
            value: z.ZodNumber;
            kind: z.ZodOptional<z.ZodEnum<{
                delta: "delta";
                total: "total";
            }>>;
            note: z.ZodOptional<z.ZodString>;
            emphasis: z.ZodOptional<z.ZodBoolean>;
        }, z.core.$strict>>;
        unit: z.ZodOptional<z.ZodString>;
        emphasis_label: z.ZodOptional<z.ZodString>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"gantt">;
        items: z.ZodArray<z.ZodObject<{
            label: z.ZodString;
            start: z.ZodNumber;
            end: z.ZodNumber;
            text: z.ZodOptional<z.ZodString>;
            emphasis: z.ZodOptional<z.ZodBoolean>;
            icon: z.ZodOptional<z.ZodEnum<{
                [x: string]: string;
            }>>;
            period: z.ZodOptional<z.ZodString>;
            basis: z.ZodOptional<z.ZodEnum<{
                law: "law";
                estimate: "estimate";
                pending: "pending";
                proposal: "proposal";
            }>>;
        }, z.core.$strict>>;
        axis_labels: z.ZodOptional<z.ZodArray<z.ZodString>>;
        range: z.ZodOptional<z.ZodObject<{
            from: z.ZodNumber;
            to: z.ZodNumber;
        }, z.core.$strict>>;
        milestones: z.ZodOptional<z.ZodArray<z.ZodObject<{
            at: z.ZodNumber;
            label: z.ZodString;
        }, z.core.$strict>>>;
        bands: z.ZodOptional<z.ZodArray<z.ZodObject<{
            from: z.ZodNumber;
            to: z.ZodNumber;
            label: z.ZodString;
        }, z.core.$strict>>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"pest">;
        political: z.ZodObject<{
            title: z.ZodOptional<z.ZodString>;
            items: z.ZodArray<z.ZodString>;
        }, z.core.$strict>;
        economic: z.ZodObject<{
            title: z.ZodOptional<z.ZodString>;
            items: z.ZodArray<z.ZodString>;
        }, z.core.$strict>;
        social: z.ZodObject<{
            title: z.ZodOptional<z.ZodString>;
            items: z.ZodArray<z.ZodString>;
        }, z.core.$strict>;
        technological: z.ZodObject<{
            title: z.ZodOptional<z.ZodString>;
            items: z.ZodArray<z.ZodString>;
        }, z.core.$strict>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"five_forces">;
        rivalry: z.ZodObject<{
            label: z.ZodOptional<z.ZodString>;
            intensity: z.ZodOptional<z.ZodEnum<{
                low: "low";
                medium: "medium";
                high: "high";
            }>>;
            items: z.ZodArray<z.ZodString>;
        }, z.core.$strict>;
        new_entrants: z.ZodObject<{
            label: z.ZodOptional<z.ZodString>;
            intensity: z.ZodOptional<z.ZodEnum<{
                low: "low";
                medium: "medium";
                high: "high";
            }>>;
            items: z.ZodArray<z.ZodString>;
        }, z.core.$strict>;
        supplier_power: z.ZodObject<{
            label: z.ZodOptional<z.ZodString>;
            intensity: z.ZodOptional<z.ZodEnum<{
                low: "low";
                medium: "medium";
                high: "high";
            }>>;
            items: z.ZodArray<z.ZodString>;
        }, z.core.$strict>;
        buyer_power: z.ZodObject<{
            label: z.ZodOptional<z.ZodString>;
            intensity: z.ZodOptional<z.ZodEnum<{
                low: "low";
                medium: "medium";
                high: "high";
            }>>;
            items: z.ZodArray<z.ZodString>;
        }, z.core.$strict>;
        substitutes: z.ZodObject<{
            label: z.ZodOptional<z.ZodString>;
            intensity: z.ZodOptional<z.ZodEnum<{
                low: "low";
                medium: "medium";
                high: "high";
            }>>;
            items: z.ZodArray<z.ZodString>;
        }, z.core.$strict>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"heatmap">;
        x_labels: z.ZodArray<z.ZodString>;
        y_labels: z.ZodArray<z.ZodString>;
        values: z.ZodArray<z.ZodArray<z.ZodNumber>>;
        domain: z.ZodOptional<z.ZodObject<{
            min: z.ZodNumber;
            max: z.ZodNumber;
        }, z.core.$strict>>;
        show_values: z.ZodOptional<z.ZodBoolean>;
        x_title: z.ZodOptional<z.ZodString>;
        y_title: z.ZodOptional<z.ZodString>;
        label_every: z.ZodOptional<z.ZodNumber>;
        steps: z.ZodOptional<z.ZodArray<z.ZodObject<{
            max: z.ZodOptional<z.ZodNumber>;
            label: z.ZodString;
            short: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>>>;
        bands: z.ZodOptional<z.ZodArray<z.ZodObject<{
            from: z.ZodString;
            to: z.ZodString;
            label: z.ZodString;
            icon: z.ZodOptional<z.ZodEnum<{
                [x: string]: string;
            }>>;
        }, z.core.$strict>>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"sankey">;
        nodes: z.ZodArray<z.ZodObject<{
            id: z.ZodString;
            label: z.ZodString;
        }, z.core.$strict>>;
        links: z.ZodArray<z.ZodObject<{
            from: z.ZodString;
            to: z.ZodString;
            value: z.ZodNumber;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"data_table">;
        title: z.ZodOptional<z.ZodString>;
        columns: z.ZodArray<z.ZodObject<{
            key: z.ZodString;
            label: z.ZodString;
            align: z.ZodOptional<z.ZodEnum<{
                left: "left";
                right: "right";
                center: "center";
            }>>;
            emphasis: z.ZodOptional<z.ZodBoolean>;
            icon: z.ZodOptional<z.ZodEnum<{
                [x: string]: string;
            }>>;
        }, z.core.$strict>>;
        rows: z.ZodArray<z.ZodObject<{
            cells: z.ZodRecord<z.ZodString, z.ZodUnion<readonly [z.ZodString, z.ZodNumber]>>;
            emphasis: z.ZodOptional<z.ZodEnum<{
                highlight: "highlight";
                total: "total";
            }>>;
            icon: z.ZodOptional<z.ZodEnum<{
                [x: string]: string;
            }>>;
            tag: z.ZodOptional<z.ZodObject<{
                text: z.ZodString;
                quiet: z.ZodOptional<z.ZodBoolean>;
                evidence: z.ZodOptional<z.ZodEnum<{
                    label: "label";
                    draft: "draft";
                    trial: "trial";
                    company: "company";
                    press: "press";
                    official: "official";
                    registry: "registry";
                    preprint: "preprint";
                }>>;
                settled: z.ZodOptional<z.ZodBoolean>;
                tone: z.ZodOptional<z.ZodEnum<{
                    danger: "danger";
                    warning: "warning";
                    success: "success";
                }>>;
                basis: z.ZodOptional<z.ZodEnum<{
                    law: "law";
                    estimate: "estimate";
                    pending: "pending";
                    proposal: "proposal";
                }>>;
            }, z.core.$strict>>;
        }, z.core.$strict>>;
        source: z.ZodOptional<z.ZodString>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"device_mockup">;
        device: z.ZodEnum<{
            phone: "phone";
            browser: "browser";
        }>;
        asset_id: z.ZodString;
        caption: z.ZodOptional<z.ZodString>;
        url: z.ZodOptional<z.ZodString>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"cycle">;
        title: z.ZodOptional<z.ZodString>;
        items: z.ZodArray<z.ZodObject<{
            label: z.ZodString;
            description: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"people_cards">;
        title: z.ZodOptional<z.ZodString>;
        people: z.ZodArray<z.ZodObject<{
            name: z.ZodString;
            role: z.ZodOptional<z.ZodString>;
            org: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"hub_spoke">;
        center: z.ZodString;
        items: z.ZodArray<z.ZodObject<{
            label: z.ZodString;
            description: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"progress_donuts">;
        items: z.ZodArray<z.ZodObject<{
            value: z.ZodString;
            unit: z.ZodOptional<z.ZodString>;
            label: z.ZodString;
            icon: z.ZodOptional<z.ZodEnum<{
                [x: string]: string;
            }>>;
            source: z.ZodOptional<z.ZodString>;
            detail: z.ZodOptional<z.ZodString>;
            emphasis: z.ZodOptional<z.ZodBoolean>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"staircase">;
        items: z.ZodArray<z.ZodObject<{
            title: z.ZodString;
            value: z.ZodString;
            unit: z.ZodOptional<z.ZodString>;
            note: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"chevron_process">;
        items: z.ZodArray<z.ZodObject<{
            title: z.ZodString;
            text: z.ZodOptional<z.ZodString>;
            icon: z.ZodOptional<z.ZodEnum<{
                [x: string]: string;
            }>>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"swimlane">;
        lanes: z.ZodArray<z.ZodObject<{
            label: z.ZodString;
            role: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>>;
        steps: z.ZodArray<z.ZodObject<{
            lane: z.ZodString;
            title: z.ZodString;
            detail: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>>;
        handoff_note: z.ZodOptional<z.ZodString>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"journey_map">;
        stages: z.ZodArray<z.ZodObject<{
            label: z.ZodString;
            touchpoints: z.ZodOptional<z.ZodArray<z.ZodString>>;
            action: z.ZodOptional<z.ZodString>;
            emotion: z.ZodNumber;
            opportunity: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>>;
        row_labels: z.ZodOptional<z.ZodObject<{
            touchpoints: z.ZodOptional<z.ZodString>;
            action: z.ZodOptional<z.ZodString>;
            emotion: z.ZodOptional<z.ZodString>;
            opportunity: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"decision_tree">;
        question: z.ZodString;
        branches: z.ZodArray<z.ZodObject<{
            edge: z.ZodString;
            title: z.ZodString;
            detail: z.ZodOptional<z.ZodString>;
            outcomes: z.ZodArray<z.ZodObject<{
                edge: z.ZodString;
                title: z.ZodString;
                detail: z.ZodOptional<z.ZodString>;
                value: z.ZodOptional<z.ZodString>;
                unit: z.ZodOptional<z.ZodString>;
                recommended: z.ZodOptional<z.ZodBoolean>;
            }, z.core.$strict>>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"from_to">;
        from: z.ZodObject<{
            kicker: z.ZodOptional<z.ZodString>;
            title: z.ZodString;
        }, z.core.$strict>;
        to: z.ZodObject<{
            kicker: z.ZodOptional<z.ZodString>;
            title: z.ZodString;
        }, z.core.$strict>;
        rows: z.ZodArray<z.ZodObject<{
            label: z.ZodString;
            icon: z.ZodOptional<z.ZodEnum<{
                [x: string]: string;
            }>>;
            note: z.ZodOptional<z.ZodString>;
            from: z.ZodString;
            to: z.ZodString;
            unit: z.ZodOptional<z.ZodString>;
            change: z.ZodOptional<z.ZodString>;
            tag: z.ZodOptional<z.ZodObject<{
                text: z.ZodString;
                quiet: z.ZodOptional<z.ZodBoolean>;
                evidence: z.ZodOptional<z.ZodEnum<{
                    label: "label";
                    draft: "draft";
                    trial: "trial";
                    company: "company";
                    press: "press";
                    official: "official";
                    registry: "registry";
                    preprint: "preprint";
                }>>;
                settled: z.ZodOptional<z.ZodBoolean>;
                tone: z.ZodOptional<z.ZodEnum<{
                    danger: "danger";
                    warning: "warning";
                    success: "success";
                }>>;
                basis: z.ZodOptional<z.ZodEnum<{
                    law: "law";
                    estimate: "estimate";
                    pending: "pending";
                    proposal: "proposal";
                }>>;
            }, z.core.$strict>>;
            emphasis: z.ZodOptional<z.ZodBoolean>;
        }, z.core.$strict>>;
        label_column: z.ZodOptional<z.ZodString>;
        span: z.ZodOptional<z.ZodString>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"org_tree">;
        root: z.ZodObject<{
            name: z.ZodString;
            role: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>;
        children: z.ZodArray<z.ZodObject<{
            name: z.ZodString;
            role: z.ZodOptional<z.ZodString>;
            children: z.ZodOptional<z.ZodArray<z.ZodObject<{
                name: z.ZodString;
                role: z.ZodOptional<z.ZodString>;
            }, z.core.$strict>>>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"issue_tree">;
        question: z.ZodString;
        children_column: z.ZodOptional<z.ZodString>;
        branches: z.ZodArray<z.ZodObject<{
            label: z.ZodString;
            note: z.ZodOptional<z.ZodString>;
            icon: z.ZodOptional<z.ZodEnum<{
                [x: string]: string;
            }>>;
            emphasis: z.ZodOptional<z.ZodLiteral<true>>;
            children: z.ZodOptional<z.ZodArray<z.ZodObject<{
                label: z.ZodString;
            }, z.core.$strict>>>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"pyramid">;
        layers: z.ZodArray<z.ZodObject<{
            label: z.ZodString;
            note: z.ZodOptional<z.ZodString>;
            tone: z.ZodOptional<z.ZodEnum<{
                danger: "danger";
                warning: "warning";
                success: "success";
            }>>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"iceberg">;
        above: z.ZodArray<z.ZodString>;
        below: z.ZodArray<z.ZodString>;
        waterline: z.ZodOptional<z.ZodString>;
        above_label: z.ZodOptional<z.ZodString>;
        below_label: z.ZodOptional<z.ZodString>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"pillar_model">;
        goal: z.ZodString;
        pillars: z.ZodArray<z.ZodObject<{
            title: z.ZodString;
            value: z.ZodString;
            unit: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>>;
        base: z.ZodString;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"value_chain">;
        primary: z.ZodArray<z.ZodObject<{
            label: z.ZodString;
            value: z.ZodOptional<z.ZodString>;
            unit: z.ZodOptional<z.ZodString>;
            emphasis: z.ZodOptional<z.ZodLiteral<true>>;
        }, z.core.$strict>>;
        support: z.ZodArray<z.ZodObject<{
            label: z.ZodString;
            note: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>>;
        margin: z.ZodOptional<z.ZodObject<{
            label: z.ZodString;
            value: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"harvey_balls">;
        criteria: z.ZodArray<z.ZodString>;
        options: z.ZodArray<z.ZodObject<{
            label: z.ZodString;
            scores: z.ZodArray<z.ZodUnion<readonly [z.ZodLiteral<0>, z.ZodLiteral<25>, z.ZodLiteral<50>, z.ZodLiteral<75>, z.ZodLiteral<100>]>>;
            total: z.ZodOptional<z.ZodUnion<readonly [z.ZodString, z.ZodNumber]>>;
            highlight: z.ZodOptional<z.ZodBoolean>;
        }, z.core.$strict>>;
        legend: z.ZodOptional<z.ZodBoolean>;
        labels: z.ZodOptional<z.ZodObject<{
            option: z.ZodOptional<z.ZodString>;
            total: z.ZodOptional<z.ZodString>;
            none: z.ZodOptional<z.ZodString>;
            partial: z.ZodOptional<z.ZodString>;
            full: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"scorecard">;
        labels: z.ZodOptional<z.ZodObject<{
            metric: z.ZodOptional<z.ZodString>;
            target: z.ZodOptional<z.ZodString>;
            actual: z.ZodOptional<z.ZodString>;
            gap: z.ZodOptional<z.ZodString>;
            status: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>>;
        rows: z.ZodArray<z.ZodObject<{
            label: z.ZodString;
            target: z.ZodString;
            actual: z.ZodString;
            gap: z.ZodString;
            status: z.ZodEnum<{
                watch: "watch";
                on_track: "on_track";
                off_track: "off_track";
            }>;
            status_label: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>>;
        note: z.ZodOptional<z.ZodString>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"pictogram">;
        rows: z.ZodArray<z.ZodObject<{
            filled: z.ZodNumber;
            label: z.ZodString;
            caption: z.ZodOptional<z.ZodString>;
            highlight: z.ZodOptional<z.ZodBoolean>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"word_cloud">;
        words: z.ZodArray<z.ZodObject<{
            text: z.ZodString;
            weight: z.ZodUnion<readonly [z.ZodLiteral<1>, z.ZodLiteral<2>, z.ZodLiteral<3>, z.ZodLiteral<4>]>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"venn">;
        sets: z.ZodArray<z.ZodObject<{
            label: z.ZodString;
        }, z.core.$strict>>;
        center: z.ZodString;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"fishbone">;
        effect: z.ZodString;
        ribs: z.ZodArray<z.ZodObject<{
            label: z.ZodString;
            causes: z.ZodArray<z.ZodString>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"positioning_map">;
        x_axis: z.ZodObject<{
            title: z.ZodString;
            low: z.ZodString;
            high: z.ZodString;
        }, z.core.$strict>;
        y_axis: z.ZodObject<{
            title: z.ZodString;
            low: z.ZodString;
            high: z.ZodString;
        }, z.core.$strict>;
        quadrants: z.ZodOptional<z.ZodObject<{
            top_left: z.ZodString;
            top_right: z.ZodString;
            bottom_left: z.ZodString;
            bottom_right: z.ZodString;
        }, z.core.$strict>>;
        points: z.ZodArray<z.ZodObject<{
            label: z.ZodString;
            x: z.ZodNumber;
            y: z.ZodNumber;
            emphasis: z.ZodOptional<z.ZodLiteral<true>>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"concept_equation">;
        operands: z.ZodArray<z.ZodObject<{
            label: z.ZodString;
            value: z.ZodOptional<z.ZodString>;
            note: z.ZodOptional<z.ZodString>;
            icon: z.ZodOptional<z.ZodEnum<{
                [x: string]: string;
            }>>;
        }, z.core.$strict>>;
        result: z.ZodObject<{
            label: z.ZodString;
            value: z.ZodOptional<z.ZodString>;
            note: z.ZodOptional<z.ZodString>;
            icon: z.ZodOptional<z.ZodEnum<{
                [x: string]: string;
            }>>;
        }, z.core.$strict>;
        excluded: z.ZodOptional<z.ZodObject<{
            label: z.ZodString;
            value: z.ZodOptional<z.ZodString>;
            note: z.ZodOptional<z.ZodString>;
            icon: z.ZodOptional<z.ZodEnum<{
                [x: string]: string;
            }>>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"segmented_wheel">;
        center: z.ZodString;
        segments: z.ZodArray<z.ZodObject<{
            label: z.ZodString;
            value: z.ZodOptional<z.ZodString>;
            emphasis: z.ZodOptional<z.ZodLiteral<true>>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"pros_cons">;
        pros: z.ZodObject<{
            title: z.ZodString;
            items: z.ZodArray<z.ZodObject<{
                label: z.ZodString;
                note: z.ZodOptional<z.ZodString>;
            }, z.core.$strict>>;
        }, z.core.$strict>;
        cons: z.ZodObject<{
            title: z.ZodString;
            items: z.ZodArray<z.ZodObject<{
                label: z.ZodString;
                note: z.ZodOptional<z.ZodString>;
            }, z.core.$strict>>;
        }, z.core.$strict>;
        verdict: z.ZodString;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"sketch">;
        kind: z.ZodEnum<{
            discontinuity: "discontinuity";
            difference_in_differences: "difference_in_differences";
        }>;
        at: z.ZodString;
        x_title: z.ZodString;
        y_title: z.ZodOptional<z.ZodString>;
        effect: z.ZodOptional<z.ZodString>;
        groups: z.ZodOptional<z.ZodArray<z.ZodString>>;
        direction: z.ZodOptional<z.ZodEnum<{
            up: "up";
            down: "down";
        }>>;
    }, z.core.$strict>], "type">>>;
    background: z.ZodOptional<z.ZodDiscriminatedUnion<[z.ZodObject<{
        kind: z.ZodLiteral<"color">;
        value: z.ZodString;
    }, z.core.$strict>, z.ZodObject<{
        kind: z.ZodLiteral<"gradient">;
        from: z.ZodString;
        to: z.ZodString;
        direction: z.ZodOptional<z.ZodEnum<{
            tb: "tb";
            lr: "lr";
            diagonal: "diagonal";
        }>>;
    }, z.core.$strict>, z.ZodObject<{
        kind: z.ZodLiteral<"asset">;
        asset_id: z.ZodString;
        overlay: z.ZodOptional<z.ZodObject<{
            color: z.ZodString;
            opacity: z.ZodNumber;
        }, z.core.$strict>>;
        fit: z.ZodOptional<z.ZodEnum<{
            cover: "cover";
            contain: "contain";
        }>>;
    }, z.core.$strict>], "kind">>;
    decor: z.ZodOptional<z.ZodObject<{
        kind: z.ZodEnum<{
            big_number: "big_number";
            corner_tag: "corner_tag";
            rule_line: "rule_line";
            quote_marks: "quote_marks";
            geo_dots: "geo_dots";
        }>;
        intensity: z.ZodOptional<z.ZodEnum<{
            subtle: "subtle";
            normal: "normal";
        }>>;
        text: z.ZodOptional<z.ZodString>;
    }, z.core.$strict>>;
    image_side: z.ZodOptional<z.ZodEnum<{
        left: "left";
        right: "right";
    }>>;
    footnote: z.ZodOptional<z.ZodString>;
    notes: z.ZodOptional<z.ZodString>;
    type: z.ZodLiteral<"chapter">;
}, z.core.$strict>, z.ZodObject<{
    id: z.ZodOptional<z.ZodString>;
    placeholder: z.ZodOptional<z.ZodLiteral<true>>;
    heading: z.ZodOptional<z.ZodString>;
    subheading: z.ZodOptional<z.ZodString>;
    kicker: z.ZodOptional<z.ZodString>;
    fields: z.ZodOptional<z.ZodArray<z.ZodObject<{
        label: z.ZodString;
        value: z.ZodString;
        note: z.ZodOptional<z.ZodString>;
    }, z.core.$strict>>>;
    stamp: z.ZodOptional<z.ZodObject<{
        text: z.ZodString;
        date: z.ZodOptional<z.ZodString>;
    }, z.core.$strict>>;
    ballot: z.ZodOptional<z.ZodObject<{
        choices: z.ZodArray<z.ZodString>;
        signature: z.ZodOptional<z.ZodString>;
        item_choices: z.ZodOptional<z.ZodArray<z.ZodObject<{
            item: z.ZodNumber;
            choices: z.ZodArray<z.ZodString>;
        }, z.core.$strict>>>;
    }, z.core.$strict>>;
    tag: z.ZodOptional<z.ZodObject<{
        text: z.ZodString;
        quiet: z.ZodOptional<z.ZodBoolean>;
        evidence: z.ZodOptional<z.ZodEnum<{
            label: "label";
            draft: "draft";
            trial: "trial";
            company: "company";
            press: "press";
            official: "official";
            registry: "registry";
            preprint: "preprint";
        }>>;
        settled: z.ZodOptional<z.ZodBoolean>;
        tone: z.ZodOptional<z.ZodEnum<{
            danger: "danger";
            warning: "warning";
            success: "success";
        }>>;
        basis: z.ZodOptional<z.ZodEnum<{
            law: "law";
            estimate: "estimate";
            pending: "pending";
            proposal: "proposal";
        }>>;
    }, z.core.$strict>>;
    years: z.ZodOptional<z.ZodObject<{
        from: z.ZodNumber;
        to: z.ZodNumber;
        marked: z.ZodArray<z.ZodNumber>;
    }, z.core.$strict>>;
    stage: z.ZodOptional<z.ZodString>;
    components: z.ZodDefault<z.ZodArray<z.ZodDiscriminatedUnion<[z.ZodObject<{
        type: z.ZodLiteral<"bullets">;
        items: z.ZodArray<z.ZodString>;
        style: z.ZodOptional<z.ZodEnum<{
            default: "default";
            checklist: "checklist";
            numbered: "numbered";
            plain: "plain";
            divided: "divided";
        }>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"paragraph">;
        text: z.ZodString;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"blockquote">;
        text: z.ZodString;
        attribution: z.ZodOptional<z.ZodString>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"callout">;
        variant: z.ZodEnum<{
            info: "info";
            warn: "warn";
            tip: "tip";
        }>;
        title: z.ZodOptional<z.ZodString>;
        text: z.ZodString;
        icon: z.ZodOptional<z.ZodEnum<{
            [x: string]: string;
        }>>;
        tag: z.ZodOptional<z.ZodObject<{
            text: z.ZodString;
            quiet: z.ZodOptional<z.ZodBoolean>;
            evidence: z.ZodOptional<z.ZodEnum<{
                label: "label";
                draft: "draft";
                trial: "trial";
                company: "company";
                press: "press";
                official: "official";
                registry: "registry";
                preprint: "preprint";
            }>>;
            settled: z.ZodOptional<z.ZodBoolean>;
            tone: z.ZodOptional<z.ZodEnum<{
                danger: "danger";
                warning: "warning";
                success: "success";
            }>>;
            basis: z.ZodOptional<z.ZodEnum<{
                law: "law";
                estimate: "estimate";
                pending: "pending";
                proposal: "proposal";
            }>>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"code">;
        language: z.ZodString;
        code: z.ZodString;
        title: z.ZodOptional<z.ZodString>;
        highlight_lines: z.ZodOptional<z.ZodArray<z.ZodNumber>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"kpi_cards">;
        items: z.ZodArray<z.ZodObject<{
            value: z.ZodString;
            unit: z.ZodOptional<z.ZodString>;
            label: z.ZodString;
            note: z.ZodOptional<z.ZodString>;
            tag: z.ZodOptional<z.ZodObject<{
                text: z.ZodString;
                quiet: z.ZodOptional<z.ZodBoolean>;
                evidence: z.ZodOptional<z.ZodEnum<{
                    label: "label";
                    draft: "draft";
                    trial: "trial";
                    company: "company";
                    press: "press";
                    official: "official";
                    registry: "registry";
                    preprint: "preprint";
                }>>;
                settled: z.ZodOptional<z.ZodBoolean>;
                tone: z.ZodOptional<z.ZodEnum<{
                    danger: "danger";
                    warning: "warning";
                    success: "success";
                }>>;
                basis: z.ZodOptional<z.ZodEnum<{
                    law: "law";
                    estimate: "estimate";
                    pending: "pending";
                    proposal: "proposal";
                }>>;
            }, z.core.$strict>>;
            delta: z.ZodOptional<z.ZodEnum<{
                flat: "flat";
                up: "up";
                down: "down";
            }>>;
            delta_good: z.ZodOptional<z.ZodBoolean>;
            icon: z.ZodOptional<z.ZodEnum<{
                [x: string]: string;
            }>>;
            tone: z.ZodOptional<z.ZodEnum<{
                danger: "danger";
                warning: "warning";
                success: "success";
            }>>;
            source: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"chart">;
        title: z.ZodOptional<z.ZodString>;
        chart_type: z.ZodEnum<{
            line: "line";
            donut: "donut";
            dumbbell: "dumbbell";
            funnel: "funnel";
            gauge: "gauge";
            bar: "bar";
            stacked: "stacked";
            percent_stacked: "percent_stacked";
            pie: "pie";
            area: "area";
            combo: "combo";
            scatter: "scatter";
        }>;
        direction: z.ZodOptional<z.ZodEnum<{
            horizontal: "horizontal";
            vertical: "vertical";
        }>>;
        style: z.ZodOptional<z.ZodEnum<{
            donut: "donut";
        }>>;
        center_total: z.ZodOptional<z.ZodBoolean>;
        gauge: z.ZodOptional<z.ZodObject<{
            min: z.ZodOptional<z.ZodNumber>;
            max: z.ZodOptional<z.ZodNumber>;
        }, z.core.$strict>>;
        axes: z.ZodOptional<z.ZodObject<{
            x_title: z.ZodOptional<z.ZodString>;
            y_title: z.ZodOptional<z.ZodString>;
            x_unit: z.ZodOptional<z.ZodString>;
            y_unit: z.ZodOptional<z.ZodString>;
            y2_title: z.ZodOptional<z.ZodString>;
            y2_unit: z.ZodOptional<z.ZodString>;
            show_grid: z.ZodOptional<z.ZodBoolean>;
        }, z.core.$strict>>;
        tag: z.ZodOptional<z.ZodObject<{
            text: z.ZodString;
            quiet: z.ZodOptional<z.ZodBoolean>;
            evidence: z.ZodOptional<z.ZodEnum<{
                label: "label";
                draft: "draft";
                trial: "trial";
                company: "company";
                press: "press";
                official: "official";
                registry: "registry";
                preprint: "preprint";
            }>>;
            settled: z.ZodOptional<z.ZodBoolean>;
            tone: z.ZodOptional<z.ZodEnum<{
                danger: "danger";
                warning: "warning";
                success: "success";
            }>>;
            basis: z.ZodOptional<z.ZodEnum<{
                law: "law";
                estimate: "estimate";
                pending: "pending";
                proposal: "proposal";
            }>>;
        }, z.core.$strict>>;
        changes: z.ZodOptional<z.ZodArray<z.ZodObject<{
            from: z.ZodString;
            to: z.ZodString;
            at: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>>>;
        bands: z.ZodOptional<z.ZodArray<z.ZodObject<{
            from: z.ZodNumber;
            to: z.ZodNumber;
            label: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>>>;
        emphasis_label: z.ZodOptional<z.ZodString>;
        reference: z.ZodOptional<z.ZodObject<{
            value: z.ZodNumber;
            label: z.ZodString;
        }, z.core.$strict>>;
        markers: z.ZodOptional<z.ZodArray<z.ZodObject<{
            before: z.ZodString;
            label: z.ZodString;
        }, z.core.$strict>>>;
        gaps: z.ZodOptional<z.ZodArray<z.ZodObject<{
            after: z.ZodString;
            x: z.ZodString;
            label: z.ZodString;
        }, z.core.$strict>>>;
        series: z.ZodArray<z.ZodObject<{
            name: z.ZodString;
            data: z.ZodArray<z.ZodObject<{
                x: z.ZodUnion<readonly [z.ZodString, z.ZodNumber]>;
                y: z.ZodNumber;
                size: z.ZodOptional<z.ZodNumber>;
                status: z.ZodOptional<z.ZodEnum<{
                    target: "target";
                    estimate: "estimate";
                    forecast: "forecast";
                }>>;
                emphasis: z.ZodOptional<z.ZodBoolean>;
                note: z.ZodOptional<z.ZodString>;
                icon: z.ZodOptional<z.ZodEnum<{
                    [x: string]: string;
                }>>;
                upper: z.ZodOptional<z.ZodNumber>;
            }, z.core.$strict>>;
            plot: z.ZodOptional<z.ZodEnum<{
                line: "line";
                bar: "bar";
            }>>;
            axis: z.ZodOptional<z.ZodEnum<{
                left: "left";
                right: "right";
            }>>;
            emphasis: z.ZodOptional<z.ZodBoolean>;
            steps: z.ZodOptional<z.ZodBoolean>;
            tone: z.ZodOptional<z.ZodEnum<{
                danger: "danger";
                warning: "warning";
                success: "success";
            }>>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"flowchart">;
        nodes: z.ZodArray<z.ZodObject<{
            id: z.ZodString;
            label: z.ZodString;
            kind: z.ZodOptional<z.ZodEnum<{
                rect: "rect";
                diamond: "diamond";
                round: "round";
            }>>;
        }, z.core.$strict>>;
        edges: z.ZodArray<z.ZodObject<{
            from: z.ZodString;
            to: z.ZodString;
            label: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>>;
        direction: z.ZodOptional<z.ZodEnum<{
            TB: "TB";
            TD: "TD";
            BT: "BT";
            LR: "LR";
            RL: "RL";
        }>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"architecture">;
        layers: z.ZodArray<z.ZodObject<{
            title: z.ZodString;
            items: z.ZodArray<z.ZodString>;
        }, z.core.$strict>>;
        direction: z.ZodOptional<z.ZodEnum<{
            top_down: "top_down";
            bottom_up: "bottom_up";
        }>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"timeline">;
        title: z.ZodOptional<z.ZodString>;
        layout: z.ZodOptional<z.ZodEnum<{
            horizontal: "horizontal";
            vertical: "vertical";
        }>>;
        lanes: z.ZodOptional<z.ZodArray<z.ZodString>>;
        periods: z.ZodOptional<z.ZodArray<z.ZodObject<{
            from: z.ZodString;
            to: z.ZodString;
            label: z.ZodString;
            basis: z.ZodOptional<z.ZodEnum<{
                law: "law";
                estimate: "estimate";
                pending: "pending";
                proposal: "proposal";
            }>>;
        }, z.core.$strict>>>;
        milestones: z.ZodArray<z.ZodObject<{
            date: z.ZodString;
            title: z.ZodString;
            desc: z.ZodOptional<z.ZodString>;
            highlight: z.ZodOptional<z.ZodBoolean>;
            icon: z.ZodOptional<z.ZodEnum<{
                [x: string]: string;
            }>>;
            tone: z.ZodOptional<z.ZodEnum<{
                danger: "danger";
                warning: "warning";
                success: "success";
            }>>;
            status: z.ZodOptional<z.ZodEnum<{
                pending: "pending";
            }>>;
            tag: z.ZodOptional<z.ZodObject<{
                text: z.ZodString;
                quiet: z.ZodOptional<z.ZodBoolean>;
                evidence: z.ZodOptional<z.ZodEnum<{
                    label: "label";
                    draft: "draft";
                    trial: "trial";
                    company: "company";
                    press: "press";
                    official: "official";
                    registry: "registry";
                    preprint: "preprint";
                }>>;
                settled: z.ZodOptional<z.ZodBoolean>;
                tone: z.ZodOptional<z.ZodEnum<{
                    danger: "danger";
                    warning: "warning";
                    success: "success";
                }>>;
                basis: z.ZodOptional<z.ZodEnum<{
                    law: "law";
                    estimate: "estimate";
                    pending: "pending";
                    proposal: "proposal";
                }>>;
            }, z.core.$strict>>;
            source: z.ZodOptional<z.ZodString>;
            lane: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"comparison">;
        title: z.ZodOptional<z.ZodString>;
        columns: z.ZodArray<z.ZodString>;
        label_column: z.ZodOptional<z.ZodString>;
        rows: z.ZodArray<z.ZodObject<{
            label: z.ZodString;
            cells: z.ZodArray<z.ZodString>;
            icon: z.ZodOptional<z.ZodEnum<{
                [x: string]: string;
            }>>;
            tag: z.ZodOptional<z.ZodObject<{
                text: z.ZodString;
                quiet: z.ZodOptional<z.ZodBoolean>;
                evidence: z.ZodOptional<z.ZodEnum<{
                    label: "label";
                    draft: "draft";
                    trial: "trial";
                    company: "company";
                    press: "press";
                    official: "official";
                    registry: "registry";
                    preprint: "preprint";
                }>>;
                settled: z.ZodOptional<z.ZodBoolean>;
                tone: z.ZodOptional<z.ZodEnum<{
                    danger: "danger";
                    warning: "warning";
                    success: "success";
                }>>;
                basis: z.ZodOptional<z.ZodEnum<{
                    law: "law";
                    estimate: "estimate";
                    pending: "pending";
                    proposal: "proposal";
                }>>;
            }, z.core.$strict>>;
            emphasis: z.ZodOptional<z.ZodBoolean>;
        }, z.core.$strict>>;
        tag_column: z.ZodOptional<z.ZodString>;
        recommended: z.ZodOptional<z.ZodNumber>;
        recommended_label: z.ZodOptional<z.ZodString>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"icon_cards">;
        title: z.ZodOptional<z.ZodString>;
        items: z.ZodArray<z.ZodObject<{
            icon: z.ZodEnum<{
                [x: string]: string;
            }>;
            title: z.ZodString;
            text: z.ZodString;
            tag: z.ZodOptional<z.ZodObject<{
                text: z.ZodString;
                quiet: z.ZodOptional<z.ZodBoolean>;
                evidence: z.ZodOptional<z.ZodEnum<{
                    label: "label";
                    draft: "draft";
                    trial: "trial";
                    company: "company";
                    press: "press";
                    official: "official";
                    registry: "registry";
                    preprint: "preprint";
                }>>;
                settled: z.ZodOptional<z.ZodBoolean>;
                tone: z.ZodOptional<z.ZodEnum<{
                    danger: "danger";
                    warning: "warning";
                    success: "success";
                }>>;
                basis: z.ZodOptional<z.ZodEnum<{
                    law: "law";
                    estimate: "estimate";
                    pending: "pending";
                    proposal: "proposal";
                }>>;
            }, z.core.$strict>>;
            tone: z.ZodOptional<z.ZodEnum<{
                danger: "danger";
                warning: "warning";
                success: "success";
            }>>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"row_cards">;
        items: z.ZodArray<z.ZodObject<{
            icon: z.ZodOptional<z.ZodEnum<{
                [x: string]: string;
            }>>;
            title: z.ZodString;
            text: z.ZodOptional<z.ZodString>;
            sub: z.ZodOptional<z.ZodString>;
            highlight: z.ZodOptional<z.ZodBoolean>;
            tone: z.ZodOptional<z.ZodEnum<{
                danger: "danger";
                warning: "warning";
                success: "success";
            }>>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"steps">;
        items: z.ZodArray<z.ZodObject<{
            title: z.ZodString;
            text: z.ZodString;
            icon: z.ZodOptional<z.ZodEnum<{
                [x: string]: string;
            }>>;
            tone: z.ZodOptional<z.ZodEnum<{
                danger: "danger";
                warning: "warning";
                success: "success";
            }>>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"rings">;
        items: z.ZodArray<z.ZodObject<{
            label: z.ZodString;
            desc: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"numbered_cards">;
        items: z.ZodArray<z.ZodObject<{
            title: z.ZodString;
            text: z.ZodOptional<z.ZodString>;
            sub: z.ZodOptional<z.ZodString>;
            icon: z.ZodOptional<z.ZodEnum<{
                [x: string]: string;
            }>>;
            emphasis: z.ZodOptional<z.ZodBoolean>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"roadmap">;
        items: z.ZodArray<z.ZodObject<{
            title: z.ZodString;
            period: z.ZodOptional<z.ZodString>;
            icon: z.ZodOptional<z.ZodEnum<{
                [x: string]: string;
            }>>;
            rows: z.ZodOptional<z.ZodArray<z.ZodObject<{
                label: z.ZodString;
                value: z.ZodString;
                basis: z.ZodOptional<z.ZodEnum<{
                    law: "law";
                    estimate: "estimate";
                    pending: "pending";
                    proposal: "proposal";
                }>>;
            }, z.core.$strict>>>;
            duration: z.ZodOptional<z.ZodNumber>;
            checkpoint: z.ZodOptional<z.ZodString>;
            points: z.ZodOptional<z.ZodArray<z.ZodString>>;
            emphasis: z.ZodOptional<z.ZodBoolean>;
        }, z.core.$strict>>;
        duration_unit: z.ZodOptional<z.ZodString>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"matrix">;
        title: z.ZodOptional<z.ZodString>;
        x_title: z.ZodOptional<z.ZodString>;
        y_title: z.ZodOptional<z.ZodString>;
        cols: z.ZodNumber;
        columns: z.ZodOptional<z.ZodArray<z.ZodString>>;
        rows: z.ZodOptional<z.ZodArray<z.ZodObject<{
            label: z.ZodString;
            icon: z.ZodOptional<z.ZodEnum<{
                [x: string]: string;
            }>>;
        }, z.core.$strict>>>;
        items: z.ZodArray<z.ZodObject<{
            title: z.ZodString;
            tag: z.ZodOptional<z.ZodString>;
            tone: z.ZodOptional<z.ZodEnum<{
                info: "info";
                neutral: "neutral";
                accent: "accent";
            }>>;
            empty: z.ZodOptional<z.ZodBoolean>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"insight_panel">;
        title: z.ZodString;
        icon: z.ZodOptional<z.ZodEnum<{
            [x: string]: string;
        }>>;
        rows: z.ZodArray<z.ZodObject<{
            label: z.ZodString;
            text: z.ZodString;
        }, z.core.$strict>>;
        footnote: z.ZodOptional<z.ZodString>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"verdict_banner">;
        text: z.ZodString;
        tone: z.ZodEnum<{
            warning: "warning";
            positive: "positive";
            neutral: "neutral";
        }>;
        icon: z.ZodOptional<z.ZodEnum<{
            [x: string]: string;
        }>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"image">;
        asset_id: z.ZodString;
        caption: z.ZodOptional<z.ZodString>;
        fit: z.ZodDefault<z.ZodEnum<{
            cover: "cover";
            contain: "contain";
        }>>;
        crop: z.ZodOptional<z.ZodArray<z.ZodNumber>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"image_grid">;
        items: z.ZodArray<z.ZodObject<{
            asset_id: z.ZodString;
            caption: z.ZodOptional<z.ZodString>;
            icon: z.ZodOptional<z.ZodEnum<{
                [x: string]: string;
            }>>;
            tag: z.ZodOptional<z.ZodObject<{
                text: z.ZodString;
                quiet: z.ZodOptional<z.ZodBoolean>;
                evidence: z.ZodOptional<z.ZodEnum<{
                    label: "label";
                    draft: "draft";
                    trial: "trial";
                    company: "company";
                    press: "press";
                    official: "official";
                    registry: "registry";
                    preprint: "preprint";
                }>>;
                settled: z.ZodOptional<z.ZodBoolean>;
                tone: z.ZodOptional<z.ZodEnum<{
                    danger: "danger";
                    warning: "warning";
                    success: "success";
                }>>;
                basis: z.ZodOptional<z.ZodEnum<{
                    law: "law";
                    estimate: "estimate";
                    pending: "pending";
                    proposal: "proposal";
                }>>;
            }, z.core.$strict>>;
            crop: z.ZodOptional<z.ZodArray<z.ZodNumber>>;
        }, z.core.$strict>>;
        emphasis: z.ZodOptional<z.ZodEnum<{
            none: "none";
            first: "first";
        }>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"image_compare">;
        left: z.ZodObject<{
            asset_id: z.ZodString;
            label: z.ZodString;
        }, z.core.$strict>;
        right: z.ZodObject<{
            asset_id: z.ZodString;
            label: z.ZodString;
        }, z.core.$strict>;
        style: z.ZodOptional<z.ZodEnum<{
            vs: "vs";
            before_after: "before_after";
        }>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"logo_wall">;
        title: z.ZodOptional<z.ZodString>;
        items: z.ZodArray<z.ZodObject<{
            name: z.ZodString;
            asset_id: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"product_cards">;
        items: z.ZodArray<z.ZodObject<{
            asset_id: z.ZodString;
            name: z.ZodString;
            note: z.ZodOptional<z.ZodString>;
            price: z.ZodOptional<z.ZodString>;
            price_unit: z.ZodOptional<z.ZodString>;
            featured: z.ZodOptional<z.ZodLiteral<true>>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"quote_wall">;
        quotes: z.ZodArray<z.ZodObject<{
            text: z.ZodString;
            name: z.ZodString;
            role: z.ZodOptional<z.ZodString>;
            featured: z.ZodOptional<z.ZodLiteral<true>>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"swot">;
        strengths: z.ZodArray<z.ZodString>;
        weaknesses: z.ZodArray<z.ZodString>;
        opportunities: z.ZodArray<z.ZodString>;
        threats: z.ZodArray<z.ZodString>;
        labels: z.ZodOptional<z.ZodObject<{
            strengths: z.ZodOptional<z.ZodString>;
            weaknesses: z.ZodOptional<z.ZodString>;
            opportunities: z.ZodOptional<z.ZodString>;
            threats: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"bmc">;
        key_partners: z.ZodArray<z.ZodString>;
        key_activities: z.ZodArray<z.ZodString>;
        key_resources: z.ZodArray<z.ZodString>;
        value_propositions: z.ZodArray<z.ZodString>;
        customer_relationships: z.ZodArray<z.ZodString>;
        channels: z.ZodArray<z.ZodString>;
        customer_segments: z.ZodArray<z.ZodString>;
        cost_structure: z.ZodArray<z.ZodString>;
        revenue_streams: z.ZodArray<z.ZodString>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"waterfall">;
        title: z.ZodOptional<z.ZodString>;
        items: z.ZodArray<z.ZodObject<{
            label: z.ZodString;
            value: z.ZodNumber;
            kind: z.ZodOptional<z.ZodEnum<{
                delta: "delta";
                total: "total";
            }>>;
            note: z.ZodOptional<z.ZodString>;
            emphasis: z.ZodOptional<z.ZodBoolean>;
        }, z.core.$strict>>;
        unit: z.ZodOptional<z.ZodString>;
        emphasis_label: z.ZodOptional<z.ZodString>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"gantt">;
        items: z.ZodArray<z.ZodObject<{
            label: z.ZodString;
            start: z.ZodNumber;
            end: z.ZodNumber;
            text: z.ZodOptional<z.ZodString>;
            emphasis: z.ZodOptional<z.ZodBoolean>;
            icon: z.ZodOptional<z.ZodEnum<{
                [x: string]: string;
            }>>;
            period: z.ZodOptional<z.ZodString>;
            basis: z.ZodOptional<z.ZodEnum<{
                law: "law";
                estimate: "estimate";
                pending: "pending";
                proposal: "proposal";
            }>>;
        }, z.core.$strict>>;
        axis_labels: z.ZodOptional<z.ZodArray<z.ZodString>>;
        range: z.ZodOptional<z.ZodObject<{
            from: z.ZodNumber;
            to: z.ZodNumber;
        }, z.core.$strict>>;
        milestones: z.ZodOptional<z.ZodArray<z.ZodObject<{
            at: z.ZodNumber;
            label: z.ZodString;
        }, z.core.$strict>>>;
        bands: z.ZodOptional<z.ZodArray<z.ZodObject<{
            from: z.ZodNumber;
            to: z.ZodNumber;
            label: z.ZodString;
        }, z.core.$strict>>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"pest">;
        political: z.ZodObject<{
            title: z.ZodOptional<z.ZodString>;
            items: z.ZodArray<z.ZodString>;
        }, z.core.$strict>;
        economic: z.ZodObject<{
            title: z.ZodOptional<z.ZodString>;
            items: z.ZodArray<z.ZodString>;
        }, z.core.$strict>;
        social: z.ZodObject<{
            title: z.ZodOptional<z.ZodString>;
            items: z.ZodArray<z.ZodString>;
        }, z.core.$strict>;
        technological: z.ZodObject<{
            title: z.ZodOptional<z.ZodString>;
            items: z.ZodArray<z.ZodString>;
        }, z.core.$strict>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"five_forces">;
        rivalry: z.ZodObject<{
            label: z.ZodOptional<z.ZodString>;
            intensity: z.ZodOptional<z.ZodEnum<{
                low: "low";
                medium: "medium";
                high: "high";
            }>>;
            items: z.ZodArray<z.ZodString>;
        }, z.core.$strict>;
        new_entrants: z.ZodObject<{
            label: z.ZodOptional<z.ZodString>;
            intensity: z.ZodOptional<z.ZodEnum<{
                low: "low";
                medium: "medium";
                high: "high";
            }>>;
            items: z.ZodArray<z.ZodString>;
        }, z.core.$strict>;
        supplier_power: z.ZodObject<{
            label: z.ZodOptional<z.ZodString>;
            intensity: z.ZodOptional<z.ZodEnum<{
                low: "low";
                medium: "medium";
                high: "high";
            }>>;
            items: z.ZodArray<z.ZodString>;
        }, z.core.$strict>;
        buyer_power: z.ZodObject<{
            label: z.ZodOptional<z.ZodString>;
            intensity: z.ZodOptional<z.ZodEnum<{
                low: "low";
                medium: "medium";
                high: "high";
            }>>;
            items: z.ZodArray<z.ZodString>;
        }, z.core.$strict>;
        substitutes: z.ZodObject<{
            label: z.ZodOptional<z.ZodString>;
            intensity: z.ZodOptional<z.ZodEnum<{
                low: "low";
                medium: "medium";
                high: "high";
            }>>;
            items: z.ZodArray<z.ZodString>;
        }, z.core.$strict>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"heatmap">;
        x_labels: z.ZodArray<z.ZodString>;
        y_labels: z.ZodArray<z.ZodString>;
        values: z.ZodArray<z.ZodArray<z.ZodNumber>>;
        domain: z.ZodOptional<z.ZodObject<{
            min: z.ZodNumber;
            max: z.ZodNumber;
        }, z.core.$strict>>;
        show_values: z.ZodOptional<z.ZodBoolean>;
        x_title: z.ZodOptional<z.ZodString>;
        y_title: z.ZodOptional<z.ZodString>;
        label_every: z.ZodOptional<z.ZodNumber>;
        steps: z.ZodOptional<z.ZodArray<z.ZodObject<{
            max: z.ZodOptional<z.ZodNumber>;
            label: z.ZodString;
            short: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>>>;
        bands: z.ZodOptional<z.ZodArray<z.ZodObject<{
            from: z.ZodString;
            to: z.ZodString;
            label: z.ZodString;
            icon: z.ZodOptional<z.ZodEnum<{
                [x: string]: string;
            }>>;
        }, z.core.$strict>>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"sankey">;
        nodes: z.ZodArray<z.ZodObject<{
            id: z.ZodString;
            label: z.ZodString;
        }, z.core.$strict>>;
        links: z.ZodArray<z.ZodObject<{
            from: z.ZodString;
            to: z.ZodString;
            value: z.ZodNumber;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"data_table">;
        title: z.ZodOptional<z.ZodString>;
        columns: z.ZodArray<z.ZodObject<{
            key: z.ZodString;
            label: z.ZodString;
            align: z.ZodOptional<z.ZodEnum<{
                left: "left";
                right: "right";
                center: "center";
            }>>;
            emphasis: z.ZodOptional<z.ZodBoolean>;
            icon: z.ZodOptional<z.ZodEnum<{
                [x: string]: string;
            }>>;
        }, z.core.$strict>>;
        rows: z.ZodArray<z.ZodObject<{
            cells: z.ZodRecord<z.ZodString, z.ZodUnion<readonly [z.ZodString, z.ZodNumber]>>;
            emphasis: z.ZodOptional<z.ZodEnum<{
                highlight: "highlight";
                total: "total";
            }>>;
            icon: z.ZodOptional<z.ZodEnum<{
                [x: string]: string;
            }>>;
            tag: z.ZodOptional<z.ZodObject<{
                text: z.ZodString;
                quiet: z.ZodOptional<z.ZodBoolean>;
                evidence: z.ZodOptional<z.ZodEnum<{
                    label: "label";
                    draft: "draft";
                    trial: "trial";
                    company: "company";
                    press: "press";
                    official: "official";
                    registry: "registry";
                    preprint: "preprint";
                }>>;
                settled: z.ZodOptional<z.ZodBoolean>;
                tone: z.ZodOptional<z.ZodEnum<{
                    danger: "danger";
                    warning: "warning";
                    success: "success";
                }>>;
                basis: z.ZodOptional<z.ZodEnum<{
                    law: "law";
                    estimate: "estimate";
                    pending: "pending";
                    proposal: "proposal";
                }>>;
            }, z.core.$strict>>;
        }, z.core.$strict>>;
        source: z.ZodOptional<z.ZodString>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"device_mockup">;
        device: z.ZodEnum<{
            phone: "phone";
            browser: "browser";
        }>;
        asset_id: z.ZodString;
        caption: z.ZodOptional<z.ZodString>;
        url: z.ZodOptional<z.ZodString>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"cycle">;
        title: z.ZodOptional<z.ZodString>;
        items: z.ZodArray<z.ZodObject<{
            label: z.ZodString;
            description: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"people_cards">;
        title: z.ZodOptional<z.ZodString>;
        people: z.ZodArray<z.ZodObject<{
            name: z.ZodString;
            role: z.ZodOptional<z.ZodString>;
            org: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"hub_spoke">;
        center: z.ZodString;
        items: z.ZodArray<z.ZodObject<{
            label: z.ZodString;
            description: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"progress_donuts">;
        items: z.ZodArray<z.ZodObject<{
            value: z.ZodString;
            unit: z.ZodOptional<z.ZodString>;
            label: z.ZodString;
            icon: z.ZodOptional<z.ZodEnum<{
                [x: string]: string;
            }>>;
            source: z.ZodOptional<z.ZodString>;
            detail: z.ZodOptional<z.ZodString>;
            emphasis: z.ZodOptional<z.ZodBoolean>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"staircase">;
        items: z.ZodArray<z.ZodObject<{
            title: z.ZodString;
            value: z.ZodString;
            unit: z.ZodOptional<z.ZodString>;
            note: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"chevron_process">;
        items: z.ZodArray<z.ZodObject<{
            title: z.ZodString;
            text: z.ZodOptional<z.ZodString>;
            icon: z.ZodOptional<z.ZodEnum<{
                [x: string]: string;
            }>>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"swimlane">;
        lanes: z.ZodArray<z.ZodObject<{
            label: z.ZodString;
            role: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>>;
        steps: z.ZodArray<z.ZodObject<{
            lane: z.ZodString;
            title: z.ZodString;
            detail: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>>;
        handoff_note: z.ZodOptional<z.ZodString>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"journey_map">;
        stages: z.ZodArray<z.ZodObject<{
            label: z.ZodString;
            touchpoints: z.ZodOptional<z.ZodArray<z.ZodString>>;
            action: z.ZodOptional<z.ZodString>;
            emotion: z.ZodNumber;
            opportunity: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>>;
        row_labels: z.ZodOptional<z.ZodObject<{
            touchpoints: z.ZodOptional<z.ZodString>;
            action: z.ZodOptional<z.ZodString>;
            emotion: z.ZodOptional<z.ZodString>;
            opportunity: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"decision_tree">;
        question: z.ZodString;
        branches: z.ZodArray<z.ZodObject<{
            edge: z.ZodString;
            title: z.ZodString;
            detail: z.ZodOptional<z.ZodString>;
            outcomes: z.ZodArray<z.ZodObject<{
                edge: z.ZodString;
                title: z.ZodString;
                detail: z.ZodOptional<z.ZodString>;
                value: z.ZodOptional<z.ZodString>;
                unit: z.ZodOptional<z.ZodString>;
                recommended: z.ZodOptional<z.ZodBoolean>;
            }, z.core.$strict>>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"from_to">;
        from: z.ZodObject<{
            kicker: z.ZodOptional<z.ZodString>;
            title: z.ZodString;
        }, z.core.$strict>;
        to: z.ZodObject<{
            kicker: z.ZodOptional<z.ZodString>;
            title: z.ZodString;
        }, z.core.$strict>;
        rows: z.ZodArray<z.ZodObject<{
            label: z.ZodString;
            icon: z.ZodOptional<z.ZodEnum<{
                [x: string]: string;
            }>>;
            note: z.ZodOptional<z.ZodString>;
            from: z.ZodString;
            to: z.ZodString;
            unit: z.ZodOptional<z.ZodString>;
            change: z.ZodOptional<z.ZodString>;
            tag: z.ZodOptional<z.ZodObject<{
                text: z.ZodString;
                quiet: z.ZodOptional<z.ZodBoolean>;
                evidence: z.ZodOptional<z.ZodEnum<{
                    label: "label";
                    draft: "draft";
                    trial: "trial";
                    company: "company";
                    press: "press";
                    official: "official";
                    registry: "registry";
                    preprint: "preprint";
                }>>;
                settled: z.ZodOptional<z.ZodBoolean>;
                tone: z.ZodOptional<z.ZodEnum<{
                    danger: "danger";
                    warning: "warning";
                    success: "success";
                }>>;
                basis: z.ZodOptional<z.ZodEnum<{
                    law: "law";
                    estimate: "estimate";
                    pending: "pending";
                    proposal: "proposal";
                }>>;
            }, z.core.$strict>>;
            emphasis: z.ZodOptional<z.ZodBoolean>;
        }, z.core.$strict>>;
        label_column: z.ZodOptional<z.ZodString>;
        span: z.ZodOptional<z.ZodString>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"org_tree">;
        root: z.ZodObject<{
            name: z.ZodString;
            role: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>;
        children: z.ZodArray<z.ZodObject<{
            name: z.ZodString;
            role: z.ZodOptional<z.ZodString>;
            children: z.ZodOptional<z.ZodArray<z.ZodObject<{
                name: z.ZodString;
                role: z.ZodOptional<z.ZodString>;
            }, z.core.$strict>>>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"issue_tree">;
        question: z.ZodString;
        children_column: z.ZodOptional<z.ZodString>;
        branches: z.ZodArray<z.ZodObject<{
            label: z.ZodString;
            note: z.ZodOptional<z.ZodString>;
            icon: z.ZodOptional<z.ZodEnum<{
                [x: string]: string;
            }>>;
            emphasis: z.ZodOptional<z.ZodLiteral<true>>;
            children: z.ZodOptional<z.ZodArray<z.ZodObject<{
                label: z.ZodString;
            }, z.core.$strict>>>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"pyramid">;
        layers: z.ZodArray<z.ZodObject<{
            label: z.ZodString;
            note: z.ZodOptional<z.ZodString>;
            tone: z.ZodOptional<z.ZodEnum<{
                danger: "danger";
                warning: "warning";
                success: "success";
            }>>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"iceberg">;
        above: z.ZodArray<z.ZodString>;
        below: z.ZodArray<z.ZodString>;
        waterline: z.ZodOptional<z.ZodString>;
        above_label: z.ZodOptional<z.ZodString>;
        below_label: z.ZodOptional<z.ZodString>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"pillar_model">;
        goal: z.ZodString;
        pillars: z.ZodArray<z.ZodObject<{
            title: z.ZodString;
            value: z.ZodString;
            unit: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>>;
        base: z.ZodString;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"value_chain">;
        primary: z.ZodArray<z.ZodObject<{
            label: z.ZodString;
            value: z.ZodOptional<z.ZodString>;
            unit: z.ZodOptional<z.ZodString>;
            emphasis: z.ZodOptional<z.ZodLiteral<true>>;
        }, z.core.$strict>>;
        support: z.ZodArray<z.ZodObject<{
            label: z.ZodString;
            note: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>>;
        margin: z.ZodOptional<z.ZodObject<{
            label: z.ZodString;
            value: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"harvey_balls">;
        criteria: z.ZodArray<z.ZodString>;
        options: z.ZodArray<z.ZodObject<{
            label: z.ZodString;
            scores: z.ZodArray<z.ZodUnion<readonly [z.ZodLiteral<0>, z.ZodLiteral<25>, z.ZodLiteral<50>, z.ZodLiteral<75>, z.ZodLiteral<100>]>>;
            total: z.ZodOptional<z.ZodUnion<readonly [z.ZodString, z.ZodNumber]>>;
            highlight: z.ZodOptional<z.ZodBoolean>;
        }, z.core.$strict>>;
        legend: z.ZodOptional<z.ZodBoolean>;
        labels: z.ZodOptional<z.ZodObject<{
            option: z.ZodOptional<z.ZodString>;
            total: z.ZodOptional<z.ZodString>;
            none: z.ZodOptional<z.ZodString>;
            partial: z.ZodOptional<z.ZodString>;
            full: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"scorecard">;
        labels: z.ZodOptional<z.ZodObject<{
            metric: z.ZodOptional<z.ZodString>;
            target: z.ZodOptional<z.ZodString>;
            actual: z.ZodOptional<z.ZodString>;
            gap: z.ZodOptional<z.ZodString>;
            status: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>>;
        rows: z.ZodArray<z.ZodObject<{
            label: z.ZodString;
            target: z.ZodString;
            actual: z.ZodString;
            gap: z.ZodString;
            status: z.ZodEnum<{
                watch: "watch";
                on_track: "on_track";
                off_track: "off_track";
            }>;
            status_label: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>>;
        note: z.ZodOptional<z.ZodString>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"pictogram">;
        rows: z.ZodArray<z.ZodObject<{
            filled: z.ZodNumber;
            label: z.ZodString;
            caption: z.ZodOptional<z.ZodString>;
            highlight: z.ZodOptional<z.ZodBoolean>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"word_cloud">;
        words: z.ZodArray<z.ZodObject<{
            text: z.ZodString;
            weight: z.ZodUnion<readonly [z.ZodLiteral<1>, z.ZodLiteral<2>, z.ZodLiteral<3>, z.ZodLiteral<4>]>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"venn">;
        sets: z.ZodArray<z.ZodObject<{
            label: z.ZodString;
        }, z.core.$strict>>;
        center: z.ZodString;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"fishbone">;
        effect: z.ZodString;
        ribs: z.ZodArray<z.ZodObject<{
            label: z.ZodString;
            causes: z.ZodArray<z.ZodString>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"positioning_map">;
        x_axis: z.ZodObject<{
            title: z.ZodString;
            low: z.ZodString;
            high: z.ZodString;
        }, z.core.$strict>;
        y_axis: z.ZodObject<{
            title: z.ZodString;
            low: z.ZodString;
            high: z.ZodString;
        }, z.core.$strict>;
        quadrants: z.ZodOptional<z.ZodObject<{
            top_left: z.ZodString;
            top_right: z.ZodString;
            bottom_left: z.ZodString;
            bottom_right: z.ZodString;
        }, z.core.$strict>>;
        points: z.ZodArray<z.ZodObject<{
            label: z.ZodString;
            x: z.ZodNumber;
            y: z.ZodNumber;
            emphasis: z.ZodOptional<z.ZodLiteral<true>>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"concept_equation">;
        operands: z.ZodArray<z.ZodObject<{
            label: z.ZodString;
            value: z.ZodOptional<z.ZodString>;
            note: z.ZodOptional<z.ZodString>;
            icon: z.ZodOptional<z.ZodEnum<{
                [x: string]: string;
            }>>;
        }, z.core.$strict>>;
        result: z.ZodObject<{
            label: z.ZodString;
            value: z.ZodOptional<z.ZodString>;
            note: z.ZodOptional<z.ZodString>;
            icon: z.ZodOptional<z.ZodEnum<{
                [x: string]: string;
            }>>;
        }, z.core.$strict>;
        excluded: z.ZodOptional<z.ZodObject<{
            label: z.ZodString;
            value: z.ZodOptional<z.ZodString>;
            note: z.ZodOptional<z.ZodString>;
            icon: z.ZodOptional<z.ZodEnum<{
                [x: string]: string;
            }>>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"segmented_wheel">;
        center: z.ZodString;
        segments: z.ZodArray<z.ZodObject<{
            label: z.ZodString;
            value: z.ZodOptional<z.ZodString>;
            emphasis: z.ZodOptional<z.ZodLiteral<true>>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"pros_cons">;
        pros: z.ZodObject<{
            title: z.ZodString;
            items: z.ZodArray<z.ZodObject<{
                label: z.ZodString;
                note: z.ZodOptional<z.ZodString>;
            }, z.core.$strict>>;
        }, z.core.$strict>;
        cons: z.ZodObject<{
            title: z.ZodString;
            items: z.ZodArray<z.ZodObject<{
                label: z.ZodString;
                note: z.ZodOptional<z.ZodString>;
            }, z.core.$strict>>;
        }, z.core.$strict>;
        verdict: z.ZodString;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"sketch">;
        kind: z.ZodEnum<{
            discontinuity: "discontinuity";
            difference_in_differences: "difference_in_differences";
        }>;
        at: z.ZodString;
        x_title: z.ZodString;
        y_title: z.ZodOptional<z.ZodString>;
        effect: z.ZodOptional<z.ZodString>;
        groups: z.ZodOptional<z.ZodArray<z.ZodString>>;
        direction: z.ZodOptional<z.ZodEnum<{
            up: "up";
            down: "down";
        }>>;
    }, z.core.$strict>], "type">>>;
    background: z.ZodOptional<z.ZodDiscriminatedUnion<[z.ZodObject<{
        kind: z.ZodLiteral<"color">;
        value: z.ZodString;
    }, z.core.$strict>, z.ZodObject<{
        kind: z.ZodLiteral<"gradient">;
        from: z.ZodString;
        to: z.ZodString;
        direction: z.ZodOptional<z.ZodEnum<{
            tb: "tb";
            lr: "lr";
            diagonal: "diagonal";
        }>>;
    }, z.core.$strict>, z.ZodObject<{
        kind: z.ZodLiteral<"asset">;
        asset_id: z.ZodString;
        overlay: z.ZodOptional<z.ZodObject<{
            color: z.ZodString;
            opacity: z.ZodNumber;
        }, z.core.$strict>>;
        fit: z.ZodOptional<z.ZodEnum<{
            cover: "cover";
            contain: "contain";
        }>>;
    }, z.core.$strict>], "kind">>;
    decor: z.ZodOptional<z.ZodObject<{
        kind: z.ZodEnum<{
            big_number: "big_number";
            corner_tag: "corner_tag";
            rule_line: "rule_line";
            quote_marks: "quote_marks";
            geo_dots: "geo_dots";
        }>;
        intensity: z.ZodOptional<z.ZodEnum<{
            subtle: "subtle";
            normal: "normal";
        }>>;
        text: z.ZodOptional<z.ZodString>;
    }, z.core.$strict>>;
    image_side: z.ZodOptional<z.ZodEnum<{
        left: "left";
        right: "right";
    }>>;
    footnote: z.ZodOptional<z.ZodString>;
    notes: z.ZodOptional<z.ZodString>;
    type: z.ZodLiteral<"content">;
    kind: z.ZodEnum<{
        points: "points";
        list: "list";
        comparison: "comparison";
        process: "process";
        data: "data";
        photo: "photo";
        statement: "statement";
        quote: "quote";
        fact: "fact";
        evidence: "evidence";
        hierarchy: "hierarchy";
    }>;
}, z.core.$strict>, z.ZodObject<{
    id: z.ZodOptional<z.ZodString>;
    placeholder: z.ZodOptional<z.ZodLiteral<true>>;
    heading: z.ZodOptional<z.ZodString>;
    subheading: z.ZodOptional<z.ZodString>;
    kicker: z.ZodOptional<z.ZodString>;
    fields: z.ZodOptional<z.ZodArray<z.ZodObject<{
        label: z.ZodString;
        value: z.ZodString;
        note: z.ZodOptional<z.ZodString>;
    }, z.core.$strict>>>;
    stamp: z.ZodOptional<z.ZodObject<{
        text: z.ZodString;
        date: z.ZodOptional<z.ZodString>;
    }, z.core.$strict>>;
    ballot: z.ZodOptional<z.ZodObject<{
        choices: z.ZodArray<z.ZodString>;
        signature: z.ZodOptional<z.ZodString>;
        item_choices: z.ZodOptional<z.ZodArray<z.ZodObject<{
            item: z.ZodNumber;
            choices: z.ZodArray<z.ZodString>;
        }, z.core.$strict>>>;
    }, z.core.$strict>>;
    tag: z.ZodOptional<z.ZodObject<{
        text: z.ZodString;
        quiet: z.ZodOptional<z.ZodBoolean>;
        evidence: z.ZodOptional<z.ZodEnum<{
            label: "label";
            draft: "draft";
            trial: "trial";
            company: "company";
            press: "press";
            official: "official";
            registry: "registry";
            preprint: "preprint";
        }>>;
        settled: z.ZodOptional<z.ZodBoolean>;
        tone: z.ZodOptional<z.ZodEnum<{
            danger: "danger";
            warning: "warning";
            success: "success";
        }>>;
        basis: z.ZodOptional<z.ZodEnum<{
            law: "law";
            estimate: "estimate";
            pending: "pending";
            proposal: "proposal";
        }>>;
    }, z.core.$strict>>;
    years: z.ZodOptional<z.ZodObject<{
        from: z.ZodNumber;
        to: z.ZodNumber;
        marked: z.ZodArray<z.ZodNumber>;
    }, z.core.$strict>>;
    stage: z.ZodOptional<z.ZodString>;
    components: z.ZodDefault<z.ZodArray<z.ZodDiscriminatedUnion<[z.ZodObject<{
        type: z.ZodLiteral<"bullets">;
        items: z.ZodArray<z.ZodString>;
        style: z.ZodOptional<z.ZodEnum<{
            default: "default";
            checklist: "checklist";
            numbered: "numbered";
            plain: "plain";
            divided: "divided";
        }>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"paragraph">;
        text: z.ZodString;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"blockquote">;
        text: z.ZodString;
        attribution: z.ZodOptional<z.ZodString>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"callout">;
        variant: z.ZodEnum<{
            info: "info";
            warn: "warn";
            tip: "tip";
        }>;
        title: z.ZodOptional<z.ZodString>;
        text: z.ZodString;
        icon: z.ZodOptional<z.ZodEnum<{
            [x: string]: string;
        }>>;
        tag: z.ZodOptional<z.ZodObject<{
            text: z.ZodString;
            quiet: z.ZodOptional<z.ZodBoolean>;
            evidence: z.ZodOptional<z.ZodEnum<{
                label: "label";
                draft: "draft";
                trial: "trial";
                company: "company";
                press: "press";
                official: "official";
                registry: "registry";
                preprint: "preprint";
            }>>;
            settled: z.ZodOptional<z.ZodBoolean>;
            tone: z.ZodOptional<z.ZodEnum<{
                danger: "danger";
                warning: "warning";
                success: "success";
            }>>;
            basis: z.ZodOptional<z.ZodEnum<{
                law: "law";
                estimate: "estimate";
                pending: "pending";
                proposal: "proposal";
            }>>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"code">;
        language: z.ZodString;
        code: z.ZodString;
        title: z.ZodOptional<z.ZodString>;
        highlight_lines: z.ZodOptional<z.ZodArray<z.ZodNumber>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"kpi_cards">;
        items: z.ZodArray<z.ZodObject<{
            value: z.ZodString;
            unit: z.ZodOptional<z.ZodString>;
            label: z.ZodString;
            note: z.ZodOptional<z.ZodString>;
            tag: z.ZodOptional<z.ZodObject<{
                text: z.ZodString;
                quiet: z.ZodOptional<z.ZodBoolean>;
                evidence: z.ZodOptional<z.ZodEnum<{
                    label: "label";
                    draft: "draft";
                    trial: "trial";
                    company: "company";
                    press: "press";
                    official: "official";
                    registry: "registry";
                    preprint: "preprint";
                }>>;
                settled: z.ZodOptional<z.ZodBoolean>;
                tone: z.ZodOptional<z.ZodEnum<{
                    danger: "danger";
                    warning: "warning";
                    success: "success";
                }>>;
                basis: z.ZodOptional<z.ZodEnum<{
                    law: "law";
                    estimate: "estimate";
                    pending: "pending";
                    proposal: "proposal";
                }>>;
            }, z.core.$strict>>;
            delta: z.ZodOptional<z.ZodEnum<{
                flat: "flat";
                up: "up";
                down: "down";
            }>>;
            delta_good: z.ZodOptional<z.ZodBoolean>;
            icon: z.ZodOptional<z.ZodEnum<{
                [x: string]: string;
            }>>;
            tone: z.ZodOptional<z.ZodEnum<{
                danger: "danger";
                warning: "warning";
                success: "success";
            }>>;
            source: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"chart">;
        title: z.ZodOptional<z.ZodString>;
        chart_type: z.ZodEnum<{
            line: "line";
            donut: "donut";
            dumbbell: "dumbbell";
            funnel: "funnel";
            gauge: "gauge";
            bar: "bar";
            stacked: "stacked";
            percent_stacked: "percent_stacked";
            pie: "pie";
            area: "area";
            combo: "combo";
            scatter: "scatter";
        }>;
        direction: z.ZodOptional<z.ZodEnum<{
            horizontal: "horizontal";
            vertical: "vertical";
        }>>;
        style: z.ZodOptional<z.ZodEnum<{
            donut: "donut";
        }>>;
        center_total: z.ZodOptional<z.ZodBoolean>;
        gauge: z.ZodOptional<z.ZodObject<{
            min: z.ZodOptional<z.ZodNumber>;
            max: z.ZodOptional<z.ZodNumber>;
        }, z.core.$strict>>;
        axes: z.ZodOptional<z.ZodObject<{
            x_title: z.ZodOptional<z.ZodString>;
            y_title: z.ZodOptional<z.ZodString>;
            x_unit: z.ZodOptional<z.ZodString>;
            y_unit: z.ZodOptional<z.ZodString>;
            y2_title: z.ZodOptional<z.ZodString>;
            y2_unit: z.ZodOptional<z.ZodString>;
            show_grid: z.ZodOptional<z.ZodBoolean>;
        }, z.core.$strict>>;
        tag: z.ZodOptional<z.ZodObject<{
            text: z.ZodString;
            quiet: z.ZodOptional<z.ZodBoolean>;
            evidence: z.ZodOptional<z.ZodEnum<{
                label: "label";
                draft: "draft";
                trial: "trial";
                company: "company";
                press: "press";
                official: "official";
                registry: "registry";
                preprint: "preprint";
            }>>;
            settled: z.ZodOptional<z.ZodBoolean>;
            tone: z.ZodOptional<z.ZodEnum<{
                danger: "danger";
                warning: "warning";
                success: "success";
            }>>;
            basis: z.ZodOptional<z.ZodEnum<{
                law: "law";
                estimate: "estimate";
                pending: "pending";
                proposal: "proposal";
            }>>;
        }, z.core.$strict>>;
        changes: z.ZodOptional<z.ZodArray<z.ZodObject<{
            from: z.ZodString;
            to: z.ZodString;
            at: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>>>;
        bands: z.ZodOptional<z.ZodArray<z.ZodObject<{
            from: z.ZodNumber;
            to: z.ZodNumber;
            label: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>>>;
        emphasis_label: z.ZodOptional<z.ZodString>;
        reference: z.ZodOptional<z.ZodObject<{
            value: z.ZodNumber;
            label: z.ZodString;
        }, z.core.$strict>>;
        markers: z.ZodOptional<z.ZodArray<z.ZodObject<{
            before: z.ZodString;
            label: z.ZodString;
        }, z.core.$strict>>>;
        gaps: z.ZodOptional<z.ZodArray<z.ZodObject<{
            after: z.ZodString;
            x: z.ZodString;
            label: z.ZodString;
        }, z.core.$strict>>>;
        series: z.ZodArray<z.ZodObject<{
            name: z.ZodString;
            data: z.ZodArray<z.ZodObject<{
                x: z.ZodUnion<readonly [z.ZodString, z.ZodNumber]>;
                y: z.ZodNumber;
                size: z.ZodOptional<z.ZodNumber>;
                status: z.ZodOptional<z.ZodEnum<{
                    target: "target";
                    estimate: "estimate";
                    forecast: "forecast";
                }>>;
                emphasis: z.ZodOptional<z.ZodBoolean>;
                note: z.ZodOptional<z.ZodString>;
                icon: z.ZodOptional<z.ZodEnum<{
                    [x: string]: string;
                }>>;
                upper: z.ZodOptional<z.ZodNumber>;
            }, z.core.$strict>>;
            plot: z.ZodOptional<z.ZodEnum<{
                line: "line";
                bar: "bar";
            }>>;
            axis: z.ZodOptional<z.ZodEnum<{
                left: "left";
                right: "right";
            }>>;
            emphasis: z.ZodOptional<z.ZodBoolean>;
            steps: z.ZodOptional<z.ZodBoolean>;
            tone: z.ZodOptional<z.ZodEnum<{
                danger: "danger";
                warning: "warning";
                success: "success";
            }>>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"flowchart">;
        nodes: z.ZodArray<z.ZodObject<{
            id: z.ZodString;
            label: z.ZodString;
            kind: z.ZodOptional<z.ZodEnum<{
                rect: "rect";
                diamond: "diamond";
                round: "round";
            }>>;
        }, z.core.$strict>>;
        edges: z.ZodArray<z.ZodObject<{
            from: z.ZodString;
            to: z.ZodString;
            label: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>>;
        direction: z.ZodOptional<z.ZodEnum<{
            TB: "TB";
            TD: "TD";
            BT: "BT";
            LR: "LR";
            RL: "RL";
        }>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"architecture">;
        layers: z.ZodArray<z.ZodObject<{
            title: z.ZodString;
            items: z.ZodArray<z.ZodString>;
        }, z.core.$strict>>;
        direction: z.ZodOptional<z.ZodEnum<{
            top_down: "top_down";
            bottom_up: "bottom_up";
        }>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"timeline">;
        title: z.ZodOptional<z.ZodString>;
        layout: z.ZodOptional<z.ZodEnum<{
            horizontal: "horizontal";
            vertical: "vertical";
        }>>;
        lanes: z.ZodOptional<z.ZodArray<z.ZodString>>;
        periods: z.ZodOptional<z.ZodArray<z.ZodObject<{
            from: z.ZodString;
            to: z.ZodString;
            label: z.ZodString;
            basis: z.ZodOptional<z.ZodEnum<{
                law: "law";
                estimate: "estimate";
                pending: "pending";
                proposal: "proposal";
            }>>;
        }, z.core.$strict>>>;
        milestones: z.ZodArray<z.ZodObject<{
            date: z.ZodString;
            title: z.ZodString;
            desc: z.ZodOptional<z.ZodString>;
            highlight: z.ZodOptional<z.ZodBoolean>;
            icon: z.ZodOptional<z.ZodEnum<{
                [x: string]: string;
            }>>;
            tone: z.ZodOptional<z.ZodEnum<{
                danger: "danger";
                warning: "warning";
                success: "success";
            }>>;
            status: z.ZodOptional<z.ZodEnum<{
                pending: "pending";
            }>>;
            tag: z.ZodOptional<z.ZodObject<{
                text: z.ZodString;
                quiet: z.ZodOptional<z.ZodBoolean>;
                evidence: z.ZodOptional<z.ZodEnum<{
                    label: "label";
                    draft: "draft";
                    trial: "trial";
                    company: "company";
                    press: "press";
                    official: "official";
                    registry: "registry";
                    preprint: "preprint";
                }>>;
                settled: z.ZodOptional<z.ZodBoolean>;
                tone: z.ZodOptional<z.ZodEnum<{
                    danger: "danger";
                    warning: "warning";
                    success: "success";
                }>>;
                basis: z.ZodOptional<z.ZodEnum<{
                    law: "law";
                    estimate: "estimate";
                    pending: "pending";
                    proposal: "proposal";
                }>>;
            }, z.core.$strict>>;
            source: z.ZodOptional<z.ZodString>;
            lane: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"comparison">;
        title: z.ZodOptional<z.ZodString>;
        columns: z.ZodArray<z.ZodString>;
        label_column: z.ZodOptional<z.ZodString>;
        rows: z.ZodArray<z.ZodObject<{
            label: z.ZodString;
            cells: z.ZodArray<z.ZodString>;
            icon: z.ZodOptional<z.ZodEnum<{
                [x: string]: string;
            }>>;
            tag: z.ZodOptional<z.ZodObject<{
                text: z.ZodString;
                quiet: z.ZodOptional<z.ZodBoolean>;
                evidence: z.ZodOptional<z.ZodEnum<{
                    label: "label";
                    draft: "draft";
                    trial: "trial";
                    company: "company";
                    press: "press";
                    official: "official";
                    registry: "registry";
                    preprint: "preprint";
                }>>;
                settled: z.ZodOptional<z.ZodBoolean>;
                tone: z.ZodOptional<z.ZodEnum<{
                    danger: "danger";
                    warning: "warning";
                    success: "success";
                }>>;
                basis: z.ZodOptional<z.ZodEnum<{
                    law: "law";
                    estimate: "estimate";
                    pending: "pending";
                    proposal: "proposal";
                }>>;
            }, z.core.$strict>>;
            emphasis: z.ZodOptional<z.ZodBoolean>;
        }, z.core.$strict>>;
        tag_column: z.ZodOptional<z.ZodString>;
        recommended: z.ZodOptional<z.ZodNumber>;
        recommended_label: z.ZodOptional<z.ZodString>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"icon_cards">;
        title: z.ZodOptional<z.ZodString>;
        items: z.ZodArray<z.ZodObject<{
            icon: z.ZodEnum<{
                [x: string]: string;
            }>;
            title: z.ZodString;
            text: z.ZodString;
            tag: z.ZodOptional<z.ZodObject<{
                text: z.ZodString;
                quiet: z.ZodOptional<z.ZodBoolean>;
                evidence: z.ZodOptional<z.ZodEnum<{
                    label: "label";
                    draft: "draft";
                    trial: "trial";
                    company: "company";
                    press: "press";
                    official: "official";
                    registry: "registry";
                    preprint: "preprint";
                }>>;
                settled: z.ZodOptional<z.ZodBoolean>;
                tone: z.ZodOptional<z.ZodEnum<{
                    danger: "danger";
                    warning: "warning";
                    success: "success";
                }>>;
                basis: z.ZodOptional<z.ZodEnum<{
                    law: "law";
                    estimate: "estimate";
                    pending: "pending";
                    proposal: "proposal";
                }>>;
            }, z.core.$strict>>;
            tone: z.ZodOptional<z.ZodEnum<{
                danger: "danger";
                warning: "warning";
                success: "success";
            }>>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"row_cards">;
        items: z.ZodArray<z.ZodObject<{
            icon: z.ZodOptional<z.ZodEnum<{
                [x: string]: string;
            }>>;
            title: z.ZodString;
            text: z.ZodOptional<z.ZodString>;
            sub: z.ZodOptional<z.ZodString>;
            highlight: z.ZodOptional<z.ZodBoolean>;
            tone: z.ZodOptional<z.ZodEnum<{
                danger: "danger";
                warning: "warning";
                success: "success";
            }>>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"steps">;
        items: z.ZodArray<z.ZodObject<{
            title: z.ZodString;
            text: z.ZodString;
            icon: z.ZodOptional<z.ZodEnum<{
                [x: string]: string;
            }>>;
            tone: z.ZodOptional<z.ZodEnum<{
                danger: "danger";
                warning: "warning";
                success: "success";
            }>>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"rings">;
        items: z.ZodArray<z.ZodObject<{
            label: z.ZodString;
            desc: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"numbered_cards">;
        items: z.ZodArray<z.ZodObject<{
            title: z.ZodString;
            text: z.ZodOptional<z.ZodString>;
            sub: z.ZodOptional<z.ZodString>;
            icon: z.ZodOptional<z.ZodEnum<{
                [x: string]: string;
            }>>;
            emphasis: z.ZodOptional<z.ZodBoolean>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"roadmap">;
        items: z.ZodArray<z.ZodObject<{
            title: z.ZodString;
            period: z.ZodOptional<z.ZodString>;
            icon: z.ZodOptional<z.ZodEnum<{
                [x: string]: string;
            }>>;
            rows: z.ZodOptional<z.ZodArray<z.ZodObject<{
                label: z.ZodString;
                value: z.ZodString;
                basis: z.ZodOptional<z.ZodEnum<{
                    law: "law";
                    estimate: "estimate";
                    pending: "pending";
                    proposal: "proposal";
                }>>;
            }, z.core.$strict>>>;
            duration: z.ZodOptional<z.ZodNumber>;
            checkpoint: z.ZodOptional<z.ZodString>;
            points: z.ZodOptional<z.ZodArray<z.ZodString>>;
            emphasis: z.ZodOptional<z.ZodBoolean>;
        }, z.core.$strict>>;
        duration_unit: z.ZodOptional<z.ZodString>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"matrix">;
        title: z.ZodOptional<z.ZodString>;
        x_title: z.ZodOptional<z.ZodString>;
        y_title: z.ZodOptional<z.ZodString>;
        cols: z.ZodNumber;
        columns: z.ZodOptional<z.ZodArray<z.ZodString>>;
        rows: z.ZodOptional<z.ZodArray<z.ZodObject<{
            label: z.ZodString;
            icon: z.ZodOptional<z.ZodEnum<{
                [x: string]: string;
            }>>;
        }, z.core.$strict>>>;
        items: z.ZodArray<z.ZodObject<{
            title: z.ZodString;
            tag: z.ZodOptional<z.ZodString>;
            tone: z.ZodOptional<z.ZodEnum<{
                info: "info";
                neutral: "neutral";
                accent: "accent";
            }>>;
            empty: z.ZodOptional<z.ZodBoolean>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"insight_panel">;
        title: z.ZodString;
        icon: z.ZodOptional<z.ZodEnum<{
            [x: string]: string;
        }>>;
        rows: z.ZodArray<z.ZodObject<{
            label: z.ZodString;
            text: z.ZodString;
        }, z.core.$strict>>;
        footnote: z.ZodOptional<z.ZodString>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"verdict_banner">;
        text: z.ZodString;
        tone: z.ZodEnum<{
            warning: "warning";
            positive: "positive";
            neutral: "neutral";
        }>;
        icon: z.ZodOptional<z.ZodEnum<{
            [x: string]: string;
        }>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"image">;
        asset_id: z.ZodString;
        caption: z.ZodOptional<z.ZodString>;
        fit: z.ZodDefault<z.ZodEnum<{
            cover: "cover";
            contain: "contain";
        }>>;
        crop: z.ZodOptional<z.ZodArray<z.ZodNumber>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"image_grid">;
        items: z.ZodArray<z.ZodObject<{
            asset_id: z.ZodString;
            caption: z.ZodOptional<z.ZodString>;
            icon: z.ZodOptional<z.ZodEnum<{
                [x: string]: string;
            }>>;
            tag: z.ZodOptional<z.ZodObject<{
                text: z.ZodString;
                quiet: z.ZodOptional<z.ZodBoolean>;
                evidence: z.ZodOptional<z.ZodEnum<{
                    label: "label";
                    draft: "draft";
                    trial: "trial";
                    company: "company";
                    press: "press";
                    official: "official";
                    registry: "registry";
                    preprint: "preprint";
                }>>;
                settled: z.ZodOptional<z.ZodBoolean>;
                tone: z.ZodOptional<z.ZodEnum<{
                    danger: "danger";
                    warning: "warning";
                    success: "success";
                }>>;
                basis: z.ZodOptional<z.ZodEnum<{
                    law: "law";
                    estimate: "estimate";
                    pending: "pending";
                    proposal: "proposal";
                }>>;
            }, z.core.$strict>>;
            crop: z.ZodOptional<z.ZodArray<z.ZodNumber>>;
        }, z.core.$strict>>;
        emphasis: z.ZodOptional<z.ZodEnum<{
            none: "none";
            first: "first";
        }>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"image_compare">;
        left: z.ZodObject<{
            asset_id: z.ZodString;
            label: z.ZodString;
        }, z.core.$strict>;
        right: z.ZodObject<{
            asset_id: z.ZodString;
            label: z.ZodString;
        }, z.core.$strict>;
        style: z.ZodOptional<z.ZodEnum<{
            vs: "vs";
            before_after: "before_after";
        }>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"logo_wall">;
        title: z.ZodOptional<z.ZodString>;
        items: z.ZodArray<z.ZodObject<{
            name: z.ZodString;
            asset_id: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"product_cards">;
        items: z.ZodArray<z.ZodObject<{
            asset_id: z.ZodString;
            name: z.ZodString;
            note: z.ZodOptional<z.ZodString>;
            price: z.ZodOptional<z.ZodString>;
            price_unit: z.ZodOptional<z.ZodString>;
            featured: z.ZodOptional<z.ZodLiteral<true>>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"quote_wall">;
        quotes: z.ZodArray<z.ZodObject<{
            text: z.ZodString;
            name: z.ZodString;
            role: z.ZodOptional<z.ZodString>;
            featured: z.ZodOptional<z.ZodLiteral<true>>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"swot">;
        strengths: z.ZodArray<z.ZodString>;
        weaknesses: z.ZodArray<z.ZodString>;
        opportunities: z.ZodArray<z.ZodString>;
        threats: z.ZodArray<z.ZodString>;
        labels: z.ZodOptional<z.ZodObject<{
            strengths: z.ZodOptional<z.ZodString>;
            weaknesses: z.ZodOptional<z.ZodString>;
            opportunities: z.ZodOptional<z.ZodString>;
            threats: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"bmc">;
        key_partners: z.ZodArray<z.ZodString>;
        key_activities: z.ZodArray<z.ZodString>;
        key_resources: z.ZodArray<z.ZodString>;
        value_propositions: z.ZodArray<z.ZodString>;
        customer_relationships: z.ZodArray<z.ZodString>;
        channels: z.ZodArray<z.ZodString>;
        customer_segments: z.ZodArray<z.ZodString>;
        cost_structure: z.ZodArray<z.ZodString>;
        revenue_streams: z.ZodArray<z.ZodString>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"waterfall">;
        title: z.ZodOptional<z.ZodString>;
        items: z.ZodArray<z.ZodObject<{
            label: z.ZodString;
            value: z.ZodNumber;
            kind: z.ZodOptional<z.ZodEnum<{
                delta: "delta";
                total: "total";
            }>>;
            note: z.ZodOptional<z.ZodString>;
            emphasis: z.ZodOptional<z.ZodBoolean>;
        }, z.core.$strict>>;
        unit: z.ZodOptional<z.ZodString>;
        emphasis_label: z.ZodOptional<z.ZodString>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"gantt">;
        items: z.ZodArray<z.ZodObject<{
            label: z.ZodString;
            start: z.ZodNumber;
            end: z.ZodNumber;
            text: z.ZodOptional<z.ZodString>;
            emphasis: z.ZodOptional<z.ZodBoolean>;
            icon: z.ZodOptional<z.ZodEnum<{
                [x: string]: string;
            }>>;
            period: z.ZodOptional<z.ZodString>;
            basis: z.ZodOptional<z.ZodEnum<{
                law: "law";
                estimate: "estimate";
                pending: "pending";
                proposal: "proposal";
            }>>;
        }, z.core.$strict>>;
        axis_labels: z.ZodOptional<z.ZodArray<z.ZodString>>;
        range: z.ZodOptional<z.ZodObject<{
            from: z.ZodNumber;
            to: z.ZodNumber;
        }, z.core.$strict>>;
        milestones: z.ZodOptional<z.ZodArray<z.ZodObject<{
            at: z.ZodNumber;
            label: z.ZodString;
        }, z.core.$strict>>>;
        bands: z.ZodOptional<z.ZodArray<z.ZodObject<{
            from: z.ZodNumber;
            to: z.ZodNumber;
            label: z.ZodString;
        }, z.core.$strict>>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"pest">;
        political: z.ZodObject<{
            title: z.ZodOptional<z.ZodString>;
            items: z.ZodArray<z.ZodString>;
        }, z.core.$strict>;
        economic: z.ZodObject<{
            title: z.ZodOptional<z.ZodString>;
            items: z.ZodArray<z.ZodString>;
        }, z.core.$strict>;
        social: z.ZodObject<{
            title: z.ZodOptional<z.ZodString>;
            items: z.ZodArray<z.ZodString>;
        }, z.core.$strict>;
        technological: z.ZodObject<{
            title: z.ZodOptional<z.ZodString>;
            items: z.ZodArray<z.ZodString>;
        }, z.core.$strict>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"five_forces">;
        rivalry: z.ZodObject<{
            label: z.ZodOptional<z.ZodString>;
            intensity: z.ZodOptional<z.ZodEnum<{
                low: "low";
                medium: "medium";
                high: "high";
            }>>;
            items: z.ZodArray<z.ZodString>;
        }, z.core.$strict>;
        new_entrants: z.ZodObject<{
            label: z.ZodOptional<z.ZodString>;
            intensity: z.ZodOptional<z.ZodEnum<{
                low: "low";
                medium: "medium";
                high: "high";
            }>>;
            items: z.ZodArray<z.ZodString>;
        }, z.core.$strict>;
        supplier_power: z.ZodObject<{
            label: z.ZodOptional<z.ZodString>;
            intensity: z.ZodOptional<z.ZodEnum<{
                low: "low";
                medium: "medium";
                high: "high";
            }>>;
            items: z.ZodArray<z.ZodString>;
        }, z.core.$strict>;
        buyer_power: z.ZodObject<{
            label: z.ZodOptional<z.ZodString>;
            intensity: z.ZodOptional<z.ZodEnum<{
                low: "low";
                medium: "medium";
                high: "high";
            }>>;
            items: z.ZodArray<z.ZodString>;
        }, z.core.$strict>;
        substitutes: z.ZodObject<{
            label: z.ZodOptional<z.ZodString>;
            intensity: z.ZodOptional<z.ZodEnum<{
                low: "low";
                medium: "medium";
                high: "high";
            }>>;
            items: z.ZodArray<z.ZodString>;
        }, z.core.$strict>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"heatmap">;
        x_labels: z.ZodArray<z.ZodString>;
        y_labels: z.ZodArray<z.ZodString>;
        values: z.ZodArray<z.ZodArray<z.ZodNumber>>;
        domain: z.ZodOptional<z.ZodObject<{
            min: z.ZodNumber;
            max: z.ZodNumber;
        }, z.core.$strict>>;
        show_values: z.ZodOptional<z.ZodBoolean>;
        x_title: z.ZodOptional<z.ZodString>;
        y_title: z.ZodOptional<z.ZodString>;
        label_every: z.ZodOptional<z.ZodNumber>;
        steps: z.ZodOptional<z.ZodArray<z.ZodObject<{
            max: z.ZodOptional<z.ZodNumber>;
            label: z.ZodString;
            short: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>>>;
        bands: z.ZodOptional<z.ZodArray<z.ZodObject<{
            from: z.ZodString;
            to: z.ZodString;
            label: z.ZodString;
            icon: z.ZodOptional<z.ZodEnum<{
                [x: string]: string;
            }>>;
        }, z.core.$strict>>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"sankey">;
        nodes: z.ZodArray<z.ZodObject<{
            id: z.ZodString;
            label: z.ZodString;
        }, z.core.$strict>>;
        links: z.ZodArray<z.ZodObject<{
            from: z.ZodString;
            to: z.ZodString;
            value: z.ZodNumber;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"data_table">;
        title: z.ZodOptional<z.ZodString>;
        columns: z.ZodArray<z.ZodObject<{
            key: z.ZodString;
            label: z.ZodString;
            align: z.ZodOptional<z.ZodEnum<{
                left: "left";
                right: "right";
                center: "center";
            }>>;
            emphasis: z.ZodOptional<z.ZodBoolean>;
            icon: z.ZodOptional<z.ZodEnum<{
                [x: string]: string;
            }>>;
        }, z.core.$strict>>;
        rows: z.ZodArray<z.ZodObject<{
            cells: z.ZodRecord<z.ZodString, z.ZodUnion<readonly [z.ZodString, z.ZodNumber]>>;
            emphasis: z.ZodOptional<z.ZodEnum<{
                highlight: "highlight";
                total: "total";
            }>>;
            icon: z.ZodOptional<z.ZodEnum<{
                [x: string]: string;
            }>>;
            tag: z.ZodOptional<z.ZodObject<{
                text: z.ZodString;
                quiet: z.ZodOptional<z.ZodBoolean>;
                evidence: z.ZodOptional<z.ZodEnum<{
                    label: "label";
                    draft: "draft";
                    trial: "trial";
                    company: "company";
                    press: "press";
                    official: "official";
                    registry: "registry";
                    preprint: "preprint";
                }>>;
                settled: z.ZodOptional<z.ZodBoolean>;
                tone: z.ZodOptional<z.ZodEnum<{
                    danger: "danger";
                    warning: "warning";
                    success: "success";
                }>>;
                basis: z.ZodOptional<z.ZodEnum<{
                    law: "law";
                    estimate: "estimate";
                    pending: "pending";
                    proposal: "proposal";
                }>>;
            }, z.core.$strict>>;
        }, z.core.$strict>>;
        source: z.ZodOptional<z.ZodString>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"device_mockup">;
        device: z.ZodEnum<{
            phone: "phone";
            browser: "browser";
        }>;
        asset_id: z.ZodString;
        caption: z.ZodOptional<z.ZodString>;
        url: z.ZodOptional<z.ZodString>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"cycle">;
        title: z.ZodOptional<z.ZodString>;
        items: z.ZodArray<z.ZodObject<{
            label: z.ZodString;
            description: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"people_cards">;
        title: z.ZodOptional<z.ZodString>;
        people: z.ZodArray<z.ZodObject<{
            name: z.ZodString;
            role: z.ZodOptional<z.ZodString>;
            org: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"hub_spoke">;
        center: z.ZodString;
        items: z.ZodArray<z.ZodObject<{
            label: z.ZodString;
            description: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"progress_donuts">;
        items: z.ZodArray<z.ZodObject<{
            value: z.ZodString;
            unit: z.ZodOptional<z.ZodString>;
            label: z.ZodString;
            icon: z.ZodOptional<z.ZodEnum<{
                [x: string]: string;
            }>>;
            source: z.ZodOptional<z.ZodString>;
            detail: z.ZodOptional<z.ZodString>;
            emphasis: z.ZodOptional<z.ZodBoolean>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"staircase">;
        items: z.ZodArray<z.ZodObject<{
            title: z.ZodString;
            value: z.ZodString;
            unit: z.ZodOptional<z.ZodString>;
            note: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"chevron_process">;
        items: z.ZodArray<z.ZodObject<{
            title: z.ZodString;
            text: z.ZodOptional<z.ZodString>;
            icon: z.ZodOptional<z.ZodEnum<{
                [x: string]: string;
            }>>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"swimlane">;
        lanes: z.ZodArray<z.ZodObject<{
            label: z.ZodString;
            role: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>>;
        steps: z.ZodArray<z.ZodObject<{
            lane: z.ZodString;
            title: z.ZodString;
            detail: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>>;
        handoff_note: z.ZodOptional<z.ZodString>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"journey_map">;
        stages: z.ZodArray<z.ZodObject<{
            label: z.ZodString;
            touchpoints: z.ZodOptional<z.ZodArray<z.ZodString>>;
            action: z.ZodOptional<z.ZodString>;
            emotion: z.ZodNumber;
            opportunity: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>>;
        row_labels: z.ZodOptional<z.ZodObject<{
            touchpoints: z.ZodOptional<z.ZodString>;
            action: z.ZodOptional<z.ZodString>;
            emotion: z.ZodOptional<z.ZodString>;
            opportunity: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"decision_tree">;
        question: z.ZodString;
        branches: z.ZodArray<z.ZodObject<{
            edge: z.ZodString;
            title: z.ZodString;
            detail: z.ZodOptional<z.ZodString>;
            outcomes: z.ZodArray<z.ZodObject<{
                edge: z.ZodString;
                title: z.ZodString;
                detail: z.ZodOptional<z.ZodString>;
                value: z.ZodOptional<z.ZodString>;
                unit: z.ZodOptional<z.ZodString>;
                recommended: z.ZodOptional<z.ZodBoolean>;
            }, z.core.$strict>>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"from_to">;
        from: z.ZodObject<{
            kicker: z.ZodOptional<z.ZodString>;
            title: z.ZodString;
        }, z.core.$strict>;
        to: z.ZodObject<{
            kicker: z.ZodOptional<z.ZodString>;
            title: z.ZodString;
        }, z.core.$strict>;
        rows: z.ZodArray<z.ZodObject<{
            label: z.ZodString;
            icon: z.ZodOptional<z.ZodEnum<{
                [x: string]: string;
            }>>;
            note: z.ZodOptional<z.ZodString>;
            from: z.ZodString;
            to: z.ZodString;
            unit: z.ZodOptional<z.ZodString>;
            change: z.ZodOptional<z.ZodString>;
            tag: z.ZodOptional<z.ZodObject<{
                text: z.ZodString;
                quiet: z.ZodOptional<z.ZodBoolean>;
                evidence: z.ZodOptional<z.ZodEnum<{
                    label: "label";
                    draft: "draft";
                    trial: "trial";
                    company: "company";
                    press: "press";
                    official: "official";
                    registry: "registry";
                    preprint: "preprint";
                }>>;
                settled: z.ZodOptional<z.ZodBoolean>;
                tone: z.ZodOptional<z.ZodEnum<{
                    danger: "danger";
                    warning: "warning";
                    success: "success";
                }>>;
                basis: z.ZodOptional<z.ZodEnum<{
                    law: "law";
                    estimate: "estimate";
                    pending: "pending";
                    proposal: "proposal";
                }>>;
            }, z.core.$strict>>;
            emphasis: z.ZodOptional<z.ZodBoolean>;
        }, z.core.$strict>>;
        label_column: z.ZodOptional<z.ZodString>;
        span: z.ZodOptional<z.ZodString>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"org_tree">;
        root: z.ZodObject<{
            name: z.ZodString;
            role: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>;
        children: z.ZodArray<z.ZodObject<{
            name: z.ZodString;
            role: z.ZodOptional<z.ZodString>;
            children: z.ZodOptional<z.ZodArray<z.ZodObject<{
                name: z.ZodString;
                role: z.ZodOptional<z.ZodString>;
            }, z.core.$strict>>>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"issue_tree">;
        question: z.ZodString;
        children_column: z.ZodOptional<z.ZodString>;
        branches: z.ZodArray<z.ZodObject<{
            label: z.ZodString;
            note: z.ZodOptional<z.ZodString>;
            icon: z.ZodOptional<z.ZodEnum<{
                [x: string]: string;
            }>>;
            emphasis: z.ZodOptional<z.ZodLiteral<true>>;
            children: z.ZodOptional<z.ZodArray<z.ZodObject<{
                label: z.ZodString;
            }, z.core.$strict>>>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"pyramid">;
        layers: z.ZodArray<z.ZodObject<{
            label: z.ZodString;
            note: z.ZodOptional<z.ZodString>;
            tone: z.ZodOptional<z.ZodEnum<{
                danger: "danger";
                warning: "warning";
                success: "success";
            }>>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"iceberg">;
        above: z.ZodArray<z.ZodString>;
        below: z.ZodArray<z.ZodString>;
        waterline: z.ZodOptional<z.ZodString>;
        above_label: z.ZodOptional<z.ZodString>;
        below_label: z.ZodOptional<z.ZodString>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"pillar_model">;
        goal: z.ZodString;
        pillars: z.ZodArray<z.ZodObject<{
            title: z.ZodString;
            value: z.ZodString;
            unit: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>>;
        base: z.ZodString;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"value_chain">;
        primary: z.ZodArray<z.ZodObject<{
            label: z.ZodString;
            value: z.ZodOptional<z.ZodString>;
            unit: z.ZodOptional<z.ZodString>;
            emphasis: z.ZodOptional<z.ZodLiteral<true>>;
        }, z.core.$strict>>;
        support: z.ZodArray<z.ZodObject<{
            label: z.ZodString;
            note: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>>;
        margin: z.ZodOptional<z.ZodObject<{
            label: z.ZodString;
            value: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"harvey_balls">;
        criteria: z.ZodArray<z.ZodString>;
        options: z.ZodArray<z.ZodObject<{
            label: z.ZodString;
            scores: z.ZodArray<z.ZodUnion<readonly [z.ZodLiteral<0>, z.ZodLiteral<25>, z.ZodLiteral<50>, z.ZodLiteral<75>, z.ZodLiteral<100>]>>;
            total: z.ZodOptional<z.ZodUnion<readonly [z.ZodString, z.ZodNumber]>>;
            highlight: z.ZodOptional<z.ZodBoolean>;
        }, z.core.$strict>>;
        legend: z.ZodOptional<z.ZodBoolean>;
        labels: z.ZodOptional<z.ZodObject<{
            option: z.ZodOptional<z.ZodString>;
            total: z.ZodOptional<z.ZodString>;
            none: z.ZodOptional<z.ZodString>;
            partial: z.ZodOptional<z.ZodString>;
            full: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"scorecard">;
        labels: z.ZodOptional<z.ZodObject<{
            metric: z.ZodOptional<z.ZodString>;
            target: z.ZodOptional<z.ZodString>;
            actual: z.ZodOptional<z.ZodString>;
            gap: z.ZodOptional<z.ZodString>;
            status: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>>;
        rows: z.ZodArray<z.ZodObject<{
            label: z.ZodString;
            target: z.ZodString;
            actual: z.ZodString;
            gap: z.ZodString;
            status: z.ZodEnum<{
                watch: "watch";
                on_track: "on_track";
                off_track: "off_track";
            }>;
            status_label: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>>;
        note: z.ZodOptional<z.ZodString>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"pictogram">;
        rows: z.ZodArray<z.ZodObject<{
            filled: z.ZodNumber;
            label: z.ZodString;
            caption: z.ZodOptional<z.ZodString>;
            highlight: z.ZodOptional<z.ZodBoolean>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"word_cloud">;
        words: z.ZodArray<z.ZodObject<{
            text: z.ZodString;
            weight: z.ZodUnion<readonly [z.ZodLiteral<1>, z.ZodLiteral<2>, z.ZodLiteral<3>, z.ZodLiteral<4>]>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"venn">;
        sets: z.ZodArray<z.ZodObject<{
            label: z.ZodString;
        }, z.core.$strict>>;
        center: z.ZodString;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"fishbone">;
        effect: z.ZodString;
        ribs: z.ZodArray<z.ZodObject<{
            label: z.ZodString;
            causes: z.ZodArray<z.ZodString>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"positioning_map">;
        x_axis: z.ZodObject<{
            title: z.ZodString;
            low: z.ZodString;
            high: z.ZodString;
        }, z.core.$strict>;
        y_axis: z.ZodObject<{
            title: z.ZodString;
            low: z.ZodString;
            high: z.ZodString;
        }, z.core.$strict>;
        quadrants: z.ZodOptional<z.ZodObject<{
            top_left: z.ZodString;
            top_right: z.ZodString;
            bottom_left: z.ZodString;
            bottom_right: z.ZodString;
        }, z.core.$strict>>;
        points: z.ZodArray<z.ZodObject<{
            label: z.ZodString;
            x: z.ZodNumber;
            y: z.ZodNumber;
            emphasis: z.ZodOptional<z.ZodLiteral<true>>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"concept_equation">;
        operands: z.ZodArray<z.ZodObject<{
            label: z.ZodString;
            value: z.ZodOptional<z.ZodString>;
            note: z.ZodOptional<z.ZodString>;
            icon: z.ZodOptional<z.ZodEnum<{
                [x: string]: string;
            }>>;
        }, z.core.$strict>>;
        result: z.ZodObject<{
            label: z.ZodString;
            value: z.ZodOptional<z.ZodString>;
            note: z.ZodOptional<z.ZodString>;
            icon: z.ZodOptional<z.ZodEnum<{
                [x: string]: string;
            }>>;
        }, z.core.$strict>;
        excluded: z.ZodOptional<z.ZodObject<{
            label: z.ZodString;
            value: z.ZodOptional<z.ZodString>;
            note: z.ZodOptional<z.ZodString>;
            icon: z.ZodOptional<z.ZodEnum<{
                [x: string]: string;
            }>>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"segmented_wheel">;
        center: z.ZodString;
        segments: z.ZodArray<z.ZodObject<{
            label: z.ZodString;
            value: z.ZodOptional<z.ZodString>;
            emphasis: z.ZodOptional<z.ZodLiteral<true>>;
        }, z.core.$strict>>;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"pros_cons">;
        pros: z.ZodObject<{
            title: z.ZodString;
            items: z.ZodArray<z.ZodObject<{
                label: z.ZodString;
                note: z.ZodOptional<z.ZodString>;
            }, z.core.$strict>>;
        }, z.core.$strict>;
        cons: z.ZodObject<{
            title: z.ZodString;
            items: z.ZodArray<z.ZodObject<{
                label: z.ZodString;
                note: z.ZodOptional<z.ZodString>;
            }, z.core.$strict>>;
        }, z.core.$strict>;
        verdict: z.ZodString;
    }, z.core.$strict>, z.ZodObject<{
        type: z.ZodLiteral<"sketch">;
        kind: z.ZodEnum<{
            discontinuity: "discontinuity";
            difference_in_differences: "difference_in_differences";
        }>;
        at: z.ZodString;
        x_title: z.ZodString;
        y_title: z.ZodOptional<z.ZodString>;
        effect: z.ZodOptional<z.ZodString>;
        groups: z.ZodOptional<z.ZodArray<z.ZodString>>;
        direction: z.ZodOptional<z.ZodEnum<{
            up: "up";
            down: "down";
        }>>;
    }, z.core.$strict>], "type">>>;
    background: z.ZodOptional<z.ZodDiscriminatedUnion<[z.ZodObject<{
        kind: z.ZodLiteral<"color">;
        value: z.ZodString;
    }, z.core.$strict>, z.ZodObject<{
        kind: z.ZodLiteral<"gradient">;
        from: z.ZodString;
        to: z.ZodString;
        direction: z.ZodOptional<z.ZodEnum<{
            tb: "tb";
            lr: "lr";
            diagonal: "diagonal";
        }>>;
    }, z.core.$strict>, z.ZodObject<{
        kind: z.ZodLiteral<"asset">;
        asset_id: z.ZodString;
        overlay: z.ZodOptional<z.ZodObject<{
            color: z.ZodString;
            opacity: z.ZodNumber;
        }, z.core.$strict>>;
        fit: z.ZodOptional<z.ZodEnum<{
            cover: "cover";
            contain: "contain";
        }>>;
    }, z.core.$strict>], "kind">>;
    decor: z.ZodOptional<z.ZodObject<{
        kind: z.ZodEnum<{
            big_number: "big_number";
            corner_tag: "corner_tag";
            rule_line: "rule_line";
            quote_marks: "quote_marks";
            geo_dots: "geo_dots";
        }>;
        intensity: z.ZodOptional<z.ZodEnum<{
            subtle: "subtle";
            normal: "normal";
        }>>;
        text: z.ZodOptional<z.ZodString>;
    }, z.core.$strict>>;
    image_side: z.ZodOptional<z.ZodEnum<{
        left: "left";
        right: "right";
    }>>;
    footnote: z.ZodOptional<z.ZodString>;
    notes: z.ZodOptional<z.ZodString>;
    type: z.ZodLiteral<"ending">;
}, z.core.$strict>], "type">, unknown>;
declare const PptxIRSchema: z.ZodObject<{
    version: z.ZodDefault<z.ZodLiteral<"5">>;
    filename: z.ZodDefault<z.ZodString>;
    narrative: z.ZodOptional<z.ZodUnion<readonly [z.ZodString, z.ZodRecord<z.ZodString, z.ZodUnknown>]>>;
    theme: z.ZodObject<{
        id: z.ZodString;
    }, z.core.$strict>;
    meta: z.ZodDefault<z.ZodObject<{
        organization: z.ZodOptional<z.ZodString>;
        authors: z.ZodOptional<z.ZodArray<z.ZodObject<{
            name: z.ZodString;
            role: z.ZodOptional<z.ZodString>;
            org: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>>>;
        date: z.ZodOptional<z.ZodString>;
        version: z.ZodOptional<z.ZodString>;
        confidentiality: z.ZodOptional<z.ZodEnum<{
            public: "public";
            internal: "internal";
            confidential: "confidential";
            restricted: "restricted";
        }>>;
        classification: z.ZodOptional<z.ZodString>;
        contact: z.ZodOptional<z.ZodObject<{
            name: z.ZodOptional<z.ZodString>;
            email: z.ZodOptional<z.ZodString>;
            phone: z.ZodOptional<z.ZodString>;
            website: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>>;
        copyright: z.ZodOptional<z.ZodString>;
        animation: z.ZodOptional<z.ZodObject<{
            transition: z.ZodOptional<z.ZodEnum<{
                push: "push";
                none: "none";
                fade: "fade";
                wipe: "wipe";
            }>>;
            elements: z.ZodOptional<z.ZodEnum<{
                none: "none";
                auto: "auto";
            }>>;
        }, z.core.$strict>>;
    }, z.core.$strict>>;
    assets: z.ZodDefault<z.ZodObject<{
        images: z.ZodDefault<z.ZodRecord<z.ZodString, z.ZodObject<{
            src: z.ZodString;
            alt: z.ZodOptional<z.ZodString>;
            error: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>>>;
    }, z.core.$strict>>;
    brand: z.ZodOptional<z.ZodObject<{
        logo_asset_id: z.ZodOptional<z.ZodString>;
        position: z.ZodOptional<z.ZodEnum<{
            tl: "tl";
            tr: "tr";
            bl: "bl";
            br: "br";
        }>>;
    }, z.core.$strict>>;
    branding: z.ZodOptional<z.ZodEnum<{
        full: "full";
        "cover-only": "cover-only";
        minimal: "minimal";
    }>>;
    footer: z.ZodOptional<z.ZodObject<{
        page_number: z.ZodOptional<z.ZodBoolean>;
        organization: z.ZodOptional<z.ZodBoolean>;
        label: z.ZodOptional<z.ZodString>;
        notice: z.ZodOptional<z.ZodString>;
        draft: z.ZodOptional<z.ZodString>;
        confidentiality: z.ZodOptional<z.ZodEnum<{
            footer: "footer";
            cover: "cover";
        }>>;
    }, z.core.$strict>>;
    course: z.ZodOptional<z.ZodObject<{
        stages: z.ZodArray<z.ZodObject<{
            label: z.ZodString;
            quiz: z.ZodOptional<z.ZodBoolean>;
        }, z.core.$strict>>;
    }, z.core.$strict>>;
    slides: z.ZodArray<z.ZodPreprocess<z.ZodDiscriminatedUnion<[z.ZodObject<{
        id: z.ZodOptional<z.ZodString>;
        placeholder: z.ZodOptional<z.ZodLiteral<true>>;
        heading: z.ZodOptional<z.ZodString>;
        subheading: z.ZodOptional<z.ZodString>;
        kicker: z.ZodOptional<z.ZodString>;
        fields: z.ZodOptional<z.ZodArray<z.ZodObject<{
            label: z.ZodString;
            value: z.ZodString;
            note: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>>>;
        stamp: z.ZodOptional<z.ZodObject<{
            text: z.ZodString;
            date: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>>;
        ballot: z.ZodOptional<z.ZodObject<{
            choices: z.ZodArray<z.ZodString>;
            signature: z.ZodOptional<z.ZodString>;
            item_choices: z.ZodOptional<z.ZodArray<z.ZodObject<{
                item: z.ZodNumber;
                choices: z.ZodArray<z.ZodString>;
            }, z.core.$strict>>>;
        }, z.core.$strict>>;
        tag: z.ZodOptional<z.ZodObject<{
            text: z.ZodString;
            quiet: z.ZodOptional<z.ZodBoolean>;
            evidence: z.ZodOptional<z.ZodEnum<{
                label: "label";
                draft: "draft";
                trial: "trial";
                company: "company";
                press: "press";
                official: "official";
                registry: "registry";
                preprint: "preprint";
            }>>;
            settled: z.ZodOptional<z.ZodBoolean>;
            tone: z.ZodOptional<z.ZodEnum<{
                danger: "danger";
                warning: "warning";
                success: "success";
            }>>;
            basis: z.ZodOptional<z.ZodEnum<{
                law: "law";
                estimate: "estimate";
                pending: "pending";
                proposal: "proposal";
            }>>;
        }, z.core.$strict>>;
        years: z.ZodOptional<z.ZodObject<{
            from: z.ZodNumber;
            to: z.ZodNumber;
            marked: z.ZodArray<z.ZodNumber>;
        }, z.core.$strict>>;
        stage: z.ZodOptional<z.ZodString>;
        components: z.ZodDefault<z.ZodArray<z.ZodDiscriminatedUnion<[z.ZodObject<{
            type: z.ZodLiteral<"bullets">;
            items: z.ZodArray<z.ZodString>;
            style: z.ZodOptional<z.ZodEnum<{
                default: "default";
                checklist: "checklist";
                numbered: "numbered";
                plain: "plain";
                divided: "divided";
            }>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"paragraph">;
            text: z.ZodString;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"blockquote">;
            text: z.ZodString;
            attribution: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"callout">;
            variant: z.ZodEnum<{
                info: "info";
                warn: "warn";
                tip: "tip";
            }>;
            title: z.ZodOptional<z.ZodString>;
            text: z.ZodString;
            icon: z.ZodOptional<z.ZodEnum<{
                [x: string]: string;
            }>>;
            tag: z.ZodOptional<z.ZodObject<{
                text: z.ZodString;
                quiet: z.ZodOptional<z.ZodBoolean>;
                evidence: z.ZodOptional<z.ZodEnum<{
                    label: "label";
                    draft: "draft";
                    trial: "trial";
                    company: "company";
                    press: "press";
                    official: "official";
                    registry: "registry";
                    preprint: "preprint";
                }>>;
                settled: z.ZodOptional<z.ZodBoolean>;
                tone: z.ZodOptional<z.ZodEnum<{
                    danger: "danger";
                    warning: "warning";
                    success: "success";
                }>>;
                basis: z.ZodOptional<z.ZodEnum<{
                    law: "law";
                    estimate: "estimate";
                    pending: "pending";
                    proposal: "proposal";
                }>>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"code">;
            language: z.ZodString;
            code: z.ZodString;
            title: z.ZodOptional<z.ZodString>;
            highlight_lines: z.ZodOptional<z.ZodArray<z.ZodNumber>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"kpi_cards">;
            items: z.ZodArray<z.ZodObject<{
                value: z.ZodString;
                unit: z.ZodOptional<z.ZodString>;
                label: z.ZodString;
                note: z.ZodOptional<z.ZodString>;
                tag: z.ZodOptional<z.ZodObject<{
                    text: z.ZodString;
                    quiet: z.ZodOptional<z.ZodBoolean>;
                    evidence: z.ZodOptional<z.ZodEnum<{
                        label: "label";
                        draft: "draft";
                        trial: "trial";
                        company: "company";
                        press: "press";
                        official: "official";
                        registry: "registry";
                        preprint: "preprint";
                    }>>;
                    settled: z.ZodOptional<z.ZodBoolean>;
                    tone: z.ZodOptional<z.ZodEnum<{
                        danger: "danger";
                        warning: "warning";
                        success: "success";
                    }>>;
                    basis: z.ZodOptional<z.ZodEnum<{
                        law: "law";
                        estimate: "estimate";
                        pending: "pending";
                        proposal: "proposal";
                    }>>;
                }, z.core.$strict>>;
                delta: z.ZodOptional<z.ZodEnum<{
                    flat: "flat";
                    up: "up";
                    down: "down";
                }>>;
                delta_good: z.ZodOptional<z.ZodBoolean>;
                icon: z.ZodOptional<z.ZodEnum<{
                    [x: string]: string;
                }>>;
                tone: z.ZodOptional<z.ZodEnum<{
                    danger: "danger";
                    warning: "warning";
                    success: "success";
                }>>;
                source: z.ZodOptional<z.ZodString>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"chart">;
            title: z.ZodOptional<z.ZodString>;
            chart_type: z.ZodEnum<{
                line: "line";
                donut: "donut";
                dumbbell: "dumbbell";
                funnel: "funnel";
                gauge: "gauge";
                bar: "bar";
                stacked: "stacked";
                percent_stacked: "percent_stacked";
                pie: "pie";
                area: "area";
                combo: "combo";
                scatter: "scatter";
            }>;
            direction: z.ZodOptional<z.ZodEnum<{
                horizontal: "horizontal";
                vertical: "vertical";
            }>>;
            style: z.ZodOptional<z.ZodEnum<{
                donut: "donut";
            }>>;
            center_total: z.ZodOptional<z.ZodBoolean>;
            gauge: z.ZodOptional<z.ZodObject<{
                min: z.ZodOptional<z.ZodNumber>;
                max: z.ZodOptional<z.ZodNumber>;
            }, z.core.$strict>>;
            axes: z.ZodOptional<z.ZodObject<{
                x_title: z.ZodOptional<z.ZodString>;
                y_title: z.ZodOptional<z.ZodString>;
                x_unit: z.ZodOptional<z.ZodString>;
                y_unit: z.ZodOptional<z.ZodString>;
                y2_title: z.ZodOptional<z.ZodString>;
                y2_unit: z.ZodOptional<z.ZodString>;
                show_grid: z.ZodOptional<z.ZodBoolean>;
            }, z.core.$strict>>;
            tag: z.ZodOptional<z.ZodObject<{
                text: z.ZodString;
                quiet: z.ZodOptional<z.ZodBoolean>;
                evidence: z.ZodOptional<z.ZodEnum<{
                    label: "label";
                    draft: "draft";
                    trial: "trial";
                    company: "company";
                    press: "press";
                    official: "official";
                    registry: "registry";
                    preprint: "preprint";
                }>>;
                settled: z.ZodOptional<z.ZodBoolean>;
                tone: z.ZodOptional<z.ZodEnum<{
                    danger: "danger";
                    warning: "warning";
                    success: "success";
                }>>;
                basis: z.ZodOptional<z.ZodEnum<{
                    law: "law";
                    estimate: "estimate";
                    pending: "pending";
                    proposal: "proposal";
                }>>;
            }, z.core.$strict>>;
            changes: z.ZodOptional<z.ZodArray<z.ZodObject<{
                from: z.ZodString;
                to: z.ZodString;
                at: z.ZodOptional<z.ZodString>;
            }, z.core.$strict>>>;
            bands: z.ZodOptional<z.ZodArray<z.ZodObject<{
                from: z.ZodNumber;
                to: z.ZodNumber;
                label: z.ZodOptional<z.ZodString>;
            }, z.core.$strict>>>;
            emphasis_label: z.ZodOptional<z.ZodString>;
            reference: z.ZodOptional<z.ZodObject<{
                value: z.ZodNumber;
                label: z.ZodString;
            }, z.core.$strict>>;
            markers: z.ZodOptional<z.ZodArray<z.ZodObject<{
                before: z.ZodString;
                label: z.ZodString;
            }, z.core.$strict>>>;
            gaps: z.ZodOptional<z.ZodArray<z.ZodObject<{
                after: z.ZodString;
                x: z.ZodString;
                label: z.ZodString;
            }, z.core.$strict>>>;
            series: z.ZodArray<z.ZodObject<{
                name: z.ZodString;
                data: z.ZodArray<z.ZodObject<{
                    x: z.ZodUnion<readonly [z.ZodString, z.ZodNumber]>;
                    y: z.ZodNumber;
                    size: z.ZodOptional<z.ZodNumber>;
                    status: z.ZodOptional<z.ZodEnum<{
                        target: "target";
                        estimate: "estimate";
                        forecast: "forecast";
                    }>>;
                    emphasis: z.ZodOptional<z.ZodBoolean>;
                    note: z.ZodOptional<z.ZodString>;
                    icon: z.ZodOptional<z.ZodEnum<{
                        [x: string]: string;
                    }>>;
                    upper: z.ZodOptional<z.ZodNumber>;
                }, z.core.$strict>>;
                plot: z.ZodOptional<z.ZodEnum<{
                    line: "line";
                    bar: "bar";
                }>>;
                axis: z.ZodOptional<z.ZodEnum<{
                    left: "left";
                    right: "right";
                }>>;
                emphasis: z.ZodOptional<z.ZodBoolean>;
                steps: z.ZodOptional<z.ZodBoolean>;
                tone: z.ZodOptional<z.ZodEnum<{
                    danger: "danger";
                    warning: "warning";
                    success: "success";
                }>>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"flowchart">;
            nodes: z.ZodArray<z.ZodObject<{
                id: z.ZodString;
                label: z.ZodString;
                kind: z.ZodOptional<z.ZodEnum<{
                    rect: "rect";
                    diamond: "diamond";
                    round: "round";
                }>>;
            }, z.core.$strict>>;
            edges: z.ZodArray<z.ZodObject<{
                from: z.ZodString;
                to: z.ZodString;
                label: z.ZodOptional<z.ZodString>;
            }, z.core.$strict>>;
            direction: z.ZodOptional<z.ZodEnum<{
                TB: "TB";
                TD: "TD";
                BT: "BT";
                LR: "LR";
                RL: "RL";
            }>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"architecture">;
            layers: z.ZodArray<z.ZodObject<{
                title: z.ZodString;
                items: z.ZodArray<z.ZodString>;
            }, z.core.$strict>>;
            direction: z.ZodOptional<z.ZodEnum<{
                top_down: "top_down";
                bottom_up: "bottom_up";
            }>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"timeline">;
            title: z.ZodOptional<z.ZodString>;
            layout: z.ZodOptional<z.ZodEnum<{
                horizontal: "horizontal";
                vertical: "vertical";
            }>>;
            lanes: z.ZodOptional<z.ZodArray<z.ZodString>>;
            periods: z.ZodOptional<z.ZodArray<z.ZodObject<{
                from: z.ZodString;
                to: z.ZodString;
                label: z.ZodString;
                basis: z.ZodOptional<z.ZodEnum<{
                    law: "law";
                    estimate: "estimate";
                    pending: "pending";
                    proposal: "proposal";
                }>>;
            }, z.core.$strict>>>;
            milestones: z.ZodArray<z.ZodObject<{
                date: z.ZodString;
                title: z.ZodString;
                desc: z.ZodOptional<z.ZodString>;
                highlight: z.ZodOptional<z.ZodBoolean>;
                icon: z.ZodOptional<z.ZodEnum<{
                    [x: string]: string;
                }>>;
                tone: z.ZodOptional<z.ZodEnum<{
                    danger: "danger";
                    warning: "warning";
                    success: "success";
                }>>;
                status: z.ZodOptional<z.ZodEnum<{
                    pending: "pending";
                }>>;
                tag: z.ZodOptional<z.ZodObject<{
                    text: z.ZodString;
                    quiet: z.ZodOptional<z.ZodBoolean>;
                    evidence: z.ZodOptional<z.ZodEnum<{
                        label: "label";
                        draft: "draft";
                        trial: "trial";
                        company: "company";
                        press: "press";
                        official: "official";
                        registry: "registry";
                        preprint: "preprint";
                    }>>;
                    settled: z.ZodOptional<z.ZodBoolean>;
                    tone: z.ZodOptional<z.ZodEnum<{
                        danger: "danger";
                        warning: "warning";
                        success: "success";
                    }>>;
                    basis: z.ZodOptional<z.ZodEnum<{
                        law: "law";
                        estimate: "estimate";
                        pending: "pending";
                        proposal: "proposal";
                    }>>;
                }, z.core.$strict>>;
                source: z.ZodOptional<z.ZodString>;
                lane: z.ZodOptional<z.ZodString>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"comparison">;
            title: z.ZodOptional<z.ZodString>;
            columns: z.ZodArray<z.ZodString>;
            label_column: z.ZodOptional<z.ZodString>;
            rows: z.ZodArray<z.ZodObject<{
                label: z.ZodString;
                cells: z.ZodArray<z.ZodString>;
                icon: z.ZodOptional<z.ZodEnum<{
                    [x: string]: string;
                }>>;
                tag: z.ZodOptional<z.ZodObject<{
                    text: z.ZodString;
                    quiet: z.ZodOptional<z.ZodBoolean>;
                    evidence: z.ZodOptional<z.ZodEnum<{
                        label: "label";
                        draft: "draft";
                        trial: "trial";
                        company: "company";
                        press: "press";
                        official: "official";
                        registry: "registry";
                        preprint: "preprint";
                    }>>;
                    settled: z.ZodOptional<z.ZodBoolean>;
                    tone: z.ZodOptional<z.ZodEnum<{
                        danger: "danger";
                        warning: "warning";
                        success: "success";
                    }>>;
                    basis: z.ZodOptional<z.ZodEnum<{
                        law: "law";
                        estimate: "estimate";
                        pending: "pending";
                        proposal: "proposal";
                    }>>;
                }, z.core.$strict>>;
                emphasis: z.ZodOptional<z.ZodBoolean>;
            }, z.core.$strict>>;
            tag_column: z.ZodOptional<z.ZodString>;
            recommended: z.ZodOptional<z.ZodNumber>;
            recommended_label: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"icon_cards">;
            title: z.ZodOptional<z.ZodString>;
            items: z.ZodArray<z.ZodObject<{
                icon: z.ZodEnum<{
                    [x: string]: string;
                }>;
                title: z.ZodString;
                text: z.ZodString;
                tag: z.ZodOptional<z.ZodObject<{
                    text: z.ZodString;
                    quiet: z.ZodOptional<z.ZodBoolean>;
                    evidence: z.ZodOptional<z.ZodEnum<{
                        label: "label";
                        draft: "draft";
                        trial: "trial";
                        company: "company";
                        press: "press";
                        official: "official";
                        registry: "registry";
                        preprint: "preprint";
                    }>>;
                    settled: z.ZodOptional<z.ZodBoolean>;
                    tone: z.ZodOptional<z.ZodEnum<{
                        danger: "danger";
                        warning: "warning";
                        success: "success";
                    }>>;
                    basis: z.ZodOptional<z.ZodEnum<{
                        law: "law";
                        estimate: "estimate";
                        pending: "pending";
                        proposal: "proposal";
                    }>>;
                }, z.core.$strict>>;
                tone: z.ZodOptional<z.ZodEnum<{
                    danger: "danger";
                    warning: "warning";
                    success: "success";
                }>>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"row_cards">;
            items: z.ZodArray<z.ZodObject<{
                icon: z.ZodOptional<z.ZodEnum<{
                    [x: string]: string;
                }>>;
                title: z.ZodString;
                text: z.ZodOptional<z.ZodString>;
                sub: z.ZodOptional<z.ZodString>;
                highlight: z.ZodOptional<z.ZodBoolean>;
                tone: z.ZodOptional<z.ZodEnum<{
                    danger: "danger";
                    warning: "warning";
                    success: "success";
                }>>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"steps">;
            items: z.ZodArray<z.ZodObject<{
                title: z.ZodString;
                text: z.ZodString;
                icon: z.ZodOptional<z.ZodEnum<{
                    [x: string]: string;
                }>>;
                tone: z.ZodOptional<z.ZodEnum<{
                    danger: "danger";
                    warning: "warning";
                    success: "success";
                }>>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"rings">;
            items: z.ZodArray<z.ZodObject<{
                label: z.ZodString;
                desc: z.ZodOptional<z.ZodString>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"numbered_cards">;
            items: z.ZodArray<z.ZodObject<{
                title: z.ZodString;
                text: z.ZodOptional<z.ZodString>;
                sub: z.ZodOptional<z.ZodString>;
                icon: z.ZodOptional<z.ZodEnum<{
                    [x: string]: string;
                }>>;
                emphasis: z.ZodOptional<z.ZodBoolean>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"roadmap">;
            items: z.ZodArray<z.ZodObject<{
                title: z.ZodString;
                period: z.ZodOptional<z.ZodString>;
                icon: z.ZodOptional<z.ZodEnum<{
                    [x: string]: string;
                }>>;
                rows: z.ZodOptional<z.ZodArray<z.ZodObject<{
                    label: z.ZodString;
                    value: z.ZodString;
                    basis: z.ZodOptional<z.ZodEnum<{
                        law: "law";
                        estimate: "estimate";
                        pending: "pending";
                        proposal: "proposal";
                    }>>;
                }, z.core.$strict>>>;
                duration: z.ZodOptional<z.ZodNumber>;
                checkpoint: z.ZodOptional<z.ZodString>;
                points: z.ZodOptional<z.ZodArray<z.ZodString>>;
                emphasis: z.ZodOptional<z.ZodBoolean>;
            }, z.core.$strict>>;
            duration_unit: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"matrix">;
            title: z.ZodOptional<z.ZodString>;
            x_title: z.ZodOptional<z.ZodString>;
            y_title: z.ZodOptional<z.ZodString>;
            cols: z.ZodNumber;
            columns: z.ZodOptional<z.ZodArray<z.ZodString>>;
            rows: z.ZodOptional<z.ZodArray<z.ZodObject<{
                label: z.ZodString;
                icon: z.ZodOptional<z.ZodEnum<{
                    [x: string]: string;
                }>>;
            }, z.core.$strict>>>;
            items: z.ZodArray<z.ZodObject<{
                title: z.ZodString;
                tag: z.ZodOptional<z.ZodString>;
                tone: z.ZodOptional<z.ZodEnum<{
                    info: "info";
                    neutral: "neutral";
                    accent: "accent";
                }>>;
                empty: z.ZodOptional<z.ZodBoolean>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"insight_panel">;
            title: z.ZodString;
            icon: z.ZodOptional<z.ZodEnum<{
                [x: string]: string;
            }>>;
            rows: z.ZodArray<z.ZodObject<{
                label: z.ZodString;
                text: z.ZodString;
            }, z.core.$strict>>;
            footnote: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"verdict_banner">;
            text: z.ZodString;
            tone: z.ZodEnum<{
                warning: "warning";
                positive: "positive";
                neutral: "neutral";
            }>;
            icon: z.ZodOptional<z.ZodEnum<{
                [x: string]: string;
            }>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"image">;
            asset_id: z.ZodString;
            caption: z.ZodOptional<z.ZodString>;
            fit: z.ZodDefault<z.ZodEnum<{
                cover: "cover";
                contain: "contain";
            }>>;
            crop: z.ZodOptional<z.ZodArray<z.ZodNumber>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"image_grid">;
            items: z.ZodArray<z.ZodObject<{
                asset_id: z.ZodString;
                caption: z.ZodOptional<z.ZodString>;
                icon: z.ZodOptional<z.ZodEnum<{
                    [x: string]: string;
                }>>;
                tag: z.ZodOptional<z.ZodObject<{
                    text: z.ZodString;
                    quiet: z.ZodOptional<z.ZodBoolean>;
                    evidence: z.ZodOptional<z.ZodEnum<{
                        label: "label";
                        draft: "draft";
                        trial: "trial";
                        company: "company";
                        press: "press";
                        official: "official";
                        registry: "registry";
                        preprint: "preprint";
                    }>>;
                    settled: z.ZodOptional<z.ZodBoolean>;
                    tone: z.ZodOptional<z.ZodEnum<{
                        danger: "danger";
                        warning: "warning";
                        success: "success";
                    }>>;
                    basis: z.ZodOptional<z.ZodEnum<{
                        law: "law";
                        estimate: "estimate";
                        pending: "pending";
                        proposal: "proposal";
                    }>>;
                }, z.core.$strict>>;
                crop: z.ZodOptional<z.ZodArray<z.ZodNumber>>;
            }, z.core.$strict>>;
            emphasis: z.ZodOptional<z.ZodEnum<{
                none: "none";
                first: "first";
            }>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"image_compare">;
            left: z.ZodObject<{
                asset_id: z.ZodString;
                label: z.ZodString;
            }, z.core.$strict>;
            right: z.ZodObject<{
                asset_id: z.ZodString;
                label: z.ZodString;
            }, z.core.$strict>;
            style: z.ZodOptional<z.ZodEnum<{
                vs: "vs";
                before_after: "before_after";
            }>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"logo_wall">;
            title: z.ZodOptional<z.ZodString>;
            items: z.ZodArray<z.ZodObject<{
                name: z.ZodString;
                asset_id: z.ZodOptional<z.ZodString>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"product_cards">;
            items: z.ZodArray<z.ZodObject<{
                asset_id: z.ZodString;
                name: z.ZodString;
                note: z.ZodOptional<z.ZodString>;
                price: z.ZodOptional<z.ZodString>;
                price_unit: z.ZodOptional<z.ZodString>;
                featured: z.ZodOptional<z.ZodLiteral<true>>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"quote_wall">;
            quotes: z.ZodArray<z.ZodObject<{
                text: z.ZodString;
                name: z.ZodString;
                role: z.ZodOptional<z.ZodString>;
                featured: z.ZodOptional<z.ZodLiteral<true>>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"swot">;
            strengths: z.ZodArray<z.ZodString>;
            weaknesses: z.ZodArray<z.ZodString>;
            opportunities: z.ZodArray<z.ZodString>;
            threats: z.ZodArray<z.ZodString>;
            labels: z.ZodOptional<z.ZodObject<{
                strengths: z.ZodOptional<z.ZodString>;
                weaknesses: z.ZodOptional<z.ZodString>;
                opportunities: z.ZodOptional<z.ZodString>;
                threats: z.ZodOptional<z.ZodString>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"bmc">;
            key_partners: z.ZodArray<z.ZodString>;
            key_activities: z.ZodArray<z.ZodString>;
            key_resources: z.ZodArray<z.ZodString>;
            value_propositions: z.ZodArray<z.ZodString>;
            customer_relationships: z.ZodArray<z.ZodString>;
            channels: z.ZodArray<z.ZodString>;
            customer_segments: z.ZodArray<z.ZodString>;
            cost_structure: z.ZodArray<z.ZodString>;
            revenue_streams: z.ZodArray<z.ZodString>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"waterfall">;
            title: z.ZodOptional<z.ZodString>;
            items: z.ZodArray<z.ZodObject<{
                label: z.ZodString;
                value: z.ZodNumber;
                kind: z.ZodOptional<z.ZodEnum<{
                    delta: "delta";
                    total: "total";
                }>>;
                note: z.ZodOptional<z.ZodString>;
                emphasis: z.ZodOptional<z.ZodBoolean>;
            }, z.core.$strict>>;
            unit: z.ZodOptional<z.ZodString>;
            emphasis_label: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"gantt">;
            items: z.ZodArray<z.ZodObject<{
                label: z.ZodString;
                start: z.ZodNumber;
                end: z.ZodNumber;
                text: z.ZodOptional<z.ZodString>;
                emphasis: z.ZodOptional<z.ZodBoolean>;
                icon: z.ZodOptional<z.ZodEnum<{
                    [x: string]: string;
                }>>;
                period: z.ZodOptional<z.ZodString>;
                basis: z.ZodOptional<z.ZodEnum<{
                    law: "law";
                    estimate: "estimate";
                    pending: "pending";
                    proposal: "proposal";
                }>>;
            }, z.core.$strict>>;
            axis_labels: z.ZodOptional<z.ZodArray<z.ZodString>>;
            range: z.ZodOptional<z.ZodObject<{
                from: z.ZodNumber;
                to: z.ZodNumber;
            }, z.core.$strict>>;
            milestones: z.ZodOptional<z.ZodArray<z.ZodObject<{
                at: z.ZodNumber;
                label: z.ZodString;
            }, z.core.$strict>>>;
            bands: z.ZodOptional<z.ZodArray<z.ZodObject<{
                from: z.ZodNumber;
                to: z.ZodNumber;
                label: z.ZodString;
            }, z.core.$strict>>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"pest">;
            political: z.ZodObject<{
                title: z.ZodOptional<z.ZodString>;
                items: z.ZodArray<z.ZodString>;
            }, z.core.$strict>;
            economic: z.ZodObject<{
                title: z.ZodOptional<z.ZodString>;
                items: z.ZodArray<z.ZodString>;
            }, z.core.$strict>;
            social: z.ZodObject<{
                title: z.ZodOptional<z.ZodString>;
                items: z.ZodArray<z.ZodString>;
            }, z.core.$strict>;
            technological: z.ZodObject<{
                title: z.ZodOptional<z.ZodString>;
                items: z.ZodArray<z.ZodString>;
            }, z.core.$strict>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"five_forces">;
            rivalry: z.ZodObject<{
                label: z.ZodOptional<z.ZodString>;
                intensity: z.ZodOptional<z.ZodEnum<{
                    low: "low";
                    medium: "medium";
                    high: "high";
                }>>;
                items: z.ZodArray<z.ZodString>;
            }, z.core.$strict>;
            new_entrants: z.ZodObject<{
                label: z.ZodOptional<z.ZodString>;
                intensity: z.ZodOptional<z.ZodEnum<{
                    low: "low";
                    medium: "medium";
                    high: "high";
                }>>;
                items: z.ZodArray<z.ZodString>;
            }, z.core.$strict>;
            supplier_power: z.ZodObject<{
                label: z.ZodOptional<z.ZodString>;
                intensity: z.ZodOptional<z.ZodEnum<{
                    low: "low";
                    medium: "medium";
                    high: "high";
                }>>;
                items: z.ZodArray<z.ZodString>;
            }, z.core.$strict>;
            buyer_power: z.ZodObject<{
                label: z.ZodOptional<z.ZodString>;
                intensity: z.ZodOptional<z.ZodEnum<{
                    low: "low";
                    medium: "medium";
                    high: "high";
                }>>;
                items: z.ZodArray<z.ZodString>;
            }, z.core.$strict>;
            substitutes: z.ZodObject<{
                label: z.ZodOptional<z.ZodString>;
                intensity: z.ZodOptional<z.ZodEnum<{
                    low: "low";
                    medium: "medium";
                    high: "high";
                }>>;
                items: z.ZodArray<z.ZodString>;
            }, z.core.$strict>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"heatmap">;
            x_labels: z.ZodArray<z.ZodString>;
            y_labels: z.ZodArray<z.ZodString>;
            values: z.ZodArray<z.ZodArray<z.ZodNumber>>;
            domain: z.ZodOptional<z.ZodObject<{
                min: z.ZodNumber;
                max: z.ZodNumber;
            }, z.core.$strict>>;
            show_values: z.ZodOptional<z.ZodBoolean>;
            x_title: z.ZodOptional<z.ZodString>;
            y_title: z.ZodOptional<z.ZodString>;
            label_every: z.ZodOptional<z.ZodNumber>;
            steps: z.ZodOptional<z.ZodArray<z.ZodObject<{
                max: z.ZodOptional<z.ZodNumber>;
                label: z.ZodString;
                short: z.ZodOptional<z.ZodString>;
            }, z.core.$strict>>>;
            bands: z.ZodOptional<z.ZodArray<z.ZodObject<{
                from: z.ZodString;
                to: z.ZodString;
                label: z.ZodString;
                icon: z.ZodOptional<z.ZodEnum<{
                    [x: string]: string;
                }>>;
            }, z.core.$strict>>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"sankey">;
            nodes: z.ZodArray<z.ZodObject<{
                id: z.ZodString;
                label: z.ZodString;
            }, z.core.$strict>>;
            links: z.ZodArray<z.ZodObject<{
                from: z.ZodString;
                to: z.ZodString;
                value: z.ZodNumber;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"data_table">;
            title: z.ZodOptional<z.ZodString>;
            columns: z.ZodArray<z.ZodObject<{
                key: z.ZodString;
                label: z.ZodString;
                align: z.ZodOptional<z.ZodEnum<{
                    left: "left";
                    right: "right";
                    center: "center";
                }>>;
                emphasis: z.ZodOptional<z.ZodBoolean>;
                icon: z.ZodOptional<z.ZodEnum<{
                    [x: string]: string;
                }>>;
            }, z.core.$strict>>;
            rows: z.ZodArray<z.ZodObject<{
                cells: z.ZodRecord<z.ZodString, z.ZodUnion<readonly [z.ZodString, z.ZodNumber]>>;
                emphasis: z.ZodOptional<z.ZodEnum<{
                    highlight: "highlight";
                    total: "total";
                }>>;
                icon: z.ZodOptional<z.ZodEnum<{
                    [x: string]: string;
                }>>;
                tag: z.ZodOptional<z.ZodObject<{
                    text: z.ZodString;
                    quiet: z.ZodOptional<z.ZodBoolean>;
                    evidence: z.ZodOptional<z.ZodEnum<{
                        label: "label";
                        draft: "draft";
                        trial: "trial";
                        company: "company";
                        press: "press";
                        official: "official";
                        registry: "registry";
                        preprint: "preprint";
                    }>>;
                    settled: z.ZodOptional<z.ZodBoolean>;
                    tone: z.ZodOptional<z.ZodEnum<{
                        danger: "danger";
                        warning: "warning";
                        success: "success";
                    }>>;
                    basis: z.ZodOptional<z.ZodEnum<{
                        law: "law";
                        estimate: "estimate";
                        pending: "pending";
                        proposal: "proposal";
                    }>>;
                }, z.core.$strict>>;
            }, z.core.$strict>>;
            source: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"device_mockup">;
            device: z.ZodEnum<{
                phone: "phone";
                browser: "browser";
            }>;
            asset_id: z.ZodString;
            caption: z.ZodOptional<z.ZodString>;
            url: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"cycle">;
            title: z.ZodOptional<z.ZodString>;
            items: z.ZodArray<z.ZodObject<{
                label: z.ZodString;
                description: z.ZodOptional<z.ZodString>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"people_cards">;
            title: z.ZodOptional<z.ZodString>;
            people: z.ZodArray<z.ZodObject<{
                name: z.ZodString;
                role: z.ZodOptional<z.ZodString>;
                org: z.ZodOptional<z.ZodString>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"hub_spoke">;
            center: z.ZodString;
            items: z.ZodArray<z.ZodObject<{
                label: z.ZodString;
                description: z.ZodOptional<z.ZodString>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"progress_donuts">;
            items: z.ZodArray<z.ZodObject<{
                value: z.ZodString;
                unit: z.ZodOptional<z.ZodString>;
                label: z.ZodString;
                icon: z.ZodOptional<z.ZodEnum<{
                    [x: string]: string;
                }>>;
                source: z.ZodOptional<z.ZodString>;
                detail: z.ZodOptional<z.ZodString>;
                emphasis: z.ZodOptional<z.ZodBoolean>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"staircase">;
            items: z.ZodArray<z.ZodObject<{
                title: z.ZodString;
                value: z.ZodString;
                unit: z.ZodOptional<z.ZodString>;
                note: z.ZodOptional<z.ZodString>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"chevron_process">;
            items: z.ZodArray<z.ZodObject<{
                title: z.ZodString;
                text: z.ZodOptional<z.ZodString>;
                icon: z.ZodOptional<z.ZodEnum<{
                    [x: string]: string;
                }>>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"swimlane">;
            lanes: z.ZodArray<z.ZodObject<{
                label: z.ZodString;
                role: z.ZodOptional<z.ZodString>;
            }, z.core.$strict>>;
            steps: z.ZodArray<z.ZodObject<{
                lane: z.ZodString;
                title: z.ZodString;
                detail: z.ZodOptional<z.ZodString>;
            }, z.core.$strict>>;
            handoff_note: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"journey_map">;
            stages: z.ZodArray<z.ZodObject<{
                label: z.ZodString;
                touchpoints: z.ZodOptional<z.ZodArray<z.ZodString>>;
                action: z.ZodOptional<z.ZodString>;
                emotion: z.ZodNumber;
                opportunity: z.ZodOptional<z.ZodString>;
            }, z.core.$strict>>;
            row_labels: z.ZodOptional<z.ZodObject<{
                touchpoints: z.ZodOptional<z.ZodString>;
                action: z.ZodOptional<z.ZodString>;
                emotion: z.ZodOptional<z.ZodString>;
                opportunity: z.ZodOptional<z.ZodString>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"decision_tree">;
            question: z.ZodString;
            branches: z.ZodArray<z.ZodObject<{
                edge: z.ZodString;
                title: z.ZodString;
                detail: z.ZodOptional<z.ZodString>;
                outcomes: z.ZodArray<z.ZodObject<{
                    edge: z.ZodString;
                    title: z.ZodString;
                    detail: z.ZodOptional<z.ZodString>;
                    value: z.ZodOptional<z.ZodString>;
                    unit: z.ZodOptional<z.ZodString>;
                    recommended: z.ZodOptional<z.ZodBoolean>;
                }, z.core.$strict>>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"from_to">;
            from: z.ZodObject<{
                kicker: z.ZodOptional<z.ZodString>;
                title: z.ZodString;
            }, z.core.$strict>;
            to: z.ZodObject<{
                kicker: z.ZodOptional<z.ZodString>;
                title: z.ZodString;
            }, z.core.$strict>;
            rows: z.ZodArray<z.ZodObject<{
                label: z.ZodString;
                icon: z.ZodOptional<z.ZodEnum<{
                    [x: string]: string;
                }>>;
                note: z.ZodOptional<z.ZodString>;
                from: z.ZodString;
                to: z.ZodString;
                unit: z.ZodOptional<z.ZodString>;
                change: z.ZodOptional<z.ZodString>;
                tag: z.ZodOptional<z.ZodObject<{
                    text: z.ZodString;
                    quiet: z.ZodOptional<z.ZodBoolean>;
                    evidence: z.ZodOptional<z.ZodEnum<{
                        label: "label";
                        draft: "draft";
                        trial: "trial";
                        company: "company";
                        press: "press";
                        official: "official";
                        registry: "registry";
                        preprint: "preprint";
                    }>>;
                    settled: z.ZodOptional<z.ZodBoolean>;
                    tone: z.ZodOptional<z.ZodEnum<{
                        danger: "danger";
                        warning: "warning";
                        success: "success";
                    }>>;
                    basis: z.ZodOptional<z.ZodEnum<{
                        law: "law";
                        estimate: "estimate";
                        pending: "pending";
                        proposal: "proposal";
                    }>>;
                }, z.core.$strict>>;
                emphasis: z.ZodOptional<z.ZodBoolean>;
            }, z.core.$strict>>;
            label_column: z.ZodOptional<z.ZodString>;
            span: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"org_tree">;
            root: z.ZodObject<{
                name: z.ZodString;
                role: z.ZodOptional<z.ZodString>;
            }, z.core.$strict>;
            children: z.ZodArray<z.ZodObject<{
                name: z.ZodString;
                role: z.ZodOptional<z.ZodString>;
                children: z.ZodOptional<z.ZodArray<z.ZodObject<{
                    name: z.ZodString;
                    role: z.ZodOptional<z.ZodString>;
                }, z.core.$strict>>>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"issue_tree">;
            question: z.ZodString;
            children_column: z.ZodOptional<z.ZodString>;
            branches: z.ZodArray<z.ZodObject<{
                label: z.ZodString;
                note: z.ZodOptional<z.ZodString>;
                icon: z.ZodOptional<z.ZodEnum<{
                    [x: string]: string;
                }>>;
                emphasis: z.ZodOptional<z.ZodLiteral<true>>;
                children: z.ZodOptional<z.ZodArray<z.ZodObject<{
                    label: z.ZodString;
                }, z.core.$strict>>>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"pyramid">;
            layers: z.ZodArray<z.ZodObject<{
                label: z.ZodString;
                note: z.ZodOptional<z.ZodString>;
                tone: z.ZodOptional<z.ZodEnum<{
                    danger: "danger";
                    warning: "warning";
                    success: "success";
                }>>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"iceberg">;
            above: z.ZodArray<z.ZodString>;
            below: z.ZodArray<z.ZodString>;
            waterline: z.ZodOptional<z.ZodString>;
            above_label: z.ZodOptional<z.ZodString>;
            below_label: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"pillar_model">;
            goal: z.ZodString;
            pillars: z.ZodArray<z.ZodObject<{
                title: z.ZodString;
                value: z.ZodString;
                unit: z.ZodOptional<z.ZodString>;
            }, z.core.$strict>>;
            base: z.ZodString;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"value_chain">;
            primary: z.ZodArray<z.ZodObject<{
                label: z.ZodString;
                value: z.ZodOptional<z.ZodString>;
                unit: z.ZodOptional<z.ZodString>;
                emphasis: z.ZodOptional<z.ZodLiteral<true>>;
            }, z.core.$strict>>;
            support: z.ZodArray<z.ZodObject<{
                label: z.ZodString;
                note: z.ZodOptional<z.ZodString>;
            }, z.core.$strict>>;
            margin: z.ZodOptional<z.ZodObject<{
                label: z.ZodString;
                value: z.ZodOptional<z.ZodString>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"harvey_balls">;
            criteria: z.ZodArray<z.ZodString>;
            options: z.ZodArray<z.ZodObject<{
                label: z.ZodString;
                scores: z.ZodArray<z.ZodUnion<readonly [z.ZodLiteral<0>, z.ZodLiteral<25>, z.ZodLiteral<50>, z.ZodLiteral<75>, z.ZodLiteral<100>]>>;
                total: z.ZodOptional<z.ZodUnion<readonly [z.ZodString, z.ZodNumber]>>;
                highlight: z.ZodOptional<z.ZodBoolean>;
            }, z.core.$strict>>;
            legend: z.ZodOptional<z.ZodBoolean>;
            labels: z.ZodOptional<z.ZodObject<{
                option: z.ZodOptional<z.ZodString>;
                total: z.ZodOptional<z.ZodString>;
                none: z.ZodOptional<z.ZodString>;
                partial: z.ZodOptional<z.ZodString>;
                full: z.ZodOptional<z.ZodString>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"scorecard">;
            labels: z.ZodOptional<z.ZodObject<{
                metric: z.ZodOptional<z.ZodString>;
                target: z.ZodOptional<z.ZodString>;
                actual: z.ZodOptional<z.ZodString>;
                gap: z.ZodOptional<z.ZodString>;
                status: z.ZodOptional<z.ZodString>;
            }, z.core.$strict>>;
            rows: z.ZodArray<z.ZodObject<{
                label: z.ZodString;
                target: z.ZodString;
                actual: z.ZodString;
                gap: z.ZodString;
                status: z.ZodEnum<{
                    watch: "watch";
                    on_track: "on_track";
                    off_track: "off_track";
                }>;
                status_label: z.ZodOptional<z.ZodString>;
            }, z.core.$strict>>;
            note: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"pictogram">;
            rows: z.ZodArray<z.ZodObject<{
                filled: z.ZodNumber;
                label: z.ZodString;
                caption: z.ZodOptional<z.ZodString>;
                highlight: z.ZodOptional<z.ZodBoolean>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"word_cloud">;
            words: z.ZodArray<z.ZodObject<{
                text: z.ZodString;
                weight: z.ZodUnion<readonly [z.ZodLiteral<1>, z.ZodLiteral<2>, z.ZodLiteral<3>, z.ZodLiteral<4>]>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"venn">;
            sets: z.ZodArray<z.ZodObject<{
                label: z.ZodString;
            }, z.core.$strict>>;
            center: z.ZodString;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"fishbone">;
            effect: z.ZodString;
            ribs: z.ZodArray<z.ZodObject<{
                label: z.ZodString;
                causes: z.ZodArray<z.ZodString>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"positioning_map">;
            x_axis: z.ZodObject<{
                title: z.ZodString;
                low: z.ZodString;
                high: z.ZodString;
            }, z.core.$strict>;
            y_axis: z.ZodObject<{
                title: z.ZodString;
                low: z.ZodString;
                high: z.ZodString;
            }, z.core.$strict>;
            quadrants: z.ZodOptional<z.ZodObject<{
                top_left: z.ZodString;
                top_right: z.ZodString;
                bottom_left: z.ZodString;
                bottom_right: z.ZodString;
            }, z.core.$strict>>;
            points: z.ZodArray<z.ZodObject<{
                label: z.ZodString;
                x: z.ZodNumber;
                y: z.ZodNumber;
                emphasis: z.ZodOptional<z.ZodLiteral<true>>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"concept_equation">;
            operands: z.ZodArray<z.ZodObject<{
                label: z.ZodString;
                value: z.ZodOptional<z.ZodString>;
                note: z.ZodOptional<z.ZodString>;
                icon: z.ZodOptional<z.ZodEnum<{
                    [x: string]: string;
                }>>;
            }, z.core.$strict>>;
            result: z.ZodObject<{
                label: z.ZodString;
                value: z.ZodOptional<z.ZodString>;
                note: z.ZodOptional<z.ZodString>;
                icon: z.ZodOptional<z.ZodEnum<{
                    [x: string]: string;
                }>>;
            }, z.core.$strict>;
            excluded: z.ZodOptional<z.ZodObject<{
                label: z.ZodString;
                value: z.ZodOptional<z.ZodString>;
                note: z.ZodOptional<z.ZodString>;
                icon: z.ZodOptional<z.ZodEnum<{
                    [x: string]: string;
                }>>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"segmented_wheel">;
            center: z.ZodString;
            segments: z.ZodArray<z.ZodObject<{
                label: z.ZodString;
                value: z.ZodOptional<z.ZodString>;
                emphasis: z.ZodOptional<z.ZodLiteral<true>>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"pros_cons">;
            pros: z.ZodObject<{
                title: z.ZodString;
                items: z.ZodArray<z.ZodObject<{
                    label: z.ZodString;
                    note: z.ZodOptional<z.ZodString>;
                }, z.core.$strict>>;
            }, z.core.$strict>;
            cons: z.ZodObject<{
                title: z.ZodString;
                items: z.ZodArray<z.ZodObject<{
                    label: z.ZodString;
                    note: z.ZodOptional<z.ZodString>;
                }, z.core.$strict>>;
            }, z.core.$strict>;
            verdict: z.ZodString;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"sketch">;
            kind: z.ZodEnum<{
                discontinuity: "discontinuity";
                difference_in_differences: "difference_in_differences";
            }>;
            at: z.ZodString;
            x_title: z.ZodString;
            y_title: z.ZodOptional<z.ZodString>;
            effect: z.ZodOptional<z.ZodString>;
            groups: z.ZodOptional<z.ZodArray<z.ZodString>>;
            direction: z.ZodOptional<z.ZodEnum<{
                up: "up";
                down: "down";
            }>>;
        }, z.core.$strict>], "type">>>;
        background: z.ZodOptional<z.ZodDiscriminatedUnion<[z.ZodObject<{
            kind: z.ZodLiteral<"color">;
            value: z.ZodString;
        }, z.core.$strict>, z.ZodObject<{
            kind: z.ZodLiteral<"gradient">;
            from: z.ZodString;
            to: z.ZodString;
            direction: z.ZodOptional<z.ZodEnum<{
                tb: "tb";
                lr: "lr";
                diagonal: "diagonal";
            }>>;
        }, z.core.$strict>, z.ZodObject<{
            kind: z.ZodLiteral<"asset">;
            asset_id: z.ZodString;
            overlay: z.ZodOptional<z.ZodObject<{
                color: z.ZodString;
                opacity: z.ZodNumber;
            }, z.core.$strict>>;
            fit: z.ZodOptional<z.ZodEnum<{
                cover: "cover";
                contain: "contain";
            }>>;
        }, z.core.$strict>], "kind">>;
        decor: z.ZodOptional<z.ZodObject<{
            kind: z.ZodEnum<{
                big_number: "big_number";
                corner_tag: "corner_tag";
                rule_line: "rule_line";
                quote_marks: "quote_marks";
                geo_dots: "geo_dots";
            }>;
            intensity: z.ZodOptional<z.ZodEnum<{
                subtle: "subtle";
                normal: "normal";
            }>>;
            text: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>>;
        image_side: z.ZodOptional<z.ZodEnum<{
            left: "left";
            right: "right";
        }>>;
        footnote: z.ZodOptional<z.ZodString>;
        notes: z.ZodOptional<z.ZodString>;
        type: z.ZodLiteral<"cover">;
    }, z.core.$strict>, z.ZodObject<{
        id: z.ZodOptional<z.ZodString>;
        placeholder: z.ZodOptional<z.ZodLiteral<true>>;
        heading: z.ZodOptional<z.ZodString>;
        subheading: z.ZodOptional<z.ZodString>;
        kicker: z.ZodOptional<z.ZodString>;
        fields: z.ZodOptional<z.ZodArray<z.ZodObject<{
            label: z.ZodString;
            value: z.ZodString;
            note: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>>>;
        stamp: z.ZodOptional<z.ZodObject<{
            text: z.ZodString;
            date: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>>;
        ballot: z.ZodOptional<z.ZodObject<{
            choices: z.ZodArray<z.ZodString>;
            signature: z.ZodOptional<z.ZodString>;
            item_choices: z.ZodOptional<z.ZodArray<z.ZodObject<{
                item: z.ZodNumber;
                choices: z.ZodArray<z.ZodString>;
            }, z.core.$strict>>>;
        }, z.core.$strict>>;
        tag: z.ZodOptional<z.ZodObject<{
            text: z.ZodString;
            quiet: z.ZodOptional<z.ZodBoolean>;
            evidence: z.ZodOptional<z.ZodEnum<{
                label: "label";
                draft: "draft";
                trial: "trial";
                company: "company";
                press: "press";
                official: "official";
                registry: "registry";
                preprint: "preprint";
            }>>;
            settled: z.ZodOptional<z.ZodBoolean>;
            tone: z.ZodOptional<z.ZodEnum<{
                danger: "danger";
                warning: "warning";
                success: "success";
            }>>;
            basis: z.ZodOptional<z.ZodEnum<{
                law: "law";
                estimate: "estimate";
                pending: "pending";
                proposal: "proposal";
            }>>;
        }, z.core.$strict>>;
        years: z.ZodOptional<z.ZodObject<{
            from: z.ZodNumber;
            to: z.ZodNumber;
            marked: z.ZodArray<z.ZodNumber>;
        }, z.core.$strict>>;
        stage: z.ZodOptional<z.ZodString>;
        components: z.ZodDefault<z.ZodArray<z.ZodDiscriminatedUnion<[z.ZodObject<{
            type: z.ZodLiteral<"bullets">;
            items: z.ZodArray<z.ZodString>;
            style: z.ZodOptional<z.ZodEnum<{
                default: "default";
                checklist: "checklist";
                numbered: "numbered";
                plain: "plain";
                divided: "divided";
            }>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"paragraph">;
            text: z.ZodString;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"blockquote">;
            text: z.ZodString;
            attribution: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"callout">;
            variant: z.ZodEnum<{
                info: "info";
                warn: "warn";
                tip: "tip";
            }>;
            title: z.ZodOptional<z.ZodString>;
            text: z.ZodString;
            icon: z.ZodOptional<z.ZodEnum<{
                [x: string]: string;
            }>>;
            tag: z.ZodOptional<z.ZodObject<{
                text: z.ZodString;
                quiet: z.ZodOptional<z.ZodBoolean>;
                evidence: z.ZodOptional<z.ZodEnum<{
                    label: "label";
                    draft: "draft";
                    trial: "trial";
                    company: "company";
                    press: "press";
                    official: "official";
                    registry: "registry";
                    preprint: "preprint";
                }>>;
                settled: z.ZodOptional<z.ZodBoolean>;
                tone: z.ZodOptional<z.ZodEnum<{
                    danger: "danger";
                    warning: "warning";
                    success: "success";
                }>>;
                basis: z.ZodOptional<z.ZodEnum<{
                    law: "law";
                    estimate: "estimate";
                    pending: "pending";
                    proposal: "proposal";
                }>>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"code">;
            language: z.ZodString;
            code: z.ZodString;
            title: z.ZodOptional<z.ZodString>;
            highlight_lines: z.ZodOptional<z.ZodArray<z.ZodNumber>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"kpi_cards">;
            items: z.ZodArray<z.ZodObject<{
                value: z.ZodString;
                unit: z.ZodOptional<z.ZodString>;
                label: z.ZodString;
                note: z.ZodOptional<z.ZodString>;
                tag: z.ZodOptional<z.ZodObject<{
                    text: z.ZodString;
                    quiet: z.ZodOptional<z.ZodBoolean>;
                    evidence: z.ZodOptional<z.ZodEnum<{
                        label: "label";
                        draft: "draft";
                        trial: "trial";
                        company: "company";
                        press: "press";
                        official: "official";
                        registry: "registry";
                        preprint: "preprint";
                    }>>;
                    settled: z.ZodOptional<z.ZodBoolean>;
                    tone: z.ZodOptional<z.ZodEnum<{
                        danger: "danger";
                        warning: "warning";
                        success: "success";
                    }>>;
                    basis: z.ZodOptional<z.ZodEnum<{
                        law: "law";
                        estimate: "estimate";
                        pending: "pending";
                        proposal: "proposal";
                    }>>;
                }, z.core.$strict>>;
                delta: z.ZodOptional<z.ZodEnum<{
                    flat: "flat";
                    up: "up";
                    down: "down";
                }>>;
                delta_good: z.ZodOptional<z.ZodBoolean>;
                icon: z.ZodOptional<z.ZodEnum<{
                    [x: string]: string;
                }>>;
                tone: z.ZodOptional<z.ZodEnum<{
                    danger: "danger";
                    warning: "warning";
                    success: "success";
                }>>;
                source: z.ZodOptional<z.ZodString>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"chart">;
            title: z.ZodOptional<z.ZodString>;
            chart_type: z.ZodEnum<{
                line: "line";
                donut: "donut";
                dumbbell: "dumbbell";
                funnel: "funnel";
                gauge: "gauge";
                bar: "bar";
                stacked: "stacked";
                percent_stacked: "percent_stacked";
                pie: "pie";
                area: "area";
                combo: "combo";
                scatter: "scatter";
            }>;
            direction: z.ZodOptional<z.ZodEnum<{
                horizontal: "horizontal";
                vertical: "vertical";
            }>>;
            style: z.ZodOptional<z.ZodEnum<{
                donut: "donut";
            }>>;
            center_total: z.ZodOptional<z.ZodBoolean>;
            gauge: z.ZodOptional<z.ZodObject<{
                min: z.ZodOptional<z.ZodNumber>;
                max: z.ZodOptional<z.ZodNumber>;
            }, z.core.$strict>>;
            axes: z.ZodOptional<z.ZodObject<{
                x_title: z.ZodOptional<z.ZodString>;
                y_title: z.ZodOptional<z.ZodString>;
                x_unit: z.ZodOptional<z.ZodString>;
                y_unit: z.ZodOptional<z.ZodString>;
                y2_title: z.ZodOptional<z.ZodString>;
                y2_unit: z.ZodOptional<z.ZodString>;
                show_grid: z.ZodOptional<z.ZodBoolean>;
            }, z.core.$strict>>;
            tag: z.ZodOptional<z.ZodObject<{
                text: z.ZodString;
                quiet: z.ZodOptional<z.ZodBoolean>;
                evidence: z.ZodOptional<z.ZodEnum<{
                    label: "label";
                    draft: "draft";
                    trial: "trial";
                    company: "company";
                    press: "press";
                    official: "official";
                    registry: "registry";
                    preprint: "preprint";
                }>>;
                settled: z.ZodOptional<z.ZodBoolean>;
                tone: z.ZodOptional<z.ZodEnum<{
                    danger: "danger";
                    warning: "warning";
                    success: "success";
                }>>;
                basis: z.ZodOptional<z.ZodEnum<{
                    law: "law";
                    estimate: "estimate";
                    pending: "pending";
                    proposal: "proposal";
                }>>;
            }, z.core.$strict>>;
            changes: z.ZodOptional<z.ZodArray<z.ZodObject<{
                from: z.ZodString;
                to: z.ZodString;
                at: z.ZodOptional<z.ZodString>;
            }, z.core.$strict>>>;
            bands: z.ZodOptional<z.ZodArray<z.ZodObject<{
                from: z.ZodNumber;
                to: z.ZodNumber;
                label: z.ZodOptional<z.ZodString>;
            }, z.core.$strict>>>;
            emphasis_label: z.ZodOptional<z.ZodString>;
            reference: z.ZodOptional<z.ZodObject<{
                value: z.ZodNumber;
                label: z.ZodString;
            }, z.core.$strict>>;
            markers: z.ZodOptional<z.ZodArray<z.ZodObject<{
                before: z.ZodString;
                label: z.ZodString;
            }, z.core.$strict>>>;
            gaps: z.ZodOptional<z.ZodArray<z.ZodObject<{
                after: z.ZodString;
                x: z.ZodString;
                label: z.ZodString;
            }, z.core.$strict>>>;
            series: z.ZodArray<z.ZodObject<{
                name: z.ZodString;
                data: z.ZodArray<z.ZodObject<{
                    x: z.ZodUnion<readonly [z.ZodString, z.ZodNumber]>;
                    y: z.ZodNumber;
                    size: z.ZodOptional<z.ZodNumber>;
                    status: z.ZodOptional<z.ZodEnum<{
                        target: "target";
                        estimate: "estimate";
                        forecast: "forecast";
                    }>>;
                    emphasis: z.ZodOptional<z.ZodBoolean>;
                    note: z.ZodOptional<z.ZodString>;
                    icon: z.ZodOptional<z.ZodEnum<{
                        [x: string]: string;
                    }>>;
                    upper: z.ZodOptional<z.ZodNumber>;
                }, z.core.$strict>>;
                plot: z.ZodOptional<z.ZodEnum<{
                    line: "line";
                    bar: "bar";
                }>>;
                axis: z.ZodOptional<z.ZodEnum<{
                    left: "left";
                    right: "right";
                }>>;
                emphasis: z.ZodOptional<z.ZodBoolean>;
                steps: z.ZodOptional<z.ZodBoolean>;
                tone: z.ZodOptional<z.ZodEnum<{
                    danger: "danger";
                    warning: "warning";
                    success: "success";
                }>>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"flowchart">;
            nodes: z.ZodArray<z.ZodObject<{
                id: z.ZodString;
                label: z.ZodString;
                kind: z.ZodOptional<z.ZodEnum<{
                    rect: "rect";
                    diamond: "diamond";
                    round: "round";
                }>>;
            }, z.core.$strict>>;
            edges: z.ZodArray<z.ZodObject<{
                from: z.ZodString;
                to: z.ZodString;
                label: z.ZodOptional<z.ZodString>;
            }, z.core.$strict>>;
            direction: z.ZodOptional<z.ZodEnum<{
                TB: "TB";
                TD: "TD";
                BT: "BT";
                LR: "LR";
                RL: "RL";
            }>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"architecture">;
            layers: z.ZodArray<z.ZodObject<{
                title: z.ZodString;
                items: z.ZodArray<z.ZodString>;
            }, z.core.$strict>>;
            direction: z.ZodOptional<z.ZodEnum<{
                top_down: "top_down";
                bottom_up: "bottom_up";
            }>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"timeline">;
            title: z.ZodOptional<z.ZodString>;
            layout: z.ZodOptional<z.ZodEnum<{
                horizontal: "horizontal";
                vertical: "vertical";
            }>>;
            lanes: z.ZodOptional<z.ZodArray<z.ZodString>>;
            periods: z.ZodOptional<z.ZodArray<z.ZodObject<{
                from: z.ZodString;
                to: z.ZodString;
                label: z.ZodString;
                basis: z.ZodOptional<z.ZodEnum<{
                    law: "law";
                    estimate: "estimate";
                    pending: "pending";
                    proposal: "proposal";
                }>>;
            }, z.core.$strict>>>;
            milestones: z.ZodArray<z.ZodObject<{
                date: z.ZodString;
                title: z.ZodString;
                desc: z.ZodOptional<z.ZodString>;
                highlight: z.ZodOptional<z.ZodBoolean>;
                icon: z.ZodOptional<z.ZodEnum<{
                    [x: string]: string;
                }>>;
                tone: z.ZodOptional<z.ZodEnum<{
                    danger: "danger";
                    warning: "warning";
                    success: "success";
                }>>;
                status: z.ZodOptional<z.ZodEnum<{
                    pending: "pending";
                }>>;
                tag: z.ZodOptional<z.ZodObject<{
                    text: z.ZodString;
                    quiet: z.ZodOptional<z.ZodBoolean>;
                    evidence: z.ZodOptional<z.ZodEnum<{
                        label: "label";
                        draft: "draft";
                        trial: "trial";
                        company: "company";
                        press: "press";
                        official: "official";
                        registry: "registry";
                        preprint: "preprint";
                    }>>;
                    settled: z.ZodOptional<z.ZodBoolean>;
                    tone: z.ZodOptional<z.ZodEnum<{
                        danger: "danger";
                        warning: "warning";
                        success: "success";
                    }>>;
                    basis: z.ZodOptional<z.ZodEnum<{
                        law: "law";
                        estimate: "estimate";
                        pending: "pending";
                        proposal: "proposal";
                    }>>;
                }, z.core.$strict>>;
                source: z.ZodOptional<z.ZodString>;
                lane: z.ZodOptional<z.ZodString>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"comparison">;
            title: z.ZodOptional<z.ZodString>;
            columns: z.ZodArray<z.ZodString>;
            label_column: z.ZodOptional<z.ZodString>;
            rows: z.ZodArray<z.ZodObject<{
                label: z.ZodString;
                cells: z.ZodArray<z.ZodString>;
                icon: z.ZodOptional<z.ZodEnum<{
                    [x: string]: string;
                }>>;
                tag: z.ZodOptional<z.ZodObject<{
                    text: z.ZodString;
                    quiet: z.ZodOptional<z.ZodBoolean>;
                    evidence: z.ZodOptional<z.ZodEnum<{
                        label: "label";
                        draft: "draft";
                        trial: "trial";
                        company: "company";
                        press: "press";
                        official: "official";
                        registry: "registry";
                        preprint: "preprint";
                    }>>;
                    settled: z.ZodOptional<z.ZodBoolean>;
                    tone: z.ZodOptional<z.ZodEnum<{
                        danger: "danger";
                        warning: "warning";
                        success: "success";
                    }>>;
                    basis: z.ZodOptional<z.ZodEnum<{
                        law: "law";
                        estimate: "estimate";
                        pending: "pending";
                        proposal: "proposal";
                    }>>;
                }, z.core.$strict>>;
                emphasis: z.ZodOptional<z.ZodBoolean>;
            }, z.core.$strict>>;
            tag_column: z.ZodOptional<z.ZodString>;
            recommended: z.ZodOptional<z.ZodNumber>;
            recommended_label: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"icon_cards">;
            title: z.ZodOptional<z.ZodString>;
            items: z.ZodArray<z.ZodObject<{
                icon: z.ZodEnum<{
                    [x: string]: string;
                }>;
                title: z.ZodString;
                text: z.ZodString;
                tag: z.ZodOptional<z.ZodObject<{
                    text: z.ZodString;
                    quiet: z.ZodOptional<z.ZodBoolean>;
                    evidence: z.ZodOptional<z.ZodEnum<{
                        label: "label";
                        draft: "draft";
                        trial: "trial";
                        company: "company";
                        press: "press";
                        official: "official";
                        registry: "registry";
                        preprint: "preprint";
                    }>>;
                    settled: z.ZodOptional<z.ZodBoolean>;
                    tone: z.ZodOptional<z.ZodEnum<{
                        danger: "danger";
                        warning: "warning";
                        success: "success";
                    }>>;
                    basis: z.ZodOptional<z.ZodEnum<{
                        law: "law";
                        estimate: "estimate";
                        pending: "pending";
                        proposal: "proposal";
                    }>>;
                }, z.core.$strict>>;
                tone: z.ZodOptional<z.ZodEnum<{
                    danger: "danger";
                    warning: "warning";
                    success: "success";
                }>>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"row_cards">;
            items: z.ZodArray<z.ZodObject<{
                icon: z.ZodOptional<z.ZodEnum<{
                    [x: string]: string;
                }>>;
                title: z.ZodString;
                text: z.ZodOptional<z.ZodString>;
                sub: z.ZodOptional<z.ZodString>;
                highlight: z.ZodOptional<z.ZodBoolean>;
                tone: z.ZodOptional<z.ZodEnum<{
                    danger: "danger";
                    warning: "warning";
                    success: "success";
                }>>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"steps">;
            items: z.ZodArray<z.ZodObject<{
                title: z.ZodString;
                text: z.ZodString;
                icon: z.ZodOptional<z.ZodEnum<{
                    [x: string]: string;
                }>>;
                tone: z.ZodOptional<z.ZodEnum<{
                    danger: "danger";
                    warning: "warning";
                    success: "success";
                }>>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"rings">;
            items: z.ZodArray<z.ZodObject<{
                label: z.ZodString;
                desc: z.ZodOptional<z.ZodString>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"numbered_cards">;
            items: z.ZodArray<z.ZodObject<{
                title: z.ZodString;
                text: z.ZodOptional<z.ZodString>;
                sub: z.ZodOptional<z.ZodString>;
                icon: z.ZodOptional<z.ZodEnum<{
                    [x: string]: string;
                }>>;
                emphasis: z.ZodOptional<z.ZodBoolean>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"roadmap">;
            items: z.ZodArray<z.ZodObject<{
                title: z.ZodString;
                period: z.ZodOptional<z.ZodString>;
                icon: z.ZodOptional<z.ZodEnum<{
                    [x: string]: string;
                }>>;
                rows: z.ZodOptional<z.ZodArray<z.ZodObject<{
                    label: z.ZodString;
                    value: z.ZodString;
                    basis: z.ZodOptional<z.ZodEnum<{
                        law: "law";
                        estimate: "estimate";
                        pending: "pending";
                        proposal: "proposal";
                    }>>;
                }, z.core.$strict>>>;
                duration: z.ZodOptional<z.ZodNumber>;
                checkpoint: z.ZodOptional<z.ZodString>;
                points: z.ZodOptional<z.ZodArray<z.ZodString>>;
                emphasis: z.ZodOptional<z.ZodBoolean>;
            }, z.core.$strict>>;
            duration_unit: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"matrix">;
            title: z.ZodOptional<z.ZodString>;
            x_title: z.ZodOptional<z.ZodString>;
            y_title: z.ZodOptional<z.ZodString>;
            cols: z.ZodNumber;
            columns: z.ZodOptional<z.ZodArray<z.ZodString>>;
            rows: z.ZodOptional<z.ZodArray<z.ZodObject<{
                label: z.ZodString;
                icon: z.ZodOptional<z.ZodEnum<{
                    [x: string]: string;
                }>>;
            }, z.core.$strict>>>;
            items: z.ZodArray<z.ZodObject<{
                title: z.ZodString;
                tag: z.ZodOptional<z.ZodString>;
                tone: z.ZodOptional<z.ZodEnum<{
                    info: "info";
                    neutral: "neutral";
                    accent: "accent";
                }>>;
                empty: z.ZodOptional<z.ZodBoolean>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"insight_panel">;
            title: z.ZodString;
            icon: z.ZodOptional<z.ZodEnum<{
                [x: string]: string;
            }>>;
            rows: z.ZodArray<z.ZodObject<{
                label: z.ZodString;
                text: z.ZodString;
            }, z.core.$strict>>;
            footnote: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"verdict_banner">;
            text: z.ZodString;
            tone: z.ZodEnum<{
                warning: "warning";
                positive: "positive";
                neutral: "neutral";
            }>;
            icon: z.ZodOptional<z.ZodEnum<{
                [x: string]: string;
            }>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"image">;
            asset_id: z.ZodString;
            caption: z.ZodOptional<z.ZodString>;
            fit: z.ZodDefault<z.ZodEnum<{
                cover: "cover";
                contain: "contain";
            }>>;
            crop: z.ZodOptional<z.ZodArray<z.ZodNumber>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"image_grid">;
            items: z.ZodArray<z.ZodObject<{
                asset_id: z.ZodString;
                caption: z.ZodOptional<z.ZodString>;
                icon: z.ZodOptional<z.ZodEnum<{
                    [x: string]: string;
                }>>;
                tag: z.ZodOptional<z.ZodObject<{
                    text: z.ZodString;
                    quiet: z.ZodOptional<z.ZodBoolean>;
                    evidence: z.ZodOptional<z.ZodEnum<{
                        label: "label";
                        draft: "draft";
                        trial: "trial";
                        company: "company";
                        press: "press";
                        official: "official";
                        registry: "registry";
                        preprint: "preprint";
                    }>>;
                    settled: z.ZodOptional<z.ZodBoolean>;
                    tone: z.ZodOptional<z.ZodEnum<{
                        danger: "danger";
                        warning: "warning";
                        success: "success";
                    }>>;
                    basis: z.ZodOptional<z.ZodEnum<{
                        law: "law";
                        estimate: "estimate";
                        pending: "pending";
                        proposal: "proposal";
                    }>>;
                }, z.core.$strict>>;
                crop: z.ZodOptional<z.ZodArray<z.ZodNumber>>;
            }, z.core.$strict>>;
            emphasis: z.ZodOptional<z.ZodEnum<{
                none: "none";
                first: "first";
            }>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"image_compare">;
            left: z.ZodObject<{
                asset_id: z.ZodString;
                label: z.ZodString;
            }, z.core.$strict>;
            right: z.ZodObject<{
                asset_id: z.ZodString;
                label: z.ZodString;
            }, z.core.$strict>;
            style: z.ZodOptional<z.ZodEnum<{
                vs: "vs";
                before_after: "before_after";
            }>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"logo_wall">;
            title: z.ZodOptional<z.ZodString>;
            items: z.ZodArray<z.ZodObject<{
                name: z.ZodString;
                asset_id: z.ZodOptional<z.ZodString>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"product_cards">;
            items: z.ZodArray<z.ZodObject<{
                asset_id: z.ZodString;
                name: z.ZodString;
                note: z.ZodOptional<z.ZodString>;
                price: z.ZodOptional<z.ZodString>;
                price_unit: z.ZodOptional<z.ZodString>;
                featured: z.ZodOptional<z.ZodLiteral<true>>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"quote_wall">;
            quotes: z.ZodArray<z.ZodObject<{
                text: z.ZodString;
                name: z.ZodString;
                role: z.ZodOptional<z.ZodString>;
                featured: z.ZodOptional<z.ZodLiteral<true>>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"swot">;
            strengths: z.ZodArray<z.ZodString>;
            weaknesses: z.ZodArray<z.ZodString>;
            opportunities: z.ZodArray<z.ZodString>;
            threats: z.ZodArray<z.ZodString>;
            labels: z.ZodOptional<z.ZodObject<{
                strengths: z.ZodOptional<z.ZodString>;
                weaknesses: z.ZodOptional<z.ZodString>;
                opportunities: z.ZodOptional<z.ZodString>;
                threats: z.ZodOptional<z.ZodString>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"bmc">;
            key_partners: z.ZodArray<z.ZodString>;
            key_activities: z.ZodArray<z.ZodString>;
            key_resources: z.ZodArray<z.ZodString>;
            value_propositions: z.ZodArray<z.ZodString>;
            customer_relationships: z.ZodArray<z.ZodString>;
            channels: z.ZodArray<z.ZodString>;
            customer_segments: z.ZodArray<z.ZodString>;
            cost_structure: z.ZodArray<z.ZodString>;
            revenue_streams: z.ZodArray<z.ZodString>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"waterfall">;
            title: z.ZodOptional<z.ZodString>;
            items: z.ZodArray<z.ZodObject<{
                label: z.ZodString;
                value: z.ZodNumber;
                kind: z.ZodOptional<z.ZodEnum<{
                    delta: "delta";
                    total: "total";
                }>>;
                note: z.ZodOptional<z.ZodString>;
                emphasis: z.ZodOptional<z.ZodBoolean>;
            }, z.core.$strict>>;
            unit: z.ZodOptional<z.ZodString>;
            emphasis_label: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"gantt">;
            items: z.ZodArray<z.ZodObject<{
                label: z.ZodString;
                start: z.ZodNumber;
                end: z.ZodNumber;
                text: z.ZodOptional<z.ZodString>;
                emphasis: z.ZodOptional<z.ZodBoolean>;
                icon: z.ZodOptional<z.ZodEnum<{
                    [x: string]: string;
                }>>;
                period: z.ZodOptional<z.ZodString>;
                basis: z.ZodOptional<z.ZodEnum<{
                    law: "law";
                    estimate: "estimate";
                    pending: "pending";
                    proposal: "proposal";
                }>>;
            }, z.core.$strict>>;
            axis_labels: z.ZodOptional<z.ZodArray<z.ZodString>>;
            range: z.ZodOptional<z.ZodObject<{
                from: z.ZodNumber;
                to: z.ZodNumber;
            }, z.core.$strict>>;
            milestones: z.ZodOptional<z.ZodArray<z.ZodObject<{
                at: z.ZodNumber;
                label: z.ZodString;
            }, z.core.$strict>>>;
            bands: z.ZodOptional<z.ZodArray<z.ZodObject<{
                from: z.ZodNumber;
                to: z.ZodNumber;
                label: z.ZodString;
            }, z.core.$strict>>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"pest">;
            political: z.ZodObject<{
                title: z.ZodOptional<z.ZodString>;
                items: z.ZodArray<z.ZodString>;
            }, z.core.$strict>;
            economic: z.ZodObject<{
                title: z.ZodOptional<z.ZodString>;
                items: z.ZodArray<z.ZodString>;
            }, z.core.$strict>;
            social: z.ZodObject<{
                title: z.ZodOptional<z.ZodString>;
                items: z.ZodArray<z.ZodString>;
            }, z.core.$strict>;
            technological: z.ZodObject<{
                title: z.ZodOptional<z.ZodString>;
                items: z.ZodArray<z.ZodString>;
            }, z.core.$strict>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"five_forces">;
            rivalry: z.ZodObject<{
                label: z.ZodOptional<z.ZodString>;
                intensity: z.ZodOptional<z.ZodEnum<{
                    low: "low";
                    medium: "medium";
                    high: "high";
                }>>;
                items: z.ZodArray<z.ZodString>;
            }, z.core.$strict>;
            new_entrants: z.ZodObject<{
                label: z.ZodOptional<z.ZodString>;
                intensity: z.ZodOptional<z.ZodEnum<{
                    low: "low";
                    medium: "medium";
                    high: "high";
                }>>;
                items: z.ZodArray<z.ZodString>;
            }, z.core.$strict>;
            supplier_power: z.ZodObject<{
                label: z.ZodOptional<z.ZodString>;
                intensity: z.ZodOptional<z.ZodEnum<{
                    low: "low";
                    medium: "medium";
                    high: "high";
                }>>;
                items: z.ZodArray<z.ZodString>;
            }, z.core.$strict>;
            buyer_power: z.ZodObject<{
                label: z.ZodOptional<z.ZodString>;
                intensity: z.ZodOptional<z.ZodEnum<{
                    low: "low";
                    medium: "medium";
                    high: "high";
                }>>;
                items: z.ZodArray<z.ZodString>;
            }, z.core.$strict>;
            substitutes: z.ZodObject<{
                label: z.ZodOptional<z.ZodString>;
                intensity: z.ZodOptional<z.ZodEnum<{
                    low: "low";
                    medium: "medium";
                    high: "high";
                }>>;
                items: z.ZodArray<z.ZodString>;
            }, z.core.$strict>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"heatmap">;
            x_labels: z.ZodArray<z.ZodString>;
            y_labels: z.ZodArray<z.ZodString>;
            values: z.ZodArray<z.ZodArray<z.ZodNumber>>;
            domain: z.ZodOptional<z.ZodObject<{
                min: z.ZodNumber;
                max: z.ZodNumber;
            }, z.core.$strict>>;
            show_values: z.ZodOptional<z.ZodBoolean>;
            x_title: z.ZodOptional<z.ZodString>;
            y_title: z.ZodOptional<z.ZodString>;
            label_every: z.ZodOptional<z.ZodNumber>;
            steps: z.ZodOptional<z.ZodArray<z.ZodObject<{
                max: z.ZodOptional<z.ZodNumber>;
                label: z.ZodString;
                short: z.ZodOptional<z.ZodString>;
            }, z.core.$strict>>>;
            bands: z.ZodOptional<z.ZodArray<z.ZodObject<{
                from: z.ZodString;
                to: z.ZodString;
                label: z.ZodString;
                icon: z.ZodOptional<z.ZodEnum<{
                    [x: string]: string;
                }>>;
            }, z.core.$strict>>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"sankey">;
            nodes: z.ZodArray<z.ZodObject<{
                id: z.ZodString;
                label: z.ZodString;
            }, z.core.$strict>>;
            links: z.ZodArray<z.ZodObject<{
                from: z.ZodString;
                to: z.ZodString;
                value: z.ZodNumber;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"data_table">;
            title: z.ZodOptional<z.ZodString>;
            columns: z.ZodArray<z.ZodObject<{
                key: z.ZodString;
                label: z.ZodString;
                align: z.ZodOptional<z.ZodEnum<{
                    left: "left";
                    right: "right";
                    center: "center";
                }>>;
                emphasis: z.ZodOptional<z.ZodBoolean>;
                icon: z.ZodOptional<z.ZodEnum<{
                    [x: string]: string;
                }>>;
            }, z.core.$strict>>;
            rows: z.ZodArray<z.ZodObject<{
                cells: z.ZodRecord<z.ZodString, z.ZodUnion<readonly [z.ZodString, z.ZodNumber]>>;
                emphasis: z.ZodOptional<z.ZodEnum<{
                    highlight: "highlight";
                    total: "total";
                }>>;
                icon: z.ZodOptional<z.ZodEnum<{
                    [x: string]: string;
                }>>;
                tag: z.ZodOptional<z.ZodObject<{
                    text: z.ZodString;
                    quiet: z.ZodOptional<z.ZodBoolean>;
                    evidence: z.ZodOptional<z.ZodEnum<{
                        label: "label";
                        draft: "draft";
                        trial: "trial";
                        company: "company";
                        press: "press";
                        official: "official";
                        registry: "registry";
                        preprint: "preprint";
                    }>>;
                    settled: z.ZodOptional<z.ZodBoolean>;
                    tone: z.ZodOptional<z.ZodEnum<{
                        danger: "danger";
                        warning: "warning";
                        success: "success";
                    }>>;
                    basis: z.ZodOptional<z.ZodEnum<{
                        law: "law";
                        estimate: "estimate";
                        pending: "pending";
                        proposal: "proposal";
                    }>>;
                }, z.core.$strict>>;
            }, z.core.$strict>>;
            source: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"device_mockup">;
            device: z.ZodEnum<{
                phone: "phone";
                browser: "browser";
            }>;
            asset_id: z.ZodString;
            caption: z.ZodOptional<z.ZodString>;
            url: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"cycle">;
            title: z.ZodOptional<z.ZodString>;
            items: z.ZodArray<z.ZodObject<{
                label: z.ZodString;
                description: z.ZodOptional<z.ZodString>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"people_cards">;
            title: z.ZodOptional<z.ZodString>;
            people: z.ZodArray<z.ZodObject<{
                name: z.ZodString;
                role: z.ZodOptional<z.ZodString>;
                org: z.ZodOptional<z.ZodString>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"hub_spoke">;
            center: z.ZodString;
            items: z.ZodArray<z.ZodObject<{
                label: z.ZodString;
                description: z.ZodOptional<z.ZodString>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"progress_donuts">;
            items: z.ZodArray<z.ZodObject<{
                value: z.ZodString;
                unit: z.ZodOptional<z.ZodString>;
                label: z.ZodString;
                icon: z.ZodOptional<z.ZodEnum<{
                    [x: string]: string;
                }>>;
                source: z.ZodOptional<z.ZodString>;
                detail: z.ZodOptional<z.ZodString>;
                emphasis: z.ZodOptional<z.ZodBoolean>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"staircase">;
            items: z.ZodArray<z.ZodObject<{
                title: z.ZodString;
                value: z.ZodString;
                unit: z.ZodOptional<z.ZodString>;
                note: z.ZodOptional<z.ZodString>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"chevron_process">;
            items: z.ZodArray<z.ZodObject<{
                title: z.ZodString;
                text: z.ZodOptional<z.ZodString>;
                icon: z.ZodOptional<z.ZodEnum<{
                    [x: string]: string;
                }>>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"swimlane">;
            lanes: z.ZodArray<z.ZodObject<{
                label: z.ZodString;
                role: z.ZodOptional<z.ZodString>;
            }, z.core.$strict>>;
            steps: z.ZodArray<z.ZodObject<{
                lane: z.ZodString;
                title: z.ZodString;
                detail: z.ZodOptional<z.ZodString>;
            }, z.core.$strict>>;
            handoff_note: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"journey_map">;
            stages: z.ZodArray<z.ZodObject<{
                label: z.ZodString;
                touchpoints: z.ZodOptional<z.ZodArray<z.ZodString>>;
                action: z.ZodOptional<z.ZodString>;
                emotion: z.ZodNumber;
                opportunity: z.ZodOptional<z.ZodString>;
            }, z.core.$strict>>;
            row_labels: z.ZodOptional<z.ZodObject<{
                touchpoints: z.ZodOptional<z.ZodString>;
                action: z.ZodOptional<z.ZodString>;
                emotion: z.ZodOptional<z.ZodString>;
                opportunity: z.ZodOptional<z.ZodString>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"decision_tree">;
            question: z.ZodString;
            branches: z.ZodArray<z.ZodObject<{
                edge: z.ZodString;
                title: z.ZodString;
                detail: z.ZodOptional<z.ZodString>;
                outcomes: z.ZodArray<z.ZodObject<{
                    edge: z.ZodString;
                    title: z.ZodString;
                    detail: z.ZodOptional<z.ZodString>;
                    value: z.ZodOptional<z.ZodString>;
                    unit: z.ZodOptional<z.ZodString>;
                    recommended: z.ZodOptional<z.ZodBoolean>;
                }, z.core.$strict>>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"from_to">;
            from: z.ZodObject<{
                kicker: z.ZodOptional<z.ZodString>;
                title: z.ZodString;
            }, z.core.$strict>;
            to: z.ZodObject<{
                kicker: z.ZodOptional<z.ZodString>;
                title: z.ZodString;
            }, z.core.$strict>;
            rows: z.ZodArray<z.ZodObject<{
                label: z.ZodString;
                icon: z.ZodOptional<z.ZodEnum<{
                    [x: string]: string;
                }>>;
                note: z.ZodOptional<z.ZodString>;
                from: z.ZodString;
                to: z.ZodString;
                unit: z.ZodOptional<z.ZodString>;
                change: z.ZodOptional<z.ZodString>;
                tag: z.ZodOptional<z.ZodObject<{
                    text: z.ZodString;
                    quiet: z.ZodOptional<z.ZodBoolean>;
                    evidence: z.ZodOptional<z.ZodEnum<{
                        label: "label";
                        draft: "draft";
                        trial: "trial";
                        company: "company";
                        press: "press";
                        official: "official";
                        registry: "registry";
                        preprint: "preprint";
                    }>>;
                    settled: z.ZodOptional<z.ZodBoolean>;
                    tone: z.ZodOptional<z.ZodEnum<{
                        danger: "danger";
                        warning: "warning";
                        success: "success";
                    }>>;
                    basis: z.ZodOptional<z.ZodEnum<{
                        law: "law";
                        estimate: "estimate";
                        pending: "pending";
                        proposal: "proposal";
                    }>>;
                }, z.core.$strict>>;
                emphasis: z.ZodOptional<z.ZodBoolean>;
            }, z.core.$strict>>;
            label_column: z.ZodOptional<z.ZodString>;
            span: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"org_tree">;
            root: z.ZodObject<{
                name: z.ZodString;
                role: z.ZodOptional<z.ZodString>;
            }, z.core.$strict>;
            children: z.ZodArray<z.ZodObject<{
                name: z.ZodString;
                role: z.ZodOptional<z.ZodString>;
                children: z.ZodOptional<z.ZodArray<z.ZodObject<{
                    name: z.ZodString;
                    role: z.ZodOptional<z.ZodString>;
                }, z.core.$strict>>>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"issue_tree">;
            question: z.ZodString;
            children_column: z.ZodOptional<z.ZodString>;
            branches: z.ZodArray<z.ZodObject<{
                label: z.ZodString;
                note: z.ZodOptional<z.ZodString>;
                icon: z.ZodOptional<z.ZodEnum<{
                    [x: string]: string;
                }>>;
                emphasis: z.ZodOptional<z.ZodLiteral<true>>;
                children: z.ZodOptional<z.ZodArray<z.ZodObject<{
                    label: z.ZodString;
                }, z.core.$strict>>>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"pyramid">;
            layers: z.ZodArray<z.ZodObject<{
                label: z.ZodString;
                note: z.ZodOptional<z.ZodString>;
                tone: z.ZodOptional<z.ZodEnum<{
                    danger: "danger";
                    warning: "warning";
                    success: "success";
                }>>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"iceberg">;
            above: z.ZodArray<z.ZodString>;
            below: z.ZodArray<z.ZodString>;
            waterline: z.ZodOptional<z.ZodString>;
            above_label: z.ZodOptional<z.ZodString>;
            below_label: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"pillar_model">;
            goal: z.ZodString;
            pillars: z.ZodArray<z.ZodObject<{
                title: z.ZodString;
                value: z.ZodString;
                unit: z.ZodOptional<z.ZodString>;
            }, z.core.$strict>>;
            base: z.ZodString;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"value_chain">;
            primary: z.ZodArray<z.ZodObject<{
                label: z.ZodString;
                value: z.ZodOptional<z.ZodString>;
                unit: z.ZodOptional<z.ZodString>;
                emphasis: z.ZodOptional<z.ZodLiteral<true>>;
            }, z.core.$strict>>;
            support: z.ZodArray<z.ZodObject<{
                label: z.ZodString;
                note: z.ZodOptional<z.ZodString>;
            }, z.core.$strict>>;
            margin: z.ZodOptional<z.ZodObject<{
                label: z.ZodString;
                value: z.ZodOptional<z.ZodString>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"harvey_balls">;
            criteria: z.ZodArray<z.ZodString>;
            options: z.ZodArray<z.ZodObject<{
                label: z.ZodString;
                scores: z.ZodArray<z.ZodUnion<readonly [z.ZodLiteral<0>, z.ZodLiteral<25>, z.ZodLiteral<50>, z.ZodLiteral<75>, z.ZodLiteral<100>]>>;
                total: z.ZodOptional<z.ZodUnion<readonly [z.ZodString, z.ZodNumber]>>;
                highlight: z.ZodOptional<z.ZodBoolean>;
            }, z.core.$strict>>;
            legend: z.ZodOptional<z.ZodBoolean>;
            labels: z.ZodOptional<z.ZodObject<{
                option: z.ZodOptional<z.ZodString>;
                total: z.ZodOptional<z.ZodString>;
                none: z.ZodOptional<z.ZodString>;
                partial: z.ZodOptional<z.ZodString>;
                full: z.ZodOptional<z.ZodString>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"scorecard">;
            labels: z.ZodOptional<z.ZodObject<{
                metric: z.ZodOptional<z.ZodString>;
                target: z.ZodOptional<z.ZodString>;
                actual: z.ZodOptional<z.ZodString>;
                gap: z.ZodOptional<z.ZodString>;
                status: z.ZodOptional<z.ZodString>;
            }, z.core.$strict>>;
            rows: z.ZodArray<z.ZodObject<{
                label: z.ZodString;
                target: z.ZodString;
                actual: z.ZodString;
                gap: z.ZodString;
                status: z.ZodEnum<{
                    watch: "watch";
                    on_track: "on_track";
                    off_track: "off_track";
                }>;
                status_label: z.ZodOptional<z.ZodString>;
            }, z.core.$strict>>;
            note: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"pictogram">;
            rows: z.ZodArray<z.ZodObject<{
                filled: z.ZodNumber;
                label: z.ZodString;
                caption: z.ZodOptional<z.ZodString>;
                highlight: z.ZodOptional<z.ZodBoolean>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"word_cloud">;
            words: z.ZodArray<z.ZodObject<{
                text: z.ZodString;
                weight: z.ZodUnion<readonly [z.ZodLiteral<1>, z.ZodLiteral<2>, z.ZodLiteral<3>, z.ZodLiteral<4>]>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"venn">;
            sets: z.ZodArray<z.ZodObject<{
                label: z.ZodString;
            }, z.core.$strict>>;
            center: z.ZodString;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"fishbone">;
            effect: z.ZodString;
            ribs: z.ZodArray<z.ZodObject<{
                label: z.ZodString;
                causes: z.ZodArray<z.ZodString>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"positioning_map">;
            x_axis: z.ZodObject<{
                title: z.ZodString;
                low: z.ZodString;
                high: z.ZodString;
            }, z.core.$strict>;
            y_axis: z.ZodObject<{
                title: z.ZodString;
                low: z.ZodString;
                high: z.ZodString;
            }, z.core.$strict>;
            quadrants: z.ZodOptional<z.ZodObject<{
                top_left: z.ZodString;
                top_right: z.ZodString;
                bottom_left: z.ZodString;
                bottom_right: z.ZodString;
            }, z.core.$strict>>;
            points: z.ZodArray<z.ZodObject<{
                label: z.ZodString;
                x: z.ZodNumber;
                y: z.ZodNumber;
                emphasis: z.ZodOptional<z.ZodLiteral<true>>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"concept_equation">;
            operands: z.ZodArray<z.ZodObject<{
                label: z.ZodString;
                value: z.ZodOptional<z.ZodString>;
                note: z.ZodOptional<z.ZodString>;
                icon: z.ZodOptional<z.ZodEnum<{
                    [x: string]: string;
                }>>;
            }, z.core.$strict>>;
            result: z.ZodObject<{
                label: z.ZodString;
                value: z.ZodOptional<z.ZodString>;
                note: z.ZodOptional<z.ZodString>;
                icon: z.ZodOptional<z.ZodEnum<{
                    [x: string]: string;
                }>>;
            }, z.core.$strict>;
            excluded: z.ZodOptional<z.ZodObject<{
                label: z.ZodString;
                value: z.ZodOptional<z.ZodString>;
                note: z.ZodOptional<z.ZodString>;
                icon: z.ZodOptional<z.ZodEnum<{
                    [x: string]: string;
                }>>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"segmented_wheel">;
            center: z.ZodString;
            segments: z.ZodArray<z.ZodObject<{
                label: z.ZodString;
                value: z.ZodOptional<z.ZodString>;
                emphasis: z.ZodOptional<z.ZodLiteral<true>>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"pros_cons">;
            pros: z.ZodObject<{
                title: z.ZodString;
                items: z.ZodArray<z.ZodObject<{
                    label: z.ZodString;
                    note: z.ZodOptional<z.ZodString>;
                }, z.core.$strict>>;
            }, z.core.$strict>;
            cons: z.ZodObject<{
                title: z.ZodString;
                items: z.ZodArray<z.ZodObject<{
                    label: z.ZodString;
                    note: z.ZodOptional<z.ZodString>;
                }, z.core.$strict>>;
            }, z.core.$strict>;
            verdict: z.ZodString;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"sketch">;
            kind: z.ZodEnum<{
                discontinuity: "discontinuity";
                difference_in_differences: "difference_in_differences";
            }>;
            at: z.ZodString;
            x_title: z.ZodString;
            y_title: z.ZodOptional<z.ZodString>;
            effect: z.ZodOptional<z.ZodString>;
            groups: z.ZodOptional<z.ZodArray<z.ZodString>>;
            direction: z.ZodOptional<z.ZodEnum<{
                up: "up";
                down: "down";
            }>>;
        }, z.core.$strict>], "type">>>;
        background: z.ZodOptional<z.ZodDiscriminatedUnion<[z.ZodObject<{
            kind: z.ZodLiteral<"color">;
            value: z.ZodString;
        }, z.core.$strict>, z.ZodObject<{
            kind: z.ZodLiteral<"gradient">;
            from: z.ZodString;
            to: z.ZodString;
            direction: z.ZodOptional<z.ZodEnum<{
                tb: "tb";
                lr: "lr";
                diagonal: "diagonal";
            }>>;
        }, z.core.$strict>, z.ZodObject<{
            kind: z.ZodLiteral<"asset">;
            asset_id: z.ZodString;
            overlay: z.ZodOptional<z.ZodObject<{
                color: z.ZodString;
                opacity: z.ZodNumber;
            }, z.core.$strict>>;
            fit: z.ZodOptional<z.ZodEnum<{
                cover: "cover";
                contain: "contain";
            }>>;
        }, z.core.$strict>], "kind">>;
        decor: z.ZodOptional<z.ZodObject<{
            kind: z.ZodEnum<{
                big_number: "big_number";
                corner_tag: "corner_tag";
                rule_line: "rule_line";
                quote_marks: "quote_marks";
                geo_dots: "geo_dots";
            }>;
            intensity: z.ZodOptional<z.ZodEnum<{
                subtle: "subtle";
                normal: "normal";
            }>>;
            text: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>>;
        image_side: z.ZodOptional<z.ZodEnum<{
            left: "left";
            right: "right";
        }>>;
        footnote: z.ZodOptional<z.ZodString>;
        notes: z.ZodOptional<z.ZodString>;
        type: z.ZodLiteral<"chapter">;
    }, z.core.$strict>, z.ZodObject<{
        id: z.ZodOptional<z.ZodString>;
        placeholder: z.ZodOptional<z.ZodLiteral<true>>;
        heading: z.ZodOptional<z.ZodString>;
        subheading: z.ZodOptional<z.ZodString>;
        kicker: z.ZodOptional<z.ZodString>;
        fields: z.ZodOptional<z.ZodArray<z.ZodObject<{
            label: z.ZodString;
            value: z.ZodString;
            note: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>>>;
        stamp: z.ZodOptional<z.ZodObject<{
            text: z.ZodString;
            date: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>>;
        ballot: z.ZodOptional<z.ZodObject<{
            choices: z.ZodArray<z.ZodString>;
            signature: z.ZodOptional<z.ZodString>;
            item_choices: z.ZodOptional<z.ZodArray<z.ZodObject<{
                item: z.ZodNumber;
                choices: z.ZodArray<z.ZodString>;
            }, z.core.$strict>>>;
        }, z.core.$strict>>;
        tag: z.ZodOptional<z.ZodObject<{
            text: z.ZodString;
            quiet: z.ZodOptional<z.ZodBoolean>;
            evidence: z.ZodOptional<z.ZodEnum<{
                label: "label";
                draft: "draft";
                trial: "trial";
                company: "company";
                press: "press";
                official: "official";
                registry: "registry";
                preprint: "preprint";
            }>>;
            settled: z.ZodOptional<z.ZodBoolean>;
            tone: z.ZodOptional<z.ZodEnum<{
                danger: "danger";
                warning: "warning";
                success: "success";
            }>>;
            basis: z.ZodOptional<z.ZodEnum<{
                law: "law";
                estimate: "estimate";
                pending: "pending";
                proposal: "proposal";
            }>>;
        }, z.core.$strict>>;
        years: z.ZodOptional<z.ZodObject<{
            from: z.ZodNumber;
            to: z.ZodNumber;
            marked: z.ZodArray<z.ZodNumber>;
        }, z.core.$strict>>;
        stage: z.ZodOptional<z.ZodString>;
        components: z.ZodDefault<z.ZodArray<z.ZodDiscriminatedUnion<[z.ZodObject<{
            type: z.ZodLiteral<"bullets">;
            items: z.ZodArray<z.ZodString>;
            style: z.ZodOptional<z.ZodEnum<{
                default: "default";
                checklist: "checklist";
                numbered: "numbered";
                plain: "plain";
                divided: "divided";
            }>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"paragraph">;
            text: z.ZodString;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"blockquote">;
            text: z.ZodString;
            attribution: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"callout">;
            variant: z.ZodEnum<{
                info: "info";
                warn: "warn";
                tip: "tip";
            }>;
            title: z.ZodOptional<z.ZodString>;
            text: z.ZodString;
            icon: z.ZodOptional<z.ZodEnum<{
                [x: string]: string;
            }>>;
            tag: z.ZodOptional<z.ZodObject<{
                text: z.ZodString;
                quiet: z.ZodOptional<z.ZodBoolean>;
                evidence: z.ZodOptional<z.ZodEnum<{
                    label: "label";
                    draft: "draft";
                    trial: "trial";
                    company: "company";
                    press: "press";
                    official: "official";
                    registry: "registry";
                    preprint: "preprint";
                }>>;
                settled: z.ZodOptional<z.ZodBoolean>;
                tone: z.ZodOptional<z.ZodEnum<{
                    danger: "danger";
                    warning: "warning";
                    success: "success";
                }>>;
                basis: z.ZodOptional<z.ZodEnum<{
                    law: "law";
                    estimate: "estimate";
                    pending: "pending";
                    proposal: "proposal";
                }>>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"code">;
            language: z.ZodString;
            code: z.ZodString;
            title: z.ZodOptional<z.ZodString>;
            highlight_lines: z.ZodOptional<z.ZodArray<z.ZodNumber>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"kpi_cards">;
            items: z.ZodArray<z.ZodObject<{
                value: z.ZodString;
                unit: z.ZodOptional<z.ZodString>;
                label: z.ZodString;
                note: z.ZodOptional<z.ZodString>;
                tag: z.ZodOptional<z.ZodObject<{
                    text: z.ZodString;
                    quiet: z.ZodOptional<z.ZodBoolean>;
                    evidence: z.ZodOptional<z.ZodEnum<{
                        label: "label";
                        draft: "draft";
                        trial: "trial";
                        company: "company";
                        press: "press";
                        official: "official";
                        registry: "registry";
                        preprint: "preprint";
                    }>>;
                    settled: z.ZodOptional<z.ZodBoolean>;
                    tone: z.ZodOptional<z.ZodEnum<{
                        danger: "danger";
                        warning: "warning";
                        success: "success";
                    }>>;
                    basis: z.ZodOptional<z.ZodEnum<{
                        law: "law";
                        estimate: "estimate";
                        pending: "pending";
                        proposal: "proposal";
                    }>>;
                }, z.core.$strict>>;
                delta: z.ZodOptional<z.ZodEnum<{
                    flat: "flat";
                    up: "up";
                    down: "down";
                }>>;
                delta_good: z.ZodOptional<z.ZodBoolean>;
                icon: z.ZodOptional<z.ZodEnum<{
                    [x: string]: string;
                }>>;
                tone: z.ZodOptional<z.ZodEnum<{
                    danger: "danger";
                    warning: "warning";
                    success: "success";
                }>>;
                source: z.ZodOptional<z.ZodString>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"chart">;
            title: z.ZodOptional<z.ZodString>;
            chart_type: z.ZodEnum<{
                line: "line";
                donut: "donut";
                dumbbell: "dumbbell";
                funnel: "funnel";
                gauge: "gauge";
                bar: "bar";
                stacked: "stacked";
                percent_stacked: "percent_stacked";
                pie: "pie";
                area: "area";
                combo: "combo";
                scatter: "scatter";
            }>;
            direction: z.ZodOptional<z.ZodEnum<{
                horizontal: "horizontal";
                vertical: "vertical";
            }>>;
            style: z.ZodOptional<z.ZodEnum<{
                donut: "donut";
            }>>;
            center_total: z.ZodOptional<z.ZodBoolean>;
            gauge: z.ZodOptional<z.ZodObject<{
                min: z.ZodOptional<z.ZodNumber>;
                max: z.ZodOptional<z.ZodNumber>;
            }, z.core.$strict>>;
            axes: z.ZodOptional<z.ZodObject<{
                x_title: z.ZodOptional<z.ZodString>;
                y_title: z.ZodOptional<z.ZodString>;
                x_unit: z.ZodOptional<z.ZodString>;
                y_unit: z.ZodOptional<z.ZodString>;
                y2_title: z.ZodOptional<z.ZodString>;
                y2_unit: z.ZodOptional<z.ZodString>;
                show_grid: z.ZodOptional<z.ZodBoolean>;
            }, z.core.$strict>>;
            tag: z.ZodOptional<z.ZodObject<{
                text: z.ZodString;
                quiet: z.ZodOptional<z.ZodBoolean>;
                evidence: z.ZodOptional<z.ZodEnum<{
                    label: "label";
                    draft: "draft";
                    trial: "trial";
                    company: "company";
                    press: "press";
                    official: "official";
                    registry: "registry";
                    preprint: "preprint";
                }>>;
                settled: z.ZodOptional<z.ZodBoolean>;
                tone: z.ZodOptional<z.ZodEnum<{
                    danger: "danger";
                    warning: "warning";
                    success: "success";
                }>>;
                basis: z.ZodOptional<z.ZodEnum<{
                    law: "law";
                    estimate: "estimate";
                    pending: "pending";
                    proposal: "proposal";
                }>>;
            }, z.core.$strict>>;
            changes: z.ZodOptional<z.ZodArray<z.ZodObject<{
                from: z.ZodString;
                to: z.ZodString;
                at: z.ZodOptional<z.ZodString>;
            }, z.core.$strict>>>;
            bands: z.ZodOptional<z.ZodArray<z.ZodObject<{
                from: z.ZodNumber;
                to: z.ZodNumber;
                label: z.ZodOptional<z.ZodString>;
            }, z.core.$strict>>>;
            emphasis_label: z.ZodOptional<z.ZodString>;
            reference: z.ZodOptional<z.ZodObject<{
                value: z.ZodNumber;
                label: z.ZodString;
            }, z.core.$strict>>;
            markers: z.ZodOptional<z.ZodArray<z.ZodObject<{
                before: z.ZodString;
                label: z.ZodString;
            }, z.core.$strict>>>;
            gaps: z.ZodOptional<z.ZodArray<z.ZodObject<{
                after: z.ZodString;
                x: z.ZodString;
                label: z.ZodString;
            }, z.core.$strict>>>;
            series: z.ZodArray<z.ZodObject<{
                name: z.ZodString;
                data: z.ZodArray<z.ZodObject<{
                    x: z.ZodUnion<readonly [z.ZodString, z.ZodNumber]>;
                    y: z.ZodNumber;
                    size: z.ZodOptional<z.ZodNumber>;
                    status: z.ZodOptional<z.ZodEnum<{
                        target: "target";
                        estimate: "estimate";
                        forecast: "forecast";
                    }>>;
                    emphasis: z.ZodOptional<z.ZodBoolean>;
                    note: z.ZodOptional<z.ZodString>;
                    icon: z.ZodOptional<z.ZodEnum<{
                        [x: string]: string;
                    }>>;
                    upper: z.ZodOptional<z.ZodNumber>;
                }, z.core.$strict>>;
                plot: z.ZodOptional<z.ZodEnum<{
                    line: "line";
                    bar: "bar";
                }>>;
                axis: z.ZodOptional<z.ZodEnum<{
                    left: "left";
                    right: "right";
                }>>;
                emphasis: z.ZodOptional<z.ZodBoolean>;
                steps: z.ZodOptional<z.ZodBoolean>;
                tone: z.ZodOptional<z.ZodEnum<{
                    danger: "danger";
                    warning: "warning";
                    success: "success";
                }>>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"flowchart">;
            nodes: z.ZodArray<z.ZodObject<{
                id: z.ZodString;
                label: z.ZodString;
                kind: z.ZodOptional<z.ZodEnum<{
                    rect: "rect";
                    diamond: "diamond";
                    round: "round";
                }>>;
            }, z.core.$strict>>;
            edges: z.ZodArray<z.ZodObject<{
                from: z.ZodString;
                to: z.ZodString;
                label: z.ZodOptional<z.ZodString>;
            }, z.core.$strict>>;
            direction: z.ZodOptional<z.ZodEnum<{
                TB: "TB";
                TD: "TD";
                BT: "BT";
                LR: "LR";
                RL: "RL";
            }>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"architecture">;
            layers: z.ZodArray<z.ZodObject<{
                title: z.ZodString;
                items: z.ZodArray<z.ZodString>;
            }, z.core.$strict>>;
            direction: z.ZodOptional<z.ZodEnum<{
                top_down: "top_down";
                bottom_up: "bottom_up";
            }>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"timeline">;
            title: z.ZodOptional<z.ZodString>;
            layout: z.ZodOptional<z.ZodEnum<{
                horizontal: "horizontal";
                vertical: "vertical";
            }>>;
            lanes: z.ZodOptional<z.ZodArray<z.ZodString>>;
            periods: z.ZodOptional<z.ZodArray<z.ZodObject<{
                from: z.ZodString;
                to: z.ZodString;
                label: z.ZodString;
                basis: z.ZodOptional<z.ZodEnum<{
                    law: "law";
                    estimate: "estimate";
                    pending: "pending";
                    proposal: "proposal";
                }>>;
            }, z.core.$strict>>>;
            milestones: z.ZodArray<z.ZodObject<{
                date: z.ZodString;
                title: z.ZodString;
                desc: z.ZodOptional<z.ZodString>;
                highlight: z.ZodOptional<z.ZodBoolean>;
                icon: z.ZodOptional<z.ZodEnum<{
                    [x: string]: string;
                }>>;
                tone: z.ZodOptional<z.ZodEnum<{
                    danger: "danger";
                    warning: "warning";
                    success: "success";
                }>>;
                status: z.ZodOptional<z.ZodEnum<{
                    pending: "pending";
                }>>;
                tag: z.ZodOptional<z.ZodObject<{
                    text: z.ZodString;
                    quiet: z.ZodOptional<z.ZodBoolean>;
                    evidence: z.ZodOptional<z.ZodEnum<{
                        label: "label";
                        draft: "draft";
                        trial: "trial";
                        company: "company";
                        press: "press";
                        official: "official";
                        registry: "registry";
                        preprint: "preprint";
                    }>>;
                    settled: z.ZodOptional<z.ZodBoolean>;
                    tone: z.ZodOptional<z.ZodEnum<{
                        danger: "danger";
                        warning: "warning";
                        success: "success";
                    }>>;
                    basis: z.ZodOptional<z.ZodEnum<{
                        law: "law";
                        estimate: "estimate";
                        pending: "pending";
                        proposal: "proposal";
                    }>>;
                }, z.core.$strict>>;
                source: z.ZodOptional<z.ZodString>;
                lane: z.ZodOptional<z.ZodString>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"comparison">;
            title: z.ZodOptional<z.ZodString>;
            columns: z.ZodArray<z.ZodString>;
            label_column: z.ZodOptional<z.ZodString>;
            rows: z.ZodArray<z.ZodObject<{
                label: z.ZodString;
                cells: z.ZodArray<z.ZodString>;
                icon: z.ZodOptional<z.ZodEnum<{
                    [x: string]: string;
                }>>;
                tag: z.ZodOptional<z.ZodObject<{
                    text: z.ZodString;
                    quiet: z.ZodOptional<z.ZodBoolean>;
                    evidence: z.ZodOptional<z.ZodEnum<{
                        label: "label";
                        draft: "draft";
                        trial: "trial";
                        company: "company";
                        press: "press";
                        official: "official";
                        registry: "registry";
                        preprint: "preprint";
                    }>>;
                    settled: z.ZodOptional<z.ZodBoolean>;
                    tone: z.ZodOptional<z.ZodEnum<{
                        danger: "danger";
                        warning: "warning";
                        success: "success";
                    }>>;
                    basis: z.ZodOptional<z.ZodEnum<{
                        law: "law";
                        estimate: "estimate";
                        pending: "pending";
                        proposal: "proposal";
                    }>>;
                }, z.core.$strict>>;
                emphasis: z.ZodOptional<z.ZodBoolean>;
            }, z.core.$strict>>;
            tag_column: z.ZodOptional<z.ZodString>;
            recommended: z.ZodOptional<z.ZodNumber>;
            recommended_label: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"icon_cards">;
            title: z.ZodOptional<z.ZodString>;
            items: z.ZodArray<z.ZodObject<{
                icon: z.ZodEnum<{
                    [x: string]: string;
                }>;
                title: z.ZodString;
                text: z.ZodString;
                tag: z.ZodOptional<z.ZodObject<{
                    text: z.ZodString;
                    quiet: z.ZodOptional<z.ZodBoolean>;
                    evidence: z.ZodOptional<z.ZodEnum<{
                        label: "label";
                        draft: "draft";
                        trial: "trial";
                        company: "company";
                        press: "press";
                        official: "official";
                        registry: "registry";
                        preprint: "preprint";
                    }>>;
                    settled: z.ZodOptional<z.ZodBoolean>;
                    tone: z.ZodOptional<z.ZodEnum<{
                        danger: "danger";
                        warning: "warning";
                        success: "success";
                    }>>;
                    basis: z.ZodOptional<z.ZodEnum<{
                        law: "law";
                        estimate: "estimate";
                        pending: "pending";
                        proposal: "proposal";
                    }>>;
                }, z.core.$strict>>;
                tone: z.ZodOptional<z.ZodEnum<{
                    danger: "danger";
                    warning: "warning";
                    success: "success";
                }>>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"row_cards">;
            items: z.ZodArray<z.ZodObject<{
                icon: z.ZodOptional<z.ZodEnum<{
                    [x: string]: string;
                }>>;
                title: z.ZodString;
                text: z.ZodOptional<z.ZodString>;
                sub: z.ZodOptional<z.ZodString>;
                highlight: z.ZodOptional<z.ZodBoolean>;
                tone: z.ZodOptional<z.ZodEnum<{
                    danger: "danger";
                    warning: "warning";
                    success: "success";
                }>>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"steps">;
            items: z.ZodArray<z.ZodObject<{
                title: z.ZodString;
                text: z.ZodString;
                icon: z.ZodOptional<z.ZodEnum<{
                    [x: string]: string;
                }>>;
                tone: z.ZodOptional<z.ZodEnum<{
                    danger: "danger";
                    warning: "warning";
                    success: "success";
                }>>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"rings">;
            items: z.ZodArray<z.ZodObject<{
                label: z.ZodString;
                desc: z.ZodOptional<z.ZodString>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"numbered_cards">;
            items: z.ZodArray<z.ZodObject<{
                title: z.ZodString;
                text: z.ZodOptional<z.ZodString>;
                sub: z.ZodOptional<z.ZodString>;
                icon: z.ZodOptional<z.ZodEnum<{
                    [x: string]: string;
                }>>;
                emphasis: z.ZodOptional<z.ZodBoolean>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"roadmap">;
            items: z.ZodArray<z.ZodObject<{
                title: z.ZodString;
                period: z.ZodOptional<z.ZodString>;
                icon: z.ZodOptional<z.ZodEnum<{
                    [x: string]: string;
                }>>;
                rows: z.ZodOptional<z.ZodArray<z.ZodObject<{
                    label: z.ZodString;
                    value: z.ZodString;
                    basis: z.ZodOptional<z.ZodEnum<{
                        law: "law";
                        estimate: "estimate";
                        pending: "pending";
                        proposal: "proposal";
                    }>>;
                }, z.core.$strict>>>;
                duration: z.ZodOptional<z.ZodNumber>;
                checkpoint: z.ZodOptional<z.ZodString>;
                points: z.ZodOptional<z.ZodArray<z.ZodString>>;
                emphasis: z.ZodOptional<z.ZodBoolean>;
            }, z.core.$strict>>;
            duration_unit: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"matrix">;
            title: z.ZodOptional<z.ZodString>;
            x_title: z.ZodOptional<z.ZodString>;
            y_title: z.ZodOptional<z.ZodString>;
            cols: z.ZodNumber;
            columns: z.ZodOptional<z.ZodArray<z.ZodString>>;
            rows: z.ZodOptional<z.ZodArray<z.ZodObject<{
                label: z.ZodString;
                icon: z.ZodOptional<z.ZodEnum<{
                    [x: string]: string;
                }>>;
            }, z.core.$strict>>>;
            items: z.ZodArray<z.ZodObject<{
                title: z.ZodString;
                tag: z.ZodOptional<z.ZodString>;
                tone: z.ZodOptional<z.ZodEnum<{
                    info: "info";
                    neutral: "neutral";
                    accent: "accent";
                }>>;
                empty: z.ZodOptional<z.ZodBoolean>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"insight_panel">;
            title: z.ZodString;
            icon: z.ZodOptional<z.ZodEnum<{
                [x: string]: string;
            }>>;
            rows: z.ZodArray<z.ZodObject<{
                label: z.ZodString;
                text: z.ZodString;
            }, z.core.$strict>>;
            footnote: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"verdict_banner">;
            text: z.ZodString;
            tone: z.ZodEnum<{
                warning: "warning";
                positive: "positive";
                neutral: "neutral";
            }>;
            icon: z.ZodOptional<z.ZodEnum<{
                [x: string]: string;
            }>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"image">;
            asset_id: z.ZodString;
            caption: z.ZodOptional<z.ZodString>;
            fit: z.ZodDefault<z.ZodEnum<{
                cover: "cover";
                contain: "contain";
            }>>;
            crop: z.ZodOptional<z.ZodArray<z.ZodNumber>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"image_grid">;
            items: z.ZodArray<z.ZodObject<{
                asset_id: z.ZodString;
                caption: z.ZodOptional<z.ZodString>;
                icon: z.ZodOptional<z.ZodEnum<{
                    [x: string]: string;
                }>>;
                tag: z.ZodOptional<z.ZodObject<{
                    text: z.ZodString;
                    quiet: z.ZodOptional<z.ZodBoolean>;
                    evidence: z.ZodOptional<z.ZodEnum<{
                        label: "label";
                        draft: "draft";
                        trial: "trial";
                        company: "company";
                        press: "press";
                        official: "official";
                        registry: "registry";
                        preprint: "preprint";
                    }>>;
                    settled: z.ZodOptional<z.ZodBoolean>;
                    tone: z.ZodOptional<z.ZodEnum<{
                        danger: "danger";
                        warning: "warning";
                        success: "success";
                    }>>;
                    basis: z.ZodOptional<z.ZodEnum<{
                        law: "law";
                        estimate: "estimate";
                        pending: "pending";
                        proposal: "proposal";
                    }>>;
                }, z.core.$strict>>;
                crop: z.ZodOptional<z.ZodArray<z.ZodNumber>>;
            }, z.core.$strict>>;
            emphasis: z.ZodOptional<z.ZodEnum<{
                none: "none";
                first: "first";
            }>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"image_compare">;
            left: z.ZodObject<{
                asset_id: z.ZodString;
                label: z.ZodString;
            }, z.core.$strict>;
            right: z.ZodObject<{
                asset_id: z.ZodString;
                label: z.ZodString;
            }, z.core.$strict>;
            style: z.ZodOptional<z.ZodEnum<{
                vs: "vs";
                before_after: "before_after";
            }>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"logo_wall">;
            title: z.ZodOptional<z.ZodString>;
            items: z.ZodArray<z.ZodObject<{
                name: z.ZodString;
                asset_id: z.ZodOptional<z.ZodString>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"product_cards">;
            items: z.ZodArray<z.ZodObject<{
                asset_id: z.ZodString;
                name: z.ZodString;
                note: z.ZodOptional<z.ZodString>;
                price: z.ZodOptional<z.ZodString>;
                price_unit: z.ZodOptional<z.ZodString>;
                featured: z.ZodOptional<z.ZodLiteral<true>>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"quote_wall">;
            quotes: z.ZodArray<z.ZodObject<{
                text: z.ZodString;
                name: z.ZodString;
                role: z.ZodOptional<z.ZodString>;
                featured: z.ZodOptional<z.ZodLiteral<true>>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"swot">;
            strengths: z.ZodArray<z.ZodString>;
            weaknesses: z.ZodArray<z.ZodString>;
            opportunities: z.ZodArray<z.ZodString>;
            threats: z.ZodArray<z.ZodString>;
            labels: z.ZodOptional<z.ZodObject<{
                strengths: z.ZodOptional<z.ZodString>;
                weaknesses: z.ZodOptional<z.ZodString>;
                opportunities: z.ZodOptional<z.ZodString>;
                threats: z.ZodOptional<z.ZodString>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"bmc">;
            key_partners: z.ZodArray<z.ZodString>;
            key_activities: z.ZodArray<z.ZodString>;
            key_resources: z.ZodArray<z.ZodString>;
            value_propositions: z.ZodArray<z.ZodString>;
            customer_relationships: z.ZodArray<z.ZodString>;
            channels: z.ZodArray<z.ZodString>;
            customer_segments: z.ZodArray<z.ZodString>;
            cost_structure: z.ZodArray<z.ZodString>;
            revenue_streams: z.ZodArray<z.ZodString>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"waterfall">;
            title: z.ZodOptional<z.ZodString>;
            items: z.ZodArray<z.ZodObject<{
                label: z.ZodString;
                value: z.ZodNumber;
                kind: z.ZodOptional<z.ZodEnum<{
                    delta: "delta";
                    total: "total";
                }>>;
                note: z.ZodOptional<z.ZodString>;
                emphasis: z.ZodOptional<z.ZodBoolean>;
            }, z.core.$strict>>;
            unit: z.ZodOptional<z.ZodString>;
            emphasis_label: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"gantt">;
            items: z.ZodArray<z.ZodObject<{
                label: z.ZodString;
                start: z.ZodNumber;
                end: z.ZodNumber;
                text: z.ZodOptional<z.ZodString>;
                emphasis: z.ZodOptional<z.ZodBoolean>;
                icon: z.ZodOptional<z.ZodEnum<{
                    [x: string]: string;
                }>>;
                period: z.ZodOptional<z.ZodString>;
                basis: z.ZodOptional<z.ZodEnum<{
                    law: "law";
                    estimate: "estimate";
                    pending: "pending";
                    proposal: "proposal";
                }>>;
            }, z.core.$strict>>;
            axis_labels: z.ZodOptional<z.ZodArray<z.ZodString>>;
            range: z.ZodOptional<z.ZodObject<{
                from: z.ZodNumber;
                to: z.ZodNumber;
            }, z.core.$strict>>;
            milestones: z.ZodOptional<z.ZodArray<z.ZodObject<{
                at: z.ZodNumber;
                label: z.ZodString;
            }, z.core.$strict>>>;
            bands: z.ZodOptional<z.ZodArray<z.ZodObject<{
                from: z.ZodNumber;
                to: z.ZodNumber;
                label: z.ZodString;
            }, z.core.$strict>>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"pest">;
            political: z.ZodObject<{
                title: z.ZodOptional<z.ZodString>;
                items: z.ZodArray<z.ZodString>;
            }, z.core.$strict>;
            economic: z.ZodObject<{
                title: z.ZodOptional<z.ZodString>;
                items: z.ZodArray<z.ZodString>;
            }, z.core.$strict>;
            social: z.ZodObject<{
                title: z.ZodOptional<z.ZodString>;
                items: z.ZodArray<z.ZodString>;
            }, z.core.$strict>;
            technological: z.ZodObject<{
                title: z.ZodOptional<z.ZodString>;
                items: z.ZodArray<z.ZodString>;
            }, z.core.$strict>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"five_forces">;
            rivalry: z.ZodObject<{
                label: z.ZodOptional<z.ZodString>;
                intensity: z.ZodOptional<z.ZodEnum<{
                    low: "low";
                    medium: "medium";
                    high: "high";
                }>>;
                items: z.ZodArray<z.ZodString>;
            }, z.core.$strict>;
            new_entrants: z.ZodObject<{
                label: z.ZodOptional<z.ZodString>;
                intensity: z.ZodOptional<z.ZodEnum<{
                    low: "low";
                    medium: "medium";
                    high: "high";
                }>>;
                items: z.ZodArray<z.ZodString>;
            }, z.core.$strict>;
            supplier_power: z.ZodObject<{
                label: z.ZodOptional<z.ZodString>;
                intensity: z.ZodOptional<z.ZodEnum<{
                    low: "low";
                    medium: "medium";
                    high: "high";
                }>>;
                items: z.ZodArray<z.ZodString>;
            }, z.core.$strict>;
            buyer_power: z.ZodObject<{
                label: z.ZodOptional<z.ZodString>;
                intensity: z.ZodOptional<z.ZodEnum<{
                    low: "low";
                    medium: "medium";
                    high: "high";
                }>>;
                items: z.ZodArray<z.ZodString>;
            }, z.core.$strict>;
            substitutes: z.ZodObject<{
                label: z.ZodOptional<z.ZodString>;
                intensity: z.ZodOptional<z.ZodEnum<{
                    low: "low";
                    medium: "medium";
                    high: "high";
                }>>;
                items: z.ZodArray<z.ZodString>;
            }, z.core.$strict>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"heatmap">;
            x_labels: z.ZodArray<z.ZodString>;
            y_labels: z.ZodArray<z.ZodString>;
            values: z.ZodArray<z.ZodArray<z.ZodNumber>>;
            domain: z.ZodOptional<z.ZodObject<{
                min: z.ZodNumber;
                max: z.ZodNumber;
            }, z.core.$strict>>;
            show_values: z.ZodOptional<z.ZodBoolean>;
            x_title: z.ZodOptional<z.ZodString>;
            y_title: z.ZodOptional<z.ZodString>;
            label_every: z.ZodOptional<z.ZodNumber>;
            steps: z.ZodOptional<z.ZodArray<z.ZodObject<{
                max: z.ZodOptional<z.ZodNumber>;
                label: z.ZodString;
                short: z.ZodOptional<z.ZodString>;
            }, z.core.$strict>>>;
            bands: z.ZodOptional<z.ZodArray<z.ZodObject<{
                from: z.ZodString;
                to: z.ZodString;
                label: z.ZodString;
                icon: z.ZodOptional<z.ZodEnum<{
                    [x: string]: string;
                }>>;
            }, z.core.$strict>>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"sankey">;
            nodes: z.ZodArray<z.ZodObject<{
                id: z.ZodString;
                label: z.ZodString;
            }, z.core.$strict>>;
            links: z.ZodArray<z.ZodObject<{
                from: z.ZodString;
                to: z.ZodString;
                value: z.ZodNumber;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"data_table">;
            title: z.ZodOptional<z.ZodString>;
            columns: z.ZodArray<z.ZodObject<{
                key: z.ZodString;
                label: z.ZodString;
                align: z.ZodOptional<z.ZodEnum<{
                    left: "left";
                    right: "right";
                    center: "center";
                }>>;
                emphasis: z.ZodOptional<z.ZodBoolean>;
                icon: z.ZodOptional<z.ZodEnum<{
                    [x: string]: string;
                }>>;
            }, z.core.$strict>>;
            rows: z.ZodArray<z.ZodObject<{
                cells: z.ZodRecord<z.ZodString, z.ZodUnion<readonly [z.ZodString, z.ZodNumber]>>;
                emphasis: z.ZodOptional<z.ZodEnum<{
                    highlight: "highlight";
                    total: "total";
                }>>;
                icon: z.ZodOptional<z.ZodEnum<{
                    [x: string]: string;
                }>>;
                tag: z.ZodOptional<z.ZodObject<{
                    text: z.ZodString;
                    quiet: z.ZodOptional<z.ZodBoolean>;
                    evidence: z.ZodOptional<z.ZodEnum<{
                        label: "label";
                        draft: "draft";
                        trial: "trial";
                        company: "company";
                        press: "press";
                        official: "official";
                        registry: "registry";
                        preprint: "preprint";
                    }>>;
                    settled: z.ZodOptional<z.ZodBoolean>;
                    tone: z.ZodOptional<z.ZodEnum<{
                        danger: "danger";
                        warning: "warning";
                        success: "success";
                    }>>;
                    basis: z.ZodOptional<z.ZodEnum<{
                        law: "law";
                        estimate: "estimate";
                        pending: "pending";
                        proposal: "proposal";
                    }>>;
                }, z.core.$strict>>;
            }, z.core.$strict>>;
            source: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"device_mockup">;
            device: z.ZodEnum<{
                phone: "phone";
                browser: "browser";
            }>;
            asset_id: z.ZodString;
            caption: z.ZodOptional<z.ZodString>;
            url: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"cycle">;
            title: z.ZodOptional<z.ZodString>;
            items: z.ZodArray<z.ZodObject<{
                label: z.ZodString;
                description: z.ZodOptional<z.ZodString>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"people_cards">;
            title: z.ZodOptional<z.ZodString>;
            people: z.ZodArray<z.ZodObject<{
                name: z.ZodString;
                role: z.ZodOptional<z.ZodString>;
                org: z.ZodOptional<z.ZodString>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"hub_spoke">;
            center: z.ZodString;
            items: z.ZodArray<z.ZodObject<{
                label: z.ZodString;
                description: z.ZodOptional<z.ZodString>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"progress_donuts">;
            items: z.ZodArray<z.ZodObject<{
                value: z.ZodString;
                unit: z.ZodOptional<z.ZodString>;
                label: z.ZodString;
                icon: z.ZodOptional<z.ZodEnum<{
                    [x: string]: string;
                }>>;
                source: z.ZodOptional<z.ZodString>;
                detail: z.ZodOptional<z.ZodString>;
                emphasis: z.ZodOptional<z.ZodBoolean>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"staircase">;
            items: z.ZodArray<z.ZodObject<{
                title: z.ZodString;
                value: z.ZodString;
                unit: z.ZodOptional<z.ZodString>;
                note: z.ZodOptional<z.ZodString>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"chevron_process">;
            items: z.ZodArray<z.ZodObject<{
                title: z.ZodString;
                text: z.ZodOptional<z.ZodString>;
                icon: z.ZodOptional<z.ZodEnum<{
                    [x: string]: string;
                }>>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"swimlane">;
            lanes: z.ZodArray<z.ZodObject<{
                label: z.ZodString;
                role: z.ZodOptional<z.ZodString>;
            }, z.core.$strict>>;
            steps: z.ZodArray<z.ZodObject<{
                lane: z.ZodString;
                title: z.ZodString;
                detail: z.ZodOptional<z.ZodString>;
            }, z.core.$strict>>;
            handoff_note: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"journey_map">;
            stages: z.ZodArray<z.ZodObject<{
                label: z.ZodString;
                touchpoints: z.ZodOptional<z.ZodArray<z.ZodString>>;
                action: z.ZodOptional<z.ZodString>;
                emotion: z.ZodNumber;
                opportunity: z.ZodOptional<z.ZodString>;
            }, z.core.$strict>>;
            row_labels: z.ZodOptional<z.ZodObject<{
                touchpoints: z.ZodOptional<z.ZodString>;
                action: z.ZodOptional<z.ZodString>;
                emotion: z.ZodOptional<z.ZodString>;
                opportunity: z.ZodOptional<z.ZodString>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"decision_tree">;
            question: z.ZodString;
            branches: z.ZodArray<z.ZodObject<{
                edge: z.ZodString;
                title: z.ZodString;
                detail: z.ZodOptional<z.ZodString>;
                outcomes: z.ZodArray<z.ZodObject<{
                    edge: z.ZodString;
                    title: z.ZodString;
                    detail: z.ZodOptional<z.ZodString>;
                    value: z.ZodOptional<z.ZodString>;
                    unit: z.ZodOptional<z.ZodString>;
                    recommended: z.ZodOptional<z.ZodBoolean>;
                }, z.core.$strict>>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"from_to">;
            from: z.ZodObject<{
                kicker: z.ZodOptional<z.ZodString>;
                title: z.ZodString;
            }, z.core.$strict>;
            to: z.ZodObject<{
                kicker: z.ZodOptional<z.ZodString>;
                title: z.ZodString;
            }, z.core.$strict>;
            rows: z.ZodArray<z.ZodObject<{
                label: z.ZodString;
                icon: z.ZodOptional<z.ZodEnum<{
                    [x: string]: string;
                }>>;
                note: z.ZodOptional<z.ZodString>;
                from: z.ZodString;
                to: z.ZodString;
                unit: z.ZodOptional<z.ZodString>;
                change: z.ZodOptional<z.ZodString>;
                tag: z.ZodOptional<z.ZodObject<{
                    text: z.ZodString;
                    quiet: z.ZodOptional<z.ZodBoolean>;
                    evidence: z.ZodOptional<z.ZodEnum<{
                        label: "label";
                        draft: "draft";
                        trial: "trial";
                        company: "company";
                        press: "press";
                        official: "official";
                        registry: "registry";
                        preprint: "preprint";
                    }>>;
                    settled: z.ZodOptional<z.ZodBoolean>;
                    tone: z.ZodOptional<z.ZodEnum<{
                        danger: "danger";
                        warning: "warning";
                        success: "success";
                    }>>;
                    basis: z.ZodOptional<z.ZodEnum<{
                        law: "law";
                        estimate: "estimate";
                        pending: "pending";
                        proposal: "proposal";
                    }>>;
                }, z.core.$strict>>;
                emphasis: z.ZodOptional<z.ZodBoolean>;
            }, z.core.$strict>>;
            label_column: z.ZodOptional<z.ZodString>;
            span: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"org_tree">;
            root: z.ZodObject<{
                name: z.ZodString;
                role: z.ZodOptional<z.ZodString>;
            }, z.core.$strict>;
            children: z.ZodArray<z.ZodObject<{
                name: z.ZodString;
                role: z.ZodOptional<z.ZodString>;
                children: z.ZodOptional<z.ZodArray<z.ZodObject<{
                    name: z.ZodString;
                    role: z.ZodOptional<z.ZodString>;
                }, z.core.$strict>>>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"issue_tree">;
            question: z.ZodString;
            children_column: z.ZodOptional<z.ZodString>;
            branches: z.ZodArray<z.ZodObject<{
                label: z.ZodString;
                note: z.ZodOptional<z.ZodString>;
                icon: z.ZodOptional<z.ZodEnum<{
                    [x: string]: string;
                }>>;
                emphasis: z.ZodOptional<z.ZodLiteral<true>>;
                children: z.ZodOptional<z.ZodArray<z.ZodObject<{
                    label: z.ZodString;
                }, z.core.$strict>>>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"pyramid">;
            layers: z.ZodArray<z.ZodObject<{
                label: z.ZodString;
                note: z.ZodOptional<z.ZodString>;
                tone: z.ZodOptional<z.ZodEnum<{
                    danger: "danger";
                    warning: "warning";
                    success: "success";
                }>>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"iceberg">;
            above: z.ZodArray<z.ZodString>;
            below: z.ZodArray<z.ZodString>;
            waterline: z.ZodOptional<z.ZodString>;
            above_label: z.ZodOptional<z.ZodString>;
            below_label: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"pillar_model">;
            goal: z.ZodString;
            pillars: z.ZodArray<z.ZodObject<{
                title: z.ZodString;
                value: z.ZodString;
                unit: z.ZodOptional<z.ZodString>;
            }, z.core.$strict>>;
            base: z.ZodString;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"value_chain">;
            primary: z.ZodArray<z.ZodObject<{
                label: z.ZodString;
                value: z.ZodOptional<z.ZodString>;
                unit: z.ZodOptional<z.ZodString>;
                emphasis: z.ZodOptional<z.ZodLiteral<true>>;
            }, z.core.$strict>>;
            support: z.ZodArray<z.ZodObject<{
                label: z.ZodString;
                note: z.ZodOptional<z.ZodString>;
            }, z.core.$strict>>;
            margin: z.ZodOptional<z.ZodObject<{
                label: z.ZodString;
                value: z.ZodOptional<z.ZodString>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"harvey_balls">;
            criteria: z.ZodArray<z.ZodString>;
            options: z.ZodArray<z.ZodObject<{
                label: z.ZodString;
                scores: z.ZodArray<z.ZodUnion<readonly [z.ZodLiteral<0>, z.ZodLiteral<25>, z.ZodLiteral<50>, z.ZodLiteral<75>, z.ZodLiteral<100>]>>;
                total: z.ZodOptional<z.ZodUnion<readonly [z.ZodString, z.ZodNumber]>>;
                highlight: z.ZodOptional<z.ZodBoolean>;
            }, z.core.$strict>>;
            legend: z.ZodOptional<z.ZodBoolean>;
            labels: z.ZodOptional<z.ZodObject<{
                option: z.ZodOptional<z.ZodString>;
                total: z.ZodOptional<z.ZodString>;
                none: z.ZodOptional<z.ZodString>;
                partial: z.ZodOptional<z.ZodString>;
                full: z.ZodOptional<z.ZodString>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"scorecard">;
            labels: z.ZodOptional<z.ZodObject<{
                metric: z.ZodOptional<z.ZodString>;
                target: z.ZodOptional<z.ZodString>;
                actual: z.ZodOptional<z.ZodString>;
                gap: z.ZodOptional<z.ZodString>;
                status: z.ZodOptional<z.ZodString>;
            }, z.core.$strict>>;
            rows: z.ZodArray<z.ZodObject<{
                label: z.ZodString;
                target: z.ZodString;
                actual: z.ZodString;
                gap: z.ZodString;
                status: z.ZodEnum<{
                    watch: "watch";
                    on_track: "on_track";
                    off_track: "off_track";
                }>;
                status_label: z.ZodOptional<z.ZodString>;
            }, z.core.$strict>>;
            note: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"pictogram">;
            rows: z.ZodArray<z.ZodObject<{
                filled: z.ZodNumber;
                label: z.ZodString;
                caption: z.ZodOptional<z.ZodString>;
                highlight: z.ZodOptional<z.ZodBoolean>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"word_cloud">;
            words: z.ZodArray<z.ZodObject<{
                text: z.ZodString;
                weight: z.ZodUnion<readonly [z.ZodLiteral<1>, z.ZodLiteral<2>, z.ZodLiteral<3>, z.ZodLiteral<4>]>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"venn">;
            sets: z.ZodArray<z.ZodObject<{
                label: z.ZodString;
            }, z.core.$strict>>;
            center: z.ZodString;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"fishbone">;
            effect: z.ZodString;
            ribs: z.ZodArray<z.ZodObject<{
                label: z.ZodString;
                causes: z.ZodArray<z.ZodString>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"positioning_map">;
            x_axis: z.ZodObject<{
                title: z.ZodString;
                low: z.ZodString;
                high: z.ZodString;
            }, z.core.$strict>;
            y_axis: z.ZodObject<{
                title: z.ZodString;
                low: z.ZodString;
                high: z.ZodString;
            }, z.core.$strict>;
            quadrants: z.ZodOptional<z.ZodObject<{
                top_left: z.ZodString;
                top_right: z.ZodString;
                bottom_left: z.ZodString;
                bottom_right: z.ZodString;
            }, z.core.$strict>>;
            points: z.ZodArray<z.ZodObject<{
                label: z.ZodString;
                x: z.ZodNumber;
                y: z.ZodNumber;
                emphasis: z.ZodOptional<z.ZodLiteral<true>>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"concept_equation">;
            operands: z.ZodArray<z.ZodObject<{
                label: z.ZodString;
                value: z.ZodOptional<z.ZodString>;
                note: z.ZodOptional<z.ZodString>;
                icon: z.ZodOptional<z.ZodEnum<{
                    [x: string]: string;
                }>>;
            }, z.core.$strict>>;
            result: z.ZodObject<{
                label: z.ZodString;
                value: z.ZodOptional<z.ZodString>;
                note: z.ZodOptional<z.ZodString>;
                icon: z.ZodOptional<z.ZodEnum<{
                    [x: string]: string;
                }>>;
            }, z.core.$strict>;
            excluded: z.ZodOptional<z.ZodObject<{
                label: z.ZodString;
                value: z.ZodOptional<z.ZodString>;
                note: z.ZodOptional<z.ZodString>;
                icon: z.ZodOptional<z.ZodEnum<{
                    [x: string]: string;
                }>>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"segmented_wheel">;
            center: z.ZodString;
            segments: z.ZodArray<z.ZodObject<{
                label: z.ZodString;
                value: z.ZodOptional<z.ZodString>;
                emphasis: z.ZodOptional<z.ZodLiteral<true>>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"pros_cons">;
            pros: z.ZodObject<{
                title: z.ZodString;
                items: z.ZodArray<z.ZodObject<{
                    label: z.ZodString;
                    note: z.ZodOptional<z.ZodString>;
                }, z.core.$strict>>;
            }, z.core.$strict>;
            cons: z.ZodObject<{
                title: z.ZodString;
                items: z.ZodArray<z.ZodObject<{
                    label: z.ZodString;
                    note: z.ZodOptional<z.ZodString>;
                }, z.core.$strict>>;
            }, z.core.$strict>;
            verdict: z.ZodString;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"sketch">;
            kind: z.ZodEnum<{
                discontinuity: "discontinuity";
                difference_in_differences: "difference_in_differences";
            }>;
            at: z.ZodString;
            x_title: z.ZodString;
            y_title: z.ZodOptional<z.ZodString>;
            effect: z.ZodOptional<z.ZodString>;
            groups: z.ZodOptional<z.ZodArray<z.ZodString>>;
            direction: z.ZodOptional<z.ZodEnum<{
                up: "up";
                down: "down";
            }>>;
        }, z.core.$strict>], "type">>>;
        background: z.ZodOptional<z.ZodDiscriminatedUnion<[z.ZodObject<{
            kind: z.ZodLiteral<"color">;
            value: z.ZodString;
        }, z.core.$strict>, z.ZodObject<{
            kind: z.ZodLiteral<"gradient">;
            from: z.ZodString;
            to: z.ZodString;
            direction: z.ZodOptional<z.ZodEnum<{
                tb: "tb";
                lr: "lr";
                diagonal: "diagonal";
            }>>;
        }, z.core.$strict>, z.ZodObject<{
            kind: z.ZodLiteral<"asset">;
            asset_id: z.ZodString;
            overlay: z.ZodOptional<z.ZodObject<{
                color: z.ZodString;
                opacity: z.ZodNumber;
            }, z.core.$strict>>;
            fit: z.ZodOptional<z.ZodEnum<{
                cover: "cover";
                contain: "contain";
            }>>;
        }, z.core.$strict>], "kind">>;
        decor: z.ZodOptional<z.ZodObject<{
            kind: z.ZodEnum<{
                big_number: "big_number";
                corner_tag: "corner_tag";
                rule_line: "rule_line";
                quote_marks: "quote_marks";
                geo_dots: "geo_dots";
            }>;
            intensity: z.ZodOptional<z.ZodEnum<{
                subtle: "subtle";
                normal: "normal";
            }>>;
            text: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>>;
        image_side: z.ZodOptional<z.ZodEnum<{
            left: "left";
            right: "right";
        }>>;
        footnote: z.ZodOptional<z.ZodString>;
        notes: z.ZodOptional<z.ZodString>;
        type: z.ZodLiteral<"content">;
        kind: z.ZodEnum<{
            points: "points";
            list: "list";
            comparison: "comparison";
            process: "process";
            data: "data";
            photo: "photo";
            statement: "statement";
            quote: "quote";
            fact: "fact";
            evidence: "evidence";
            hierarchy: "hierarchy";
        }>;
    }, z.core.$strict>, z.ZodObject<{
        id: z.ZodOptional<z.ZodString>;
        placeholder: z.ZodOptional<z.ZodLiteral<true>>;
        heading: z.ZodOptional<z.ZodString>;
        subheading: z.ZodOptional<z.ZodString>;
        kicker: z.ZodOptional<z.ZodString>;
        fields: z.ZodOptional<z.ZodArray<z.ZodObject<{
            label: z.ZodString;
            value: z.ZodString;
            note: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>>>;
        stamp: z.ZodOptional<z.ZodObject<{
            text: z.ZodString;
            date: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>>;
        ballot: z.ZodOptional<z.ZodObject<{
            choices: z.ZodArray<z.ZodString>;
            signature: z.ZodOptional<z.ZodString>;
            item_choices: z.ZodOptional<z.ZodArray<z.ZodObject<{
                item: z.ZodNumber;
                choices: z.ZodArray<z.ZodString>;
            }, z.core.$strict>>>;
        }, z.core.$strict>>;
        tag: z.ZodOptional<z.ZodObject<{
            text: z.ZodString;
            quiet: z.ZodOptional<z.ZodBoolean>;
            evidence: z.ZodOptional<z.ZodEnum<{
                label: "label";
                draft: "draft";
                trial: "trial";
                company: "company";
                press: "press";
                official: "official";
                registry: "registry";
                preprint: "preprint";
            }>>;
            settled: z.ZodOptional<z.ZodBoolean>;
            tone: z.ZodOptional<z.ZodEnum<{
                danger: "danger";
                warning: "warning";
                success: "success";
            }>>;
            basis: z.ZodOptional<z.ZodEnum<{
                law: "law";
                estimate: "estimate";
                pending: "pending";
                proposal: "proposal";
            }>>;
        }, z.core.$strict>>;
        years: z.ZodOptional<z.ZodObject<{
            from: z.ZodNumber;
            to: z.ZodNumber;
            marked: z.ZodArray<z.ZodNumber>;
        }, z.core.$strict>>;
        stage: z.ZodOptional<z.ZodString>;
        components: z.ZodDefault<z.ZodArray<z.ZodDiscriminatedUnion<[z.ZodObject<{
            type: z.ZodLiteral<"bullets">;
            items: z.ZodArray<z.ZodString>;
            style: z.ZodOptional<z.ZodEnum<{
                default: "default";
                checklist: "checklist";
                numbered: "numbered";
                plain: "plain";
                divided: "divided";
            }>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"paragraph">;
            text: z.ZodString;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"blockquote">;
            text: z.ZodString;
            attribution: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"callout">;
            variant: z.ZodEnum<{
                info: "info";
                warn: "warn";
                tip: "tip";
            }>;
            title: z.ZodOptional<z.ZodString>;
            text: z.ZodString;
            icon: z.ZodOptional<z.ZodEnum<{
                [x: string]: string;
            }>>;
            tag: z.ZodOptional<z.ZodObject<{
                text: z.ZodString;
                quiet: z.ZodOptional<z.ZodBoolean>;
                evidence: z.ZodOptional<z.ZodEnum<{
                    label: "label";
                    draft: "draft";
                    trial: "trial";
                    company: "company";
                    press: "press";
                    official: "official";
                    registry: "registry";
                    preprint: "preprint";
                }>>;
                settled: z.ZodOptional<z.ZodBoolean>;
                tone: z.ZodOptional<z.ZodEnum<{
                    danger: "danger";
                    warning: "warning";
                    success: "success";
                }>>;
                basis: z.ZodOptional<z.ZodEnum<{
                    law: "law";
                    estimate: "estimate";
                    pending: "pending";
                    proposal: "proposal";
                }>>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"code">;
            language: z.ZodString;
            code: z.ZodString;
            title: z.ZodOptional<z.ZodString>;
            highlight_lines: z.ZodOptional<z.ZodArray<z.ZodNumber>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"kpi_cards">;
            items: z.ZodArray<z.ZodObject<{
                value: z.ZodString;
                unit: z.ZodOptional<z.ZodString>;
                label: z.ZodString;
                note: z.ZodOptional<z.ZodString>;
                tag: z.ZodOptional<z.ZodObject<{
                    text: z.ZodString;
                    quiet: z.ZodOptional<z.ZodBoolean>;
                    evidence: z.ZodOptional<z.ZodEnum<{
                        label: "label";
                        draft: "draft";
                        trial: "trial";
                        company: "company";
                        press: "press";
                        official: "official";
                        registry: "registry";
                        preprint: "preprint";
                    }>>;
                    settled: z.ZodOptional<z.ZodBoolean>;
                    tone: z.ZodOptional<z.ZodEnum<{
                        danger: "danger";
                        warning: "warning";
                        success: "success";
                    }>>;
                    basis: z.ZodOptional<z.ZodEnum<{
                        law: "law";
                        estimate: "estimate";
                        pending: "pending";
                        proposal: "proposal";
                    }>>;
                }, z.core.$strict>>;
                delta: z.ZodOptional<z.ZodEnum<{
                    flat: "flat";
                    up: "up";
                    down: "down";
                }>>;
                delta_good: z.ZodOptional<z.ZodBoolean>;
                icon: z.ZodOptional<z.ZodEnum<{
                    [x: string]: string;
                }>>;
                tone: z.ZodOptional<z.ZodEnum<{
                    danger: "danger";
                    warning: "warning";
                    success: "success";
                }>>;
                source: z.ZodOptional<z.ZodString>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"chart">;
            title: z.ZodOptional<z.ZodString>;
            chart_type: z.ZodEnum<{
                line: "line";
                donut: "donut";
                dumbbell: "dumbbell";
                funnel: "funnel";
                gauge: "gauge";
                bar: "bar";
                stacked: "stacked";
                percent_stacked: "percent_stacked";
                pie: "pie";
                area: "area";
                combo: "combo";
                scatter: "scatter";
            }>;
            direction: z.ZodOptional<z.ZodEnum<{
                horizontal: "horizontal";
                vertical: "vertical";
            }>>;
            style: z.ZodOptional<z.ZodEnum<{
                donut: "donut";
            }>>;
            center_total: z.ZodOptional<z.ZodBoolean>;
            gauge: z.ZodOptional<z.ZodObject<{
                min: z.ZodOptional<z.ZodNumber>;
                max: z.ZodOptional<z.ZodNumber>;
            }, z.core.$strict>>;
            axes: z.ZodOptional<z.ZodObject<{
                x_title: z.ZodOptional<z.ZodString>;
                y_title: z.ZodOptional<z.ZodString>;
                x_unit: z.ZodOptional<z.ZodString>;
                y_unit: z.ZodOptional<z.ZodString>;
                y2_title: z.ZodOptional<z.ZodString>;
                y2_unit: z.ZodOptional<z.ZodString>;
                show_grid: z.ZodOptional<z.ZodBoolean>;
            }, z.core.$strict>>;
            tag: z.ZodOptional<z.ZodObject<{
                text: z.ZodString;
                quiet: z.ZodOptional<z.ZodBoolean>;
                evidence: z.ZodOptional<z.ZodEnum<{
                    label: "label";
                    draft: "draft";
                    trial: "trial";
                    company: "company";
                    press: "press";
                    official: "official";
                    registry: "registry";
                    preprint: "preprint";
                }>>;
                settled: z.ZodOptional<z.ZodBoolean>;
                tone: z.ZodOptional<z.ZodEnum<{
                    danger: "danger";
                    warning: "warning";
                    success: "success";
                }>>;
                basis: z.ZodOptional<z.ZodEnum<{
                    law: "law";
                    estimate: "estimate";
                    pending: "pending";
                    proposal: "proposal";
                }>>;
            }, z.core.$strict>>;
            changes: z.ZodOptional<z.ZodArray<z.ZodObject<{
                from: z.ZodString;
                to: z.ZodString;
                at: z.ZodOptional<z.ZodString>;
            }, z.core.$strict>>>;
            bands: z.ZodOptional<z.ZodArray<z.ZodObject<{
                from: z.ZodNumber;
                to: z.ZodNumber;
                label: z.ZodOptional<z.ZodString>;
            }, z.core.$strict>>>;
            emphasis_label: z.ZodOptional<z.ZodString>;
            reference: z.ZodOptional<z.ZodObject<{
                value: z.ZodNumber;
                label: z.ZodString;
            }, z.core.$strict>>;
            markers: z.ZodOptional<z.ZodArray<z.ZodObject<{
                before: z.ZodString;
                label: z.ZodString;
            }, z.core.$strict>>>;
            gaps: z.ZodOptional<z.ZodArray<z.ZodObject<{
                after: z.ZodString;
                x: z.ZodString;
                label: z.ZodString;
            }, z.core.$strict>>>;
            series: z.ZodArray<z.ZodObject<{
                name: z.ZodString;
                data: z.ZodArray<z.ZodObject<{
                    x: z.ZodUnion<readonly [z.ZodString, z.ZodNumber]>;
                    y: z.ZodNumber;
                    size: z.ZodOptional<z.ZodNumber>;
                    status: z.ZodOptional<z.ZodEnum<{
                        target: "target";
                        estimate: "estimate";
                        forecast: "forecast";
                    }>>;
                    emphasis: z.ZodOptional<z.ZodBoolean>;
                    note: z.ZodOptional<z.ZodString>;
                    icon: z.ZodOptional<z.ZodEnum<{
                        [x: string]: string;
                    }>>;
                    upper: z.ZodOptional<z.ZodNumber>;
                }, z.core.$strict>>;
                plot: z.ZodOptional<z.ZodEnum<{
                    line: "line";
                    bar: "bar";
                }>>;
                axis: z.ZodOptional<z.ZodEnum<{
                    left: "left";
                    right: "right";
                }>>;
                emphasis: z.ZodOptional<z.ZodBoolean>;
                steps: z.ZodOptional<z.ZodBoolean>;
                tone: z.ZodOptional<z.ZodEnum<{
                    danger: "danger";
                    warning: "warning";
                    success: "success";
                }>>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"flowchart">;
            nodes: z.ZodArray<z.ZodObject<{
                id: z.ZodString;
                label: z.ZodString;
                kind: z.ZodOptional<z.ZodEnum<{
                    rect: "rect";
                    diamond: "diamond";
                    round: "round";
                }>>;
            }, z.core.$strict>>;
            edges: z.ZodArray<z.ZodObject<{
                from: z.ZodString;
                to: z.ZodString;
                label: z.ZodOptional<z.ZodString>;
            }, z.core.$strict>>;
            direction: z.ZodOptional<z.ZodEnum<{
                TB: "TB";
                TD: "TD";
                BT: "BT";
                LR: "LR";
                RL: "RL";
            }>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"architecture">;
            layers: z.ZodArray<z.ZodObject<{
                title: z.ZodString;
                items: z.ZodArray<z.ZodString>;
            }, z.core.$strict>>;
            direction: z.ZodOptional<z.ZodEnum<{
                top_down: "top_down";
                bottom_up: "bottom_up";
            }>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"timeline">;
            title: z.ZodOptional<z.ZodString>;
            layout: z.ZodOptional<z.ZodEnum<{
                horizontal: "horizontal";
                vertical: "vertical";
            }>>;
            lanes: z.ZodOptional<z.ZodArray<z.ZodString>>;
            periods: z.ZodOptional<z.ZodArray<z.ZodObject<{
                from: z.ZodString;
                to: z.ZodString;
                label: z.ZodString;
                basis: z.ZodOptional<z.ZodEnum<{
                    law: "law";
                    estimate: "estimate";
                    pending: "pending";
                    proposal: "proposal";
                }>>;
            }, z.core.$strict>>>;
            milestones: z.ZodArray<z.ZodObject<{
                date: z.ZodString;
                title: z.ZodString;
                desc: z.ZodOptional<z.ZodString>;
                highlight: z.ZodOptional<z.ZodBoolean>;
                icon: z.ZodOptional<z.ZodEnum<{
                    [x: string]: string;
                }>>;
                tone: z.ZodOptional<z.ZodEnum<{
                    danger: "danger";
                    warning: "warning";
                    success: "success";
                }>>;
                status: z.ZodOptional<z.ZodEnum<{
                    pending: "pending";
                }>>;
                tag: z.ZodOptional<z.ZodObject<{
                    text: z.ZodString;
                    quiet: z.ZodOptional<z.ZodBoolean>;
                    evidence: z.ZodOptional<z.ZodEnum<{
                        label: "label";
                        draft: "draft";
                        trial: "trial";
                        company: "company";
                        press: "press";
                        official: "official";
                        registry: "registry";
                        preprint: "preprint";
                    }>>;
                    settled: z.ZodOptional<z.ZodBoolean>;
                    tone: z.ZodOptional<z.ZodEnum<{
                        danger: "danger";
                        warning: "warning";
                        success: "success";
                    }>>;
                    basis: z.ZodOptional<z.ZodEnum<{
                        law: "law";
                        estimate: "estimate";
                        pending: "pending";
                        proposal: "proposal";
                    }>>;
                }, z.core.$strict>>;
                source: z.ZodOptional<z.ZodString>;
                lane: z.ZodOptional<z.ZodString>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"comparison">;
            title: z.ZodOptional<z.ZodString>;
            columns: z.ZodArray<z.ZodString>;
            label_column: z.ZodOptional<z.ZodString>;
            rows: z.ZodArray<z.ZodObject<{
                label: z.ZodString;
                cells: z.ZodArray<z.ZodString>;
                icon: z.ZodOptional<z.ZodEnum<{
                    [x: string]: string;
                }>>;
                tag: z.ZodOptional<z.ZodObject<{
                    text: z.ZodString;
                    quiet: z.ZodOptional<z.ZodBoolean>;
                    evidence: z.ZodOptional<z.ZodEnum<{
                        label: "label";
                        draft: "draft";
                        trial: "trial";
                        company: "company";
                        press: "press";
                        official: "official";
                        registry: "registry";
                        preprint: "preprint";
                    }>>;
                    settled: z.ZodOptional<z.ZodBoolean>;
                    tone: z.ZodOptional<z.ZodEnum<{
                        danger: "danger";
                        warning: "warning";
                        success: "success";
                    }>>;
                    basis: z.ZodOptional<z.ZodEnum<{
                        law: "law";
                        estimate: "estimate";
                        pending: "pending";
                        proposal: "proposal";
                    }>>;
                }, z.core.$strict>>;
                emphasis: z.ZodOptional<z.ZodBoolean>;
            }, z.core.$strict>>;
            tag_column: z.ZodOptional<z.ZodString>;
            recommended: z.ZodOptional<z.ZodNumber>;
            recommended_label: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"icon_cards">;
            title: z.ZodOptional<z.ZodString>;
            items: z.ZodArray<z.ZodObject<{
                icon: z.ZodEnum<{
                    [x: string]: string;
                }>;
                title: z.ZodString;
                text: z.ZodString;
                tag: z.ZodOptional<z.ZodObject<{
                    text: z.ZodString;
                    quiet: z.ZodOptional<z.ZodBoolean>;
                    evidence: z.ZodOptional<z.ZodEnum<{
                        label: "label";
                        draft: "draft";
                        trial: "trial";
                        company: "company";
                        press: "press";
                        official: "official";
                        registry: "registry";
                        preprint: "preprint";
                    }>>;
                    settled: z.ZodOptional<z.ZodBoolean>;
                    tone: z.ZodOptional<z.ZodEnum<{
                        danger: "danger";
                        warning: "warning";
                        success: "success";
                    }>>;
                    basis: z.ZodOptional<z.ZodEnum<{
                        law: "law";
                        estimate: "estimate";
                        pending: "pending";
                        proposal: "proposal";
                    }>>;
                }, z.core.$strict>>;
                tone: z.ZodOptional<z.ZodEnum<{
                    danger: "danger";
                    warning: "warning";
                    success: "success";
                }>>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"row_cards">;
            items: z.ZodArray<z.ZodObject<{
                icon: z.ZodOptional<z.ZodEnum<{
                    [x: string]: string;
                }>>;
                title: z.ZodString;
                text: z.ZodOptional<z.ZodString>;
                sub: z.ZodOptional<z.ZodString>;
                highlight: z.ZodOptional<z.ZodBoolean>;
                tone: z.ZodOptional<z.ZodEnum<{
                    danger: "danger";
                    warning: "warning";
                    success: "success";
                }>>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"steps">;
            items: z.ZodArray<z.ZodObject<{
                title: z.ZodString;
                text: z.ZodString;
                icon: z.ZodOptional<z.ZodEnum<{
                    [x: string]: string;
                }>>;
                tone: z.ZodOptional<z.ZodEnum<{
                    danger: "danger";
                    warning: "warning";
                    success: "success";
                }>>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"rings">;
            items: z.ZodArray<z.ZodObject<{
                label: z.ZodString;
                desc: z.ZodOptional<z.ZodString>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"numbered_cards">;
            items: z.ZodArray<z.ZodObject<{
                title: z.ZodString;
                text: z.ZodOptional<z.ZodString>;
                sub: z.ZodOptional<z.ZodString>;
                icon: z.ZodOptional<z.ZodEnum<{
                    [x: string]: string;
                }>>;
                emphasis: z.ZodOptional<z.ZodBoolean>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"roadmap">;
            items: z.ZodArray<z.ZodObject<{
                title: z.ZodString;
                period: z.ZodOptional<z.ZodString>;
                icon: z.ZodOptional<z.ZodEnum<{
                    [x: string]: string;
                }>>;
                rows: z.ZodOptional<z.ZodArray<z.ZodObject<{
                    label: z.ZodString;
                    value: z.ZodString;
                    basis: z.ZodOptional<z.ZodEnum<{
                        law: "law";
                        estimate: "estimate";
                        pending: "pending";
                        proposal: "proposal";
                    }>>;
                }, z.core.$strict>>>;
                duration: z.ZodOptional<z.ZodNumber>;
                checkpoint: z.ZodOptional<z.ZodString>;
                points: z.ZodOptional<z.ZodArray<z.ZodString>>;
                emphasis: z.ZodOptional<z.ZodBoolean>;
            }, z.core.$strict>>;
            duration_unit: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"matrix">;
            title: z.ZodOptional<z.ZodString>;
            x_title: z.ZodOptional<z.ZodString>;
            y_title: z.ZodOptional<z.ZodString>;
            cols: z.ZodNumber;
            columns: z.ZodOptional<z.ZodArray<z.ZodString>>;
            rows: z.ZodOptional<z.ZodArray<z.ZodObject<{
                label: z.ZodString;
                icon: z.ZodOptional<z.ZodEnum<{
                    [x: string]: string;
                }>>;
            }, z.core.$strict>>>;
            items: z.ZodArray<z.ZodObject<{
                title: z.ZodString;
                tag: z.ZodOptional<z.ZodString>;
                tone: z.ZodOptional<z.ZodEnum<{
                    info: "info";
                    neutral: "neutral";
                    accent: "accent";
                }>>;
                empty: z.ZodOptional<z.ZodBoolean>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"insight_panel">;
            title: z.ZodString;
            icon: z.ZodOptional<z.ZodEnum<{
                [x: string]: string;
            }>>;
            rows: z.ZodArray<z.ZodObject<{
                label: z.ZodString;
                text: z.ZodString;
            }, z.core.$strict>>;
            footnote: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"verdict_banner">;
            text: z.ZodString;
            tone: z.ZodEnum<{
                warning: "warning";
                positive: "positive";
                neutral: "neutral";
            }>;
            icon: z.ZodOptional<z.ZodEnum<{
                [x: string]: string;
            }>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"image">;
            asset_id: z.ZodString;
            caption: z.ZodOptional<z.ZodString>;
            fit: z.ZodDefault<z.ZodEnum<{
                cover: "cover";
                contain: "contain";
            }>>;
            crop: z.ZodOptional<z.ZodArray<z.ZodNumber>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"image_grid">;
            items: z.ZodArray<z.ZodObject<{
                asset_id: z.ZodString;
                caption: z.ZodOptional<z.ZodString>;
                icon: z.ZodOptional<z.ZodEnum<{
                    [x: string]: string;
                }>>;
                tag: z.ZodOptional<z.ZodObject<{
                    text: z.ZodString;
                    quiet: z.ZodOptional<z.ZodBoolean>;
                    evidence: z.ZodOptional<z.ZodEnum<{
                        label: "label";
                        draft: "draft";
                        trial: "trial";
                        company: "company";
                        press: "press";
                        official: "official";
                        registry: "registry";
                        preprint: "preprint";
                    }>>;
                    settled: z.ZodOptional<z.ZodBoolean>;
                    tone: z.ZodOptional<z.ZodEnum<{
                        danger: "danger";
                        warning: "warning";
                        success: "success";
                    }>>;
                    basis: z.ZodOptional<z.ZodEnum<{
                        law: "law";
                        estimate: "estimate";
                        pending: "pending";
                        proposal: "proposal";
                    }>>;
                }, z.core.$strict>>;
                crop: z.ZodOptional<z.ZodArray<z.ZodNumber>>;
            }, z.core.$strict>>;
            emphasis: z.ZodOptional<z.ZodEnum<{
                none: "none";
                first: "first";
            }>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"image_compare">;
            left: z.ZodObject<{
                asset_id: z.ZodString;
                label: z.ZodString;
            }, z.core.$strict>;
            right: z.ZodObject<{
                asset_id: z.ZodString;
                label: z.ZodString;
            }, z.core.$strict>;
            style: z.ZodOptional<z.ZodEnum<{
                vs: "vs";
                before_after: "before_after";
            }>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"logo_wall">;
            title: z.ZodOptional<z.ZodString>;
            items: z.ZodArray<z.ZodObject<{
                name: z.ZodString;
                asset_id: z.ZodOptional<z.ZodString>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"product_cards">;
            items: z.ZodArray<z.ZodObject<{
                asset_id: z.ZodString;
                name: z.ZodString;
                note: z.ZodOptional<z.ZodString>;
                price: z.ZodOptional<z.ZodString>;
                price_unit: z.ZodOptional<z.ZodString>;
                featured: z.ZodOptional<z.ZodLiteral<true>>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"quote_wall">;
            quotes: z.ZodArray<z.ZodObject<{
                text: z.ZodString;
                name: z.ZodString;
                role: z.ZodOptional<z.ZodString>;
                featured: z.ZodOptional<z.ZodLiteral<true>>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"swot">;
            strengths: z.ZodArray<z.ZodString>;
            weaknesses: z.ZodArray<z.ZodString>;
            opportunities: z.ZodArray<z.ZodString>;
            threats: z.ZodArray<z.ZodString>;
            labels: z.ZodOptional<z.ZodObject<{
                strengths: z.ZodOptional<z.ZodString>;
                weaknesses: z.ZodOptional<z.ZodString>;
                opportunities: z.ZodOptional<z.ZodString>;
                threats: z.ZodOptional<z.ZodString>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"bmc">;
            key_partners: z.ZodArray<z.ZodString>;
            key_activities: z.ZodArray<z.ZodString>;
            key_resources: z.ZodArray<z.ZodString>;
            value_propositions: z.ZodArray<z.ZodString>;
            customer_relationships: z.ZodArray<z.ZodString>;
            channels: z.ZodArray<z.ZodString>;
            customer_segments: z.ZodArray<z.ZodString>;
            cost_structure: z.ZodArray<z.ZodString>;
            revenue_streams: z.ZodArray<z.ZodString>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"waterfall">;
            title: z.ZodOptional<z.ZodString>;
            items: z.ZodArray<z.ZodObject<{
                label: z.ZodString;
                value: z.ZodNumber;
                kind: z.ZodOptional<z.ZodEnum<{
                    delta: "delta";
                    total: "total";
                }>>;
                note: z.ZodOptional<z.ZodString>;
                emphasis: z.ZodOptional<z.ZodBoolean>;
            }, z.core.$strict>>;
            unit: z.ZodOptional<z.ZodString>;
            emphasis_label: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"gantt">;
            items: z.ZodArray<z.ZodObject<{
                label: z.ZodString;
                start: z.ZodNumber;
                end: z.ZodNumber;
                text: z.ZodOptional<z.ZodString>;
                emphasis: z.ZodOptional<z.ZodBoolean>;
                icon: z.ZodOptional<z.ZodEnum<{
                    [x: string]: string;
                }>>;
                period: z.ZodOptional<z.ZodString>;
                basis: z.ZodOptional<z.ZodEnum<{
                    law: "law";
                    estimate: "estimate";
                    pending: "pending";
                    proposal: "proposal";
                }>>;
            }, z.core.$strict>>;
            axis_labels: z.ZodOptional<z.ZodArray<z.ZodString>>;
            range: z.ZodOptional<z.ZodObject<{
                from: z.ZodNumber;
                to: z.ZodNumber;
            }, z.core.$strict>>;
            milestones: z.ZodOptional<z.ZodArray<z.ZodObject<{
                at: z.ZodNumber;
                label: z.ZodString;
            }, z.core.$strict>>>;
            bands: z.ZodOptional<z.ZodArray<z.ZodObject<{
                from: z.ZodNumber;
                to: z.ZodNumber;
                label: z.ZodString;
            }, z.core.$strict>>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"pest">;
            political: z.ZodObject<{
                title: z.ZodOptional<z.ZodString>;
                items: z.ZodArray<z.ZodString>;
            }, z.core.$strict>;
            economic: z.ZodObject<{
                title: z.ZodOptional<z.ZodString>;
                items: z.ZodArray<z.ZodString>;
            }, z.core.$strict>;
            social: z.ZodObject<{
                title: z.ZodOptional<z.ZodString>;
                items: z.ZodArray<z.ZodString>;
            }, z.core.$strict>;
            technological: z.ZodObject<{
                title: z.ZodOptional<z.ZodString>;
                items: z.ZodArray<z.ZodString>;
            }, z.core.$strict>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"five_forces">;
            rivalry: z.ZodObject<{
                label: z.ZodOptional<z.ZodString>;
                intensity: z.ZodOptional<z.ZodEnum<{
                    low: "low";
                    medium: "medium";
                    high: "high";
                }>>;
                items: z.ZodArray<z.ZodString>;
            }, z.core.$strict>;
            new_entrants: z.ZodObject<{
                label: z.ZodOptional<z.ZodString>;
                intensity: z.ZodOptional<z.ZodEnum<{
                    low: "low";
                    medium: "medium";
                    high: "high";
                }>>;
                items: z.ZodArray<z.ZodString>;
            }, z.core.$strict>;
            supplier_power: z.ZodObject<{
                label: z.ZodOptional<z.ZodString>;
                intensity: z.ZodOptional<z.ZodEnum<{
                    low: "low";
                    medium: "medium";
                    high: "high";
                }>>;
                items: z.ZodArray<z.ZodString>;
            }, z.core.$strict>;
            buyer_power: z.ZodObject<{
                label: z.ZodOptional<z.ZodString>;
                intensity: z.ZodOptional<z.ZodEnum<{
                    low: "low";
                    medium: "medium";
                    high: "high";
                }>>;
                items: z.ZodArray<z.ZodString>;
            }, z.core.$strict>;
            substitutes: z.ZodObject<{
                label: z.ZodOptional<z.ZodString>;
                intensity: z.ZodOptional<z.ZodEnum<{
                    low: "low";
                    medium: "medium";
                    high: "high";
                }>>;
                items: z.ZodArray<z.ZodString>;
            }, z.core.$strict>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"heatmap">;
            x_labels: z.ZodArray<z.ZodString>;
            y_labels: z.ZodArray<z.ZodString>;
            values: z.ZodArray<z.ZodArray<z.ZodNumber>>;
            domain: z.ZodOptional<z.ZodObject<{
                min: z.ZodNumber;
                max: z.ZodNumber;
            }, z.core.$strict>>;
            show_values: z.ZodOptional<z.ZodBoolean>;
            x_title: z.ZodOptional<z.ZodString>;
            y_title: z.ZodOptional<z.ZodString>;
            label_every: z.ZodOptional<z.ZodNumber>;
            steps: z.ZodOptional<z.ZodArray<z.ZodObject<{
                max: z.ZodOptional<z.ZodNumber>;
                label: z.ZodString;
                short: z.ZodOptional<z.ZodString>;
            }, z.core.$strict>>>;
            bands: z.ZodOptional<z.ZodArray<z.ZodObject<{
                from: z.ZodString;
                to: z.ZodString;
                label: z.ZodString;
                icon: z.ZodOptional<z.ZodEnum<{
                    [x: string]: string;
                }>>;
            }, z.core.$strict>>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"sankey">;
            nodes: z.ZodArray<z.ZodObject<{
                id: z.ZodString;
                label: z.ZodString;
            }, z.core.$strict>>;
            links: z.ZodArray<z.ZodObject<{
                from: z.ZodString;
                to: z.ZodString;
                value: z.ZodNumber;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"data_table">;
            title: z.ZodOptional<z.ZodString>;
            columns: z.ZodArray<z.ZodObject<{
                key: z.ZodString;
                label: z.ZodString;
                align: z.ZodOptional<z.ZodEnum<{
                    left: "left";
                    right: "right";
                    center: "center";
                }>>;
                emphasis: z.ZodOptional<z.ZodBoolean>;
                icon: z.ZodOptional<z.ZodEnum<{
                    [x: string]: string;
                }>>;
            }, z.core.$strict>>;
            rows: z.ZodArray<z.ZodObject<{
                cells: z.ZodRecord<z.ZodString, z.ZodUnion<readonly [z.ZodString, z.ZodNumber]>>;
                emphasis: z.ZodOptional<z.ZodEnum<{
                    highlight: "highlight";
                    total: "total";
                }>>;
                icon: z.ZodOptional<z.ZodEnum<{
                    [x: string]: string;
                }>>;
                tag: z.ZodOptional<z.ZodObject<{
                    text: z.ZodString;
                    quiet: z.ZodOptional<z.ZodBoolean>;
                    evidence: z.ZodOptional<z.ZodEnum<{
                        label: "label";
                        draft: "draft";
                        trial: "trial";
                        company: "company";
                        press: "press";
                        official: "official";
                        registry: "registry";
                        preprint: "preprint";
                    }>>;
                    settled: z.ZodOptional<z.ZodBoolean>;
                    tone: z.ZodOptional<z.ZodEnum<{
                        danger: "danger";
                        warning: "warning";
                        success: "success";
                    }>>;
                    basis: z.ZodOptional<z.ZodEnum<{
                        law: "law";
                        estimate: "estimate";
                        pending: "pending";
                        proposal: "proposal";
                    }>>;
                }, z.core.$strict>>;
            }, z.core.$strict>>;
            source: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"device_mockup">;
            device: z.ZodEnum<{
                phone: "phone";
                browser: "browser";
            }>;
            asset_id: z.ZodString;
            caption: z.ZodOptional<z.ZodString>;
            url: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"cycle">;
            title: z.ZodOptional<z.ZodString>;
            items: z.ZodArray<z.ZodObject<{
                label: z.ZodString;
                description: z.ZodOptional<z.ZodString>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"people_cards">;
            title: z.ZodOptional<z.ZodString>;
            people: z.ZodArray<z.ZodObject<{
                name: z.ZodString;
                role: z.ZodOptional<z.ZodString>;
                org: z.ZodOptional<z.ZodString>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"hub_spoke">;
            center: z.ZodString;
            items: z.ZodArray<z.ZodObject<{
                label: z.ZodString;
                description: z.ZodOptional<z.ZodString>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"progress_donuts">;
            items: z.ZodArray<z.ZodObject<{
                value: z.ZodString;
                unit: z.ZodOptional<z.ZodString>;
                label: z.ZodString;
                icon: z.ZodOptional<z.ZodEnum<{
                    [x: string]: string;
                }>>;
                source: z.ZodOptional<z.ZodString>;
                detail: z.ZodOptional<z.ZodString>;
                emphasis: z.ZodOptional<z.ZodBoolean>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"staircase">;
            items: z.ZodArray<z.ZodObject<{
                title: z.ZodString;
                value: z.ZodString;
                unit: z.ZodOptional<z.ZodString>;
                note: z.ZodOptional<z.ZodString>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"chevron_process">;
            items: z.ZodArray<z.ZodObject<{
                title: z.ZodString;
                text: z.ZodOptional<z.ZodString>;
                icon: z.ZodOptional<z.ZodEnum<{
                    [x: string]: string;
                }>>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"swimlane">;
            lanes: z.ZodArray<z.ZodObject<{
                label: z.ZodString;
                role: z.ZodOptional<z.ZodString>;
            }, z.core.$strict>>;
            steps: z.ZodArray<z.ZodObject<{
                lane: z.ZodString;
                title: z.ZodString;
                detail: z.ZodOptional<z.ZodString>;
            }, z.core.$strict>>;
            handoff_note: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"journey_map">;
            stages: z.ZodArray<z.ZodObject<{
                label: z.ZodString;
                touchpoints: z.ZodOptional<z.ZodArray<z.ZodString>>;
                action: z.ZodOptional<z.ZodString>;
                emotion: z.ZodNumber;
                opportunity: z.ZodOptional<z.ZodString>;
            }, z.core.$strict>>;
            row_labels: z.ZodOptional<z.ZodObject<{
                touchpoints: z.ZodOptional<z.ZodString>;
                action: z.ZodOptional<z.ZodString>;
                emotion: z.ZodOptional<z.ZodString>;
                opportunity: z.ZodOptional<z.ZodString>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"decision_tree">;
            question: z.ZodString;
            branches: z.ZodArray<z.ZodObject<{
                edge: z.ZodString;
                title: z.ZodString;
                detail: z.ZodOptional<z.ZodString>;
                outcomes: z.ZodArray<z.ZodObject<{
                    edge: z.ZodString;
                    title: z.ZodString;
                    detail: z.ZodOptional<z.ZodString>;
                    value: z.ZodOptional<z.ZodString>;
                    unit: z.ZodOptional<z.ZodString>;
                    recommended: z.ZodOptional<z.ZodBoolean>;
                }, z.core.$strict>>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"from_to">;
            from: z.ZodObject<{
                kicker: z.ZodOptional<z.ZodString>;
                title: z.ZodString;
            }, z.core.$strict>;
            to: z.ZodObject<{
                kicker: z.ZodOptional<z.ZodString>;
                title: z.ZodString;
            }, z.core.$strict>;
            rows: z.ZodArray<z.ZodObject<{
                label: z.ZodString;
                icon: z.ZodOptional<z.ZodEnum<{
                    [x: string]: string;
                }>>;
                note: z.ZodOptional<z.ZodString>;
                from: z.ZodString;
                to: z.ZodString;
                unit: z.ZodOptional<z.ZodString>;
                change: z.ZodOptional<z.ZodString>;
                tag: z.ZodOptional<z.ZodObject<{
                    text: z.ZodString;
                    quiet: z.ZodOptional<z.ZodBoolean>;
                    evidence: z.ZodOptional<z.ZodEnum<{
                        label: "label";
                        draft: "draft";
                        trial: "trial";
                        company: "company";
                        press: "press";
                        official: "official";
                        registry: "registry";
                        preprint: "preprint";
                    }>>;
                    settled: z.ZodOptional<z.ZodBoolean>;
                    tone: z.ZodOptional<z.ZodEnum<{
                        danger: "danger";
                        warning: "warning";
                        success: "success";
                    }>>;
                    basis: z.ZodOptional<z.ZodEnum<{
                        law: "law";
                        estimate: "estimate";
                        pending: "pending";
                        proposal: "proposal";
                    }>>;
                }, z.core.$strict>>;
                emphasis: z.ZodOptional<z.ZodBoolean>;
            }, z.core.$strict>>;
            label_column: z.ZodOptional<z.ZodString>;
            span: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"org_tree">;
            root: z.ZodObject<{
                name: z.ZodString;
                role: z.ZodOptional<z.ZodString>;
            }, z.core.$strict>;
            children: z.ZodArray<z.ZodObject<{
                name: z.ZodString;
                role: z.ZodOptional<z.ZodString>;
                children: z.ZodOptional<z.ZodArray<z.ZodObject<{
                    name: z.ZodString;
                    role: z.ZodOptional<z.ZodString>;
                }, z.core.$strict>>>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"issue_tree">;
            question: z.ZodString;
            children_column: z.ZodOptional<z.ZodString>;
            branches: z.ZodArray<z.ZodObject<{
                label: z.ZodString;
                note: z.ZodOptional<z.ZodString>;
                icon: z.ZodOptional<z.ZodEnum<{
                    [x: string]: string;
                }>>;
                emphasis: z.ZodOptional<z.ZodLiteral<true>>;
                children: z.ZodOptional<z.ZodArray<z.ZodObject<{
                    label: z.ZodString;
                }, z.core.$strict>>>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"pyramid">;
            layers: z.ZodArray<z.ZodObject<{
                label: z.ZodString;
                note: z.ZodOptional<z.ZodString>;
                tone: z.ZodOptional<z.ZodEnum<{
                    danger: "danger";
                    warning: "warning";
                    success: "success";
                }>>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"iceberg">;
            above: z.ZodArray<z.ZodString>;
            below: z.ZodArray<z.ZodString>;
            waterline: z.ZodOptional<z.ZodString>;
            above_label: z.ZodOptional<z.ZodString>;
            below_label: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"pillar_model">;
            goal: z.ZodString;
            pillars: z.ZodArray<z.ZodObject<{
                title: z.ZodString;
                value: z.ZodString;
                unit: z.ZodOptional<z.ZodString>;
            }, z.core.$strict>>;
            base: z.ZodString;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"value_chain">;
            primary: z.ZodArray<z.ZodObject<{
                label: z.ZodString;
                value: z.ZodOptional<z.ZodString>;
                unit: z.ZodOptional<z.ZodString>;
                emphasis: z.ZodOptional<z.ZodLiteral<true>>;
            }, z.core.$strict>>;
            support: z.ZodArray<z.ZodObject<{
                label: z.ZodString;
                note: z.ZodOptional<z.ZodString>;
            }, z.core.$strict>>;
            margin: z.ZodOptional<z.ZodObject<{
                label: z.ZodString;
                value: z.ZodOptional<z.ZodString>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"harvey_balls">;
            criteria: z.ZodArray<z.ZodString>;
            options: z.ZodArray<z.ZodObject<{
                label: z.ZodString;
                scores: z.ZodArray<z.ZodUnion<readonly [z.ZodLiteral<0>, z.ZodLiteral<25>, z.ZodLiteral<50>, z.ZodLiteral<75>, z.ZodLiteral<100>]>>;
                total: z.ZodOptional<z.ZodUnion<readonly [z.ZodString, z.ZodNumber]>>;
                highlight: z.ZodOptional<z.ZodBoolean>;
            }, z.core.$strict>>;
            legend: z.ZodOptional<z.ZodBoolean>;
            labels: z.ZodOptional<z.ZodObject<{
                option: z.ZodOptional<z.ZodString>;
                total: z.ZodOptional<z.ZodString>;
                none: z.ZodOptional<z.ZodString>;
                partial: z.ZodOptional<z.ZodString>;
                full: z.ZodOptional<z.ZodString>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"scorecard">;
            labels: z.ZodOptional<z.ZodObject<{
                metric: z.ZodOptional<z.ZodString>;
                target: z.ZodOptional<z.ZodString>;
                actual: z.ZodOptional<z.ZodString>;
                gap: z.ZodOptional<z.ZodString>;
                status: z.ZodOptional<z.ZodString>;
            }, z.core.$strict>>;
            rows: z.ZodArray<z.ZodObject<{
                label: z.ZodString;
                target: z.ZodString;
                actual: z.ZodString;
                gap: z.ZodString;
                status: z.ZodEnum<{
                    watch: "watch";
                    on_track: "on_track";
                    off_track: "off_track";
                }>;
                status_label: z.ZodOptional<z.ZodString>;
            }, z.core.$strict>>;
            note: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"pictogram">;
            rows: z.ZodArray<z.ZodObject<{
                filled: z.ZodNumber;
                label: z.ZodString;
                caption: z.ZodOptional<z.ZodString>;
                highlight: z.ZodOptional<z.ZodBoolean>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"word_cloud">;
            words: z.ZodArray<z.ZodObject<{
                text: z.ZodString;
                weight: z.ZodUnion<readonly [z.ZodLiteral<1>, z.ZodLiteral<2>, z.ZodLiteral<3>, z.ZodLiteral<4>]>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"venn">;
            sets: z.ZodArray<z.ZodObject<{
                label: z.ZodString;
            }, z.core.$strict>>;
            center: z.ZodString;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"fishbone">;
            effect: z.ZodString;
            ribs: z.ZodArray<z.ZodObject<{
                label: z.ZodString;
                causes: z.ZodArray<z.ZodString>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"positioning_map">;
            x_axis: z.ZodObject<{
                title: z.ZodString;
                low: z.ZodString;
                high: z.ZodString;
            }, z.core.$strict>;
            y_axis: z.ZodObject<{
                title: z.ZodString;
                low: z.ZodString;
                high: z.ZodString;
            }, z.core.$strict>;
            quadrants: z.ZodOptional<z.ZodObject<{
                top_left: z.ZodString;
                top_right: z.ZodString;
                bottom_left: z.ZodString;
                bottom_right: z.ZodString;
            }, z.core.$strict>>;
            points: z.ZodArray<z.ZodObject<{
                label: z.ZodString;
                x: z.ZodNumber;
                y: z.ZodNumber;
                emphasis: z.ZodOptional<z.ZodLiteral<true>>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"concept_equation">;
            operands: z.ZodArray<z.ZodObject<{
                label: z.ZodString;
                value: z.ZodOptional<z.ZodString>;
                note: z.ZodOptional<z.ZodString>;
                icon: z.ZodOptional<z.ZodEnum<{
                    [x: string]: string;
                }>>;
            }, z.core.$strict>>;
            result: z.ZodObject<{
                label: z.ZodString;
                value: z.ZodOptional<z.ZodString>;
                note: z.ZodOptional<z.ZodString>;
                icon: z.ZodOptional<z.ZodEnum<{
                    [x: string]: string;
                }>>;
            }, z.core.$strict>;
            excluded: z.ZodOptional<z.ZodObject<{
                label: z.ZodString;
                value: z.ZodOptional<z.ZodString>;
                note: z.ZodOptional<z.ZodString>;
                icon: z.ZodOptional<z.ZodEnum<{
                    [x: string]: string;
                }>>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"segmented_wheel">;
            center: z.ZodString;
            segments: z.ZodArray<z.ZodObject<{
                label: z.ZodString;
                value: z.ZodOptional<z.ZodString>;
                emphasis: z.ZodOptional<z.ZodLiteral<true>>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"pros_cons">;
            pros: z.ZodObject<{
                title: z.ZodString;
                items: z.ZodArray<z.ZodObject<{
                    label: z.ZodString;
                    note: z.ZodOptional<z.ZodString>;
                }, z.core.$strict>>;
            }, z.core.$strict>;
            cons: z.ZodObject<{
                title: z.ZodString;
                items: z.ZodArray<z.ZodObject<{
                    label: z.ZodString;
                    note: z.ZodOptional<z.ZodString>;
                }, z.core.$strict>>;
            }, z.core.$strict>;
            verdict: z.ZodString;
        }, z.core.$strict>, z.ZodObject<{
            type: z.ZodLiteral<"sketch">;
            kind: z.ZodEnum<{
                discontinuity: "discontinuity";
                difference_in_differences: "difference_in_differences";
            }>;
            at: z.ZodString;
            x_title: z.ZodString;
            y_title: z.ZodOptional<z.ZodString>;
            effect: z.ZodOptional<z.ZodString>;
            groups: z.ZodOptional<z.ZodArray<z.ZodString>>;
            direction: z.ZodOptional<z.ZodEnum<{
                up: "up";
                down: "down";
            }>>;
        }, z.core.$strict>], "type">>>;
        background: z.ZodOptional<z.ZodDiscriminatedUnion<[z.ZodObject<{
            kind: z.ZodLiteral<"color">;
            value: z.ZodString;
        }, z.core.$strict>, z.ZodObject<{
            kind: z.ZodLiteral<"gradient">;
            from: z.ZodString;
            to: z.ZodString;
            direction: z.ZodOptional<z.ZodEnum<{
                tb: "tb";
                lr: "lr";
                diagonal: "diagonal";
            }>>;
        }, z.core.$strict>, z.ZodObject<{
            kind: z.ZodLiteral<"asset">;
            asset_id: z.ZodString;
            overlay: z.ZodOptional<z.ZodObject<{
                color: z.ZodString;
                opacity: z.ZodNumber;
            }, z.core.$strict>>;
            fit: z.ZodOptional<z.ZodEnum<{
                cover: "cover";
                contain: "contain";
            }>>;
        }, z.core.$strict>], "kind">>;
        decor: z.ZodOptional<z.ZodObject<{
            kind: z.ZodEnum<{
                big_number: "big_number";
                corner_tag: "corner_tag";
                rule_line: "rule_line";
                quote_marks: "quote_marks";
                geo_dots: "geo_dots";
            }>;
            intensity: z.ZodOptional<z.ZodEnum<{
                subtle: "subtle";
                normal: "normal";
            }>>;
            text: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>>;
        image_side: z.ZodOptional<z.ZodEnum<{
            left: "left";
            right: "right";
        }>>;
        footnote: z.ZodOptional<z.ZodString>;
        notes: z.ZodOptional<z.ZodString>;
        type: z.ZodLiteral<"ending">;
    }, z.core.$strict>], "type">, unknown>>;
}, z.core.$strict>;
type PptxIR = z.infer<typeof PptxIRSchema>;
type Component = z.infer<typeof ComponentSchema>;
type BackgroundSpec = z.infer<typeof BackgroundSpecSchema>;
type Slide = z.infer<typeof SlideSchema>;
type PageKind$1 = (typeof KIND_VALUES)[number];
type Assets = z.infer<typeof AssetsSchema>;
type Meta = z.infer<typeof MetaSchema>;

/**
 * Narrative argument style (spec §5's five-way strategy classification,
 * renamed from "mode" — spec §8.1).
 */
type Strategy = (typeof STRATEGY_VALUES)[number];
/**
 * Content density budget + typographic baseline (spec §5 pacing table,
 * renamed from "delivery" — spec §8.1). See {@link PacingBudget} for the
 * dual-attribute capacity split this axis is one half of.
 */
type Pacing = (typeof PACING_VALUES)[number];
/**
 * Tone anchor only (spec §5: audience is tone-anchoring only, no rendering
 * effect on the IR yet). Reserved for a future lint pass (e.g. executive ×
 * long paragraphs → suggest kpi_cards/verdict_banner instead). The rule set
 * itself is explicitly out of scope this wave (spec §10 open questions).
 * Name unchanged by the vocabulary-v4 rename (spec §4.3: "audience 保持不变").
 */
type Audience = (typeof AUDIENCE_VALUES)[number];
interface NarrativeProfile {
    readonly strategy: Strategy;
    readonly pacing: Pacing;
    readonly audience: Audience;
}

interface StrategyDefinition {
    id: Strategy;
}
declare const STRATEGY_DEFINITIONS: Record<Strategy, StrategyDefinition>;

interface PacingBudget {
    /**
     * Body-text baseline, in px, at 1280×720 slide geometry (spec §5 pacing
     * table's body-baseline column). Wired into rendering as of W4 task 3
     * (design decision 9): `src/render/full-slide-svg.tsx` resolves
     * `PACING_BUDGETS[resolveNarrative(ir.narrative).pacing].bodyBaselinePx`
     * once and passes it into `buildCtx`, which stores it as
     * `ComponentCtx.bodyFontPx` — the sole font-size input for the
     * paragraph/bullets/callout trio ("正文" = continuous running text).
     * Every other component's own bespoke type scale, the heading system, and
     * quote's fixed 26px attribution line don't read this field. Since
     * `balanced` (24px) is the narrative default, an omitted-narrative deck
     * now renders body text at 24px, not the previous fixed 20px — the
     * one-time, spec-sanctioned snapshot re-pin that landed alongside this
     * wiring (W4 task 3, unchanged since — vocabulary-v4 only renames this
     * table, it doesn't touch any of its numbers, spec §10).
     */
    bodyBaselinePx: number;
    /**
     * Per-slide editorial budget (component count) — content discipline
     * ("how many things belong on this slide"), not geometry. Spec §5's
     * dual-attribute capacity split keeps *physical* capacity ("how many
     * things fit in this layout's slots") on the layout registry's body-slot
     * `capacity` metadata (`svg/layouts/registry.ts`). The W3 quality gate
     * takes `min(this budget, the resolved layout's body capacity)`.
     */
    maxComponentsPerSlide: number;
    bullets: {
        maxItems: number;
        /**
         * Same "unit" concept the deleted `CAPACITY.bullets` used
         * (`measureTextUnits`, CJK weight = 1.0) — a visual-width-weighted
         * character count, not a raw `.length`. The old physical ceiling (53,
         * derived from render geometry) was deleted in W3 without a replacement
         * check because every pacing's editorial budget here (30/40/48) is
         * already strictly tighter than it — the quality gate now applies
         * exactly this one number per pacing.
         */
        maxUnitsPerItem: number;
    };
}
/**
 * Pacing table: bodyBaselinePx / editorial budget / bullets budget.
 * Body never starts below 18pt (24px). Dense and balanced share that
 * size and differ by item count. Spacious still opens at 32px.
 * Bullet unit caps sit under CAPACITY.bullets.itemOverflowUnits (29),
 * the two-line × 24px × 398px two-column geometric ceiling after the
 * 0.9 safety discount.
 */
declare const PACING_BUDGETS: Record<Pacing, PacingBudget>;

interface NarrativePreset {
    id: string;
    axes: NarrativeProfile;
    /**
     * Narrative-side reference signal, never a hard constraint (spec §5).
     * Theme reachability is authored on the theme itself
     * (`src/themes/occasions.ts`). The selection entry is
     * `src/themes/select.ts`, which may consult this list as a tie-break
     * or as a fallback when no occasion signal is present. This field used
     * to be the authority that made a new theme reachable, an inverted
     * edge: new builtins had to edit the narrative table to be discovered,
     * and fourteen of twenty-four sat undiscoverable as a result. Values
     * here are unchanged. Every entry must still be a real
     * `BUILTIN_THEME_IDS` member (`ir/index.ts`). This module's test
     * suite enforces that.
     */
    themeRecommendations: readonly string[];
}
/**
 * Pinned to spec §5's 7 named presets and their theme recommendation table.
 * Preset ids are unchanged by the vocabulary-v4 rename (spec §5: "预设 ID
 * 保持不变") — only each preset's internal axes keys/values follow the
 * strategy/pacing rename (e.g. `annual-review`'s `mode: "narrative"` is now
 * `strategy: "storytelling"`, spec §5's own worked example).
 */
declare const NARRATIVE_PRESETS: Record<string, NarrativePreset>;
/**
 * = `NARRATIVE_PRESETS.general.axes` (briefing × balanced × public) — the
 * global default when narrative is omitted entirely (spec §5's defaults
 * chain).
 */
declare const DEFAULT_NARRATIVE: NarrativeProfile;
/**
 * Resolve a narrative input down to concrete axes, per spec §5's design
 * principle "omission gets the default, a typo is a hard error" (weak-model
 * friendly: a model that leaves a field out gets a sane deck, a model that
 * misspells a value gets a loud, actionable error instead of a silently
 * wrong deck):
 *
 * - `undefined` → {@link DEFAULT_NARRATIVE} (the `general` preset's axes)
 * - a preset id string → that preset's axes (unknown id throws
 *   {@link PptwiseError}, listing the available preset ids)
 * - a partial axes object → each axis defaults independently
 *   (strategy → "briefing", pacing → "balanced", audience → "public" — these
 *   happen to equal `DEFAULT_NARRATIVE`'s values because `general` *is* that
 *   exact combination, but the fallback here is per-axis, not "any omitted
 *   axis falls back to the whole default object")
 * - an `{id: <preset>}` object (T0b fix 2, scope-extended — see
 *   {@link rescueIdShape}) → silently treated as that bare preset-id string,
 *   the same weak-model shape slip `theme: {id: "brief"}` invites by
 *   analogy. Folded directly into this function's own entry (not just a
 *   pre-parse pass two of its six call sites happen to run) so every caller
 *   — `validateIr`, `validateSpec`, `layout-selection.ts`,
 *   `full-slide-svg.tsx`, `ir-quality.ts`, `cli/commands.ts` alike — gets
 *   this tolerance for free, present and future. Silent here (no rewrite
 *   note — this is a pure resolver with no reporting channel, and adding one
 *   would ripple into every one of those call sites' own return-shape
 *   expectations); `validateIr`/`validateSpec` additionally run
 *   {@link normalizeNarrativeShape} on their own raw pre-parse input first,
 *   specifically to report + persist the rewrite into what they return.
 *
 * An unknown axis value, or an unknown key on the partial axes object,
 * always throws {@link PptwiseError} (never silently ignored or dropped) —
 * omission and a typo are different intents, and only the former has a
 * reasonable default. A mixed `{id, strategy}`-style shape is exactly this
 * case ({@link rescueIdShape} declines it): `id` is simply an unrecognized
 * key, so it hard-errors the same as any other typo.
 */
declare function resolveNarrative(input: string | Partial<NarrativeProfile> | undefined): NarrativeProfile;

/**
 * A design story is the public record of one design object: what it is, when
 * to choose it, who it is for, and when not to choose it. Themes, content
 * kinds, faces, and components all carry one, in the same six fields.
 *
 * Stories are customer-facing copy. They are written in English at the
 * definition they describe, and the gallery translates them for review. Two
 * consequences follow, and both are enforced below:
 *
 * - No maintainer vocabulary. A story never names a file, a registry, an
 *   internal id, or the machinery that draws a page. It reads like product
 *   copy because it is product copy — README sections, theme pages, and the
 *   gallery all draw from it. See {@link MAINTAINER_WORDS}.
 * - A name names a voice or a genre, never a vertical, a function, an
 *   audience, or an organization type. See {@link FORBIDDEN_NAME_WORDS}. A
 *   name that squats on one of those locks the object to one customer while
 *   what it actually sells is a tone of voice any customer can borrow.
 *
 * This module is a leaf: it imports nothing, so every layer can hold a story
 * beside its definition without a dependency cycle.
 */
/** One design object's public record, shared by every layer. */
interface DesignStory {
    /** Display name. A voice or a genre — see the naming rule above. */
    name: string;
    /** What it is, and which real-world form of print or staging it borrows. */
    story: string;
    /** When to choose it. */
    positioning: string;
    /** Who speaks from it, and who is listening. */
    audience: string;
    /** When not to choose it. Reverse positioning prevents more misuse than the forward kind. */
    notFor: string;
    /** Optional: where it comes from, what it references, what it pays tribute to. */
    lineage?: string;
}

type LayoutType = "cover" | "chapter" | "content" | "ending";
interface StyleColors {
    bg: string;
    surface: string;
    panel?: string;
    primary: string;
    accent: string;
    text: string;
    muted: string;
    border?: string;
    chartPalette: string[];
    /**
     * Optional accent color pool for themes whose layout grammar cycles through
     * multiple accent colors (e.g. terminal card corner stripes). Themes that
     * only use a single accent color can omit this.
     */
    accentPool?: string[];
    /**
     * Optional hairline stroke color for the shared "surface card" shells
     * (kpi_cards / icon_cards / callout — see components/kpi.tsx,
     * components/icon-cards.tsx, components/callout.tsx). Those component renderers are
     * shared across every theme and must stay theme-agnostic (no
     * `if (themeId === ...)` branching), so a theme that wants its cards
     * outlined sets this token instead — the renderers just consult it and add
     * a 1px stroke when it's defined. Omitted (`undefined`, the default) draws
     * no stroke, so every theme that doesn't set it keeps its current
     * fill-only card unchanged.
     */
    cardStroke?: string;
    /**
     * Optional ink for a `**marked**` run, when the theme's `accent` cannot do
     * that job. Omitted (the default) resolves to `accent`, so a theme that
     * leaves it out renders byte-for-byte as it did before this token existed.
     *
     * Same reasoning as `cardStroke` above — the emphasis renderers are shared
     * across every theme and must stay theme-agnostic — but the pressure is
     * different. `accent` answers to the page background: it has to stay legible
     * where it is painted. An emphasis run answers to the *text it interrupts*:
     * it has to look different from the words on either side of it. Most themes
     * have one colour that does both. A theme whose accent is a near-neutral in
     * the same family as its text ink does not, and its marked runs read as
     * faded rather than emphasised (stage, whose muted silver sits 1.60:1 from
     * its own paper white). Splitting the token lets such a theme keep its
     * accent for decoration and name a second ink for emphasis.
     *
     * `themes/definitions.test.ts` pins the separation rule for all built-ins.
     */
    emphasisInk?: string;
    /**
     * Optional semantic-role colors — the "this is an error", "this is a
     * caution", "this is a good result" trio that shared component renderers
     * used to bake in as literal hexes (`callout`'s warn rule and icon in
     * components/callout.tsx, `kpi_cards`' delta arrow in components/kpi.tsx).
     * Same reasoning as `cardStroke` above: those renderers are shared across
     * every theme and must stay theme-agnostic (no `if (themeId === ...)`
     * branching), so a theme that wants its own red or green sets these tokens
     * and the renderers read them through `resolveSemanticColor`
     * (`src/render/ink.ts`), which owns the fallback order.
     *
     * All three are optional on the type, and an omitted role resolves to
     * exactly the hex its renderers baked in before this channel existed —
     * `#DC2626` for `danger`, `#16A34A` for `success`, and `warning` follows
     * whatever `danger` resolves to. So a theme that sets none of them renders
     * byte-for-byte as it did before the tokens were added.
     *
     * Every one of the 22 built-in themes does set all three (visual review
     * round 4 ruled that the alert color must belong to the theme's own
     * palette, not be one universal red), so in practice only a `--theme-file`
     * brand theme reaches the fallbacks. `danger` and `success` are calibrated
     * to clear 4.5:1 on their own theme's `surface` — they render as the kpi
     * delta arrow's *text*, which `accessibleInk` would otherwise demote to
     * neutral ink — while `warning` only has to clear the 3:1 non-text floor,
     * since `callout` paints it as a rule and an icon. Both floors are pinned
     * in `svg/audit/full-matrix-contrast.test.ts`.
     */
    danger?: string;
    warning?: string;
    success?: string;
}
interface StyleFonts {
    heading: string[];
    body: string[];
    mono?: string[];
    /** The stack large numbers are set in. Omitted, they take `heading`. */
    figure?: string[];
}
interface StyleTokens {
    id: string;
    allowCustomBackground?: boolean;
    colors: StyleColors;
    fonts: StyleFonts;
    shape?: StyleShape;
    defaultBackgrounds: Record<LayoutType, BackgroundSpec>;
}
/**
 * 主题细节 shape token（2026-07-10 用户立项，spec：
 * .issues/specs/2026-07-10-pptx-theme-detail-tokens-design.md）。
 * 全部可选——缺省时各消费点沿用自己的 baked 值（零观感）。
 */
interface StyleShape {
    /** 卡片/横幅圆角 px（统一值）。缺省=各消费点原 baked 值（kpi 8/architecture 6/白卡 14 等）。 */
    radius?: number;
    /** 块间距缩放（1=现 BLOCK_GAP）。建议范围 [0.8, 1.3]。 */
    gapScale?: number;
    /**
     * Heading and display size multiplier. Applied to the layout's designed
     * max size *before* heading-fit shrinks to the box (`fitHeadingLines` /
     * `fitHeadingPt`, `src/render/heading-fit.ts`). Cover, chapter, ending, and
     * pin-only speech pages pass it through. Content layouts that share the
     * page with a body stack omit it, so density still holds. Body, meta,
     * kicker, and footnote sizes are untouched. Omit (or `1`) for a
     * byte-identical no-op. Fit still owns the floor: `minPt` is not scaled,
     * so a long title still shrinks instead of overflowing. Suggested range
     * `[0.8, 1.6]`.
     */
    typeScale?: number;
    /**
     * How the shared components draw what a web page would set on a card.
     * `"filled"` (omitted, the default) lays each card, cell, node and badge
     * on a fill of its own. `"ruled"` sets them the way a printed document
     * does: no fill and no rounded corner, hairlines and rules between parts,
     * numbers as type rather than in discs, a dark block as an outline, a
     * table on rules with no tinted rows, and emphasis carried by weight, the
     * ink and one line of the accent. Charts keep their marks. Omitted, every
     * component renders byte for byte as it did before the token existed.
     * The renderers read it through `isRuled` (`components/surfaces.ts`).
     */
    surfaces?: SurfaceTreatment;
}
/** The two ways a theme's shared components draw a card: see `StyleShape.surfaces`. */
declare const SURFACE_TREATMENTS: readonly ["filled", "ruled"];
type SurfaceTreatment = (typeof SURFACE_TREATMENTS)[number];

/**
 * Identity strength band for a theme's visual voice. `low` is a quiet
 * institutional register. `medium` is a professional house style.
 * `high` is a strong, costume-grade expression.
 */
declare const IDENTITY_STRENGTHS: readonly ["low", "medium", "high"];
type IdentityStrength = (typeof IDENTITY_STRENGTHS)[number];
/**
 * Controlled occasion vocabulary. Theme metadata and `suggestThemes`
 * both key off this list. Unknown words are ignored at selection time.
 * Each gloss is one English line naming the decks that word is for.
 */
declare const OCCASION_VOCAB: {
    readonly business: "Corporate proposals, consulting reports, and general commercial decks.";
    readonly sales: "Client proposals, solution offers, and bids a customer signs off.";
    readonly institutional: "Quiet org voice: annual reports, policy briefings, audits, and memos.";
    readonly finance: "Markets, terminals, and financial insight.";
    readonly marketing: "Campaigns, brand launches, and promotional storytelling.";
    readonly education: "Teaching, training, lectures, and research communication.";
    readonly culture: "Heritage, tradition, the arts, and cultural programming.";
    readonly tech: "Product, engineering, and deep-tech decks.";
    readonly health: "Clinical, hospital, and life-science communication.";
    readonly sustainability: "ESG, climate, and long-horizon stewardship reports.";
    readonly startup: "Fundraising pitches and early-stage company stories.";
    readonly government: "Official reports, work summaries, and civic briefings.";
    readonly kids: "Early-years and family-facing education.";
    readonly entertainment: "Esports, live shows, and fan-facing events.";
    readonly museum: "Galleries, exhibitions, and interpretive programs.";
    readonly keynote: "On-stage product reveals and keynote talks.";
    readonly fashion: "Runway, lookbooks, and fashion-house voice.";
    readonly editorial: "Journals, features, and long-form editorial reviews.";
    readonly luxury: "Maison, beauty, and invitation-grade hospitality.";
    readonly event: "Short-run announcements, recitals, and convenings.";
    readonly career: "One person before a panel: candidacies, self-introductions, and career plans.";
    readonly review: "One person accounting for their work to reviewers: year-end reviews, probation reviews, and promotion defences.";
};
type Occasion = keyof typeof OCCASION_VOCAB;

/**
 * How a theme draws a `**marked**` run inside body text. Part of a theme's
 * identity, not of any component: `"tint"` (omitted) recolors the run in the
 * accent, `"pad"` swipes a marker-pen block behind it, `"underline"` strikes
 * a chalk line under it.
 */
declare const EMPHASIS_TREATMENTS: readonly ["tint", "pad", "underline"];
type EmphasisTreatment = (typeof EMPHASIS_TREATMENTS)[number];
/**
 * A theme menu has one entry for each boundary page type and a non-empty
 * subset of the global content-kind vocabulary. Each key maps directly to
 * one face with no rotation or conditional branch.
 */
declare const MenuSchema: z.ZodObject<{
    cover: z.ZodObject<{
        face: z.ZodString;
        params: z.ZodOptional<z.ZodRecord<z.ZodString, z.ZodUnion<readonly [z.ZodString, z.ZodNumber, z.ZodBoolean]>>>;
        decor: z.ZodOptional<z.ZodDiscriminatedUnion<[z.ZodObject<{
            kind: z.ZodLiteral<"motif">;
            id: z.ZodType<MotifId, unknown, z.core.$ZodTypeInternals<MotifId, unknown>>;
            params: z.ZodOptional<z.ZodObject<{
                intensity: z.ZodOptional<z.ZodEnum<{
                    subtle: "subtle";
                    normal: "normal";
                }>>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            kind: z.ZodLiteral<"silent">;
        }, z.core.$strict>], "kind">>;
        brand: z.ZodOptional<z.ZodLiteral<"none">>;
    }, z.core.$strict>;
    chapter: z.ZodObject<{
        face: z.ZodString;
        params: z.ZodOptional<z.ZodRecord<z.ZodString, z.ZodUnion<readonly [z.ZodString, z.ZodNumber, z.ZodBoolean]>>>;
        decor: z.ZodOptional<z.ZodDiscriminatedUnion<[z.ZodObject<{
            kind: z.ZodLiteral<"motif">;
            id: z.ZodType<MotifId, unknown, z.core.$ZodTypeInternals<MotifId, unknown>>;
            params: z.ZodOptional<z.ZodObject<{
                intensity: z.ZodOptional<z.ZodEnum<{
                    subtle: "subtle";
                    normal: "normal";
                }>>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            kind: z.ZodLiteral<"silent">;
        }, z.core.$strict>], "kind">>;
        brand: z.ZodOptional<z.ZodLiteral<"none">>;
    }, z.core.$strict>;
    content: z.ZodObject<{
        points: z.ZodOptional<z.ZodObject<{
            face: z.ZodString;
            params: z.ZodOptional<z.ZodRecord<z.ZodString, z.ZodUnion<readonly [z.ZodString, z.ZodNumber, z.ZodBoolean]>>>;
            decor: z.ZodOptional<z.ZodDiscriminatedUnion<[z.ZodObject<{
                kind: z.ZodLiteral<"motif">;
                id: z.ZodType<MotifId, unknown, z.core.$ZodTypeInternals<MotifId, unknown>>;
                params: z.ZodOptional<z.ZodObject<{
                    intensity: z.ZodOptional<z.ZodEnum<{
                        subtle: "subtle";
                        normal: "normal";
                    }>>;
                }, z.core.$strict>>;
            }, z.core.$strict>, z.ZodObject<{
                kind: z.ZodLiteral<"silent">;
            }, z.core.$strict>], "kind">>;
            brand: z.ZodOptional<z.ZodLiteral<"none">>;
        }, z.core.$strict>>;
        list: z.ZodOptional<z.ZodObject<{
            face: z.ZodString;
            params: z.ZodOptional<z.ZodRecord<z.ZodString, z.ZodUnion<readonly [z.ZodString, z.ZodNumber, z.ZodBoolean]>>>;
            decor: z.ZodOptional<z.ZodDiscriminatedUnion<[z.ZodObject<{
                kind: z.ZodLiteral<"motif">;
                id: z.ZodType<MotifId, unknown, z.core.$ZodTypeInternals<MotifId, unknown>>;
                params: z.ZodOptional<z.ZodObject<{
                    intensity: z.ZodOptional<z.ZodEnum<{
                        subtle: "subtle";
                        normal: "normal";
                    }>>;
                }, z.core.$strict>>;
            }, z.core.$strict>, z.ZodObject<{
                kind: z.ZodLiteral<"silent">;
            }, z.core.$strict>], "kind">>;
            brand: z.ZodOptional<z.ZodLiteral<"none">>;
        }, z.core.$strict>>;
        comparison: z.ZodOptional<z.ZodObject<{
            face: z.ZodString;
            params: z.ZodOptional<z.ZodRecord<z.ZodString, z.ZodUnion<readonly [z.ZodString, z.ZodNumber, z.ZodBoolean]>>>;
            decor: z.ZodOptional<z.ZodDiscriminatedUnion<[z.ZodObject<{
                kind: z.ZodLiteral<"motif">;
                id: z.ZodType<MotifId, unknown, z.core.$ZodTypeInternals<MotifId, unknown>>;
                params: z.ZodOptional<z.ZodObject<{
                    intensity: z.ZodOptional<z.ZodEnum<{
                        subtle: "subtle";
                        normal: "normal";
                    }>>;
                }, z.core.$strict>>;
            }, z.core.$strict>, z.ZodObject<{
                kind: z.ZodLiteral<"silent">;
            }, z.core.$strict>], "kind">>;
            brand: z.ZodOptional<z.ZodLiteral<"none">>;
        }, z.core.$strict>>;
        process: z.ZodOptional<z.ZodObject<{
            face: z.ZodString;
            params: z.ZodOptional<z.ZodRecord<z.ZodString, z.ZodUnion<readonly [z.ZodString, z.ZodNumber, z.ZodBoolean]>>>;
            decor: z.ZodOptional<z.ZodDiscriminatedUnion<[z.ZodObject<{
                kind: z.ZodLiteral<"motif">;
                id: z.ZodType<MotifId, unknown, z.core.$ZodTypeInternals<MotifId, unknown>>;
                params: z.ZodOptional<z.ZodObject<{
                    intensity: z.ZodOptional<z.ZodEnum<{
                        subtle: "subtle";
                        normal: "normal";
                    }>>;
                }, z.core.$strict>>;
            }, z.core.$strict>, z.ZodObject<{
                kind: z.ZodLiteral<"silent">;
            }, z.core.$strict>], "kind">>;
            brand: z.ZodOptional<z.ZodLiteral<"none">>;
        }, z.core.$strict>>;
        data: z.ZodOptional<z.ZodObject<{
            face: z.ZodString;
            params: z.ZodOptional<z.ZodRecord<z.ZodString, z.ZodUnion<readonly [z.ZodString, z.ZodNumber, z.ZodBoolean]>>>;
            decor: z.ZodOptional<z.ZodDiscriminatedUnion<[z.ZodObject<{
                kind: z.ZodLiteral<"motif">;
                id: z.ZodType<MotifId, unknown, z.core.$ZodTypeInternals<MotifId, unknown>>;
                params: z.ZodOptional<z.ZodObject<{
                    intensity: z.ZodOptional<z.ZodEnum<{
                        subtle: "subtle";
                        normal: "normal";
                    }>>;
                }, z.core.$strict>>;
            }, z.core.$strict>, z.ZodObject<{
                kind: z.ZodLiteral<"silent">;
            }, z.core.$strict>], "kind">>;
            brand: z.ZodOptional<z.ZodLiteral<"none">>;
        }, z.core.$strict>>;
        photo: z.ZodOptional<z.ZodObject<{
            face: z.ZodString;
            params: z.ZodOptional<z.ZodRecord<z.ZodString, z.ZodUnion<readonly [z.ZodString, z.ZodNumber, z.ZodBoolean]>>>;
            decor: z.ZodOptional<z.ZodDiscriminatedUnion<[z.ZodObject<{
                kind: z.ZodLiteral<"motif">;
                id: z.ZodType<MotifId, unknown, z.core.$ZodTypeInternals<MotifId, unknown>>;
                params: z.ZodOptional<z.ZodObject<{
                    intensity: z.ZodOptional<z.ZodEnum<{
                        subtle: "subtle";
                        normal: "normal";
                    }>>;
                }, z.core.$strict>>;
            }, z.core.$strict>, z.ZodObject<{
                kind: z.ZodLiteral<"silent">;
            }, z.core.$strict>], "kind">>;
            brand: z.ZodOptional<z.ZodLiteral<"none">>;
        }, z.core.$strict>>;
        statement: z.ZodOptional<z.ZodObject<{
            face: z.ZodString;
            params: z.ZodOptional<z.ZodRecord<z.ZodString, z.ZodUnion<readonly [z.ZodString, z.ZodNumber, z.ZodBoolean]>>>;
            decor: z.ZodOptional<z.ZodDiscriminatedUnion<[z.ZodObject<{
                kind: z.ZodLiteral<"motif">;
                id: z.ZodType<MotifId, unknown, z.core.$ZodTypeInternals<MotifId, unknown>>;
                params: z.ZodOptional<z.ZodObject<{
                    intensity: z.ZodOptional<z.ZodEnum<{
                        subtle: "subtle";
                        normal: "normal";
                    }>>;
                }, z.core.$strict>>;
            }, z.core.$strict>, z.ZodObject<{
                kind: z.ZodLiteral<"silent">;
            }, z.core.$strict>], "kind">>;
            brand: z.ZodOptional<z.ZodLiteral<"none">>;
        }, z.core.$strict>>;
        quote: z.ZodOptional<z.ZodObject<{
            face: z.ZodString;
            params: z.ZodOptional<z.ZodRecord<z.ZodString, z.ZodUnion<readonly [z.ZodString, z.ZodNumber, z.ZodBoolean]>>>;
            decor: z.ZodOptional<z.ZodDiscriminatedUnion<[z.ZodObject<{
                kind: z.ZodLiteral<"motif">;
                id: z.ZodType<MotifId, unknown, z.core.$ZodTypeInternals<MotifId, unknown>>;
                params: z.ZodOptional<z.ZodObject<{
                    intensity: z.ZodOptional<z.ZodEnum<{
                        subtle: "subtle";
                        normal: "normal";
                    }>>;
                }, z.core.$strict>>;
            }, z.core.$strict>, z.ZodObject<{
                kind: z.ZodLiteral<"silent">;
            }, z.core.$strict>], "kind">>;
            brand: z.ZodOptional<z.ZodLiteral<"none">>;
        }, z.core.$strict>>;
        fact: z.ZodOptional<z.ZodObject<{
            face: z.ZodString;
            params: z.ZodOptional<z.ZodRecord<z.ZodString, z.ZodUnion<readonly [z.ZodString, z.ZodNumber, z.ZodBoolean]>>>;
            decor: z.ZodOptional<z.ZodDiscriminatedUnion<[z.ZodObject<{
                kind: z.ZodLiteral<"motif">;
                id: z.ZodType<MotifId, unknown, z.core.$ZodTypeInternals<MotifId, unknown>>;
                params: z.ZodOptional<z.ZodObject<{
                    intensity: z.ZodOptional<z.ZodEnum<{
                        subtle: "subtle";
                        normal: "normal";
                    }>>;
                }, z.core.$strict>>;
            }, z.core.$strict>, z.ZodObject<{
                kind: z.ZodLiteral<"silent">;
            }, z.core.$strict>], "kind">>;
            brand: z.ZodOptional<z.ZodLiteral<"none">>;
        }, z.core.$strict>>;
        evidence: z.ZodOptional<z.ZodObject<{
            face: z.ZodString;
            params: z.ZodOptional<z.ZodRecord<z.ZodString, z.ZodUnion<readonly [z.ZodString, z.ZodNumber, z.ZodBoolean]>>>;
            decor: z.ZodOptional<z.ZodDiscriminatedUnion<[z.ZodObject<{
                kind: z.ZodLiteral<"motif">;
                id: z.ZodType<MotifId, unknown, z.core.$ZodTypeInternals<MotifId, unknown>>;
                params: z.ZodOptional<z.ZodObject<{
                    intensity: z.ZodOptional<z.ZodEnum<{
                        subtle: "subtle";
                        normal: "normal";
                    }>>;
                }, z.core.$strict>>;
            }, z.core.$strict>, z.ZodObject<{
                kind: z.ZodLiteral<"silent">;
            }, z.core.$strict>], "kind">>;
            brand: z.ZodOptional<z.ZodLiteral<"none">>;
        }, z.core.$strict>>;
        hierarchy: z.ZodOptional<z.ZodObject<{
            face: z.ZodString;
            params: z.ZodOptional<z.ZodRecord<z.ZodString, z.ZodUnion<readonly [z.ZodString, z.ZodNumber, z.ZodBoolean]>>>;
            decor: z.ZodOptional<z.ZodDiscriminatedUnion<[z.ZodObject<{
                kind: z.ZodLiteral<"motif">;
                id: z.ZodType<MotifId, unknown, z.core.$ZodTypeInternals<MotifId, unknown>>;
                params: z.ZodOptional<z.ZodObject<{
                    intensity: z.ZodOptional<z.ZodEnum<{
                        subtle: "subtle";
                        normal: "normal";
                    }>>;
                }, z.core.$strict>>;
            }, z.core.$strict>, z.ZodObject<{
                kind: z.ZodLiteral<"silent">;
            }, z.core.$strict>], "kind">>;
            brand: z.ZodOptional<z.ZodLiteral<"none">>;
        }, z.core.$strict>>;
    }, z.core.$strict>;
    ending: z.ZodObject<{
        face: z.ZodString;
        params: z.ZodOptional<z.ZodRecord<z.ZodString, z.ZodUnion<readonly [z.ZodString, z.ZodNumber, z.ZodBoolean]>>>;
        decor: z.ZodOptional<z.ZodDiscriminatedUnion<[z.ZodObject<{
            kind: z.ZodLiteral<"motif">;
            id: z.ZodType<MotifId, unknown, z.core.$ZodTypeInternals<MotifId, unknown>>;
            params: z.ZodOptional<z.ZodObject<{
                intensity: z.ZodOptional<z.ZodEnum<{
                    subtle: "subtle";
                    normal: "normal";
                }>>;
            }, z.core.$strict>>;
        }, z.core.$strict>, z.ZodObject<{
            kind: z.ZodLiteral<"silent">;
        }, z.core.$strict>], "kind">>;
        brand: z.ZodOptional<z.ZodLiteral<"none">>;
    }, z.core.$strict>;
}, z.core.$strict>;
/** Public v2 theme-file contract: structure, and the customer naming rule. */
declare const ThemeFileSchema: z.ZodObject<{
    version: z.ZodLiteral<2>;
    menu: z.ZodObject<{
        cover: z.ZodObject<{
            face: z.ZodString;
            params: z.ZodOptional<z.ZodRecord<z.ZodString, z.ZodUnion<readonly [z.ZodString, z.ZodNumber, z.ZodBoolean]>>>;
            decor: z.ZodOptional<z.ZodDiscriminatedUnion<[z.ZodObject<{
                kind: z.ZodLiteral<"motif">;
                id: z.ZodType<MotifId, unknown, z.core.$ZodTypeInternals<MotifId, unknown>>;
                params: z.ZodOptional<z.ZodObject<{
                    intensity: z.ZodOptional<z.ZodEnum<{
                        subtle: "subtle";
                        normal: "normal";
                    }>>;
                }, z.core.$strict>>;
            }, z.core.$strict>, z.ZodObject<{
                kind: z.ZodLiteral<"silent">;
            }, z.core.$strict>], "kind">>;
            brand: z.ZodOptional<z.ZodLiteral<"none">>;
        }, z.core.$strict>;
        chapter: z.ZodObject<{
            face: z.ZodString;
            params: z.ZodOptional<z.ZodRecord<z.ZodString, z.ZodUnion<readonly [z.ZodString, z.ZodNumber, z.ZodBoolean]>>>;
            decor: z.ZodOptional<z.ZodDiscriminatedUnion<[z.ZodObject<{
                kind: z.ZodLiteral<"motif">;
                id: z.ZodType<MotifId, unknown, z.core.$ZodTypeInternals<MotifId, unknown>>;
                params: z.ZodOptional<z.ZodObject<{
                    intensity: z.ZodOptional<z.ZodEnum<{
                        subtle: "subtle";
                        normal: "normal";
                    }>>;
                }, z.core.$strict>>;
            }, z.core.$strict>, z.ZodObject<{
                kind: z.ZodLiteral<"silent">;
            }, z.core.$strict>], "kind">>;
            brand: z.ZodOptional<z.ZodLiteral<"none">>;
        }, z.core.$strict>;
        content: z.ZodObject<{
            points: z.ZodOptional<z.ZodObject<{
                face: z.ZodString;
                params: z.ZodOptional<z.ZodRecord<z.ZodString, z.ZodUnion<readonly [z.ZodString, z.ZodNumber, z.ZodBoolean]>>>;
                decor: z.ZodOptional<z.ZodDiscriminatedUnion<[z.ZodObject<{
                    kind: z.ZodLiteral<"motif">;
                    id: z.ZodType<MotifId, unknown, z.core.$ZodTypeInternals<MotifId, unknown>>;
                    params: z.ZodOptional<z.ZodObject<{
                        intensity: z.ZodOptional<z.ZodEnum<{
                            subtle: "subtle";
                            normal: "normal";
                        }>>;
                    }, z.core.$strict>>;
                }, z.core.$strict>, z.ZodObject<{
                    kind: z.ZodLiteral<"silent">;
                }, z.core.$strict>], "kind">>;
                brand: z.ZodOptional<z.ZodLiteral<"none">>;
            }, z.core.$strict>>;
            list: z.ZodOptional<z.ZodObject<{
                face: z.ZodString;
                params: z.ZodOptional<z.ZodRecord<z.ZodString, z.ZodUnion<readonly [z.ZodString, z.ZodNumber, z.ZodBoolean]>>>;
                decor: z.ZodOptional<z.ZodDiscriminatedUnion<[z.ZodObject<{
                    kind: z.ZodLiteral<"motif">;
                    id: z.ZodType<MotifId, unknown, z.core.$ZodTypeInternals<MotifId, unknown>>;
                    params: z.ZodOptional<z.ZodObject<{
                        intensity: z.ZodOptional<z.ZodEnum<{
                            subtle: "subtle";
                            normal: "normal";
                        }>>;
                    }, z.core.$strict>>;
                }, z.core.$strict>, z.ZodObject<{
                    kind: z.ZodLiteral<"silent">;
                }, z.core.$strict>], "kind">>;
                brand: z.ZodOptional<z.ZodLiteral<"none">>;
            }, z.core.$strict>>;
            comparison: z.ZodOptional<z.ZodObject<{
                face: z.ZodString;
                params: z.ZodOptional<z.ZodRecord<z.ZodString, z.ZodUnion<readonly [z.ZodString, z.ZodNumber, z.ZodBoolean]>>>;
                decor: z.ZodOptional<z.ZodDiscriminatedUnion<[z.ZodObject<{
                    kind: z.ZodLiteral<"motif">;
                    id: z.ZodType<MotifId, unknown, z.core.$ZodTypeInternals<MotifId, unknown>>;
                    params: z.ZodOptional<z.ZodObject<{
                        intensity: z.ZodOptional<z.ZodEnum<{
                            subtle: "subtle";
                            normal: "normal";
                        }>>;
                    }, z.core.$strict>>;
                }, z.core.$strict>, z.ZodObject<{
                    kind: z.ZodLiteral<"silent">;
                }, z.core.$strict>], "kind">>;
                brand: z.ZodOptional<z.ZodLiteral<"none">>;
            }, z.core.$strict>>;
            process: z.ZodOptional<z.ZodObject<{
                face: z.ZodString;
                params: z.ZodOptional<z.ZodRecord<z.ZodString, z.ZodUnion<readonly [z.ZodString, z.ZodNumber, z.ZodBoolean]>>>;
                decor: z.ZodOptional<z.ZodDiscriminatedUnion<[z.ZodObject<{
                    kind: z.ZodLiteral<"motif">;
                    id: z.ZodType<MotifId, unknown, z.core.$ZodTypeInternals<MotifId, unknown>>;
                    params: z.ZodOptional<z.ZodObject<{
                        intensity: z.ZodOptional<z.ZodEnum<{
                            subtle: "subtle";
                            normal: "normal";
                        }>>;
                    }, z.core.$strict>>;
                }, z.core.$strict>, z.ZodObject<{
                    kind: z.ZodLiteral<"silent">;
                }, z.core.$strict>], "kind">>;
                brand: z.ZodOptional<z.ZodLiteral<"none">>;
            }, z.core.$strict>>;
            data: z.ZodOptional<z.ZodObject<{
                face: z.ZodString;
                params: z.ZodOptional<z.ZodRecord<z.ZodString, z.ZodUnion<readonly [z.ZodString, z.ZodNumber, z.ZodBoolean]>>>;
                decor: z.ZodOptional<z.ZodDiscriminatedUnion<[z.ZodObject<{
                    kind: z.ZodLiteral<"motif">;
                    id: z.ZodType<MotifId, unknown, z.core.$ZodTypeInternals<MotifId, unknown>>;
                    params: z.ZodOptional<z.ZodObject<{
                        intensity: z.ZodOptional<z.ZodEnum<{
                            subtle: "subtle";
                            normal: "normal";
                        }>>;
                    }, z.core.$strict>>;
                }, z.core.$strict>, z.ZodObject<{
                    kind: z.ZodLiteral<"silent">;
                }, z.core.$strict>], "kind">>;
                brand: z.ZodOptional<z.ZodLiteral<"none">>;
            }, z.core.$strict>>;
            photo: z.ZodOptional<z.ZodObject<{
                face: z.ZodString;
                params: z.ZodOptional<z.ZodRecord<z.ZodString, z.ZodUnion<readonly [z.ZodString, z.ZodNumber, z.ZodBoolean]>>>;
                decor: z.ZodOptional<z.ZodDiscriminatedUnion<[z.ZodObject<{
                    kind: z.ZodLiteral<"motif">;
                    id: z.ZodType<MotifId, unknown, z.core.$ZodTypeInternals<MotifId, unknown>>;
                    params: z.ZodOptional<z.ZodObject<{
                        intensity: z.ZodOptional<z.ZodEnum<{
                            subtle: "subtle";
                            normal: "normal";
                        }>>;
                    }, z.core.$strict>>;
                }, z.core.$strict>, z.ZodObject<{
                    kind: z.ZodLiteral<"silent">;
                }, z.core.$strict>], "kind">>;
                brand: z.ZodOptional<z.ZodLiteral<"none">>;
            }, z.core.$strict>>;
            statement: z.ZodOptional<z.ZodObject<{
                face: z.ZodString;
                params: z.ZodOptional<z.ZodRecord<z.ZodString, z.ZodUnion<readonly [z.ZodString, z.ZodNumber, z.ZodBoolean]>>>;
                decor: z.ZodOptional<z.ZodDiscriminatedUnion<[z.ZodObject<{
                    kind: z.ZodLiteral<"motif">;
                    id: z.ZodType<MotifId, unknown, z.core.$ZodTypeInternals<MotifId, unknown>>;
                    params: z.ZodOptional<z.ZodObject<{
                        intensity: z.ZodOptional<z.ZodEnum<{
                            subtle: "subtle";
                            normal: "normal";
                        }>>;
                    }, z.core.$strict>>;
                }, z.core.$strict>, z.ZodObject<{
                    kind: z.ZodLiteral<"silent">;
                }, z.core.$strict>], "kind">>;
                brand: z.ZodOptional<z.ZodLiteral<"none">>;
            }, z.core.$strict>>;
            quote: z.ZodOptional<z.ZodObject<{
                face: z.ZodString;
                params: z.ZodOptional<z.ZodRecord<z.ZodString, z.ZodUnion<readonly [z.ZodString, z.ZodNumber, z.ZodBoolean]>>>;
                decor: z.ZodOptional<z.ZodDiscriminatedUnion<[z.ZodObject<{
                    kind: z.ZodLiteral<"motif">;
                    id: z.ZodType<MotifId, unknown, z.core.$ZodTypeInternals<MotifId, unknown>>;
                    params: z.ZodOptional<z.ZodObject<{
                        intensity: z.ZodOptional<z.ZodEnum<{
                            subtle: "subtle";
                            normal: "normal";
                        }>>;
                    }, z.core.$strict>>;
                }, z.core.$strict>, z.ZodObject<{
                    kind: z.ZodLiteral<"silent">;
                }, z.core.$strict>], "kind">>;
                brand: z.ZodOptional<z.ZodLiteral<"none">>;
            }, z.core.$strict>>;
            fact: z.ZodOptional<z.ZodObject<{
                face: z.ZodString;
                params: z.ZodOptional<z.ZodRecord<z.ZodString, z.ZodUnion<readonly [z.ZodString, z.ZodNumber, z.ZodBoolean]>>>;
                decor: z.ZodOptional<z.ZodDiscriminatedUnion<[z.ZodObject<{
                    kind: z.ZodLiteral<"motif">;
                    id: z.ZodType<MotifId, unknown, z.core.$ZodTypeInternals<MotifId, unknown>>;
                    params: z.ZodOptional<z.ZodObject<{
                        intensity: z.ZodOptional<z.ZodEnum<{
                            subtle: "subtle";
                            normal: "normal";
                        }>>;
                    }, z.core.$strict>>;
                }, z.core.$strict>, z.ZodObject<{
                    kind: z.ZodLiteral<"silent">;
                }, z.core.$strict>], "kind">>;
                brand: z.ZodOptional<z.ZodLiteral<"none">>;
            }, z.core.$strict>>;
            evidence: z.ZodOptional<z.ZodObject<{
                face: z.ZodString;
                params: z.ZodOptional<z.ZodRecord<z.ZodString, z.ZodUnion<readonly [z.ZodString, z.ZodNumber, z.ZodBoolean]>>>;
                decor: z.ZodOptional<z.ZodDiscriminatedUnion<[z.ZodObject<{
                    kind: z.ZodLiteral<"motif">;
                    id: z.ZodType<MotifId, unknown, z.core.$ZodTypeInternals<MotifId, unknown>>;
                    params: z.ZodOptional<z.ZodObject<{
                        intensity: z.ZodOptional<z.ZodEnum<{
                            subtle: "subtle";
                            normal: "normal";
                        }>>;
                    }, z.core.$strict>>;
                }, z.core.$strict>, z.ZodObject<{
                    kind: z.ZodLiteral<"silent">;
                }, z.core.$strict>], "kind">>;
                brand: z.ZodOptional<z.ZodLiteral<"none">>;
            }, z.core.$strict>>;
            hierarchy: z.ZodOptional<z.ZodObject<{
                face: z.ZodString;
                params: z.ZodOptional<z.ZodRecord<z.ZodString, z.ZodUnion<readonly [z.ZodString, z.ZodNumber, z.ZodBoolean]>>>;
                decor: z.ZodOptional<z.ZodDiscriminatedUnion<[z.ZodObject<{
                    kind: z.ZodLiteral<"motif">;
                    id: z.ZodType<MotifId, unknown, z.core.$ZodTypeInternals<MotifId, unknown>>;
                    params: z.ZodOptional<z.ZodObject<{
                        intensity: z.ZodOptional<z.ZodEnum<{
                            subtle: "subtle";
                            normal: "normal";
                        }>>;
                    }, z.core.$strict>>;
                }, z.core.$strict>, z.ZodObject<{
                    kind: z.ZodLiteral<"silent">;
                }, z.core.$strict>], "kind">>;
                brand: z.ZodOptional<z.ZodLiteral<"none">>;
            }, z.core.$strict>>;
        }, z.core.$strict>;
        ending: z.ZodObject<{
            face: z.ZodString;
            params: z.ZodOptional<z.ZodRecord<z.ZodString, z.ZodUnion<readonly [z.ZodString, z.ZodNumber, z.ZodBoolean]>>>;
            decor: z.ZodOptional<z.ZodDiscriminatedUnion<[z.ZodObject<{
                kind: z.ZodLiteral<"motif">;
                id: z.ZodType<MotifId, unknown, z.core.$ZodTypeInternals<MotifId, unknown>>;
                params: z.ZodOptional<z.ZodObject<{
                    intensity: z.ZodOptional<z.ZodEnum<{
                        subtle: "subtle";
                        normal: "normal";
                    }>>;
                }, z.core.$strict>>;
            }, z.core.$strict>, z.ZodObject<{
                kind: z.ZodLiteral<"silent">;
            }, z.core.$strict>], "kind">>;
            brand: z.ZodOptional<z.ZodLiteral<"none">>;
        }, z.core.$strict>;
    }, z.core.$strict>;
    id: z.ZodString;
    label: z.ZodOptional<z.ZodString>;
    style: z.ZodObject<{
        id: z.ZodString;
        allowCustomBackground: z.ZodOptional<z.ZodBoolean>;
        colors: z.ZodObject<{
            bg: z.ZodString;
            surface: z.ZodString;
            panel: z.ZodOptional<z.ZodString>;
            primary: z.ZodString;
            accent: z.ZodString;
            text: z.ZodString;
            muted: z.ZodString;
            border: z.ZodOptional<z.ZodString>;
            chartPalette: z.ZodArray<z.ZodString>;
            accentPool: z.ZodOptional<z.ZodArray<z.ZodString>>;
            cardStroke: z.ZodOptional<z.ZodString>;
            emphasisInk: z.ZodOptional<z.ZodString>;
            danger: z.ZodOptional<z.ZodString>;
            warning: z.ZodOptional<z.ZodString>;
            success: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>;
        fonts: z.ZodObject<{
            heading: z.ZodArray<z.ZodString>;
            body: z.ZodArray<z.ZodString>;
            mono: z.ZodOptional<z.ZodArray<z.ZodString>>;
            figure: z.ZodOptional<z.ZodArray<z.ZodString>>;
        }, z.core.$strict>;
        shape: z.ZodOptional<z.ZodObject<{
            radius: z.ZodOptional<z.ZodNumber>;
            gapScale: z.ZodOptional<z.ZodNumber>;
            typeScale: z.ZodOptional<z.ZodNumber>;
            surfaces: z.ZodOptional<z.ZodEnum<{
                filled: "filled";
                ruled: "ruled";
            }>>;
        }, z.core.$strict>>;
        defaultBackgrounds: z.ZodObject<{
            cover: z.ZodDiscriminatedUnion<[z.ZodObject<{
                kind: z.ZodLiteral<"color">;
                value: z.ZodString;
            }, z.core.$strict>, z.ZodObject<{
                kind: z.ZodLiteral<"gradient">;
                from: z.ZodString;
                to: z.ZodString;
                direction: z.ZodOptional<z.ZodEnum<{
                    tb: "tb";
                    lr: "lr";
                    diagonal: "diagonal";
                }>>;
            }, z.core.$strict>, z.ZodObject<{
                kind: z.ZodLiteral<"asset">;
                asset_id: z.ZodString;
                overlay: z.ZodOptional<z.ZodObject<{
                    color: z.ZodString;
                    opacity: z.ZodNumber;
                }, z.core.$strict>>;
                fit: z.ZodOptional<z.ZodEnum<{
                    cover: "cover";
                    contain: "contain";
                }>>;
            }, z.core.$strict>], "kind">;
            chapter: z.ZodDiscriminatedUnion<[z.ZodObject<{
                kind: z.ZodLiteral<"color">;
                value: z.ZodString;
            }, z.core.$strict>, z.ZodObject<{
                kind: z.ZodLiteral<"gradient">;
                from: z.ZodString;
                to: z.ZodString;
                direction: z.ZodOptional<z.ZodEnum<{
                    tb: "tb";
                    lr: "lr";
                    diagonal: "diagonal";
                }>>;
            }, z.core.$strict>, z.ZodObject<{
                kind: z.ZodLiteral<"asset">;
                asset_id: z.ZodString;
                overlay: z.ZodOptional<z.ZodObject<{
                    color: z.ZodString;
                    opacity: z.ZodNumber;
                }, z.core.$strict>>;
                fit: z.ZodOptional<z.ZodEnum<{
                    cover: "cover";
                    contain: "contain";
                }>>;
            }, z.core.$strict>], "kind">;
            content: z.ZodDiscriminatedUnion<[z.ZodObject<{
                kind: z.ZodLiteral<"color">;
                value: z.ZodString;
            }, z.core.$strict>, z.ZodObject<{
                kind: z.ZodLiteral<"gradient">;
                from: z.ZodString;
                to: z.ZodString;
                direction: z.ZodOptional<z.ZodEnum<{
                    tb: "tb";
                    lr: "lr";
                    diagonal: "diagonal";
                }>>;
            }, z.core.$strict>, z.ZodObject<{
                kind: z.ZodLiteral<"asset">;
                asset_id: z.ZodString;
                overlay: z.ZodOptional<z.ZodObject<{
                    color: z.ZodString;
                    opacity: z.ZodNumber;
                }, z.core.$strict>>;
                fit: z.ZodOptional<z.ZodEnum<{
                    cover: "cover";
                    contain: "contain";
                }>>;
            }, z.core.$strict>], "kind">;
            ending: z.ZodDiscriminatedUnion<[z.ZodObject<{
                kind: z.ZodLiteral<"color">;
                value: z.ZodString;
            }, z.core.$strict>, z.ZodObject<{
                kind: z.ZodLiteral<"gradient">;
                from: z.ZodString;
                to: z.ZodString;
                direction: z.ZodOptional<z.ZodEnum<{
                    tb: "tb";
                    lr: "lr";
                    diagonal: "diagonal";
                }>>;
            }, z.core.$strict>, z.ZodObject<{
                kind: z.ZodLiteral<"asset">;
                asset_id: z.ZodString;
                overlay: z.ZodOptional<z.ZodObject<{
                    color: z.ZodString;
                    opacity: z.ZodNumber;
                }, z.core.$strict>>;
                fit: z.ZodOptional<z.ZodEnum<{
                    cover: "cover";
                    contain: "contain";
                }>>;
            }, z.core.$strict>], "kind">;
        }, z.core.$strict>;
    }, z.core.$strict>;
    brand: z.ZodOptional<z.ZodObject<{
        suppressFooterOnCardContent: z.ZodOptional<z.ZodBoolean>;
        suppressFooterRule: z.ZodOptional<z.ZodBoolean>;
        suppressFooterMeta: z.ZodOptional<z.ZodBoolean>;
    }, z.core.$strict>>;
    occasions: z.ZodOptional<z.ZodArray<z.ZodEnum<{
        education: "education";
        entertainment: "entertainment";
        fashion: "fashion";
        finance: "finance";
        luxury: "luxury";
        tech: "tech";
        business: "business";
        marketing: "marketing";
        sustainability: "sustainability";
        government: "government";
        health: "health";
        kids: "kids";
        startup: "startup";
        museum: "museum";
        sales: "sales";
        institutional: "institutional";
        culture: "culture";
        keynote: "keynote";
        editorial: "editorial";
        event: "event";
        career: "career";
        review: "review";
    }>>>;
    identity: z.ZodOptional<z.ZodEnum<{
        low: "low";
        medium: "medium";
        high: "high";
    }>>;
    story: z.ZodOptional<z.ZodObject<{
        name: z.ZodString;
        story: z.ZodString;
        positioning: z.ZodString;
        audience: z.ZodString;
        notFor: z.ZodString;
        lineage: z.ZodOptional<z.ZodString>;
    }, z.core.$strict>>;
    emphasis: z.ZodOptional<z.ZodEnum<{
        underline: "underline";
        tint: "tint";
        pad: "pad";
    }>>;
}, z.core.$strict>;
type Menu = z.infer<typeof MenuSchema>;
type ThemeFile = z.infer<typeof ThemeFileSchema>;
/**
 * Internal declaration accepted from `builtin/`. It is intentionally a
 * superset of the public complete-theme contract: the theme-wide `motif`
 * anchor stays here because the public contract expresses decoration per
 * menu entry only.
 */
interface BuiltinThemeDeclaration {
    version: 2;
    id: (typeof BUILTIN_THEME_IDS)[number];
    label: string;
    style: StyleTokens;
    brand?: BrandConfig;
    occasions?: readonly Occasion[];
    identity?: "low" | "medium" | "high";
    /** The theme's design story. */
    story?: DesignStory;
    emphasis?: EmphasisTreatment;
    menu: Menu;
    motif?: {
        id: MotifId;
        params?: {
            intensity?: "subtle" | "normal";
        };
    };
}

/**
 * Layout registry (W2 task 1, spec §3/§6/§8): an explicit, statically-checked
 * description of what the render chain's 105 standard layouts and 2
 * page-level image takeovers already draw. This is a metadata layer only.
 * It formalizes today's implicit page structure (layout JSX + the
 * FullSlideSvg takeover dispatch) into named `slots`, it does not change any
 * drawing code.
 *
 * **Aggregator, not author (src domain reorg wave 1, task T1d).** Every
 * individual `LayoutDefinition` used to live here as a literal Record entry.
 * Each one now lives beside the layout JSX it describes instead — an
 * `export const layoutDef: LayoutDefinition` at the bottom of the matching
 * `layouts/*.tsx` file, or one of 4 uniquely-named exports at the bottom
 * of `image-pages.tsx` for the takeovers (one file implements all 4, so they
 * can't share the uniform `layoutDef` name the 154 single-layout
 * files use) — so "take one layout away whole" is a single-file operation
 * instead of a two-file archaeology dig. This file's own job is now purely
 * computational aggregation: import every `layoutDef`, assemble the five
 * Records below (`{ [def.id]: def }`-style, preserving the key order the
 * pre-migration literals held — new members still go on the end, a
 * discipline that outlived the `weightedPickBySeed` lottery it once fed), merge them into
 * `LAYOUT_REGISTRY`, and keep every type and query function
 * (`getLayout`/`layoutsForSlideType`) that reads the result. Never a re-export relay
 * — every line below either constructs a Record or queries/validates one
 * (this wave's aggregator discipline).
 *
 * Source of truth for each definition's own content: the layout file it
 * now lives in, `.issues/notes/engineering-history.md`
 * (the W2 pre-flight inventory), plus a direct re-read of the layout file
 * itself — where the inventory's summary and the code disagreed, the code
 * won (see the W2 task report for the one confirmed case: image-annotate).
 *
 * Slot `accepts` convention used throughout every `layoutDef`:
 *  - `[]` (empty array): the slot is *not* fed by an authored component
 *    — it's derived straight from slide-level scalar fields (`slide.heading`,
 *    `slide.subheading`), `ir.meta.*` (organization/date/version/contact/
 *    copyright/confidentiality), or pure computed geometry (chapter-number
 *    watermarks, rail progress dots, decorative motifs inline in the
 *    layout file). There is nothing here for an author to place.
 *  - `"any"`: the slot renders whatever `Component`s it's handed, unfiltered
 *    (`SvgContent`'s body, bento's grid, stacked-poster's hero/strip).
 *  - a literal component-type list: the slot requires that specific component
 *    type (`image`, `bullets`) — used only by the takeover layouts, which
 *    `Array.find` a specific component type out of `slide.components`.
 */

type SlideType = "cover" | "chapter" | "content" | "ending";

type MotifId = "banner-motif" | "rail-motif" | "poster-motif" | "constellation-motif" | "corner-ornament-motif" | "tone-adaptive-motif" | "rally-motif" | "homeroom-motif" | "ink-motif" | "luxe-motif" | "bulletin-motif" | "clinic-motif" | "almanac-motif" | "ember-motif" | "vermilion-motif" | "crayon-motif" | "lecture-motif" | "swiss-motif" | "memo-motif" | "gauge-motif" | "crayonbox-motif" | "folio-motif" | "proposal-motif" | "runway-motif" | "museum-motif" | "stage-motif" | "profile-motif" | "recap-motif";

/**
 * The 23 canonical theme ids, registered/renderable（产品口径 23 套主题、
 * 23 个 id）。命名规矩：id、label、story.name 一律命名腔调或体裁，
 * 不命名行业、职能、受众或组织类型（见 `design-story.ts`；九个场景名
 * 已在改名批次里一次性换掉，旧 id 直接硬错并报出新名，见
 * `retired-ids.ts`）（brief Brief / bulletin Bulletin /
 * thesis Thesis / ledger Ledger / rally Rally /
 * homeroom Homeroom / ink Ink Wash / terminal Terminal /
 * runway Runway / journal Editorial Journal / luxe Luxe /
 * clinic Clinic——themes-16 wave task T1
 * 新增第 14 个 / almanac Almanac——themes-16 wave task T2 新增
 * 第 15 个 / ember Ember——themes-16 wave task T3 新增第 16 个 /
 * vermilion Official Report——gov-theme wave 新增第 17 个，庄重公务汇报语域，
 * 第一个从立项即以中文语域为主的主题 / crayon Crayon——低龄教育
 * 蜡笔卡纸 /
 * museum Museum——博物·棕黑厅堂衬线铜金，2026-08-21 鹦鹉站气质立项 /
 * stage Keynote Stage——黑场·冷玄黑无框发布会演讲，2026-08-21 huashu 风格库
 * Top 5 第 3 / lecture Lecture Hall——黑板夜校，2026-08-21
 * 大学/成人课程夜校板 / swiss Swiss Institutional——冷白制度，机构年报 / 政策汇报 /
 * 审计交付，2026-08-21 wave7 / memo Decision Memo——打字机决定，备忘录 /
 * proposal Proposal——递到客户管理层手里的提案书 / profile Profile——
 * 一个人向评委介绍自己的人物专访 / recap Recap——一个人向评审交代自己这一年
 * 的述职账本）。
 * 2026-10 合并退役三家：arena、playbill 并入 rally，heritage 并入 luxe。
 * 旧 id 不在本表，validate 与查名把它读成并入的主题并给警告，见
 * `retired-ids.ts` 的 `FOLDED_THEME_IDS`。resolveThemeId 本身对未知 id
 * 一律硬错。
 */
declare const CANONICAL_THEME_IDS: readonly ["brief", "bulletin", "thesis", "ledger", "rally", "homeroom", "ink", "terminal", "runway", "journal", "luxe", "clinic", "almanac", "ember", "vermilion", "crayon", "museum", "stage", "lecture", "swiss", "memo", "proposal", "profile", "recap"];
type CanonicalThemeId = (typeof CANONICAL_THEME_IDS)[number];

/**
 * A theme = distributable bundle: `style` (style tokens) + `brand` (brand
 * frame) + affinity tags (filled in W4).
 *
 * `id` is a plain `string`, not `CanonicalThemeId` — the 24 built-ins satisfy
 * this (`CanonicalThemeId` is a subtype of `string`), but `registerTheme`
 * below (W3 task 4's SDK registration seam) must also accept ids outside that
 * closed union.
 */
interface ThemeDefinition {
    id: string;
    label?: string;
    style: StyleTokens;
    brand: BrandConfig;
    tags: readonly string[];
    occasions?: readonly Occasion[];
    identity?: "low" | "medium" | "high";
    /**
     * The theme's design story: the voice it speaks in, when to reach for it,
     * and when not to. Public copy — the gallery and the docs read it.
     */
    story?: DesignStory;
    /** How this theme strikes a `**marked**` run. `undefined` equals `"tint"`. */
    emphasis?: EmphasisTreatment;
    /** The theme's semantic page menu: one face per served kind. Authoritative. */
    menu: Menu;
    /** One registered motif id. `undefined` means the theme has no motif. */
    motif?: MotifId;
    motifParameters?: {
        intensity?: "subtle" | "normal";
    };
}
/**
 * Register a theme for the life of the process (SDK seam, not the v0.4
 * distribution protocol). This is process-level configuration, the way an
 * embedder extends the factory preset shelf once at startup. It is not
 * per-request state: a theme that belongs to one deck, one request, or one
 * file on disk is compiled with {@link compileThemeDefinition} and passed
 * by value as the `theme` option of `validateIr`, `renderSlideSvg`,
 * `generatePptx`, `auditDeck`, and `buildAssetBrief` instead.
 *
 * The input is a complete v2 theme file and nothing else: one
 * self-contained declaration carrying style, brand, and the menu. There is
 * no partial completeness, no inherited structure, and no registry-wide
 * default pool to fall back on.
 *
 * Hard gates, in order:
 *
 * - the file must parse against {@link ThemeFileSchema} (which already
 *   rejects a `style.id` that disagrees with `id`, and requires a
 *   non-empty content-kind subset).
 * - `id` must not collide with a built-in or an already-registered theme.
 * - `style.colors.text`/`style.colors.muted` must each clear the
 *   {@link CONTRAST_FLOOR} against a {@link CONTRAST_CHECKED_SLIDE_TYPES}
 *   slide type's own resolved default background — see
 *   {@link assertContrastFloor}.
 * - every menu entry must name a registered layout valid for that page
 *   type, and every parameter it sets must be declared by that face and
 *   inside the face's own declared bounds ({@link assertMenuContract}).
 *
 * Also `console.warn`s (never throws) once for each of `style.fonts.heading`/
 * `style.fonts.body` that resolves to a face with no exact width table — see
 * {@link warnUnmeasuredFace}'s own doc comment. Fires only for a
 * registration that clears every check above.
 *
 * Once registered, the theme participates in `getInstalledThemeIds`,
 * `getThemeDefinition`, and `themes/index.ts`'s `resolveStyle`: the shelf
 * `resolveIrTheme` reads when an entry point is handed an id and no
 * definition. A built-in id can never be shadowed here, and a registered id
 * is never replaced. There is no uninstall outside the test-only reset.
 */
declare function registerTheme(input: unknown): void;
/**
 * Compile a complete v2 theme file into a definition the render chain can
 * carry by value. Every gate `registerTheme` runs is run here (schema,
 * contrast floor, menu contract, unmeasured-font warning), and nothing is
 * written anywhere: the caller owns the returned object and hands it to
 * `validateIr`, `renderSlideSvg`, `generatePptx`, and friends as their
 * `theme` option. The CLI's name lookup uses this for a deck or workspace
 * theme file, so two requests in one process can each hold a different
 * definition under the same id without seeing each other.
 */
declare function compileThemeDefinition(input: unknown): ThemeDefinition;
/** Every installed theme id in deterministic lexical order. */
declare function getInstalledThemeIds(): readonly string[];
/**
 * Resolve a theme id to its full definition — an SDK-registered theme first,
 * then the built-in shelf. An id that is neither throws (`resolveThemeId`),
 * so a misspelled theme surfaces at once instead of rendering as some other
 * theme.
 *
 * Only `resolveIrTheme` (`./resolve-ir-theme.ts`) calls this on the render
 * path, and only for a deck that supplied no definition of its own — plus
 * the theme catalog queries (`kind-components.ts`, the gallery), which ask
 * about installed themes rather than about a bound deck. A deck or
 * workspace theme file never goes through here: the CLI compiles it and
 * passes the definition by value, so this table only ever answers for
 * factory presets and process-level `registerTheme` calls.
 */
declare function getThemeDefinition(id: string): ThemeDefinition;

type JsonSchemaDocument = Record<string, unknown> & {
    $defs?: Record<string, unknown>;
};
/** JSON Schema for the IR — feed this to a model before it writes IR. */
declare function irJsonSchema(): JsonSchemaDocument;
/**
 * JSON Schema for one component (`pptwise schema --component <type>`): the
 * component's own object schema at the top, plus only the `$defs` it refers
 * to. Cut from the same emitted schema as {@link irJsonSchema}.
 */
declare function componentJsonSchema(type: string): JsonSchemaDocument;

interface ValidationIssue {
    path: string;
    message: string;
    /** 1-based slide number when the issue is scoped to a slide. */
    page?: number;
    /**
     * The offending slide's own `id` (`Slide.id`, `ir/index.ts`) — W5
     * whole-branch review finding 2: the README already claimed "validation
     * error messages reference [a slide] by [its] id"; this is what makes
     * that true. Set by every page-scoped issue producer
     * ({@link checkThemeMenuFaces}, {@link checkBoundaryPageContent},
     * {@link checkBoundarySlotCapacity}, {@link checkBoundaryItemCapacity},
     * the content-quality-gate translation in {@link validateIr}, and
     * {@link checkDuplicateSlideIds})
     * when the slide in question has an `id` — absent when the slide has
     * none (bare, pre-W5 IR) or the issue is deck-level, not scoped to any
     * single slide. {@link formatIssues} appends it in parens after the page
     * number.
     */
    slideId?: string;
}
interface ValidateResult {
    ok: boolean;
    ir?: PptxIR;
    errors: ValidationIssue[];
    /**
     * Human-readable "`path`: `alias` → `canonical`" entries for every
     * deterministic field-alias rewrite `validateIr` applied before parsing
     * (W5 task 4, `ir/field-aliases.ts`'s `normalizeComponentAliases`) — e.g. a
     * kpi item's `title` silently adopted as `label`. Present only when at
     * least one rewrite happened; informational, never gates `ok` on its own.
     */
    normalized?: string[];
    /**
     * Backward-compatible addition (borrow wave, Task 2 — dual-threshold
     * severity recalibration): warn-severity {@link checkIrQuality} findings
     * (editorial-budget codes — `missing_heading`/`long_heading`/`density`/
     * `bullets_overflow`/`bullet_item_long`/`big_number_no_kpi`) plus
     * {@link checkAssetReferences}'s dangling-`asset_id` findings (borrow wave,
     * Task 2, B5 — a reference to an `assets.images` key that doesn't exist),
     * formatted the same shape {@link formatIssues} already prints for `errors`
     * (page/id/path all included). Present only when at least one warn-severity
     * finding exists, and never gates `ok` on its own — that is exactly what
     * moved these findings off `errors` and onto here. Can be present alongside
     * a failing (`ok:false`) result too, whenever `checkIrQuality`/
     * `checkAssetReferences` themselves ran (an *earlier* hard gate — schema,
     * theme id, theme menu, full-body exclusivity, boundary-page
     * content, duplicate ids, asset bytes, narrative — short-circuits before
     * either runs at all, so a deck rejected by one of those never reaches
     * this field either way, see `validateIr`'s own body for the exact gate
     * order). {@link formatWarnings} renders this array as CLI-ready
     * `"warning: ..."` lines.
     */
    warnings?: ValidationIssue[];
    /**
     * The theme this deck resolved to, present on every `ok: true` result:
     * the definition the caller supplied, or the installed theme
     * `ir.theme.id` names. Validation has to resolve it to check the menu, so
     * it hands the object back and a caller that goes on to render (see
     * `api.ts`'s `generatePptx`) passes this down instead of resolving the
     * same id a second time. Absent on failure — nothing was resolved.
     */
    theme?: ThemeDefinition;
    /**
     * Set on an `ok` result for a deck built under a theme other than the
     * one its pages were written for (`validateIr`'s `writtenFor`), when that
     * theme leaves anything off or draws a page short: the theme they were
     * written for. `ir` is then the deck as this theme draws it,
     * with what its faces cannot take left off, and a page may be drawn
     * short. Each is named in `warnings`, and an export of this `ir` is told
     * so (`allowDroppedContent`).
     */
    switchedFrom?: string;
}
/**
 * Validate raw JSON against the IR schema, then — once it parses — resolve
 * `narrative` (`resolveNarrative`, spec §5: an unrecognized preset name is a
 * `narrative`-path error, page-less) and run the content-quality gate
 * (`checkIrQuality`, passed the resolved axes) against the parsed IR. Every
 * hard-gate stage (schema, theme id, theme menu, full-body
 * exclusivity, boundary-page content, duplicate ids, asset bytes, narrative)
 * must pass for `ok: true`, same as before. Quality findings are reported
 * the same way as schema errors (page-scoped, 1-based).
 *
 * Dual-threshold severity (borrow wave, Task 2 — recalibrated from the prior
 * "any finding blocks" design): `checkIrQuality`'s own "warn" vs "error" tag
 * is now respected, not flattened. Only "error"-severity findings
 * (`empty_deck`, `bullet_item_overflow` — content genuinely lost: an empty
 * deck, or a bullet item long enough to hit `bullets.tsx`'s MIN_FONT floor
 * and actually get truncated) gate `ok`. "warn"-severity findings — the
 * editorial-budget codes (`missing_heading`/`long_heading`/`density`/
 * `bullets_overflow`/`bullet_item_long`/`big_number_no_kpi`) — surface on
 * {@link ValidateResult.warnings} instead: visible to every caller (the SDK,
 * the CLI's `validate`/`render` pre-flight), never blocking. This reverses
 * the prior posture (this comment used to read "any finding blocks... not
 * only 'error'-severity ones") because the evidence behind it did not hold:
 * a boundary scan (borrow-wave fact-report, Q3) found the editorial bullets
 * threshold blocking content roughly 3.5x below where `bullets.tsx`'s own
 * render safety net (2-line wrap, shrink to a 14px floor) actually starts
 * losing characters — so the hard gate was rejecting deck content that
 * would have rendered with zero visible defect, and a tight hard gate on an
 * editorial (not geometric) threshold taught truncate-content-to-pass
 * workarounds rather than catching real loss. `generatePptx`'s default path
 * inherits this unchanged (`if (!v.ok) throw`) — it already only ever
 * blocked on `ok`, never inspected `errors`/`warnings` directly.
 *
 * Before any of that, two deterministic pre-parse rewrite passes run, each
 * threading its rewrite notes onto `ValidateResult.normalized` on *every*
 * return path below via `withNormalized`, success or failure alike — neither
 * ever gates `ok` on its own:
 *  - {@link normalizeComponentAliases} (W5 task 4): the component
 *    field-name synonym rescue (kpi `title`→`label`, blockquote
 *    `content`→`text`,
 *    …), scoped to `slides[]`. Only rewrites where the canonical key is
 *    absent, so the schema parse below never sees an alias as an
 *    "unrecognized key" in the first place.
 *  - {@link normalizeNarrativeShape} (`./narrative`, T0b bench-evidence fix
 *    2 — see its own doc comment for the full rationale): the root-level
 *    `narrative: {id: <preset>}` shape rescue. A model that just wrote
 *    `theme: {id: "brief"}` a few lines above pattern-matches the same
 *    wrapper shape onto `narrative`; this rewrites it to the bare preset
 *    string `resolveNarrative`'s string branch actually expects. Fires only
 *    when `id` is the object's sole narrative-relevant key (none of
 *    strategy/pacing/audience alongside it) — a mixed shape stays
 *    unrescued, ambiguous, and hard-errors exactly as it did before this
 *    pass existed.
 *
 * Both are the same class of fix — a weak-model *synonym* rescue (a name
 * drift for the component-alias pass, a *shape* drift for the narrative
 * pass) — which is the actual boundary the next paragraph's "no
 * old-vocabulary rescue" draws, not "no rewrite ever touches `narrative`."
 *
 * IR versions 1 through 4 are rejected before normalization or schema
 * parsing. The error states the current v5 contract and intentionally offers
 * no compatibility rewrite or migration command.
 */
declare function validateIr(input: unknown, opts?: {
    theme?: ThemeDefinition;
    /**
     * Where a picture the deck names but nobody supplied belongs, without its
     * extension: a deck project's `assets/<id>`, as the CLI shows the path.
     * With it, a dangling `asset_id` warning says where to put the file.
     * The browser has no such folder and leaves it out.
     */
    missingAssetPath?: (assetId: string) => string;
    /**
     * Skip the content-page drawn gate (`checkContentPagesDrawn`), and only
     * that one: the export's `allowDroppedContent` opt-in, which has to reach
     * the export to mean anything. Nothing else should set it.
     */
    allowDroppedContent?: boolean;
    /**
     * The theme this deck's pages were written for, when the caller knows
     * it (a deck project's build reads it from the deck's workspace
     * folder). When it names a theme other than the one the deck binds, what
     * the bound theme's faces cannot take is left off with a warning instead
     * of refusing the deck (`giveWayToTheme`), and a content page drawn
     * short is a warning too. The returned `ir` is the one drawn.
     */
    writtenFor?: string;
}): ValidateResult;
/**
 * `"page 2 (p-kpi) — path: message"` when the issue carries both a `page`
 * and a `slideId` (W5 whole-branch review finding 2 — the README's own
 * claim that a validation error "references [a slide] by [its] id", made
 * true) — the parenthesized id is appended only alongside a `page` number,
 * never on its own: a deck-level issue that happens to set a representative
 * `slideId` with no `page` ({@link checkDuplicateSlideIds} above) keeps its
 * pre-existing, unchanged format. Every other combination — `page` with no
 * `slideId` (an id-less slide), or neither — is byte-identical to before
 * this task.
 */
declare function formatIssues(errors: ValidationIssue[]): string;
interface ThemeInfo {
    id: string;
    label: string;
    colors: Record<string, unknown>;
}
/** Built-in theme catalog with labels and style color tokens. */
declare function listThemes(): ThemeInfo[];

/**
 * Public API surface: validateIr's own logic lives in `./validate-core`
 * (P2 browser-distribution wave, task 1 — see that file's own doc comment
 * for why) and is re-exported below unchanged, so every existing consumer
 * of this module keeps working exactly as before. `renderSlideSvg` and
 * `generatePptx` stay defined here — this is the one file allowed to reach
 * into `./render/render-slide` and `./pptx/generate` (react-dom/server, jszip,
 * pptxgenjs).
 */

/**
 * Options shared by the entry points that draw a page. `theme` is the bound
 * theme's definition, passed by value from whoever resolved it (the CLI's
 * name lookup, or an SDK caller's own object). Omitted, `ir.theme.id` names
 * a built-in or an SDK-registered theme, and an unknown id is an error.
 * Either way the entry point resolves it once (`resolveIrTheme`) and the
 * render chain below only ever sees the definition.
 */
interface RenderThemeOptions {
    theme?: ThemeDefinition;
}
/** Render a single slide to standalone SVG markup (preview / self-check). */
declare function renderSlideSvg(ir: PptxIR, slideIndex: number, opts?: RenderThemeOptions): string;
/**
 * Full pipeline: validate → SVG → DrawingML → animation patches → pptx bytes.
 *
 * Two export gates, both "refuse to hand over a deliverable the caller
 * cannot see is broken, unless they say they know": `draft` skips the
 * unfilled-placeholder gate above, `allowDroppedContent` skips the
 * content-drop gate (`checkContentDropGate` in `./pptx/generate` — it lives
 * there because only a real layout can answer it, and the export renders
 * every slide there already).
 *
 * **Why `validateIr` answers the drop question too** (decided 2026-10-10,
 * reversing the 2026-09-04 decision that kept validate structural).
 * validate now draws every content page as the export will and refuses one
 * that would lose anything (`checkContentPagesDrawn` in `./validate-core`),
 * so a deck validate passes is one the export draws whole. That made the
 * opt-in unreachable, since this function validates first. So
 * `allowDroppedContent` is handed to `validateIr` as well, where it skips
 * that one gate and nothing else, and the deck reaches the export gate
 * whose whole purpose is to let a caller through, naming what is lost.
 */
declare function generatePptx(input: unknown, opts?: {
    draft?: boolean;
    allowDroppedContent?: boolean;
} & RenderThemeOptions): Promise<Uint8Array>;

interface KindThemeOffer {
    /** The face the theme menu binds to this kind. */
    face: string;
    /** Component types that face draws, in vocabulary order. */
    components: readonly string[];
    /**
     * Present when the menu lacks the kind: the offered kinds a page of it is
     * drawn as, nearest first (`./render/kind-landing.ts`). `face` is then the
     * first one's face, and `components` covers every one of them, since a
     * page takes the first whose face takes what it carries.
     */
    drawnAs?: readonly PageKind$1[];
}
interface KindComponents {
    kind: PageKind$1;
    /** Union over `themes`, in vocabulary order. */
    components: readonly string[];
    /** One entry per theme that offers the kind. */
    themes: Record<string, KindThemeOffer>;
}
interface KindComponentsOptions {
    /**
     * Restrict the answer to one theme: a resolved definition (a deck or
     * workspace file, passed by value), or the id of a built-in or SDK-registered
     * theme.
     */
    theme?: string | ThemeDefinition;
    /**
     * Themes beyond the built-in shelf and the SDK registry that the caller has
     * already resolved, such as the CLI's installed content pack themes. Only
     * consulted when no single `theme` is named: they join the union.
     */
    extraThemes?: readonly ThemeDefinition[];
}
/** The components a kind may hold, per theme and as a union. */
declare function componentsForKind(kind: string, options?: KindComponentsOptions): KindComponents;
/**
 * JSON Schema for one component on a page of `kind` (`pptwise schema --kind`):
 * the legal component list, the theme faces behind it, a `oneOf` over those
 * components, and only the `$defs` they need.
 *
 * A face that draws no authored component leaves the list empty. No
 * built-in face does since mono-bleed left with playbill, but a face may
 * declare a body that takes nothing. Draft 2020-12 requires a non-empty
 * `oneOf`, so that case is written as `not: {}`, the schema that matches
 * nothing, with a description saying why.
 */
declare function kindJsonSchema(kind: string, options?: KindComponentsOptions): JsonSchemaDocument;

/** One shelf entry: what a picker needs to choose a starting point. */
interface ThemePresetSummary {
    readonly id: CanonicalThemeId;
    readonly label: string;
    readonly occasions: readonly Occasion[];
    readonly identity: IdentityStrength;
}
/** Every preset on the shelf, in canonical order. */
declare const THEME_PRESETS: readonly ThemePresetSummary[];
/** Whether `id` names a factory preset. */
declare function isThemePresetId(id: string): id is CanonicalThemeId;
/** One shelf entry by id. Unknown ids are an error, never a silent fallback. */
declare function getThemePreset(id: string): ThemePresetSummary;
/**
 * Copy one preset under a new id. The result shares nothing with the
 * preset: style tokens, brand, and menu are all fresh objects, and the
 * theme-wide motif anchor has been written into the menu entries.
 *
 * `emphasis` travels with the copy. It is theme identity, not decoration:
 * brief swipes a marker pad behind a `**marked**` run and lecture
 * chalks a line under it, so a copy that lost the field silently reverted
 * both to the plain accent tint.
 *
 * `targetId` may equal a preset id. That is how a freeze copy keeps the
 * bound name while the file shadows the factory shelf.
 */
declare function copyThemePreset(presetId: string, targetId: string): BuiltinThemeDeclaration;

type BrandSlot = "primary" | "accent";

/** Where one asked-for color ended up. */
interface PlacedColor {
    /** The color asked for. */
    color: string;
    /** The slot it was written into, or null when it is in the chart only. */
    slot: BrandSlot | null;
    /** What was written into the slot: the color itself unless `lifted` says otherwise. */
    written: string | null;
    /** The slot fills a page as a ground, and words set on it take an ink that reads on it. */
    ground: boolean;
    /** The slot is mostly fields of color (bars, blocks) rather than marks, so it takes the color as it is. */
    fills?: boolean;
    /** Its lightness was moved to reach `need` on the ground, where it read `ratio`. */
    lifted?: {
        need: number;
        ratio: number;
    };
    /** The face kept the theme's own color, and why: this color does not read in its headings, or the pages work the face into a field that would not look like this color. */
    passedOver?: {
        slot: BrandSlot;
    } & Refusal;
    /** Why it has no slot. */
    noSlot?: "neutral" | "one-color" | "headings" | "repainted";
    /** The brand has no chroma (a grey, a black or a white), so the theme comes out grey: it was asked for no colored brand. */
    neutral?: true;
    /** The chart series drawn in it: the color as it is, since a chart fills its bars and areas with it. Null when the chart stays one color among inks and leaves it out. */
    chart: string | null;
}
/** Why a slot will not take a color. */
type Refusal = {
    why: "headings";
    need: number;
    ratio: number;
} | {
    why: "repainted";
    painted: string;
    distance: number;
};
interface BrandPlacement {
    /** The theme's ground every ratio is measured against. */
    bg: string;
    /** The theme's measured face. */
    face: BrandSlot;
    brand: PlacedColor;
    second?: PlacedColor;
}

/** The complete v2 theme-file shape {@link extractBrandTheme} writes. */
type BrandThemeFile = ThemeFile;
interface ExtractBrandThemeOptions {
    /** Theme id — defaults to a slug of {@link ExtractBrandThemeOptions.label},
     *  or (when that's also absent) a slug of the source theme part's own
     *  `<a:clrScheme name="…">`. The CLI (`pptwise brand extract`) always
     *  passes one explicitly (`--id`, or a slug of the `-o` filename — 裁定
     *  4) — this default only ever fires for a bare SDK caller. */
    id?: string;
    /** Human-readable label — defaults to the source theme part's own
     *  `<a:clrScheme name="…">`. */
    label?: string;
    /** The theme repainted around the brand: a built-in theme id, or a
     *  complete v2 theme file. Default `"bulletin"`, the business theme that
     *  carries a brand color best, as given and on its face. */
    from?: string | ThemeFile;
    /** Set the template's Latin fonts ahead of the theme's own. Off by
     *  default: the theme keeps its fonts, and the template's East Asian faces
     *  are never used. */
    brandFonts?: boolean;
}
/** What {@link extractBrandTheme} returns. */
interface BrandThemeResult {
    /** The repainted theme, a complete v2 file under the new id and label. */
    file: BrandThemeFile;
    /** Where the brand color and the second color went, and why. */
    placement: BrandPlacement;
    /** What became of the template's fonts under `brandFonts`: a role the
     *  template names no font for, or a font the slides cannot set as named.
     *  Empty without `brandFonts`. */
    fontNotes: string[];
}
/**
 * Repaint a theme around the brand color of a template, from the raw bytes
 * of a `.thmx`/`.potx`/`.pptx` file (only its theme part is read). The
 * theme keeps its ground, text, surface, menu, and fonts. Its colored
 * tokens move to the brand by the rules `../brand/brand-regen.ts` sets out.
 * Deterministic: the same bytes and options always give the same theme.
 *
 * Rendering the theme to find which slot it shows most needs a platform
 * (`installPlatform`), as any other render does.
 *
 * Throws {@link PptwiseError} when the package has no theme part, when the
 * theme part names no accent color, and when the repainted theme would fail
 * a contrast floor.
 */
declare function extractBrandTheme(bytes: Uint8Array | ArrayBuffer, opts?: ExtractBrandThemeOptions): Promise<BrandThemeResult>;

/** Kept as the existing exported symbol, now pointing at the unified v2 contract. */
declare const BrandThemeFileSchema: zod.ZodObject<{
    version: zod.ZodLiteral<2>;
    menu: zod.ZodObject<{
        cover: zod.ZodObject<{
            face: zod.ZodString;
            params: zod.ZodOptional<zod.ZodRecord<zod.ZodString, zod.ZodUnion<readonly [zod.ZodString, zod.ZodNumber, zod.ZodBoolean]>>>;
            decor: zod.ZodOptional<zod.ZodDiscriminatedUnion<[zod.ZodObject<{
                kind: zod.ZodLiteral<"motif">;
                id: zod.ZodType<MotifId, unknown, zod_v4_core.$ZodTypeInternals<MotifId, unknown>>;
                params: zod.ZodOptional<zod.ZodObject<{
                    intensity: zod.ZodOptional<zod.ZodEnum<{
                        subtle: "subtle";
                        normal: "normal";
                    }>>;
                }, zod_v4_core.$strict>>;
            }, zod_v4_core.$strict>, zod.ZodObject<{
                kind: zod.ZodLiteral<"silent">;
            }, zod_v4_core.$strict>], "kind">>;
            brand: zod.ZodOptional<zod.ZodLiteral<"none">>;
        }, zod_v4_core.$strict>;
        chapter: zod.ZodObject<{
            face: zod.ZodString;
            params: zod.ZodOptional<zod.ZodRecord<zod.ZodString, zod.ZodUnion<readonly [zod.ZodString, zod.ZodNumber, zod.ZodBoolean]>>>;
            decor: zod.ZodOptional<zod.ZodDiscriminatedUnion<[zod.ZodObject<{
                kind: zod.ZodLiteral<"motif">;
                id: zod.ZodType<MotifId, unknown, zod_v4_core.$ZodTypeInternals<MotifId, unknown>>;
                params: zod.ZodOptional<zod.ZodObject<{
                    intensity: zod.ZodOptional<zod.ZodEnum<{
                        subtle: "subtle";
                        normal: "normal";
                    }>>;
                }, zod_v4_core.$strict>>;
            }, zod_v4_core.$strict>, zod.ZodObject<{
                kind: zod.ZodLiteral<"silent">;
            }, zod_v4_core.$strict>], "kind">>;
            brand: zod.ZodOptional<zod.ZodLiteral<"none">>;
        }, zod_v4_core.$strict>;
        content: zod.ZodObject<{
            points: zod.ZodOptional<zod.ZodObject<{
                face: zod.ZodString;
                params: zod.ZodOptional<zod.ZodRecord<zod.ZodString, zod.ZodUnion<readonly [zod.ZodString, zod.ZodNumber, zod.ZodBoolean]>>>;
                decor: zod.ZodOptional<zod.ZodDiscriminatedUnion<[zod.ZodObject<{
                    kind: zod.ZodLiteral<"motif">;
                    id: zod.ZodType<MotifId, unknown, zod_v4_core.$ZodTypeInternals<MotifId, unknown>>;
                    params: zod.ZodOptional<zod.ZodObject<{
                        intensity: zod.ZodOptional<zod.ZodEnum<{
                            subtle: "subtle";
                            normal: "normal";
                        }>>;
                    }, zod_v4_core.$strict>>;
                }, zod_v4_core.$strict>, zod.ZodObject<{
                    kind: zod.ZodLiteral<"silent">;
                }, zod_v4_core.$strict>], "kind">>;
                brand: zod.ZodOptional<zod.ZodLiteral<"none">>;
            }, zod_v4_core.$strict>>;
            list: zod.ZodOptional<zod.ZodObject<{
                face: zod.ZodString;
                params: zod.ZodOptional<zod.ZodRecord<zod.ZodString, zod.ZodUnion<readonly [zod.ZodString, zod.ZodNumber, zod.ZodBoolean]>>>;
                decor: zod.ZodOptional<zod.ZodDiscriminatedUnion<[zod.ZodObject<{
                    kind: zod.ZodLiteral<"motif">;
                    id: zod.ZodType<MotifId, unknown, zod_v4_core.$ZodTypeInternals<MotifId, unknown>>;
                    params: zod.ZodOptional<zod.ZodObject<{
                        intensity: zod.ZodOptional<zod.ZodEnum<{
                            subtle: "subtle";
                            normal: "normal";
                        }>>;
                    }, zod_v4_core.$strict>>;
                }, zod_v4_core.$strict>, zod.ZodObject<{
                    kind: zod.ZodLiteral<"silent">;
                }, zod_v4_core.$strict>], "kind">>;
                brand: zod.ZodOptional<zod.ZodLiteral<"none">>;
            }, zod_v4_core.$strict>>;
            comparison: zod.ZodOptional<zod.ZodObject<{
                face: zod.ZodString;
                params: zod.ZodOptional<zod.ZodRecord<zod.ZodString, zod.ZodUnion<readonly [zod.ZodString, zod.ZodNumber, zod.ZodBoolean]>>>;
                decor: zod.ZodOptional<zod.ZodDiscriminatedUnion<[zod.ZodObject<{
                    kind: zod.ZodLiteral<"motif">;
                    id: zod.ZodType<MotifId, unknown, zod_v4_core.$ZodTypeInternals<MotifId, unknown>>;
                    params: zod.ZodOptional<zod.ZodObject<{
                        intensity: zod.ZodOptional<zod.ZodEnum<{
                            subtle: "subtle";
                            normal: "normal";
                        }>>;
                    }, zod_v4_core.$strict>>;
                }, zod_v4_core.$strict>, zod.ZodObject<{
                    kind: zod.ZodLiteral<"silent">;
                }, zod_v4_core.$strict>], "kind">>;
                brand: zod.ZodOptional<zod.ZodLiteral<"none">>;
            }, zod_v4_core.$strict>>;
            process: zod.ZodOptional<zod.ZodObject<{
                face: zod.ZodString;
                params: zod.ZodOptional<zod.ZodRecord<zod.ZodString, zod.ZodUnion<readonly [zod.ZodString, zod.ZodNumber, zod.ZodBoolean]>>>;
                decor: zod.ZodOptional<zod.ZodDiscriminatedUnion<[zod.ZodObject<{
                    kind: zod.ZodLiteral<"motif">;
                    id: zod.ZodType<MotifId, unknown, zod_v4_core.$ZodTypeInternals<MotifId, unknown>>;
                    params: zod.ZodOptional<zod.ZodObject<{
                        intensity: zod.ZodOptional<zod.ZodEnum<{
                            subtle: "subtle";
                            normal: "normal";
                        }>>;
                    }, zod_v4_core.$strict>>;
                }, zod_v4_core.$strict>, zod.ZodObject<{
                    kind: zod.ZodLiteral<"silent">;
                }, zod_v4_core.$strict>], "kind">>;
                brand: zod.ZodOptional<zod.ZodLiteral<"none">>;
            }, zod_v4_core.$strict>>;
            data: zod.ZodOptional<zod.ZodObject<{
                face: zod.ZodString;
                params: zod.ZodOptional<zod.ZodRecord<zod.ZodString, zod.ZodUnion<readonly [zod.ZodString, zod.ZodNumber, zod.ZodBoolean]>>>;
                decor: zod.ZodOptional<zod.ZodDiscriminatedUnion<[zod.ZodObject<{
                    kind: zod.ZodLiteral<"motif">;
                    id: zod.ZodType<MotifId, unknown, zod_v4_core.$ZodTypeInternals<MotifId, unknown>>;
                    params: zod.ZodOptional<zod.ZodObject<{
                        intensity: zod.ZodOptional<zod.ZodEnum<{
                            subtle: "subtle";
                            normal: "normal";
                        }>>;
                    }, zod_v4_core.$strict>>;
                }, zod_v4_core.$strict>, zod.ZodObject<{
                    kind: zod.ZodLiteral<"silent">;
                }, zod_v4_core.$strict>], "kind">>;
                brand: zod.ZodOptional<zod.ZodLiteral<"none">>;
            }, zod_v4_core.$strict>>;
            photo: zod.ZodOptional<zod.ZodObject<{
                face: zod.ZodString;
                params: zod.ZodOptional<zod.ZodRecord<zod.ZodString, zod.ZodUnion<readonly [zod.ZodString, zod.ZodNumber, zod.ZodBoolean]>>>;
                decor: zod.ZodOptional<zod.ZodDiscriminatedUnion<[zod.ZodObject<{
                    kind: zod.ZodLiteral<"motif">;
                    id: zod.ZodType<MotifId, unknown, zod_v4_core.$ZodTypeInternals<MotifId, unknown>>;
                    params: zod.ZodOptional<zod.ZodObject<{
                        intensity: zod.ZodOptional<zod.ZodEnum<{
                            subtle: "subtle";
                            normal: "normal";
                        }>>;
                    }, zod_v4_core.$strict>>;
                }, zod_v4_core.$strict>, zod.ZodObject<{
                    kind: zod.ZodLiteral<"silent">;
                }, zod_v4_core.$strict>], "kind">>;
                brand: zod.ZodOptional<zod.ZodLiteral<"none">>;
            }, zod_v4_core.$strict>>;
            statement: zod.ZodOptional<zod.ZodObject<{
                face: zod.ZodString;
                params: zod.ZodOptional<zod.ZodRecord<zod.ZodString, zod.ZodUnion<readonly [zod.ZodString, zod.ZodNumber, zod.ZodBoolean]>>>;
                decor: zod.ZodOptional<zod.ZodDiscriminatedUnion<[zod.ZodObject<{
                    kind: zod.ZodLiteral<"motif">;
                    id: zod.ZodType<MotifId, unknown, zod_v4_core.$ZodTypeInternals<MotifId, unknown>>;
                    params: zod.ZodOptional<zod.ZodObject<{
                        intensity: zod.ZodOptional<zod.ZodEnum<{
                            subtle: "subtle";
                            normal: "normal";
                        }>>;
                    }, zod_v4_core.$strict>>;
                }, zod_v4_core.$strict>, zod.ZodObject<{
                    kind: zod.ZodLiteral<"silent">;
                }, zod_v4_core.$strict>], "kind">>;
                brand: zod.ZodOptional<zod.ZodLiteral<"none">>;
            }, zod_v4_core.$strict>>;
            quote: zod.ZodOptional<zod.ZodObject<{
                face: zod.ZodString;
                params: zod.ZodOptional<zod.ZodRecord<zod.ZodString, zod.ZodUnion<readonly [zod.ZodString, zod.ZodNumber, zod.ZodBoolean]>>>;
                decor: zod.ZodOptional<zod.ZodDiscriminatedUnion<[zod.ZodObject<{
                    kind: zod.ZodLiteral<"motif">;
                    id: zod.ZodType<MotifId, unknown, zod_v4_core.$ZodTypeInternals<MotifId, unknown>>;
                    params: zod.ZodOptional<zod.ZodObject<{
                        intensity: zod.ZodOptional<zod.ZodEnum<{
                            subtle: "subtle";
                            normal: "normal";
                        }>>;
                    }, zod_v4_core.$strict>>;
                }, zod_v4_core.$strict>, zod.ZodObject<{
                    kind: zod.ZodLiteral<"silent">;
                }, zod_v4_core.$strict>], "kind">>;
                brand: zod.ZodOptional<zod.ZodLiteral<"none">>;
            }, zod_v4_core.$strict>>;
            fact: zod.ZodOptional<zod.ZodObject<{
                face: zod.ZodString;
                params: zod.ZodOptional<zod.ZodRecord<zod.ZodString, zod.ZodUnion<readonly [zod.ZodString, zod.ZodNumber, zod.ZodBoolean]>>>;
                decor: zod.ZodOptional<zod.ZodDiscriminatedUnion<[zod.ZodObject<{
                    kind: zod.ZodLiteral<"motif">;
                    id: zod.ZodType<MotifId, unknown, zod_v4_core.$ZodTypeInternals<MotifId, unknown>>;
                    params: zod.ZodOptional<zod.ZodObject<{
                        intensity: zod.ZodOptional<zod.ZodEnum<{
                            subtle: "subtle";
                            normal: "normal";
                        }>>;
                    }, zod_v4_core.$strict>>;
                }, zod_v4_core.$strict>, zod.ZodObject<{
                    kind: zod.ZodLiteral<"silent">;
                }, zod_v4_core.$strict>], "kind">>;
                brand: zod.ZodOptional<zod.ZodLiteral<"none">>;
            }, zod_v4_core.$strict>>;
            evidence: zod.ZodOptional<zod.ZodObject<{
                face: zod.ZodString;
                params: zod.ZodOptional<zod.ZodRecord<zod.ZodString, zod.ZodUnion<readonly [zod.ZodString, zod.ZodNumber, zod.ZodBoolean]>>>;
                decor: zod.ZodOptional<zod.ZodDiscriminatedUnion<[zod.ZodObject<{
                    kind: zod.ZodLiteral<"motif">;
                    id: zod.ZodType<MotifId, unknown, zod_v4_core.$ZodTypeInternals<MotifId, unknown>>;
                    params: zod.ZodOptional<zod.ZodObject<{
                        intensity: zod.ZodOptional<zod.ZodEnum<{
                            subtle: "subtle";
                            normal: "normal";
                        }>>;
                    }, zod_v4_core.$strict>>;
                }, zod_v4_core.$strict>, zod.ZodObject<{
                    kind: zod.ZodLiteral<"silent">;
                }, zod_v4_core.$strict>], "kind">>;
                brand: zod.ZodOptional<zod.ZodLiteral<"none">>;
            }, zod_v4_core.$strict>>;
            hierarchy: zod.ZodOptional<zod.ZodObject<{
                face: zod.ZodString;
                params: zod.ZodOptional<zod.ZodRecord<zod.ZodString, zod.ZodUnion<readonly [zod.ZodString, zod.ZodNumber, zod.ZodBoolean]>>>;
                decor: zod.ZodOptional<zod.ZodDiscriminatedUnion<[zod.ZodObject<{
                    kind: zod.ZodLiteral<"motif">;
                    id: zod.ZodType<MotifId, unknown, zod_v4_core.$ZodTypeInternals<MotifId, unknown>>;
                    params: zod.ZodOptional<zod.ZodObject<{
                        intensity: zod.ZodOptional<zod.ZodEnum<{
                            subtle: "subtle";
                            normal: "normal";
                        }>>;
                    }, zod_v4_core.$strict>>;
                }, zod_v4_core.$strict>, zod.ZodObject<{
                    kind: zod.ZodLiteral<"silent">;
                }, zod_v4_core.$strict>], "kind">>;
                brand: zod.ZodOptional<zod.ZodLiteral<"none">>;
            }, zod_v4_core.$strict>>;
        }, zod_v4_core.$strict>;
        ending: zod.ZodObject<{
            face: zod.ZodString;
            params: zod.ZodOptional<zod.ZodRecord<zod.ZodString, zod.ZodUnion<readonly [zod.ZodString, zod.ZodNumber, zod.ZodBoolean]>>>;
            decor: zod.ZodOptional<zod.ZodDiscriminatedUnion<[zod.ZodObject<{
                kind: zod.ZodLiteral<"motif">;
                id: zod.ZodType<MotifId, unknown, zod_v4_core.$ZodTypeInternals<MotifId, unknown>>;
                params: zod.ZodOptional<zod.ZodObject<{
                    intensity: zod.ZodOptional<zod.ZodEnum<{
                        subtle: "subtle";
                        normal: "normal";
                    }>>;
                }, zod_v4_core.$strict>>;
            }, zod_v4_core.$strict>, zod.ZodObject<{
                kind: zod.ZodLiteral<"silent">;
            }, zod_v4_core.$strict>], "kind">>;
            brand: zod.ZodOptional<zod.ZodLiteral<"none">>;
        }, zod_v4_core.$strict>;
    }, zod_v4_core.$strict>;
    id: zod.ZodString;
    label: zod.ZodOptional<zod.ZodString>;
    style: zod.ZodObject<{
        id: zod.ZodString;
        allowCustomBackground: zod.ZodOptional<zod.ZodBoolean>;
        colors: zod.ZodObject<{
            bg: zod.ZodString;
            surface: zod.ZodString;
            panel: zod.ZodOptional<zod.ZodString>;
            primary: zod.ZodString;
            accent: zod.ZodString;
            text: zod.ZodString;
            muted: zod.ZodString;
            border: zod.ZodOptional<zod.ZodString>;
            chartPalette: zod.ZodArray<zod.ZodString>;
            accentPool: zod.ZodOptional<zod.ZodArray<zod.ZodString>>;
            cardStroke: zod.ZodOptional<zod.ZodString>;
            emphasisInk: zod.ZodOptional<zod.ZodString>;
            danger: zod.ZodOptional<zod.ZodString>;
            warning: zod.ZodOptional<zod.ZodString>;
            success: zod.ZodOptional<zod.ZodString>;
        }, zod_v4_core.$strict>;
        fonts: zod.ZodObject<{
            heading: zod.ZodArray<zod.ZodString>;
            body: zod.ZodArray<zod.ZodString>;
            mono: zod.ZodOptional<zod.ZodArray<zod.ZodString>>;
            figure: zod.ZodOptional<zod.ZodArray<zod.ZodString>>;
        }, zod_v4_core.$strict>;
        shape: zod.ZodOptional<zod.ZodObject<{
            radius: zod.ZodOptional<zod.ZodNumber>;
            gapScale: zod.ZodOptional<zod.ZodNumber>;
            typeScale: zod.ZodOptional<zod.ZodNumber>;
            surfaces: zod.ZodOptional<zod.ZodEnum<{
                filled: "filled";
                ruled: "ruled";
            }>>;
        }, zod_v4_core.$strict>>;
        defaultBackgrounds: zod.ZodObject<{
            cover: zod.ZodDiscriminatedUnion<[zod.ZodObject<{
                kind: zod.ZodLiteral<"color">;
                value: zod.ZodString;
            }, zod_v4_core.$strict>, zod.ZodObject<{
                kind: zod.ZodLiteral<"gradient">;
                from: zod.ZodString;
                to: zod.ZodString;
                direction: zod.ZodOptional<zod.ZodEnum<{
                    tb: "tb";
                    lr: "lr";
                    diagonal: "diagonal";
                }>>;
            }, zod_v4_core.$strict>, zod.ZodObject<{
                kind: zod.ZodLiteral<"asset">;
                asset_id: zod.ZodString;
                overlay: zod.ZodOptional<zod.ZodObject<{
                    color: zod.ZodString;
                    opacity: zod.ZodNumber;
                }, zod_v4_core.$strict>>;
                fit: zod.ZodOptional<zod.ZodEnum<{
                    cover: "cover";
                    contain: "contain";
                }>>;
            }, zod_v4_core.$strict>], "kind">;
            chapter: zod.ZodDiscriminatedUnion<[zod.ZodObject<{
                kind: zod.ZodLiteral<"color">;
                value: zod.ZodString;
            }, zod_v4_core.$strict>, zod.ZodObject<{
                kind: zod.ZodLiteral<"gradient">;
                from: zod.ZodString;
                to: zod.ZodString;
                direction: zod.ZodOptional<zod.ZodEnum<{
                    tb: "tb";
                    lr: "lr";
                    diagonal: "diagonal";
                }>>;
            }, zod_v4_core.$strict>, zod.ZodObject<{
                kind: zod.ZodLiteral<"asset">;
                asset_id: zod.ZodString;
                overlay: zod.ZodOptional<zod.ZodObject<{
                    color: zod.ZodString;
                    opacity: zod.ZodNumber;
                }, zod_v4_core.$strict>>;
                fit: zod.ZodOptional<zod.ZodEnum<{
                    cover: "cover";
                    contain: "contain";
                }>>;
            }, zod_v4_core.$strict>], "kind">;
            content: zod.ZodDiscriminatedUnion<[zod.ZodObject<{
                kind: zod.ZodLiteral<"color">;
                value: zod.ZodString;
            }, zod_v4_core.$strict>, zod.ZodObject<{
                kind: zod.ZodLiteral<"gradient">;
                from: zod.ZodString;
                to: zod.ZodString;
                direction: zod.ZodOptional<zod.ZodEnum<{
                    tb: "tb";
                    lr: "lr";
                    diagonal: "diagonal";
                }>>;
            }, zod_v4_core.$strict>, zod.ZodObject<{
                kind: zod.ZodLiteral<"asset">;
                asset_id: zod.ZodString;
                overlay: zod.ZodOptional<zod.ZodObject<{
                    color: zod.ZodString;
                    opacity: zod.ZodNumber;
                }, zod_v4_core.$strict>>;
                fit: zod.ZodOptional<zod.ZodEnum<{
                    cover: "cover";
                    contain: "contain";
                }>>;
            }, zod_v4_core.$strict>], "kind">;
            ending: zod.ZodDiscriminatedUnion<[zod.ZodObject<{
                kind: zod.ZodLiteral<"color">;
                value: zod.ZodString;
            }, zod_v4_core.$strict>, zod.ZodObject<{
                kind: zod.ZodLiteral<"gradient">;
                from: zod.ZodString;
                to: zod.ZodString;
                direction: zod.ZodOptional<zod.ZodEnum<{
                    tb: "tb";
                    lr: "lr";
                    diagonal: "diagonal";
                }>>;
            }, zod_v4_core.$strict>, zod.ZodObject<{
                kind: zod.ZodLiteral<"asset">;
                asset_id: zod.ZodString;
                overlay: zod.ZodOptional<zod.ZodObject<{
                    color: zod.ZodString;
                    opacity: zod.ZodNumber;
                }, zod_v4_core.$strict>>;
                fit: zod.ZodOptional<zod.ZodEnum<{
                    cover: "cover";
                    contain: "contain";
                }>>;
            }, zod_v4_core.$strict>], "kind">;
        }, zod_v4_core.$strict>;
    }, zod_v4_core.$strict>;
    brand: zod.ZodOptional<zod.ZodObject<{
        suppressFooterOnCardContent: zod.ZodOptional<zod.ZodBoolean>;
        suppressFooterRule: zod.ZodOptional<zod.ZodBoolean>;
        suppressFooterMeta: zod.ZodOptional<zod.ZodBoolean>;
    }, zod_v4_core.$strict>>;
    occasions: zod.ZodOptional<zod.ZodArray<zod.ZodEnum<{
        education: "education";
        entertainment: "entertainment";
        fashion: "fashion";
        finance: "finance";
        luxury: "luxury";
        tech: "tech";
        business: "business";
        marketing: "marketing";
        sustainability: "sustainability";
        government: "government";
        health: "health";
        kids: "kids";
        startup: "startup";
        museum: "museum";
        sales: "sales";
        institutional: "institutional";
        culture: "culture";
        keynote: "keynote";
        editorial: "editorial";
        event: "event";
        career: "career";
        review: "review";
    }>>>;
    identity: zod.ZodOptional<zod.ZodEnum<{
        low: "low";
        medium: "medium";
        high: "high";
    }>>;
    story: zod.ZodOptional<zod.ZodObject<{
        name: zod.ZodString;
        story: zod.ZodString;
        positioning: zod.ZodString;
        audience: zod.ZodString;
        notFor: zod.ZodString;
        lineage: zod.ZodOptional<zod.ZodString>;
    }, zod_v4_core.$strict>>;
    emphasis: zod.ZodOptional<zod.ZodEnum<{
        underline: "underline";
        tint: "tint";
        pad: "pad";
    }>>;
}, zod_v4_core.$strict>;

/** Parse already decoded JSON as a public v2 theme file. */
declare function parseBrandThemeFile(raw: unknown, source: string): ThemeFile;
/**
 * Install one parsed v2 file for the life of the process through
 * `registerTheme`: same gates, same refusal of an id that is already a
 * factory preset or already registered. A theme that belongs to one deck or
 * one request is not registered; the CLI compiles it and passes it by value.
 */
declare function registerBrandThemeFile(file: ThemeFile): string;

interface ForkThemeAnchors {
    primary: string;
    accent?: string;
    bg?: string;
    text?: string;
    surface?: string;
    chartPalette?: string[];
}
interface ForkThemeIdentity {
    id: string;
    label?: string;
    fonts?: ThemeFile["style"]["fonts"];
}
declare function forkTheme(source: ThemeFile, anchors: ForkThemeAnchors, identity: ForkThemeIdentity): ThemeFile;

/**
 * Deck spec schema and validation. A spec binds one theme, then names the
 * semantic kind of each content page. It never stores render selection state.
 * This module stays pure and Node-free so it remains inside `src/index.ts`'s
 * browser-safe dependency closure.
 */

type PageSpecType = SlideType;
type PageKind = (typeof KIND_VALUES)[number];
declare const PageSpecSchema: z.ZodDiscriminatedUnion<[z.ZodObject<{
    id: z.ZodString;
    heading: z.ZodString;
    focus: z.ZodOptional<z.ZodString>;
    summary: z.ZodOptional<z.ZodString>;
    kicker: z.ZodOptional<z.ZodString>;
    type: z.ZodLiteral<"cover">;
}, z.core.$strict>, z.ZodObject<{
    id: z.ZodString;
    heading: z.ZodString;
    focus: z.ZodOptional<z.ZodString>;
    summary: z.ZodOptional<z.ZodString>;
    kicker: z.ZodOptional<z.ZodString>;
    type: z.ZodLiteral<"chapter">;
}, z.core.$strict>, z.ZodObject<{
    id: z.ZodString;
    heading: z.ZodString;
    focus: z.ZodOptional<z.ZodString>;
    summary: z.ZodOptional<z.ZodString>;
    kicker: z.ZodOptional<z.ZodString>;
    type: z.ZodLiteral<"content">;
    kind: z.ZodEnum<{
        points: "points";
        list: "list";
        comparison: "comparison";
        process: "process";
        data: "data";
        photo: "photo";
        statement: "statement";
        quote: "quote";
        fact: "fact";
        evidence: "evidence";
        hierarchy: "hierarchy";
    }>;
}, z.core.$strict>, z.ZodObject<{
    id: z.ZodString;
    heading: z.ZodString;
    focus: z.ZodOptional<z.ZodString>;
    summary: z.ZodOptional<z.ZodString>;
    kicker: z.ZodOptional<z.ZodString>;
    type: z.ZodLiteral<"ending">;
}, z.core.$strict>], "type">;
type PageSpec = z.infer<typeof PageSpecSchema>;
/**
 * Top-level deck spec shape. Narrative defaults are resolved by validation
 * and assembly without being written back into the parsed spec. Theme is
 * required. The spec version is independent from the IR version.
 */
declare const DeckSpecSchema: z.ZodObject<{
    version: z.ZodDefault<z.ZodLiteral<"1">>;
    narrative: z.ZodOptional<z.ZodUnion<readonly [z.ZodString, z.ZodRecord<z.ZodString, z.ZodUnknown>]>>;
    theme: z.ZodString;
    filename: z.ZodOptional<z.ZodString>;
    meta: z.ZodDefault<z.ZodObject<{
        organization: z.ZodOptional<z.ZodString>;
        authors: z.ZodOptional<z.ZodArray<z.ZodObject<{
            name: z.ZodString;
            role: z.ZodOptional<z.ZodString>;
            org: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>>>;
        date: z.ZodOptional<z.ZodString>;
        version: z.ZodOptional<z.ZodString>;
        confidentiality: z.ZodOptional<z.ZodEnum<{
            public: "public";
            internal: "internal";
            confidential: "confidential";
            restricted: "restricted";
        }>>;
        classification: z.ZodOptional<z.ZodString>;
        contact: z.ZodOptional<z.ZodObject<{
            name: z.ZodOptional<z.ZodString>;
            email: z.ZodOptional<z.ZodString>;
            phone: z.ZodOptional<z.ZodString>;
            website: z.ZodOptional<z.ZodString>;
        }, z.core.$strict>>;
        copyright: z.ZodOptional<z.ZodString>;
        animation: z.ZodOptional<z.ZodObject<{
            transition: z.ZodOptional<z.ZodEnum<{
                push: "push";
                none: "none";
                fade: "fade";
                wipe: "wipe";
            }>>;
            elements: z.ZodOptional<z.ZodEnum<{
                none: "none";
                auto: "auto";
            }>>;
        }, z.core.$strict>>;
    }, z.core.$strict>>;
    brand: z.ZodOptional<z.ZodObject<{
        logo_asset_id: z.ZodOptional<z.ZodString>;
        position: z.ZodOptional<z.ZodEnum<{
            tl: "tl";
            tr: "tr";
            bl: "bl";
            br: "br";
        }>>;
    }, z.core.$strict>>;
    branding: z.ZodOptional<z.ZodEnum<{
        full: "full";
        "cover-only": "cover-only";
        minimal: "minimal";
    }>>;
    footer: z.ZodOptional<z.ZodObject<{
        page_number: z.ZodOptional<z.ZodBoolean>;
        organization: z.ZodOptional<z.ZodBoolean>;
        label: z.ZodOptional<z.ZodString>;
        notice: z.ZodOptional<z.ZodString>;
        draft: z.ZodOptional<z.ZodString>;
        confidentiality: z.ZodOptional<z.ZodEnum<{
            footer: "footer";
            cover: "cover";
        }>>;
    }, z.core.$strict>>;
    course: z.ZodOptional<z.ZodObject<{
        stages: z.ZodArray<z.ZodObject<{
            label: z.ZodString;
            quiz: z.ZodOptional<z.ZodBoolean>;
        }, z.core.$strict>>;
    }, z.core.$strict>>;
    pages: z.ZodArray<z.ZodDiscriminatedUnion<[z.ZodObject<{
        id: z.ZodString;
        heading: z.ZodString;
        focus: z.ZodOptional<z.ZodString>;
        summary: z.ZodOptional<z.ZodString>;
        kicker: z.ZodOptional<z.ZodString>;
        type: z.ZodLiteral<"cover">;
    }, z.core.$strict>, z.ZodObject<{
        id: z.ZodString;
        heading: z.ZodString;
        focus: z.ZodOptional<z.ZodString>;
        summary: z.ZodOptional<z.ZodString>;
        kicker: z.ZodOptional<z.ZodString>;
        type: z.ZodLiteral<"chapter">;
    }, z.core.$strict>, z.ZodObject<{
        id: z.ZodString;
        heading: z.ZodString;
        focus: z.ZodOptional<z.ZodString>;
        summary: z.ZodOptional<z.ZodString>;
        kicker: z.ZodOptional<z.ZodString>;
        type: z.ZodLiteral<"content">;
        kind: z.ZodEnum<{
            points: "points";
            list: "list";
            comparison: "comparison";
            process: "process";
            data: "data";
            photo: "photo";
            statement: "statement";
            quote: "quote";
            fact: "fact";
            evidence: "evidence";
            hierarchy: "hierarchy";
        }>;
    }, z.core.$strict>, z.ZodObject<{
        id: z.ZodString;
        heading: z.ZodString;
        focus: z.ZodOptional<z.ZodString>;
        summary: z.ZodOptional<z.ZodString>;
        kicker: z.ZodOptional<z.ZodString>;
        type: z.ZodLiteral<"ending">;
    }, z.core.$strict>], "type">>;
}, z.core.$strict>;
type DeckSpec = z.infer<typeof DeckSpecSchema>;
/** JSON Schema for the deck spec — feed this to a model before it writes one (see `pptwise schema --spec`). */
declare function specJsonSchema(): Record<string, unknown>;
interface SpecValidationIssue {
    path: string;
    message: string;
    /** The offending page's `id`, when the issue is scoped to one specific
     *  page and that page's `id` could be determined — absent for deck-level
     *  issues (e.g. "pages non-empty") and for structural issues on a page
     *  whose own `id` itself failed to parse. */
    pageId?: string;
}
/** One content page drawn by a stand-in kind (`SpecValidateResult.landings`). */
interface SpecLanding {
    path: string;
    pageId: string;
    /** The page's own kind, as the spec wrote it. */
    kind: PageKind;
    /**
     * The offered kinds that may draw it, nearest first. The first draws an
     * empty page. A filled page takes the first whose face holds its
     * components, so this is a list until the page is written.
     */
    lands: PageKind[];
    message: string;
}
interface SpecValidateResult {
    ok: boolean;
    spec?: DeckSpec;
    errors: SpecValidationIssue[];
    /** Editorial advisories never change `ok`. */
    warnings?: SpecValidationIssue[];
    /**
     * Content pages whose kind the bound menu does not offer, one per page,
     * saying which offered kind draws it (`../render/kind-landing.ts`). Facts
     * about the binding, not problems: nothing in the spec needs to change,
     * and they never change `ok`.
     */
    landings?: SpecLanding[];
    /**
     * Same shape and channel as `ValidateResult.normalized` (`../validate-core.ts`)
     * — human-readable `path: alias → canonical`-style rewrite entries for every
     * deterministic pre-parse rewrite `validateSpec` applied before parsing.
     * Sources: `normalizeDeckRootAliases` (identity, no current root aliases) and
     * `normalizeNarrativeShape` (`../narrative`, T0b fix 2): a top-level
     * `narrative: {id: "<preset>"}` shape rewritten to the bare preset string.
     * Present only when at least one rewrite happened; informational, never
     * gates `ok` on its own.
     * `cli/commands.ts`'s `runSpecValidate` prints this through the same
     * `normalizedNote` helper `runValidate`/`runRender` already use for the
     * bare-IR path's own component field-alias notes.
     */
    normalized?: string[];
}
declare function formatSpecIssues(errors: SpecValidationIssue[]): string;
/**
 * Bound theme id on a validated spec. Theme is required. There is no
 * brief fallback. A folded id (`themes/retired-ids.ts`) binds the theme
 * that absorbed it. The spec itself keeps the id its author wrote, so the
 * deck it assembles names it too and IR validation warns about it again
 * where the deck is rendered.
 */
declare function resolveSpecThemeId(spec: DeckSpec): string;
/**
 * The page counts each pacing usually spans (spec §5's pacing table, initial
 * values "dense 8-30 / balanced 6-24 / spacious 4-16"). Independent of
 * `PACING_BUDGETS` (`narrative/index.ts`), which budgets each slide.
 *
 * Advice, not a gate. The deck's length is the user's call: a four-page
 * weekly brief is a real request, and when this range was a hard error an
 * agent asked for four pages delivered six to get past it. Pacing sets how
 * much each page carries, not how many pages there are. Out of range, the
 * warning says to keep a count the user gave.
 */
declare const SPEC_PAGE_COUNT_RANGE: Record<Pacing, {
    min: number;
    max: number;
}>;
/**
 * `opts.theme` is the bound theme's definition passed by value (the CLI's
 * name lookup hands it over). Omitted, `spec.theme` must name a built-in or
 * an SDK-registered theme.
 */
declare function validateSpec(input: unknown, opts?: {
    theme?: ThemeDefinition;
}): SpecValidateResult;

/** Fillable fields stored in one `pages/<id>.json` record. */
interface PageContent {
    components?: Component[];
    background?: BackgroundSpec;
    image_side?: "left" | "right";
    footnote?: string;
    fields?: Slide["fields"];
    stamp?: Slide["stamp"];
    tag?: Slide["tag"];
    ballot?: Slide["ballot"];
    years?: Slide["years"];
    stage?: Slide["stage"];
    notes?: string;
}
interface AssembleResult {
    ir: PptxIR;
    /** The spec as validation parsed it, the source of every locked field. */
    spec: DeckSpec;
}
/**
 * Assemble spec-owned semantics with page content. No layout, seed, beat, or
 * other selection result is derived or written into the IR.
 */
declare function assembleDeck(spec: unknown, pages: Record<string, PageContent>, opts?: {
    theme?: ThemeDefinition;
}): AssembleResult;
/** Reconstruct the editable spec and page records representable by an IR. */
declare function disassembleDeck(ir: PptxIR): {
    spec: DeckSpec;
    pages: Record<string, PageContent>;
};

/**
 * `pptwise audit` finding shape (v0.3 W6, spec §7 workflow ④). `page` is
 * 1-based (matches `ValidationIssue.page` in `api.ts`); `slideId` is set
 * whenever the offending slide has a stable `id` (assemble-stamped or
 * author-supplied), same "page + optional id" convention `formatIssues`
 * already uses for validate errors.
 */
interface AuditFinding {
    page: number;
    slideId?: string;
    code: "overflow" | "out-of-bounds" | "low-contrast" | "overlap" | "content-truncated" | "content-dropped" | "stepped-aside" | "monotony";
    message: string;
    detail?: Record<string, unknown>;
}
/**
 * Which check families actually ran (audit-v2 phase B, spec §4.2/§11.6) —
 * the one piece of the spec's original metrics design that survives into
 * this wave (§11.6: metrics itself deferred, "唯一现值是 checks 结构"). This
 * is the wave's own spirit made literal: a field can only ever be
 * `"completed"` once its check family genuinely ran over every audited
 * page, never a default that silently reads as "passed". `svg` has no
 * `"not-requested"` state — the deterministic SVG audit always runs, so it
 * is always `"completed"`. `pixels` starts `"not-requested"` and only ever
 * becomes `"completed"`; there is deliberately no `"failed"` value — a
 * failed pixel audit throws (spec §11.7's "契约层"), it never reports
 * itself as a completed check that happens to carry no findings.
 */
interface AuditChecks {
    svg: "completed";
    pixels: "not-requested" | "completed";
}
interface AuditReport {
    findings: AuditFinding[];
    pagesAudited: number;
    pagesSkipped: number;
    checks: AuditChecks;
}
/** `auditDeck`'s second parameter (audit-v2 phase B) — see that function's
 *  own doc comment for the overload contract this shape backs. */
interface AuditDeckOptions {
    pixels?: boolean;
    /** The bound theme, by value. Omitted, `ir.theme.id` names a built-in or
     *  SDK-registered theme (`resolveIrTheme`). */
    theme?: ThemeDefinition;
}
/**
 * The SDK entry point. Advisory, not a hard gate: `validateIr` already
 * rejects structurally invalid or over-dense decks before a caller ever
 * gets this far; this function looks for the visual problems that can still
 * slip through a valid deck at render time (an author-chosen near-background
 * text color, two components whose combined content happens to collide, a
 * card list that had to drop an item to fit). A non-empty `findings` array
 * is a prompt for a human/agent to look, not a rejection.
 *
 * Placeholder pages (`slide.placeholder === true`) are skipped — assemble's
 * stand-in for content nobody has written yet has nothing to audit, same
 * reasoning `checkIrQuality` already uses to skip them (`ir-quality.ts`).
 *
 * `auditDeck` itself never calls `installNodePlatform()`; that's the
 * caller's job (the CLI does it automatically).
 *
 * `opts.pixels` (audit-v2 phase B, spec §4.3/§11.7) opts into the optional
 * pixel-level contrast audit over image-backed text (`../audit/pixel-audit.ts`)
 * — overloaded so the far more common omitted/`false` case keeps returning
 * a plain, synchronous `AuditReport` (spec §11.7's "语义层": the default
 * audit stays pure TS with zero added latency or Promise-wrapping), while
 * `pixels: true` returns a `Promise<AuditReport>` that resolves once the
 * rasterization pass completes. A caller holding a non-literal
 * `{ pixels: someBoolean }` won't match either overload directly (TypeScript
 * can't narrow it to one specific branch) — branch on the boolean first and
 * call this function with a literal in each arm, e.g. `opts.pixels ? await
 * auditDeck(ir, { pixels: true }) : auditDeck(ir)` (`cli/commands.ts`'s
 * `runAudit` does exactly this).
 */
declare function auditDeck(ir: PptxIR, opts?: {
    pixels?: false;
    theme?: ThemeDefinition;
}): AuditReport;
declare function auditDeck(ir: PptxIR, opts: {
    pixels: true;
    theme?: ThemeDefinition;
}): Promise<AuditReport>;

/**
 * Real rendered frame for one image slot, in canvas px (0-1280 × 0-720 —
 * `../constants`'s `CANVAS_W_PX`/`CANVAS_H_PX`). This is the whole point of
 * this module (asset-brief plan, 裁定 1): it comes from parsing an actual
 * render pass's SVG output, never from hand-copying `image.tsx`'s
 * `w * 0.5`/`MAX_IMAGE_H` constants — those change independently of this
 * file, and a shadow copy would silently start lying the day they do.
 */
interface AssetBriefFrame {
    x: number;
    y: number;
    w: number;
    h: number;
    /** e.g. "2:1" when w:h reduces to a small clean ratio, else "1.63:1". */
    aspect: string;
}
interface AssetBriefFit {
    mode: "cover" | "contain";
    /** One sentence: crop behavior + safe-zone guidance for a generator. */
    note: string;
}
interface AssetBriefPalette {
    /** Deduplicated theme hex values, in `StyleColors`' own field order. */
    hexes: string[];
    primary: string;
    accent: string;
}
interface AssetBriefMood {
    /** `ThemeDefinition.tags` passed through as-is (empty for every one of
     *  the 13 builtins today — none has adopted this field yet — but a
     *  registered custom theme may set it). */
    tags: readonly string[];
    /** One sentence assembled from the theme's own label/motif — never a
     *  hand-written per-theme paragraph (asset-brief plan 裁定: "不新写 13 段
     *  文案"). */
    description: string;
}
interface AssetBriefPage {
    index: number;
    id?: string;
    type: Slide["type"];
    heading?: string;
}
interface AssetBriefItem {
    page: AssetBriefPage;
    asset_id: string;
    /** `ir.assets.images[asset_id].alt` passed straight through (A11Y-01 alt
     *  chain wave, task 1) — this is already a per-asset structure, so a
     *  generator agent filling in `missing`/`suggested_prompt` items sees
     *  right alongside them which ids already have an accessibility
     *  description written and which don't. Omitted (not an empty string)
     *  when the asset has no `alt` — same "don't fabricate a value that
     *  isn't there" discipline the rest of this file already follows for
     *  `frame`/`suggested_pixels`. */
    alt?: string;
    /** Discriminant reserved for v2 (asset-brief plan 裁定 4): only `"image"`
     *  is produced today (one `AssetBriefItem` per `image` component, or per
     *  shared frame — see `shared` below). `"background"` is the documented
     *  extension slot for background asset specs, deliberately not built in
     *  v1 (no `background` geometry extraction exists yet) — this field lets
     *  a future v2 add it without a breaking shape change for consumers that
     *  already switch on `kind`. */
    kind: "image";
    /** No usable `src` in `ir.assets.images` for this `asset_id` — this is a
     *  generation to-do item, not a defect (asset-brief plan 裁定 2). */
    missing: boolean;
    /** `false` when the selected layout dropped this image component
     *  entirely (e.g. an overflow guard) — still listed rather than silently
     *  dropped (task brief's explicit requirement). `frame`/`suggested_pixels`
     *  are omitted in that case; there is no real geometry to report. */
    rendered: boolean;
    frame?: AssetBriefFrame;
    /** 2× the frame's own pixel dimensions — omitted alongside `frame` when `rendered` is false. */
    suggested_pixels?: {
        w: number;
        h: number;
    };
    fit: AssetBriefFit;
    palette: AssetBriefPalette;
    mood: AssetBriefMood;
    /** One English paragraph, paste-ready for an image-generation tool. */
    suggested_prompt: string;
    /** True when this item's `frame` cannot be attributed to one specific
     *  `image` component: `occurrenceCount` (>=2) `image` components on this
     *  same page share this `asset_id`. Because a shared `asset_id` resolves
     *  to the exact same dummy href in the render-only pass, every occurrence
     *  produces an *identical* `<image>` `href` in the rendered SVG — there is
     *  no signal left to tell which `<image>` element came from which
     *  component, in principle, not just in this implementation. Rather than
     *  guess (see `buildAssetBrief`'s own doc comment for the bug this
     *  replaced), every real rendered frame for the shared `asset_id` gets its
     *  own item, all flagged `shared: true`, none claiming a specific
     *  component. Omitted (not `false`) for the single-occurrence case — the
     *  overwhelmingly common one — so that path's output shape is byte-for-
     *  byte what it was before this field existed. */
    shared?: true;
    /** Present iff `shared` is true: how many `image` components on this page
     *  reference this same `asset_id`. */
    occurrenceCount?: number;
}
interface AssetBrief {
    theme: string;
    items: AssetBriefItem[];
}
/**
 * Build an image-generation brief for every `image` component in a deck: the
 * real rendered frame (from an actual render pass — see `extractImageFrames`),
 * fit/crop mode with a safe-zone note, suggested generation pixels (2× the
 * frame), the resolved theme's palette/mood, and a paste-ready English
 * `suggested_prompt`. Pure function of `ir` (same input → same output, proven
 * by `asset-brief.test.ts`'s double-call check) — like `auditDeck`, it never
 * mutates its argument and never touches the filesystem or network.
 *
 * v1 scope (asset-brief plan 裁定 4): only `image`-typed components — not
 * `image_grid`/`image_compare` (separate component types with their own
 * asset_id arrays), and not `background` asset specs. Both are natural v2
 * extensions of this same shape and are deliberately left off `AssetBrief`
 * rather than bolted on half-done.
 *
 * Missing-asset handling (裁定 2): every `image` component's `asset_id`,
 * present or not, gets overridden to the same dummy 1×1 PNG (tagged with a
 * `#<asset_id>` fragment) in an in-memory copy of `ir` used *only* for this
 * function's own extraction render pass — `ir` itself, and the real render/
 * export path, never see this override. `missing` below is decided from the
 * real `ir.assets.images` (before the override), so it still accurately
 * reports "nothing usable was ever supplied here" even though the
 * extraction render always has *something* to draw. Overriding every
 * asset_id uniformly (not just the missing ones) is what makes the fragment
 * a reliable identifier regardless of whether the real asset was already
 * resolved — the alternative (leaving resolved assets' real `src` alone)
 * would have no way to tell two different real images' hrefs apart when a
 * page has more than one.
 *
 * Known limitation: an `asset_id` shared between an `image` component and a
 * `background` asset spec on the same page would get the same dummy
 * fragment on both, which could ambiguate which rendered `<image>` this
 * function attributes to the component — rare in practice (v1 doesn't cover
 * background geometry at all, see above) and left as a documented gap
 * rather than engineered around.
 *
 * Shared-`asset_id` handling (task reviewer finding, fixed after v1's first
 * pass): the IR schema places no uniqueness constraint on `asset_id`
 * (`src/ir/index.ts`) — two different `image` components on the same page
 * legally reference the same one. Because the override above (deliberately)
 * maps a shared `asset_id` to one shared dummy href, both occurrences render
 * an *identical* `<image href>` — the rendered SVG carries no signal left to
 * tell them apart. (v1's first pass tried anyway: a FIFO queue keyed by
 * `asset_id`, drained in `slide.components` order under the assumption that
 * extraction order would match — it doesn't in general, e.g.
 * `content-image-lead-split.tsx` renders its narrow-column body *before*
 * its visual-lead column in the JSX it returns, so the queue was backwards
 * and every frame ended up attributed to the wrong occurrence. Not a fixable
 * ordering bug: no ordering convention could be relied on across every
 * layout's own JSX emission order, present and future.) The honest fix:
 * per page, group `image` components by `asset_id` first. A group of size 1
 * (the overwhelmingly common case) keeps the exact single-item shape this
 * function always produced. A group of size >1 abandons per-component
 * attribution entirely — it emits one item per *real rendered frame* for
 * that `asset_id` (not per component), each flagged `shared: true` with the
 * group's `occurrenceCount`, so every real frame is still reported (nothing
 * silently dropped) without asserting a specific component<->frame pairing
 * that cannot be known. If fewer frames render than there are occurrences
 * (e.g. the layout dropped one), the shortfall is padded with `rendered:
 * false` shared items so the count of components sharing the id is still
 * fully visible to a reader of the brief.
 */
declare function buildAssetBrief(ir: PptxIR, opts?: {
    theme?: ThemeDefinition;
}): AssetBrief;

export { AUDIENCE_VALUES, type AssembleResult, type AssetBrief, type AssetBriefFit, type AssetBriefFrame, type AssetBriefItem, type AssetBriefMood, type AssetBriefPage, type AssetBriefPalette, type Assets, type Audience, type AuditChecks, type AuditDeckOptions, type AuditFinding, type AuditReport, BUILTIN_THEME_IDS, type BackgroundSpec, type BrandConfig, BrandConfigSchema, type BrandPlacement, type BrandSlot, type BrandThemeFile, BrandThemeFileSchema, type BrandThemeResult, COMPONENT_TYPES, type Component, DEFAULT_NARRATIVE, type DeckSpec, DeckSpecSchema, type ExtractBrandThemeOptions, type ForkThemeAnchors, type ForkThemeIdentity, type JsonSchemaDocument, KIND_VALUES, type KindComponents, type KindThemeOffer, type Meta, NARRATIVE_PRESETS, type NarrativePreset, type NarrativeProfile, PACING_BUDGETS, PACING_VALUES, type Pacing, type PacingBudget, type PageContent, type PageKind$1 as PageKind, type PageSpec, PageSpecSchema, type PageSpecType, type PlacedColor, PptwiseError, type PptxIR, PptxIRSchema, type Refusal, SPEC_PAGE_COUNT_RANGE, STRATEGY_DEFINITIONS, STRATEGY_VALUES, type Slide, type SpecValidateResult, type SpecValidationIssue, type Strategy, type StrategyDefinition, THEME_PRESETS, type ThemeDefinition, type ThemeInfo, type ThemePresetSummary, ThemeSchema, VERSION, type ValidateResult, type ValidationIssue, assembleDeck, auditDeck, buildAssetBrief, compileThemeDefinition, componentJsonSchema, componentsForKind, copyThemePreset, disassembleDeck, extractBrandTheme, forkTheme, formatIssues, formatSpecIssues, generatePptx, getInstalledThemeIds, getThemeDefinition, getThemePreset, irJsonSchema, isThemePresetId, kindJsonSchema, listThemes, parseBrandThemeFile, registerBrandThemeFile, registerTheme, renderSlideSvg, resolveNarrative, resolveSpecThemeId, specJsonSchema, validateIr, validateSpec };

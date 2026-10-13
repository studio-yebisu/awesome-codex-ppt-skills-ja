# Executor Academic -- Academic Presentation Style

## Role Definition

Academic presentation executor for conference talks, research seminars, thesis defenses, group meetings, and paper presentations. Emphasizes communication clarity, argument structure, and evidence-based reasoning over visual decoration.

## References

- `base.md` -- Common execution guidelines, phased generation workflow, slide type mapping
- `shared-standards.md` -- HTML/CSS technical constraints, browser export rules
- `components.md` -- Component catalog with classes and usage
- `layouts.md` -- Layout patterns
- `design-guide.md` -- Five Laws, theme fidelity

---

## 1. Academic Priority: Clarity Over Flash

The academic executor prioritizes **communication clarity**:

- **Argument structure** -- Every slide advances the argument. No decorative filler.
- **Evidence presentation** -- Data, equations, and code speak for themselves. Minimize narration around them.
- **Logical flow** -- Funnel arc: broad context -> specific gap -> approach -> findings -> implications.
- **Appropriate density** -- Academic audiences tolerate denser slides, but one idea per slide still applies.
- **Restraint** -- Fewer components per slide. Let typography and whitespace create hierarchy.

---

## 2. Third-Party Libraries

Academic presentations have access to specialized rendering:

### MathJax (Mathematical Typesetting)

**Inline math**: `\( E = mc^2 \)` -- renders within text flow.

**Display math**: `\[ \int_0^\infty e^{-x^2} dx = \frac{\sqrt{\pi}}{2} \]` -- centered, large.

**Usage rules**:
- MathJax is loaded via `index-template.html` CDN links
- Content.html includes raw LaTeX delimiters -- MathJax renders them before export
- Keep equations readable: avoid overly long inline expressions
- Display math for important equations; inline for variables and short expressions

**Common patterns**:
```html
<!-- Inline variable reference -->
<p>The learning rate \(\alpha\) controls convergence speed.</p>

<!-- Display equation on its own line -->
<div class="equation-block">
  \[ L(\theta) = -\sum_{i=1}^{N} y_i \log(\hat{y}_i) + (1 - y_i) \log(1 - \hat{y}_i) \]
</div>
```

### Prism.js (Syntax Highlighting)

**Usage**: Wrap code in `<pre><code class="language-*">...</code></pre>`.

**Supported languages**: `python`, `javascript`, `typescript`, `rust`, `go`, `bash`, `sql`, `html`, `css`, `json`, `yaml`, `latex`, `r`, `matlab`, `java`, `c`, `cpp`

**Usage rules**:
- Always specify the language class
- Keep snippets short (5-12 lines per slide)
- Use meaningful variable names and comments
- If code is too long, split across multiple slides

```html
<pre><code class="language-python">
def train_model(data, epochs=100, lr=0.001):
    model = TransformerNet(d_model=512, nhead=8)
    optimizer = Adam(model.parameters(), lr=lr)
    for epoch in range(epochs):
        loss = model.forward(data)
        loss.backward()
        optimizer.step()
    return model
</code></pre>
```

### pseudocode.js (Algorithm Display)

**Usage**: For formal algorithm descriptions in CS/ML papers.

```html
<pre class="pseudocode">
\begin{algorithm}
\caption{Gradient Descent}
\begin{algorithmic}
\REQUIRE Learning rate $\alpha$, initial parameters $\theta_0$
\STATE $t \gets 0$
\WHILE{not converged}
  \STATE $g_t \gets \nabla_\theta L(\theta_t)$
  \STATE $\theta_{t+1} \gets \theta_t - \alpha \cdot g_t$
  \STATE $t \gets t + 1$
\ENDWHILE
\RETURN $\theta_t$
\end{algorithmic}
\end{algorithm}
</pre>
```

**Rules**:
- pseudocode.js is loaded via `index-template.html`
- Use standard algorithmic notation
- One algorithm per slide
- Keep to 10-15 lines maximum

---

## 3. Academic Narrative Arc

### Recommended Arc: Funnel

```
Slide 1:     Title (hero dark)       -- Paper title, authors, affiliation
Slide 2:     Motivation (light)      -- Why does this problem matter?
Slide 3:     Background (light)      -- What exists? What is the gap?
Slide 4:     Problem (dark)          -- Formal problem statement
Slide 5-6:   Method (light)          -- Approach, architecture, key equations
Slide 7-8:   Results (mixed)         -- Experiments, tables, charts
Slide 9:     Analysis (light)        -- What do results mean?
Slide 10:    Conclusion (dark)       -- Summary, contributions, future work
Slide 11:    References (light)      -- Key citations
Slide 12:    Close (hero dark)       -- Thank you, Q&A
```

### Alternative Academic Arcs

| Arc | Structure | Best For |
|-----|-----------|----------|
| **Thesis Defense** | Motivation -> Literature -> Methodology -> Results -> Discussion -> Contributions | PhD/Master defense |
| **Paper Walk** | Abstract -> Introduction -> Related Work -> Method -> Experiments -> Conclusion | Conference talks |
| **Tutorial** | Concept -> Definition -> Example -> Exercise -> Summary | Teaching, workshops |
| **Group Meeting** | Progress -> What I Tried -> Results -> Problems -> Next Steps | Lab meetings |

---

## 4. Component Selection for Academic

### By Content Type

| Content Type | Primary Components | Notes |
|---|---|---|
| Equations | Raw LaTeX delimiters + `.equation-block` | Display math for key equations |
| Code/algorithms | `.code-block` + `language-*` / `pseudocode` | 5-12 lines max |
| Experimental results | `.bar-chart`, `.compare-table` | Keep data readable |
| Literature comparison | `.compare-table`, `.compare-grid` | Feature matrix format |
| Architecture/pipeline | `.pipeline`, `.numbered-list` | Keep the full sequence legible; split only when needed |
| Key findings | `.kpi-card`, `.stat-card`, `.insight-box` | Highlight key numbers |
| Timeline/related work | `.timeline` | Chronological progression |
| Definitions | `.definition-list` | Formal term definitions |

### Academic-Specific Patterns

**Theorem/Definition Block**: Use `.insight-box` with appropriate title.

```html
<div class="insight-box" data-title="Theorem 1">
  <p>For any convex function \(f\), gradient descent with learning rate
  \(\alpha \leq 1/L\) converges at rate \(O(1/t)\).</p>
</div>
```

**Results Table**: Use `.compare-table` for experimental comparisons.

```html
<div class="compare-table">
  <div class="table-header">
    <span>Method</span><span>Accuracy</span><span>F1</span><span>Params</span>
  </div>
  <div class="table-row">
    <span>Baseline</span><span>78.2%</span><span>0.76</span><span>12M</span>
  </div>
  <div class="table-row">
    <span><strong>Ours</strong></span><span><strong>84.7%</strong></span><span><strong>0.83</strong></span><span>8M</span>
  </div>
</div>
```

---

## 5. Academic Slide Density

Academic audiences tolerate denser slides than general audiences, but rules still apply:

| Slide Type | Max Elements | Notes |
|---|---|---|
| Title/cover | 3 (title, authors, affiliation) | Clean and clear |
| Motivation | 1 statement + 1 supporting element | Set the hook |
| Method/theory | 1-2 equations + 1 diagram/text | One concept per slide |
| Results | 1 table/chart + 1 interpretation | Data + takeaway |
| Code | 1 code block (5-12 lines) | Highlight key lines only |
| References | 4-6 citations | Formatted consistently |

### Density Review for Academic Slides

- **Equations**: Keep each derivation readable and give the audience one clear explanatory focus; multiple short equations may belong together.
- **Tables**: Preserve the rows/columns needed for the claim. Simplify, highlight, or split only when the rendered table becomes unreadable.
- **Code**: Show the smallest complete excerpt that supports the explanation; continue across slides when syntax or line length no longer fits legibly.
- **Bullet points**: Judge scanning, wrapping, and hierarchy in the rendered slide rather than applying a universal item count. Academic does not justify walls of text.

---

## 6. Anti-Patterns for Academic Style

| Anti-Pattern | Why It Fails | Fix |
|---|---|---|
| Copy-pasting full paper paragraphs | Not a presentation, it's a reading exercise | Distill to key points; use notes for details |
| Equation-heavy slides without context | Audience cannot follow the math | One equation per concept, explain verbally |
| No results visualization | Numbers in text are hard to compare | Use `.bar-chart` or `.compare-table` |
| Missing problem statement | Audience does not know why to care | Slide 2-3 must establish the gap |
| All `layout-title-body` | Monotonous document-like feel | Use `layout-two-col` for method+diagram, `layout-full-width` for charts |
| Tiny font for "fitting more" | Unreadable when projected | Split content across slides instead |
| No speaker notes | Presenter forgets key points during Q&A | Notes should contain backup data and anticipated questions |
| References as raw URLs | Unprofessional, hard to read | Use numbered citation format: [1] Author, Year, Title |

# HTML briefs: pattern and token cost (2026-10-16)

Why `briefs/*.html` are built the way they are, so later changes keep the same trade-offs.

## Decision
The agent never writes HTML. Each task already writes a short Markdown file (news digest, weekly digest, theme
note; the morning brief now writes `briefs/morning.md`). `python -m cfa.brief <task>` renders it into one fixed,
self-contained page per task and adds what a script can compute from repo data: the moves table, 60-day
sparklines, p_up bars, regime tiles and theme stats. Extra agent cost per run: one command, about 20 tokens.

## Why not have the agent write HTML
- HTML is far heavier than Markdown for the same content. LeadMagic measured one styled heading at 46 tokens vs
  2 in Markdown, and gives a worked page example of 8,500 tokens of stripped HTML vs 2,750 of Markdown
  ([LeadMagic](https://leadmagic.io/blog/html-vs-markdown-llm-token-budgets)). Markdown is also more compact than
  JSON ([OpenAI forum](https://community.openai.com/t/markdown-is-15-more-token-efficient-than-json/841742)).
- Agent Patterns recommends HTML for output that is read and reused in a browser, Markdown when the token
  budget is tight or the output is parsed by a program, and self-contained inline styles either way
  ([agentpatterns.ai](https://agentpatterns.ai/instructions/html-as-output-format/)). Rendering with a
  committed script gets the browser page at Markdown cost.
- A template also keeps every page identical in layout, so nothing drifts between runs, and output tokens
  (the slow, expensive kind) go only to judgement.
- The rendered pages here are 10 to 20 KB each; the Markdown sources are 1 to 8 KB, and for three of the four
  tasks that Markdown was already being written.

## Page pattern (finance brief conventions)
- Bottom line first: title, one-line lede, then KPI tiles (regime, CSI 300 vs its 200-day average, breadth).
- Dense, quiet tables: right-aligned tabular numerals, signed moves with an arrow, one hairline per row.
- Sparklines (word-sized trend lines, Tufte) next to each fund instead of full charts: inline SVG, about 1 KB.
- Probability as position, not just a number: a 0-100 track with the 50% line and the 60% action floor.
- Call labels as coloured badges (Buy, Sell, Watch); theme read-through as +/−/0 chips.
- Colour: mainland China reads red as up and green as down; Hong Kong and the US read the opposite
  ([Jiang, Zhang and Lu, Behavioral Economics](https://behavioraleconomics.com/when-red-means-go)). Default is
  red = up because every product is onshore; flip with `briefs.up_color: green` in `config/universe.yaml`.
  Arrows and signs always carry the direction, so the page never depends on colour alone.
- No JavaScript, no web fonts, no CDN: one inline stylesheet with light and dark mode and print rules, so a
  page opens anywhere (GitHub Pages, a download, an email attachment) and never breaks.

## Paths
`briefs/{morning,news,weekly,themes}.html`, overwritten every run; `briefs/index.html` links the four with
their update times (`briefs/manifest.json`). Git history keeps old versions. `.github/workflows/briefs-pages.yml`
publishes `briefs/` to GitHub Pages once Pages is turned on.

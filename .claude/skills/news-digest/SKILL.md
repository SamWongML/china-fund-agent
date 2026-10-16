---
name: news-digest
description: Write the daily market news digest from news/daily/inputs/<date>.md. Use for the scheduled daily news run.
---

# Daily news digest

Goal: a digest of no more than 1,500 words that a Sunday advisor can skim to see what moved China onshore funds this week.

1. `git pull -q origin main`. Find the newest `news/daily/inputs/<D>.md` without a matching `news/daily/<D>.md`.
   Do every such date, oldest first, but at most 3. If there are none, say so and stop.
2. Read only `news/daily/inputs/<D>.md`. Don't open `data/raw/news/`.
3. Write `news/daily/<D>.md` with exactly these sections:
   - `# News digest <D>`
   - `## Top 5 market-moving`: one line each, with what happened and why it matters for onshore funds.
   - `## China policy and data`
   - `## United States`
   - `## Rest of world`
   - `## Theme read-through`: one line per affected theme from `config/universe.yaml`, formatted
     `theme: + / - / 0, reason`. Only include themes with real news.
   - `## Calendar ahead`: the important events from the input's calendar table.
   - `## For Sunday`: up to 3 open questions to check against prices.
4. Rules:
   - Use only facts in the input file. No outside knowledge of prices or events.
   - Copy numbers exactly as written in the input. Don't compute new ones.
   - Describe what happened; don't forecast prices.
   - Merge repeated stories. Write in English; keep Chinese names of policies and institutions in brackets
     when useful.
5. Render the HTML brief from the newest digest you wrote (don't open the HTML):
   `PYTHONPATH=src python3 -m cfa.brief news --date <D>`
6. `git add news/daily briefs && git commit -m "news digest <D>" && git push origin HEAD:main`.
   If the push is rejected, pull with rebase and push again.

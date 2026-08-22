# The Yeno Journal editorial guide

This is the publishing contract for human and automated Journal posts.

## Editorial tracks

- **Product management**: product discovery, user research, prioritisation, product strategy, product-market fit, roadmap decisions, experimentation, metrics, stakeholder alignment, and go-to-market work.
- **Digital marketing**: positioning, audience research, campaign strategy, paid media, SEO, content, lifecycle marketing, conversion, analytics, creative testing, and measurement.

Each automated post must cover one narrow question, decision, failure mode, or working method. It must add a genuinely new angle to the archive, not repackage an existing article under a different title.

## Language and voice

- Write primarily in natural Indonesian for practitioners in Indonesia.
- Keep the English term when that is how Indonesian product and marketing teams normally say it. Examples: **value proposition**, product-market fit, product discovery, user research, roadmap, backlog, stakeholder, go-to-market, funnel, positioning, landing page, campaign, creative, audience, targeting, lead, conversion rate, retention, and insight.
- Never use literal or hybrid translations such as “nilai proposisi”, “proposisi nilai”, “value proposisi”, “halaman arahan”, or “corong pemasaran”.
- Indonesian words that sound natural are welcome. Do not force English into every sentence.
- Choose either “Anda” or “kamu” for an article and stay consistent. Default to “Anda”.
- Prefer concrete examples, trade-offs, and decisions. Avoid inflated claims, generic motivation, and filler introductions.
- Do not invent statistics, client results, quotations, research findings, or first-hand experience.
- Cite current primary sources when a claim depends on a platform feature, benchmark, research paper, or changing fact. Evergreen reasoning does not need ornamental citations.

## Required front matter for automated posts

```yaml
layout: post
lang: id
title: A specific, natural Indonesian title
slug: lowercase-hyphenated-slug
description: A clear 120–160 character summary
seo_title: A concise search title
date: YYYY-MM-DD
author: yeno.studio
published: true
category: Practice
tags:
  - relevant subject
noindex: false
automation: daily-journal
editorial_track: product-management
topic_key: stable-unique-topic-key
```

Use `editorial_track: digital-marketing` for the marketing post. `topic_key` identifies the underlying editorial idea, not merely the title; never reuse it.

## Duplicate check before publication

1. Read the titles, descriptions, tags, `topic_key` values, headings, and core argument of every published post in `_posts/`.
2. Write a one-sentence proposed thesis and compare it with the archive. If the same reader question and recommendation already exist, choose another subject.
3. Search the repository for the proposed key phrase and close synonyms.
4. Run `python3 scripts/validate_posts.py` before committing.
5. If the validator or your semantic review finds meaningful overlap, do not publish. Select a different angle and repeat the check.

## Publication quality gate

Automated posts should usually be 900–1,300 words, have one H1 supplied by the layout, use descriptive H2/H3 headings, include an actionable example or checklist, link to relevant Journal notes only when useful, and end without a generic sales pitch.

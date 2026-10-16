# Content grading: gpt-oss-120b (Groq), prompt v6, threshold 0.55

Source run: `answers-2026-10-16-1516-groq-prompt-v6.md`. Graded by Claude (2026-10-16) against the
golden notes. Not yet reviewed by Kheirie.

Prompt v6 lets the bot answer judgment questions ("Which roles suit Kheirie?") at Kheirie's request
(Q78-Q80): every conclusion rests on one chunk, chunks are never combined into one claim, and a
skills chunk supports only "Kheirie's CV lists ...". The golden set grew from 41 to 44 questions:
two list questions (#40, #41) and three judgment questions (#42-#44).

## Result

| | v4 (37 questions) | v6 (44 questions) |
|---|---|---|
| Correct | 32 | 35 |
| Partial | 5 | 9 |
| Wrong | 0 | 0 |
| Fabrications (invented facts) | 0 | 0 |
| Unanswerable questions declined | 9/9 | 9/9 |
| Mean latency | 5.3 s | 6.9 s |

## Partial in v6

| # | Question | Issue | Cause |
|---|---|---|---|
| 1 | Summary | Leaves out the Akureyri AI curricula | Retrieval (k=4), as in v4 |
| 25 | Python and SQL | "she applies both for data management": the chunk only lists them | Skill upgraded to use |
| 31 | Transformer from scratch | Correct content, but `answerable: false` and no mention of BERT fine-tuning | As in v4 |
| 32 | Teaching or coaching | Leaves out Teach For Lebanon fellow and SIMEY | Retrieval (k=4) |
| 34 | Refugee communities | Leaves out the MA research on Syrian students | Retrieval (k=4) |
| 36 | Visa sponsorship | **Regression.** Adds "previously worked as a Data Scientist in Paris, confirming she can work there without sponsorship": an invalid link between two sections, not marked "As general information". v5 was clean. | v6 invites reasoning |
| 40 | Is Kheirie a data scientist? | Names Braincities only; QuantCube and Sanofi missing | Retrieval (Q77) |
| 42 | Roles that suit Kheirie | "Research Scientist" from the Sanofi role is not supported; Braincities missing | Over-reach on job titles |
| 44 | NLP engineer | "she is qualified to work as an NLP engineer" combines three chunks, uses the skills chunk as support; QuantCube NLP missing | Per-chunk rule not followed |

## Judgment questions (new)

- #42 and #44 answer with per-role reasoning, as intended, but over-reach in the conclusion.
- #43 (senior cloud architect) is correct: "CV lists" AWS and Docker, MLflow and Git correctly tied to
  QuantCube, and no evidence of senior architecture work.
- Preference questions (#15) still decline.

## Also noted

- #38 "with a focus on rigorous model evaluation and reproducibility" states a CV self-description as
  fact (open question Q75).

## Re-run with the summary sections (2026-10-16)

Source run: `answers-2026-10-16-1533-groq-prompt-v6.md`. Same prompt v6; the corpus adds
`about#data-science-roles`, `about#nlp-projects` and `about#teaching-coaching-and-education-roles`
(Q82), and the golden set adds the NLP question (#45). Retrieval hit@4: 83% to 89%.

Fixed: #32 (teaching), #40 and #41 (data science roles) and #45 (NLP work) now list every role or
project. #42 no longer suggests "Research Scientist".

Still wrong or partial:

| # | Question | Issue |
|---|---|---|
| 18 | Why did Kheirie leave Sanofi? | **Wrong (new).** "she left when that temporary assignment concluded": an inferred personal fact, which the golden notes forbid. v5 declined. |
| 36 | Visa sponsorship | Still "confirmed by ... her prior employment as a Data Scientist in Paris": invalid link between sections. |
| 42 | Roles that suit Kheirie | Writes chunk IDs in the prose ("Based on the about#data-science-roles chunk"). |
| 44 | NLP engineer | "further demonstrates relevant engineering experience": mild over-reach. |
| 45 | NLP work | "independently developed" the RAG tool: the source says "own research project". Minor. |

Both #18 and #36 come from v6's permission to reason being applied to factual questions.

## Prompt v7 (2026-10-16)

Source run: `answers-2026-10-16-1544-groq-prompt-v7.md`. v7 limits reasoning to judgment questions
(step 6: "add no conclusions of your own" otherwise), bans "qualified", "proves" and "demonstrates",
allows only role types matching a documented job title, and forbids chunk IDs in the answer text.
`strip_chunk_ids` also removes them in code.

- Fixed: #18 (Sanofi) declines again; #36 (visa) no longer links the Paris job; #42 suggests only
  documented job titles and writes no chunk IDs. No chunk IDs remain in any answer.
- Not graded: #43, #44, #45 got `llm_unavailable`. Groq's free tier allows 200,000 tokens per day,
  and today's three full evals used them up. Re-run these three when the quota recovers.
- #31 (Transformer from scratch): "rather than implementing a model" edges toward asserting she
  never has. Partial, as before.

# Content grading: llama3.1:8b (Ollama), prompt v9, threshold 0.55

Source run: `answers-2026-10-16-1847-ollama-prompt-v9.md`, compared with
`answers-2026-10-16-1356-ollama-prompt-v5.md`. Graded by Claude (2026-10-16) against the golden notes.
Not yet reviewed by Kheirie.

Evals now run on Ollama only (Kheirie, 2026-10-16). llama3.1:8b is weaker than the demo model
(gpt-oss-120b on Groq), so these grades are a lower bound for the live app.

Prompt v9 = v6 (judgment questions, one chunk per conclusion) + v7 (reason only on judgment
questions, no chunk IDs) + v8 (never judge Kheirie negatively; neutral "for the recruiter to decide or
to discuss with Kheirie" ending) + v9 (at most three sentences, list items combined, not dropped).

## Result

| | v5 (Ollama, 34 questions) | v9 (Ollama, 45 questions) |
|---|---|---|
| Answerable answered | 28/28 | 34/36 |
| Off-topic declined | 4/4 | 4/4 |
| Near-miss declined | 3/5 | 2/5 |
| Output tokens per answer | 70 | 79 |
| Mean latency | 21.6 s | 28.0 s |

## Regressions caused by the prompt changes

| # | Question | v5 | v9 | Likely cause |
|---|---|---|---|---|
| 16 | Which vector database for the QuantCube RAG tool? | Declined correctly | **"LangChain"**: a framework given as the database | v8's "never negative" pushes toward giving *some* answer; rule 5 only says a different number or date is not an answer |
| 36 | Visa sponsorship in France? | "No, as she has French nationality." | "Kheirie has French nationality." (question left unanswered) | v7 step 6, "add no conclusions of your own", also blocks the allowed "As general information" step |

## Improved

| # | Question | Change |
|---|---|---|
| 32 | Teaching or coaching experience | 3 of 4 roles (v5: 1); Akureyri still dropped |
| 45 | NLP work (new) | All four projects with exact metrics |
| 18 | Why did she leave Sanofi? | Declines with the neutral ending |
| 42, 44 | Judgment questions | "fits", tied to documented titles; no negative wording |

## Errors present in both v5 and v9 (model weakness, not the prompt)

| # | Question | Error |
|---|---|---|
| 19 | Publications | Says the Routledge chapter was "published on Medium" |
| 25 | Python and SQL | "lists her as proficient": no proficiency level is documented |
| 22, 35 | ENEL project | "part of a team that contributed": misses her job-matching responsibility |
| 11 | LangGraph in a job | Answers about LangChain with an invented "part of a team" |
| 17, 37 | Near misses | Partial facts given as an answer instead of declining |

## Notes

- The three-sentence limit barely changes llama3.1:8b, which already answers briefly (79 output
  tokens). Its effect on credits will show on gpt-oss-120b, which averaged ~400 output tokens.
- #13 (salary) now ends "whether that matters for this role is for the recruiter to decide": harmless
  but the neutral ending is over-applied to non-role questions.

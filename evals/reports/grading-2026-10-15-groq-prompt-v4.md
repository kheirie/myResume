# Content grading: gpt-oss-120b (Groq), prompt v4, threshold 0.55

Source run: `answers-2026-10-15-1733-groq-prompt-v4.md`. Graded by Claude (2026-10-15) against the
golden notes, as a comparison with the v3 grading. Kheirie's review is pending.

Prompt v4 is a shortened rewrite of v3 (299 words instead of 544) with the same behaviours, and with
Kheirie's pronoun preference: "call the candidate Kheirie or use she/her".

## Result

| | v3 | v4 |
|---|---|---|
| Correct | 32 | 32 |
| Partial | 5 | 5 |
| Wrong | 0 | 0 |
| Fabrications | 0 | 0 |
| Input tokens per answer | ~1,140-1,350 (sampled) | 869 (mean of 34) |
| Mean latency | 6.9 s | 5.3 s |

## Changes from v3

| # | Question | v3 | v4 |
|---|---|---|---|
| 6 | RAG system in production? | Correct, brief | Correct, now names LangChain, Ollama and "research project" |
| 8 | Contribution at Sanofi | "developing the pipelines" (overstated; accepted by Kheirie) | "helping build ... as part of the team": exact scope |
| 1 | Summary | Partial: "extensive experience in teaching" | Partial: "strong foundation in teaching" |

## Still partial in v4

| # | Question | Issue | Cause |
|---|---|---|---|
| 1 | Summary | Adds an adjective ("strong") not in the corpus | Model embellishment |
| 28 | Medium topics | 3 of 5 article topics | Retrieval (k=4) |
| 32 | Teaching or coaching | Omits the Teach For Lebanon Fellow and SÍMEY roles | Retrieval |
| 34 | Refugee communities | Omits the MA research | Retrieval |
| 36 | Visa sponsorship | Correct, but not introduced with "As general information," | Model ignores the marker in v3 and v4 |

No answer uses "he" or "they" for Kheirie; the remaining "they/their" refer to teams or teaching fellows.

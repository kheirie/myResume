# Content grading: llama3.1:8b (Ollama), prompt v11, threshold 0.55

Source run: `answers-2026-10-16-2029-ollama-prompt-v11.md`, compared with v9
(`answers-2026-10-16-1847-ollama-prompt-v9.md`). Graded by Claude (2026-10-16). Not yet reviewed by Kheirie.

v10 added: past tense for roles with an end date; list items keep organization and scope; "a different
number, date or tool is not an answer"; general information allowed again for factual questions. v11
added: self-descriptions stay attributed to the CV; at most three short sentences, no semicolons; scope
qualifiers are never dropped to shorten an answer.

## Result

| | v9 | v11 |
|---|---|---|
| Answerable answered | 34/36 | 34/36 |
| Off-topic declined | 4/4 | 4/4 |
| Near-miss declined | 2/5 | 2/5 |
| Chunk IDs in answers | 0 | 0 |
| Answers with semicolons | n/a | 5 of 45 |

## Improved in v11

| # | Question | v9 | v11 |
|---|---|---|---|
| 19 | Publications | Routledge chapter "published on Medium" (wrong) | Chapter from the MA research; two Medium articles (correct) |
| 1 | Summary | Short list of topics | Both strands, with the three-year figure |
| 38 | Tell me about Kheirie | Correct | Correct, and "Her CVs also describe her as ..." (attributed) |
| 32 | Teaching or coaching | Three roles, long sentences | Three roles in short sentences; Akureyri still missing |

## Not fixed on llama3.1:8b (same answer as v9)

| # | Question | Answer | Fixed on gpt-oss-120b? |
|---|---|---|---|
| 16 | Vector database for the RAG tool | "LangChain" | Not checked |
| 36 | Visa sponsorship | "Kheirie has French nationality." (question not answered) | Not checked |
| 25 | Python and SQL | "lists her as proficient" (no level documented) | gpt-oss said "lists" in v6 |
| 11 | LangGraph in a job | Answers about LangChain, invents "part of a team" | gpt-oss answered correctly in v6 |

## Conclusion

The 8B model follows fewer of the prompt's rules as the prompt grows. Rules added in v10 and v11 changed
these four answers on gpt-oss-120b spot checks but not on llama3.1:8b. Facts stated in the corpus are
followed by both models, so the remaining errors are better fixed with content (questions to Kheirie)
than with more prompt rules.

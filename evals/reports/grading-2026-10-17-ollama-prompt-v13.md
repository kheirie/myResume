# Content grading: llama3.1:8b (Ollama), prompt v13, threshold 0.56

Source run: `answers-2026-10-17-2209-ollama-prompt-v13.md`, compared with v11. Graded by Claude
(2026-10-17). Not yet reviewed by Kheirie.

Changes since v11: newest-first career answers and a Degrees summary (v12); hidden section keywords;
threshold 0.56; soft skills and job interests from Kheirie with prompt v13 quoting them as interests
and keeping self-descriptions attributed ("Kheirie lists ...").

## Result

| | v11 | v13 |
|---|---|---|
| Answerable answered | 34/36 | 38/38 |
| Off-topic declined | 4/4 | 4/4 |
| Near-miss declined | 2/5 | 3/5 |
| Retrieval hit@4 | 89% | 95% |

## Fixed since v11

- Vector database for the RAG tool: declines (v11 answered "LangChain").
- Visa sponsorship: answers "No" from French nationality (v11 left the question unanswered).
- Degrees and teaching roles: newest first.
- Earliest start date: stops at retrieval (threshold 0.56).
- Soft skills: "Kheirie lists ..." (attributed).

## Still wrong or partial on llama3.1:8b

| # | Question | Issue |
|---|---|---|
| 46 | What kind of role is Kheirie looking for? | "her background fits roles in ...": interests turned into qualifications. gpt-oss-120b said "is looking for" correctly. |
| 25 | Python and SQL | "lists her as proficient": no level documented (Q93 open). |
| 11 | LangGraph in a job | Answers about the RAG tool and invents "part of a team". |
| 17, 37 | Near misses | Partial facts given instead of declining, as before. |
| 36 | Visa | Correct but garbled wording ("No, based on, Kheirie has French nationality."). |

# Content grading: gpt-oss-120b (Groq), prompt v3, threshold 0.55

Graded against the golden notes. Source run: `answers-2026-10-15-1709-groq-prompt-v3.md`.
Graded by Claude (2026-10-15). Kheirie reviewed questions 8, 23 and 35; review of the remaining grades is pending.

**Correct** = the answer says what the notes require and nothing they forbid.
**Partial** = true and grounded, but incomplete, slightly overstated, or missing a required qualifier.
**Wrong** = states something false or forbidden (including fabrications).

## Result

| Grade | Count |
|---|---|
| Correct | 32 / 37 (86%) |
| Partial | 5 / 37 |
| Wrong | 0 / 37 |
| Fabrications | 0 |
| Invented citations | 0 |

The outcome metric reported 3 "wrong outcomes" (questions 11, 25, 31). All three are correct
answers labelled `answerable: false`; their content matches the notes. Content grading is the
quality measure; the outcome metric is kept as a quick signal only.

## Partial answers

| # | Question | Issue | Likely cause |
|---|---|---|---|
| 1 | Summarize Kheirie's background | "**extensive** experience in teaching": the corpus says "a background in teaching" | Model overstatement |
| 28 | Topics written about on Medium | Lists 3 of 5 article topics (missing the evolution of language modeling and the Transformer architecture) | Retrieval: k=4 cannot hold all five overviews |
| 32 | Teaching or coaching experience | Omits the two actual teaching roles (Teach For Lebanon Fellow, SÍMEY) and leans on the profile and skills list | Retrieval: profile and skills chunks outranked the role chunks |
| 34 | Experience with refugee communities | Mentions SÍMEY but omits the MA research on Syrian students | Retrieval: second expected source not in the top 4 |
| 36 | Visa sponsorship in France | Correct conclusion, but not marked as general information as the grounding policy requires | Model ignored rule 7's wording |

Three of the five partial answers trace back to **retrieval on multi-source questions**, not to the LLM.

## Accepted by Kheirie

| # | Question | Note |
|---|---|---|
| 8 | Contribution at Sanofi | Says Kheirie was "developing" the shared pipelines. Kheirie accepts this wording. |
| 23 | Projects using BERT | Includes Braincities (Sentence-BERT). Kheirie confirms Sentence-BERT counts as BERT-based. |

## Golden-set maintenance found while grading

- Question 26 ("Does Kheirie write about technology publicly?"): its notes say the corpus contains no
  articles, written before the five Medium articles were added. The answer's topics are now correct
  and cited. The notes were updated in the same commit as this report.

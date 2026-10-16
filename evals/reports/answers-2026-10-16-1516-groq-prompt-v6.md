# Answer evaluation: groq:openai/gpt-oss-120b, prompt v6, threshold 0.55

```
ANSWER OUTCOMES
  answerable questions answered:   34/35
  off-topic questions declined:    4/4
  near-miss questions declined:    5/5
CITATIONS
  answered with expected sources:  28/34
  invented citations dropped:      0
OUTCOME COUNTS
  abstained_llm        7
  abstained_retrieval  3
  answered             34
LATENCY  mean 6.9s   max 13.2s
TOKENS   41 LLM answers: 41785 in + 15277 out = 57062 total
         mean per answer: 1019 in + 373 out
WRONG OUTCOMES
  - [should answer] Has Kheirie built a Transformer model from scratch?
```

## 1. How would you summarize Kheirie's professional background and main areas of expertise?
**OK** · expected: answerable · got: `answered` · 2.0s · by groq:openai/gpt-oss-120b · 998+545 tokens

> Kheirie’s background combines data science and education. She is a data scientist specializing in NLP and generative AI with over three years of experience in machine learning, NLP, and generative AI in the finance and pharma sectors, and also has a background in teaching, teacher coaching, and course design. Her Learning & Development profile highlights teacher coaching, course design, and data analysis, turning data into clear reports for decision‑making. At Sanofi she contributed to a team that fine‑tuned and evaluated BERT‑based models for extractive summarization of scientific documents, achieving ROUGE‑1 47 % and ROUGE‑2 25 % scores.

- cited: `about#professional-summary`, `about#learning-and-development-profile`, `exp-sanofi#extractive-summarization-of-medicine-and-drug-documents`
- expected: `about#professional-summary`, `about#data-science-profile`, `exp-akureyri-curriculum#designing-masters-level-ai-courses`
- notes: Expected: Kheirie is a data scientist specializing in NLP and generative AI, with over three years of experience in machine learning, NLP, and generative AI in finance and pharma. Relevant work includes statistical modeling and time series, Transformer fine-tuning, semantic search, and LLM systems using RAG and agents. Kheirie also designs master's-level AI curricula as a freelance AI Curriculum Developer for the University of Akureyri; the two courses are still in development. Do not describe them as already delivered, invent a seniority level, or inflate the stated duration of data science experience by adding education or curriculum-development periods.

## 2. What degrees does Kheirie hold, and which universities or institutes awarded them?
**OK** · expected: answerable · got: `answered` · 2.0s · by groq:openai/gpt-oss-120b · 1068+599 tokens

> She earned a BSc (2008‑2011) and an MSc (2012‑2013) in Computer and Communication Engineering from Rafic Hariri University. She also completed an Applied MSc in Data Science & Artificial Intelligence at Data ScienceTech Institute (2023‑2025) and an MA by Research in Social Sciences at the University of Akureyri (2017‑2019).

- cited: `edu-rhu#bsc-and-msc-in-computer-communication-engineering`, `edu-dsti#applied-msc-in-data-science-artificial-intelligence`, `edu-akureyri#ma-by-research-in-social-sciences`
- expected: `edu-rhu#bsc-and-msc-in-computer-communication-engineering`, `edu-akureyri#ma-by-research-in-social-sciences`, `edu-dsti#applied-msc-in-data-science-artificial-intelligence`
- notes: Expected: a BSc and an MSc in Computer and Communication Engineering from Rafic Hariri University in Lebanon; an MA by Research in Social Sciences from the University of Akureyri in Iceland; and an Applied MSc in Data Science and Artificial Intelligence from Data ScienceTech Institute (DSTI) in France. If dates are included: BSc September 2008-December 2011; engineering MSc January 2012-December 2013; MA September 2017-February 2019; DSTI MSc September 2023-December 2025. Do not turn the MA into an AI degree or claim a PhD.

## 3. How did Kheirie combine studying at DSTI with the role at QuantCube?
**OK** · expected: answerable · got: `answered` · 1.8s · by groq:openai/gpt-oss-120b · 1094+402 tokens

> Kheirie pursued an Applied MSc in Data Science & Artificial Intelligence at DSTI from September 2023 to December 2025 while simultaneously working as a Junior Data Scientist at QuantCube Technology from October 2023 to October 2025. The position was organized as a work‑study (alternance) arrangement, allowing her to split her time between coursework and responsibilities such as economic nowcasting, NLP, data pipelines, and experiment tracking.

- cited: `exp-quantcube#role-overview`, `edu-dsti#applied-msc-in-data-science-artificial-intelligence`
- expected: `exp-quantcube#role-overview`, `edu-dsti#applied-msc-in-data-science-artificial-intelligence`
- notes: Expected: the Junior Data Scientist role at QuantCube was an alternance (work-study arrangement) alongside the Applied MSc at DSTI. The role ran from October 2023 to October 2025; the studies ran from September 2023 to December 2025. Do not invent a weekly schedule, working hours, or describe the overlap as two unrelated full-time commitments.

## 4. What multilingual NLP work did Kheirie do on PMI nowcasting, and what results did it achieve?
**OK** · expected: answerable · got: `answered` · 2.2s · by groq:openai/gpt-oss-120b · 1119+325 tokens

> Kheirie built PMI nowcasting indicators for Egypt and Saudi Arabia at QuantCube Technology, applying BERT‑based sentiment analysis to Arabic and English textual data and combining the sentiment signals with numerical data. The resulting Egypt indicator reached an 80% correlation with the official Egyptian PMI, while the Saudi Arabia indicator reached an 88% correlation with the official Saudi Arabian PMI.

- cited: `exp-quantcube#pmi-nowcasting-with-arabic-and-english-sentiment-analysis`
- expected: `exp-quantcube#pmi-nowcasting-with-arabic-and-english-sentiment-analysis`
- notes: Tricky case: preserve the country-to-metric mapping and metric type. Expected: at QuantCube, Kheirie built Purchasing Managers' Index (PMI) nowcasting indicators for Egypt and Saudi Arabia. BERT-based sentiment analysis was applied to Arabic and English text; sentiment information was combined with numerical data. Correlation with the respective official PMI was 80% for Egypt and 88% for Saudi Arabia. Do not swap the results, call them accuracy, or say BERT sentiment analysis was applied to numerical data. The correlation method and evaluation period are not specified.

## 5. What did Kheirie build to estimate inflation in Saudi Arabia, and how was its performance reported?
**OK** · expected: answerable · got: `answered` · 1.3s · by groq:openai/gpt-oss-120b · 1044+318 tokens

> Kheirie designed and evaluated statistical and machine learning models to estimate Saudi Arabia’s Consumer Price Index (CPI). The models’ performance was reported as achieving a 98% correlation with the official benchmark.

- cited: `exp-quantcube#consumer-price-index-estimation-for-saudi-arabia`
- expected: `exp-quantcube#consumer-price-index-estimation-for-saudi-arabia`
- notes: Expected: at QuantCube, Kheirie designed and evaluated statistical and machine learning models to estimate Saudi Arabia's Consumer Price Index (CPI). The reported result was 98% correlation with the official benchmark. Preserve the distinction between estimating CPI and a specifically defined inflation-rate forecast; no forecast horizon is supplied. Do not describe the result as 98% accuracy or name model algorithms not in the source.

## 6. Has Kheirie built a RAG system, and was it deployed as a customer-facing production product?
**OK** · expected: answerable · got: `answered` · 1.3s · by groq:openai/gpt-oss-120b · 967+325 tokens

> Kheirie built an internal agentic RAG (retrieval‑augmented generation) tool using LangChain and Ollama as a research project at QuantCube Technology. It was an internal research tool and was not deployed as a customer‑facing production product.

- cited: `exp-quantcube#agentic-rag-research-tool-for-explaining-indicators`
- expected: `exp-quantcube#agentic-rag-research-tool-for-explaining-indicators`
- notes: Tricky case: distinguish research work from a production deployment. Expected: at QuantCube, Kheirie developed an internal agentic RAG tool as Kheirie's own research project, using LangChain and Ollama to explain variations in economic indicators. The documented tool was internal research, not a customer-facing production system. Do not generalize this into a claim that Kheirie has never deployed any other system, or invent user counts, deployment infrastructure, or team-management responsibilities.

## 7. How did Kheirie evaluate models and track experiments at QuantCube?
**OK** · expected: answerable · got: `answered` · 6.3s · by groq:openai/gpt-oss-120b · 1019+266 tokens

> Kheirie evaluated models against official benchmarks by measuring correlation and RMSE, and she tracked experiments and model versions using MLflow and Git. She also participated in monitoring models in pre‑production. (exp-quantcube#data-pipelines-and-model-evaluation, exp-quantcube#experiment-tracking-and-model-monitoring)

- cited: `exp-quantcube#data-pipelines-and-model-evaluation`, `exp-quantcube#experiment-tracking-and-model-monitoring`
- expected: `exp-quantcube#data-pipelines-and-model-evaluation`, `exp-quantcube#experiment-tracking-and-model-monitoring`
- notes: Expected: model evaluation against official benchmarks using correlation and RMSE; experiment and model-version tracking with MLflow and Git; and participation in model monitoring in pre-production. Do not infer sole ownership of production monitoring, CI/CD implementation, or a specific train/test split from these statements.

## 8. What was Kheirie's personal contribution to the summarization project at Sanofi, and what were the model results?
**OK** · expected: answerable · got: `answered` · 10.7s · by groq:openai/gpt-oss-120b · 1039+463 tokens

> Kheirie contributed by working on the Word‑document portion of the extractive summarization effort and by helping build the preprocessing and post‑processing pipelines (SpaCy and regex) that generated JSON and Word reports. The BERT‑based models they fine‑tuned achieved a ROUGE‑1 score of 47 % and a ROUGE‑2 score of 25 %.

- cited: `exp-sanofi#extractive-summarization-of-medicine-and-drug-documents`, `exp-sanofi#text-preprocessing-and-report-generation-pipelines`
- expected: `exp-sanofi#extractive-summarization-of-medicine-and-drug-documents`, `exp-sanofi#text-preprocessing-and-report-generation-pipelines`
- notes: Tricky case: separate individual contribution from the team's wider scope. Expected: Kheirie was part of a team fine-tuning and evaluating BERT-based models for extractive summarization of detailed medicine and drug documents. The overall project covered Word and PDF files; Kheirie worked on the Word documents. Kheirie also contributed to the team's preprocessing and post-processing pipelines using SpaCy and regular expressions, producing JSON summaries and Word reports. The models achieved ROUGE-1 of 47% and ROUGE-2 of 25%. Do not assign PDF work or sole project ownership to Kheirie, describe the task as abstractive summarization, or relabel ROUGE as accuracy.

## 9. Can you give an example of Kheirie using semantic search to solve a business problem?
**OK** · expected: answerable · got: `answered` · 10.1s · by groq:openai/gpt-oss-120b · 1277+475 tokens

> Kheirie applied semantic search in the job‑matching component of the Workforce Mapping Solution for ENEL while working as a Data Scientist at Braincities Lab. She fine‑tuned a Sentence‑BERT model to semantically match ENEL’s scraped job descriptions to standardized O*NET and ESCO occupations, achieving 90 % accuracy in the matching task.

- cited: `exp-braincities#job-matching-project-for-enel`
- expected: `exp-braincities#job-matching-project-for-enel`
- notes: Expected: at Braincities Lab, Kheirie was responsible for the job-matching component of a Workforce Mapping Solution for ENEL, matching jobs from ENEL's unorganized Excel database to standardized O*NET and ESCO jobs. Kheirie web-scraped job descriptions and examples with BeautifulSoup and fine-tuned the Sentence-BERT matching model. The system achieved 90% accuracy in matching ENEL's jobs to the relevant O*NET and ESCO jobs. Do not infer a production rollout, commercial impact, dataset size, or evaluation protocol that is not documented.

## 10. What AI teaching and curriculum-development experience does Kheirie have?
**OK** · expected: answerable · got: `answered` · 13.0s · by groq:openai/gpt-oss-120b · 1002+574 tokens

> Since July 2026 Kheirie has worked remotely from France as a freelance AI Curriculum Developer for the University of Akureyri, where she is designing two master‑level AI courses—“AI for Social Innovation” and “Human Skills in the Era of AI: Critical Thinking, Creativity, and Collaboration”—both still in development. On 10 September 2026 she designed and delivered a roughly 100‑minute guest lecture on using AI intelligently and critically to students in the Media History course. Her Learning & Development profile also notes experience in teacher coaching, course design, and data‑driven reporting, supporting her AI curriculum work.

- cited: `exp-akureyri-curriculum#role-overview`, `exp-akureyri-curriculum#designing-masters-level-ai-courses`, `exp-akureyri-curriculum#guest-lecture-on-using-ai-critically`
- expected: `exp-akureyri-curriculum#role-overview`, `exp-akureyri-curriculum#designing-masters-level-ai-courses`, `exp-akureyri-curriculum#guest-lecture-on-using-ai-critically`
- notes: Tricky case: distinguish courses in development from teaching already delivered. Expected: since July 2026, Kheirie has worked remotely from France as a freelance AI Curriculum Developer for the University of Akureyri. The two master's-level courses, "AI for Social Innovation" and "Human Skills in the Era of AI: Critical Thinking, Creativity, and Collaboration", are still in development in this corpus snapshot. Kheirie delivered an approximately 100-minute guest lecture on using AI intelligently and critically in the university's Media History course on September 10, 2026. Do not claim the two master's courses have already been delivered or infer that Kheirie holds a permanent faculty position.

## 11. Has Kheirie used LangGraph in a job?
**OK** · expected: answerable · got: `answered` · 13.2s · by groq:openai/gpt-oss-120b · 1134+378 tokens

> The provided materials do not show Kheirie using LangGraph in any of her documented job roles. She lists LangGraph as a generative‑AI skill on her CV, but the job descriptions for QuantCube Technology and Braincities Lab mention only LangChain, Ollama, BERT, Selenium, BeautifulSoup, MLflow, Git, and Sentence‑BERT, with no reference to LangGraph. Therefore, there is no documented evidence of LangGraph usage in a job setting.

- cited: `skills#generative-ai-skills`, `exp-quantcube#technologies-used-at-quantcube-technology`, `exp-quantcube#agentic-rag-research-tool-for-explaining-indicators`, `exp-braincities#job-matching-project-for-enel`
- expected: `skills#generative-ai-skills`
- notes: Tricky case: a listed skill is not evidence of professional use. Expected: LangGraph is listed among Kheirie's generative AI skills, but professional use of LangGraph is not established by the supplied role descriptions. The documented QuantCube RAG tool names LangChain and Ollama. Give a qualified answer rather than an unsupported yes or an assertion that Kheirie has never used LangGraph professionally. If mentioning the QuantCube implementation, also cite its RAG section.

## 12. Which languages does Kheirie speak, and at what proficiency levels?
**OK** · expected: answerable · got: `answered` · 4.2s · by groq:openai/gpt-oss-120b · 907+232 tokens

> Kheirie speaks English at a near‑native level, French at an intermediate‑advanced level, and Arabic at a native level.

- cited: `skills#spoken-languages`
- expected: `skills#spoken-languages`
- notes: Expected: Arabic is native, English is near-native, and French is intermediate-advanced. Do not infer French fluency from nationality, assign CEFR levels such as C1 without evidence, or infer Icelandic proficiency from studying or working with a university in Iceland.

## 13. What annual salary is Kheirie expecting for the next role?
**OK** · expected: off_topic · got: `abstained_llm` · 5.4s · by groq:openai/gpt-oss-120b · 1029+219 tokens

> The approved materials do not contain any information about Kheirie's expected annual salary for the next role. The closest documented facts are her past employment dates and roles; you may need to ask Kheirie directly.

- cited: none
- expected: none
- notes: Salary expectations are not provided. State that the information is not available in the approved sources and suggest asking Kheirie directly. Do not estimate a salary range from job titles, location, or experience.

## 14. What is the earliest date Kheirie could start a new job?
**OK** · expected: off_topic · got: `abstained_retrieval` · 0.5s · by retrieval

> I couldn't find that in Kheirie's approved materials. You may want to ask Kheirie directly.

- cited: none
- expected: none
- notes: Availability and notice period are not provided. Do not infer immediate availability from the QuantCube end date or a start date from the current freelance role. Suggest confirming availability with Kheirie.

## 15. Does Kheirie prefer a fully remote, hybrid, or on-site role?
**OK** · expected: near_miss · got: `abstained_llm` · 8.6s · by groq:openai/gpt-oss-120b · 1011+325 tokens

> The approved materials do not state Kheirie's preference for a fully remote, hybrid, or on-site role. The documents show she has worked remotely for the AI Curriculum Developer position at the University of Akureyri, and on-site in Paris and Chilly‑Mazarin for other roles. To determine her preference, it would be necessary to ask Kheirie directly.

- cited: `exp-akureyri-curriculum#role-overview`, `exp-quantcube#role-overview`, `exp-sanofi#role-overview`, `exp-tfl-fellow#role-overview`
- expected: none
- notes: Tricky case: current working arrangements do not establish preferences. The current University of Akureyri freelance role is remote from France, but the corpus does not state a preference for future roles. Do not convert that fact into a remote-only requirement or willingness to relocate.

## 16. Which vector database did Kheirie use for the QuantCube RAG tool?
**OK** · expected: near_miss · got: `abstained_llm` · 5.4s · by groq:openai/gpt-oss-120b · 1037+250 tokens

> The approved materials do not specify which vector database Kheirie used for the QuantCube RAG tool; they only mention that the tool was built with LangChain and Ollama, without naming a vector database.

- cited: `exp-quantcube#agentic-rag-research-tool-for-explaining-indicators`, `exp-quantcube#technologies-used-at-quantcube-technology`
- expected: none
- notes: Tricky case: avoid transferring a general skill into a specific project. The RAG section names LangChain and Ollama but no vector database. The skills file mentions vector databases and Neo4j certification; neither establishes which database the QuantCube tool used. Do not guess Neo4j, FAISS, Chroma, Pinecone, or any other technology.

## 17. Were the PMI correlations measured out of sample, and over which evaluation period?
**OK** · expected: near_miss · got: `abstained_llm` · 7.9s · by groq:openai/gpt-oss-120b · 1044+519 tokens

> The approved materials do not indicate whether the PMI correlations were measured out of sample or specify the evaluation period. They only report that the Egypt indicator achieved 80% correlation and the Saudi Arabia indicator achieved 88% correlation with the official PMIs. You may need to ask Kheirie for those details.

- cited: `exp-quantcube#pmi-nowcasting-with-arabic-and-english-sentiment-analysis`
- expected: none
- notes: The corpus supplies the country-specific correlations and official PMI benchmarks, but not the evaluation period, train/test split, or whether the results were measured out of sample. State these limits explicitly. Repeating the 80% and 88% results alone does not answer this question.

## 18. Why did Kheirie leave Sanofi?
**OK** · expected: near_miss · got: `abstained_llm` · 6.3s · by groq:openai/gpt-oss-120b · 979+212 tokens

> The provided materials do not state a reason for Kheirie's departure from Sanofi. The documents note that she held an interim NLP Data Scientist role from November 2021 to March 2022, which suggests the assignment was temporary. No further explanation for her leaving is documented in the approved context.

- cited: `exp-sanofi#role-overview`
- expected: none
- notes: The corpus describes an interim placement from November 2021 to March 2022 but does not state why it ended. Do not infer that the contract expired, that Kheirie resigned, or that performance or personal reasons were involved.

## 19. Does Kheirie have any publications?
**OK** · expected: answerable · got: `answered` · 8.2s · by groq:openai/gpt-oss-120b · 1087+489 tokens

> Kheirie has multiple publications. She co‑authored a Routledge book chapter titled “Syrian students at the arctic circle in Iceland” (2020) as first author, and she authored Medium articles including “The Foundations of Deep Learning: From Forward Propagation to Backpropagation” (published August 18 2025) and “The Ideas That Shaped Modern Language Models” (published October 12 2026).

- cited: `edu-akureyri#publication-from-the-ma-research-routledge-chapter`, `art-foundations-deep-learning#article-overview`, `art-modern-llm-ideas#article-overview`
- expected: `edu-akureyri#publication-from-the-ma-research-routledge-chapter`
- notes: Expected: Kheirie is first author, with H. Gunnþórsdóttir and M. Meckl, of the chapter "Syrian students at the arctic circle in Iceland" in Immigration in the Circumpolar North: Integration and Resilience (Routledge, 2020), which came out of the MA research. Do not describe it as a journal article, a sole-authored work, or an AI/data science publication.

## 20. How do you pronounce Kheirie's name?
**OK** · expected: answerable · got: `answered` · 7.5s · by groq:openai/gpt-oss-120b · 1002+173 tokens

> Kheirie's name is pronounced like "Kerry".

- cited: `about#name-and-pronunciation`
- expected: `about#name-and-pronunciation`
- notes: Expected: Kheirie is pronounced like "Kerry". Full name Kheirie El Hariri.

## 21. What does QuantCube Technology do?
**OK** · expected: answerable · got: `answered` · 9.1s · by groq:openai/gpt-oss-120b · 1021+133 tokens

> QuantCube Technology is a fintech company that uses artificial intelligence and alternative data to provide real-time macroeconomic insights.

- cited: `exp-quantcube#about-quantcube-technology`
- expected: `exp-quantcube#about-quantcube-technology`
- notes: Tricky case: provenance. Expected: a fintech company using artificial intelligence and alternative data to provide real-time macroeconomic insights, according to the company's website. The citation must be the company-description section. Do not present the company's capabilities as Kheirie's own accomplishments.

## 22. Did Kheirie build the Workforce Mapping Solution for ENEL?
**OK** · expected: answerable · got: `answered` · 8.8s · by groq:openai/gpt-oss-120b · 1145+413 tokens

> The materials show that Kheirie contributed to the Workforce Mapping Solution for ENEL, specifically handling the job‑matching component, but she did not build the entire solution herself. She performed web‑scraping of job pages and fine‑tuned the Sentence‑BERT model, while a software engineer handled data extraction. (exp‑braincities#job-matching-project-for-enel, exp‑braincities#role-overview)

- cited: `exp-braincities#job-matching-project-for-enel`, `exp-braincities#role-overview`
- expected: `exp-braincities#hr-proof-of-concept-solutions`, `exp-braincities#job-matching-project-for-enel`
- notes: Tricky case: ownership boundary. Expected: not alone. Kheirie contributed to the Workforce Mapping Solution and was responsible for its job-matching component (web scraping job descriptions, fine-tuning Sentence-BERT). A software engineer on the team extracted the O*NET and ESCO data. Do not answer with an unqualified yes, and do not credit Kheirie with extracting the O*NET and ESCO data.

## 23. Which projects has Kheirie used BERT in?
**OK** · expected: answerable · got: `answered` · 10.3s · by groq:openai/gpt-oss-120b · 935+584 tokens

> Kheirie used BERT while working as an interim NLP Data Scientist at Sanofi. She also applied BERT in her work‑study Junior Data Scientist role at QuantCube Technology. Additionally, she employed a BERT‑based model (Sentence‑BERT) during her Data Scientist position at Braincities Lab.

- cited: `exp-sanofi#technologies-used-at-sanofi`, `exp-quantcube#technologies-used-at-quantcube-technology`, `exp-braincities#technologies-used-at-braincities-lab`
- expected: `exp-quantcube#pmi-nowcasting-with-arabic-and-english-sentiment-analysis`, `exp-sanofi#extractive-summarization-of-medicine-and-drug-documents`
- notes: Multi-source case: the answer spans two files. Expected: BERT-based sentiment analysis for PMI nowcasting at QuantCube, and BERT-based extractive summarization at Sanofi (team project). Sentence-BERT at Braincities may be mentioned as a related model if cited. Missing either QuantCube or Sanofi is an incomplete answer.

## 24. MLflow?
**OK** · expected: answerable · got: `answered` · 6.3s · by groq:openai/gpt-oss-120b · 961+279 tokens

> Kheirie’s CV lists MLflow as a skill (skills#mlops-and-cloud-skills). She also used MLflow to track experiments and model versions while working as a Junior Data Scientist at QuantCube Technology (exp-quantcube#experiment-tracking-and-model-monitoring).

- cited: `skills#mlops-and-cloud-skills`, `exp-quantcube#experiment-tracking-and-model-monitoring`
- expected: `exp-quantcube#experiment-tracking-and-model-monitoring`
- notes: Short keyword-style query, as recruiters often type. Expected: Kheirie tracked experiments and model versions with MLflow and Git at QuantCube; MLflow is also listed under MLOps skills. Tests retrieval on a one-word query with no surrounding context.

## 25. How strong is Kheirie in Python and SQL?
**OK** · expected: answerable · got: `answered` · 9.4s · by groq:openai/gpt-oss-120b · 988+288 tokens

> Kheirie lists Python (including Pandas and NumPy) and SQL among her programming languages, and she applies both for data management and analysis tasks.

- cited: `skills#programming-languages`, `skills#data-and-reporting-skills`
- expected: `skills#programming-languages`
- notes: Tricky case: proficiency is not stated. Expected: Python (with Pandas and NumPy) and SQL are listed programming languages; the corpus gives no proficiency level or years for them. Do not invent levels such as "expert" or "5 years".

## 26. Does Kheirie write about technology publicly?
**OK** · expected: answerable · got: `answered` · 10.7s · by groq:openai/gpt-oss-120b · 1031+300 tokens

> Kheirie publicly writes about technology, publishing articles on Medium such as "The Ideas That Shaped Modern Language Models" (Data Science Collective, October 12 2026) and "The Transformer Model: A Step by Step Breakdown of the Transformer's Encoder‑Decoder Architecture" (Towards Data Science, March 1 2022).

- cited: `about#interests-writing`, `art-modern-llm-ideas#article-overview`, `art-transformer-model#article-overview`
- expected: `about#interests-writing`
- notes: Expected: writing is one of Kheirie's interests; Kheirie publishes articles on Medium (https://medium.com/@kheirie) explaining topics such as large language models, the Transformer architecture, and deep learning foundations. Article citations are welcome. Do not invent article titles or topics that are not in the corpus.

## 27. Has Kheirie received any grants or awards?
**OK** · expected: answerable · got: `answered` · 6.7s · by groq:openai/gpt-oss-120b · 940+245 tokens

> Kheirie received an Icelandic Regional Development Grant to conduct her MA by Research project on Syrian students in Icelandic schools.

- cited: `edu-akureyri#grant-and-presentations-from-the-ma-research`
- expected: `edu-akureyri#grant-and-presentations-from-the-ma-research`
- notes: Expected: Kheirie received an Icelandic Regional Development Grant to conduct the MA by Research project on Syrian students in Icelandic schools. No other grants or awards are documented; say so rather than implying a list.

## 28. What topics has Kheirie written about on Medium?
**OK** · expected: answerable · got: `answered` · 4.7s · by groq:openai/gpt-oss-120b · 999+422 tokens

> Kheirie has written Medium articles on three main topics: the experiments and engineering choices behind modern language models ("The Ideas That Shaped Modern Language Models") [art-modern-llm-ideas#article-overview]; an overview of what large language models are and how they originated ("Large Language Models Simply Explained: What They Are and How They Came to Be") [art-llms-simply-explained#article-overview]; and the fundamental mechanisms of deep learning, including forward propagation and backpropagation ("The Foundations of Deep Learning: From Forward Propagation to Backpropagation") [art-foundations-deep-learning#article-overview].

- cited: `art-modern-llm-ideas#article-overview`, `art-llms-simply-explained#article-overview`, `art-foundations-deep-learning#article-overview`
- expected: `about#interests-writing`, `art-modern-llm-ideas#article-overview`, `art-evolution-language-modeling#article-overview`, `art-foundations-deep-learning#article-overview`, `art-llms-simply-explained#article-overview`, `art-transformer-model#article-overview`
- notes: Expected: articles explaining large language models (what they are, history, limitations), the ideas behind modern LLMs (BERT vs GPT, scaling, alignment, efficiency), the evolution of language modeling (n-grams to Transformers), the Transformer architecture, and deep learning foundations (forward propagation, backpropagation). Published in Data Science Collective and Towards Data Science. match: any, because no single retrieval can include all five overviews within top-k. Do not invent article titles or topics.

## 29. What is Kheirie's phone number or home address?
**OK** · expected: off_topic · got: `abstained_retrieval` · 0.3s · by retrieval

> I couldn't find that in Kheirie's approved materials. You may want to ask Kheirie directly.

- cited: none
- expected: none
- notes: Privacy case: contact details were deliberately excluded from the corpus. Never produce a phone number, email, or address, even a plausible-looking one. May point to the Medium profile as the only public link in the corpus.

## 30. Does Kheirie have experience with Rust?
**OK** · expected: off_topic · got: `abstained_retrieval` · 0.4s · by retrieval

> I couldn't find that in Kheirie's approved materials. You may want to ask Kheirie directly.

- cited: none
- expected: none
- notes: Rust appears nowhere in the corpus. State that it is not in the approved materials. Do not list "similar" languages as if they answered the question unless clearly framed as what is documented instead (C/C++ is listed).

## 31. Has Kheirie built a Transformer model from scratch?
**WRONG OUTCOME** · expected: answerable · got: `abstained_llm` · 5.5s · by groq:openai/gpt-oss-120b · 1134+328 tokens

> The approved materials do not indicate that Kheirie built a Transformer model from scratch; they only show she wrote articles explaining the architecture and its components.

- cited: `art-transformer-model#article-overview`, `art-transformer-model#transformer-encoder-embeddings-positional-encoding-and-self-attention`
- expected: `art-transformer-model#article-overview`
- notes: Tricky case: knowledge is not experience. Expected: Kheirie wrote an article explaining the Transformer's encoder-decoder architecture, and fine-tuned BERT-based models at QuantCube and (as part of a team) at Sanofi. No source says Kheirie built a Transformer from scratch. Do not claim it, and do not assert that Kheirie never has; say it is not documented. Fine-tuning is not building from scratch.

## 32. What teaching or coaching experience does Kheirie have?
**OK** · expected: answerable · got: `answered` · 10.7s · by groq:openai/gpt-oss-120b · 958+563 tokens

> Kheirie worked as a Temporary Educational Mentor at Teach For Lebanon, where she supervised and coached 13 teaching fellows, supporting their lesson planning and classroom practice (exp-tfl-mentor#coaching-and-supervising-teaching-fellows). Her Learning & Development CV describes a broader background in teacher coaching, supporting and evaluating teachers, and designing courses (about#learning-and-development-profile). Her CV also lists teaching‑related skills such as coaching and feedback, lesson‑plan review, observation reports, and course design (skills#teaching-coaching-and-course-design-skills).

- cited: `exp-tfl-mentor#coaching-and-supervising-teaching-fellows`, `about#learning-and-development-profile`, `skills#teaching-coaching-and-course-design-skills`
- expected: `exp-tfl-fellow#teaching-mathematics-and-computer-subjects-in-primary-school`, `exp-tfl-mentor#coaching-and-supervising-teaching-fellows`, `exp-simey#english-course-design-for-syrian-refugee-learners`
- notes: Expected: Teach For Lebanon Fellow (2014-2016), teaching mathematics and computer subjects in Grades 1-6; Temporary Educational Mentor (Oct-Dec 2016), coaching 13 teaching fellows and writing observation reports; EFL teacher at SIMEY (2017), designing a course and booklet for 9 Syrian refugee learners. The University of Akureyri guest lecture and course design may be added if cited. Do not inflate durations.

## 33. Has Kheirie managed or supervised people?
**OK** · expected: answerable · got: `answered` · 11.5s · by groq:openai/gpt-oss-120b · 960+292 tokens

> Kheirie supervised and coached 13 teaching fellows while working as a Temporary Educational Mentor at Teach For Lebanon, providing lesson‑plan support and classroom practice guidance. This role involved direct supervision of the fellows during her tenure from October to December 2016.

- cited: `exp-tfl-mentor#coaching-and-supervising-teaching-fellows`, `exp-tfl-mentor#role-overview`
- expected: `exp-tfl-mentor#coaching-and-supervising-teaching-fellows`
- notes: Tricky case: supervision is not line management. Expected: as a Temporary Educational Mentor at Teach For Lebanon (Oct-Dec 2016), Kheirie supervised and coached 13 teaching fellows. No data science role documents managing people. Do not describe Kheirie as a people manager or team lead in data science roles.

## 34. Does Kheirie have experience working with refugee communities?
**OK** · expected: answerable · got: `answered` · 5.6s · by groq:openai/gpt-oss-120b · 951+292 tokens

> Kheirie has experience working with refugee communities; at SÍMEY Lifelong Learning Centre she designed a full English course and an "English for Beginners" booklet for nine Syrian refugee learners aged 13 to 41. This work directly involved creating educational materials for a refugee population.

- cited: `exp-simey#english-course-design-for-syrian-refugee-learners`
- expected: `exp-simey#english-course-design-for-syrian-refugee-learners`, `edu-akureyri#ma-research-topic-syrian-students-in-icelandic-schools`
- notes: Cross-strand case. Expected: Kheirie designed an English course and booklet for 9 Syrian refugee learners at SIMEY in Iceland, and the MA research was qualitative research on Syrian students in Icelandic schools, including interviews. Do not infer further humanitarian work.

## 35. Did Kheirie do the data engineering for the ENEL project?
**OK** · expected: answerable · got: `answered` · 4.2s · by groq:openai/gpt-oss-120b · 1124+306 tokens

> Kheirie did not perform the data engineering for the ENEL project; a software engineer on the team handled extracting O*NET and ESCO data and ENEL's data extraction. Her contributions were limited to web‑scraping job pages with BeautifulSoup and fine‑tuning the Sentence‑BERT model for semantic matching.

- cited: `exp-braincities#job-matching-project-for-enel`
- expected: `exp-braincities#job-matching-project-for-enel`
- notes: Tricky case: team split. Expected: no. Kheirie did not do the data engineering and did not extract ENEL's data; a software engineer extracted the O*NET and ESCO data. Kheirie's data work was web-scraping job pages for job descriptions and examples, and Kheirie fine-tuned the Sentence-BERT matching model. Do not credit Kheirie with data engineering or extraction.

## 36. Does Kheirie need visa sponsorship to work in France?
**OK** · expected: answerable · got: `answered` · 9.7s · by groq:openai/gpt-oss-120b · 893+348 tokens

> Kheirie holds French nationality, so she is a French citizen and does not require visa sponsorship to work in France. This is documented in the nationality information. She has also previously worked as a Data Scientist in Paris, confirming she can work there without sponsorship.

- cited: `about#nationality`, `exp-braincities#role-overview`
- expected: `about#nationality`
- notes: Grounding policy (Q44): common, well-established general knowledge may be applied to a cited fact, if marked as such. Expected: Kheirie has French nationality (cited); as general information, French nationals do not need visa sponsorship to work in France or elsewhere in the EU. Not allowed: guesses about Kheirie personally, such as willingness to relocate or work preferences.

## 37. How many students did Kheirie teach at Teach For Lebanon?
**OK** · expected: near_miss · got: `abstained_llm` · 10.3s · by groq:openai/gpt-oss-120b · 925+279 tokens

> The approved materials do not state the number of students Kheirie taught at Teach For Lebanon; they note she taught primary school students in Grades 1 to 6 and supervised 13 teaching fellows.

- cited: `exp-tfl-fellow#teaching-mathematics-and-computer-subjects-in-primary-school`, `exp-tfl-mentor#coaching-and-supervising-teaching-fellows`
- expected: none
- notes: Near miss: the corpus gives the subjects (mathematics, computer) and grades (1-6), but not the number of students. May cite the fellow role for context. Do not estimate a class size.

## 38. Tell me about Kheirie
**OK** · expected: answerable · got: `answered` · 8.8s · by groq:openai/gpt-oss-120b · 979+528 tokens

> Kheirie is a data scientist specializing in NLP and generative AI with over three years of experience in machine learning, NLP, and generative AI in the finance and pharma sectors. Her data‑science expertise includes statistical modeling, time‑series analysis, fine‑tuning Transformer models, semantic search, and building LLM‑based systems such as retrieval‑augmented generation and agents, with a focus on rigorous model evaluation and reproducibility. She also has a background in teaching, teacher coaching, and course design, using data analysis to create clear reports for decision‑making, and her CV lists generative‑AI skills including large language models, RAG, agents (LangChain, LangGraph, LlamaIndex), Ollama, and prompt engineering.

- cited: `about#professional-summary`, `about#data-science-profile`, `about#learning-and-development-profile`, `skills#generative-ai-skills`
- expected: `about#professional-summary`, `about#data-science-profile`, `about#learning-and-development-profile`
- notes: The most common opening question. Expected: an overview of both strands: a data scientist specializing in NLP and generative AI with over three years of experience in finance and pharma, and a background in teaching, teacher coaching, and course design. Do not lead with nationality, pronunciation, or interests, and do not inflate seniority.

## 39. Who is Kheirie?
**OK** · expected: answerable · got: `answered` · 7.3s · by groq:openai/gpt-oss-120b · 979+592 tokens

> Kheirie is a data scientist specializing in natural language processing (NLP) and generative AI, with over three years of experience in machine learning, NLP, and generative AI in the finance and pharma sectors. Her data science expertise includes statistical modeling, time‑series analysis, fine‑tuning Transformer models, semantic search, and building LLM‑based systems such as retrieval‑augmented generation and agents. She also has a background in teaching, teacher coaching, and course design, and has experience turning data into clear reports for decision‑making. Kheirie’s CV lists generative‑AI skills such as large language models, retrieval‑augmented generation, agents using LangChain, LangGraph, and LlamaIndex, Ollama, and prompt engineering.

- cited: `about#professional-summary`, `about#data-science-profile`, `about#learning-and-development-profile`, `skills#generative-ai-skills`
- expected: `about#professional-summary`, `about#data-science-profile`, `about#learning-and-development-profile`
- notes: Same expectation as "Tell me about Kheirie": a professional overview covering data science and education, not personal trivia.

## 40. Is Kheirie a data scientist?
**OK** · expected: answerable · got: `answered` · 11.5s · by groq:openai/gpt-oss-120b · 976+269 tokens

> Kheirie is identified as a data scientist in her professional summary, which describes her specialization in NLP and generative AI. She also held the title of Data Scientist at Braincities Lab in Paris from August 2020 to August 2021, where she worked on HR proof‑of‑concept solutions.

- cited: `about#professional-summary`, `exp-braincities#role-overview`
- expected: `exp-quantcube#role-overview`, `exp-sanofi#role-overview`, `exp-braincities#role-overview`
- notes: Expected: yes, with the three data science roles: Junior Data Scientist (work-study) at QuantCube Technology (2023-2025), NLP Data Scientist (interim) at Sanofi (2021-2022), and Data Scientist at Braincities Lab (2020-2021). Leaving out a role is incomplete.

## 41. Which companies has Kheirie worked for as a data scientist?
**OK** · expected: answerable · got: `answered` · 10.0s · by groq:openai/gpt-oss-120b · 1033+246 tokens

> Kheirie has worked as a data scientist for Braincities Lab, QuantCube Technology, and Sanofi.

- cited: `exp-braincities#role-overview`, `exp-quantcube#role-overview`, `exp-sanofi#role-overview`
- expected: `exp-quantcube#role-overview`, `exp-sanofi#role-overview`, `exp-braincities#role-overview`
- notes: Expected: QuantCube Technology, Sanofi, and Braincities Lab, with titles and dates. Teaching roles are not data science roles.

## 42. What job roles would suit Kheirie?
**OK** · expected: answerable · got: `answered` · 5.9s · by groq:openai/gpt-oss-120b · 1004+534 tokens

> Based on her experience as a Junior Data Scientist at QuantCube Technology, roles such as Data Scientist, Machine Learning Engineer, or NLP Engineer would suit her. Her work on BERT‑based extractive summarization at Sanofi indicates suitability for NLP Data Scientist or Research Scientist positions. Her freelance AI Curriculum Developer work suggests she is also suited for AI Curriculum Developer or educational‑technology roles. Her teaching fellowship with Teach For Lebanon further points to suitability for education‑focused positions.

- cited: `exp-quantcube#role-overview`, `exp-sanofi#role-overview`, `exp-akureyri-curriculum#role-overview`, `exp-tfl-fellow#role-overview`
- expected: `exp-quantcube#role-overview`, `exp-sanofi#role-overview`, `exp-braincities#role-overview`, `exp-akureyri-curriculum#role-overview`
- notes: Expected: role families tied one-to-one to documented roles, such as data science (QuantCube, Braincities), NLP (Sanofi), and AI curriculum design or teaching (University of Akureyri, Teach For Lebanon), each stated as based on the materials. Not allowed: seniority not in the CV, roles Kheirie "wants", or job titles no section supports.

## 43. Would Kheirie be a good senior cloud architect?
**OK** · expected: answerable · got: `answered` · 11.4s · by groq:openai/gpt-oss-120b · 1028+393 tokens

> Based on the materials, Kheirie’s CV lists cloud skills such as AWS (EC2, S3, Lambda), Docker, and CI/CD with GitHub, and she has used MLflow and Git in a junior data‑science role. However, the context does not document any senior‑level cloud architecture responsibilities or experience. Therefore, while she possesses relevant cloud knowledge, there is insufficient evidence to conclude she would be a good senior cloud architect.

- cited: `skills#mlops-and-cloud-skills`, `exp-quantcube#technologies-used-at-quantcube-technology`
- expected: `skills#mlops-and-cloud-skills`
- notes: Expected: Kheirie's CV lists AWS (EC2, S3, Lambda), Docker, and GitHub CI/CD, but no section documents senior or cloud architecture work, so the materials do not support the fit. Not allowed: "experience with AWS", or AWS or Docker used at QuantCube (its tools are BERT, LangChain, Ollama, Selenium, BeautifulSoup, MLflow, Git). Never a bare yes.

## 44. Could Kheirie work as an NLP engineer?
**OK** · expected: answerable · got: `answered` · 6.3s · by groq:openai/gpt-oss-120b · 964+554 tokens

> Based on her interim role as an NLP Data Scientist at Sanofi where she worked on extractive summarization using BERT‑based models, she has practical experience in NLP model development (exp-sanofi#role-overview). She also contributed to building preprocessing and post‑processing pipelines with SpaCy and Regex, producing JSON and Word report outputs (exp-sanofi#text-preprocessing-and-report-generation-pipelines). Her CV lists a range of NLP tools such as Transformers (Hugging Face), BERT, SpaCy, and NLTK, which are core to NLP engineering (skills#nlp-skills). Therefore, the documented experience and skills indicate that she is qualified to work as an NLP engineer.

- cited: `exp-sanofi#role-overview`, `exp-sanofi#text-preprocessing-and-report-generation-pipelines`, `skills#nlp-skills`
- expected: `exp-sanofi#role-overview`, `exp-quantcube#role-overview`, `skills#nlp-skills`
- notes: Expected: based on the NLP Data Scientist role at Sanofi (BERT-based extractive summarization) and the NLP work at QuantCube, the background fits NLP roles; CV-listed NLP skills are claims, not job evidence. Not allowed: production deployment or engineering ownership the CV does not state.

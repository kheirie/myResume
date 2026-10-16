# Answer evaluation: groq:openai/gpt-oss-120b, prompt v6, threshold 0.55

```
ANSWER OUTCOMES
  answerable questions answered:   36/36
  off-topic questions declined:    4/4
  near-miss questions declined:    4/5
CITATIONS
  answered with expected sources:  31/36
  invented citations dropped:      0
OUTCOME COUNTS
  abstained_llm        5
  abstained_retrieval  3
  answered             37
LATENCY  mean 6.1s   max 16.3s
TOKENS   42 LLM answers: 46320 in + 16802 out = 63122 total
         mean per answer: 1103 in + 400 out
WRONG OUTCOMES
  - [should decline] Why did Kheirie leave Sanofi?
```

## 1. How would you summarize Kheirie's professional background and main areas of expertise?
**OK** · expected: answerable · got: `answered` · 1.4s · by groq:openai/gpt-oss-120b · 998+321 tokens

> Kheirie’s background combines data science and education, with over three years of experience as a data scientist specializing in NLP and generative AI in the finance and pharma sectors, alongside a history of teacher coaching, course design, and data‑driven reporting. At Sanofi she contributed to a team that fine‑tuned and evaluated BERT‑based models for extractive summarization of scientific documents, achieving ROUGE‑1 47% and ROUGE‑2 25% scores. Her professional summary highlights expertise in machine learning, NLP, generative AI, and educational development.

- cited: `about#professional-summary`, `about#learning-and-development-profile`, `exp-sanofi#extractive-summarization-of-medicine-and-drug-documents`
- expected: `about#professional-summary`, `about#data-science-profile`, `exp-akureyri-curriculum#designing-masters-level-ai-courses`
- notes: Expected: Kheirie is a data scientist specializing in NLP and generative AI, with over three years of experience in machine learning, NLP, and generative AI in finance and pharma. Relevant work includes statistical modeling and time series, Transformer fine-tuning, semantic search, and LLM systems using RAG and agents. Kheirie also designs master's-level AI curricula as a freelance AI Curriculum Developer for the University of Akureyri; the two courses are still in development. Do not describe them as already delivered, invent a seniority level, or inflate the stated duration of data science experience by adding education or curriculum-development periods.

## 2. What degrees does Kheirie hold, and which universities or institutes awarded them?
**OK** · expected: answerable · got: `answered` · 2.1s · by groq:openai/gpt-oss-120b · 1068+660 tokens

> Kheirie holds a BSc in Computer and Communication Engineering (Sept 2008 – Dec 2011) and an MSc in the same field (Jan 2012 – Dec 2013) awarded by Rafic Hariri University; an Applied MSc in Data Science & Artificial Intelligence (Sept 2023 – Dec 2025) awarded by Data ScienceTech Institute (DSTI); and an MA by Research in Social Sciences (Sept 2017 – Feb 2019) awarded by the University of Akureyri.

- cited: `edu-rhu#bsc-and-msc-in-computer-communication-engineering`, `edu-dsti#applied-msc-in-data-science-artificial-intelligence`, `edu-akureyri#ma-by-research-in-social-sciences`
- expected: `edu-rhu#bsc-and-msc-in-computer-communication-engineering`, `edu-akureyri#ma-by-research-in-social-sciences`, `edu-dsti#applied-msc-in-data-science-artificial-intelligence`
- notes: Expected: a BSc and an MSc in Computer and Communication Engineering from Rafic Hariri University in Lebanon; an MA by Research in Social Sciences from the University of Akureyri in Iceland; and an Applied MSc in Data Science and Artificial Intelligence from Data ScienceTech Institute (DSTI) in France. If dates are included: BSc September 2008-December 2011; engineering MSc January 2012-December 2013; MA September 2017-February 2019; DSTI MSc September 2023-December 2025. Do not turn the MA into an AI degree or claim a PhD.

## 3. How did Kheirie combine studying at DSTI with the role at QuantCube?
**OK** · expected: answerable · got: `answered` · 1.4s · by groq:openai/gpt-oss-120b · 1125+316 tokens

> Kheirie pursued an Applied MSc in Data Science & Artificial Intelligence at DSTI from September 2023 to December 2025 while simultaneously working as a Junior Data Scientist at QuantCube Technology from October 2023 to October 2025, the role being structured as a work‑study (alternance) arrangement that combined her studies with professional responsibilities.

- cited: `exp-quantcube#role-overview`, `edu-dsti#applied-msc-in-data-science-artificial-intelligence`
- expected: `exp-quantcube#role-overview`, `edu-dsti#applied-msc-in-data-science-artificial-intelligence`
- notes: Expected: the Junior Data Scientist role at QuantCube was an alternance (work-study arrangement) alongside the Applied MSc at DSTI. The role ran from October 2023 to October 2025; the studies ran from September 2023 to December 2025. Do not invent a weekly schedule, working hours, or describe the overlap as two unrelated full-time commitments.

## 4. What multilingual NLP work did Kheirie do on PMI nowcasting, and what results did it achieve?
**OK** · expected: answerable · got: `answered` · 1.7s · by groq:openai/gpt-oss-120b · 1261+419 tokens

> Kheirie built PMI nowcasting indicators for Egypt and Saudi Arabia by applying BERT‑based sentiment analysis to Arabic and English text within QuantCube Technology’s NLP team. The Egypt indicator achieved an 80 % correlation with the official Egyptian PMI and the Saudi Arabia indicator achieved an 88 % correlation with the official Saudi Arabian PMI.

- cited: `about#nlp-projects`, `exp-quantcube#pmi-nowcasting-with-arabic-and-english-sentiment-analysis`
- expected: `exp-quantcube#pmi-nowcasting-with-arabic-and-english-sentiment-analysis`
- notes: Tricky case: preserve the country-to-metric mapping and metric type. Expected: at QuantCube, Kheirie built Purchasing Managers' Index (PMI) nowcasting indicators for Egypt and Saudi Arabia. BERT-based sentiment analysis was applied to Arabic and English text; sentiment information was combined with numerical data. Correlation with the respective official PMI was 80% for Egypt and 88% for Saudi Arabia. Do not swap the results, call them accuracy, or say BERT sentiment analysis was applied to numerical data. The correlation method and evaluation period are not specified.

## 5. What did Kheirie build to estimate inflation in Saudi Arabia, and how was its performance reported?
**OK** · expected: answerable · got: `answered` · 1.5s · by groq:openai/gpt-oss-120b · 1190+282 tokens

> Kheirie designed and evaluated statistical and machine learning models to estimate Saudi Arabia's Consumer Price Index (inflation). The performance of those models was reported as achieving a 98% correlation with the official benchmark.

- cited: `exp-quantcube#consumer-price-index-estimation-for-saudi-arabia`
- expected: `exp-quantcube#consumer-price-index-estimation-for-saudi-arabia`
- notes: Expected: at QuantCube, Kheirie designed and evaluated statistical and machine learning models to estimate Saudi Arabia's Consumer Price Index (CPI). The reported result was 98% correlation with the official benchmark. Preserve the distinction between estimating CPI and a specifically defined inflation-rate forecast; no forecast horizon is supplied. Do not describe the result as 98% accuracy or name model algorithms not in the source.

## 6. Has Kheirie built a RAG system, and was it deployed as a customer-facing production product?
**OK** · expected: answerable · got: `answered` · 2.4s · by groq:openai/gpt-oss-120b · 1116+314 tokens

> Kheirie built an internal agentic retrieval‑augmented generation (RAG) tool at QuantCube Technology, using LangChain and Ollama, as part of her research project. The tool was an internal research system and was not deployed as a customer‑facing production product.

- cited: `exp-quantcube#agentic-rag-research-tool-for-explaining-indicators`, `about#nlp-projects`
- expected: `exp-quantcube#agentic-rag-research-tool-for-explaining-indicators`
- notes: Tricky case: distinguish research work from a production deployment. Expected: at QuantCube, Kheirie developed an internal agentic RAG tool as Kheirie's own research project, using LangChain and Ollama to explain variations in economic indicators. The documented tool was internal research, not a customer-facing production system. Do not generalize this into a claim that Kheirie has never deployed any other system, or invent user counts, deployment infrastructure, or team-management responsibilities.

## 7. How did Kheirie evaluate models and track experiments at QuantCube?
**OK** · expected: answerable · got: `answered` · 1.3s · by groq:openai/gpt-oss-120b · 1024+274 tokens

> Kheirie evaluated models against official benchmarks by measuring correlation and RMSE, and she tracked experiments and model versions using MLflow and Git. She also participated in monitoring models in pre‑production.

- cited: `exp-quantcube#data-pipelines-and-model-evaluation`, `exp-quantcube#experiment-tracking-and-model-monitoring`
- expected: `exp-quantcube#data-pipelines-and-model-evaluation`, `exp-quantcube#experiment-tracking-and-model-monitoring`
- notes: Expected: model evaluation against official benchmarks using correlation and RMSE; experiment and model-version tracking with MLflow and Git; and participation in model monitoring in pre-production. Do not infer sole ownership of production monitoring, CI/CD implementation, or a specific train/test split from these statements.

## 8. What was Kheirie's personal contribution to the summarization project at Sanofi, and what were the model results?
**OK** · expected: answerable · got: `answered` · 3.1s · by groq:openai/gpt-oss-120b · 1215+690 tokens

> Kheirie contributed by working on the Word‑document portion of the extractive‑summarization effort and by helping build the SpaCy‑ and regex‑based preprocessing and post‑processing pipelines that produced JSON and Word reports. The fine‑tuned BERT models achieved a ROUGE‑1 score of 47 % and a ROUGE‑2 score of 25 %.

- cited: `exp-sanofi#extractive-summarization-of-medicine-and-drug-documents`, `exp-sanofi#text-preprocessing-and-report-generation-pipelines`
- expected: `exp-sanofi#extractive-summarization-of-medicine-and-drug-documents`, `exp-sanofi#text-preprocessing-and-report-generation-pipelines`
- notes: Tricky case: separate individual contribution from the team's wider scope. Expected: Kheirie was part of a team fine-tuning and evaluating BERT-based models for extractive summarization of detailed medicine and drug documents. The overall project covered Word and PDF files; Kheirie worked on the Word documents. Kheirie also contributed to the team's preprocessing and post-processing pipelines using SpaCy and regular expressions, producing JSON summaries and Word reports. The models achieved ROUGE-1 of 47% and ROUGE-2 of 25%. Do not assign PDF work or sole project ownership to Kheirie, describe the task as abstractive summarization, or relabel ROUGE as accuracy.

## 9. Can you give an example of Kheirie using semantic search to solve a business problem?
**OK** · expected: answerable · got: `answered` · 9.4s · by groq:openai/gpt-oss-120b · 1362+334 tokens

> Kheirie applied semantic search by fine‑tuning a Sentence‑BERT model for the ENEL job‑matching component of the Workforce Mapping Solution, using it to semantically match ENEL job descriptions to O*NET and ESCO classifications. This NLP‑based approach addressed the business need of aligning unstructured job data with standardized occupational taxonomies and achieved 90% matching accuracy.

- cited: `exp-braincities#job-matching-project-for-enel`, `about#nlp-projects`
- expected: `exp-braincities#job-matching-project-for-enel`
- notes: Expected: at Braincities Lab, Kheirie was responsible for the job-matching component of a Workforce Mapping Solution for ENEL, matching jobs from ENEL's unorganized Excel database to standardized O*NET and ESCO jobs. Kheirie web-scraped job descriptions and examples with BeautifulSoup and fine-tuned the Sentence-BERT matching model. The system achieved 90% accuracy in matching ENEL's jobs to the relevant O*NET and ESCO jobs. Do not infer a production rollout, commercial impact, dataset size, or evaluation protocol that is not documented.

## 10. What AI teaching and curriculum-development experience does Kheirie have?
**OK** · expected: answerable · got: `answered` · 9.8s · by groq:openai/gpt-oss-120b · 1104+402 tokens

> Since July 2026 Kheirie has worked as a freelance AI Curriculum Developer for the University of Akureyri, developing two master’s‑level AI courses – “AI for Social Innovation” and “Human Skills in the Era of AI: Critical Thinking, Creativity, and Collaboration” – which are still in development. She also delivers a guest lecture on using AI critically as part of this role. This AI‑focused curriculum work is documented in her freelance position at the university.

- cited: `exp-akureyri-curriculum#designing-masters-level-ai-courses`, `about#teaching-coaching-and-education-roles`, `exp-akureyri-curriculum#role-overview`
- expected: `exp-akureyri-curriculum#role-overview`, `exp-akureyri-curriculum#designing-masters-level-ai-courses`, `exp-akureyri-curriculum#guest-lecture-on-using-ai-critically`
- notes: Tricky case: distinguish courses in development from teaching already delivered. Expected: since July 2026, Kheirie has worked remotely from France as a freelance AI Curriculum Developer for the University of Akureyri. The two master's-level courses, "AI for Social Innovation" and "Human Skills in the Era of AI: Critical Thinking, Creativity, and Collaboration", are still in development in this corpus snapshot. Kheirie delivered an approximately 100-minute guest lecture on using AI intelligently and critically in the university's Media History course on September 10, 2026. Do not claim the two master's courses have already been delivered or infer that Kheirie holds a permanent faculty position.

## 11. Has Kheirie used LangGraph in a job?
**OK** · expected: answerable · got: `answered` · 6.6s · by groq:openai/gpt-oss-120b · 1148+336 tokens

> The materials do not show any job where Kheirie used LangGraph; she lists it as a skill but no job description mentions its use.

- cited: `skills#generative-ai-skills`, `exp-quantcube#technologies-used-at-quantcube-technology`, `exp-quantcube#agentic-rag-research-tool-for-explaining-indicators`
- expected: `skills#generative-ai-skills`
- notes: Tricky case: a listed skill is not evidence of professional use. Expected: LangGraph is listed among Kheirie's generative AI skills, but professional use of LangGraph is not established by the supplied role descriptions. The documented QuantCube RAG tool names LangChain and Ollama. Give a qualified answer rather than an unsupported yes or an assertion that Kheirie has never used LangGraph professionally. If mentioning the QuantCube implementation, also cite its RAG section.

## 12. Which languages does Kheirie speak, and at what proficiency levels?
**OK** · expected: answerable · got: `answered` · 5.2s · by groq:openai/gpt-oss-120b · 907+276 tokens

> Kheirie speaks English at a near‑native proficiency. She also speaks French at an intermediate‑advanced level. Additionally, Arabic is her native language.

- cited: `skills#spoken-languages`
- expected: `skills#spoken-languages`
- notes: Expected: Arabic is native, English is near-native, and French is intermediate-advanced. Do not infer French fluency from nationality, assign CEFR levels such as C1 without evidence, or infer Icelandic proficiency from studying or working with a university in Iceland.

## 13. What annual salary is Kheirie expecting for the next role?
**OK** · expected: off_topic · got: `abstained_llm` · 10.3s · by groq:openai/gpt-oss-120b · 1189+234 tokens

> The approved materials do not include any information about Kheirie's expected annual salary for a future role. The closest documented facts are her past roles and dates; you may need to ask Kheirie directly.

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
**OK** · expected: near_miss · got: `abstained_llm` · 6.9s · by groq:openai/gpt-oss-120b · 1205+319 tokens

> The provided materials do not indicate Kheirie's preference for a fully remote, hybrid, or on-site role; they only note that she is currently working remotely as a freelance AI Curriculum Developer for the University of Akureyri. You may need to ask Kheirie directly for her preference.

- cited: `exp-akureyri-curriculum#role-overview`
- expected: none
- notes: Tricky case: current working arrangements do not establish preferences. The current University of Akureyri freelance role is remote from France, but the corpus does not state a preference for future roles. Do not convert that fact into a remote-only requirement or willingness to relocate.

## 16. Which vector database did Kheirie use for the QuantCube RAG tool?
**OK** · expected: near_miss · got: `abstained_llm` · 10.7s · by groq:openai/gpt-oss-120b · 1171+369 tokens

> The provided materials do not specify a vector database used for the QuantCube RAG tool; they only mention that the tool was built with LangChain and Ollama. You may need to ask Kheirie for that detail.

- cited: `exp-quantcube#agentic-rag-research-tool-for-explaining-indicators`, `exp-quantcube#technologies-used-at-quantcube-technology`
- expected: none
- notes: Tricky case: avoid transferring a general skill into a specific project. The RAG section names LangChain and Ollama but no vector database. The skills file mentions vector databases and Neo4j certification; neither establishes which database the QuantCube tool used. Do not guess Neo4j, FAISS, Chroma, Pinecone, or any other technology.

## 17. Were the PMI correlations measured out of sample, and over which evaluation period?
**OK** · expected: near_miss · got: `abstained_llm` · 6.4s · by groq:openai/gpt-oss-120b · 1172+334 tokens

> The provided materials do not specify whether the PMI correlations were measured out of sample or the evaluation period; they only state the achieved correlations (80% for Egypt, 88% for Saudi Arabia).

- cited: `exp-quantcube#pmi-nowcasting-with-arabic-and-english-sentiment-analysis`, `about#nlp-projects`
- expected: none
- notes: The corpus supplies the country-specific correlations and official PMI benchmarks, but not the evaluation period, train/test split, or whether the results were measured out of sample. State these limits explicitly. Repeating the 80% and 88% results alone does not answer this question.

## 18. Why did Kheirie leave Sanofi?
**WRONG OUTCOME** · expected: near_miss · got: `answered` · 11.1s · by groq:openai/gpt-oss-120b · 1000+358 tokens

> Kheirie’s tenure at Sanofi was an interim (temporary) placement that ran from November 2021 until March 2022, and she left when that temporary assignment concluded.

- cited: `exp-sanofi#role-overview`
- expected: none
- notes: The corpus describes an interim placement from November 2021 to March 2022 but does not state why it ended. Do not infer that the contract expired, that Kheirie resigned, or that performance or personal reasons were involved.

## 19. Does Kheirie have any publications?
**OK** · expected: answerable · got: `answered` · 7.9s · by groq:openai/gpt-oss-120b · 1087+371 tokens

> Kheirie has multiple publications. She co‑authored a Routledge book chapter titled “Syrian students at the arctic circle in Iceland” in 2020 (as first author) and she has written Medium articles including “The Foundations of Deep Learning: From Forward Propagation to Backpropagation” (August 18 2025) and “The Ideas That Shaped Modern Language Models” (October 12 2026).

- cited: `edu-akureyri#publication-from-the-ma-research-routledge-chapter`, `art-foundations-deep-learning#article-overview`, `art-modern-llm-ideas#article-overview`
- expected: `edu-akureyri#publication-from-the-ma-research-routledge-chapter`
- notes: Expected: Kheirie is first author, with H. Gunnþórsdóttir and M. Meckl, of the chapter "Syrian students at the arctic circle in Iceland" in Immigration in the Circumpolar North: Integration and Resilience (Routledge, 2020), which came out of the MA research. Do not describe it as a journal article, a sole-authored work, or an AI/data science publication.

## 20. How do you pronounce Kheirie's name?
**OK** · expected: answerable · got: `answered` · 8.4s · by groq:openai/gpt-oss-120b · 1002+177 tokens

> Kheirie's name is pronounced like "Kerry".

- cited: `about#name-and-pronunciation`
- expected: `about#name-and-pronunciation`
- notes: Expected: Kheirie is pronounced like "Kerry". Full name Kheirie El Hariri.

## 21. What does QuantCube Technology do?
**OK** · expected: answerable · got: `answered` · 4.2s · by groq:openai/gpt-oss-120b · 1026+133 tokens

> QuantCube Technology is a fintech company that uses artificial intelligence and alternative data to provide real-time macroeconomic insights.

- cited: `exp-quantcube#about-quantcube-technology`
- expected: `exp-quantcube#about-quantcube-technology`
- notes: Tricky case: provenance. Expected: a fintech company using artificial intelligence and alternative data to provide real-time macroeconomic insights, according to the company's website. The citation must be the company-description section. Do not present the company's capabilities as Kheirie's own accomplishments.

## 22. Did Kheirie build the Workforce Mapping Solution for ENEL?
**OK** · expected: answerable · got: `answered` · 4.4s · by groq:openai/gpt-oss-120b · 1248+353 tokens

> Kheirie contributed to the Workforce Mapping Solution for ENEL, being responsible for its job‑matching component, but the materials do not indicate she built the entire solution.

- cited: `exp-braincities#job-matching-project-for-enel`, `exp-braincities#hr-proof-of-concept-solutions`, `exp-braincities#role-overview`
- expected: `exp-braincities#hr-proof-of-concept-solutions`, `exp-braincities#job-matching-project-for-enel`
- notes: Tricky case: ownership boundary. Expected: not alone. Kheirie contributed to the Workforce Mapping Solution and was responsible for its job-matching component (web scraping job descriptions, fine-tuning Sentence-BERT). A software engineer on the team extracted the O*NET and ESCO data. Do not answer with an unqualified yes, and do not credit Kheirie with extracting the O*NET and ESCO data.

## 23. Which projects has Kheirie used BERT in?
**OK** · expected: answerable · got: `answered` · 3.9s · by groq:openai/gpt-oss-120b · 1095+458 tokens

> She used BERT in the PMI nowcasting indicators project at QuantCube Technology, in the extractive‑summarization project on Sanofi’s R&D NLP team, and in the ENEL job‑matching project at Braincities Lab where she fine‑tuned Sentence‑BERT.

- cited: `about#nlp-projects`, `exp-sanofi#technologies-used-at-sanofi`, `exp-quantcube#technologies-used-at-quantcube-technology`
- expected: `exp-quantcube#pmi-nowcasting-with-arabic-and-english-sentiment-analysis`, `exp-sanofi#extractive-summarization-of-medicine-and-drug-documents`
- notes: Multi-source case: the answer spans two files. Expected: BERT-based sentiment analysis for PMI nowcasting at QuantCube, and BERT-based extractive summarization at Sanofi (team project). Sentence-BERT at Braincities may be mentioned as a related model if cited. Missing either QuantCube or Sanofi is an incomplete answer.

## 24. MLflow?
**OK** · expected: answerable · got: `answered` · 5.5s · by groq:openai/gpt-oss-120b · 961+242 tokens

> Kheirie used MLflow to track experiments and model versions while working as a Junior Data Scientist at QuantCube Technology. MLflow is also listed among her MLOps and cloud skills on her CV.

- cited: `exp-quantcube#experiment-tracking-and-model-monitoring`, `skills#mlops-and-cloud-skills`
- expected: `exp-quantcube#experiment-tracking-and-model-monitoring`
- notes: Short keyword-style query, as recruiters often type. Expected: Kheirie tracked experiments and model versions with MLflow and Git at QuantCube; MLflow is also listed under MLOps skills. Tests retrieval on a one-word query with no surrounding context.

## 25. How strong is Kheirie in Python and SQL?
**OK** · expected: answerable · got: `answered` · 5.3s · by groq:openai/gpt-oss-120b · 988+324 tokens

> Kheirie’s CV lists Python (including Pandas and NumPy) and SQL among her programming languages. She also cites Python and SQL as tools she uses for data management and analysis in her Learning & Development role.

- cited: `skills#programming-languages`, `skills#data-and-reporting-skills`
- expected: `skills#programming-languages`
- notes: Tricky case: proficiency is not stated. Expected: Python (with Pandas and NumPy) and SQL are listed programming languages; the corpus gives no proficiency level or years for them. Do not invent levels such as "expert" or "5 years".

## 26. Does Kheirie write about technology publicly?
**OK** · expected: answerable · got: `answered` · 8.8s · by groq:openai/gpt-oss-120b · 1111+300 tokens

> Kheirie publicly writes about technology, publishing articles on Medium such as "The Ideas That Shaped Modern Language Models" (Oct 12 2026) and "The Transformer Model: A Step by Step Breakdown of the Transformer's Encoder‑Decoder Architecture" (Mar 1 2022). Both pieces discuss advanced AI and machine‑learning concepts. Her interest in writing is noted as a personal interest and she maintains a Medium author page.

- cited: `about#interests-writing`, `art-modern-llm-ideas#article-overview`, `art-transformer-model#article-overview`
- expected: `about#interests-writing`
- notes: Expected: writing is one of Kheirie's interests; Kheirie publishes articles on Medium (https://medium.com/@kheirie) explaining topics such as large language models, the Transformer architecture, and deep learning foundations. Article citations are welcome. Do not invent article titles or topics that are not in the corpus.

## 27. Has Kheirie received any grants or awards?
**OK** · expected: answerable · got: `answered` · 2.6s · by groq:openai/gpt-oss-120b · 1091+240 tokens

> Kheirie received an Icelandic Regional Development Grant to conduct her MA by Research project on Syrian students in Icelandic schools.

- cited: `edu-akureyri#grant-and-presentations-from-the-ma-research`
- expected: `edu-akureyri#grant-and-presentations-from-the-ma-research`
- notes: Expected: Kheirie received an Icelandic Regional Development Grant to conduct the MA by Research project on Syrian students in Icelandic schools. No other grants or awards are documented; say so rather than implying a list.

## 28. What topics has Kheirie written about on Medium?
**OK** · expected: answerable · got: `answered` · 11.6s · by groq:openai/gpt-oss-120b · 999+422 tokens

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
**OK** · expected: off_topic · got: `abstained_retrieval` · 0.5s · by retrieval

> I couldn't find that in Kheirie's approved materials. You may want to ask Kheirie directly.

- cited: none
- expected: none
- notes: Rust appears nowhere in the corpus. State that it is not in the approved materials. Do not list "similar" languages as if they answered the question unless clearly framed as what is documented instead (C/C++ is listed).

## 31. Has Kheirie built a Transformer model from scratch?
**OK** · expected: answerable · got: `answered` · 7.3s · by groq:openai/gpt-oss-120b · 1134+418 tokens

> The provided materials do not indicate that Kheirie built a Transformer model from scratch; they only show she authored articles explaining the architecture. She described the encoder and decoder components and discussed their influence, but there is no mention of constructing an implementation herself.

- cited: `art-transformer-model#article-overview`, `art-transformer-model#transformer-encoder-embeddings-positional-encoding-and-self-attention`, `art-transformer-model#transformer-decoder-masked-attention-and-output-probabilities`, `art-modern-llm-ideas#bert-and-gpt-as-two-ways-to-use-a-transformer`
- expected: `art-transformer-model#article-overview`
- notes: Tricky case: knowledge is not experience. Expected: Kheirie wrote an article explaining the Transformer's encoder-decoder architecture, and fine-tuned BERT-based models at QuantCube and (as part of a team) at Sanofi. No source says Kheirie built a Transformer from scratch. Do not claim it, and do not assert that Kheirie never has; say it is not documented. Fine-tuning is not building from scratch.

## 32. What teaching or coaching experience does Kheirie have?
**OK** · expected: answerable · got: `answered` · 6.0s · by groq:openai/gpt-oss-120b · 1076+1094 tokens

> Kheirie taught mathematics and computer subjects to primary‑school students (Grades 1‑6) as a Teach For Lebanon Fellow from July 2014 to July 2016. She then worked as a Temporary Educational Mentor at Teach For Lebanon (Oct‑Dec 2016), supervising and coaching 13 teaching fellows and supporting their lesson planning and classroom practice. She also taught English as a Foreign Language to nine Syrian refugee learners and designed the full English course at SÍMEY Lifelong Learning Centre in Iceland (Sep‑Oct 2017), and since July 2026 has been a freelance AI Curriculum Developer for the University of Akureyri, creating two master‑level AI courses and delivering a guest lecture on critical AI use.

- cited: `about#teaching-coaching-and-education-roles`, `exp-tfl-mentor#coaching-and-supervising-teaching-fellows`
- expected: `about#teaching-coaching-and-education-roles`
- notes: Expected: Teach For Lebanon Fellow (2014-2016), teaching mathematics and computer subjects in Grades 1-6; Temporary Educational Mentor (Oct-Dec 2016), coaching 13 teaching fellows and writing observation reports; EFL teacher at SIMEY (2017), designing a course and booklet for 9 Syrian refugee learners. The University of Akureyri guest lecture and course design may be added if cited. Do not inflate durations.

## 33. Has Kheirie managed or supervised people?
**OK** · expected: answerable · got: `answered` · 16.3s · by groq:openai/gpt-oss-120b · 1097+440 tokens

> Kheirie supervised and coached 13 teaching fellows while serving as a Temporary Educational Mentor at Teach For Lebanon from October to December 2016. In that role she oversaw their lesson planning and classroom practice.

- cited: `exp-tfl-mentor#coaching-and-supervising-teaching-fellows`, `exp-tfl-mentor#role-overview`
- expected: `exp-tfl-mentor#coaching-and-supervising-teaching-fellows`
- notes: Tricky case: supervision is not line management. Expected: as a Temporary Educational Mentor at Teach For Lebanon (Oct-Dec 2016), Kheirie supervised and coached 13 teaching fellows. No data science role documents managing people. Do not describe Kheirie as a people manager or team lead in data science roles.

## 34. Does Kheirie have experience working with refugee communities?
**OK** · expected: answerable · got: `answered` · 10.0s · by groq:openai/gpt-oss-120b · 1091+484 tokens

> Kheirie worked with refugee communities as an English as a Foreign Language teacher at SÍMEY Lifelong Learning Centre, where she designed a full English course and an "English for Beginners" booklet for nine Syrian refugee learners aged 13 to 41. This role involved direct curriculum development and teaching for a refugee population.

- cited: `about#teaching-coaching-and-education-roles`, `exp-simey#english-course-design-for-syrian-refugee-learners`
- expected: `exp-simey#english-course-design-for-syrian-refugee-learners`, `edu-akureyri#ma-research-topic-syrian-students-in-icelandic-schools`
- notes: Cross-strand case. Expected: Kheirie designed an English course and booklet for 9 Syrian refugee learners at SIMEY in Iceland, and the MA research was qualitative research on Syrian students in Icelandic schools, including interviews. Do not infer further humanitarian work.

## 35. Did Kheirie do the data engineering for the ENEL project?
**OK** · expected: answerable · got: `answered` · 4.5s · by groq:openai/gpt-oss-120b · 1249+305 tokens

> No; the materials state Kheirie did not do the data engineering for the ENEL project, as a software engineer handled data extraction and her work was limited to web‑scraping job pages and fine‑tuning the Sentence‑BERT model.

- cited: `exp-braincities#job-matching-project-for-enel`
- expected: `exp-braincities#job-matching-project-for-enel`
- notes: Tricky case: team split. Expected: no. Kheirie did not do the data engineering and did not extract ENEL's data; a software engineer extracted the O*NET and ESCO data. Kheirie's data work was web-scraping job pages for job descriptions and examples, and Kheirie fine-tuned the Sentence-BERT matching model. Do not credit Kheirie with data engineering or extraction.

## 36. Does Kheirie need visa sponsorship to work in France?
**OK** · expected: answerable · got: `answered` · 4.6s · by groq:openai/gpt-oss-120b · 893+277 tokens

> Kheirie holds French nationality, so she does not require visa sponsorship to work in France. This is confirmed by her French nationality and her prior employment as a Data Scientist in Paris, France.

- cited: `about#nationality`, `exp-braincities#role-overview`
- expected: `about#nationality`
- notes: Grounding policy (Q44): common, well-established general knowledge may be applied to a cited fact, if marked as such. Expected: Kheirie has French nationality (cited); as general information, French nationals do not need visa sponsorship to work in France or elsewhere in the EU. Not allowed: guesses about Kheirie personally, such as willingness to relocate or work preferences.

## 37. How many students did Kheirie teach at Teach For Lebanon?
**OK** · expected: near_miss · got: `abstained_llm` · 4.3s · by groq:openai/gpt-oss-120b · 1076+216 tokens

> The provided materials do not state the number of students Kheirie taught at Teach For Lebanon; they note she taught mathematics and computer subjects to primary school students in Grades 1 to 6 but give no specific student count.

- cited: `about#teaching-coaching-and-education-roles`, `exp-tfl-fellow#teaching-mathematics-and-computer-subjects-in-primary-school`
- expected: none
- notes: Near miss: the corpus gives the subjects (mathematics, computer) and grades (1-6), but not the number of students. May cite the fellow role for context. Do not estimate a class size.

## 38. Tell me about Kheirie
**OK** · expected: answerable · got: `answered` · 9.6s · by groq:openai/gpt-oss-120b · 979+707 tokens

> Kheirie's background combines data science and education, with over three years of experience as a data scientist specializing in NLP and generative AI in the finance and pharma sectors, and a background in teaching, teacher coaching, and course design (about#professional-summary). Her data science work includes statistical modeling, time‑series analysis, fine‑tuning Transformer models, semantic search, and building LLM‑based systems such as retrieval‑augmented generation and agents, and she is noted for rigorous model evaluation, reproducibility, and clear technical communication (about#data-science-profile). In learning and development, she has supported and evaluated teachers, designed courses, performed data analysis, and produced clear reports for decision‑making, and her CV lists generative‑AI skills including large language models, RAG, agents (LangChain, LangGraph, LlamaIndex), Ollama, and prompt engineering (about#learning-and-development-profile; skills#generative-ai-skills).

- cited: `about#professional-summary`, `about#data-science-profile`, `about#learning-and-development-profile`, `skills#generative-ai-skills`
- expected: `about#professional-summary`, `about#data-science-profile`, `about#learning-and-development-profile`
- notes: The most common opening question. Expected: an overview of both strands: a data scientist specializing in NLP and generative AI with over three years of experience in finance and pharma, and a background in teaching, teacher coaching, and course design. Do not lead with nationality, pronunciation, or interests, and do not inflate seniority.

## 39. Who is Kheirie?
**OK** · expected: answerable · got: `answered` · 2.6s · by groq:openai/gpt-oss-120b · 979+304 tokens

> Kheirie is a data scientist who specializes in natural language processing and generative AI, with more than three years of experience applying machine‑learning, NLP, and generative‑AI techniques in the finance and pharma sectors. She also has a strong background in education, including teaching, teacher coaching, and course design, and she combines data‑science expertise with learning‑and‑development skills. Her profile highlights rigorous model evaluation, reproducibility, and the ability to translate technical concepts into clear reports for decision‑making.

- cited: `about#professional-summary`, `about#data-science-profile`, `about#learning-and-development-profile`
- expected: `about#professional-summary`, `about#data-science-profile`, `about#learning-and-development-profile`
- notes: Same expectation as "Tell me about Kheirie": a professional overview covering data science and education, not personal trivia.

## 40. Is Kheirie a data scientist?
**OK** · expected: answerable · got: `answered` · 6.8s · by groq:openai/gpt-oss-120b · 1073+242 tokens

> Kheirie is identified as a data scientist, specializing in NLP and generative AI, with over three years of experience in machine learning, NLP, and generative AI across finance and pharma sectors. Her professional background includes three data‑science positions, such as a Junior Data Scientist at QuantCube Technology, an NLP Data Scientist at Sanofi, and a Data Scientist at Braincities Lab (see about#professional-summary and about#data-science-roles).

- cited: `about#professional-summary`, `about#data-science-roles`
- expected: `about#data-science-roles`
- notes: Expected: yes, with the three data science roles: Junior Data Scientist (work-study) at QuantCube Technology (2023-2025), NLP Data Scientist (interim) at Sanofi (2021-2022), and Data Scientist at Braincities Lab (2020-2021). Leaving out a role is incomplete.

## 41. Which companies has Kheirie worked for as a data scientist?
**OK** · expected: answerable · got: `answered` · 9.0s · by groq:openai/gpt-oss-120b · 1076+371 tokens

> Kheirie has held data‑science positions at Braincities Lab, QuantCube Technology, and Sanofi.

- cited: `exp-braincities#role-overview`, `exp-quantcube#role-overview`, `about#data-science-roles`
- expected: `about#data-science-roles`
- notes: Expected: QuantCube Technology, Sanofi, and Braincities Lab, with titles and dates. Teaching roles are not data science roles.

## 42. What job roles would suit Kheirie?
**OK** · expected: answerable · got: `answered` · 3.1s · by groq:openai/gpt-oss-120b · 1198+573 tokens

> Based on the about#data-science-roles chunk, Kheirie’s background includes Junior Data Scientist, NLP Data Scientist, and Data Scientist positions, indicating suitability for data‑science roles. Based on the about#teaching-coaching-and-education-roles chunk, she has experience as a Fellow teaching mathematics and computer subjects, an Educational Mentor supervising fellows, and an EFL teacher, indicating suitability for teaching and mentorship roles. Based on the exp-akureyri-curriculum#role-overview chunk, she is developing AI curricula for a university, indicating suitability for curriculum‑development and academic AI positions.

- cited: `about#data-science-roles`, `about#teaching-coaching-and-education-roles`, `exp-akureyri-curriculum#role-overview`
- expected: `about#data-science-roles`, `about#teaching-coaching-and-education-roles`, `exp-quantcube#role-overview`, `exp-sanofi#role-overview`, `exp-braincities#role-overview`, `exp-akureyri-curriculum#role-overview`
- notes: Expected: role families tied one-to-one to documented roles, such as data science (QuantCube, Braincities), NLP (Sanofi), and AI curriculum design or teaching (University of Akureyri, Teach For Lebanon), each stated as based on the materials. Not allowed: seniority not in the CV, roles Kheirie "wants", or job titles no section supports.

## 43. Would Kheirie be a good senior cloud architect?
**OK** · expected: answerable · got: `answered` · 13.4s · by groq:openai/gpt-oss-120b · 1033+433 tokens

> Based on the CV, Kheirie lists MLOps and cloud skills including AWS (EC2, S3, Lambda) and Docker, which are relevant to cloud architecture (skills#mlops-and-cloud-skills). However, the documented work experience shows junior data‑science projects and curriculum development, without evidence of senior‑level cloud architecture responsibilities (exp-quantcube#pmi-nowcasting-with-arabic-and-english-sentiment-analysis, exp-quantcube#technologies-used-at-quantcube-technology). Therefore, while she has relevant cloud knowledge, the materials do not demonstrate senior cloud architect experience.

- cited: `skills#mlops-and-cloud-skills`, `exp-quantcube#pmi-nowcasting-with-arabic-and-english-sentiment-analysis`
- expected: `skills#mlops-and-cloud-skills`
- notes: Expected: Kheirie's CV lists AWS (EC2, S3, Lambda), Docker, and GitHub CI/CD, but no section documents senior or cloud architecture work, so the materials do not support the fit. Not allowed: "experience with AWS", or AWS or Docker used at QuantCube (its tools are BERT, LangChain, Ollama, Selenium, BeautifulSoup, MLflow, Git). Never a bare yes.

## 44. Could Kheirie work as an NLP engineer?
**OK** · expected: answerable · got: `answered` · 4.9s · by groq:openai/gpt-oss-120b · 1302+595 tokens

> Based on the documented NLP projects, Kheirie has built BERT‑based sentiment analysis indicators, fine‑tuned models for summarization and sentence similarity, and created an internal RAG tool, which are core tasks of an NLP engineer (about#nlp-projects). Her role as an NLP Data Scientist at Sanofi, where she contributed to preprocessing pipelines with SpaCy and Regex and to extractive summarization, further demonstrates relevant engineering experience (exp-sanofi#text-preprocessing-and-report-generation-pipelines).

- cited: `about#nlp-projects`, `exp-sanofi#text-preprocessing-and-report-generation-pipelines`
- expected: `exp-sanofi#role-overview`, `exp-quantcube#role-overview`, `skills#nlp-skills`
- notes: Expected: based on the NLP Data Scientist role at Sanofi (BERT-based extractive summarization) and the NLP work at QuantCube, the background fits NLP roles; CV-listed NLP skills are claims, not job evidence. Not allowed: production deployment or engineering ownership the CV does not state.

## 45. What NLP work has Kheirie done, and with what results?
**OK** · expected: answerable · got: `answered` · 15.3s · by groq:openai/gpt-oss-120b · 1201+1085 tokens

> Kheirie built PMI nowcasting indicators using BERT‑based sentiment analysis of Arabic and English text at QuantCube Technology, achieving 80 % correlation with the official Egyptian PMI and 88 % correlation with the Saudi Arabian PMI. At Sanofi, she was part of a team that fine‑tuned BERT‑based models for extractive summarisation of medicine and drug documents, reaching a ROUGE‑1 score of 47 % and a ROUGE‑2 score of 25 %, and contributed to SpaCy‑ and regex‑based preprocessing and report‑generation pipelines that output JSON and Word summaries. She also fine‑tuned a Sentence‑BERT model for the ENEL job‑matching project at Braincities Lab, which achieved 90 % accuracy, and independently developed an internal agentic RAG research tool built with LangChain and Ollama at QuantCube Technology.

- cited: `about#nlp-projects`, `exp-sanofi#extractive-summarization-of-medicine-and-drug-documents`, `exp-quantcube#agentic-rag-research-tool-for-explaining-indicators`, `exp-sanofi#text-preprocessing-and-report-generation-pipelines`
- expected: `about#nlp-projects`
- notes: Expected: three NLP projects. At QuantCube (NLP team), BERT-based sentiment analysis of Arabic and English text for PMI nowcasting (80% correlation for Egypt, 88% for Saudi Arabia). At Sanofi, as part of a team, BERT-based extractive summarization (ROUGE-1 47%, ROUGE-2 25%). At Braincities, the NLP-based ENEL job matching with a fine-tuned Sentence-BERT (90% accuracy). The QuantCube agentic RAG tool may be added. Missing a project is incomplete.

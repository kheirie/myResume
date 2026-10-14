---
id: art-transformer-model
title: "Article: The Transformer Model"
status: approved
source_type: article
publication: Towards Data Science (Medium)
published: 2022-03-01
url: https://medium.com/data-science/attention-is-all-you-need-e498378552f9
sources:
  - Medium article, https://medium.com/data-science/attention-is-all-you-need-e498378552f9 (text retrieved via Medium RSS, 2026-10-13)
  - Clarifications from Kheirie (2026-10-13)
open_questions: []
---

## Article overview
Kheirie wrote "The Transformer Model: A Step by Step Breakdown of the Transformer's Encoder-Decoder Architecture", published on Medium in Towards Data Science on March 1, 2022. The article examines the architecture introduced in the 2017 paper "Attention Is All You Need" and what makes it powerful. Several figures in the article were created by Kheirie.

## Transformer encoder: embeddings, positional encoding, and self-attention
In the article "The Transformer Model", Kheirie explains the Transformer encoder step by step, using the example of translating "I am a student" into French. It covers tokenization, the embedding layer, positional encoding (needed because the model has no recurrence or convolution), self-attention with query, key, and value vectors, and residual connections with Add & Norm before the feed-forward network.

## Transformer decoder: masked attention and output probabilities
In the article "The Transformer Model", Kheirie explains the Transformer decoder: the components it shares with the encoder, its two inputs, masked multi-head attention that blocks access to later positions, and the final linear and softmax layers that produce word probabilities. The article notes the Transformer's influence on NLP models such as BERT and its growing use in computer vision.

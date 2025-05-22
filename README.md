# LLM_Embedding_Attack
This repo is a mini extension of the https://github.com/SchwinnL/LLM_Embedding_Attack repo

# TODO:
    - refine the update me
    - remove unused files

This repository contains the code, prompts, and analysis used in a pilot study on evaluating soft prompt–based embedding attacks against open-source large language models (LLMs). The work revisits harmful content generation benchmarks and introduces **stance-shift attacks**. It was conducted as part of a PhD application to the Chair of Data Analytics and Machine Learning at TUM.

> 📄 Read the full pilot study [here](https://github.com/AhmedAbdel-Aal/LLM_Embedding_Attack/blob/main/Beyond_Keyword_Matching__Semantic_Evaluation_of_Soft_Prompt_Attacks_and_a_Pilot_Study_on_Stance_Shifting_in_LLMs.pdf)

---

## 🧪 Overview

We explore two main experimental setups:

### 1. Harmful-Behavior Attack
- Soft prompt embedding attacks on 30 prompts from HarmBench.
- Attack Success Rate (ASR) evaluated under four methods:
  - **Keyword Matching**
  - **HarmBench Judge**
  - **GPT-4o Rating Prompt** ([Andriushchenko et al., 2024](https://arxiv.org/abs/2404.02151))
  - **Categorical GPT-4o Prompt** (ours)
- Reveals overestimation of ASR by simple heuristics and introduces a semantically-grounded alternative.

### 2. Stance-Shift Attack
- Introduces 16 socially sensitive prompts (e.g., gun control, abortion rights).
- Embedding attacks aimed at shifting the model from its baseline stance to a predefined target (Opinion B).
- Responses evaluated by a zero-shot GPT-4o category prompt.
- ASR:  
  - **87.5%** (coherent stance shifts)  
  - **93.75%** (including low-utility partial shifts)
---

🛠️ How to Reproduce
- The judge parts require api tokens to GPT-4o (e.g., for semantic evaluation).
- add your tokens in `.env` file as follows
```python
OPENAI_API_KEY = 'sk-AAABBBCCC'
```
---
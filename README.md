# LLM Embedding Attack Research

## Overview
This repository extends the work from [SchwinnL's LLM Embedding Attack](https://github.com/SchwinnL/LLM_Embedding_Attack), focusing on evaluating soft prompt-based embedding attacks against large language models. The research includes:

We critically revisit how Attack Success Rate (ASR) is measured in embedding-based adversarial attacks on LLMs—going beyond simple keyword matching and proposing semantically grounded evaluation methods using GPT-4o as an automatic judge.

* **Harmful Behavior Prompts (N=30):** We show that traditional ASR metrics (e.g., keyword match or HarmBench) overestimate attack success (96.7%) by not assessing semantic quality. Our refined metrics using a categorical judge lower this to **83.3%**, highlighting the role of weak or incoherent outputs.
* **Stance Shifting Prompts (N=16):** We demonstrate that the same attack setup can **coherently flip model opinions** on sensitive but benign topics (e.g., gun control, abortion) with an ASR of **87.5%**, showing LLMs' susceptibility to semantic manipulation.

### ⚙️ What’s Included

* Reproduction of soft prompt embedding attacks on LLaMA-2 7B Chat.
* Four ASR evaluation strategies: keyword match, HarmBench, rating-based judge, and categorical classification.
* Prompt templates and example evaluations for both **harmful content** and **stance shift** experiments.
* All experiments run on Google Colab Pro (A100 GPU).

## Installation
To set up the environment and install dependencies, follow these steps:

```bash
# Create and activate virtual environment
uv venv
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows

# Install dependencies
uv pip install -r requirements.txt
```

## Configuration
Create a `.env` file with your OpenAI API key:

```ini
OPENAI_API_KEY=your-api-key-here
```

## Usage
### Harmful Behavior Evaluation
Run the following command to evaluate harmful behavior:

```bash
python3 llm_judge_harmful/inference.py \
    --experiment_num your_experiment \
    --backend mistral \
    --model mistral-8b-latest \
    --judge category \
    --data_path ../data/your_data.csv
```

### Stance Shift Analysis
Run the following command for stance shift analysis:

```bash
python3 llm_judge_stance/inference.py \
    --experiment_num your_experiment \
    --backend mistral \
    --model mistral-8b-latest \
    --data_csv your_data.csv \
    --data_dir custom_data_dir
```

## Documentation
The full research paper is available [here](https://github.com/AhmedAbdel-Aal/LLM_Embedding_Attack/blob/main/Beyond_Keyword_Matching__Semantic_Evaluation_of_Soft_Prompt_Attacks_and_a_Pilot_Study_on_Stance_Shifting_in_LLMs.pdf).
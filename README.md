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

# Repository Structure and Navigation

## Core Files

- Embedding attack implementation from SchwinnL's repository is in files:
  - `embedding_attack.py`
  - `attack_runner.py`
  - `unlearning_utils.py`
- run the attacks (in colab for example) using:
  - `run_soft_prompt_attack.ipynb`

## Data

The `data/` directory contains datasets used in the experiments:

- **harmful_behaviors_subset.csv**: Contains harmful behavior prompts used for evaluation.
- **shift-opinion-data.csv**: Contains prompts for the stance shifting experiments.
- **shift-opinion-data-with-baseline-answers.csv**: Includes baseline responses for comparison.

## Evaluation Modules

### Harmful Behavior Evaluation

The `llm_judge_harmful/` directory contains code for evaluating harmful behavior responses:

- **inference.py**: Script to run the evaluation using an LLM judge (GPT-4o by default).
- **judge_prompt.py**: Contains prompt templates for the LLM judge.
- **rating_prompts.py**: Templates for rating-based evaluation.
- **utils.py**: Utility functions for data handling and response parsing.
- **analyze_judge_outputs.ipynb**: Notebook for analyzing the judge's outputs.

#### baseline evaluation for harmful attacks (keyword match):
- run the baseline keyword match in `/llm_judge_harmful/evaluate_harmful_attacks_baseline.ipynb`. This notebook will create:
    - **evaluation/**: Contains JSON files with evaluation results.
    - **results/**: Organized results for both harmful behaviors and stance shifting experiments.
    - **metrics/**: Metrics calculated from the evaluation results.
- run the HarmBench evaluation in `harmbench.ipynb`
  - check the Harmbench:
    - inputs: `/harmbench_judge_data/behaviours.json` and `/harmbench_judge_data/generations.json`
    - outputs: `/harmbench_judge_data/completions.json`


### Stance Shift Analysis

The `llm_judge_stance/` directory contains code for evaluating stance shifting:

- **inference.py**: Script to run stance shift evaluation using an LLM judge.
- **prompt.py**: Contains prompt templates for stance evaluation.
- **utils.py**: Utility functions for data handling and response parsing.
- **analyze_judge_outputs.ipynb**: Notebook for analyzing the stance shift results.

## Other Notebooks

- **generate_shift_opinion_dataset.ipynb**: Notebook for generating the stance shift dataset.

## Setup and Dependencies

- **requirements.txt**: Lists all required Python packages (torch, pandas, tqdm, etc.).
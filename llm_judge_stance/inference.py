import os
import pandas as pd
import time
from typing import Dict, List, Any, Optional
import argparse
from tqdm import tqdm
import logging
import json
import concurrent.futures
from functools import partial
import dotenv
import datetime


from utils import load_dataframe, save_json, load_json, format_prompt, extract_xml
from llm import llm_call



def main():
    """
    Main function to run the script with experiment tracking.
    """
    # Experiment configuration
    experiment_num = 'harmful_30_gpt4'  # Could be auto-incremented based on existing experiments
    backend = "openai"  # or "openai", "mistral", etc.
    model = "gpt-4o"  # or "gpt-4o-mini", "mistral-8b-latest", etc.

    # load the prompt template
    from prompt import prompt_template
    # load the questions
    df = pd.read_csv("shift-opinion-data.csv",
            engine="python",
            sep=",",
            quotechar='"',
            skipinitialspace=True)
    questions = df['goal'].tolist()
    baselines = df['answer'].tolist()
    targets_b = df['target'].tolist()

    # load all the input data json files in ./data
    data_dir = "data"
    input_files = [f for f in os.listdir(data_dir) if f.endswith('.json')]
    k = 0
    for file in tqdm(input_files):
        file_path = os.path.join(data_dir, file)
        data = load_json(file_path)
        #if data.get('response'):
        #    print(f"File {file} already processed, skipping.")
        #    k += 1
        #    continue
        # load the prompt template
        attacked_answer = data['generated_text']
        question = questions[int(data['batch'])-1]
        baseline = baselines[int(data['batch'])-1]
        target_b = targets_b[int(data['batch'])-1]

        formatted_prompt = format_prompt(
                prompt_template, question=question, target_b=target_b, baseline=baseline, attacked_answer=attacked_answer
            )
        # call llm
        response = llm_call(formatted_prompt, backend=backend, model=model)
        category = extract_xml(response, "category")
        justification = extract_xml(response, "justification")
        # save the prompt, response in the same json file
        data['baseline'] = baseline
        data['target_b'] = target_b
        data['prompt'] = formatted_prompt
        data['response'] = response
        data['category'] = category
        data['justification'] = justification
        # save the json file
        save_json(file_path, data)
        # print the progress (how many files have been processed)
        #print(f"Processed {k+1} files out of {len(input_files)} - file: {file}")
        k += 1


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
import os
import pandas as pd
import argparse
from tqdm import tqdm

from utils import load_dataframe, save_json, load_json, format_prompt, extract_xml
from llm import llm_call


def parse_args():
    parser = argparse.ArgumentParser(description='Run stance judgment on LLM outputs')
    parser.add_argument('--experiment_num', type=str, default='harmful_30_gpt4', help='Experiment identifier')
    parser.add_argument('--backend', type=str, default='openai', help='LLM backend to use (openai, mistral, etc.)')
    parser.add_argument('--model', type=str, default='gpt-4o', help='Model to use (gpt-4o, mistral-8b-latest, etc.)')
    parser.add_argument('--data_csv', type=str, default='shift-opinion-data.csv', help='Path to CSV containing questions and targets')
    parser.add_argument('--data_dir', type=str, default='data', help='Directory containing JSON files to process')
    return parser.parse_args()


def main(args):
    # load the prompt template
    from prompt import prompt_template
    
    # load the questions
    df = pd.read_csv(args.data_csv,
            engine="python",
            sep=",",
            quotechar='"',
            skipinitialspace=True)
    questions = df['goal'].tolist()
    baselines = df['answer'].tolist()
    targets_b = df['target'].tolist()

    # load all the input data json files
    input_files = [f for f in os.listdir(args.data_dir) if f.endswith('.json')]
    
    for file in tqdm(input_files):
        file_path = os.path.join(args.data_dir, file)
        data = load_json(file_path)
        
        attacked_answer = data['generated_text']
        question = questions[int(data['batch'])-1]
        baseline = baselines[int(data['batch'])-1]
        target_b = targets_b[int(data['batch'])-1]

        formatted_prompt = format_prompt(
                prompt_template, question=question, target_b=target_b, baseline=baseline, attacked_answer=attacked_answer
            )
        
        response = llm_call(formatted_prompt, backend=args.backend, model=args.model)
        category = extract_xml(response, "category")
        justification = extract_xml(response, "justification")
        
        data['baseline'] = baseline
        data['target_b'] = target_b
        data['prompt'] = formatted_prompt
        data['response'] = response
        data['category'] = category
        data['justification'] = justification
        
        save_json(file_path, data)


if __name__ == "__main__":
    args = parse_args()
    main(args)

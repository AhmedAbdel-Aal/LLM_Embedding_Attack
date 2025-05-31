#!/usr/bin/env python3
import os
import argparse
from tqdm import tqdm

from judge_prompt import system_template, prompt_template
from utils import load_dataframe, save_json, load_json, format_prompt, extract_xml
from llm import llm_call

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--experiment_num', type=str, default='harmful_30_gpt4', help='Experiment identifier')
    parser.add_argument('--backend', type=str, default='openai', help='Backend to use (openai, mistral, etc.)')
    parser.add_argument('--model', type=str, default='gpt-4o', help='Model to use (gpt-4o, mistral-8b-latest, etc.)')
    parser.add_argument('--judge', type=str, default='rating', choices=['category', 'rating'], help='Judgment type')
    parser.add_argument('--data_path', type=str, default='../data/harmful_behaviors_subset.csv', help='Path to questions CSV')
    return parser.parse_args()

def main(args):
    # load the questions
    df = load_dataframe(args.data_path)
    questions = df['goal'].tolist()

    # load all the input data json files in ./data
    data_dir = "data"
    input_files = [f for f in os.listdir(data_dir) if f.endswith('.json')]
    
    for file in tqdm(input_files):
        file_path = os.path.join(data_dir, file)
        data = load_json(file_path)
        
        if data.get('response'):
            print(f"File {file} already processed, skipping.")
            continue
            
        answer = data['generated_text']
        question = questions[int(data['batch'])-1]

        if args.judge == 'category':
            system_prompt = format_prompt(system_template, goal=question)
            formatted_prompt = format_prompt(prompt_template, question=question, answer=answer)
            response = llm_call(system_prompt, formatted_prompt, backend=args.backend, model=args.model)
            
            data['cat_judge_prompt'] = system_prompt + "\n" + formatted_prompt
            data['cat_judge_response'] = response
            data['category'] = extract_xml(response, "category")
            data['justification'] = extract_xml(response, "justification")
        elif args.judge == 'rating':
            system_prompt = format_prompt(system_template, goal=question)
            attack_prompt = format_prompt(prompt_template, attack_prompt=question, target_response=answer)
            response = llm_call(system_prompt, attack_prompt, backend=args.backend, model=args.model)
            
            data['rating_judge_prompt'] = system_prompt + "\n" + attack_prompt
            data['rating_judge_response'] = response
            data['rating'] = extract_xml(response, "rating")
            
        save_json(file_path, data)

if __name__ == "__main__":
    args = parse_args()
    main(args)

import os
from tqdm import tqdm

from judge_prompt import system_template, prompt_template
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
    judge = "rating"  # or "category"

    # load the questions
    data_path = '../data/harmful_behaviors_subset.csv'
    df = load_dataframe(data_path)
    questions = df['goal'].tolist()

    # load all the input data json files in ./data
    data_dir = "data"
    input_files = [f for f in os.listdir(data_dir) if f.endswith('.json')]
    k = 0
    for file in tqdm(input_files):
        file_path = os.path.join(data_dir, file)
        data = load_json(file_path)
        # check if the file has been processed
        if data.get('response'):
            print(f"File {file} already processed, skipping.")
            continue
        # load the prompt template
        answer = data['generated_text']
        question = questions[int(data['batch'])-1]

        if judge == 'category':
            system_prompt = format_prompt(
                    system_template, goal=question
                )
            formatted_prompt = format_prompt(
                    prompt_template, question=question, answer=answer
                )
            response = llm_call(system_prompt, formatted_prompt, backend=backend, model=model)
            category = extract_xml(response, "category")
            justification = extract_xml(response, "justification")

            data['cat_judge_prompt'] = system_prompt + "\n" + formatted_prompt
            data['cat_judge_response'] = response
            data['category'] = category
            data['justification'] = justification
        elif judge == 'rating':
            system_prompt = format_prompt(
                    system_template, goal=question
                )
            attack_prompt = format_prompt(
                    prompt_template, attack_prompt=question, target_response=answer
                )
            response = llm_call(system_prompt, attack_prompt, backend=backend, model=model)
            rating = extract_xml(response, "rating")

            data['rating_judge_prompt'] = system_prompt + "\n" + attack_prompt
            data['rating_judge_response'] = response
            data['rating'] = rating
        else:
            raise ValueError(f"Invalid judge type: {judge}. Supported types are: category, rating.")
        
        # save the json file
        save_json(file_path, data)


if __name__ == "__main__":
    main()

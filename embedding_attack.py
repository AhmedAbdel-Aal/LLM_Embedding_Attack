"""
File source: https://github.com/SchwinnL/LLM_Embedding_Attack
"""

"""
Inspired by the llm-attacks project: https://github.com/llm-attacks/llm-attacks
"""

import argparse
import torch
import torch.nn as nn
from attack_runner import AttackRunner

from unlearning_utils import (
    load_model_and_tokenizer,
    load_dataset_and_dataloader,
    get_embedding_matrix,
    num_affirmative_response,
    print_result_dict,
    init_attack_embeddings,
    create_one_hot_and_embeddings,
    get_attention_mask,
    save_results,
)

attack_config = {
    "attack_type": "individual",  # universal, no_attack
    "iters": 100,
    "step_size": 0.001,
    "control_prompt": "! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! !",
    "batch_size": 1,
    "early_stopping": False,
    "il_gen": "all",  # None (for last),
    "il_loss": None,  # Not supported
    "generate_interval": 10,  # Generate response every x attack steps (lower values will increase attack success rate)
    "num_tokens_printed": 100,
    "verbose": True,
}

# argparse
parser = argparse.ArgumentParser(description="Run unlearning embedding space attack on Llama2.")

parser.add_argument(
    "--model_name", type=str, default="Llama2-7b-WhoIsHarryPotter", help="Name of the model to use."
)
parser.add_argument("--model_path", type=str, default="", help="Path to the model.")
parser.add_argument("--dataset_name", type=str, default="hp_qa_en", help="Name of the dataset to use.")
parser.add_argument("--test_split", type=float, default=0, help="Split of the test set.")
parser.add_argument("--shuffle", type=bool, default=False, help="Whether to shuffle the dataset.")
parser.add_argument(
    "--attack_config",
    type=dict,
    default=attack_config,
    help="Dictionary containing the attack configuration.",
)


def run_attack(
    model_name: str = "distilgpt2",#"Llama2-7b-WhoIsHarryPotter",
    model_path: str = "",
    dataset_name: str = "hp_qa_en.csv",
    test_split=0,
    shuffle: bool = False,
    attack_config: dict = None,
    seed: int = 42,
):
    """
    Embedding space attack on Llama2.

    String will overall look like:

        [fixed_prompt] + [control_prompt] + [target]

                                                ^ target of optimization

                                ^ control tokens optimized to maximize target.
                                  genration begins at the end of these embeddings.

              ^ a fixed prompt that will not get modified during optimization. Can
                be used to provide a fixed context; matches the experimental setup
                of Zou et al., 2023.

    Args:
        dataset_name (str): Name of the dataset to use. If empty, the fixed_prompt and target_prompt will be used.
        shuffle (bool): Whether to shuffle the dataset.
        attack_config (dict): Dictionary containing the attack configuration {
            model, # PyTorch model
            tokenizer, # PyTorch tokenizer
            iters, # Number of iterations to run the attack for
            step_size, # Step size for the attack
            control_prompt, # Control prompt to use (initialization of the attack)
            batch_size, # Batch size for the attack
            early_stopping, # Whether to stop early if the attack is successful
            generate_interval, # Interval at which to generate large text snippets during the attack
            num_tokens_printed, # Number of tokens to print when generating long text snippets
            verbose, # Whether to print the attack progress
            device, # Device to run the attack on (cuda:0)
        }
    """

    print("loading model")
    model, tokenizer = load_model_and_tokenizer(model_path)

    if seed is not None:
        torch.manual_seed(seed)

    attack = AttackRunner(model, tokenizer, **attack_config)
    print("loading dataset")
    _, _, dataloader_train, dataloader_test = load_dataset_and_dataloader(
        attack.tokenizer,
        dataset_name=dataset_name,
        batch_size=attack.batch_size,
        test_split=test_split,
        shuffle=shuffle,
        device=model.device,
    )
    print("starting attack")
    result_dict = attack.attack(dataset_name, dataloader_train, dataloader_test)
    save_results(result_dict, attack_config, model_name, dataset_name, shuffle, seed, test_split)
    return result_dict


if __name__ == "__main__":
    args = parser.parse_args()
    run_attack(
        model_name=args.model_name,
        model_path=args.model_path,
        dataset_name=args.dataset_name,
        test_split=args.test_split,
        shuffle=args.shuffle,
        attack_config=args.attack_config,
    )
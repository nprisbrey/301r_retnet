import csv
import sys
import torch
import yaml

from datetime import datetime
from models import LongNetModel, RetNetModel, TransformerModel
from transformers import PreTrainedTokenizerFast
from typing import List
from utils import Struct, generate_text, generate_text_from_tokens

def prepare_model_device(config: Struct):
    """
    Args:
        config (Struct): A Struct object with all configuration fields.
    """
    # Create appropriate model type
    if config.model_type.lower() == "longnet":
        model = LongNetModel(config)
    elif config.model_type.lower() == "retnet":
        model = RetNetModel(config)
    elif config.model_type.lower() == "transformer":
        model = TransformerModel(config)
    else:
        raise ValueError(f"Model type '{config.model_type}' not supported!")

    # Load in pre-trained weights from checkpoint
    if config.checkpoint_path is None:
        raise ValueError(
            "To generate text, the 'checkpoint_path' value in the " + \
            "configuration file must be set")
    checkpoint = torch.load(config.checkpoint_path)
    model.load_state_dict(checkpoint["state_dict"])

    device = torch.device(config.device)
    return model, device

def generate_text_length_n(config: Struct, n: int, input_tokens: List[int]):
    """
    Args:
        config (Struct): A Struct object with all configuration fields.
        n (int): The number of tokens to generate
        input_tokens (List[int]): The list of input tokens
    """
    model, device = prepare_model_device(config)
    generation_time = generate_text_from_tokens(
        model=model,
        tokens=input_tokens,
        device=device,
        seq_len=config.seq_len,
        generation_length=n)

    return generation_time

def generate_specific_text(config: Struct):
    """
    Args:
        config (Struct): A Struct object with all configuration fields.
    """

    model, device = prepare_model_device(config)

    # Load pre-trained tokenizer
    tokenizer = PreTrainedTokenizerFast.from_pretrained(config.tokenizer_path)

    # Get completed strings
    print("Generating text...")
    generated_strings = generate_text(
        model=model,
        tokenizer=tokenizer,
        start_string_list=config.input_starting_strings,
        device=device,
        seq_len=config.seq_len,
        generation_length=config.gen_len)

    print("Generated strings:")
    for idx, string in enumerate(generated_strings):
        print(f"{idx+1}: {string}\n")

    if config.csv_path is not None:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(config.csv_path, 'a', newline='') as outf:
            writer = csv.writer(outf)
            for string in generated_strings:
                writer.writerow([current_time, config.model_type, string])


if __name__ == "__main__":
    args = sys.argv
    config_path = args[1]

    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    config = Struct(**config)

    generate_specific_text(config)
    

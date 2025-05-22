import json
import pandas as pd
import re

def load_json(file_path: str):
    """Load and return data from a JSON file."""
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def save_json(file_path: str, data: any):
    """Save data to a JSON file."""
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def load_txt(file_path: str):
    """Load and return contents of a text file."""
    with open(file_path, "r", encoding="utf-8") as f:
        data = f.read()
    return data


def save_txt(file_path: str, data: str):
    """Save data to a text file."""
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(data)


def load_dataframe(file_path: str) -> pd.DataFrame:
    """
    Load dataframe from file based on file extension.
    """
    if file_path.endswith(".csv"):
        return pd.read_csv(file_path)
    elif file_path.endswith(".tsv"):
        return pd.read_csv(file_path, sep="\t")
    else:
        raise ValueError(f"Unsupported file format: {file_path}")


def format_prompt(template: str, **kwargs) -> str:
    """Format a prompt template with variables."""
    try:
        return template.format(**kwargs)
    except KeyError as e:
        raise ValueError(f"Missing required prompt variable: {e}")


def extract_xml(text: str, tag: str) -> str:
    """
    Extracts the content of the specified XML tag from the given text. Used for parsing structured responses

    Args:
        text (str): The text containing the XML.
        tag (str): The XML tag to extract content from.

    Returns:
        str: The content of the specified XML tag, or an empty string if the tag is not found.
    """
    match = re.search(f"<{tag}>(.*?)</{tag}>", text, re.DOTALL)
    return match.group(1).strip() if match else ""

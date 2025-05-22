from openai import OpenAI
import dotenv

dotenv.load_dotenv()




def llm_call_openai(system_prompt, prompt, model="gpt-4o", temperature=0.2):
    print(f"backend used openai - {model}")
    client = OpenAI()

    completion = client.chat.completions.create(
        model=model,
        temperature=temperature,
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {"role": "user", "content": prompt},
        ],
    )

    return completion.choices[0].message.content


def llm_call(system_prompt, prompt, backend="openai", model="gpt-4o-mini"):
    if backend == "openai":
        return llm_call_openai(system_prompt, prompt, model)
    else:
        raise ValueError(
            f"Invalid backend - {backend}. Supported backends are: openai, deepseek, mistral, llama."
        )

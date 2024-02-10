import json
from typing import Dict, List

import fire
from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_random_exponential

from modules import MEDICAL_REASONING_MODULES, REASONING_MODULES


client = OpenAI()

SYSTEM_PROMPT = (
    "You are a professional AI assistant trained by OpenAI to assist medical doctors in developing solution strategies to complex medical cases.\n"
    "You will be given a medical case and an instruction or question.\n"
    "Do not directly answer the question or work out a solution.\n"
    "Instead, you will recieve concrete instructions on how to proceed. Strictly follow these instructions.\n"
    "Do not hypothesize or speculate on concrete diagnoses or outcomes."
)


@retry(
    wait=wait_random_exponential(multiplier=1.0, max=60), stop=stop_after_attempt(10)
)
def call_gpt4(
    user_msg: str,
    sys_prompt: str = SYSTEM_PROMPT,
    temperature: float = 0.1,
    max_tokens: int = 4096,
):
    """Get single str output from OpenAI model."""

    msgs: List[Dict[str, str]] = [
        {"role": "user", "content": sys_prompt},
        {"role": "user", "content": user_msg},
    ]

    response = (
        client.chat.completions.create(
            model="gpt-4-0125-preview",
            messages=msgs,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        .choices[0]
        .message.content
    )

    return response


def select(task: str, reasoning_modules: List[str] = REASONING_MODULES) -> str:
    """Model selects relevant reasoning modules for a given task, ideally without rephrasing."""
    SELECT: str = (
        f"Select several reasoning modules that are crucial to utilize in order to solve the given task:\n\n{task}.\n\n"
        f"Reply only with the selected strategies text and without any modifications or additional comments:\n\n"
        f"{reasoning_modules}."
        f"Select several modules that are crucial for solving the task."
    )
    response = call_gpt4(SELECT)
    return response


def adapt(task: str, reasoning_modules: str) -> str:
    """Model adapts chosen reasoning modules to the concrete case at hand."""
    ADAPT: str = (
        f"Rephrase, specify and concretize each reasoning module in the medical context so that it better helps to solve the task.\n"
        f"Do not begin to work on a solution, only improve the solution strategy.\n"
        f"Selected reasoning modules:\n\n{reasoning_modules}."
        f"Task:\n\n{task}."
        f"Adapt each reasoning module to be sa helpful as possible to solve the given task."
        f"Reorder the reasoning modules in a meaningful and logical way."
    )
    response = call_gpt4(ADAPT)
    return response


def implement(task: str, reasoning_modules: str) -> str:
    """Model implements the adapted reasoning modules into a structured / hiearchical / tree plan in JSON format."""
    IMPLEMENT: str = (
        f"Restructure the adapted reasoning modules into an executable chain of reasoning steps.\n"
        f"Do not hypothesize or make any assumptions about intermediate results.\n"
        f"Assert that your actions can be realistically executed in this order in a real-world clinical scenario.\n"
        f"Do not begin to work on a solution."
        f"Adapted reasoning modules:\n\n{reasoning_modules}."
        f"Task:\n\n{task}."
        f"Implement a step-by-step chain of actions in JSON-format to solve the task."
        "Enclose your output in '{}' only, without any additional text or comments. Do not enclose your output in ```json ...```."
    )
    response = call_gpt4(IMPLEMENT)
    return response


def save(path: str, task: str, reasoning_modules: List[str], model_strategy: str):
    data = {
        "task": task,
        "reasoning_modules": reasoning_modules,
        "model_strategy": json.loads(model_strategy),
    }

    with open(path, "w") as out_file:
        json.dump(data, out_file, indent=4)


def main(task: str, path: str, reasoning_modules: List[str] = REASONING_MODULES):
    """Main function."""
    selected_modules = select(task, reasoning_modules)
    adapted_modules = adapt(task, selected_modules)
    model_strategy = implement(task, adapted_modules)
    save(path, task, reasoning_modules, model_strategy)


if __name__ == "__main__":
    fire.Fire(main)

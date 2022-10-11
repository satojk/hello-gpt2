import json

from src.openwebtext import OpenWebTextEngine
from src.gpt2 import GPT2Engine

__EXPERIMENT_PATH = './data/experiments/test.json'

def main():
    gpt = GPT2Engine()

    with open(__EXPERIMENT_PATH, 'r') as f:
        experiment = json.load(f)

    for ix, (prompt, answer) in enumerate(experiment):
        len_answer = gpt.tokenize(answer).shape[1]
        output = gpt.generate_text(prompt, num_tokens=len_answer)
        full_answer = prompt + answer
        if output == full_answer:
            print(f'Test case {ix+1} passed.')
        else:
            print(f'Test case {ix+1} failed:\nExpected:{full_answer}\nGot:{output}')


if __name__ == '__main__':
    main()

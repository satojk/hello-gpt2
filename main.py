import os
import json
import pickle

from tqdm import tqdm

from src.openwebtext import OpenWebTextEngine
from src.gpt2 import GPT2Engine, GPT2LMEngine

__EXPERIMENT_PATH = './data/experiments/test.json'
__DOCUMENT_DIR_PATH = './data/testtext'
__OUTPUT_DIR_PATH = './data/testtext_predicted'


def run_experiment(experiment_path: str, gpt: GPT2LMEngine) -> None:
    with open(experiment_path, 'r') as f:
        experiment = json.load(f)

    for ix, (prompt, answer) in enumerate(experiment):
        len_answer = gpt.tokenize(answer).shape[1]
        output = gpt.generate_text(prompt, num_tokens=len_answer)
        full_answer = prompt + answer
        if output == full_answer:
            print(f'Test case {ix+1} passed.')
        else:
            print(f'Test case {ix+1} failed:\nExpected:{full_answer}\nGot:{output}')


def predict_documents(document_dir_path: str, output_dir_path: str, gpt: GPT2LMEngine) -> None:
    for document_filename in tqdm(os.listdir(document_dir_path)):
        with open(os.path.join(document_dir_path, document_filename), 'r') as f:
            document_text = f.read()
        predictions, true_tokens = gpt.predict_document(document_text)
        with open(os.path.join(output_dir_path, document_filename.replace('.txt', '.pkl')), 'wb') as f:
            pickle.dump((predictions, true_tokens), f)


def main():
    gpt = GPT2LMEngine()
    run_experiment(__EXPERIMENT_PATH, gpt)
    predict_documents(__DOCUMENT_DIR_PATH, __OUTPUT_DIR_PATH, gpt)


if __name__ == '__main__':
     main()

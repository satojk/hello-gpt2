import os
import json
import pickle

from tqdm import tqdm

from src.openwebtext import OpenWebTextEngine
from src.gpt2 import GPT2Engine, GPT2LMEngine
from src.analysis import filter_incorrect_predictions

__EXPERIMENT_PATH = './data/experiments/test.json'
__DOCUMENT_DIR_PATH = './data/testtext'
__OUTPUT_DIR_PATH = './data/testtext_predicted'
__COMMON_TOKENS_PATH = './data/common_toks.json'


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


def read_predicted_document(document_path: str, gpt: GPT2LMEngine, ignore_set: iter=[]) -> None:
    with open(document_path, 'r') as f:
        document_text = f.read()
    predictions, true_tokens = gpt.predict_document(document_text, ignore_set=ignore_set)
    correct_predictions = filter_incorrect_predictions(predictions, true_tokens)
    for i in range(correct_predictions.shape[0]):
        print(gpt.detokenize(correct_predictions[i]))
        inp = input('>>>')
        if inp == 'q':
            return


def read_predicted_dir(document_dir_path: str, gpt: GPT2LMEngine, ignore_set: iter=[]) -> None:
    for document_filename in os.listdir(document_dir_path):
        read_predicted_document(os.path.join(document_dir_path, document_filename), gpt, ignore_set)


def main():
    with open(__COMMON_TOKENS_PATH, 'r') as f:
        common_toks = json.load(f)[:30]
    gpt = GPT2LMEngine()
    read_predicted_dir(__DOCUMENT_DIR_PATH, gpt, ignore_set=[tok_id for tok_id, freq in common_toks[:30]])


if __name__ == '__main__':
     main()

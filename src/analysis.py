import pickle

import torch


def load_predictions(predictions_path: str) -> tuple:
    with open(predictions_path, 'rb') as f:
        return pickle.load(f)


def filter_incorrect_predictions(predictions: torch.Tensor, true_tokens: torch.Tensor, ignore_set: iter=[]) -> torch.Tensor:
    correct = predictions[:, -1] == true_tokens[:, 0]
    return predictions[correct]


def filter_predictions_by_token(predictions: torch.Tensor, ignore_set: iter) -> torch.Tensor:
    for token_id in ignore_set:
        predictions = predictions[predictions[:, -1] != token_id]
    return predictions

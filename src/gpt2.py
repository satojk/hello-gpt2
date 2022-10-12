import torch

from transformers import GPT2Tokenizer, GPT2LMHeadModel

GPT2_MAX_SEQ_LEN = 1024

class GPT2Engine(object):

    def __init__(self) -> None:
        self.tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
        self.tokenizer.pad_token = self.tokenizer.eos_token
        self.model = GPT2LMHeadModel.from_pretrained(
                'gpt2',
                pad_token_id=self.tokenizer.eos_token_id,
                temperature=0)
        self.model.eval()


    def tokenize(self, text: str) -> torch.Tensor:
        return self.tokenizer.encode(text, return_tensors='pt')


    def generate_text(self, prompt: str, num_tokens: int=5, num_candidates: int=1) -> list:
        input_token_ids = self.tokenize(prompt)
        if input_token_ids.shape[1] > GPT2_MAX_SEQ_LEN:
            raise Exception('Prompt too long.')

        output_token_ids = self.model.generate(input_ids=input_token_ids,
                                               max_length=len(input_token_ids[0]) + num_tokens,
                                               do_sample=False)
        return self.tokenizer.decode(output_token_ids[0], clean_up_tokenization_spaces=True)


    def predict_document(self, document: str, window_size: int=25) -> tuple:
        '''
        Slide a window of window_size tokens across an entire document. At each
        step, use the window contents as a prompt, and generate a prediction
        for the next token.

        Return a pair of (predictions, true_tokens), where predictions is a
        large 2D tensor where each row is a prediction (window_size tokens from
        the document, followed by a final token generated by GPT2), and
        true_tokens is the transpose of the original document tokenized, minus
        the first window_size tokens (that is, each row consists of a single
        token, namely the true token that GPT2 should have predicted at each
        step).
        '''
        input_token_ids = self.tokenize(document)
        if input_token_ids.shape[1] < window_size - 1:
            raise ValueError('Window contains entire document.')
        prompts = input_token_ids.squeeze(0).unfold(0, window_size, 1)[:-1]
        predictions = self.model.generate(input_ids=prompts,
                                          max_length=window_size+1,
                                          do_sample=False)
        return predictions, input_token_ids[:, window_size:].view(-1, 1)

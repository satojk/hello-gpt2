from transformers import GPT2Tokenizer, GPT2LMHeadModel

GPT2_MAX_SEQ_LEN = 1024

class GPT2Engine(object):

    def __init__(self) -> None:
        self.tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
        self.tokenizer.pad_token = self.tokenizer.eos_token
        self.model = GPT2LMHeadModel.from_pretrained(
                "gpt2", 
                pad_token_id=self.tokenizer.eos_token_id,
                temperature=0)
        self.model.eval()


    def generate_text(self, prompt: str, num_tokens: int=5, num_candidates: int=1) -> list:
        input_token_ids = self.tokenizer.encode(prompt, return_tensors="pt")
        if input_token_ids.shape[1] > GPT2_MAX_SEQ_LEN:
            raise Exception("Prompt too long.")

        output_token_ids = self.model.generate(input_ids=input_token_ids,
                                               max_length=len(input_token_ids[0]) + num_tokens,
                                               do_sample=False)
        return self.tokenizer.decode(output_token_ids[0], clean_up_tokenization_spaces=True)

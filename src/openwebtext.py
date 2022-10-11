import os
import glob
import random

from typing import Generator

OPENWEBTEXT_PATH = 'data/openwebtext'

class OpenWebTextEngine(object):

    def __init__(self) -> None:
        self.openwebtext_path = OPENWEBTEXT_PATH


    def get_random_document_path(self) -> str:
        shard_path_pattern = os.path.join(self.openwebtext_path, 'urlsf_subset*_data')
        random_shard_path = random.choice(glob.glob(shard_path_pattern))
        return os.path.join(random_shard_path, random.choice(os.listdir(random_shard_path)))


    def get_all_document_paths(self) -> Generator[str, None, None]:
        shard_path_pattern = os.path.join(self.openwebtext_path, 'urlsf_subset*_data')
        for shard_path in glob.iglob(shard_path_pattern):
            for document_name in os.listdir(shard_path):
                yield os.path.join(shard_path, document_name)


    def get_document_text(self, document_path: str) -> str:
        with open(document_path, 'r') as f:
            return f.read()

import time

import numpy as np
from jina import Executor, DocumentArray


def generate_text():
    ar = 'abc'
    return ''.join(np.random.choice(list(ar), 10 ** 6))


class TestExecutor(Executor):
    def empty(self, docs: 'DocumentArray', **kwargs):
        return docs

    def add_text(self, docs: 'DocumentArray', **kwargs):
        for doc in docs:
            txt = generate_text()
            doc.text = txt
        return docs

    def pause(self, docs: 'DocumentArray', **kwargs):
        time.sleep(60)
        for doc in docs:
            doc.text = 'none'
        return docs

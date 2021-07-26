import time
from sys import getsizeof

import numpy as np
from jina import Executor, DocumentArray


def generate_text(x):
    chars = ['a', 'b']
    return ''.join(np.random.choice(chars, x * 10 ** 6))


class TestExecutor(Executor):
    def empty(self, docs: 'DocumentArray', **kwargs):
        return docs

    def add_text(self, docs: 'DocumentArray', **kwargs):
        for doc in docs:
            txt = generate_text(int(doc.tags['weight_mb']))
            doc.text = txt
        return docs

    def pause(self, docs: 'DocumentArray', **kwargs):
        delay = int(docs[0].tags['delay'])
        time.sleep(delay)
        for doc in docs:
            doc.text = 'size: {:.2f} Mb'.format(getsizeof(doc.text) / 1024 ** 2)
        return docs

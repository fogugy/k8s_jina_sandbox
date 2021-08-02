import os
import time
from datetime import datetime
from sys import getsizeof

import numpy as np
from jina import Executor, DocumentArray


def ts():
    return datetime.now().strftime("%a %H:%M:%S")


def generate_text(x):
    chars = ['a', 'b']
    return ''.join(np.random.choice(chars, int(x * 10 ** 6)))


def log(docs, pod_name, pre):
    l = f'{ts()} {pod_name} {pre}\n{docs}\n'
    log_path = os.environ.get('LOG_PATH')
    with open(log_path, 'a') as f:
        f.write('*' * 20 + '\n')
        f.write(l)


class TestExecutor(Executor):
    def empty(self, docs: 'DocumentArray', **kwargs):
        return docs

    def add_text(self, docs: 'DocumentArray', **kwargs):
        log(docs, 'POD0', 'IN')
        for doc in docs:
            txt = generate_text(float(doc.tags['weight_mb']))
            doc.text = txt
        delay = int(docs[0].tags['delay_pod0'])
        time.sleep(delay)
        log(docs, 'POD0', 'OUT')

    def pause(self, docs: 'DocumentArray', **kwargs):
        log(docs, 'POD1', 'IN')
        delay = int(docs[0].tags['delay_pod1'])
        time.sleep(delay)
        for doc in docs:
            doc.tags['weight_mb'] = getsizeof(doc.text) / 1024 ** 2
            doc.text = ''
        log(docs, 'POD1', 'OUT')

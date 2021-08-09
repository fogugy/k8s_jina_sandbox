from datetime import datetime
import numpy as np


def log(filename, txt):
    with open(filename, 'a') as f:
        s = ','.join([ts(datetime.now()), txt]) + '\n'
        f.write(s)


def generate_text(x):
    chars = ['a', 'b', 'c', 'd', 'e']
    return ''.join(np.random.choice(chars, x))


def ts(dt):
    return dt.strftime("%H:%M:%S")


if __name__ == '__main__':
    log('test_logs.txt', 'test log')

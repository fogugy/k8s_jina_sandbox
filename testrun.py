from jina import Flow


def test():
    f = Flow.load_config('./executors/flow.yaml')

    with f:
        f.block()


if __name__ == '__main__':
    test()

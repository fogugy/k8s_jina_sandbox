from sys import argv

import requests


headers = {'Content-Type': 'application/json'}


def stress_test(url, n, batch_size):

    for x in range(n):
        d = {"data": []}

        for bi in range(batch_size):
            d["data"].append({"id": f"{x}-{bi}"})

        print(x, 'request', end=' ... ')

        r = requests.post(
            url,
            json=d,
            headers=headers,
        )

        print(r.status_code)


if __name__ == '__main__':
    args = argv[1:]
    url = "http://" + args[0] + "/index"
    n = int(args[1])
    batch_size = int(args[2])

    stress_test(url, n, batch_size)

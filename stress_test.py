import aiohttp
import argparse
import asyncio
from datetime import datetime

headers = {'Content-Type': 'application/json'}


def ts():
    return datetime.now().strftime("%H:%M:%S")


async def stress_test():
    for x in range(n_requests):
        docs = {"data": []}

        for bi in range(batch_size):
            docs["data"].append({
                "id": f"{x}-{bi}",
                "weight_mb": weight,
                "delay": delay
            })

        async with aiohttp.ClientSession() as session:
            print(f'{ts()}', end=' ')
            data = await post_docs(session, url, docs)
            print('to', ts())


async def post_docs(
        session: aiohttp.ClientSession,
        url, docs):
    r = await session.post(
        url,
        json=docs,
        headers=headers,
    )
    return await r.json()


parser = argparse.ArgumentParser()
parser.add_argument('-u', help='host url')
parser.add_argument('-n', help='count of requests')
parser.add_argument('-b', help='batch size')
parser.add_argument('-w', help='weight of single document')
parser.add_argument('-d', help='delay on lask pod')

if __name__ == '__main__':
    args = parser.parse_args()

    url = args.u
    n_requests = int(args.n)
    batch_size = int(args.b)
    weight = float(args.w)
    delay = int(args.d)

    print(
        'n_requests:', n_requests,
        'batch_size:', batch_size,
        'weight:', weight,
        'delay:', delay,
    )

    loop = asyncio.get_event_loop()
    loop.run_until_complete(stress_test())

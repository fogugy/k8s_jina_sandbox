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
                "delay_pod0": delay0,
                "delay_pod1": delay1,
            })

        async with aiohttp.ClientSession() as session:
            print(f'{x}: {ts()}', end=' ')
            data = await post_docs(session, url, docs)
            w = data['data']['docs'][0]['tags']['weight_mb']
            wt = '{:.2f} Mb'.format(w)
            count = len(data['data']['docs'])
            print('to', ts(), f"{wt} x {count}")


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
parser.add_argument('-d0', help='delay on pod 0')
parser.add_argument('-d1', help='delay on pod 1')

if __name__ == '__main__':
    args = parser.parse_args()

    url = args.u
    n_requests = int(args.n)
    batch_size = int(args.b)
    weight = float(args.w)
    delay0 = int(args.d0)
    delay1 = int(args.d1)

    print(
        'n_requests:', n_requests,
        'batch_size:', batch_size,
        'weight:', weight,
        'delay0:', delay0,
        'delay1:', delay1,
    )

    loop = asyncio.get_event_loop()
    loop.run_until_complete(stress_test())

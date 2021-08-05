import argparse
import asyncio
import uuid

import aiohttp
from dateutil import parser as dateparser

from utils import ts, log

headers = {'Content-Type': 'application/json'}


async def test():
    async with aiohttp.ClientSession() as session:
        tasks = []

        for i, x in enumerate(range(n_requests)):
            docs = get_docs_batch()
            tasks.append(post_docs(session, url, docs, delay_query * i))

        responses = await asyncio.gather(*tasks, return_exceptions=True)
        for i, r in enumerate(responses):
            print_response(i, r)


async def post_docs(
        session: aiohttp.ClientSession,
        url,
        docs,
        delay=.0,
):
    await asyncio.sleep(delay)
    r = await session.post(
        url,
        json=docs,
        headers=headers,
    )
    return await r.json()


def get_docs_batch():
    docs = {"data": []}
    id = str(uuid.uuid4())[:4]

    for bi in range(batch_size):
        docs["data"].append({
            "id": id,
            "weight_mb": weight,
            "delay_pod0": delay0,
            "delay_pod1": delay1,
        })

    return docs


def print_response(i, r):
    log('logs.txt', str(r))
    status_ = r.get('status', {}).get('code', 'pass')
    from_ = dateparser.parse(r['routes'][0]['start_time'])
    to_ = dateparser.parse(r['routes'][-2]['end_time'])
    w_ = '{:.2f} Mb'.format(r['data']['docs'][0]['tags']['weight_mb'])
    print(f"{i}: {ts(from_)}, {ts(to_)}\t{status_}\t{w_} x {len(r['data']['docs'])}")


def get_status(r):
    return r['status'].get('code') if r['status'] else 'PASS'


parser = argparse.ArgumentParser()
parser.add_argument('-u', help='host url')
parser.add_argument('-n', help='count of requests')
parser.add_argument('-b', help='batch size')
parser.add_argument('-w', help='weight of single document')
parser.add_argument('-d0', help='delay on pod 0')
parser.add_argument('-d1', help='delay on pod 1')
parser.add_argument('-dl', help='delay between queries')

if __name__ == '__main__':
    args = parser.parse_args()

    url = args.u
    n_requests = int(args.n)
    batch_size = int(args.b)
    weight = float(args.w)
    delay0 = int(args.d0)
    delay1 = int(args.d1)
    delay_query = float(args.dl)

    print(
        'n_requests:', n_requests,
        '\nbatch size:', batch_size,
        '\nweight:', weight,
        '\ndelay pod0:', delay0,
        '\ndelay pod1:', delay1,
        '\ndelay query:', delay_query,
    )

    if delay_query > 0:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(test())
    else:
        asyncio.run(test())

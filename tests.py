import argparse
import asyncio
import uuid

import aiohttp
from dateutil import parser as dateparser

from utils import ts, log

headers = {'Content-Type': 'application/json'}


async def stress_test():
    async with aiohttp.ClientSession() as session:
        tasks = []

        for x in range(n_requests):
            docs = {"data": []}
            id = str(uuid.uuid4())[:8]

            for bi in range(batch_size):
                docs["data"].append({
                    "id": id,
                    "weight_mb": weight,
                    "delay_pod0": delay0,
                    "delay_pod1": delay1,
                })

            tasks.append(post_docs(session, url, docs))

        responses = await asyncio.gather(*tasks, return_exceptions=True)
        for i, r in enumerate(responses):
            log('logs.txt', str(r))
            status_ = r.get('status', {}).get('code', 'pass')
            from_ = dateparser.parse(r['routes'][0]['start_time'])
            to_ = dateparser.parse(r['routes'][-2]['end_time'])
            w_ = '{:.2f} Mb'.format(r['data']['docs'][0]['tags']['weight_mb'])
            print(f"{i}: {ts(from_)}, {ts(to_)}\t{status_}\t{w_} x {len(r['data']['docs'])}")


# drop the base
# check fail loss

def get_status(r):
    s = r.get('status', None)
    return r['status'].get('code') if r['status'] else 'PASS'


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
        '\nbatch_size:', batch_size,
        '\nweight:', weight,
        '\ndelay0:', delay0,
        '\ndelay1:', delay1,
    )

    asyncio.run(stress_test())

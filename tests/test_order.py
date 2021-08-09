import argparse
import asyncio
import uuid

import aiohttp

headers = {'Content-Type': 'application/json'}


async def test():
    async with aiohttp.ClientSession() as session:
        tasks = [req(session, 4), req(session, 1)]
        await asyncio.gather(*tasks, return_exceptions=True)


async def req(session, delay):
    id = str(uuid.uuid4())[:4]
    print('Request', id)
    doc = {
        "id": id,
        "delay_pod0": 0,
        "delay_pod1": delay,
    }
    docs = {"data": [doc]}
    r = await session.post(
        url,
        json=docs,
        headers=headers,
    )
    doc = (await r.json())['data']['docs'][0]
    print('Response', doc['id'])


parser = argparse.ArgumentParser()
parser.add_argument('-u', help='host url')

if __name__ == '__main__':
    args = parser.parse_args()
    url = args.u

    asyncio.run(test())

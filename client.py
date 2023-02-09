import asyncio
import json
import aiohttp
import itertools

def chunked(it,size):
    it = iter(it)
    while True:
        p = dict(itertools.islice(it,size))
        if not p:
            break
        yield p

def generate_client_dict(code,codeSize, ids):
    result = {id:[] for id in ids }
    
    counter = 0
    for i in range(0, len(code), codeSize):
        result[counter].append(code[i:i+codeSize])
        counter+=1

    return result


async def send_code(clients):
    tasks = []

    async with aiohttp.ClientSession() as s:
        for clientId, clientCode in clients.items():
           tasks.append(asyncio.create_task(s.post('http://0.0.0.0:8081/process', json={'clientCode':clientCode, 'clientId':clientId})))

        response = await asyncio.gather(*tasks)
        responseJSON = [await r.json() for r in response]

        return responseJSON
    
async def main():
    print('Loading...')
    clientIds = list(range(0,10000))
    dataset = []

    with open('./podaci.json', encoding='utf-8') as f:
        for line in f:
            d = json.loads(line)
            dataset.append(d['content'])

    clientsWCode = generate_client_dict(dataset[0],int(len(dataset[0])/len(clientIds)+1), clientIds)

    results = await send_code(clientsWCode)
    # for chunk in chunked(clientsWCode.items(), 200):
    #     results = await send_code(chunk)
    #     for r in results:
    #        print(r)


asyncio.run(main())
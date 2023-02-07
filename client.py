import asyncio
import json
import aiohttp
import pandas as pd


def generateClientDict(code,codeSize, ids):
    result = {id:[] for id in ids }
    
    counter = 0
    for i in range(0, len(code), codeSize):
        result[counter].append(code[i:i+codeSize])
        counter+=1


    return result

    
async def main():
    print('Loading...')
    clientIds = list(range(0,10000))
    dataset = []

    with open('./podaci.json', encoding='utf-8') as f:
        for line in f:
            d = json.loads(line)
#            dataset.append({'content':d['content'],'repo_name':d['repo_name'],'path':d['path']})
            dataset.append(d['content'])

    clientsWCode = generateClientDict(dataset,int(len(dataset)/len(clientIds)), clientIds)



asyncio.run(main())
import asyncio
import aiohttp
import sys
import random
import datetime
from aiohttp import web

routes = web.RouteTableDef()

NO_OF_WORKERS = random.randint(5,10)

if len(sys.argv) > 1:
    workerPorts = sys.argv[1:]
else:
    # Ako se master pokrene bez argumenata onda se smatra da su workeri
    # na portovima 8082-8091
    workerPorts = [x for x in range(8082,8082+NO_OF_WORKERS)]


workers ={id:{} for id in workerPorts}

availableWorkers = workerPorts


def chunked(List):
    for i in range(0, len(List), 1000):
        yield List[i:i+1000] 

async def send_to_worker(code):
    tasks = []
    async with aiohttp.ClientSession() as s:
        currentWorker = workerPorts[0]
        for chunk in chunked:
            tasks.append(
                asyncio.create_task(s.get(f"http://0.0.0.0:{currentWorker}", json={'file':chunk}))
            )

            currentWorker = 1 if currentWorker == NO_OF_WORKERS else currentWorker+1
            r = await asyncio.gather(tasks)
            result = [await x.json() for x in r] 
    return result

@routes.post("/process")
async def process(request):
    try:
        req = await request.json()
        clientId = req['clientId']
        clientCode = req['clientCode'][0]
        print(f"Request from client {clientId} at {datetime.datetime.now()}")

        if clientId == 98:
            print(clientCode)
        response = await send_to_worker(clientCode.splitlines())

        return web.json_response({"clientId":clientId,"result":response}, status=200)

    except Exception as e:
        print({'clientId':clientId,'error':str(e)})
    
app = web.Application()
app.router.add_routes(routes)
web.run_app(app, port=8081)
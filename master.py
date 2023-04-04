import asyncio
import aiohttp
import random
import sys
import datetime
from aiohttp import web

routes = web.RouteTableDef()

NO_OF_WORKERS = random.randint(5, 10)

if len(sys.argv) > 1:
    workerPorts = sys.argv[1:]
else:
    # Ako se master pokrene bez argumenata onda se smatra da su workeri
    # na portovima 8082-8091
    workerPorts = [x for x in range(8082, 8082 + NO_OF_WORKERS)]

workers = {x: [] for x in range(NO_OF_WORKERS)}

received_tasks = 0

completed_tasks = 0

print(f"Master running with {NO_OF_WORKERS} workers")


async def split_send(codeString, session):
    splitCode = codeString.splitlines()

    availableWorkers = workerPorts
    responses = []
    tasks = []
    for line in range(0, len(splitCode), 1000):
        if len(availableWorkers) == 0:
            r = await asyncio.gather(tasks)
            responses.append(*[await x.text() for x in r])
            currentWorker = availableWorkers.pop()
            tasks.append(
                asyncio.create_task(
                    session.post(
                        f"http://0.0.0.0:{currentWorker}/worker",
                        json={"file": codeString[line : line + 1000]},
                    )
                )
            )

    return responses


async def send_to_worker(codeList):
    allResponses = []
    async with aiohttp.ClientSession() as s:
        for code in codeList:
            allResponses.append(await split_send(code, s))

    return allResponses


@routes.post("/process")
async def process(request):
    global received_tasks
    global completed_tasks
    received_tasks += 1
    req = await request.json()
    clientId = req["clientId"]
    clientCodes = req["clientCodes"]
    try:
        print(f"Received task from client {clientId} at {datetime.datetime.now()}")

        response = await send_to_worker(clientCodes)

        print(f"Completed task from client {clientId} at {datetime.datetime.now()}")
        completed_tasks += 1
        return web.json_response({"Message": "Success"}, status=200)

    except Exception as e:
        print(f"Client: {clientId}")


app = web.Application()
app.router.add_routes(routes)
web.run_app(app, port=8081)

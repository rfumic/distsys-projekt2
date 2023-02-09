import aiohttp
import asyncio
import random
import re
import sys
from aiohttp import web

PORT = sys.argv[1]
routes = web.RouteTableDef()

def number_of_words(string):
    return len(re.findall(r'\w+',string))

@routes.get('/worker')
async def worker(request):
    await asyncio.sleep(random.uniform(0.1,0.3))
    req = await request.json()
    wordsInFile = number_of_words(req['file'])
    await asyncio.sleep(random.uniform(0.1,0.3))
   
    return web.json_response({'numberOfWords':wordsInFile},status=200)

app = web.Application()
app.router.add_routes(routes)
web.run_app(app, port=PORT)
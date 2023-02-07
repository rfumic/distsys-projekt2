import asyncio
import aiohttp
from aiohttp import web

routes = web.RouteTableDef()

@routes.post("/process")
async def process(request):
    try:
        req = await request.json()
        return web.json_response({"clientId":req['clientId'],"response":'hello world'})

    except Exception as e:
        print(str(e))
    
app = web.Application()
app.router.add_routes(routes)
web.run_app(app, port=8081)
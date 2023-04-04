import asyncio
import json
import aiohttp


def generate_client_dict(dataset):
    result = {}
    currentId = 0
    currentClientCodes = []

    for code in dataset:
        currentClientCodes.append(code)

        if len(currentClientCodes) == 10:
            result[currentId] = currentClientCodes
            currentClientCodes = []
            currentId += 1

    return result


async def send_code(clients):
    tasks = []

    async with aiohttp.ClientSession() as s:
        for id in clients:
            tasks.append(
                asyncio.create_task(
                    s.post(
                        "http://0.0.0.0:8081/process",
                        json={"clientId": id, "clientCodes": clients[id]},
                    )
                )
            )

        response = await asyncio.gather(*tasks)
        responseParsed = [await r.text() for r in response]

        return responseParsed


def avg_num_letters(codeArray):
    sum_of_lengths = 0

    for code in codeArray:
        sum_of_lengths += len("".join(code.split()))

    return sum_of_lengths / len(codeArray)


async def main():
    print("Loading...")
    dataset = []

    with open("./podaci.json", encoding="utf-8") as f:
        for line in f:
            d = json.loads(line)
            dataset.append(d["content"])

    clientsWCode = generate_client_dict(dataset)

    for client in clientsWCode.keys():
        print(
            f"Client {client} on average has {avg_num_letters(clientsWCode[client])} letters."
        )

    response = await send_code(clientsWCode)


asyncio.run(main())

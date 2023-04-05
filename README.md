# Raspodijeljeni Sustavi - Projekt 2

## Setup

1. Instalirati pakete:

```sh
pip install aiohttp
```

2. [Fake dataset JSON datoteka](https://huggingface.co/datasets/codeparrot/codeparrot-clean/resolve/main/file-000000000040.json.gz) (1 GB) mora biti `./podaci.json`

3. Pokrenuti 10 workera. Prvi argument je port workera.

```sh
python worker.py 8082
python worker.py 8083
.
.
.
python worker.py 8091
```

4. Pokrenuti master servis. Ako workeri nisu na portovima 8082-8091 predati portove kao argumente.

```sh
python master.py [PORT1] [PORT2]... [PORT10]
```

5. Pokrenuti klijenta

```sh
python client.py
```

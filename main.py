
import config
import node


from fastapi import FastAPI, Response
import json


codes = {
    config.HttpStatus.ok: 200,
    config.HttpStatus.not_found: 404,
    config.HttpStatus.internal_error: 500,
    config.HttpStatus.forbidden: 403,
}


app = FastAPI()
config = config.Config(node_id="node_1", node_type="type_1")
backend = node.Backend(config)


@app.get("/")
async def read_root():
    status, code = backend.get_status()
    return Response(content=json.dumps(status), status_code=codes[code]) 


@app.get("/command/start/{pwd}")
async def start_command(pwd: str):
    status, code = backend.command(config.Commands.start, pwd)
    return Response(content=status, status_code=codes[code])


@app.get("/command/stop/{pwd}")
async def stop_command(pwd: str):
    status, code = backend.command(config.Commands.stop, pwd)
    return Response(content=status, status_code=codes[code])


@app.get("/command/train/{pwd}")
async def train_command(pwd: str):
    status, code = backend.command(config.Commands.train, pwd)
    return Response(content=status, status_code=codes[code])
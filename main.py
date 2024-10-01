from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect, Depends
from pydantic import BaseModel
import uvicorn
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

from src.service.mistral import get_mistral_client

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")


class TextRequest(BaseModel):
    text: str


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.websocket('/ws')
async def fetch_data(
        websocket: WebSocket,
        client=Depends(get_mistral_client),
):
    await websocket.accept()
    try:
        while True:
            text = await websocket.receive_text()

            async for chunk in client.chat_ai(text):
                await websocket.send_text(chunk)
    except WebSocketDisconnect:
        pass


if __name__ == "__main__":
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8882,
    )
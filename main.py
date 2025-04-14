from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

chat = ChatOpenAI(model="gpt-4", temperature=0.7)

@app.get("/", response_class=HTMLResponse)
async def get_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/get-advice")
async def get_advice(request: Request):
    data = await request.json()
    devices = data.get("devices", [])

    if not devices:
        return JSONResponse(content={"message": "No devices provided."}, status_code=400)

    usage_description = "\n".join(
        f"{d['name']} ({d['category']}) - {d['watts']}W for {d['hours']} hrs/day"
        for d in devices
    )

    prompt = f"""Here is a list of home appliances and their daily usage:\n{usage_description}\n\nGive simple, actionable advice to reduce electricity usage based on this data. Be friendly and helpful."""

    messages = [
        SystemMessage(content="You are a helpful energy advisor."),
        HumanMessage(content=prompt)
    ]

    response = chat(messages)
    return {"message": response.content}

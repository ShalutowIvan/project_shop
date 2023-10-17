from fastapi import FastAPI
from fastapi.responses import FileResponse

#ссылка на курс по постману
#https://stepik.org/lesson/741960/step/1?unit=743634

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}



@app.get("/index")
async def index():
    return FileResponse("index.html")
    


@app.get("/calculate/")
async def calculate(num1: int, num2: int):
    res = num1 + num2

    return {"result": res}


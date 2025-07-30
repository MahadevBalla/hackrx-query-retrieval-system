from fastapi import FastAPI, Response
from app.routes import router

app = FastAPI()
app.include_router(router)


@app.get("/")
async def root():
    return {"message": "running..."}


@app.get("/favicon.ico")
async def favicon():
    return Response(status_code=204)

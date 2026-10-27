from fastapi import FastAPI, Request

app = FastAPI()


@app.middleware("http")
async def my_middleware(request: Request, call_next):

    # Runs BEFORE endpoint
    print("Request received:", request.url)

    # Send request to actual endpoint
    response = await call_next(request)

    # Runs AFTER endpoint
    print("Response status:", response.status_code)

    return response


@app.get("/hello")
async def hello():
    return {"message": "Hello"}
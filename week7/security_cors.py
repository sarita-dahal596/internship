# Import FastAPI
from fastapi import FastAPI, Header, HTTPException

# Import CORS Middleware
from fastapi.middleware.cors import CORSMiddleware



# CREATE FASTAPI APPLICATION


app = FastAPI(
    title="API Security and CORS Example"
)



# CORS


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,

    # Frontends that are allowed to access this API
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:4200"
    ],

    # Allow cookies / authorization information
    allow_credentials=True,

    # Allow GET, POST, PUT, DELETE, etc.
    allow_methods=["*"],

    # Allow request headers
    allow_headers=["*"]
)



# HOME ENDPOINT


@app.get("/")
async def home():

    return {
        "message": "Secure API is running"
    }



# PROTECTED ENDPOINT


@app.get("/protected")
async def protected_route(
    x_api_key: str = Header()
):

    # Correct API key
    correct_api_key = "my-secret-key"

    # Check API key
    if x_api_key != correct_api_key:

        raise HTTPException(
            status_code=401,
            detail="Invalid API key"
        )

    # If API key is correct
    return {
        "message": "You can access this protected API"
    }
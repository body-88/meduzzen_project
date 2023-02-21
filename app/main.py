from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

app = FastAPI()


origins = [
    "http://localhost",
    "http://localhost:8080",
    "https://localhost",
    "https://localhost:8080",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def health_check():
    return {
    "status_code": 200,
    "detail": "ok",
    "result": "working"
}



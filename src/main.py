from fastapi import FastAPI

app = FastAPI(title="To-Do-App", version="0.0.1", openapi_url="/openapi.json")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
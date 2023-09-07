import uvicorn

if __name__ == "__main__":
    uvicorn.run(app="src.app:app", port=8080, host="0.0.0.0", reload=True, workers=1)

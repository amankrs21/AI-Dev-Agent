"""
PLEASE NOTE: This file is the entry point for running the server.
It sets up and starts the server using Uvicorn.
Don't use this file in the Production environment.
Use a proper ASGI server setup for production deployments.
"""
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("src.app:app", host="127.0.0.1", port=8000, log_level="info", reload=True)

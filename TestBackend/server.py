import os
import sys
import time

import uvicorn
from fastapi import FastAPI

# Read port from command line
if len(sys.argv) < 2:
    print("Usage: python server.py <port>")
    sys.exit(1)

port = sys.argv[1]
os.environ["APP_PORT"] = port

# FastAPI app
app = FastAPI()


@app.get("/")
def root():
    from time import sleep
    temp = time.time_ns()
    print(f"ping {port} start {time.time_ns()}")
    sleep(0.5)
    temp1 = time.time_ns()
    print(f"ping {port} end {temp1}")
    print((temp1 - temp )/ 1e9)

    return {"port": os.environ["APP_PORT"]}


# If main, run uvicorn with reload
if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=int(port), reload=True)

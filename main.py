import os
import uvicorn
import requests
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Shadowlink bot is running"}

@app.post("/yl")
async def yl_handler(request: Request):
    data = await request.json()
    url = data.get("url")

    if not url or "shadowlink" not in url:
        return JSONResponse(content={"error": "Invalid or missing Shadowlink URL"}, status_code=400)

    try:
        response = requests.get(url)
        response.raise_for_status()
        json_data = response.json()

        download = json_data.get("data", {}).get("download")
        title = json_data.get("data", {}).get("title")
        thumbnail = json_data.get("data", {}).get("thumbnail")

        if not download or not download.endswith(".mkv"):
            return JSONResponse(content={"error": "MKV file not found"}, status_code=404)

        return JSONResponse(content={
            "title": title,
            "thumbnail": thumbnail,
            "download": download
        })
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)

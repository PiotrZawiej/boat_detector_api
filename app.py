from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import shutil
import os
from boat_detector import boat_detector
import tempfile
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

app = FastAPI()

app.mount("/static", StaticFiles(directory="frontend"), name="static")


UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/", response_class=HTMLResponse)
def get_index():
    with open("frontend/index.html", encoding="utf-8") as f:
        return f.read()

@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name

        output_path = os.path.join(UPLOAD_DIR, "detected_boat.jpg")

        boat_detector(
            model_path=r"runs\weights\best.pt",
            photo_path=tmp_path,
            output_path=output_path
        )

        os.remove(tmp_path)

        return {
            "message": "Detection completed",
            "detected_image_url": "/image/detected_boat.jpg"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Detection failed: {str(e)}")

@app.get("/image/{filename}")
def get_image(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Image not found")
    return FileResponse(file_path, media_type="image/jpeg")

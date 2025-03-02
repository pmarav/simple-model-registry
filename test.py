from fastapi import FastAPI, File, UploadFile, Form, HTTPException
import os
import shutil

app = FastAPI()
UPLOAD_FOLDER = "models"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.post("/models")
async def upload_model(
    file: UploadFile = File(...),
    name: str = Form(...),
    version: str = Form(...),
    accuracy: float = Form(...)
):
    if not file.filename.endswith(".pkl"):
        raise HTTPException(status_code=400, detail="Only .pkl files are allowed")
    
    filename = f"{name}_v{version}.pkl"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    
    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    return {"message": "Model uploaded successfully", "model": {"name": name, "version": version, "accuracy": accuracy, "filepath": filepath}}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
